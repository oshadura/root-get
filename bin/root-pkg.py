#!/usr/bin/env python
import sys
import os
import json
import re
from difflib import get_close_matches
from os.path import expanduser
import yaml


# FIXME: We need to be in root-get home dir before calling this script
sys.path.append(os.getcwd())

# Import classes from root-get directories
from resolver import *
from downloader.download_request import *
from analyzer.path4pkg import *
from analyzer.namelist import *
from integrator.zip4pkg import *

# Enviroment variables
HOME = expanduser("~")
os.environ["ROOT_PKG_CACHE"] = HOME + "/.cache/root-pkgs/"
ROOT_CACHE = os.environ["ROOT_PKG_CACHE"]
print("[root-get] root-get cache: {0:s}".format(ROOT_CACHE))
ROOT_SOURCES = os.environ['ROOTSOURCES']
if  ROOT_SOURCES.endswith(os.sep):
    ROOT_SOURCES = ROOT_SOURCES - os.sep
print("[root-get] ROOT sources: {0:s}".format(ROOT_SOURCES))
PKG_PATH = os.environ['ROOT_PKG_PATH']
print("[root-get] ROOT packages installation path: {0:s}".format(PKG_PATH))
PWD_PATH = os.getcwd()
print('[root-get] root-get location: {0:s}'.format(PWD_PATH))

def check_package_path(pkg):
    """ Checking names of packages
        We are considering here that "packages" are parent directories of modules
        FIXME:  add a parser from ROOT package map generated with help of CMake: map.yml """
    src_dir_root = ''
    print("[root-get] DEBUG: Checking package path")
    check_package_name = os.system('find %s -maxdepth 1 -type d  -name "%s" ! -path "*tutorials*" ! -path "*dictpch*"' % (ROOT_SOURCES, pkg))
    if check_package_name != 0:
        print("Not a ROOT package (we are working only with ROOT packages for now.)")
        return False
    else:
        # if have such directory in root then we can try to get it's real path
        path = PathChecker()
        src_dir_root = path.path4pkg(pkg, ROOT_SOURCES)
        print("[root-get] We would use a package from {0:s}".format(src_dir_root))
    return src_dir_root

def check_module_path(pkg):
    """ Checking names of modules
        Old deprecated mode where we could install separetelly modules"""
    src_dir_root = ''
    print("[root-get] DEBUG: Checking module path")
    check_module_name = os.system('find %s -mindepth 2 -type d  -name "%s" ! -path "*tutorials*" ! -path "*dictpch*"' % (ROOT_SOURCES, pkg))
    if check_module_name != 0:
        print("Not a ROOT package (we are working only with ROOT packages for now.)")
        return False
    else:
        # if have such directory in root then we can try to get it's real path
        path = PathChecker()
        src_dir_root = path.path4module(pkg, ROOT_SOURCES)
        print("[root-get] We would  use a module from {0:s}".format(src_dir_root))
    return src_dir_root

def analizer_package(pkg, src_dir_root):
    """ Extention of package/module CMake files out of existing in ROOT
        We are adopting modules to be able to build packages outside of ROOT."""
    print("[root-get] DEBUG: Preparing environment for package")
    ecanalyze = 0
    try:
        ecanalyze = os.system(PWD_PATH + "/analyzer/preparing-environment-for-pkg " + pkg + " " + src_dir_root)
    except:
        pass
    if ecanalyze != 0:
        print("[root-get] Failed to configure package")
        return False

def generation_db_modules():
    """ We can use either db.hardcoded_db() or db.generated_manifest()."""
    print("[root-get] DEBUG: Genearating DB for modules")
    database = Db4pkg()
    db_manifest = database.generated_manifest()
    if not db_manifest:
        print("[root-get] Failed to generate DB for modules only")
        return False
    return db_manifest

def generation_hardcoded_db():
    """ We can use either db.hardcoded_db() or db.generated_manifest()."""
    print("[root-get] DEBUG: Genearating hc DB for modules")
    database = Db4pkg()
    db_manifest = database.hardcoded_db()
    if not db_manifest:
        print("[root-get] Failed to generate DB for modules (test)")
        return False
    return db_manifest

def generation_db_packages():
    """ We can use either db.hardcoded_db() or db.generated_manifest()."""
    print("[root-get] DEBUG: Genearating DB for packages")
    database = Db4pkg()
    package = raw_input("Enter ROOT package name: ")
    db_manifest = database.generated_manifest_pkg(package)
    if not db_manifest:
        print("[root-get] Failed to generate DB for ROOT packages")
        return False
    return db_manifest

def print_db_manifest(db_manifest):
    """ Print DB """
    print("[root-get] Listing our DB manifest")
    print(json.dumps(db_manifest, indent=4))

def dag_pre_generation(db_manifest):
    """ Generation of reduced manifest DB to be used for DAG operations"""
    print("[root-get] DEBUG: Genearating pre DAG DB")
    database = Db4pkg()
    dag_manifest = database.pre_dag(db_manifest)
    return dag_manifest

def parser_db_manifest(db_manifest):
    print("[root-get] DEBUG: Parsing DB manifest")
    try:
        for pkg_index in db_manifest:
            if "deps" in db_manifest[pkg_index]:
                if isinstance(db_manifest[pkg_index]["deps"], str):
                    db_manifest[pkg_index]["deps"] = db_manifest[pkg_index]["deps"].split()
            else:
                db_manifest[pkg_index]["deps"] = []
            db_manifest[pkg_index]["installed"] = os.path.isdir(os.path.join(PKG_PATH, pkg_index))
    except:
        pass
    return db_manifest

def generation_lock_file_from_dag(dag_manifest):
    print("[root-get] DEBUG: Generating Lock file from DAG")
    dag = Dag4pkg()
    dag.from_dict(dag_manifest)
    dag.topological_sort()
'''
    print(dag.all_leaves())
    except:
    print('-> Missing package: {0:s}'.format(traceback.print_exc()))
    if not dag.validate()[0]:
        for value in db_manifest[pkg]["deps"]:
            if(not db_manifest[value]) or (not db_manifest[value]["installed"])
                check_package = os.system('find %s -maxdepth 1 -type d  -name "%s" !
                                            -path "*tutorials*" ! -path "*dictpch*"' % (root_sources, value))
'''

def resolver_dependencies(pkg, db_manifest):
    """ resolving dependencies without DAG """
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

def naming_checker(pkg):
    print("[root-get] DEBUG: Fixing name of package in case we printed it in a wrong way.")
    rule = re.compile('.*targets:.*')

    with open(PWD_PATH + "/manifest.yml") as manifest_file:
        read_manifest = manifest_file.read()
        get_target = rule.findall(read_manifest)
        target = [x.strip(' targets: ') for x in get_target]

    if get_close_matches(pkg, target):
        print("[root-get] The package name {0:s} is available in list of targets in {1:s}, keep on working..".format(pkg, target))
    else:
        sudopkg = pkg
        if sudopkg.islower():
            sudopkg = sudopkg.upper()
            if get_close_matches(sudopkg, target):
                pkg = sudopkg
                print("[root-get] did you mean " + pkg + " ?")
        elif sudopkg.isupper():
            sudopkg = sudopkg.lower()
            if get_close_matches(sudopkg, target):
                pkg = sudopkg
                print("[root-get] did you mean " + pkg + " ?")
        else:
            if get_close_matches(pkg, target, cutoff=0.5):
                print("[root-get] We have mixed-symbol name of package {0:s}, it is OK".format(pkg))
            #FIXME: wrong, it just selecting first symbol!
            #pkg = target[0]
    return pkg

def check_pkg_db(pkg, db_manifest):
    print("[root-get] DEBUG: Checking package in DB")
    try:
        print("[root-get] Checking package DB keys available in root-get: {0:s}".format(db_manifest.keys()))
        if pkg not in db_manifest.keys():
            print("[root-get] Can't find package {0:s} in DB".format(pkg))
            return False
    except:
        pass

def check_install_pkg_db(pkg, db_manifest):
    print("[root-get] DEBUG: Checking if package actually is already installed")
    try:
        if db_manifest[pkg].has_key("installed"):
            if db_manifest[pkg]["installed"] is True:
                return True
    except:
        pass
'''
def trigger_dependency_pkg_db(pkg, db_manifest):
    print("[root-get] DEBUG: Triggering dependency builds")
    if db_manifest[pkg]["deps"]:
        for dep in db_manifest[pkg]["deps"]:
            print("[root-get] Installing dependences {0:s}".format(dep))
            if not install_dep_pkg(dep, db_manifest):
                return False
'''

def clean_build(pkg, db_manifest):
    print("[root-get] DEBUG: Cleaning build if there is something in build directory")
    try:
        print("[root-get] DEBUG: we are cleaning in {0:s}".format(db_manifest[pkg]["path"] + "/../build"))
        ecbuild = os.system(PWD_PATH + "/builder/clean-pkg " + pkg)
        if ecbuild != 0:
            print("[root-get] Failed to clean build directory for the package.")
            return False
    except:
        pass

def rerun_configuration(pkg):
    ecrerun = os.system(PWD_PATH + "/analyzer/rerun-cmake " + pkg)
    if ecrerun != 0:
        print("[root-get] Failed to re-run cmake in directory for the package.")
        return False

def build_package(pkg, db_manifest):
    print("[root-get] DEBUG: Building package: ninja build system")
    try:
        print("[root-get] Installing {0:s}".format(pkg))
        print("[root-get] DEBUG: we are running ninja for {0:s}".format(db_manifest[pkg]["path"]))
        ecbuild = os.system(PWD_PATH + "/builder/build-pkg " + pkg)
        if ecbuild != 0:
            print("[root-get] Failed to build package.")
            return False
    except:
        pass

def prepare_package(pkg):
    print("[root-get] DEBUG: Creating Zip file from build directory of package")
    ecpackaging = os.system(PWD_PATH + "/integrator/prepare-pkg " + pkg)
    if ecpackaging != 0:
        print("[root-get] Failed to create package.")
        return False

def deploy_pkg(pkg):
    print("[root-get] DEBUG: Deploying package")
    ecinstall = os.system(PWD_PATH + "/integrator/install-pkg " + pkg)
    if ecinstall != 0:
        print("[root-get] Failed to install package in zip format.")
        ecinstallninja = os.system(PWD_PATH + "/integrator/" + "install-pkg-ninja " + pkg)
        if ecinstallninja != 0:
            print("[root-get] Failed to install package using build system")
            return False
    else:
        return "deployed"

def install_dep_pkg(pkg, db_manifest):
    """ Main installation routine only for dependency packages"""
# Checkout packages if we have them in ROOT
    src_path = check_module_path(pkg)
# Analyzing packages: generation of package/module CMakeFile.txt,
    analizer_package(pkg, src_path)
# Building DB
    db_manifest = generation_db_modules()
# Print DB
    print_db_manifest(db_manifest)
# Generating DB instance for dag
    dag_manifest = dag_pre_generation(db_manifest)
# WIP: Still not working
    generation_lock_file_from_dag(dag_manifest)
# Parcing packages in db_manifest
    #parced_db_manifest = parser_db_manifest(db_manifest)
# Resolving dependecies without DAG
    resolver_dependencies(pkg, db_manifest)
# Before buiding we need to check if pkg is really in the Db
    check_pkg_db(pkg, db_manifest)
# Check if package is installed
    if check_install_pkg_db(pkg, db_manifest):
        return True
# Trigger trigger_dependencies_pkg_db
    #trigger_dependency_pkg_db(pkg, db_manifest)
# Buiding packages
    else:
        build_package(pkg, db_manifest)
# Preparing packages
        prepare_package(pkg)
# Installing packages
        deploy_pkg(pkg)
####################
    db_manifest[pkg]["installed"] = True
    return True
#########################################################

def install_pkg(pkg):
    """ Main installation routine for main package"""
# Checkout packages if we have them in ROOT
    src_path = check_module_path(pkg)
# Analyzing packages: generation of package/module CMakeFile.txt,
    analizer_package(pkg, src_path)
# Building DB
    db_manifest = generation_db_modules()
# Print DB
    print_db_manifest(db_manifest)
# Generating DB instance for dag
    dag_manifest = dag_pre_generation(db_manifest)
# WIP: Still not working
    generation_lock_file_from_dag(dag_manifest)
# Parcing packages in db_manifest
    parced_db_manifest = parser_db_manifest(db_manifest)
# Resolving dependecies without DAG
    resolver_dependencies(pkg, parced_db_manifest)
# Adopting name of package according generated DB
# We are rewriting name of package!
    pkg = naming_checker(pkg)
# Before buiding we need to check if pkg is really in the Db
    check_pkg_db(pkg, parced_db_manifest)
# Check if package is installed
    if check_install_pkg_db(pkg, parced_db_manifest):
        return True
    else:
# Trigger trigger_dependencies_pkg_db
    #trigger_dependency_pkg_db(pkg, parced_db_manifest)
# Clean build directory
        clean_build(pkg, parced_db_manifest)
# Reruning CMake
        rerun_configuration(pkg)
# Buiding packages
        build_package(pkg, parced_db_manifest)
# Preparing packages
        prepare_package(pkg)
# Installing packages
        deploy_val = deploy_pkg(pkg)
####################
    try:
        db_manifest[pkg]["installed"] = True
    except:
        pass
    return deploy_val, True
#########################################################

def do_install(args):
    if not install_pkg(args[0]):
        exit(1)

#########################################################

def do_pkg_install(arg):
    deploy_val, truth_val = install_pkg(arg)
    if deploy_val != "deployed":
        return "failed"

#########################################################
def do_list(args):
    if not os.path.exists(ROOT_CACHE + args[0]):
        print("Package not installed yet. Please check installation.")
    else:
        db = Db4pkg()
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

actions = {
    "-i" : do_install,
    "--install" : do_install,
    "-l" : do_list,
    "--list" : do_list,
    "-s" : do_search,
    "-pi" : pkg_install,
}

if sys.argv[1] in actions.keys():
    actions[sys.argv[1]](sys.argv[2:])
else:
    print('[root-get] Error!')

exit(0)
manifest = None

with open(sys.argv[1], 'r') as stream:
    try:
        manifest = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
