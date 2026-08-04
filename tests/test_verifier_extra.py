import pytest
import base64
import jsonschema
from unittest.mock import patch, MagicMock
from registry.verifier import (
    verify_endpoint_health,
    verify_agent_registration,
)


class CustomException(Exception):
    def __init__(self, msg, detail):
        super().__init__(msg)
        self.detail = detail


def test_endpoint_health_with_detail_exception():
    with patch("registry.verifier.safe_requests_get", side_effect=CustomException("err", "Detailed error message")):
        ok, err = verify_endpoint_health("https://example.com")
        assert not ok
        assert "Detailed error message" in err


def test_registration_fetch_with_detail_exception():
    with patch("registry.verifier.safe_requests_get", side_effect=CustomException("err", "Fetch failed detail")):
        ok, reason, doc = verify_agent_registration("agent://test", "example.com", "https://example.com/agent.json")
        assert not ok
        assert "Fetch failed detail" in reason
        assert doc == {}


def test_registration_schema_validation_error():
    mock_res = MagicMock()
    mock_res.status_code = 200
    mock_res.json.return_value = {"version": "1.0", "agent_id": 12345}  # invalid type
    with patch("registry.verifier.safe_requests_get", return_value=mock_res), \
         patch("jsonschema.validate", side_effect=jsonschema.exceptions.ValidationError("Invalid agent_id")):
        ok, reason, _ = verify_agent_registration("agent://test", "example.com", "https://example.com/agent.json")
        assert not ok
        assert "Schema validation failed: Invalid agent_id" in reason


def test_registration_schema_general_error():
    mock_res = MagicMock()
    mock_res.status_code = 200
    mock_res.json.return_value = {"version": "1.0", "agent_id": "agent://test"}
    with patch("registry.verifier.safe_requests_get", return_value=mock_res), \
         patch("jsonschema.validate", side_effect=Exception("Unknown schema error")):
        ok, reason, _ = verify_agent_registration("agent://test", "example.com", "https://example.com/agent.json")
        assert not ok
        assert "Failed to run schema validation: Unknown schema error" in reason


def test_registration_manual_fallback_v1_missing():
    mock_res = MagicMock()
    mock_res.status_code = 200
    mock_res.json.return_value = {"version": "1.0", "agent_id": "agent://test"}
    with patch("registry.verifier.safe_requests_get", return_value=mock_res), \
         patch("os.path.exists", return_value=False):
        ok, reason, _ = verify_agent_registration("agent://test", "example.com", "https://example.com/agent.json")
        assert not ok
        assert "Manual schema validation failed: missing field" in reason


def test_registration_manual_fallback_v2_missing_main():
    mock_res = MagicMock()
    mock_res.status_code = 200
    mock_res.json.return_value = {"version": "2.0", "identity": {}}
    with patch("registry.verifier.safe_requests_get", return_value=mock_res), \
         patch("os.path.exists", return_value=False):
        ok, reason, _ = verify_agent_registration("agent://test", "example.com", "https://example.com/agent.json")
        assert not ok
        assert "Manual schema validation failed" in reason


def test_registration_manual_fallback_v2_missing_identity():
    mock_res = MagicMock()
    mock_res.status_code = 200
    mock_res.json.return_value = {
        "version": "2.0",
        "identity": {"agent_id": "agent://test"},
        "policy": {},
        "signature": "xxx"
    }
    with patch("registry.verifier.safe_requests_get", return_value=mock_res), \
         patch("os.path.exists", return_value=False):
        ok, reason, _ = verify_agent_registration("agent://test", "example.com", "https://example.com/agent.json")
        assert not ok
        assert "Manual schema validation failed: missing field 'identity." in reason


def test_registration_manual_fallback_v2_missing_policy():
    mock_res = MagicMock()
    mock_res.status_code = 200
    mock_res.json.return_value = {
        "version": "2.0",
        "identity": {"agent_id": "agent://test", "owner": "a", "keys": [], "endpoint": "url"},
        "policy": {},
        "signature": "xxx"
    }
    with patch("registry.verifier.safe_requests_get", return_value=mock_res), \
         patch("os.path.exists", return_value=False):
        ok, reason, _ = verify_agent_registration("agent://test", "example.com", "https://example.com/agent.json")
        assert not ok
        assert "Manual schema validation failed: missing field 'policy.capabilities'" in reason


def test_registration_no_signature():
    mock_res = MagicMock()
    mock_res.status_code = 200
    mock_res.json.return_value = {
        "version": "1.0",
        "agent_id": "agent://test",
        "owner": "o", "public_key": "k", "endpoint": "e", "capabilities": [],
        "signature": ""
    }
    with patch("registry.verifier.safe_requests_get", return_value=mock_res), \
         patch("os.path.exists", return_value=False):
        ok, reason, _ = verify_agent_registration("agent://test", "example.com", "https://example.com/agent.json")
        assert not ok
        assert "agent.json has no signature." in reason


def test_registration_invalid_base64_signature():
    mock_res = MagicMock()
    mock_res.status_code = 200
    mock_res.json.return_value = {
        "version": "1.0",
        "agent_id": "agent://test",
        "owner": "o", "public_key": "k", "endpoint": "e", "capabilities": [],
        "signature": "bad!!base64"
    }
    with patch("registry.verifier.safe_requests_get", return_value=mock_res), \
         patch("os.path.exists", return_value=False):
        ok, reason, _ = verify_agent_registration("agent://test", "example.com", "https://example.com/agent.json")
        assert not ok
        assert "Signature is not valid base64." in reason


def test_registration_canonicalize_error():
    mock_res = MagicMock()
    mock_res.status_code = 200
    mock_res.json.return_value = {
        "version": "1.0",
        "agent_id": "agent://test",
        "owner": "o", "public_key": "k", "endpoint": "e", "capabilities": [],
        "signature": base64.b64encode(b"dummy").decode("utf-8")
    }
    with patch("registry.verifier.safe_requests_get", return_value=mock_res), \
         patch("os.path.exists", return_value=False), \
         patch("registry.verifier.canonicalize", side_effect=Exception("Canon error")):
        ok, reason, _ = verify_agent_registration("agent://test", "example.com", "https://example.com/agent.json")
        assert not ok
        assert "Failed during canonicalization: Canon error" in reason


def test_registration_v2_keys_filtering():
    mock_res = MagicMock()
    mock_res.status_code = 200
    mock_res.json.return_value = {
        "version": "2.0",
        "identity": {
            "agent_id": "agent://test",
            "owner": "o",
            "keys": [
                "not_a_dict",
                {"status": "revoked", "public_key": "ed25519:xxx"},
                {"status": "active", "public_key": "rsa:invalid_prefix"},
                {"status": "active", "public_key": "ed25519:bad_bytes!@#$"}
            ],
            "endpoint": "http://e"
        },
        "policy": {"capabilities": []},
        "signature": base64.b64encode(b"dummy").decode("utf-8")
    }
    with patch("registry.verifier.safe_requests_get", return_value=mock_res), \
         patch("os.path.exists", return_value=False):
        ok, reason, _ = verify_agent_registration("agent://test", "example.com", "https://example.com/agent.json")
        assert not ok
        assert "Signature verification failed:" in reason or "No active valid keys found." in reason or "Unsupported public key" in reason
