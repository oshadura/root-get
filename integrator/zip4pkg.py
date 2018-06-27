""" A Zip4pkg class
Experiments on trying to generate package for ROOT PM
"""
import os
import zipfile

class Zip4pkg(object):
    """docstring for Zip4pkg."""
    def __init__(self, arg):
        super(Zip4pkg, self).__init__()
        self.arg = arg

    def zipdir(path, ziph):
        """ ziping our ready package
        """
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))
