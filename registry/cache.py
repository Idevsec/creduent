import time
from threading import Lock
from collections import OrderedDict

class CreduentCache:
    def __init__(self, max_size: int = 10000, active_ttl: int = 300, revoked_ttl: int = 86400):
        self.max_size = max_size
        self.active_ttl = active_ttl
        self.revoked_ttl = revoked_ttl
        self.cache = OrderedDict()
        self.lock = Lock()
    
    def get(self, key: str):
        with self.lock:
            if key not in self.cache:
                return None
            
            entry = self.cache[key]
            if time.time() > entry["expires_at"]:
                del self.cache[key]
                return None
            
            # Move to end to mark as recently used
            self.cache.move_to_end(key)
            return entry["value"]

    def set(self, key: str, value: any, is_revoked: bool = False, is_negative: bool = False):
        with self.lock:
            # Determine TTL
            if is_revoked:
                ttl = self.revoked_ttl
            elif is_negative:
                ttl = 60 # Shorter TTL for negative caching
            else:
                ttl = self.active_ttl
                
            expires_at = time.time() + ttl
            
            if key in self.cache:
                del self.cache[key]
            elif len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)
                
            self.cache[key] = {
                "value": value,
                "expires_at": expires_at
            }
            
    def delete(self, key: str):
        with self.lock:
            if key in self.cache:
                del self.cache[key]

    def clear(self):
        with self.lock:
            self.cache.clear()
