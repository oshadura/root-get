"""
"""
import os
import glob
import subprocess
import json
import re
import logging
from difflib import get_close_matches
from pathlib2 import Path

from resolver.db_resolver import *
from resolver.dag_resolver import *
from downloader.download_request import *
from analyzer.path_checker import *
from analyzer.namelist import *
from analyzer.utilities.prepare_env_package import *
from analyzer.utilities.rerun_cmake import *
from integrator.install_module import *
from integrator.install_module_ninja import *
from integrator.sedfile_utility import *
from integrator.prepare_module import *
from builder.clean_module import *
from builder.build_module import *


module_logger = logging.getLogger('root_get.package_manager')

class PackageManager(object):
    """docstring for PackageManager."""
    def __init__(self):
        self.database = DBResolver()
        self.dag = DAGResolver()
        self.logger = logging.getLogger('root_get.package_manager.PackageManager')
        self.logger.info('creating an instance of PackageManager')

    def check_package_path(self, pkg):
        """ Checking names of packages
            We are considering here that "packages" are parent directories of modules
            FIXME:  add a parser from ROOT package map generated with help of CMake: map.yml """
        PATH = PathChecker()
        src_dir_root = ''
        self.logger.info("[root-get] DEBUG: Checking package path")
        rootsources = os.getenv('ROOT_SOURCES')
        check_package_name = os.system('find %s -maxdepth 1 -type d  -name "%s" ! -path "*tutorials*" ! -path "*dictpch*"' % (rootsources, pkg))
        if check_package_name != 0:
            self.logger.info("Not a ROOT package (we are working only with ROOT packages for now.)")
            return False
        else:
            # if have such directory in root then we can try to get it's real path
            src_dir_root = PATH.path4pkg(pkg, rootsources)
            self.logger.info("[root-get] We would use a package/module from {0:s}".format(src_dir_root))
        return src_dir_root


    def downloader(self, path_value):
        rule_url = re.compile(".*packageurl:.*")

        with open(path_value) as manifest_file:
            mread = manifest_file.read()
            url = rule_url.findall(mread)
            manifest_file.close()

        parc_url = [x.lstrip(' packageurl: ') for x in url]
        d_url = parc_url[0].replace('"','')

        path = path_value.replace("manifest.yml", '')

        downloader_req = Downloader(d_url, path)
        downloader_req.download_github()
        list_files = glob.iglob(path + "/*")
        latest_file = max(list_files, key=os.path.getctime)
        return latest_file


    def yaml_validator(self, dir_path):
        validation = 'require \'yaml\';puts YAML.load_file(' + "'" + str(dir_path) + "'" + ')'
        suppress = open(os.devnull, 'w')
        return_val = subprocess.call(["ruby", "-e", validation], stdout=suppress, stderr=subprocess.STDOUT)
        return return_val

    def check_module_path(self, pkg, pwd_path):
        """ Checking names of modules
            Old deprecated mode where we could install separetelly modules
        """
        src_dir_root = ''
        self.logger.info("[root-get] DEBUG: Checking module path")
        rootsources = os.getenv('ROOT_SOURCES')
        check_module_name = os.system('find %s -mindepth 2 -type d  -name "%s" ! -path "*tutorials*" ! -path "*dictpch*"' % (rootsources, pkg))
        if check_module_name != 0:
            self.logger.info("Not a ROOT package (we are working only with ROOT packages for now.)")
            return False
        else:
            # if have such directory in root then we can try to get it's real path
            path = PathChecker()
            src_dir_root = path.path4module(pkg, rootsources)
            if src_dir_root != None:
                self.logger.info("[root-get] We would use a module from {0:s}".format(src_dir_root))
            else:
                self.logger.info("Package not present in rootbase.")
                self.logger.info("Please provide absolute path to manifest file, else enter 'NA'")
                manifest_path = raw_input()
                if manifest_path != 'NA':
                    value = self.yaml_validator(manifest_path)
                    if value == 1:
                        self.logger.info("Not a valid yml. Please provide valid yml. Exiting now.")
                    else:
                        self.logger.info("Downloading package using url.")
                        download_path = self.downloader(manifest_path)
                        #get path for downloaded directory
                        filepath = Path(download_path + "/CMakeLists.txt")
                        if filepath.is_file():
                            os.system(pwd_path + "/integrator/sedfile " + download_path)
                            src_dir_root = download_path
                        else:
                            #[WIP]
                            self.logger.info("No CMakeLists.txt present. Creating using manifest.")
                            rule_name = re.compile(".*name:.*")
                            with open(manifest_path) as manifest:
                                read = manifest.read()
                                name = rule_name.findall(read)
                            parc_name = [x.lstrip(' name: ') for x in name]
                            cml = open(download_path + "/CMakeLists.txt", 'a')
                            cml.write("ROOT_STANDARD_LIBRARY_PACKAGE(" + parc_name[0] + " DEPENDENCIES RIO)")
                            src_dir_root = download_path
                else:
                    self.logger.info("Can you provide package path..(if available)")
                    dir_path = raw_input()
                    filepath = Path(dir_path + "/CMakeLists.txt")
                    if filepath.is_file():
                        src_dir_root = dir_path
                self.logger.info("[root-get] We would use a module from {0:s}".format(src_dir_root))
        return src_dir_root

    def analizer_package(self, pkg, src_dir_root):
        """ Extention of package/module CMake files out of existing in ROOT
            We are adopting modules to be able to build packages outside of ROOT."""
        self.logger.info("[root-get] DEBUG: Preparing environment for package")
        ecanalyze = 0
        try:
            ecanalyze = prepare_env_package(pkg, src_dir_root)
        except:
            pass
        if ecanalyze != 0:
            self.logger.info("[root-get] Failed to configure package")
            return False


    def generation_db_modules(self):
        """ We can use either db.hardcoded_db() or db.generated_manifest()."""
        self.logger.info("[root-get] DEBUG: Generating DB for modules")
        db_manifest = self.database.generated_manifest()
        if not db_manifest:
            self.logger.info("[root-get] Failed to generate DB for modules only")
            return False
        return db_manifest


    def generation_hardcoded_db(self):
        """ We can use either db.hardcoded_db() or db.generated_manifest()."""
        self.logger.info("[root-get] DEBUG: Generating hc DB for modules")
        db_manifest = self.database.hardcoded_db()
        if not db_manifest:
            self.logger.info("[root-get] Failed to generate DB for modules (test)")
            return False
        return db_manifest


    def generation_db_packages(self):
        """ We can use either db.hardcoded_db() or db.generated_manifest()."""
        self.logger.info("[root-get] DEBUG: Genearating DB for packages")
        package = raw_input("Enter ROOT package name: ")
        db_manifest = self.database.generated_manifest_pkg(package)
        if not db_manifest:
            self.logger.info("[root-get] Failed to generate DB for ROOT packages")
            return False
        return db_manifest


    def print_db_manifest(self, db_manifest):
        """ Print DB """
        self.logger.info("[root-get] Listing our DB manifest")
        self.logger.info(json.dumps(db_manifest, indent=4))


    def dag_pre_generation(self, db_manifest):
        """ Generation of reduced manifest DB to be used for DAG operations"""
        self.logger.info("[root-get] DEBUG: Generating pre-DAG database")
        dag_manifest = self.database.pre_dag(db_manifest)
        self.logger.info(json.dumps(dag_manifest, indent=4))
        return dag_manifest


    def parser_db_manifest(self, db_manifest, PKG_PATH):
        self.logger.info("[root-get] DEBUG: Parsing DB manifest.")
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
        self.logger.info(json.dumps(db_manifest, indent=4))
        return db_manifest


    def generation_lock_file_from_dag(self, dag_manifest):
        self.logger.info("[root-get] DEBUG: Generating lock file from DAG.")
        self.dag.from_dict(dag_manifest)
        self.dag.topological_sort()
    '''
        self.logger.info(dag.all_leaves())
        except:
        self.logger.info('-> Missing package: {0:s}'.format(traceback.print_exc()))
        if not dag.validate()[0]:
            for value in db_manifest[pkg]["deps"]:
                if(not db_manifest[value]) or (not db_manifest[value]["installed"])
                    check_package = os.system('find %s -maxdepth 1 -type d  -name "%s" !
                                                -path "*tutorials*" ! -path "*dictpch*"' % (root_sources, value))
    '''

    def naming_checker(self, pkg):
        self.logger.info("[root-get] DEBUG: since a name of ROOT package and name of \
directory are not consistent, we need to use it the same as name of target.")
        rule = re.compile('.*targets:.*')
        # Opening manifest file
        with open("manifest.yml") as manifest_file:
            read_manifest = manifest_file.read()
            get_target = rule.findall(read_manifest)
            target = [x.strip(' targets: ') for x in get_target]
        # Opening manifest file
        if get_close_matches(pkg, target):
            self.logger.info("[root-get] The package name {0:s} is available in list of  \
            targets in {1:s}.".format(pkg, target))
        else:
            # FIXME: we need to move to better regexes
            #regexpackage = pkg
            #target_regex = "[A-z]{0}".format(regexpackage)
            #pattern = re.compile(target_regex)
            #matches = pattern.search(target)
            #if matches:
            #    print matches.group(1)
            # Old version of A.S.
            sudopkg = pkg
            if sudopkg.islower():
                sudopkg = sudopkg.upper()
                if get_close_matches(sudopkg, target):
                    pkg = sudopkg
                    self.logger.info("[root-get] did you mean " + pkg + " ?")
            elif sudopkg.isupper():
                sudopkg = sudopkg.lower()
                if get_close_matches(sudopkg, target):
                    pkg = sudopkg
                    self.logger.info("[root-get] did you mean " + pkg + " ?")
            else:
                if get_close_matches(pkg, target, cutoff=0.5):
                    self.logger.info("[root-get] We have mixed-symbol name of package {0:s}, it is OK".format(pkg))
                #FIXME: wrong, it just selecting first symbol!
                #pkg = target[0]
        return pkg


    def check_pkg_db(self, pkg, db_manifest):
        self.logger.info("[root-get] DEBUG: Checking package in DB.")
        try:
            self.logger.info("[root-get] Checking package DB keys available in root-get: {0:s}".format(db_manifest.keys()))
            if pkg not in db_manifest.keys():
                self.logger.info("[root-get] Can't find package {0:s} in DB".format(pkg))
                return False
        except:
            pass


    def check_module_db(self, module, db_manifest):
        self.logger.info("[root-get] DEBUG: Checking module in DB.")
        try:
            self.logger.info("[root-get] Checking module DB keys available in root-get: {0:s}".format(db_manifest.keys()))
            if module not in db_manifest.keys():
                self.logger.info("[root-get] Can't find module {0:s} in DB".format(module))
                return False
        except:
            pass


    def check_install_pkg_db(self, pkg, db_manifest):
        self.logger.info("[root-get] DEBUG: Checking if package actually is already installed")
        try:
            if db_manifest[pkg].has_key("installed"):
                if db_manifest[pkg]["installed"] is True:
                    self.logger.info("Package already installed. Exiting now.")
                    return True
        except:
            pass
    '''
    def trigger_dependency_pkg_db(self, pkg, db_manifest):
        self.logger.info("[root-get] DEBUG: Triggering dependency builds")
        if db_manifest[pkg]["deps"]:
            for dep in db_manifest[pkg]["deps"]:
                self.logger.info("[root-get] Installing dependences {0:s}".format(dep))
                if not install_dep_pkg(dep, db_manifest):
                    return False
    '''

    def clean_build(self, pkg, db_manifest):
        self.logger.info("[root-get] DEBUG: Cleaning build if there is something in build directory")
        try:
            ecbuild = clean_module(pkg)
            if ecbuild != 0:
                self.logger.info("[root-get] Failed to clean build directory for the package.")
                return False
        except:
            pass


    def rerun_configuration(self, pkg):
        ecrerun = rerun_cmake(pkg)
        if ecrerun != 0:
            self.logger.info("[root-get] Failed to re-run cmake in directory for the package.")
            return False


    def build_package(self, pkg, db_manifest):
        self.logger.info("[root-get] DEBUG: Building package: we are using Ninja build system.")
        try:
            self.logger.info("[root-get] Installing {0:s}".format(pkg))
            try:
                self.logger.info("[root-get] DEBUG: we are running ninja for {0:s}".format(db_manifest[pkg]["path"]))
            except:
                pass
            ecbuild = build_module(pkg)
            if ecbuild != 0:
                self.logger.info("[root-get] Failed to build package.")
                return False
        except:
            pass


    def build_module(self, module, db_manifest):
        self.logger.info("[root-get] DEBUG:  we are using Ninja build system.")
        try:
            self.logger.info("[root-get] Installing {0:s}".format(module))
            try:
                self.logger.info("[root-get] DEBUG: we are running ninja for {0:s}".format(db_manifest[module]["path"]))
            except:
                pass
            ecbuild = build_module(module)
            if ecbuild != 0:
                self.logger.info("[root-get] Failed to build package.")
                return False
        except:
            pass


    def prepare_package(self, pkg):
        self.logger.info("[root-get] DEBUG: Creating Zip file from build directory of package")
        ecpackaging = prepare_module(pkg)
        if ecpackaging != True:
            self.logger.info("[root-get] Failed to create package.")
            return False


    def prepare_module(self, module):
        self.logger.info("[root-get] DEBUG: Creating Zip file from build directory of module")
        ecpackaging = prepare_module(module)
        if ecpackaging != True:
            self.logger.info("[root-get] Failed to create module.")
            return False


    def deploy_pkg(self, pkg):
        self.logger.info("[root-get] DEBUG: Deploying package")
        ecinstall = install_module(pkg)
        if ecinstall != True:
            self.logger.info("[root-get] Failed to install package in zip format.")
            ecinstallninja = install_module_ninja(pkg)
            if ecinstallninja != 0:
                self.logger.info("[root-get] Failed to install package using build system")
                return False
        else:
            return "deployed"


    def deploy_module(self, module):
        self.logger.info("[root-get] DEBUG: Deploying module")
        ecinstall = install_module(module)
        if ecinstall != True:
            self.logger.info("[root-get] Failed to install module in zip format.")
            ecinstallninja = install_module_ninja(module)
            if ecinstallninja != True:
                self.logger.info("[root-get] Failed to install module using build system")
                return False
        else:
            return "deployed"
