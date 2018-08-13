""" A PathChecker class
        Helper that we try to use to generate package/module path
        for ROOT packages/modules for ROOT PM. Here we use a concept
        that each $ROOTSYS/{directory} is a package and directories deeper are modules.
"""

import os
import logging

class PathChecker(object):
    """ PathChecker class """
    def __init__(self):
        super(PathChecker, self).__init__()
        self.logger = logging.getLogger('analyser.namelist.NameListing')
        self.logger.info('creating an instance of NameListing')

    def path4module(self, dirname, directory='', mindepth=2, maxdepth=float('inf')):
        """ Function checking a "walking/search" functionality for ROOT modules"""
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
                        path = os.path.join(dirpath, dirname)
                    else:
                        path = os.path.join(dirpath, dirname.strip("io"))
                    return path
            elif depth > maxdepth:
                del dirs[:] # too deep, don't recurse

    def path4pkg(self, dirname, directory='', mindepth=1, maxdepth=float('inf')):
        """ Function checking a "walking/search" functionality for ROOT packages"""
        directory = os.path.normcase(directory)
        dirname = dirname.lower()
        non_acceptable_dirs = set(['tutorials', 'test', 'interpreter', 'dictpch'])
        root_depth = directory.rstrip(os.path.sep).count(os.path.sep) - 1
        for dirpath, dirs in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in non_acceptable_dirs]
            depth = dirpath.count(os.path.sep) - root_depth
            if mindepth <= depth < maxdepth:
                if dirname in dirs:
                    return os.path.join(dirpath, dirname)
                else:
                    raise Exception('We work only with ROOT modules by now')
            elif depth > maxdepth:
                del dirs[:] # too deep, don't recurse
