import re
import os
import linecache
import itertools


class Namelisting(object):
    def __init__(self, arg=None):
        super(Namelisting, self).__init__()
        self.arg = arg

    def namelist(self, arg):
        path = os.environ['ROOTSYS']
        name_rule = re.compile('.*name:.*')
        module_list = []
        pkg_list = []

        for subdir, dirs, files in os.walk(path):
            for file in files:
                if file == str(arg) + ".yml":
                    module_file_path = os.path.join(subdir, file)
                    num_lines = sum(1 for line in open(module_file_path))
                    with open(module_file_path) as filepath:
                        for pkg_line in itertools.islice(filepath, 0, 9):
                            names = name_rule.findall(pkg_line)
                            parcing_rule_name = [x.strip(' name: ') for x in names]
                            if parcing_rule_name:
                                pkg_list.append(parcing_rule_name)
                        for module_line in itertools.islice(filepath, 10, num_lines):
                            names = name_rule.findall(module_line)
                            parcing_rule_name = [x.strip(' name: ') for x in names]
                            if parcing_rule_name:
                                module_list.append(parcing_rule_name)

        print("Avaiable packages : ")
        for i in range(len(pkg_list)):
            print(pkg_list[i][0])

        print("Avaiable modules : ")
        for i in range(len(module_list)):
            print(module_list[i][0])
