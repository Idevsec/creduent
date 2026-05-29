import os
import sys
import base64
from datetime import datetime, timezone, timedelta
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

# Add parent directory to path to allow importing from creduent package
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)
from creduent.crypto import canonicalize
from creduent.utils import load_dotenv

# Load local environment variables if present
load_dotenv()

def get_registry_private_key():
    """
    Loads Ed25519 registry private key from environment variable CREDUENT_REGISTRY_KEY or local fallback.
    """
    pkey_env = os.environ.get("CREDUENT_REGISTRY_KEY")
    if pkey_env:
        try:
            if "-----BEGIN PRIVATE KEY-----" not in pkey_env:
                pkey_bytes = base64.b64decode(pkey_env)
            else:
                pkey_bytes = pkey_env.encode('utf-8')
            return serialization.load_pem_private_key(pkey_bytes, password=None)
        except Exception as e:
            print(f"[-] Error loading registry private key from env: {e}", file=sys.stderr)
            
    # Fallback to local file
    key_file = "registry_private_key.pem"
    if os.path.exists(key_file):
        try:
            with open(key_file, "rb") as f:
                return serialization.load_pem_private_key(f.read(), password=None)
        except Exception as e:
            print(f"[-] Error loading registry private key from file: {e}", file=sys.stderr)
            
    return None

def get_registry_public_key():
    """
    Loads Ed25519 registry public key from environment variable CREDUENT_REGISTRY_PUBKEY
    (or CREDUENT_REGISTRY_PUBLIC_KEY), or falls back to deriving from registry private key,
    or reading from registry_public_key.pem.
    """
    pubkey_env = os.environ.get("CREDUENT_REGISTRY_PUBKEY") or os.environ.get("CREDUENT_REGISTRY_PUBLIC_KEY")
    if pubkey_env:
        try:
            if pubkey_env.startswith("ed25519:"):
                pubkey_env = pubkey_env.split(":", 1)[1]
            try:
                pubkey_bytes = base64.b64decode(pubkey_env)
                return ed25519.Ed25519PublicKey.from_public_bytes(pubkey_bytes)
            except Exception:
                if "-----BEGIN PUBLIC KEY-----" in pubkey_env:
                    return serialization.load_pem_public_key(pubkey_env.encode('utf-8'))
        except Exception as e:
            print(f"[-] Error loading registry public key from env: {e}", file=sys.stderr)

    # Fallback: Derive from private key if private key is available
    private_key = get_registry_private_key()
    if private_key:
        try:
            return private_key.public_key()
        except Exception as e:
            print(f"[-] Error deriving public key from private key: {e}", file=sys.stderr)

    # Fallback to local file registry_public_key.pem
    pub_file = "registry_public_key.pem"
    if os.path.exists(pub_file):
        try:
            with open(pub_file, "rb") as f:
                return serialization.load_pem_public_key(f.read())
        except Exception as e:
            print(f"[-] Error loading registry public key from file: {e}", file=sys.stderr)

    return None

def sign_attestation(agent_data: dict) -> dict:
    """
    Constructs and signs a registry attestation for the verified agent.
    """
    private_key = get_registry_private_key()
    if not private_key:
        raise ValueError("CREDUENT_REGISTRY_KEY environment variable is not set or invalid.")
        
    issued_at_dt = datetime.now(timezone.utc)
    expires_at_dt = issued_at_dt + timedelta(days=365)
    
    issued_at = issued_at_dt.isoformat(timespec='seconds').replace("+00:00", "Z")
    expires_at = expires_at_dt.isoformat(timespec='seconds').replace("+00:00", "Z")
    
    attestation_obj = {
        "agent_id": agent_data["agent_id"],
        "issuer": "agent://creduent/registry",
        "level": "verified",
        "issued_at": issued_at,
        "expires_at": expires_at,
        "public_key": agent_data["public_key"],
        "domain": agent_data["domain"]
    }
    
    canonical_str = canonicalize(attestation_obj)
    canonical_bytes = canonical_str.encode('utf-8')
    signature_bytes = private_key.sign(canonical_bytes)
    signature_b64 = base64.b64encode(signature_bytes).decode('utf-8')
    
    attestation_obj["signature"] = signature_b64
    return attestation_obj

def verify_attestation(attestation_obj: dict) -> bool:
    """
    Verifies that the attestation signature is valid and signed by the registry key.
    """
    public_key = get_registry_public_key()
    if not public_key:
        raise ValueError("Registry public key not configured, cannot verify attestation.")
    
    signature_b64 = attestation_obj.get("signature")
    if not signature_b64:
        return False
        
    try:
        signature_bytes = base64.b64decode(signature_b64)
        obj_copy = attestation_obj.copy()
        obj_copy.pop("signature", None)
        
        canonical_str = canonicalize(obj_copy)
        canonical_bytes = canonical_str.encode('utf-8')
        
        public_key.verify(signature_bytes, canonical_bytes)
        return True
    except Exception:
        return False

