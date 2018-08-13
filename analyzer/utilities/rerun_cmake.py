"""
"""

import os
from shutil import copytree
from  analyzer.utilities.check_env import check_env

def rerun_cmake(pkg_name):
    """
    """
    check_env()
    cache_directory = os.getenv('ROOT_PKG_CACHE') + "/" + pkg_name + '/build'
    try:
        if not os.path.exists(cache_directory):
            os.system('mkdir -p %s' %  cache_directory)
    except OSError as e:
        print "Error: %s - %s." % (e.filename, e.strerror)
    os.chdir(cache_directory)
    cmake_reinvocation = os.system('cmake -DCMAKE_INSTALL_PREFIX=%s/%s/install \
    -DCMAKE_MODULE_PATH=%s/etc/cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=On \
    -DCMAKE_CXX_STANDARD=14 -GNinja \
    ../pkg-source' % (os.getenv('ROOT_PKG_CACHE'), pkg_name, os.getenv('ROOTSYS')))
    return cmake_reinvocation
