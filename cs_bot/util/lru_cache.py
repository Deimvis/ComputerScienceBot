import time
from copy import deepcopy
from collections import OrderedDict


class LRUCache:
    def __init__(self, max_size=128, default_value=None):
        self._cache = OrderedDict()
        self._max_size = max_size
        self._default_value = default_value

    def __getitem__(self, key):
        if key in self._cache:
            self._cache.move_to_end(key)
        else:
            if len(self._cache) >= self._max_size:
                self._cache.popitem(last=False)
            self._cache[key] = deepcopy(self._default_value)
        return self._cache[key]

    def __setitem__(self, key, value):
        if key in self._cache:
            self._cache.move_to_end(key)
        elif len(self._cache) >= self._max_size:
            self._cache.popitem(last=False)
        self._cache[key] = value

    def __delitem__(self, key):
        del self._cache[key]

    def __iter__(self):
        return iter(self._cache)


class TimeBoundedLRUCache:
    'LRUCache that invalidate old entries'

    def __init__(self, max_size=128, ttl=3600):
        self._cache = OrderedDict()
        self._max_size = max_size
        self._add_ts = {}
        self._ttl = ttl

    def is_expired(self, key):
        return int(time.time()) > self._add_ts[key] + self._ttl

    def _remove_old_entries(self):
        expired_keys = []
        for key in self._cache:
            if self.is_expired(key):
                expired_keys.append(key)
        for key in expired_keys:
            del self._cache[key]
            del self._add_ts[key]

    def __getitem__(self, key, default=None):
        if key in self._cache:
            if self.is_expired(key):
                del self._cache[key]
                del self._add_ts[key]
            else:
                self._cache.move_to_end(key)
                return self._cache[key]
        return default

    def __setitem__(self, key, value):
        if key in self._cache:
            self._cache.move_to_end(key)
        elif len(self._cache) >= self._max_size:
            expired_key, expired_value = self._cache.popitem(last=False)
            del self._add_ts[expired_key]
        self._cache[key] = value
        self._add_ts[key] = int(time.time())

    def __delitem__(self, key):
        del self._cache[key]
        del self._add_ts[key]

    def __iter__(self):
        self._remove_old_entries()
        return iter(self._cache)
