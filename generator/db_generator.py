import os
from os.path import expanduser
import re

home = expanduser("~")

class DBGenerator(object):
    """DBgenerator class"""
    def __init__(self):
        super(DBGenerator, self).__init__()

    def dbgenerator(self):
        """Function to generate module manifest 'yml' file"""
        rootdir = home + "/.cache/root-pkgs/"
        """ Set of rules to be used for generator of package DB """
        rule_name = re.compile('.*name:.*')
        rule_package_url = re.compile('.*packageurl:.*')
        rule_tag = re.compile('.*tag:.*')
        rule_path = re.compile('.*path:.*')
        rule_ph = re.compile('.*publicheaders:.*')
        rule_sources = re.compile('.*sources:.*')
        rule_targets = re.compile('.*targets:.*')
        rule_deps = re.compile('.*deps:.*')

        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                if file == "module.yml":
                    module_file_path = os.path.join(subdir, file)
                    with open(module_file_path) as filepath:
                        fp_read = filepath.read()
                        names = rule_name.findall(fp_read)
                        parcing_rule_name = [x.strip(' name: ') for x in names]
                        if parcing_rule_name:
                            manifest_file = open("manifest.yml", 'a')
                            manifest_file.write(",".join(parcing_rule_name))
                            manifest_file.write(":")
                            manifest_file.write("\n")
                            manifest_file.close()
                        rule_package_url_check = rule_package_url.findall(fp_read)
                        if rule_package_url_check:
                            manifest_file = open("manifest.yml", 'a')
                            manifest_file.write(",".join(rule_package_url_check))
                            manifest_file.write("\n")
                            manifest_file.close()
                        rule_tag_check = rule_tag.findall(fp_read)
                        if rule_tag_check:
                            manifest_file = open("manifest.yml", 'a')
                            manifest_file.write(",".join(rule_tag_check))
                            manifest_file.write("\n")
                            manifest_file.close()
                        rule_path_check = rule_path.findall(fp_read)
                        if rule_path_check:
                            manifest_file = open("manifest.yml", 'a')
                            manifest_file.write(",".join(rule_path_check))
                            manifest_file.write("\n")
                            manifest_file.close()
                        rule_ph_check = rule_ph.findall(fp_read)
                        if rule_ph_check:
                            manifest_file = open("manifest.yml", 'a')
                            manifest_file.write(",".join(rule_ph_check))
                            manifest_file.write("\n")
                            manifest_file.close()
                        rule_sources_check = rule_sources.findall(fp_read)
                        if rule_sources_check:
                            manifest_file = open("manifest.yml", 'a')
                            manifest_file.write(",".join(rule_sources_check))
                            manifest_file.write("\n")
                            manifest_file.close()
                        rule_targets_check = rule_targets.findall(fp_read)
                        if rule_targets_check:
                            manifest_file = open("manifest.yml", 'a')
                            manifest_file.write(",".join(rule_targets_check))
                            manifest_file.write("\n")
                            manifest_file.close()
                        rule_deps_check = rule_deps.findall(fp_read)
                        if rule_deps_check:
                            manifest_file = open("manifest.yml", 'a')
                            manifest_file.write(",".join(rule_deps_check))
                            manifest_file.write("\n")
                            manifest_file.close()

    def manifest_generator(self, arg):
        """Function to generate package manifest 'yml' file"""
        rootdir = os.environ['ROOTSYS']

        """ Set of rules to be used for generator of package DB """
        rule_name = re.compile('.*name:.*')
        rule_package_url = re.compile('.*packageurl:.*')
        rule_tag = re.compile('.*tag:.*')
        rule_path = re.compile('.*path:.*')
        rule_ph = re.compile('.*publicheaders:.*')
        rule_sources = re.compile('.*sources:.*')
        rule_targets = re.compile('.*targets:.*')
        rule_products = re.compile('.*products:.*')
        rule_deps = re.compile('.*deps:.*')
        rule_modules = re.compile('.*module:.*')

        with open(rootdir + "/" + arg + ".yml") as pkgfile:
            pkgread = pkgfile.read()
            names = rule_name.findall(pkgread)
            parcing_rule_name = [x.strip(' name: ') for x in names]
            rule_tag_check = rule_tag.findall(pkgread)
            rule_package_url_check = rule_package_url.findall(pkgread)
            rule_tag_check = rule_tag.findall(pkgread)
            rule_path_check = rule_path.findall(pkgread)
            rule_ph_check = rule_ph.findall(pkgread)
            rule_targets_check = rule_targets.findall(pkgread)
            rule_deps_check = rule_deps.findall(pkgread)
            rule_products_check = rule_products.findall(pkgread)
            rule_modules_check = rule_modules.findall(pkgread)
            rule_sources_check = rule_sources.findall(pkgread)

            module_len = len(rule_modules_check)

            if parcing_rule_name:
                pkg_manifest_file = open("pkg_manifest.yml", 'a')
                pkg_manifest_file.write(parcing_rule_name[0])
                pkg_manifest_file.write(":\n")

            if rule_tag_check:
                pkg_manifest_file = open("pkg_manifest.yml", 'a')
                pkg_manifest_file.write(rule_tag_check[0])
                pkg_manifest_file.write("\n")

            if rule_targets_check:
                pkg_manifest_file = open("pkg_manifest.yml", 'a')
                pkg_manifest_file.write(" target: ")
                pkg_manifest_file.write(parcing_rule_name[1])
                pkg_manifest_file.write("\n")

            if rule_products_check:
                pkg_manifest_file = open("pkg_manifest.yml", 'a')
                pkg_manifest_file.write(" products: ")
                pkg_manifest_file.write(parcing_rule_name[2])
                pkg_manifest_file.write("\n")

            """Iterating over the rule lists"""
            for i in range(3, module_len + 3):
                pkg_manifest_file = open("pkg_manifest.yml", 'a')
                pkg_manifest_file.write(" " + parcing_rule_name[i] + ":\n")
                pkg_manifest_file.write(" " + rule_package_url_check[i-3] + "\n")
                pkg_manifest_file.write(" " + rule_tag_check[i-2] + "\n")
                pkg_manifest_file.write(" " + rule_path_check[i-3] + "\n")
                pkg_manifest_file.write(" " + rule_ph_check[i-3] + "\n")
                pkg_manifest_file.write(" " + rule_sources_check[i-3] + "\n")
                pkg_manifest_file.write(" " + rule_targets_check[i-2] + "\n")
                pkg_manifest_file.write(" " + rule_deps_check[i-3] + "\n")

    def clean_deps(self):
        """Function to remove RIO, Core from deps(present by default)"""
        workdir = os.getcwd()
        rule_deps = re.compile(".*deps:.*")

        with open(workdir+"/manifest.yml", 'r') as manifest_file:
            read_manifest = manifest_file.read()

        read_manifest = read_manifest.replace("Core", '')
        read_manifest = read_manifest.replace("RIO", '')
        read_manifest = read_manifest.replace(";", '')

        with open(workdir+"/manifest.yml", 'w') as manifest_file:
            manifest_file.write(read_manifest)

        norepeat_list = []

        infile = open('manifest.yml')
        for line in infile:
            line = line.strip("\n")
            if "deps" in line:
                norepeat_list.append(line)
            if line not in norepeat_list:
                norepeat_list.append(line)
        infile.close()

        outfile = open('./manifest.yml', 'w')
        for line in norepeat_list:
            outfile.write(line + "\n")
        outfile.close()

        with open(workdir+"/manifest.yml") as manifest_file:
            manifest_file.readlines()
            manifest_read = manifest_file.read()
            rule_deps_check = rule_deps.findall(manifest_read)
            rule_deps_check = [x.strip(' deps: ') for x in rule_deps_check]
            if not rule_deps_check:
                return "no_deps"
            else:
                return "deps"

    def clean_deps_pkg(self):
        """Function to remove RIO, Core from deps(present by default)"""
        workdir = os.getcwd()
        rule_deps = re.compile(".*deps:.*")

        with open(workdir+"/pkg_manifest.yml", 'r') as manifest_file:
            read_manifest = manifest_file.read()

        read_manifest = read_manifest.replace("Core", '')
        read_manifest = read_manifest.replace("RIO", '')
        read_manifest = read_manifest.replace(";", '')

        with open(workdir+"/pkg_manifest.yml", 'w') as manifest_file:
            manifest_file.write(read_manifest)

        norepeat_list = []

        infile = open('pkg_manifest.yml')
        for line in infile:
            line = line.strip("\n")
            if line not in norepeat_list:
                norepeat_list.append(line)
        infile.close()

        outfile = open('./pkg_manifest.yml', 'w')
        for line in norepeat_list:
            outfile.write(line + "\n")
        outfile.close()

        with open(workdir+"/pkg_manifest.yml") as manifest_file:
            manifest_file.readlines()
            manifest_read = manifest_file.read()
            rule_deps_check = rule_deps.findall(manifest_read)
            rule_deps_check = [x.strip(' deps: ') for x in rule_deps_check]
            if not rule_deps_check:
                return "no_deps"
            else:
                return "deps"
