#!/usr/bin/env python3
"""LFU Caching"""
from collections import defaultdict
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache implements a caching system
    using the Least Frequently Used (LFU) policy.
    """
    def __init__(self):
        """constructor"""
        super().__init__()
        self.freq_count = defaultdict(int)
        self.frequency = defaultdict(list)
        self.min_freq = 0

    def put(self, key, item):
        """Add an item to the cache using the LFU policy."""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.freq_count[key] += 1
        else:
            if len(self.cache_data) >= self.MAX_ITEMS:
                while self.frequency[self.min_freq] == []:
                    self.min_freq += 1
                discard = self.frequency[self.min_freq].pop(0)
                del self.cache_data[discard]
                del self.freq_count[discard]
                print("DISCARD: {}".format(discard))

            self.cache_data[key] = item
            self.freq_count[key] = 1
            self.min_freq = 1

        self.frequency[self.freq_count[key]].append(key)

    def get(self, key):
        """Retrieve an item from the cache."""
        if key is None or key not in self.cache_data:
            return None

        self.freq_count[key] += 1
        self.frequency[self.freq_count[key]].append(key)

        prev_freq = self.freq_count[key] - 1
        self.frequency[prev_freq].remove(key)

        if not self.frequency[self.min_freq]:
            self.min_freq += 1

        return self.cache_data[key]
