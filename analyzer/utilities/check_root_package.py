"""
"""

import os
from  analyzer.utilities.check_env import check_env

def check_root_package(pkg_name, rootsources):
    """
    """
    check_env()
    count = os.system('find %s -type d -name "%s"' % (rootsources, pkg_name))
    if bool(count):
        return True
