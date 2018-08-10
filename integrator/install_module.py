"""
"""

import os
from analyzer.utilities.check_env import check_env

#FIXME: add prepare_pkg()
def install_module(module_name):
    """
    """
    check_env()
    archive_dir = module_name + "_module_source"
    cd_cache_dir = os.getenv('ROOT_PKG_CACHE') + "/" + module_name
    os.chdir(cd_cache_dir)
    if cd_cache_dir != None:
        os.system('unzip -l %s.zip | sed "1,3d;$d" | sed ""$d"' % (module_name))
        os.system('unzip %s.zip -d %s/$pkg_name/' % (module_name, os.getenv('ROOT_PKG_PATH')))
        return True
