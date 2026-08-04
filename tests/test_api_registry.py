import os
import json
import base64
import hashlib
import pytest
from fastapi.testclient import TestClient
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

from registry.main import app


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch, tmp_path):
    # Generate an Ed25519 key for registry signing during tests
    registry_key = ed25519.Ed25519PrivateKey.generate()
    raw_key = registry_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    monkeypatch.setenv("CREDUENT_REGISTRY_KEY", base64.b64encode(raw_key).decode("utf-8"))
    monkeypatch.setenv("CREDUENT_ADMIN_KEY", "test-admin-secret")
    monkeypatch.delenv("UPSTASH_REDIS_REST_URL", raising=False)
    monkeypatch.delenv("UPSTASH_REDIS_REST_TOKEN", raising=False)

    # Use temporary JSON storage
    db_file = str(tmp_path / "registry_test_db.json")
    wh_file = str(tmp_path / "webhooks_test_db.json")
    monkeypatch.setattr("registry.store.DB_PATH", db_file)
    monkeypatch.setattr("registry.store.WEBHOOKS_DB_PATH", wh_file)

    import registry.store

    registry.store.CHALLENGE_DB.clear()

    # Reset rate limit in-memory caches on app if present
    for db_name in ("reg_rate_db", "chal_rate_db", "rate_db"):
        if hasattr(app, db_name):
            setattr(app, db_name, {})

    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def agent_keypair():
    priv_key = ed25519.Ed25519PrivateKey.generate()
    pub_key = priv_key.public_key()
    pub_bytes = pub_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    pub_b64 = base64.b64encode(pub_bytes).decode("utf-8")
    pub_str = f"ed25519:{pub_b64}"
    return priv_key, pub_str


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "redis_configured" in data


def test_admin_attest_and_get_attestation(client, agent_keypair):
    _, pub_str = agent_keypair
    agent_id = "agent://test.agent/alpha"
    payload = {
        "agent_id": agent_id,
        "public_key": pub_str,
        "domain": "test.agent",
    }

    # Should fail without admin header
    response = client.post("/attest", json=payload)
    assert response.status_code == 403

    # Should fail with invalid admin header
    response = client.post(
        "/attest", json=payload, headers={"CREDUENT_ADMIN_KEY": "wrong-secret"}
    )
    assert response.status_code == 403

    # Should succeed with valid admin key
    response = client.post(
        "/attest", json=payload, headers={"CREDUENT_ADMIN_KEY": "test-admin-secret"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["agent_id"] == agent_id
    assert data["public_key"] == pub_str
    assert "signature" in data

    # Retrieve attestation via GET /attest/{agent_id}
    response = client.get(f"/attest/{agent_id}")
    assert response.status_code == 200
    att = response.json()
    assert att["agent_id"] == agent_id
    assert att["status"] == "active"


def test_open_registration(client, agent_keypair, monkeypatch):
    _, pub_str = agent_keypair
    agent_id = "agent://open.test/agent1"

    # Mock verify_agent_registration to succeed with v1.0 doc
    def mock_verify(agent_id, domain, agent_json_url=None):
        doc = {
            "version": "1.0",
            "agent_id": agent_id,
            "public_key": pub_str,
        }
        return True, "Valid", doc

    monkeypatch.setattr("registry.main.verify_agent_registration", mock_verify)

    req_data = {
        "agent_id": agent_id,
        "domain": "open.test",
        "agent_json_url": "https://open.test/agent.json",
    }
    response = client.post("/register", json=req_data)
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["agent_id"] == agent_id
    assert res_json["level"] == "unverified"
    assert res_json["status"] == "registered"

    # Verify registration failure when verify_agent_registration fails
    def mock_verify_fail(*args, **kwargs):
        return False, "DNS resolution failed", None

    monkeypatch.setattr("registry.main.verify_agent_registration", mock_verify_fail)
    response = client.post("/register", json={**req_data, "agent_id": "agent://open.test/fail"})
    assert response.status_code == 400
    assert "Verification failed: DNS resolution failed" in response.json()["detail"]


def test_challenge_and_verify_challenge(client, agent_keypair):
    priv_key, pub_str = agent_keypair
    agent_id = "agent://secure.agent/bot"

    # Register via admin attest first
    client.post(
        "/attest",
        json={"agent_id": agent_id, "public_key": pub_str, "domain": "secure.agent"},
        headers={"CREDUENT_ADMIN_KEY": "test-admin-secret"},
    )

    # 1. Request challenge
    response = client.get(f"/challenge/{agent_id}")
    assert response.status_code == 200
    ch_data = response.json()
    assert ch_data["agent_id"] == agent_id
    challenge_hex = ch_data["challenge"]
    nonce_hex = ch_data["nonce"]

    # 2. Sign challenge + nonce
    message = (challenge_hex + nonce_hex).encode("utf-8")
    hashed_bytes = hashlib.sha256(message).digest()
    sig_bytes = priv_key.sign(hashed_bytes)
    sig_b64 = base64.b64encode(sig_bytes).decode("utf-8")

    # 3. Verify challenge with valid signature
    resp_verify = client.post(
        "/verify-challenge",
        json={"agent_id": agent_id, "nonce": nonce_hex, "signature": sig_b64},
    )
    assert resp_verify.status_code == 200
    ver_data = resp_verify.json()
    assert ver_data["verified"] is True
    assert "proof_token" in ver_data

    # 4. Verify that nonce cannot be reused (one-time use)
    resp_reuse = client.post(
        "/verify-challenge",
        json={"agent_id": agent_id, "nonce": nonce_hex, "signature": sig_b64},
    )
    assert resp_reuse.status_code == 401

    # 5. Test invalid signature on a new challenge
    res_ch2 = client.get(f"/challenge/{agent_id}")
    ch2_nonce = res_ch2.json()["nonce"]
    resp_bad_sig = client.post(
        "/verify-challenge",
        json={"agent_id": agent_id, "nonce": ch2_nonce, "signature": "aW52YWxpZHNpZ25hdHVyZQ=="},
    )
    assert resp_bad_sig.status_code == 401


def test_revoke_agent(client, agent_keypair):
    _, pub_str = agent_keypair
    agent_id = "agent://revoke.me/now"

    # Create agent
    client.post(
        "/attest",
        json={"agent_id": agent_id, "public_key": pub_str, "domain": "revoke.me"},
        headers={"CREDUENT_ADMIN_KEY": "test-admin-secret"},
    )

    # Revoke without key should fail
    response = client.delete(f"/revoke/{agent_id}")
    assert response.status_code == 403

    # Revoke with valid admin key should succeed
    response = client.delete(
        f"/revoke/{agent_id}", headers={"CREDUENT_ADMIN_KEY": "test-admin-secret"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "revoked"

    # Get attestation should show revoked status
    get_res = client.get(f"/attest/{agent_id}")
    assert get_res.status_code == 200
    assert get_res.json()["status"] == "revoked"


def test_stats_and_list_agents(client, agent_keypair):
    _, pub_str = agent_keypair
    # Add two agents
    client.post(
        "/attest",
        json={"agent_id": "agent://stats/1", "public_key": pub_str, "domain": "stats"},
        headers={"CREDUENT_ADMIN_KEY": "test-admin-secret"},
    )
    client.post(
        "/attest",
        json={"agent_id": "agent://stats/2", "public_key": pub_str, "domain": "stats"},
        headers={"CREDUENT_ADMIN_KEY": "test-admin-secret"},
    )
    client.delete(
        "/revoke/agent://stats/2", headers={"CREDUENT_ADMIN_KEY": "test-admin-secret"}
    )

    res_list = client.get("/agents")
    assert res_list.status_code == 200
    agents = res_list.json()
    assert len(agents) == 2

    res_stats = client.get("/stats")
    assert res_stats.status_code == 200
    stats = res_stats.json()
    assert stats["total"] == 2
    assert stats["revoked"] == 1
    assert stats["unverified"] == 1


def test_gui_and_resolver_routes(client, agent_keypair):
    _, pub_str = agent_keypair
    agent_id = "agent://ui.test/bot"
    client.post(
        "/attest",
        json={"agent_id": agent_id, "public_key": pub_str, "domain": "ui.test"},
        headers={"CREDUENT_ADMIN_KEY": "test-admin-secret"},
    )

    # HTML pages
    for path in ["/resolver", "/dashboard", "/playground"]:
        res = client.get(path)
        assert res.status_code == 200
        assert "text/html" in res.headers["content-type"]

    # Landing page JSON
    res_landing = client.get("/registry")
    assert res_landing.status_code == 200
    assert res_landing.json()["protocol"] == "Creduent"

    # Direct agent URI resolution
    res_direct = client.get(f"/{agent_id}")
    assert res_direct.status_code == 200
    assert res_direct.json()["agent_id"] == agent_id
