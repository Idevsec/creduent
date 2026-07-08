import os
import sys
import json
import base64
import jsonschema
import dns.resolver
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

# Add parent directory to path to allow importing from creduent package
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)
from creduent.crypto import canonicalize
from creduent.utils import safe_requests_get

SCHEMA_PATH = os.path.join(BASE_DIR, "schemas", "agent.schema.json")


def verify_dns_txt(domain: str, agent_id: str) -> tuple[bool, str]:
    """
    Checks if _creduent.{domain} contains the agent_id in its TXT records.
    """
    txt_record_name = f"_creduent.{domain}"
    try:
        answers = dns.resolver.resolve(txt_record_name, "TXT")
        for rdata in answers:
            # Combine all pieces of the TXT record
            txt_content = "".join([s.decode("utf-8") for s in rdata.strings])
            if agent_id in txt_content:
                return True, ""
        return (
            False,
            f"DNS TXT record at {txt_record_name} found, but does not contain agent_id '{agent_id}'.",
        )
    except dns.resolver.NXDOMAIN:
        return False, f"DNS TXT record not found at {txt_record_name} (NXDOMAIN)."
    except dns.resolver.NoAnswer:
        return False, f"No TXT records found at {txt_record_name}."
    except Exception as e:
        return False, f"DNS TXT resolution failed: {str(e)}"


def verify_endpoint_health(endpoint_url: str) -> tuple[bool, str]:
    """
    Performs GET request to the agent endpoint URL to verify connectivity.
    """
    try:
        # Outbound GET request with SSRF protection
        response = safe_requests_get(endpoint_url, timeout=5)
        return True, ""
    except Exception as e:
        err_msg = str(e)
        if hasattr(e, "detail"):
            err_msg = e.detail
        return False, f"Endpoint healthcheck failed: {err_msg}"


def verify_agent_registration(
    agent_id: str, domain: str, agent_json_url: str
) -> tuple[bool, str, dict]:
    """
    Main verification pipeline for registering an agent.
    Returns (success: bool, reason: str, agent_json_dict: dict)
    """
    # 1. Fetch agent_json_url
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Creduent-Registry/1.0; +https://creduent.idevsec.com)",
            "Accept": "application/json",
        }
        response = safe_requests_get(agent_json_url, timeout=5, headers=headers)
        if response.status_code != 200:
            return False, f"Failed to fetch agent.json: HTTP {response.status_code}", {}
        doc = response.json()
    except Exception as e:
        err_msg = str(e)
        if hasattr(e, "detail"):
            err_msg = e.detail
        return False, f"Failed to fetch agent.json: {err_msg}", {}

    # 2. Validate against schema
    version = doc.get("version", "1.0")
    if version not in ["1.0", "1.1", "2.0"]:
        return False, f"Unsupported protocol version: {version}", {}

    schema_file = "agent.v2.schema.json" if version == "2.0" else "agent.schema.json"
    schema_path = os.path.join(BASE_DIR, "schemas", schema_file)

    if os.path.exists(schema_path):
        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                schema = json.load(f)
            jsonschema.validate(instance=doc, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            return False, f"Schema validation failed: {e.message}", {}
        except Exception as e:
            return False, f"Failed to run schema validation: {str(e)}", {}
    else:
        # Fallback manual validation
        if version == "2.0":
            required = ["version", "identity", "policy", "signature"]
            for field in required:
                if field not in doc:
                    return False, f"Manual schema validation failed: missing field '{field}'", {}
            identity = doc.get("identity", {})
            required_identity = ["agent_id", "owner", "keys", "endpoint"]
            for field in required_identity:
                if field not in identity:
                    return False, f"Manual schema validation failed: missing field 'identity.{field}'", {}
            policy = doc.get("policy", {})
            if "capabilities" not in policy:
                return False, f"Manual schema validation failed: missing field 'policy.capabilities'", {}
        else:
            required = [
                "version",
                "agent_id",
                "owner",
                "public_key",
                "endpoint",
                "capabilities",
                "signature",
            ]
            for field in required:
                if field not in doc:
                    return (
                        False,
                        f"Manual schema validation failed: missing field '{field}'",
                        {},
                    )

    # 3. Verify agent_id matches input
    doc_agent_id = doc.get("identity", {}).get("agent_id") if version == "2.0" else doc.get("agent_id")
    if doc_agent_id != agent_id:
        return (
            False,
            f"agent_id in agent.json ('{doc_agent_id}') does not match registration agent_id ('{agent_id}').",
            {},
        )

    # 4. Verify Ed25519 signature
    if version == "2.0":
        keys = doc.get("identity", {}).get("keys", [])
    else:
        pk_str = doc.get("public_key", "")
        keys = [{"id": "legacy", "type": "ed25519", "public_key": pk_str, "status": "active"}]

    signature_b64 = doc.get("signature")
    if not signature_b64:
        return False, "agent.json has no signature.", {}

    try:
        signature_bytes = base64.b64decode(signature_b64)
    except Exception:
        return False, "Signature is not valid base64.", {}

    # Clone and canonicalize signature-less payload
    doc_copy = doc.copy()
    doc_copy.pop("signature", None)
    try:
        canonical_str = canonicalize(doc_copy)
        canonical_bytes = canonical_str.encode("utf-8")
    except Exception as e:
        return False, f"Failed during canonicalization: {str(e)}", {}

    verified = False
    validation_error = "No active valid keys found."
    for key_entry in keys:
        if not isinstance(key_entry, dict):
            continue
        if key_entry.get("status") != "active":
            continue
        pub_key_str = key_entry.get("public_key", "")
        if not pub_key_str.startswith("ed25519:"):
            validation_error = "Unsupported public key format. Only 'ed25519:' prefix is supported."
            continue
        try:
            pk_b64 = pub_key_str.split(":", 1)[1]
            public_key_bytes = base64.b64decode(pk_b64)
            public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
            public_key.verify(signature_bytes, canonical_bytes)
            verified = True
            break
        except InvalidSignature:
            validation_error = "Cryptographic signature in agent.json is INVALID for the tested key."
        except Exception as e:
            validation_error = f"Signature verification failed: {e}"

    if not verified:
        return False, validation_error, {}

    # 5. DNS TXT lookup check
    dns_ok, dns_err = verify_dns_txt(domain, agent_id)
    if not dns_ok:
        return False, dns_err, {}

    # 6. Endpoint healthcheck
    endpoint_url = doc.get("identity", {}).get("endpoint", "") if version == "2.0" else doc.get("endpoint", "")
    endpoint_ok, endpoint_err = verify_endpoint_health(endpoint_url)
    if not endpoint_ok:
        return False, endpoint_err, {}

    return True, "Verification successful", doc
