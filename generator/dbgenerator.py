import os
import re
from os.path import expanduser

home = expanduser("~")

class Dbgenerator(object):
	def __init__(self, arg=None):
		super(Dbgenerator, self).__init__()
		self.arg = arg

	def dbgenerator(self):
		#cwd = os.getcwd()
		#rootdir = cwd + "/build"
		rootdir = home + "/.cache/root-pkgs/"

		rule1 = re.compile('.*name:.*')
		rule2 = re.compile('.*deps:.*')
		rule3 = re.compile('.*path:.*')

		for subdir, dirs, files in os.walk(rootdir):
			for file in files:
#				if file.endswith(".yml"):
				if file == "module.yml":
					fp = os.path.join(subdir, file)
					with open(fp) as t:
						fl = t.read()
						r1 = rule1.findall(fl)
						r1 = [x.strip(' name: ') for x in r1]
						r2 = rule2.findall(fl)
						r3 = rule3.findall(fl)
						if r1:
							fl2 = open("manifest.yml", 'a')
							fl2.write(",".join(r1))
							fl2.write(":")
							fl2.write("\n")
						if r2:
							fl2 = open("manifest.yml", 'a')
							fl2.write(",".join(r2))
							fl2.write("\n")
						if r3:
							fl2 = open("manifest.yml", 'a')
							fl2.write(",".join(r3))
							fl2.write("\n")

	def clean_deps(self):
		wd = os.getcwd()

		rl = re.compile(".*deps:.*")

		with open(wd+"/manifest.yml", 'r') as file:
			fd = file.read()

		fd = fd.replace("Core","")
		fd = fd.replace("RIO","")

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

