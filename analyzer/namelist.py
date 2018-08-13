import re
import os
import itertools
import logging

class NameListing(object):
    """Namelisting class"""
    def __init__(self):
        super(NameListing, self).__init__()
        self.logger = logging.getLogger('analyser.namelist.NameListing')
        self.logger.info('creating an instance of NameListing')

    def namelist(self, arg):
        """Function to show available packages and modules if present"""
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
                        for pkg_line in itertools.islice(filepath, 2, 6):
                            names = name_rule.findall(pkg_line)
                            parcing_rule_name = [x.strip(' name: ') for x in names]
                            if parcing_rule_name:
                                pkg_list.append(parcing_rule_name)
                        for module_line in itertools.islice(filepath, 10, num_lines):
                            names = name_rule.findall(module_line)
                            parcing_rule_name = [x.strip(' name: ') for x in names]
                            if parcing_rule_name:
                                module_list.append(parcing_rule_name)

        if not pkg_list:
            self.logger("No packages to show.")
        else:
            self.logger("Avaiable packages: ")
            for i in range(len(pkg_list)):
                self.logger(pkg_list[i][0])

        if not module_list:
            self.logger("No modules to show.")
        else:
            self.logger("Avaiable modules: ")
            for i in range(len(module_list)):
                self.logger(module_list[i][0])
