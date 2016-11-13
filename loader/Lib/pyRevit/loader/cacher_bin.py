import os.path as op
import pickle

from ..logger import get_logger
logger = get_logger(__name__)

from ..config import USER_TEMP_DIR, PYREVIT_ASSEMBLY_NAME, HASH_VALUE_PARAM, HASH_VERSION_PARAM, SUB_CMP_KEY
from ..exceptions import PyRevitCacheError, PyRevitCacheReadError, PyRevitCacheWriteError


loaded_packages = []


def _get_cache_file(cached_pkg):
    return op.join(USER_TEMP_DIR, '{}_cache_{}.pickle'.format(PYREVIT_ASSEMBLY_NAME, cached_pkg.name))


def _cleanup_cache_files():
    # todo: cleanup cache files?
    pass


def update_cache(parsed_pkg):
    try:
        logger.debug('Writing cache for: {}'.format(parsed_pkg))
        cache_file = _get_cache_file(parsed_pkg)
        logger.debug('Cache file is: {}'.format(cache_file))
        with open(op.join(USER_TEMP_DIR, cache_file), 'wb') as bin_cache_file:
            pickle.dump(parsed_pkg, bin_cache_file, pickle.HIGHEST_PROTOCOL)
    except Exception as err:
        raise PyRevitCacheWriteError('Error writing cache for: {} | {}'.format(parsed_pkg, err))


def get_cached_package(installed_pkg):
    for loaded_pkg in loaded_packages:
        if loaded_pkg.unique_name == installed_pkg.unique_name:
            return loaded_pkg

    try:
        logger.debug('Reading cache for: {}'.format(installed_pkg))
        cache_file = _get_cache_file(installed_pkg)
        logger.debug('Cache file is: {}'.format(cache_file))
        with open(op.join(USER_TEMP_DIR, cache_file), 'rb') as bin_cache_file:
            installed_pkg = pickle.load(bin_cache_file)
    except Exception as err:
        raise PyRevitCacheReadError('Error reading cache for: {} | {}'.format(installed_pkg, err))

    return installed_pkg


def is_cache_valid(pkg):
    try:
        cached_pkg = get_cached_package(pkg)    # type: Package
        logger.debug('Package cache version is: {} for: {}'.format(pkg.hash_version, pkg))
        cache_version_valid = cached_pkg.hash_version == pkg.hash_version

        logger.debug('Package hash value is: {} for: {}'.format(pkg.hash_value, pkg))
        cache_hash_valid = cached_pkg.hash_value == pkg.hash_value

        # add loaded package to list so it can be recovered later
        if cache_version_valid and cache_hash_valid:
            loaded_packages.append(cached_pkg)

        # cache is valid if both version and hash value match
        return cache_version_valid and cache_hash_valid

    except PyRevitCacheReadError as err:
        logger.debug(err)
        return False

    except Exception as err:
        logger.debug('Error determining cache validity: {} | {}'.format(pkg, err))
