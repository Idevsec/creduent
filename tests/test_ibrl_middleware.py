import time
import pytest
from starlette.testclient import TestClient
from fastapi import FastAPI
from registry.middleware.ibrl import IBRLMiddleware
from registry import store


@pytest.fixture
def dummy_app():
    app = FastAPI()
    app.add_middleware(IBRLMiddleware, limit_per_min=2, window_sec=300)

    @app.get("/test")
    async def get_test():
        return {"status": "ok"}

    return app


@pytest.fixture
def client(dummy_app):
    return TestClient(dummy_app)


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch, tmp_path):
    monkeypatch.delenv("UPSTASH_REDIS_REST_URL", raising=False)
    monkeypatch.delenv("UPSTASH_REDIS_REST_TOKEN", raising=False)
    db_file = str(tmp_path / "ibrl_test_db.json")
    monkeypatch.setattr("registry.store.DB_PATH", db_file)
    yield


def test_ibrl_passthrough_no_agent_id(client):
    res = client.get("/test")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
    assert "X-RateLimit-Limit" not in res.headers


def test_ibrl_missing_cryptographic_headers(client):
    res = client.get("/test", headers={"X-Creduent-Agent-ID": "agent://test"})
    assert res.status_code == 401
    assert res.json()["detail"] == "Missing cryptographic headers for IBRL"

    res = client.get("/test", headers={
        "X-Creduent-Agent-ID": "agent://test",
        "X-Creduent-Signature": "sig123"
    })
    assert res.status_code == 401


def test_ibrl_invalid_timestamp_format(client):
    res = client.get("/test", headers={
        "X-Creduent-Agent-ID": "agent://test",
        "X-Creduent-Signature": "sig123",
        "X-Creduent-Timestamp": "invalid-timestamp"
    })
    assert res.status_code == 400
    assert res.json()["detail"] == "Invalid timestamp format"


def test_ibrl_timestamp_outside_window(client):
    now = time.time()
    res = client.get("/test", headers={
        "X-Creduent-Agent-ID": "agent://test",
        "X-Creduent-Signature": "sig123",
        "X-Creduent-Timestamp": str(now - 400)
    })
    assert res.status_code == 403
    assert res.json()["detail"] == "Timestamp outside valid window"


def test_ibrl_unattested_or_revoked_agent(client, dummy_app):
    now = time.time()
    agent_id = "agent://unknown"
    res = client.get("/test", headers={
        "X-Creduent-Agent-ID": agent_id,
        "X-Creduent-Signature": "sig-unknown",
        "X-Creduent-Timestamp": str(now)
    })
    assert res.status_code == 403
    assert res.json()["detail"] == "Agent identity invalid or revoked"

    # Save attestation as status revoked
    revoked_id = "agent://revoked"
    store.save_attestation(revoked_id, {"status": "revoked", "agent_id": revoked_id})
    res = client.get("/test", headers={
        "X-Creduent-Agent-ID": revoked_id,
        "X-Creduent-Signature": "sig-revoked",
        "X-Creduent-Timestamp": str(now)
    })
    assert res.status_code == 403
    assert res.json()["detail"] == "Agent identity invalid or revoked"

    # Save attestation with level revoked
    level_revoked_id = "agent://level-revoked"
    store.save_attestation(level_revoked_id, {"level": "revoked", "agent_id": level_revoked_id})
    res2 = client.get("/test", headers={
        "X-Creduent-Agent-ID": level_revoked_id,
        "X-Creduent-Signature": "sig-level-revoked",
        "X-Creduent-Timestamp": str(now)
    })
    assert res2.status_code == 403
    assert res2.json()["detail"] == "Agent identity invalid or revoked"


def test_ibrl_replay_detection(client, dummy_app):
    now = time.time()
    agent_id = "agent://valid"
    store.save_attestation(agent_id, {"status": "active", "agent_id": agent_id})

    res = client.get("/test", headers={
        "X-Creduent-Agent-ID": agent_id,
        "X-Creduent-Signature": "sig-replay-test",
        "X-Creduent-Timestamp": str(now)
    })
    assert res.status_code == 200

    # Second request with identical signature should be blocked as replay
    res2 = client.get("/test", headers={
        "X-Creduent-Agent-ID": agent_id,
        "X-Creduent-Signature": "sig-replay-test",
        "X-Creduent-Timestamp": str(now)
    })
    assert res2.status_code == 403
    assert res2.json()["detail"] == "Replay Detected"


def test_ibrl_token_bucket_rate_limiting(client):
    agent_id = "agent://rate-limited"
    store.save_attestation(agent_id, {"status": "active", "agent_id": agent_id})

    now = time.time()
    # Req 1 (tokens: 2 -> 1)
    res1 = client.get("/test", headers={
        "X-Creduent-Agent-ID": agent_id,
        "X-Creduent-Signature": "sig-rl-1",
        "X-Creduent-Timestamp": str(now)
    })
    assert res1.status_code == 200
    assert res1.headers["X-RateLimit-Limit"] == "2"
    assert res1.headers["X-RateLimit-Remaining"] == "1"

    # Req 2 (tokens: 1 -> 0)
    res2 = client.get("/test", headers={
        "X-Creduent-Agent-ID": agent_id,
        "X-Creduent-Signature": "sig-rl-2",
        "X-Creduent-Timestamp": str(now)
    })
    assert res2.status_code == 200
    assert res2.headers["X-RateLimit-Remaining"] == "0"

    # Req 3 (tokens: 0 < 1.0 -> 429 Too Many Requests)
    res3 = client.get("/test", headers={
        "X-Creduent-Agent-ID": agent_id,
        "X-Creduent-Signature": "sig-rl-3",
        "X-Creduent-Timestamp": str(now)
    })
    assert res3.status_code == 429
    assert res3.json()["detail"] == "Too Many Requests"
    assert res3.headers["X-RateLimit-Limit"] == "2"
    assert res3.headers["X-RateLimit-Remaining"] == "0"


def test_ibrl_pruning_and_clear_state():
    app = FastAPI()
    @app.get("/test")
    def get_test():
        return {"status": "ok"}
    
    app.add_middleware(IBRLMiddleware, limit_per_min=10, window_sec=1)
    client = TestClient(app)
    agent_id = "agent://valid-pruning"
    store.save_attestation(agent_id, {"status": "active", "agent_id": agent_id})

    res1 = client.get("/test", headers={
        "X-Creduent-Agent-ID": agent_id,
        "X-Creduent-Signature": "sig-prune-1",
        "X-Creduent-Timestamp": str(time.time())
    })
    assert res1.status_code == 200

    time.sleep(1.1)
    res2 = client.get("/test", headers={
        "X-Creduent-Agent-ID": agent_id,
        "X-Creduent-Signature": "sig-prune-2",
        "X-Creduent-Timestamp": str(time.time())
    })
    assert res2.status_code == 200

    # Test clear_state on instance directly
    middleware = IBRLMiddleware(app, limit_per_min=10, window_sec=300)
    middleware._seen_signatures["test_sig"] = time.time()
    middleware._buckets["test_agent"] = {"tokens": 1.0, "last_updated": time.time()}
    middleware.clear_state()
    assert len(middleware._seen_signatures) == 0
    assert len(middleware._buckets) == 0
