import pickle
import os
import time

"""
    @summary:
    Cache the suspected url that has pattern
    Use Time-to-live cache (TTL)
    As the crawler process, remove any urls that confirmed
"""
class TrapUrlCache:
    def __init__(self, ttl=900) -> None:
        self.ttl = ttl
        self.cache_file = os.path.join("data", "trap_cache.pkl")
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        try:
            with open(self.cache_file, "rb") as file:
                self.loaded_cache = pickle.load(file)
        except FileNotFoundError:
            self.loaded_cache = {}  # Replace with file

    def set_trap_url(self, key, value):
        self.loaded_cache[key] = {
            "isTrap": value,
            "timestamp": time.time()
        }
        with open(self.cache_file, 'wb') as file:
            pickle.dump(self.loaded_cache, file)

    def is_trap_url(self, key):
        
        if key in self.loaded_cache:
            entry = self.loaded_cache[key]
            if time.time() - entry["timestamp"] <= self.ttl:
                return entry["isTrap"]
            else:
                del self.loaded_cache[key]
                with open(self.cache_file, 'wb') as file:
                    pickle.dump(self.loaded_cache, file)
        return None


trap_cache = TrapUrlCache()
