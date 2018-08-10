""" A Zip4pkg class
Experiments on trying to generate package for ROOT PM
"""
import os
import zipfile

class ZipperPackage(object):
    """docstring for Zip4pkg."""
    def __init__(self):
        pass

    def zipdir(self, path, ziph):
        """ ziping our ready package
        """
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))
