"""
"""

import os
from shutil import copytree
from  analyzer.utilities.check_env import check_env

def prepare_env_package(pkg_name, path):
    """
    """
    check_env()
    target_cmake = "pkg-source/CMakeLists.txt"
    build_directory = os.getenv('ROOT_PKG_CACHE') + "/" + pkg_name
    print("[root-get] Module directory: %s" % (build_directory))
    try:
        if os.path.exists(build_directory):
            os.removedirs(build_directory)
    except:
        pass
    os.system('mkdir -p %s' %  build_directory)
    os.chdir(build_directory)
    pkg_source = build_directory + "/pkg-source"
    copytree(path, pkg_source)
    print os.listdir(pkg_source)
    os.system('echo "include(RootFramework)\n$(cat %s)" > "%s"' % (target_cmake, target_cmake))
    os.system('echo "cmake_minimum_required(VERSION 3.7)\n$(cat %s)" > "%s"' % (target_cmake, target_cmake))
    cmake_cache = build_directory + '/build'
    print("[root-get] Module CMake build directory: %s" % (cmake_cache))
    os.system('mkdir -p %s' %  cmake_cache)
    os.chdir(cmake_cache)
    cmake = os.system('cmake -DCMAKE_INSTALL_PREFIX=%s/%s/install \
    -DCMAKE_MODULE_PATH=%s/etc/cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=On \
    -DCMAKE_CXX_STANDARD=14 -GNinja \
    ../pkg-source' % (os.getenv('ROOT_PKG_CACHE'), pkg_name, os.getenv('ROOTSYS')))
    return cmake
