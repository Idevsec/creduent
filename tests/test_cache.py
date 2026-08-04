import time
import pytest
from registry.cache import CreduentCache
from unittest.mock import patch

def test_cache_set_and_get():
    cache = CreduentCache(max_size=10, active_ttl=2, revoked_ttl=2)
    
    # Test setting valid attestation
    cache.set("agent://test1", {"status": "active"})
    assert cache.get("agent://test1") == {"status": "active"}

def test_cache_missing_logic():
    cache = CreduentCache(max_size=10, active_ttl=2, revoked_ttl=2)
    
    # Test setting missing
    cache.set("agent://test2", "MISSING", is_negative=True)
    assert cache.get("agent://test2") == "MISSING"

def test_cache_ttl_expiration():
    cache = CreduentCache(max_size=10, active_ttl=1, revoked_ttl=1)
    
    cache.set("agent://valid", {"status": "active"})
    
    # Immediately available
    assert cache.get("agent://valid") == {"status": "active"}
    
    # Wait for expiration
    time.sleep(1.1)
    
    # Should be expired
    assert cache.get("agent://valid") is None

def test_cache_negative_ttl_expiration():
    cache = CreduentCache(max_size=10)
    
    # Mock time to test hardcoded 60s negative ttl
    with patch("time.time") as mock_time:
        mock_time.return_value = 1000.0
        cache.set("agent://missing", "MISSING", is_negative=True)
        assert cache.get("agent://missing") == "MISSING"
        
        # Advance time by 61 seconds
        mock_time.return_value = 1061.0
        assert cache.get("agent://missing") is None

def test_cache_lru_eviction():
    cache = CreduentCache(max_size=2, active_ttl=10, revoked_ttl=10)
    
    cache.set("agent://test1", {"val": 1})
    cache.set("agent://test2", {"val": 2})
    
    # Both should be present
    assert cache.get("agent://test1") == {"val": 1}
    assert cache.get("agent://test2") == {"val": 2}
    
    # Add a third, should evict the least recently used (test1 since we just got test2)
    cache.set("agent://test3", {"val": 3})
    
    assert cache.get("agent://test1") is None
    assert cache.get("agent://test2") == {"val": 2}
    assert cache.get("agent://test3") == {"val": 3}

def test_cache_delete():
    cache = CreduentCache(max_size=10, active_ttl=10, revoked_ttl=10)
    
    cache.set("agent://test1", {"val": 1})
    assert cache.get("agent://test1") == {"val": 1}
    
    cache.delete("agent://test1")
    assert cache.get("agent://test1") is None
    
    # Deleting non-existent should not fail
    cache.delete("agent://does_not_exist")

def test_cache_clear():
    cache = CreduentCache(max_size=10, active_ttl=10, revoked_ttl=10)
    
    cache.set("agent://test1", {"val": 1})
    cache.set("agent://test2", {"val": 2})
    
    cache.clear()
    
    assert cache.get("agent://test1") is None
    assert cache.get("agent://test2") is None
