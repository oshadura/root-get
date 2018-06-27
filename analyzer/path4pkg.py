""" A Path4pkg class
Experiments on trying to generate package for ROOT PM
"""
import os

class Path4pkg(object):
    """docstring for Path4pkg."""
    def __init__(self, arg=None):
        super(Path4pkg, self).__init__()
        self.arg = arg

    def path4pkg(self, dirname, directory='', mindepth=2, maxdepth=float('inf')):
        # FIXME: path4pkg is working as expected, but ROUTSOURCES path can't finish with "/"
        directory = os.path.normcase(directory)
        dirname = dirname.lower()
        non_acceptable_dirs = set(['tutorials', 'test', 'interpreter', 'dictpch'])
        directory_exceptions = set(['rfio', 'io'])
        root_depth = directory.rstrip(os.path.sep).count(os.path.sep) - 1
        for dirpath, dirs, names in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in non_acceptable_dirs]
            depth = dirpath.count(os.path.sep) - root_depth
            if mindepth <= depth < maxdepth:
                if dirname in dirs or dirname.strip("io") in dirs:
                    if dirname in directory_exceptions:
                        return os.path.join(dirpath, dirname)
                    else:
                        return os.path.join(dirpath, dirname.strip("io"))
                #raise Exception('We work only with ROOT modules by now')
            elif depth > maxdepth:
                del dirs[:] # too deep, don't recurse
            #raise Exception('Exist only package with such name!')
