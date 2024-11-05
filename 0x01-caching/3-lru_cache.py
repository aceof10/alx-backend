#!/usr/bin/env python3
"""LRU caching"""
BaseCaching = __import__("base_caching").BaseCaching


class LRUCache(BaseCaching):
    """
    LRUCache implements a caching system using the
    Least Recently Used (LRU) policy.
    """
    def __init__(self):
        """constructor"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Add an item to the cache using the LRU policy."""
        if key and item:
            if key in self.cache_data:
                self.order.remove(key)
            self.cache_data[key] = item
            self.order.append(key)
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                del_key = self.order.pop(0)
                del self.cache_data[del_key]
                print("DISCARD: {}".format(del_key))

    def get(self, key):
        """Retrieve an item from the cache."""
        if key in self.cache_data:
            self.order.remove(key)
            self.order.append(key)
            return self.cache_data[key]
        return None
