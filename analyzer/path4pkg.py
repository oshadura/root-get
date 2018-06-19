""" A Path4pkg class
Experiments on trying to generate package for ROOT PM
"""
import os

class Path4pkg(object):
    """docstring for Path4pkg."""
    def __init__(self, arg=None):
        super(Path4pkg, self).__init__()
        self.arg = arg

    def path4pkg(self, dirname, directory=''):
        dirname = dirname.lower()
        non_acceptable_dirs = set(['tutorials', 'test', 'interpreter', 'dictpch'])
        directory_exceptions = set(['rfio', 'io'])
        for root, dirs, names in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in non_acceptable_dirs]
            if((dirname in dirs) or (dirname.strip("io") in dirs)):
                if(dirname in directory_exceptions):
                    return os.path.join(root, dirname)
                else:
                    return os.path.join(root, dirname.strip("io"))
            #elif dirname not in directory_exceptions in dirs
        raise Exception('We work only with ROOT packages by now')
