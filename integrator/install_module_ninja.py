"""
"""

import os
from analyzer.utilities.check_env import check_env

#FIXME: add prepare_pkg()
def install_module_ninja(module_name):
    """
    """
    check_env()
    archive_dir = module_name + "_module_source"
    cd_cache_dir = os.getenv('ROOT_PKG_CACHE') + "/" + module_name + "/build"
    os.chdir(cd_cache_dir)
    ninja_invocation = os.system('ninja install')
    return ninja_invocation
