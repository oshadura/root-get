"""
"""

import os
import logging

module_logger = logging.getLogger('analyzer.utilities.check_env')

def check_env():
    """
    """
    try:
        root_cache = os.getenv('ROOT_PKG_CACHE')
    except ValueError as err:
         module_logger.error("ROOT_PKG_CACHE [cache directory for packages] was not defined! \
        Please define it.")
    try:
        root_cache = os.getenv('ROOT_SOURCES')
    except ValueError as err:
         module_logger.error("ROOT_SOURCES [ROOT sources] was not defined! Please define it.")
    try:
        root_cache = os.getenv('ROOT_MODULES')
    except ValueError as err:
         module_logger.error("ROOT_MODULES [directory with module's configuration files] \
        was not defined! Please define it.")
    try:
        root_cache = os.getenv('ROOTSYS')
    except ValueError as err:
         module_logger.error("ROOTSYS was not defined! Please source thisroot.sh script.")
    return root_cache
