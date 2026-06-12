import os
import sys
import json
import base64
import requests
import jsonschema
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature
from mcp.server.fastmcp import FastMCP
from datetime import datetime, timezone

# Add parent directory to path to allow importing from creduent package
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)
from creduent.crypto import canonicalize
from creduent.utils import safe_requests_get, load_dotenv

# Load local environment variables if present
load_dotenv()

SCHEMA_PATH = os.path.join(BASE_DIR, 'schemas', 'agent.schema.json')

# Initialize FastMCP server
mcp = FastMCP("Creduent Verification Server")

def resolve_target(target: str) -> str:
    """
    Resolves agent_id or domain/url to a fetchable source (URL or local path).
    """
    target = target.strip()
    
    # Check if target is a local file path
    if os.path.exists(target) or os.path.exists(os.path.join(BASE_DIR, target)):
        return target

    if target.startswith("agent://"):
        import urllib.parse
        parsed = urllib.parse.urlparse(target)
        namespace = parsed.netloc
        path_parts = parsed.path.strip("/").split("/")
        if not namespace or not path_parts or not path_parts[0]:
            raise ValueError("Agent ID must follow format: agent://<namespace>/<agent-name>")
            
        # Try local registry first
        local_registry_path = os.path.join(BASE_DIR, "examples", "registry.json")
        if os.path.exists(local_registry_path):
            try:
                with open(local_registry_path, "r", encoding="utf-8") as f:
                    registry = json.load(f)
                    if target in registry:
                        return registry[target]
            except Exception:
                pass
                
        fallback_mappings = {
            "agent://creduent/reconbot": "examples/reconbot.agent.json"
        }
        if target in fallback_mappings:
            return fallback_mappings[target]
            
        return f"https://api.{namespace}.ai/.well-known/agent.json"
        
    # Domain or HTTPS URL
    if target.startswith("http://") or target.startswith("https://"):
        import urllib.parse
        parsed = urllib.parse.urlparse(target)
        if not parsed.path.endswith("/.well-known/agent.json"):
            path = parsed.path.rstrip('/') + "/.well-known/agent.json"
            return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, path, parsed.params, parsed.query, parsed.fragment))
        return target
    else:
        # Host name or IP, e.g. "localhost:8000" or "example.com"
        scheme = "http" if "localhost" in target or "127.0.0.1" in target else "https"
        return f"{scheme}://{target}/.well-known/agent.json"

def load_document(source: str):
    if source.startswith("http://") or source.startswith("https://"):
        allow_private = "localhost" in source or "127.0.0.1" in source
        r = safe_requests_get(source, timeout=5, allow_private=allow_private)
        r.raise_for_status()
        return r.json()
    else:
        path = source
        if not os.path.isabs(path):
            path = os.path.join(BASE_DIR, source)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Local file not found: {source}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

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
        target: The agent's agent:// URI (e.g. agent://creduent/reconbot) or domain (e.g. registry.idevsec.com).
        
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
        # 1. Resolve target
        resolved_source = resolve_target(target)
        
        # 2. Fetch/Load target document
        doc = load_document(resolved_source)
        
        # Extract metadata
        response_obj["agent_id"] = doc.get("agent_id", target)
        response_obj["public_key"] = doc.get("public_key", "")
        response_obj["endpoint"] = doc.get("endpoint", "")
        response_obj["capabilities"] = doc.get("capabilities", [])
        
        # 3. Validate against schema
        if os.path.exists(SCHEMA_PATH):
            with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                schema = json.load(f)
            jsonschema.validate(instance=doc, schema=schema)
        else:
            required = ["version", "agent_id", "owner", "public_key", "endpoint", "capabilities", "signature"]
            for field in required:
                if field not in doc:
                    raise ValueError(f"Missing required field: {field}")
            if doc["version"] != "1.0":
                raise ValueError(f"Unsupported protocol version: {doc['version']}")
                
        # 4. Verify Ed25519 signature using the embedded public key
        pk_str = doc.get("public_key", "")
        if pk_str.startswith("ed25519:"):
            pk_b64 = pk_str.split(":", 1)[1]
            public_key_bytes = base64.b64decode(pk_b64)
            public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
            
            signature_b64 = doc.get("signature")
            if signature_b64:
                signature_bytes = base64.b64decode(signature_b64)
                doc_copy = doc.copy()
                doc_copy.pop("signature", None)
                canonical_str = canonicalize(doc_copy)
                canonical_bytes = canonical_str.encode('utf-8')
                
                try:
                    public_key.verify(signature_bytes, canonical_bytes)
                    response_obj["self_verified"] = True
                except InvalidSignature:
                    pass
    except Exception:
        pass
        
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
