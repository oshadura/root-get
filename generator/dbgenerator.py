import os
from os.path import expanduser
import re

home = expanduser("~")

class Dbgenerator(object):
    def __init__(self, arg=None):
        super(Dbgenerator, self).__init__()
        self.arg = arg

    def dbgenerator(self):
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
                        rule_package_url_check = rule_package_url.findall(fp_read)
                        if rule_package_url_check:
                            manifest_file = open("manifest.yml", 'a')
                            manifest_file.write(",".join(rule_package_url_check))
                            manifest_file.write("\n")
                        rule_tag_check = rule_tag.findall(fp_read)
                        if rule_tag_check:
                            manifest_file = open("manifest.yml", 'a')
                            manifest_file.write(",".join(rule_tag_check))
                            manifest_file.write("\n")
                        rule_path_check = rule_path.findall(fp_read)
                        if rule_path_check:
                            manifest_file = open("manifest.yml", 'a')
                            manifest_file.write(",".join(rule_path_check))
                            manifest_file.write("\n")
                        rule_ph_check = rule_ph.findall(fp_read)
                        if rule_ph_check:
                            manifest_file = open("manifest.yml", 'a')
                            manifest_file.write(",".join(rule_ph_check))
                            manifest_file.write("\n")
                        rule_sources_check = rule_sources.findall(fp_read)
                        if rule_sources_check:
                            manifest_file = open("manifest.yml", 'a')
                            manifest_file.write(",".join(rule_sources_check))
                            manifest_file.write("\n")
                        rule_targets_check = rule_targets.findall(fp_read)
                        if rule_targets_check:
                            manifest_file = open("manifest.yml", 'a')
                            manifest_file.write(",".join(rule_targets_check))
                            manifest_file.write("\n")
                        rule_deps_check = rule_deps.findall(fp_read)
                        if rule_deps_check:
                            manifest_file = open("manifest.yml", 'a')
                            manifest_file.write(",".join(rule_deps_check))
                            manifest_file.write("\n")

    def clean_deps(self):
        workdir = os.getcwd()
        rule_deps = re.compile(".*deps:.*")

        with open(workdir+"/manifest.yml", 'r') as manifest_file:
            read_manifest = manifest_file.read()

        read_manifest = read_manifest.replace("Core", '')
        read_manifest = read_manifest.replace("RIO", '')
        read_manifest = read_manifest.replace(";", '')

        with open(workdir+"/manifest.yml", 'w') as manifest_file:
            manifest_file.write(read_manifest)

        with open(workdir+"/manifest.yml") as manifest_file:
            file_list = manifest_file.readlines()
            manifest_read = manifest_file.read()
            rule_deps_check = rule_deps.findall(manifest_read)
            rule_deps_check = [x.strip(' deps: ') for x in rule_deps_check]
            if not rule_deps_check:
                return "no_deps"
            else:
                return "deps"
