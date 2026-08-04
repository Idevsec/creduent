import base64
import json
import os
import secrets
import sys
import time
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from fastapi.testclient import TestClient
from fastapi import Request, HTTPException

from creduent.crypto import canonicalize
from registry.main import (
    app,
    get_client_ip,
    check_register_rate_limit,
    check_challenge_rate_limit,
    REGISTER_RATE_LIMIT_MAX,
    CHALLENGE_RATE_LIMIT_MAX,
)
import registry.main as main_mod
import registry.store as store_mod
import registry.signer as signer_mod


@pytest.fixture
def client(tmp_path, monkeypatch):
    registry_key = ed25519.Ed25519PrivateKey.generate()
    raw_key = registry_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    monkeypatch.setenv("CREDUENT_REGISTRY_KEY", base64.b64encode(raw_key).decode("utf-8"))
    monkeypatch.setenv("CREDUENT_ADMIN_KEY", "test-secret-key")
    monkeypatch.delenv("UPSTASH_REDIS_REST_URL", raising=False)
    monkeypatch.delenv("UPSTASH_REDIS_REST_TOKEN", raising=False)
    monkeypatch.delenv("VERCEL", raising=False)
    
    db_file = str(tmp_path / "test_main_comprehensive.json")
    wh_file = str(tmp_path / "webhooks_test_db.json")
    monkeypatch.setattr("registry.store.DB_PATH", db_file)
    monkeypatch.setattr("registry.store.WEBHOOKS_DB_PATH", wh_file)
    monkeypatch.setattr("registry.main.REGISTER_RATE_LIMIT_MAX", 10000)
    monkeypatch.setattr("registry.main.CHALLENGE_RATE_LIMIT_MAX", 10000)
    store_mod.CHALLENGE_DB.clear()
    
    for db_name in ("reg_rate_db", "chal_rate_db", "rate_db"):
        if hasattr(app, db_name):
            setattr(app, db_name, {})
            
    with TestClient(app) as c:
        yield c


def test_client_ip_and_rate_limits():
    # Test get_client_ip
    req_forwarded = MagicMock(spec=Request)
    req_forwarded.headers = {"X-Forwarded-For": "10.0.0.1, 10.0.0.2"}
    assert get_client_ip(req_forwarded) == "10.0.0.1"

    req_no_client = MagicMock(spec=Request)
    req_no_client.headers = {}
    req_no_client.client = None
    assert get_client_ip(req_no_client) == "unknown"

    # Rate limits with unknown IP return early
    check_register_rate_limit(req_no_client)
    check_challenge_rate_limit(req_no_client)

    req_client = MagicMock(spec=Request)
    req_client.headers = {}
    req_client.client = MagicMock(host="192.168.1.1")

    # VERCEL=1 without redis configured -> 500
    with patch.dict(os.environ, {"VERCEL": "1"}), patch("registry.main.is_redis_configured", return_value=False):
        with pytest.raises(HTTPException) as exc_info:
            check_register_rate_limit(req_client)
        assert exc_info.value.status_code == 500
        with pytest.raises(HTTPException) as exc_info:
            check_challenge_rate_limit(req_client)
        assert exc_info.value.status_code == 500

    # Redis branch
    mock_redis = MagicMock()
    with patch("registry.main.is_redis_configured", return_value=True), patch("registry.main.get_redis_client", return_value=mock_redis):
        # New entry
        mock_redis.get.return_value = None
        check_register_rate_limit(req_client)
        check_challenge_rate_limit(req_client)
        
        # Existing entry below max
        mock_redis.get.return_value = "1"
        check_register_rate_limit(req_client)
        check_challenge_rate_limit(req_client)

        # Reached max
        mock_redis.get.return_value = str(REGISTER_RATE_LIMIT_MAX)
        with pytest.raises(HTTPException) as exc_info:
            check_register_rate_limit(req_client)
        assert exc_info.value.status_code == 429

        mock_redis.get.return_value = str(CHALLENGE_RATE_LIMIT_MAX)
        with pytest.raises(HTTPException) as exc_info:
            check_challenge_rate_limit(req_client)
        assert exc_info.value.status_code == 429

        # Redis exception caught and ignored
        mock_redis.get.side_effect = Exception("Redis error")
        check_register_rate_limit(req_client)
        check_challenge_rate_limit(req_client)

    # In-memory rate limiting expiry and max
    with patch("registry.main.is_redis_configured", return_value=False):
        app.reg_rate_db = {"reg_limit:192.168.1.1": {"count": REGISTER_RATE_LIMIT_MAX, "expiry": time.time() + 1000}}
        with pytest.raises(HTTPException) as exc_info:
            check_register_rate_limit(req_client)
        assert exc_info.value.status_code == 429

        app.chal_rate_db = {"chal_limit:192.168.1.1": {"count": CHALLENGE_RATE_LIMIT_MAX, "expiry": time.time() + 1000}}
        with pytest.raises(HTTPException) as exc_info:
            check_challenge_rate_limit(req_client)
        assert exc_info.value.status_code == 429

        # Test expiry cleanup
        app.reg_rate_db = {"reg_limit:old": {"count": 10, "expiry": time.time() - 1000}}
        app.chal_rate_db = {"chal_limit:old": {"count": 10, "expiry": time.time() - 1000}}
        check_register_rate_limit(req_client)
        check_challenge_rate_limit(req_client)


def test_register_doc_versions_and_errors(client):
    # Version 2.0 doc
    doc_v2 = {
        "version": "2.0",
        "identity": {
            "agent_id": "agent://v2/agent",
            "keys": [{"id": "k1", "type": "ed25519", "public_key": "ed25519:abc", "status": "active"}]
        }
    }
    with patch("registry.main.verify_agent_registration", return_value=(True, "", doc_v2)):
        res = client.post("/register", json={"agent_id": "agent://v2/agent", "domain": "v2.com", "agent_json_url": "https://v2.com/a.json"})
        assert res.status_code == 200
        assert res.json()["public_key"] == "ed25519:abc"

    # Doc without active public key
    doc_no_key = {"version": "1.0", "agent_id": "agent://nokey", "keys": [{"id": "1", "status": "inactive"}]}
    with patch("registry.main.verify_agent_registration", return_value=(True, "", doc_no_key)):
        res = client.post("/register", json={"agent_id": "agent://nokey", "domain": "nokey.com", "agent_json_url": "https://nokey.com/a.json"})
        assert res.status_code == 400
        assert "No active public_key" in res.text

    # Signing failure
    with patch("registry.main.verify_agent_registration", return_value=(True, "", doc_v2)), patch("registry.main.sign_attestation", side_effect=Exception("sign fail")):
        res = client.post("/register", json={"agent_id": "agent://v2/agent", "domain": "v2.com", "agent_json_url": "https://v2.com/a.json"})
        assert res.status_code == 500
        assert "Signing failed" in res.text

    # Database write failure
    with patch("registry.main.verify_agent_registration", return_value=(True, "", doc_v2)), patch("registry.main.save_attestation", side_effect=Exception("db fail")):
        res = client.post("/register", json={"agent_id": "agent://v2/agent", "domain": "v2.com", "agent_json_url": "https://v2.com/a.json"})
        assert res.status_code == 500
        assert "Database write failed" in res.text


def test_attest_get_and_revoke_edge_cases(client):
    # Register an agent first
    pk = ed25519.Ed25519PrivateKey.generate()
    pub_b64 = base64.b64encode(pk.public_key().public_bytes(
        encoding=signer_mod.serialization.Encoding.Raw, format=signer_mod.serialization.PublicFormat.Raw
    )).decode("utf-8")
    pub_str = f"ed25519:{pub_b64}"

    doc = {"version": "1.0", "agent_id": "agent://test/agent", "public_key": pub_str}
    with patch("registry.main.verify_agent_registration", return_value=(True, "", doc)):
        res = client.post("/register", json={"agent_id": "agent://test/agent", "domain": "test.com", "agent_json_url": "http://test.com/a.json"})
        assert res.status_code == 200

    # Get attest using agent:/ normalization
    res = client.get("/attest/agent:/test/agent")
    assert res.status_code == 200
    assert res.json()["status"] == "active"

    # Get attestation not found
    res = client.get("/attest/agent://nonexistent")
    assert res.status_code == 404

    # Expired attestation & invalid expires_at
    attest = store_mod.get_attestation("agent://test/agent")
    attest["expires_at"] = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(timespec="seconds").replace("+00:00", "Z")
    store_mod.save_attestation("agent://test/agent", attest)
    res = client.get("/attest/agent://test/agent")
    assert res.json()["status"] == "expired"

    attest["expires_at"] = "invalid-date"
    store_mod.save_attestation("agent://test/agent", attest)
    res = client.get("/attest/agent://test/agent")
    assert res.json()["status"] == "expired"  # safe fallback when date parse fails

    # Revoke edge cases
    # Missing env var
    with patch.dict(os.environ, {}, clear=True):
        res = client.delete("/revoke/agent:/test/agent", headers={"CREDUENT_ADMIN_KEY": "test-secret-key"})
        assert res.status_code == 500

    # Missing header
    res = client.delete("/revoke/agent:/test/agent")
    assert res.status_code == 403

    # Invalid header
    res = client.delete("/revoke/agent:/test/agent", headers={"CREDUENT_ADMIN_KEY": "wrong"})
    assert res.status_code == 403

    # Valid revoke with normalization
    res = client.delete("/revoke/agent:/test/agent", headers={"CREDUENT_ADMIN_KEY": "test-secret-key"})
    assert res.status_code == 200

    # Get attest on revoked agent
    res = client.get("/attest/agent://test/agent")
    assert res.json()["status"] == "revoked"


def test_renew_endpoint_variations(client):
    pk = ed25519.Ed25519PrivateKey.generate()
    pub_b64 = base64.b64encode(pk.public_key().public_bytes(
        encoding=signer_mod.serialization.Encoding.Raw, format=signer_mod.serialization.PublicFormat.Raw
    )).decode("utf-8")
    pub_str = f"ed25519:{pub_b64}"

    doc = {"version": "1.0", "agent_id": "agent://renew/test", "public_key": pub_str}
    with patch("registry.main.verify_agent_registration", return_value=(True, "", doc)):
        client.post("/register", json={"agent_id": "agent://renew/test", "domain": "renew.com", "agent_json_url": "http://renew.com/a.json"})

    new_expiry = (datetime.now(timezone.utc) + timedelta(days=90)).isoformat(timespec="seconds").replace("+00:00", "Z")

    # Non-existent agent
    res = client.post("/renew", json={"agent_id": "agent://nobody", "new_expires_at": new_expiry, "signature": "abc"})
    assert res.status_code == 404

    # Unsupported public key format
    att = store_mod.get_attestation("agent://renew/test")
    att["public_key"] = "rsa:something"
    store_mod.save_attestation("agent://renew/test", att)
    res = client.post("/renew", json={"agent_id": "agent:/renew/test", "new_expires_at": new_expiry, "signature": "abc"})
    assert res.status_code == 400
    assert "Unsupported public key" in res.text

    # Restore key
    att["public_key"] = pub_str
    store_mod.save_attestation("agent://renew/test", att)

    # Invalid signature
    res = client.post("/renew", json={"agent_id": "agent:/renew/test", "new_expires_at": new_expiry, "signature": base64.b64encode(b"bad_sig").decode("utf-8")})
    assert res.status_code == 400
    assert "Invalid client signature" in res.text

    # Invalid base64 signature
    res = client.post("/renew", json={"agent_id": "agent:/renew/test", "new_expires_at": new_expiry, "signature": "not!!base64"})
    assert res.status_code == 400

    # Valid JCS dictionary signature
    payload_dict = {"agent_id": "agent:/renew/test", "new_expires_at": new_expiry}
    sig = pk.sign(canonicalize(payload_dict).encode("utf-8"))
    res = client.post("/renew", json={"agent_id": "agent:/renew/test", "new_expires_at": new_expiry, "signature": base64.b64encode(sig).decode("utf-8")})
    assert res.status_code == 200
    assert res.json()["expires_at"] == new_expiry

    # Valid delimited string signature ("agent_id|new_expires_at")
    new_expiry_2 = (datetime.now(timezone.utc) + timedelta(days=120)).isoformat(timespec="seconds").replace("+00:00", "Z")
    delim_str = f"agent://renew/test|{new_expiry_2}".encode("utf-8")
    sig2 = pk.sign(delim_str)
    res = client.post("/renew", json={"agent_id": "agent://renew/test", "new_expires_at": new_expiry_2, "signature": base64.b64encode(sig2).decode("utf-8")})
    assert res.status_code == 200
    assert res.json()["expires_at"] == new_expiry_2

    # Registry private key missing
    with patch("registry.main.get_registry_private_key", return_value=None):
        res = client.post("/renew", json={"agent_id": "agent://renew/test", "new_expires_at": new_expiry_2, "signature": base64.b64encode(sig2).decode("utf-8")})
        assert res.status_code == 500
        assert "not configured" in res.text

    # Sign exception
    with patch("registry.main.canonicalize", side_effect=Exception("canon fail")):
        res = client.post("/renew", json={"agent_id": "agent://renew/test", "new_expires_at": new_expiry_2, "signature": base64.b64encode(sig2).decode("utf-8")})
        assert res.status_code == 500

    # Save attestation exception
    with patch("registry.main.save_attestation", side_effect=Exception("save fail")):
        res = client.post("/renew", json={"agent_id": "agent://renew/test", "new_expires_at": new_expiry_2, "signature": base64.b64encode(sig2).decode("utf-8")})
        assert res.status_code == 500


def test_webhook_endpoints(client):
    pk = ed25519.Ed25519PrivateKey.generate()
    pub_b64 = base64.b64encode(pk.public_key().public_bytes(
        encoding=signer_mod.serialization.Encoding.Raw, format=signer_mod.serialization.PublicFormat.Raw
    )).decode("utf-8")
    pub_str = f"ed25519:{pub_b64}"

    doc = {"version": "1.0", "agent_id": "agent://wh/test", "public_key": pub_str}
    with patch("registry.main.verify_agent_registration", return_value=(True, "", doc)):
        client.post("/register", json={"agent_id": "agent://wh/test", "domain": "wh.com", "agent_json_url": "http://wh.com/a.json"})

    wh_url = "https://wh.com/callback"

    # Non-existent agent
    res = client.post("/webhook/register", json={"agent_id": "agent:/no", "webhook_url": wh_url, "signature": "abc"})
    assert res.status_code == 404

    # Unsupported pubkey
    att = store_mod.get_attestation("agent://wh/test")
    att["public_key"] = "rsa:xyz"
    store_mod.save_attestation("agent://wh/test", att)
    res = client.post("/webhook/register", json={"agent_id": "agent:/wh/test", "webhook_url": wh_url, "signature": "abc"})
    assert res.status_code == 400

    att["public_key"] = pub_str
    store_mod.save_attestation("agent://wh/test", att)

    # Invalid signature
    res = client.post("/webhook/register", json={"agent_id": "agent:/wh/test", "webhook_url": wh_url, "signature": base64.b64encode(b"bad").decode("utf-8")})
    assert res.status_code == 403

    # Valid JCS dictionary signature
    payload = {"agent_id": "agent:/wh/test", "webhook_url": wh_url}
    sig = pk.sign(canonicalize(payload).encode("utf-8"))
    res = client.post("/webhook/register", json={"agent_id": "agent:/wh/test", "webhook_url": wh_url, "signature": base64.b64encode(sig).decode("utf-8")})
    assert res.status_code == 200
    assert "webhook_secret" in res.json()

    # Valid delimited string signature
    delim = f"agent://wh/test|{wh_url}".encode("utf-8")
    sig2 = pk.sign(delim)
    res = client.post("/webhook/register", json={"agent_id": "agent://wh/test", "webhook_url": wh_url, "signature": base64.b64encode(sig2).decode("utf-8")})
    assert res.status_code == 200

    # Save webhook exception
    with patch("registry.main.save_webhook", side_effect=Exception("wh fail")):
        res = client.post("/webhook/register", json={"agent_id": "agent://wh/test", "webhook_url": wh_url, "signature": base64.b64encode(sig2).decode("utf-8")})
        assert res.status_code == 500

    # GET /webhook/{agent_id}
    with patch.dict(os.environ, {}, clear=True):
        res = client.get("/webhook/agent:/wh/test", headers={"CREDUENT_ADMIN_KEY": "test-secret-key"})
        assert res.status_code == 500

    res = client.get("/webhook/agent:/wh/test")
    assert res.status_code == 403

    res = client.get("/webhook/agent:/wh/test", headers={"CREDUENT-ADMIN-KEY": "wrong"})
    assert res.status_code == 403

    res = client.get("/webhook/agent:/nobody", headers={"CREDUENT_ADMIN_KEY": "test-secret-key"})
    assert res.status_code == 404

    res = client.get("/webhook/agent:/wh/test", headers={"CREDUENT_ADMIN_KEY": "test-secret-key"})
    assert res.status_code == 200
    assert res.json()["webhook_url"] == wh_url


def test_admin_attest_and_direct_attest(client):
    # POST /admin/attest
    # Missing env
    with patch.dict(os.environ, {}, clear=True):
        res = client.post("/admin/attest", json={"agent_id": "agent://adm/1", "level": "verified"}, headers={"CREDUENT_ADMIN_KEY": "test-secret-key"})
        assert res.status_code == 500

    # Missing header
    res = client.post("/admin/attest", json={"agent_id": "agent://adm/1", "level": "verified"})
    assert res.status_code == 403

    # Invalid header
    res = client.post("/admin/attest", json={"agent_id": "agent://adm/1", "level": "verified"}, headers={"CREDUENT_ADMIN_KEY": "wrong"})
    assert res.status_code == 403

    # Invalid level
    res = client.post("/admin/attest", json={"agent_id": "agent://adm/1", "level": "supergod"}, headers={"CREDUENT_ADMIN_KEY": "test-secret-key"})
    assert res.status_code == 400
    assert "Invalid level" in res.text

    # Agent not found
    res = client.post("/admin/attest", json={"agent_id": "agent:/adm/1", "level": "verified"}, headers={"CREDUENT_ADMIN_KEY": "test-secret-key"})
    assert res.status_code == 404

    # Create agent first via direct /attest
    # Missing env for /attest
    with patch.dict(os.environ, {}, clear=True):
        res = client.post("/attest", json={"agent_id": "agent:/adm/1", "public_key": "ed25519:123", "domain": "adm.com"}, headers={"CREDUENT_ADMIN_KEY": "test-secret-key"})
        assert res.status_code == 500

    res = client.post("/attest", json={"agent_id": "agent:/adm/1", "public_key": "ed25519:123", "domain": "adm.com"})
    assert res.status_code == 403

    res = client.post("/attest", json={"agent_id": "agent:/adm/1", "public_key": "ed25519:123", "domain": "adm.com"}, headers={"CREDUENT_ADMIN_KEY": "wrong"})
    assert res.status_code == 403

    # Sign fail in /attest
    with patch("registry.main.sign_attestation", side_effect=Exception("sign fail")):
        res = client.post("/attest", json={"agent_id": "agent:/adm/1", "public_key": "ed25519:123", "domain": "adm.com"}, headers={"CREDUENT_ADMIN_KEY": "test-secret-key"})
        assert res.status_code == 500

    # DB fail in /attest
    with patch("registry.main.save_attestation", side_effect=Exception("db fail")):
        res = client.post("/attest", json={"agent_id": "agent:/adm/1", "public_key": "ed25519:123", "domain": "adm.com"}, headers={"CREDUENT_ADMIN_KEY": "test-secret-key"})
        assert res.status_code == 500

    # Valid direct /attest
    res = client.post("/attest", json={"agent_id": "agent:/adm/1", "public_key": "ed25519:123", "domain": "adm.com"}, headers={"CREDUENT_ADMIN_KEY": "test-secret-key"})
    assert res.status_code == 200
    assert res.json()["level"] == "unverified"

    # Now upgrade via /admin/attest
    # Sign fail
    with patch("registry.main.sign_attestation", side_effect=Exception("sign fail")):
        res = client.post("/admin/attest", json={"agent_id": "agent:/adm/1", "level": "verified"}, headers={"CREDUENT_ADMIN_KEY": "test-secret-key"})
        assert res.status_code == 500

    # DB fail
    with patch("registry.main.save_attestation", side_effect=Exception("db fail")):
        res = client.post("/admin/attest", json={"agent_id": "agent:/adm/1", "level": "verified"}, headers={"CREDUENT_ADMIN_KEY": "test-secret-key"})
        assert res.status_code == 500

    # Valid upgrade
    res = client.post("/admin/attest", json={"agent_id": "agent:/adm/1", "level": "trusted"}, headers={"CREDUENT_ADMIN_KEY": "test-secret-key"})
    assert res.status_code == 200
    assert res.json()["level"] == "trusted"
    assert res.json()["status"] == "upgraded"


def test_stats_endpoint(client):
    # Setup agents with various levels and expiry dates
    now_dt = datetime.now(timezone.utc)
    a1 = {"agent_id": "agent://s/1", "level": "verified", "expires_at": (now_dt + timedelta(days=15)).isoformat(timespec="seconds").replace("+00:00", "Z")}
    a2 = {"agent_id": "agent://s/2", "level": "unverified", "expires_at": (now_dt + timedelta(days=60)).isoformat(timespec="seconds").replace("+00:00", "Z")}
    a3 = {"agent_id": "agent://s/3", "level": "revoked"}
    a4 = {"agent_id": "agent://s/4", "level": "trusted", "expires_at": "bad-date"}
    for a in [a1, a2, a3, a4]:
        store_mod.save_attestation(a["agent_id"], a)

    res = client.get("/stats")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 4
    assert data["verified"] >= 2
    assert data["unverified"] >= 1
    assert data["revoked"] >= 1
    assert data["expiring_soon"] >= 1


def test_challenge_endpoints_complete(client):
    pk = ed25519.Ed25519PrivateKey.generate()
    pub_b64 = base64.b64encode(pk.public_key().public_bytes(
        encoding=signer_mod.serialization.Encoding.Raw, format=signer_mod.serialization.PublicFormat.Raw
    )).decode("utf-8")
    pub_str = f"ed25519:{pub_b64}"

    doc = {"version": "1.0", "agent_id": "agent://chal/agent", "public_key": pub_str}
    with patch("registry.main.verify_agent_registration", return_value=(True, "", doc)):
        client.post("/register", json={"agent_id": "agent://chal/agent", "domain": "chal.com", "agent_json_url": "http://chal.com/a.json"})

    # GET /challenge for non-registered
    res = client.get("/challenge/agent:/nobody")
    assert res.status_code == 404

    # GET /challenge save failure
    with patch("registry.main.save_challenge", side_effect=Exception("save fail")):
        res = client.get("/challenge/agent:/chal/agent")
        assert res.status_code == 500

    # Valid challenge request
    res = client.get("/challenge/agent:/chal/agent")
    assert res.status_code == 200
    chal_data = res.json()
    nonce = chal_data["nonce"]
    challenge = chal_data["challenge"]

    # Verify challenge - non existent challenge
    res = client.post("/verify-challenge", json={"agent_id": "agent:/chal/agent", "nonce": "bad_nonce", "signature": "abc"})
    assert res.status_code == 401

    # Verify challenge - expired challenge
    chal_data["expires_at"] = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(timespec="seconds").replace("+00:00", "Z")
    store_mod.save_challenge("agent://chal/agent", nonce, chal_data)
    res = client.post("/verify-challenge", json={"agent_id": "agent:/chal/agent", "nonce": nonce, "signature": "abc"})
    assert res.status_code == 401
    assert "expired" in res.text

    # Re-request challenge
    res = client.get("/challenge/agent://chal/agent")
    chal_data = res.json()
    nonce = chal_data["nonce"]
    challenge = chal_data["challenge"]

    # Unsupported public key format during verify
    att = store_mod.get_attestation("agent://chal/agent")
    att["public_key"] = "rsa:bad"
    store_mod.save_attestation("agent://chal/agent", att)
    res = client.post("/verify-challenge", json={"agent_id": "agent:/chal/agent", "nonce": nonce, "signature": "abc"})
    assert res.status_code == 400

    att["public_key"] = pub_str
    store_mod.save_attestation("agent://chal/agent", att)

    # Invalid signature during verify
    res = client.post("/verify-challenge", json={"agent_id": "agent:/chal/agent", "nonce": nonce, "signature": base64.b64encode(b"badsig").decode("utf-8")})
    assert res.status_code == 401

    # Valid signature
    msg = (challenge + nonce).encode("utf-8")
    import hashlib
    h_bytes = hashlib.sha256(msg).digest()
    sig = pk.sign(h_bytes)
    sig_b64 = base64.b64encode(sig).decode("utf-8")

    # Verify with missing registry private key
    with patch("registry.main.get_registry_private_key", return_value=None):
        res = client.post("/verify-challenge", json={"agent_id": "agent:/chal/agent", "nonce": nonce, "signature": sig_b64})
        assert res.status_code == 500

    # Re-request challenge since one-time challenges are deleted upon verification attempt
    res = client.get("/challenge/agent://chal/agent")
    chal_data = res.json()
    nonce = chal_data["nonce"]
    challenge = chal_data["challenge"]
    msg = (challenge + nonce).encode("utf-8")
    h_bytes = hashlib.sha256(msg).digest()
    sig_b64 = base64.b64encode(pk.sign(h_bytes)).decode("utf-8")

    # Verify with signing exception in proof generation
    with patch("registry.main.canonicalize", side_effect=Exception("canon error")):
        res = client.post("/verify-challenge", json={"agent_id": "agent:/chal/agent", "nonce": nonce, "signature": sig_b64})
        assert res.status_code == 500

    # Re-request challenge for valid verify challenge test
    res = client.get("/challenge/agent://chal/agent")
    chal_data = res.json()
    nonce = chal_data["nonce"]
    challenge = chal_data["challenge"]
    msg = (challenge + nonce).encode("utf-8")
    h_bytes = hashlib.sha256(msg).digest()
    sig_b64 = base64.b64encode(pk.sign(h_bytes)).decode("utf-8")

    # Finally valid verify challenge
    res = client.post("/verify-challenge", json={"agent_id": "agent:/chal/agent", "nonce": nonce, "signature": sig_b64})
    assert res.status_code == 200
    assert res.json()["verified"] is True
    assert "proof_token" in res.json()


def test_recovery_override_and_public_key(client):
    # Register an agent first with extra metadata
    doc = {"version": "1.0", "agent_id": "agent://rec/agent", "public_key": "ed25519:old_key", "capabilities": ["tool1"], "owner": "dev", "endpoint": "http://rec.com"}
    with patch("registry.main.verify_agent_registration", return_value=(True, "", doc)):
        client.post("/register", json={"agent_id": "agent://rec/agent", "domain": "rec.com", "agent_json_url": "http://rec.com/a.json"})
    # Save extra metadata directly into db to verify preservation
    att = store_mod.get_attestation("agent://rec/agent")
    att["capabilities"] = ["tool1"]
    att["owner"] = "dev"
    att["endpoint"] = "http://rec.com"
    store_mod.save_attestation("agent://rec/agent", att)

    # Recovery override - non existent agent
    res = client.post("/recovery/override", json={"agent_id": "agent:/nobody", "domain": "rec.com", "new_public_key": "ed25519:new_key"})
    assert res.status_code == 404

    # Domain mismatch
    res = client.post("/recovery/override", json={"agent_id": "agent:/rec/agent", "domain": "wrong.com", "new_public_key": "ed25519:new_key"})
    assert res.status_code == 400
    assert "Domain mismatch" in res.text

    # DNS lookup failure
    with patch("dns.resolver.resolve", side_effect=Exception("DNS failure")):
        res = client.post("/recovery/override", json={"agent_id": "agent:/rec/agent", "domain": "rec.com", "new_public_key": "ed25519:new_key"})
        assert res.status_code == 400
        assert "DNS TXT lookup failed" in res.text

    # DNS verification failure (TXT doesn't match new key)
    mock_answer = MagicMock()
    mock_answer.strings = [b"some_other_key"]
    with patch("dns.resolver.resolve", return_value=[mock_answer]):
        res = client.post("/recovery/override", json={"agent_id": "agent:/rec/agent", "domain": "rec.com", "new_public_key": "ed25519:new_key"})
        assert res.status_code == 400
        assert "recovery verification failed" in res.text

    # Missing registry private key
    mock_answer.strings = [b"ed25519:new_key"]
    with patch("dns.resolver.resolve", return_value=[mock_answer]), patch("registry.signer.get_registry_private_key", return_value=None):
        res = client.post("/recovery/override", json={"agent_id": "agent:/rec/agent", "domain": "rec.com", "new_public_key": "ed25519:new_key"})
        assert res.status_code == 500

    # Sign failure
    with patch("dns.resolver.resolve", return_value=[mock_answer]), patch("registry.main.sign_attestation", side_effect=Exception("sign err")):
        res = client.post("/recovery/override", json={"agent_id": "agent:/rec/agent", "domain": "rec.com", "new_public_key": "ed25519:new_key"})
        assert res.status_code == 500

    # DB write failure
    with patch("dns.resolver.resolve", return_value=[mock_answer]), patch("registry.main.save_attestation", side_effect=Exception("db err")):
        res = client.post("/recovery/override", json={"agent_id": "agent:/rec/agent", "domain": "rec.com", "new_public_key": "ed25519:new_key"})
        assert res.status_code == 500

    # Valid recovery override
    with patch("dns.resolver.resolve", return_value=[mock_answer]):
        res = client.post("/recovery/override", json={"agent_id": "agent:/rec/agent", "domain": "rec.com", "new_public_key": "ed25519:new_key"})
        assert res.status_code == 200
        assert res.json()["status"] == "recovered"
        assert res.json()["public_key"] == "ed25519:new_key"
        # Check preserved metadata
        assert res.json()["owner"] == "dev"
        assert res.json()["capabilities"] == ["tool1"]

    # Test /public-key endpoint
    res = client.get("/public-key")
    assert res.status_code == 200
    assert res.json()["public_key"].startswith("ed25519:")

    with patch("registry.main.get_registry_public_key", return_value=None):
        res = client.get("/public-key")
        assert res.status_code == 500


def test_ui_endpoints_and_catch_all(client):
    # Create test agent for direct resolving
    doc = {"version": "1.0", "agent_id": "agent://ui/test", "public_key": "ed25519:123"}
    with patch("registry.main.verify_agent_registration", return_value=(True, "", doc)):
        client.post("/register", json={"agent_id": "agent://ui/test", "domain": "ui.com", "agent_json_url": "http://ui.com/a.json"})

    # Test direct resolve endpoints
    res = client.get("/agent:/ui/test")
    assert res.status_code == 200
    assert res.json()["agent_id"] == "agent://ui/test"

    res = client.get("/agent://ui/test")
    assert res.status_code == 200

    # Test catch-all resolver with various prefix formats
    res = client.get("/agent:/ui/test")
    assert res.status_code == 200

    res = client.get("/agent://ui/test")
    assert res.status_code == 200

    res = client.get("/agent:ui/test")
    assert res.status_code == 200

    res = client.get("/something/else")
    assert res.status_code == 404

    # Test GUI / HTML endpoints
    assert client.get("/resolver").status_code == 200
    assert client.get("/resolver/").status_code == 200
    assert client.get("/dashboard").status_code == 200
    assert client.get("/registry/dashboard").status_code == 200
    assert client.get("/playground").status_code == 200
    assert client.get("/registry/playground").status_code == 200

    # Test landing endpoint
    res = client.get("/registry")
    assert res.status_code == 200
    assert res.json()["protocol"] == "Creduent"
    res = client.get("/registry/")
    assert res.status_code == 200
