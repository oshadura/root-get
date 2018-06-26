import os
import re
from os.path import expanduser

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

		if os.path.isfile("manifest.yml"):
			infile = "manifest.yml"
			s = set()
			with open('temp.yml', 'w') as out:
				for line in open(infile):
					if line not in s:
						out.write(line)
						s.add(line)
		else:
			for subdir, dirs, files in os.walk(rootdir):
				for file in files:
					if file == "module.yml":
						fp = os.path.join(subdir, file)
						with open(fp) as t:
							fl = t.read()
							names = rule_name.findall(fl)
							parcing_rule_name = [x.strip(' name: ') for x in names]
							if parcing_rule_name:
								fl2 = open("manifest.yml", 'a')
								fl2.write(",".join(parcing_rule_name))
								fl2.write(":")
								fl2.write("\n")
							rule_tag_check = rule_tag.findall(fl)
							if rule_tag_check:
								fl2 = open("manifest.yml", 'a')
								fl2.write(",".join(rule_tag_check))
							#fl2.write(":")
								fl2.write("\n")
							rule_package_url_check = rule_package_url.findall(fl)
							if rule_package_url_check:
								fl2 = open("manifest.yml", 'a')
								fl2.write(",".join(rule_package_url_check))
								#fl2.write(":")
								fl2.write("\n")
							rule_ph_check = rule_ph.findall(fl)
							if rule_ph_check:
								fl2 = open("manifest.yml", 'a')
								fl2.write(",".join(rule_ph_check))
								#fl2.write(":")
								fl2.write("\n")
							rule_sources_check = rule_sources.findall(fl)
							if rule_sources_check:
								fl2 = open("manifest.yml", 'a')
								fl2.write(",".join(rule_sources_check))
								#fl2.write(":")
								fl2.write("\n")
							rule_targets_check = rule_targets.findall(fl)
							if rule_targets_check:
								fl2 = open("manifest.yml", 'a')
								fl2.write(",".join(rule_targets_check))
								#fl2.write(":")
								fl2.write("\n")
							rule_deps_check = rule_deps.findall(fl)
							if rule_deps_check:
								fl2 = open("manifest.yml", 'a')
								fl2.write(",".join(rule_deps_check))
								#fl2.write(":")
								fl2.write("\n")
							rule_path_check = rule_path.findall(fl)
							if rule_path_check:
								fl2 = open("manifest.yml", 'a')
								fl2.write(",".join(rule_path_check))
								#fl2.write(":")
								fl2.write("\n")
		if os.path.isfile('temp.yml'):
			os.remove('temp.yml')

	def clean_deps(self):
		wd = os.getcwd()
		rl = re.compile(".*deps:.*")

		with open(wd+"/manifest.yml", 'r') as file:
			fd = file.read()

		fd = fd.replace("Core", '')
		fd = fd.replace("RIO", '')
		fd = fd.replace(";", '')

		with open(wd+"/manifest.yml", 'w') as file:
			file.write(fd)

		with open(wd+"/manifest.yml") as file:
			f = file.readlines()
			t = file.read()
			r4 = rl.findall(t)
			r4 = [x.strip(' deps: ') for x in r4 ]
			if not r4:
				return "no_deps"
			else:
				return "deps"
