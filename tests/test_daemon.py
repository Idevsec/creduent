import os
import json
import urllib.error
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock, mock_open
import pytest

import registry.daemon as daemon


def test_logger(capsys):
    daemon.logging.info("test info")
    daemon.logging.warning("test warn")
    daemon.logging.error("test error")
    captured = capsys.readouterr()
    assert "[INFO] test info" in captured.out
    assert "[WARNING] test warn" in captured.out
    assert "[ERROR] test error" in captured.out


def test_is_redis_configured(monkeypatch):
    monkeypatch.delenv("UPSTASH_REDIS_REST_URL", raising=False)
    monkeypatch.delenv("UPSTASH_REDIS_REST_TOKEN", raising=False)
    assert not daemon._is_redis_configured()

    monkeypatch.setenv("UPSTASH_REDIS_REST_URL", "https://example.com")
    monkeypatch.setenv("UPSTASH_REDIS_REST_TOKEN", "YOUR_TOKEN_HERE")
    assert not daemon._is_redis_configured()

    monkeypatch.setenv("UPSTASH_REDIS_REST_TOKEN", "valid_token")
    assert daemon._is_redis_configured()


def test_get_redis_client(monkeypatch):
    monkeypatch.setenv("UPSTASH_REDIS_REST_URL", "https://redis.com")
    monkeypatch.setenv("UPSTASH_REDIS_REST_TOKEN", "secret_token")
    mock_redis_cls = MagicMock()
    with patch.dict("sys.modules", {"upstash_redis": MagicMock(Redis=mock_redis_cls)}):
        client = daemon._get_redis_client()
        mock_redis_cls.assert_called_once_with(url="https://redis.com", token="secret_token")


def test_load_json_file(tmp_path):
    assert daemon._load_json_file(str(tmp_path / "non_existent.json")) == {}

    test_file = tmp_path / "test.json"
    test_file.write_text('{"foo": "bar"}', encoding="utf-8")
    assert daemon._load_json_file(str(test_file)) == {"foo": "bar"}

    bad_file = tmp_path / "bad.json"
    bad_file.write_text('{invalid_json', encoding="utf-8")
    assert daemon._load_json_file(str(bad_file)) == {}


def test_load_registry_and_webhooks_local(monkeypatch, tmp_path):
    monkeypatch.delenv("UPSTASH_REDIS_REST_URL", raising=False)
    monkeypatch.delenv("UPSTASH_REDIS_REST_TOKEN", raising=False)
    
    reg_path = tmp_path / "reg.json"
    wh_path = tmp_path / "wh.json"
    reg_path.write_text('{"agent1": {"status": "ok"}}', encoding="utf-8")
    wh_path.write_text('{"agent1": "http://wh.url"}', encoding="utf-8")
    
    monkeypatch.setattr(daemon, "REGISTRY_DB_PATH", str(reg_path))
    monkeypatch.setattr(daemon, "WEBHOOKS_DB_PATH", str(wh_path))
    
    assert daemon.load_registry() == {"agent1": {"status": "ok"}}
    assert daemon.load_webhooks() == {"agent1": "http://wh.url"}


def test_load_registry_redis(monkeypatch):
    monkeypatch.setenv("UPSTASH_REDIS_REST_URL", "https://redis.url")
    monkeypatch.setenv("UPSTASH_REDIS_REST_TOKEN", "redis_token")
    
    mock_client = MagicMock()
    mock_client.hgetall.return_value = {
        b"agent1": b'{"status": "active"}',
        "agent2": '{"status": "expired"}',
        b"agent3": "raw_string"
    }
    with patch.object(daemon, "_get_redis_client", return_value=mock_client):
        res = daemon.load_registry()
        assert res["agent1"] == {"status": "active"}
        assert res["agent2"] == {"status": "expired"}
        assert res["agent3"] == "raw_string"
        
    mock_client.hgetall.return_value = None
    with patch.object(daemon, "_get_redis_client", return_value=mock_client):
        assert daemon.load_registry() == {}

    mock_client.hgetall.side_effect = Exception("Redis error")
    with patch.object(daemon, "_get_redis_client", return_value=mock_client):
        assert daemon.load_registry() == {}


def test_load_webhooks_redis(monkeypatch):
    monkeypatch.setenv("UPSTASH_REDIS_REST_URL", "https://redis.url")
    monkeypatch.setenv("UPSTASH_REDIS_REST_TOKEN", "redis_token")
    
    mock_client = MagicMock()
    mock_client.hgetall.return_value = {
        b"agent1": b"http://wh1",
        "agent2": "http://wh2"
    }
    with patch.object(daemon, "_get_redis_client", return_value=mock_client):
        res = daemon.load_webhooks()
        assert res["agent1"] == "http://wh1"
        assert res["agent2"] == "http://wh2"
        
    mock_client.hgetall.return_value = None
    with patch.object(daemon, "_get_redis_client", return_value=mock_client):
        assert daemon.load_webhooks() == {}

    mock_client.hgetall.side_effect = Exception("Redis error")
    with patch.object(daemon, "_get_redis_client", return_value=mock_client):
        assert daemon.load_webhooks() == {}


def test_send_webhook_success_and_errors():
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        mock_response.__enter__.return_value.getcode.return_value = 200
        mock_urlopen.return_value = mock_response
        
        ok = daemon.send_webhook("agent1", "https://wh.com", "secret", "dom.com", "2026-09-01T00:00:00Z", 10)
        assert ok is True
        
        # Test fallback domain when domain is None
        ok = daemon.send_webhook("agent1", "https://wh.com", "secret", None, "2026-09-01T00:00:00Z", 10)
        assert ok is True

    # HTTPError
    with patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError("url", 500, "Error", {}, None)):
        assert daemon.send_webhook("agent1", "https://wh.com", "secret", "dom.com", "2026-09-01T00:00:00Z", 10) is False

    # URLError
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("No route")):
        assert daemon.send_webhook("agent1", "https://wh.com", "secret", "dom.com", "2026-09-01T00:00:00Z", 10) is False

    # Unexpected exception
    with patch("urllib.request.urlopen", side_effect=Exception("Unknown")):
        assert daemon.send_webhook("agent1", "https://wh.com", "secret", "dom.com", "2026-09-01T00:00:00Z", 10) is False

    # HMAC exception fallback
    with patch("hmac.new", side_effect=Exception("HMAC error")), \
         patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        mock_response.__enter__.return_value.getcode.return_value = 200
        mock_urlopen.return_value = mock_response
        ok = daemon.send_webhook("agent1", "https://wh.com", "secret", "dom.com", "2026-09-01T00:00:00Z", 10)
        assert ok is True


def test_main_idle_and_dotenv(monkeypatch):
    monkeypatch.delenv("VERCEL", raising=False)
    with patch("creduent.utils.load_dotenv", side_effect=Exception("dotenv fail")), \
         patch.object(daemon, "load_registry", return_value={}), \
         patch.object(daemon, "load_webhooks", return_value={}):
        daemon.main()
        
    monkeypatch.setenv("VERCEL", "1")
    with patch.object(daemon, "load_registry", return_value={}), \
         patch.object(daemon, "load_webhooks", return_value={}):
        daemon.main()


def test_main_processing(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    now = datetime.now(timezone.utc)
    
    expiring_date = (now + timedelta(days=15)).isoformat()
    expired_date = (now - timedelta(days=5)).isoformat()
    active_date = (now + timedelta(days=60)).isoformat()
    
    mock_reg = {
        "revoked_agent": {"level": "revoked"},
        "no_expiry_agent": {"level": "verified"},
        "bad_expiry_agent": {"expires_at": "invalid_date_str"},
        "expiring_dict_wh": {"expires_at": expiring_date, "domain": "dom1.com"},
        "expiring_str_wh": {"expires_at": expiring_date, "domain": "dom2.com"},
        "expiring_no_wh": {"expires_at": expiring_date, "domain": "dom3.com"},
        "expired_agent": {"expires_at": expired_date},
        "active_agent": {"expires_at": active_date},
    }
    
    mock_wh = {
        "expiring_dict_wh": {"url": "http://wh1.url", "secret": "sec1"},
        "expiring_str_wh": "http://wh2.url",
    }
    
    with patch.object(daemon, "load_registry", return_value=mock_reg), \
         patch.object(daemon, "load_webhooks", return_value=mock_wh), \
         patch.object(daemon, "send_webhook", side_effect=[True, False]) as mock_send:
        daemon.main()
        assert mock_send.call_count == 2


def test_main_entry_point(monkeypatch):
    with patch.object(daemon, "main", return_value=None) as mock_main:
        # Simulate import execution or script run
        daemon.main()
        mock_main.assert_called_once()
