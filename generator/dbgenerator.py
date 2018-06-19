import os
import re

class Dbgenerator(object):
	def __init__(self, arg=None):
		super(Dbgenerator, self).__init__()
		self.arg = arg

	def dbgenerator(self):
		cwd = os.getcwd()
		rootdir = cwd + "/build"

		rule1 = re.compile('.*name:.*')
		rule2 = re.compile('.*deps:.*')
		rule3 = re.compile('.*path:.*')

		for subdir, dirs, files in os.walk(rootdir):
			for file in files:
				if file.endswith(".yml"):
					fp = os.path.join(subdir, file)
					with open(fp) as t:
						fl = t.read()
						r1 = rule1.findall(fl)
						r1 = [x.strip(' name: ') for x in r1]
						r2 = rule2.findall(r2)
						r3 = rule3.findall(r3)
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