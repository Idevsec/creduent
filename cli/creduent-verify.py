#!/usr/bin/env python3
import sys
import os
import json
import base64
import argparse
import urllib.parse
import requests
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

# Import jsonschema if available
try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

# Add parent directory to path to allow importing from creduent package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from creduent.crypto import canonicalize

def resolve_agent_id(agent_id, local_registry_path="examples/registry.json"):
    """
    Resolves agent://<namespace>/<name> to an actual file path or HTTPS URL.
    Checks local mappings first, then falls back to standard HTTP resolution.
    """
    parsed = urllib.parse.urlparse(agent_id)
    if parsed.scheme != "agent":
        raise ValueError(f"Invalid scheme: {parsed.scheme}. Expected 'agent://'")
        
    namespace = parsed.netloc
    path_parts = parsed.path.strip("/").split("/")
    if not namespace or not path_parts or not path_parts[0]:
        raise ValueError("Agent ID must follow format: agent://<namespace>/<agent-name>")
    
    agent_name = path_parts[0]
    
    # 1. Try local registry file if it exists
    if os.path.exists(local_registry_path):
        try:
            with open(local_registry_path, "r", encoding="utf-8") as f:
                registry = json.load(f)
                if agent_id in registry:
                    print(f"[+] Found registry mapping: {agent_id} -> {registry[agent_id]}")
                    return registry[agent_id]
        except Exception as e:
            print(f"[!] Warning reading registry file: {e}")
            
    # 2. Hardcoded fallback mappings for demo/test purposes
    fallback_mappings = {
        "agent://creduent/reconbot": "examples/reconbot.agent.json"
    }
    if agent_id in fallback_mappings:
        print(f"[+] Found fallback mapping: {agent_id} -> {fallback_mappings[agent_id]}")
        return fallback_mappings[agent_id]
        
    # 3. Default resolution: HTTPS well-known endpoint
    resolved_url = f"https://api.{namespace}.ai/.well-known/agent.json"
    print(f"[+] No local mapping. Resolving {agent_id} to default endpoint: {resolved_url}")
    return resolved_url

def load_document(source):
    """
    Loads JSON from local path or URL.
    """
    if source.startswith("http://") or source.startswith("https://"):
        print(f"[+] Fetching remote agent.json from {source}...")
        try:
            r = requests.get(source, timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"[-] Error: Failed to fetch remote document: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Local path
        print(f"[+] Reading local document from {source}...")
        if not os.path.exists(source):
            print(f"[-] Error: File not found at {source}", file=sys.stderr)
            sys.exit(1)
        try:
            with open(source, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[-] Error: Invalid JSON syntax: {e}", file=sys.stderr)
            sys.exit(1)

def validate_schema(doc, schema_path="schemas/agent.schema.json"):
    """
    Validates document against the official JSON schema.
    """
    print("[+] Validating against JSON schema...")
    if not os.path.exists(schema_path):
        print(f"[!] Warning: Schema file not found at {schema_path}. Running manual checks instead.")
        manual_validation(doc)
        return

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
    except Exception as e:
        print(f"[-] Error loading schema: {e}", file=sys.stderr)
        sys.exit(1)

    if HAS_JSONSCHEMA:
        try:
            jsonschema.validate(instance=doc, schema=schema)
            print("[OK] agent.json schema is valid")
        except jsonschema.exceptions.ValidationError as e:
            print(f"[-] Schema Validation Error: {e.message}", file=sys.stderr)
            sys.exit(1)
    else:
        print("[!] jsonschema module missing, executing manual fallback validation.")
        manual_validation(doc)

def manual_validation(doc):
    """
    Fallback validator checking required properties and basic syntax.
    """
    required = ["version", "agent_id", "owner", "public_key", "endpoint", "capabilities", "signature"]
    for field in required:
        if field not in doc:
            print(f"[-] Manual Schema Error: Missing required field '{field}'", file=sys.stderr)
            sys.exit(1)
            
    if doc["version"] != "1.0":
        print(f"[-] Manual Schema Error: version must be '1.0', got '{doc['version']}'", file=sys.stderr)
        sys.exit(1)
        
    if not doc["agent_id"].startswith("agent://"):
        print("[-] Manual Schema Error: agent_id must follow agent:// protocol scheme", file=sys.stderr)
        sys.exit(1)
        
    if not doc["public_key"].startswith("ed25519:"):
        print("[-] Manual Schema Error: public_key must specify ed25519 prefix", file=sys.stderr)
        sys.exit(1)
        
    if not isinstance(doc["capabilities"], list):
        print("[-] Manual Schema Error: capabilities must be an array of strings", file=sys.stderr)
        sys.exit(1)

    print("[OK] Manual schema fallback validation passed")

def verify_identity(doc):
    # 1. Parse public key
    pk_str = doc["public_key"]
    if not pk_str.startswith("ed25519:"):
        print("[-] Error: Unsupported public key format.", file=sys.stderr)
        sys.exit(1)
    
    pk_b64 = pk_str.split(":", 1)[1]
    try:
        public_key_bytes = base64.b64decode(pk_b64)
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
    except Exception as e:
        print(f"[-] Error: Invalid public key encoding: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Extract signature
    signature_b64 = doc.get("signature")
    if not signature_b64:
        print("[-] Error: Document has no signature.", file=sys.stderr)
        sys.exit(1)

    try:
        signature_bytes = base64.b64decode(signature_b64)
    except Exception as e:
        print(f"[-] Error: Invalid base64 signature encoding: {e}", file=sys.stderr)
        sys.exit(1)

    # 3. Create document clone without signature
    doc_copy = doc.copy()
    doc_copy.pop("signature", None)

    # 4. Canonicalize signature-less payload
    print("[+] Canonicalizing document using JCS (RFC 8785)...")
    try:
        canonical_str = canonicalize(doc_copy)
        canonical_bytes = canonical_str.encode('utf-8')
        print("[OK] JCS canonicalization successful")
    except Exception as e:
        print(f"[-] Error: Canonicalization failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 5. Verify signature
    print("[+] Verifying Ed25519 signature...")
    try:
        public_key.verify(signature_bytes, canonical_bytes)
        print("[OK] Ed25519 signature is cryptographically valid")
    except InvalidSignature:
        print("[-] Verification Failure: Ed25519 signature is INVALID.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[-] Error during signature verification: {e}", file=sys.stderr)
        sys.exit(1)

def check_endpoint(endpoint_url):
    print("[+] Checking endpoint connectivity...")
    try:
        # Use GET or HEAD request with a short timeout to check endpoint availability
        r = requests.get(endpoint_url, timeout=2.5)
        # If it returns any HTTP code, it is reachable.
        print(f"[OK] Endpoint is reachable (HTTP {r.status_code})")
    except Exception as e:
        print(f"[!] Warning: Endpoint is offline or unreachable: {e}")

def main():
    parser = argparse.ArgumentParser(description="Creduent Protocol - Verification Utility")
    parser.add_argument("command", choices=["verify"], help="Command to execute")
    parser.add_argument("target", help="Agent identifier: filepath, domain, agent:// URI, or HTTPS URL")
    parser.add_argument("--registry", default="examples/registry.json", help="Path to local resolver registry mappings")
    parser.add_argument("--schema", default="schemas/agent.schema.json", help="Path to agent.schema.json")
    parser.add_argument("--no-healthcheck", action="store_true", help="Skip checking endpoint connectivity")

    args = parser.parse_args()

    target = args.target

    # Resolve agent URI if target is agent://
    if target.startswith("agent://"):
        print(f"[+] Resolving URI namespace: {target}")
        try:
            target = resolve_agent_id(target, local_registry_path=args.registry)
        except Exception as e:
            print(f"[-] Error resolving Agent ID: {e}", file=sys.stderr)
            sys.exit(1)

    # Load agent.json document
    doc = load_document(target)

    # Validate Schema structure
    validate_schema(doc, schema_path=args.schema)

    # Verify cryptographic signature
    verify_identity(doc)

    # Health check endpoint connectivity
    if not args.no_healthcheck and "endpoint" in doc:
        check_endpoint(doc["endpoint"])

    print("=========================================")
    print("[SUCCESS] IDENTITY AND SYSTEM VERIFIED SUCCESSFULLY")
    print("=========================================")

if __name__ == "__main__":
    main()
