"""
"""

import os
from shutil import copytree
from  analyzer.utilities.check_env import check_env

def build_module(pkg_name):
    """
    """
    check_env()
    cache_directory = os.getenv('ROOT_PKG_CACHE') + "/" + pkg_name + '/build'
    os.chdir(cache_directory)
    build_invocation = os.system('ninja -v && ninja install')
    return build_invocation
