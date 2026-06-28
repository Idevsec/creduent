import os
import sys
import json
import base64
import requests
from mcp.server.fastmcp import FastMCP
from datetime import datetime, timezone
from creduent.verify import verify
from creduent.utils import safe_requests_get, load_dotenv

# Load local environment variables if present
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("Creduent Verification Server")

def verify_registry_signature(attestation_obj: dict) -> bool:
    """
    Verifies that the attestation signature is valid and signed by the registry key.
    Checks registry.signer if present/configured, falling back to direct public key verification from CREDUENT_REGISTRY_PUBKEY.
    """
    try:
        from registry.signer import verify_attestation
        return verify_attestation(attestation_obj)
    except Exception:
        pass
            
    pubkey_env = os.environ.get("CREDUENT_REGISTRY_PUBKEY") or os.environ.get("CREDUENT_REGISTRY_PUBLIC_KEY")
    if not pubkey_env:
        return False
        
    try:
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from creduent.crypto import canonicalize
        if pubkey_env.startswith("ed25519:"):
            pubkey_env = pubkey_env.split(":", 1)[1]
        pubkey_bytes = base64.b64decode(pubkey_env)
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(pubkey_bytes)
        
        signature_b64 = attestation_obj.get("signature")
        if not signature_b64:
            return False
        signature_bytes = base64.b64decode(signature_b64)
        
        obj_copy = attestation_obj.copy()
        obj_copy.pop("signature", None)
        canonical_str = canonicalize(obj_copy)
        canonical_bytes = canonical_str.encode('utf-8')
        
        public_key.verify(signature_bytes, canonical_bytes)
        return True
    except Exception:
        return False


@mcp.tool()
def verify_agent(target: str) -> dict:
    """
    Verify the identity of a Creduent agent using their domain or agent:// URI,
    and query the Creduent Registry for attestation status.
    
    Args:
        target: The agent's agent:// URI (e.g. agent://creduent/reconbot) or domain (e.g. creduent.idevsec.com).
        
    Returns:
        A dictionary with the verification details and attestation level.
    """
    checked_at = datetime.now(timezone.utc).isoformat(timespec='seconds').replace("+00:00", "Z")
    
    response_obj = {
        "agent_id": target,
        "self_verified": False,
        "creduent_attested": False,
        "attestation_level": "unregistered",
        "attestation_issued_at": None,
        "attestation_expires_at": None,
        "public_key": "",
        "endpoint": "",
        "capabilities": [],
        "checked_at": checked_at
    }
    
    try:
        # Use the official Creduent SDK to resolve and verify the target
        verify_result = verify(target)
        
        if verify_result.valid:
            response_obj["self_verified"] = True
            response_obj["agent_id"] = verify_result.agent_id
            response_obj["public_key"] = verify_result.public_key
            response_obj["endpoint"] = verify_result.endpoint
            response_obj["capabilities"] = verify_result.capabilities
    except Exception as e:
        print(f"Error during agent verification: {e}")
        
    # Query Creduent registry if self_verified is True
    if response_obj["self_verified"]:
        agent_id = response_obj["agent_id"]
        registry_base = os.environ.get("CREDUENT_REGISTRY_URL", "http://localhost:8001").rstrip('/')
        query_url = f"{registry_base}/attest/{agent_id}"
        
        try:
            r = safe_requests_get(query_url, timeout=5, allow_private=True)
            if r.status_code == 200:
                attestation_obj = r.json()
                if verify_registry_signature(attestation_obj):
                    response_obj["creduent_attested"] = True
                    response_obj["attestation_level"] = attestation_obj.get("level", "verified")
                    response_obj["attestation_issued_at"] = attestation_obj.get("issued_at")
                    response_obj["attestation_expires_at"] = attestation_obj.get("expires_at")
                else:
                    response_obj["attestation_level"] = "unregistered"
            elif r.status_code == 404:
                response_obj["attestation_level"] = "unregistered"
            else:
                response_obj["attestation_level"] = "registry_offline"
        except Exception:
            # Graceful degrade if registry is offline or unreachable
            response_obj["attestation_level"] = "registry_offline"
            
    return response_obj

if __name__ == "__main__":
    mcp.run()
