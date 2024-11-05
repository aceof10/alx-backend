#!/usr/bin/env python3
"""Basic dictionary"""
BaseCaching = __import__("base_caching").BaseCaching


class BasicCache(BaseCaching):
    """Basic caching system with no limit."""

    def put(self, key, item):
        """Add an item to the cache."""
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """Retrieve an item from the cache."""
        return self.cache_data.get(key)
