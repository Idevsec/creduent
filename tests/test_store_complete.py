import os
import sys
import json
import time
import pytest
from unittest.mock import patch, MagicMock
from registry import store


@pytest.fixture(autouse=True)
def clean_redis_cache():
    store._redis_client_cache = None
    if hasattr(store, 'clear_cache'): store.clear_cache()
    yield
    store._redis_client_cache = None
    if hasattr(store, 'clear_cache'): store.clear_cache()


@pytest.fixture
def tmp_db_paths(tmp_path):
    reg_db = tmp_path / "reg_db.json"
    wh_db = tmp_path / "webhooks_db.json"
    with patch.object(store, "DB_PATH", str(reg_db)), \
         patch.object(store, "WEBHOOKS_DB_PATH", str(wh_db)):
        yield reg_db, wh_db


# --- File lock tests ---

def test_file_lock_unix(tmp_path):
    f_path = str(tmp_path / "test.txt")
    with store.file_lock(f_path) as f:
        f.write("test")
    assert not os.path.exists(f_path + ".lock")


def test_file_lock_unix_error(tmp_path):
    f_path = str(tmp_path / "test_err.txt")
    if os.name != "nt":
        import fcntl
        with patch("fcntl.flock", side_effect=OSError("lock error")), \
             patch("time.sleep", return_value=None):
            with pytest.raises(IOError, match="Could not acquire registry file lock on Unix"):
                with store.file_lock(f_path):
                    pass


def test_file_lock_windows_success(tmp_path):
    f_path = str(tmp_path / "test_win.txt")
    mock_msvcrt = MagicMock()
    with patch("os.name", "nt"), \
         patch.dict(sys.modules, {"msvcrt": mock_msvcrt}):
        with store.file_lock(f_path) as f:
            f.write("windows test")
        assert mock_msvcrt.locking.called


def test_file_lock_windows_error(tmp_path):
    f_path = str(tmp_path / "test_win_err.txt")
    mock_msvcrt = MagicMock()
    mock_msvcrt.locking.side_effect = IOError("win lock error")
    with patch("os.name", "nt"), \
         patch.dict(sys.modules, {"msvcrt": mock_msvcrt}), \
         patch("time.sleep", return_value=None):
        with pytest.raises(IOError, match="Could not acquire registry file lock on Windows"):
            with store.file_lock(f_path):
                pass


# --- Redis config & diagnosis tests ---

def test_is_redis_configured_and_diagnose():
    with patch.dict(os.environ, {}, clear=True):
        assert not store.is_redis_configured()
        store.diagnose_redis()  # ensure no crash when empty

    with patch.dict(os.environ, {"UPSTASH_REDIS_REST_URL": "YOUR_URL", "UPSTASH_REDIS_REST_TOKEN": "YOUR_TOKEN"}):
        assert not store.is_redis_configured()
        store.diagnose_redis()

    with patch.dict(os.environ, {"UPSTASH_REDIS_REST_URL": "https://redis.example.com", "UPSTASH_REDIS_REST_TOKEN": "valid_token_123456"}):
        assert store.is_redis_configured()
        store.diagnose_redis()


def test_get_redis_client():
    mock_upstash = MagicMock()
    mock_client = MagicMock()
    mock_upstash.Redis.return_value = mock_client
    with patch.dict(sys.modules, {"upstash_redis": mock_upstash}), \
         patch.dict(os.environ, {"UPSTASH_REDIS_REST_URL": "http://url", "UPSTASH_REDIS_REST_TOKEN": "token"}):
        client1 = store.get_redis_client()
        client2 = store.get_redis_client()
        assert client1 is client2
        assert client1 is mock_client


# --- Attestation tests ---

def test_attestation_local_file_lifecycle(tmp_db_paths):
    reg_db, _ = tmp_db_paths
    with patch("registry.store.is_redis_configured", return_value=False):
        assert store.get_attestation("agent-1") is None
        assert store.list_agents() == []

        att = {"agent_id": "agent-1", "level": "verified"}
        store.save_attestation("agent-1", att)
        assert store.get_attestation("agent-1") == att
        assert store.list_agents() == [att]

        store.revoke_agent("agent-1")
        assert store.get_attestation("agent-1")["level"] == "revoked"

        # Revoke non-existent agent creates revoked entry
        store.revoke_agent("agent-2")
        assert store.get_attestation("agent-2")["level"] == "revoked"


def test_attestation_local_corrupted(tmp_db_paths):
    reg_db, _ = tmp_db_paths
    with patch("registry.store.is_redis_configured", return_value=False):
        reg_db.write_text("not valid json", encoding="utf-8")
        assert store.get_attestation("agent-1") is None
        assert store.list_agents() == []

        # Saving over corrupted DB resets to empty dict then saves
        store.save_attestation("agent-1", {"agent_id": "agent-1"})
        assert store.get_attestation("agent-1") == {"agent_id": "agent-1"}


def test_attestation_redis_lifecycle():
    mock_client = MagicMock()
    with patch("registry.store.is_redis_configured", return_value=True), \
         patch("registry.store.get_redis_client", return_value=mock_client):
        
        att = {"agent_id": "agent-1", "level": "verified"}
        store.save_attestation("agent-1", att)
        mock_client.hset.assert_called_with("creduent:agents", "agent-1", json.dumps(att))

        if hasattr(store, 'clear_cache'): store.clear_cache()

        # Test get_attestation with dict vs string vs invalid json
        mock_client.hget.return_value = att
        assert store.get_attestation("agent-1") == att

        if hasattr(store, 'clear_cache'): store.clear_cache()
        mock_client.hget.return_value = json.dumps(att)
        assert store.get_attestation("agent-1") == att

        if hasattr(store, 'clear_cache'): store.clear_cache()
        mock_client.hget.return_value = "invalid json"
        assert store.get_attestation("agent-1") == "invalid json"

        if hasattr(store, 'clear_cache'): store.clear_cache()
        mock_client.hget.return_value = None
        assert store.get_attestation("agent-1") is None

        # Test list_agents
        mock_client.hvals.return_value = [att, json.dumps({"agent_id": "agent-2"}), "invalid", "", None]
        agents = store.list_agents()
        assert len(agents) == 3


def test_attestation_redis_errors():
    mock_client = MagicMock()
    mock_client.hset.side_effect = Exception("redis error")
    mock_client.hget.side_effect = Exception("redis error")
    mock_client.hvals.side_effect = Exception("redis error")
    with patch("registry.store.is_redis_configured", return_value=True), \
         patch("registry.store.get_redis_client", return_value=mock_client):
        with pytest.raises(Exception, match="redis error"):
            store.save_attestation("agent-1", {"a": 1})
        assert store.get_attestation("agent-1") is None
        assert store.list_agents() == []


# --- Webhooks tests ---

def test_webhooks_local_lifecycle(tmp_db_paths):
    _, wh_db = tmp_db_paths
    with patch("registry.store.is_redis_configured", return_value=False):
        assert store.get_webhook_config("agent-1") is None
        assert store.get_webhook("agent-1") is None
        assert store.list_webhooks_configs() == {}
        assert store.list_webhooks() == {}

        secret = store.save_webhook("agent-1", "https://wh.example.com")
        assert secret.startswith("whsec_")

        cfg = store.get_webhook_config("agent-1")
        assert cfg["url"] == "https://wh.example.com"
        assert cfg["secret"] == secret
        assert store.get_webhook("agent-1") == "https://wh.example.com"

        configs = store.list_webhooks_configs()
        assert "agent-1" in configs
        assert store.list_webhooks() == {"agent-1": "https://wh.example.com"}

        store.delete_webhook("agent-1")
        assert store.get_webhook_config("agent-1") is None
        # Deleting non-existent should not fail
        store.delete_webhook("agent-1")


def test_webhooks_local_corrupted_and_legacy(tmp_db_paths):
    _, wh_db = tmp_db_paths
    with patch("registry.store.is_redis_configured", return_value=False):
        wh_db.write_text("corrupted json", encoding="utf-8")
        assert store.get_webhook_config("agent-1") is None
        assert store.list_webhooks_configs() == {}
        store.delete_webhook("agent-1")  # should handle corrupted without error

        # Write legacy URL directly into DB
        legacy_data = {
            "agent-old": "https://legacy.example.com",
            "agent-dict-no-sec": {"url": "https://no-sec.example.com"},
            "agent-json-str-no-sec": '{"url": "https://json-str.example.com"}'
        }
        wh_db.write_text(json.dumps(legacy_data), encoding="utf-8")
        
        cfg = store.get_webhook_config("agent-old")
        assert cfg["url"] == "https://legacy.example.com"
        assert cfg["secret"].startswith("whsec_legacy_")

        cfg2 = store.get_webhook_config("agent-dict-no-sec")
        assert cfg2["url"] == "https://no-sec.example.com"

        cfg3 = store.get_webhook_config("agent-json-str-no-sec")
        assert cfg3["url"] == "https://json-str.example.com"

        all_cfgs = store.list_webhooks_configs()
        assert len(all_cfgs) == 3
        assert store.list_webhooks() == {
            "agent-old": "https://legacy.example.com",
            "agent-dict-no-sec": "https://no-sec.example.com",
            "agent-json-str-no-sec": "https://json-str.example.com"
        }


def test_webhooks_redis():
    mock_client = MagicMock()
    with patch("registry.store.is_redis_configured", return_value=True), \
         patch("registry.store.get_redis_client", return_value=mock_client):
        
        store.save_webhook("agent-1", "https://redis-wh.com")
        assert mock_client.hset.called

        # test hget returning bytes or string or dict
        mock_client.hget.return_value = b'{"url": "https://redis-wh.com", "secret": "whsec_abc"}'
        assert store.get_webhook_config("agent-1") == {"url": "https://redis-wh.com", "secret": "whsec_abc"}

        mock_client.hget.return_value = {"url": "https://dict.com"}
        assert store.get_webhook_config("agent-1")["url"] == "https://dict.com"

        # list_webhooks_configs returning bytes keys and values
        mock_client.hgetall.return_value = {
            b"agent-1": b'{"url": "https://redis-wh.com", "secret": "whsec_abc"}',
            "agent-2": "https://legacy-redis.com",
            "agent-3": {"url": "https://dict-redis.com"}
        }
        cfgs = store.list_webhooks_configs()
        assert len(cfgs) == 3
        assert cfgs["agent-1"]["url"] == "https://redis-wh.com"

        store.delete_webhook("agent-1")
        mock_client.hdel.assert_called_with("creduent:webhooks", "agent-1")


def test_webhooks_redis_errors():
    mock_client = MagicMock()
    mock_client.hset.side_effect = Exception("redis hset error")
    mock_client.hget.side_effect = Exception("redis hget error")
    mock_client.hgetall.side_effect = Exception("redis hgetall error")
    mock_client.hdel.side_effect = Exception("redis hdel error")
    with patch("registry.store.is_redis_configured", return_value=True), \
         patch("registry.store.get_redis_client", return_value=mock_client):
        with pytest.raises(Exception, match="redis hset error"):
            store.save_webhook("a", "b")
        assert store.get_webhook_config("a") is None
        assert store.list_webhooks_configs() == {}
        store.delete_webhook("a")


# --- Challenge tests ---

def test_challenges_local_memory():
    with patch("registry.store.is_redis_configured", return_value=False):
        store.CHALLENGE_DB.clear()
        
        # save challenge
        store.save_challenge("agent-1", "nonce1", {"data": 123})
        assert "challenge:agent-1:nonce1" in store.CHALLENGE_DB

        # get challenge valid
        val = store.get_challenge("agent-1", "nonce1")
        assert val == {"data": 123}

        # get challenge non-existent
        assert store.get_challenge("agent-1", "nonce2") is None

        # delete challenge
        store.delete_challenge("agent-1", "nonce1")
        assert "challenge:agent-1:nonce1" not in store.CHALLENGE_DB

        # test expiry trimming
        store.CHALLENGE_DB["challenge:expired:1"] = ({"old": True}, time.time() - 10)
        assert store.get_challenge("expired", "1") is None

        store.CHALLENGE_DB["challenge:expired:2"] = ({"old": True}, time.time() - 10)
        store._prune_expired_challenges()
        assert "challenge:expired:2" not in store.CHALLENGE_DB


def test_challenges_redis_and_fallback():
    mock_client = MagicMock()
    with patch("registry.store.is_redis_configured", return_value=True), \
         patch("registry.store.get_redis_client", return_value=mock_client):
        
        store.save_challenge("a", "n", {"val": 1})
        mock_client.set.assert_called_once()

        mock_client.get.return_value = json.dumps({"val": 1})
        assert store.get_challenge("a", "n") == {"val": 1}

        mock_client.get.return_value = "invalid json"
        assert store.get_challenge("a", "n") == "invalid json"

        mock_client.get.return_value = None
        assert store.get_challenge("a", "n") is None

        store.delete_challenge("a", "n")
        mock_client.delete.assert_called_with("challenge:a:n")

        # Test redis exception falling back to local memory
        mock_client.set.side_effect = Exception("redis error")
        mock_client.get.side_effect = Exception("redis error")
        mock_client.delete.side_effect = Exception("redis error")
        
        store.CHALLENGE_DB.clear()
        store.save_challenge("fb", "n1", {"fb": True})
        assert "challenge:fb:n1" in store.CHALLENGE_DB
        
        val = store.get_challenge("fb", "n1")
        assert val == {"fb": True}

        store.delete_challenge("fb", "n1")
        assert "challenge:fb:n1" not in store.CHALLENGE_DB
