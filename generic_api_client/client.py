"""
Python client for generic API services.
"""

from collections import defaultdict
import logging

import requests

try:
    import requests_cache
    caching_avail = True
except ImportError:
    caching_avail = False


__version__ = '0.0.1'

logger = logging.getLogger(__name__)

class FoodResult:
    def __init__(self):
        pass

class BaseClient:
    """
    The base client for the an API web service.
    """

    def __init__(self, url=None):
        if url is None:
            url = self._default_url
        self.url = url
        self._cached = False
        self.app_id = self._app_id
        self.app_key = self._app_key

    def _get(self, url, params=None, verbose=True):
        params = params or {}
        res = requests.get(url, params=params)
        from_cache = getattr(res, 'from_cache', False)
        return from_cache, res

    def _post(self, url, params, verbose=True):
        res = requests.post(url, json=params)
        from_cache = getattr(res, 'from_cache', False)
        ret = res.json()
        return from_cache, ret

    def _endpoint(self, q, **kwargs):
        """ Return the query result.
        This is the wrapper for the POST query of a API web service.

        :param q: a query string describing a question.
        :type q: str
        """
        _url = self.url
        #TODO: Build json params
        params = None

        verbose = kwargs.pop('verbose', True)
        from_cache, out = self._get(_url, params=params, verbose=verbose)
        if out.status_code == 401:
            logger.error('Invalid food api key or other get param.')
            raise requests.exceptions.InvalidURL
        if verbose and from_cache:
            print('Result from cache.')
        return out.json()

    def _set_caching(self, cache_db=None, verbose=True, **kwargs):
        '''Installs a local cache for all requests.
            **cache_db** is the path to the local sqlite cache database.'''
        if caching_avail:
            if cache_db is None:
                cache_db = self._default_cache_file
            requests_cache.install_cache(
                cache_name=cache_db, allowable_methods=(
                    'GET', 'POST'), **kwargs)
            self._cached = True
            if verbose:
                print(
                    '[ Future queries will be cached in "{0}" ]'.format(
                        os.path.abspath(
                            cache_db + '.sqlite')))
        else:
            print("Error: The requests_cache python module is required to use request caching.")
            print("See - https://requests-cache.readthedocs.io/en/latest/user_guide.html#installation")
        return

    def _stop_caching(self):
        '''Stop caching.'''
        if self._cached and caching_avail:
            requests_cache.uninstall_cache()
            self._cached = False
        return

    def _clear_cache(self):
        ''' Clear the globally installed cache. '''
        try:
            requests_cache.clear()
        except AttributeError:
            # requests_cache is not enabled
            print("requests_cache is not enabled. Nothing to clear.")
