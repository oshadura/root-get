""" root_get script """

import sys
import os
import glob
import subprocess
import json
import re
from difflib import get_close_matches
from pathlib2 import Path
from os.path import expanduser
import yaml

# FIXME: We need to be in root-get home dir before calling this script
sys.path.append(os.getcwd())

# Import classes from root-get directories
from coreutils.package_manager import PackageManager
from resolver.db_resolver import *
from resolver.dag_resolver import *
from downloader.download_request import *
from analyzer.path_checker import *
from analyzer.namelist import *
from integrator.install_module import *
from integrator.install_module_ninja import *
from analyzer.utilities import check_env


# Enviroment variables
HOME = expanduser("~")
ROOT_PKG_CACHE = os.environ["ROOT_PKG_CACHE"]
print("[root-get] root-get cache: {0:s}".format(ROOT_PKG_CACHE))
#
ROOT_SOURCES = os.environ['ROOT_SOURCES']
if  ROOT_SOURCES.endswith(os.sep):
    ROOT_SOURCES = ROOT_SOURCES[:-1]
print("[root-get] ROOT sources: {0:s}".format(ROOT_SOURCES))
#
PKG_PATH = os.environ['ROOT_PKG_PATH']
print("[root-get] ROOT packages installation path: {0:s}".format(PKG_PATH))
#
PWD_PATH = os.getcwd()
print('[root-get] root-get location: {0:s}'.format(PWD_PATH))
#
ROOT_MODULES = os.environ['ROOT_MODULES']
print('[root-get] ROOT modules location: {0:s}'.format(ROOT_MODULES))


def resolver_dependencies_for_package(pkg, db_manifest):
    print("[root-get] DEBUG: Resolving dependencies without DAG: direct strategy")
    try:
        if db_manifest[pkg]["deps"] is not None:
            for dep in db_manifest[pkg]["deps"]:
                print("[root-get] Installing dependency " + dep)
                if not install_dep_pkg(dep, db_manifest):
                    return False
                else:
                    print("[root-get] Dependency {0:s} is sucessfully installed and deployed".format(dep))
        else:
            print("[root-get] No dependencies for {0:s} ".format(pkg))
    except:
        pass


def resolver_dependencies_for_module(module, db_manifest):
    print("[root-get] DEBUG: Resolving dependencies without DAG: direct strategy")
    try:
        if db_manifest[module]["deps"] is not None:
            for dep in db_manifest[module]["deps"]:
                print("[root-get] Installing dependency " + dep)
                if not install_dep_module(dep, db_manifest):
                    return False
                else:
                    print("[root-get] Dependency {0:s} is sucessfully installed and deployed".format(dep))
        else:
            print("[root-get] No dependencies for {0:s} ".format(module))
    except:
        pass


def install_dep_module(module, db_manifest, pm_instance):
    """ Main installation routine only for dependency modules"""
# Checkout packages if we have them in ROOT
    src_path = pm_instance.check_module_path(module, PWD_PATH)
# Analyzing packages: generation of package/module CMakeFile.txt,
    pm_instance.analizer_package(module, src_path)
# Building DB
    db_manifest = pm_instance.generation_db_modules()
# Print DB
    pm_instance.print_db_manifest(db_manifest)
# Generating DB instance for dag
    dag_manifest = pm_instance.dag_pre_generation(db_manifest)
# WIP: Still not working
    pm_instance.generation_lock_file_from_dag(dag_manifest)
# Parcing packages in db_manifest
    #parced_db_manifest = parser_db_manifest(db_manifest, PKG_PATH)
# Resolving dependecies without DAG
#FIXME: should be pm_instance.get_db()
    resolver_dependencies_for_module(module, db_manifest)
# Before buiding we need to check if pkg is really in the Db
    pm_instance.check_pkg_db(module, db_manifest)
# Check if package is installed
    if pm_instance.check_install_pkg_db(module, db_manifest):
        return True
# Trigger trigger_dependencies_pkg_db
    #trigger_dependency_pkg_db(pkg, db_manifest)
# Buiding modules
    else:
        pm_instance.build_package(module, db_manifest)
# Preparing modules
        pm_instance.prepare_package(module)
# Installing modules
        pm_instance.deploy_pkg(module)
####################
    db_manifest[module]["installed"] = True
    return True
#########################################################

def install_separate_module(module):
    """ Installation routine for ROOT modules.
        Depricated mode, used for testing only!"""
    PM = PackageManager()
# Checkout packages if we have them in ROOT
    src_path = PM.check_module_path(module, PWD_PATH)
# Analyzing packages: generation of package/module CMakeFile.txt,
    PM.analizer_package(module, src_path)
# Building DB
    db_manifest = PM.generation_db_modules()
# Print DB
    PM.print_db_manifest(db_manifest)
# Generating DB instance for dag
    dag_manifest = PM.dag_pre_generation(db_manifest)
# WIP: Still not working
    PM.generation_lock_file_from_dag(dag_manifest)
# Parcing packages in db_manifest
    parced_db_manifest = PM.parser_db_manifest(db_manifest, PKG_PATH)
# Resolving dependecies without DAG
    resolver_dependencies_for_module(module, parced_db_manifest)
# Adopting name of package according generated DB
# We are rewriting name of package!
    module = PM.naming_checker(module)
# Before buiding we need to check if module is really in the Db
    PM.check_module_db(module, parced_db_manifest)
# Check if package is installed
    if PM.check_module_db(module, parced_db_manifest):
        return True
    else:
# Trigger trigger_dependencies_module_db
    #trigger_dependency_module_db(module, parced_db_manifest)
# Clean build directory
        PM.clean_build(module, parced_db_manifest)
# Reruning CMake
        PM.rerun_configuration(module)
# Buiding packages
        PM.build_package(module, parced_db_manifest)
# Preparing packages
        PM.prepare_package(module)
# Installing packages
        deploy_value = PM.deploy_module(module)
####################
    try:
        db_manifest[module]["installed"] = True
    except:
        pass
    return deploy_value, True
#########################################################

def install_dep_pkg(pkg, db_manifest, pm_instance):
    """ Installation routine for dependency packages"""
# Checkout packages if we have them in ROOT
    src_path = pm_instance.check_module_path(pkg, PWD_PATH)
# Analyzing packages: generation of package/module CMakeFile.txt,
    pm_instance.analizer_package(pkg, src_path)
# Building DB
    db_manifest = pm_instance.generation_db_modules()
# Print DB
    pm_instance.print_db_manifest(db_manifest)
# Generating DB instance for dag
    dag_manifest = pm_instance.dag_pre_generation(db_manifest)
# WIP: Still not working
    pm_instance.generation_lock_file_from_dag(dag_manifest)
# Parcing packages in db_manifest
    #parced_db_manifest = parser_db_manifest(db_manifest, PKG_PATH)
# Resolving dependecies without DAG
    resolver_dependencies_for_package(pkg, db_manifest)
# Before buiding we need to check if pkg is really in the Db
    pm_instance.check_pkg_db(pkg, db_manifest)
# Check if package is installed
    if pm_instance.check_install_pkg_db(pkg, db_manifest):
        return True
# Trigger trigger_dependencies_pkg_db
    #trigger_dependency_pkg_db(pkg, db_manifest)
# Buiding packages
    else:
        pm_instance.build_package(pkg, db_manifest)
# Preparing packages
        pm_instance.prepare_package(pkg)
# Installing packages
        pm_instance.deploy_pkg(pkg)
####################
    db_manifest[pkg]["installed"] = True
    return True
#########################################################

def install_pkg(pkg):
    """ Main installation routine for main package"""
    PM = PackageManager()
# Checkout packages if we have them in ROOT
    src_path = PM.check_module_path(pkg, PWD_PATH)
# Analyzing packages: generation of package/module CMakeFile.txt,
    PM.analizer_package(pkg, src_path)
# Building DB
    db_manifest = PM.generation_db_modules()
# Print DB
    PM.print_db_manifest(db_manifest)
# Generating DB instance for dag
    dag_manifest = PM.dag_pre_generation(db_manifest)
# WIP: Still not working
    PM.generation_lock_file_from_dag(dag_manifest)
# Parcing packages in db_manifest
    parced_db_manifest = PM.parser_db_manifest(db_manifest, PKG_PATH)
# Resolving dependecies without DAG
    resolver_dependencies_for_package(pkg, parced_db_manifest)
# Adopting name of package according generated DB
# We are rewriting name of package!
    pkg = PM.naming_checker(pkg)
# Before buiding we need to check if pkg is really in the Db
    PM.check_pkg_db(pkg, parced_db_manifest)
# Check if package is installed
    if PM.check_install_pkg_db(pkg, parced_db_manifest):
        return True
    else:
# Trigger trigger_dependencies_pkg_db
    #trigger_dependency_pkg_db(pkg, parced_db_manifest)
# Clean build directory
        PM.clean_build(pkg, parced_db_manifest)
# Reruning CMake
        PM.rerun_configuration(pkg)
# Buiding packages
        PM.build_package(pkg, parced_db_manifest)
# Preparing packages
        PM.prepare_package(pkg)
# Installing packages
        deploy_val = PM.deploy_pkg(pkg)
####################
    try:
        db_manifest[pkg]["installed"] = True
    except:
        pass
    return deploy_val, True
#########################################################

def module_install(args):
    if not install_separate_module(args[0]):
        exit(1)

#########################################################

def do_pkg_install(arg):
    """
    """
    deploy_val = install_pkg(arg)
    if deploy_val != "deployed":
        return "failed"

#########################################################
def do_list(args):
    """
    """
    cache_dir = os.environ['ROOT_PKG_CACHE']
    if not os.path.exists(ROOT_PKG_CACHE + args[0]):
        print("Package not installed yet. Please check installation.")
    else:
        db = DBResolver()
        db_manifest = db.generated_manifest()
        print("Installed modules are : ")
        for pkg in list(db_manifest.keys()):
            print(pkg)
        choice = raw_input("For module attributes, enter 'Y' else 'N' ...")
        if choice == "Y" or "y":
            print(db_manifest)

#########################################################
def do_search(args):
    listing = Namelisting()
    listing.namelist(args[0])

#########################################################

def pkg_install(args):
    directory = os.environ['ROOTSYS']
    modules = []
    rule_name = re.compile('.*name:.*')
    parsename = []

    for subdir, dirs, files in os.walk(directory):
        if args[0] + ".yml" in files:
            with open(directory+'/' + args[0] + '.yml') as filepath:
                fp_read = filepath.read()
                names = rule_name.findall(fp_read)
                parsename = [x.strip(' name: ') for x in names]

    for i in range(3, len(parsename)):
        if '"' in parsename[i]:
            parsename[i] = parsename[i].replace('"', '')
            modules.append(parsename[i])

    args[0] = str(args[0])
    if args[0] == "IO":
        for i in range(len(modules)):
            install_val = do_pkg_install(modules[i])
            if install_val == "failed":
                print("\n")
                print("***********************************************")
                print("Could not install module " + modules[i])
                print("***********************************************")
                print("\n")
                i = i + 1

#########################################################

ACTIONS = {
    "-mi" : module_install,
    "--module-install" : module_install,
    "-pi" : pkg_install,
    "--package-install" : pkg_install,
    "-l" : do_list,
    "--list" : do_list,
    "-s" : do_search,
    "--search" : do_search,
}

if sys.argv[1] in ACTIONS.keys():
    ACTIONS[sys.argv[1]](sys.argv[2:])
else:
    print('[root-get] Error! Wrong usage of root-get!')

exit(0)
MANIFEST = None

with open(sys.argv[1], 'r') as stream:
    try:
        MANIFEST = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
