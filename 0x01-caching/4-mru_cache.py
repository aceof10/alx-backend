#!/usr/bin/env python3
"""MRU caching"""
BaseCaching = __import__("base_caching").BaseCaching


class MRUCache(BaseCaching):
    """
    MRUCache implements a caching system
    using the Most Recently Used (MRU) policy.
    """

    def __init__(self):
        """constructor"""
        super().__init__()
        self.mru_keys = []

    def put(self, key, item):
        """Add an item to the cache using the MRU policy."""
        if key and item:
            self.cache_data[key] = item
            if key in self.mru_keys:
                self.mru_keys.remove(key)
            self.mru_keys.append(key)
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                mru_key = self.mru_keys.pop(-2)
                del self.cache_data[mru_key]
                print("DISCARD:", mru_key)

    def get(self, key):
        """Retrieve an item from the cache."""
        if key in self.cache_data:
            self.mru_keys.remove(key)
            self.mru_keys.append(key)
            return self.cache_data[key]
        return None
