"""
"""

import os
from shutil import rmtree
from  analyzer.utilities.check_env import check_env

def clean_module(pkg_name):
    """
    """
    check_env()
    cache_directory = os.getenv('ROOT_PKG_CACHE') + "/" + pkg_name + '/build'
    if rmtree(cache_directory):
        return True
