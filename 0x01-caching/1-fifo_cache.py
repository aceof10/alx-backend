#!/urs/bin/env python3
"""FIFOCache module"""
BaseCaching = __import__("base_caching").BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFO caching system that removes the oldest item
    when the limit is exceeded.
    """
    def __init__(self):
        """constructor"""
        super().__init__()
        self.cache_list = []

    def put(self, key, item):
        """Add an item to the cache, removing the oldest entry if needed."""
        if key and item:
            if key in self.cache_data:
                self.cache_data[key] = item
                return
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discard = self.cache_list.pop(0)
                del self.cache_data[discard]
                print("DISCARD: {}".format(discard))

            self.cache_data[key] = item
            self.cache_list.append(key)

    def get(self, key):
        """Retrieve an item from the cache."""
        return self.cache_data.get(key, None)
