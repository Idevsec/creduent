import pytest
import base64
import json
from unittest.mock import patch, MagicMock
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import dns.resolver

from registry.verifier import (
    verify_dns_txt,
    verify_endpoint_health,
    verify_agent_registration,
)
from creduent.crypto import canonicalize


@pytest.fixture
def ed25519_keypair():
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    pub_b64 = base64.b64encode(pub_bytes).decode("ascii")
    return private_key, f"ed25519:{pub_b64}"


class TestVerifyDnsTxt:
    @patch("dns.resolver.resolve")
    def test_verify_dns_txt_success(self, mock_resolve):
        mock_answer = MagicMock()
        mock_answer.strings = [b"agent_id=agent://default/test_agent_123"]
        mock_resolve.return_value = [mock_answer]

        success, err = verify_dns_txt("example.com", "agent://default/test_agent_123")
        assert success is True
        assert err == ""
        mock_resolve.assert_called_once_with("_creduent.example.com", "TXT")

    @patch("dns.resolver.resolve")
    def test_verify_dns_txt_not_matching(self, mock_resolve):
        mock_answer = MagicMock()
        mock_answer.strings = [b"agent_id=agent://default/other_agent"]
        mock_resolve.return_value = [mock_answer]

        success, err = verify_dns_txt("example.com", "agent://default/test_agent_123")
        assert success is False
        assert "does not contain agent_id" in err

    @patch("dns.resolver.resolve")
    def test_verify_dns_txt_nxdomain(self, mock_resolve):
        mock_resolve.side_effect = dns.resolver.NXDOMAIN()
        success, err = verify_dns_txt("example.com", "agent://default/test_agent_123")
        assert success is False
        assert "not found at" in err or "NXDOMAIN" in err

    @patch("dns.resolver.resolve")
    def test_verify_dns_txt_no_answer(self, mock_resolve):
        mock_resolve.side_effect = dns.resolver.NoAnswer()
        success, err = verify_dns_txt("example.com", "agent://default/test_agent_123")
        assert success is False
        assert "No TXT records found" in err

    @patch("dns.resolver.resolve")
    def test_verify_dns_txt_exception(self, mock_resolve):
        mock_resolve.side_effect = Exception("Network timeout")
        success, err = verify_dns_txt("example.com", "agent://default/test_agent_123")
        assert success is False
        assert "DNS TXT resolution failed" in err


class TestVerifyEndpointHealth:
    @patch("registry.verifier.safe_requests_get")
    def test_verify_endpoint_health_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        success, err = verify_endpoint_health("https://example.com/health")
        assert success is True
        assert err == ""
        mock_get.assert_called_once_with("https://example.com/health", timeout=5)

    @patch("registry.verifier.safe_requests_get")
    def test_verify_endpoint_health_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection timed out")

        success, err = verify_endpoint_health("https://example.com/health")
        assert success is False
        assert "Endpoint healthcheck failed: Connection timed out" in err


class TestVerifyAgentRegistration:
    def _create_v1_doc(self, private_key, pub_key_str, agent_id="agent://default/agent123", endpoint="https://agent.example.com"):
        doc = {
            "version": "1.0",
            "agent_id": agent_id,
            "owner": "owner@example.com",
            "public_key": pub_key_str,
            "endpoint": endpoint,
            "capabilities": ["search", "chat"]
        }
        can_str = canonicalize(doc)
        sig_bytes = private_key.sign(can_str.encode("utf-8"))
        doc["signature"] = base64.b64encode(sig_bytes).decode("ascii")
        return doc

    def _create_v2_doc(self, private_key, pub_key_str, agent_id="agent://default/agent123", endpoint="https://agent.example.com"):
        doc = {
            "version": "2.0",
            "identity": {
                "agent_id": agent_id,
                "owner": "owner@example.com",
                "keys": [{"id": "key-1", "type": "ed25519", "public_key": pub_key_str, "status": "active"}],
                "endpoint": endpoint
            },
            "policy": {
                "capabilities": ["search", "chat"]
            }
        }
        can_str = canonicalize(doc)
        sig_bytes = private_key.sign(can_str.encode("utf-8"))
        doc["signature"] = base64.b64encode(sig_bytes).decode("ascii")
        return doc

    @patch("registry.verifier.verify_endpoint_health", return_value=(True, ""))
    @patch("registry.verifier.verify_dns_txt", return_value=(True, ""))
    @patch("registry.verifier.safe_requests_get")
    def test_registration_v1_success(self, mock_get, mock_dns, mock_health, ed25519_keypair):
        private_key, pub_str = ed25519_keypair
        doc = self._create_v1_doc(private_key, pub_str, agent_id="agent://default/my-agent")
        
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_res.json.return_value = doc
        mock_get.return_value = mock_res

        success, reason, ret_doc = verify_agent_registration("agent://default/my-agent", "example.com", "https://example.com/agent.json")
        assert success is True, f"Expected success but got error: {reason}"
        assert reason == "Verification successful"
        assert ret_doc == doc

    @patch("registry.verifier.verify_endpoint_health", return_value=(True, ""))
    @patch("registry.verifier.verify_dns_txt", return_value=(True, ""))
    @patch("registry.verifier.safe_requests_get")
    def test_registration_v2_success(self, mock_get, mock_dns, mock_health, ed25519_keypair):
        private_key, pub_str = ed25519_keypair
        doc = self._create_v2_doc(private_key, pub_str, agent_id="agent://default/my-agent")
        
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_res.json.return_value = doc
        mock_get.return_value = mock_res

        success, reason, ret_doc = verify_agent_registration("agent://default/my-agent", "example.com", "https://example.com/agent.json")
        assert success is True, f"Expected success but got error: {reason}"
        assert reason == "Verification successful"
        assert ret_doc == doc

    @patch("registry.verifier.safe_requests_get")
    def test_registration_fetch_error(self, mock_get):
        mock_res = MagicMock()
        mock_res.status_code = 404
        mock_get.return_value = mock_res

        success, reason, ret_doc = verify_agent_registration("agent://default/my-agent", "example.com", "https://example.com/agent.json")
        assert success is False
        assert "HTTP 404" in reason

    @patch("registry.verifier.safe_requests_get")
    def test_registration_unsupported_version(self, mock_get):
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_res.json.return_value = {"version": "9.9"}
        mock_get.return_value = mock_res

        success, reason, _ = verify_agent_registration("agent://default/my-agent", "example.com", "https://example.com/agent.json")
        assert success is False
        assert "Unsupported protocol version" in reason

    @patch("registry.verifier.safe_requests_get")
    def test_registration_agent_id_mismatch(self, mock_get, ed25519_keypair):
        private_key, pub_str = ed25519_keypair
        doc = self._create_v1_doc(private_key, pub_str, agent_id="agent://default/doc-agent")

        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_res.json.return_value = doc
        mock_get.return_value = mock_res

        success, reason, _ = verify_agent_registration("agent://default/reg-agent", "example.com", "https://example.com/agent.json")
        assert success is False
        assert "does not match registration agent_id" in reason

    @patch("registry.verifier.safe_requests_get")
    def test_registration_invalid_signature(self, mock_get, ed25519_keypair):
        private_key, pub_str = ed25519_keypair
        doc = self._create_v1_doc(private_key, pub_str, agent_id="agent://default/my-agent")
        doc["signature"] = base64.b64encode(b"invalid-signature-bytes" * 4).decode("ascii")

        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_res.json.return_value = doc
        mock_get.return_value = mock_res

        success, reason, _ = verify_agent_registration("agent://default/my-agent", "example.com", "https://example.com/agent.json")
        assert success is False
        assert "Cryptographic signature in agent.json is INVALID" in reason

    @patch("registry.verifier.verify_dns_txt", return_value=(False, "DNS failed"))
    @patch("registry.verifier.safe_requests_get")
    def test_registration_dns_failure(self, mock_get, mock_dns, ed25519_keypair):
        private_key, pub_str = ed25519_keypair
        doc = self._create_v1_doc(private_key, pub_str, agent_id="agent://default/my-agent")

        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_res.json.return_value = doc
        mock_get.return_value = mock_res

        success, reason, _ = verify_agent_registration("agent://default/my-agent", "example.com", "https://example.com/agent.json")
        assert success is False
        assert reason == "DNS failed"

    @patch("registry.verifier.verify_endpoint_health", return_value=(False, "Healthcheck failed"))
    @patch("registry.verifier.verify_dns_txt", return_value=(True, ""))
    @patch("registry.verifier.safe_requests_get")
    def test_registration_healthcheck_failure(self, mock_get, mock_dns, mock_health, ed25519_keypair):
        private_key, pub_str = ed25519_keypair
        doc = self._create_v1_doc(private_key, pub_str, agent_id="agent://default/my-agent")

        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_res.json.return_value = doc
        mock_get.return_value = mock_res

        success, reason, _ = verify_agent_registration("agent://default/my-agent", "example.com", "https://example.com/agent.json")
        assert success is False
        assert reason == "Healthcheck failed"
