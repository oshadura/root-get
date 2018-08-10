"""
"""

import os
from analyzer.utilities.check_env import check_env

#FIXME: add prepare_pkg()
def sedfile_utility(module_name):
    """
    """
    check_env()
    archive_dir = module_name + "_module_source"
    cd_cache_dir = os.getenv('ROOT_PKG_CACHE') + "/" + module_name + "/build"
    os.chdir(cd_cache_dir)
    if cd_cache_dir != None:
        os.system('mkdir -p %s' % (archive_dir))
        os.system('cp -R install/* %s' % (archive_dir))
        os.system('mkdir -p  %s' % (archive_dir))
        os.system('cp -R $ROOTSYS/README %s' % (archive_dir))
        os.system('mkdir -p %s' % (archive_dir))
        os.system('cp -R $ROOTSYS/LICENSE %s' % (archive_dir))
        os.chdir(archive_dir)
        os.system('zip -r ../%s.zip *' % (module_name))
        return True
    else:
        return False
