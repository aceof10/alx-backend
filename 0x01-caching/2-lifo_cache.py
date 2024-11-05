#!/usr/bin/env python3
"""LIFOCache module"""
BaseCaching = __import__("base_caching").BaseCaching


class LIFOCache(BaseCaching):
    def __init__(self):
        """constructor"""
        super().__init__()
        self.cache_stack = []

    def put(self, key, item):
        """
        Add an item to the cache,
        removing the most recent entry if needed.
        """
        if key and item:
            if key in self.cache_data:
                self.cache_stack.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discard = self.cache_stack.pop()
                del self.cache_data[discard]
                print("DISCARD: {}".format(discard))

            self.cache_data[key] = item
            self.cache_stack.append(key)

    def get(self, key):
        """
        Retrieve an item from the cache
        """
        if key in self.cache_data:
            self.cache_stack.remove(key)
            self.cache_stack.append(key)
            return self.cache_data[key]
        return None
