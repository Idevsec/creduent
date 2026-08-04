import os
import base64
import pytest
from unittest.mock import patch, mock_open, MagicMock
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from registry.signer import (
    get_registry_private_key,
    get_registry_public_key,
    sign_attestation,
    verify_attestation,
)


@pytest.fixture
def sample_keypair():
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key


def test_get_private_key_env_pem(monkeypatch, sample_keypair):
    priv, _ = sample_keypair
    pem_bytes = priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    monkeypatch.setenv("CREDUENT_REGISTRY_KEY", pem_bytes.decode("utf-8"))
    key = get_registry_private_key()
    assert key is not None
    assert isinstance(key, ed25519.Ed25519PrivateKey)


def test_get_private_key_env_b64_raw(monkeypatch, sample_keypair):
    priv, _ = sample_keypair
    raw_bytes = priv.private_bytes_raw()
    b64_str = base64.b64encode(raw_bytes).decode("utf-8")
    monkeypatch.setenv("CREDUENT_REGISTRY_KEY", b64_str)
    key = get_registry_private_key()
    assert key is not None
    assert isinstance(key, ed25519.Ed25519PrivateKey)


def test_get_private_key_env_b64_der(monkeypatch, sample_keypair):
    priv, _ = sample_keypair
    der_bytes = priv.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    b64_str = base64.b64encode(der_bytes).decode("utf-8")
    monkeypatch.setenv("CREDUENT_REGISTRY_KEY", b64_str)
    key = get_registry_private_key()
    assert key is not None
    assert isinstance(key, ed25519.Ed25519PrivateKey)


def test_get_private_key_env_invalid(monkeypatch):
    monkeypatch.setenv("CREDUENT_REGISTRY_KEY", "invalid_base64_content!!!")
    with patch("os.path.exists", return_value=False):
        key = get_registry_private_key()
        assert key is None


def test_get_private_key_file_fallback(monkeypatch, sample_keypair):
    priv, _ = sample_keypair
    pem_bytes = priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    monkeypatch.delenv("CREDUENT_REGISTRY_KEY", raising=False)
    with patch("os.path.exists", lambda path: path == "registry_private_key.pem"):
        with patch("builtins.open", mock_open(read_data=pem_bytes)):
            key = get_registry_private_key()
            assert key is not None


def test_get_private_key_file_error(monkeypatch):
    monkeypatch.delenv("CREDUENT_REGISTRY_KEY", raising=False)
    with patch("os.path.exists", lambda path: path == "registry_private_key.pem"):
        with patch("builtins.open", side_effect=IOError("Permission denied")):
            key = get_registry_private_key()
            assert key is None


def test_get_public_key_env_raw_prefix(monkeypatch, sample_keypair):
    _, pub = sample_keypair
    raw_bytes = pub.public_bytes_raw()
    b64_str = base64.b64encode(raw_bytes).decode("utf-8")
    monkeypatch.setenv("CREDUENT_REGISTRY_PUBKEY", f"ed25519:{b64_str}")
    key = get_registry_public_key()
    assert key is not None
    assert isinstance(key, ed25519.Ed25519PublicKey)


def test_get_public_key_env_pem(monkeypatch, sample_keypair):
    _, pub = sample_keypair
    pem_bytes = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    monkeypatch.setenv("CREDUENT_REGISTRY_PUBKEY", pem_bytes.decode("utf-8"))
    key = get_registry_public_key()
    assert key is not None


def test_get_public_key_env_der(monkeypatch, sample_keypair):
    _, pub = sample_keypair
    der_bytes = pub.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    b64_str = base64.b64encode(der_bytes).decode("utf-8")
    monkeypatch.setenv("CREDUENT_REGISTRY_PUBKEY", b64_str)
    key = get_registry_public_key()
    assert key is not None


def test_get_public_key_derive_from_private(monkeypatch, sample_keypair):
    priv, _ = sample_keypair
    monkeypatch.delenv("CREDUENT_REGISTRY_PUBKEY", raising=False)
    monkeypatch.delenv("CREDUENT_REGISTRY_PUBLIC_KEY", raising=False)
    with patch("registry.signer.get_registry_private_key", return_value=priv):
        key = get_registry_public_key()
        assert key is not None
        assert isinstance(key, ed25519.Ed25519PublicKey)


def test_get_public_key_derive_error(monkeypatch):
    mock_priv = MagicMock()
    mock_priv.public_key.side_effect = Exception("Derivation error")
    monkeypatch.delenv("CREDUENT_REGISTRY_PUBKEY", raising=False)
    monkeypatch.delenv("CREDUENT_REGISTRY_PUBLIC_KEY", raising=False)
    with patch("registry.signer.get_registry_private_key", return_value=mock_priv), \
         patch("os.path.exists", return_value=False):
        key = get_registry_public_key()
        assert key is None


def test_get_public_key_file_fallback(monkeypatch, sample_keypair):
    _, pub = sample_keypair
    pem_bytes = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    monkeypatch.delenv("CREDUENT_REGISTRY_PUBKEY", raising=False)
    monkeypatch.delenv("CREDUENT_REGISTRY_PUBLIC_KEY", raising=False)
    with patch("registry.signer.get_registry_private_key", return_value=None), \
         patch("os.path.exists", lambda p: p == "registry_public_key.pem"), \
         patch("builtins.open", mock_open(read_data=pem_bytes)):
        key = get_registry_public_key()
        assert key is not None


def test_get_public_key_file_error(monkeypatch):
    monkeypatch.delenv("CREDUENT_REGISTRY_PUBKEY", raising=False)
    monkeypatch.delenv("CREDUENT_REGISTRY_PUBLIC_KEY", raising=False)
    with patch("registry.signer.get_registry_private_key", return_value=None), \
         patch("os.path.exists", lambda p: p == "registry_public_key.pem"), \
         patch("builtins.open", side_effect=IOError("Read error")):
        key = get_registry_public_key()
        assert key is None


def test_sign_and_verify_attestation_success(monkeypatch, sample_keypair):
    priv, pub = sample_keypair
    agent_data = {
        "agent_id": "agent://creduent/test1",
        "public_key": "ed25519:testpub",
        "domain": "test1.com"
    }
    with patch("registry.signer.get_registry_private_key", return_value=priv), \
         patch("registry.signer.get_registry_public_key", return_value=pub):
        attestation = sign_attestation(agent_data, level="verified")
        assert attestation["agent_id"] == "agent://creduent/test1"
        assert attestation["level"] == "verified"
        assert "signature" in attestation
        assert verify_attestation(attestation) is True


def test_sign_attestation_no_key():
    with patch("registry.signer.get_registry_private_key", return_value=None):
        with pytest.raises(ValueError, match="not set or invalid"):
            sign_attestation({"agent_id": "a", "public_key": "b", "domain": "c"})


def test_verify_attestation_no_key():
    with patch("registry.signer.get_registry_public_key", return_value=None):
        with pytest.raises(ValueError, match="not configured"):
            verify_attestation({"signature": "xxx"})


def test_verify_attestation_no_signature(sample_keypair):
    _, pub = sample_keypair
    with patch("registry.signer.get_registry_public_key", return_value=pub):
        assert verify_attestation({"agent_id": "a"}) is False


def test_verify_attestation_invalid_signature(sample_keypair):
    _, pub = sample_keypair
    with patch("registry.signer.get_registry_public_key", return_value=pub):
        assert verify_attestation({"agent_id": "a", "signature": "invalid_base64++"}) is False
