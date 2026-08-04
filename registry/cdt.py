import uuid
import base64
from datetime import datetime, timezone, timedelta
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from creduent.crypto import canonicalize

MAX_DELEGATION_DEPTH = 5

def issue_cdt(
    delegator_privkey: ed25519.Ed25519PrivateKey, 
    delegator_id: str,
    delegate_id: str, 
    delegate_public_key: str, 
    capabilities: list, 
    reversibility_tier: str, 
    tools: list = None, 
    limits: dict = None, 
    intent_hash: str = "none"
) -> dict:
    """
    Issues a signed Creduent Delegation Token (CDT).
    """
    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(hours=1)
    
    cdt = {
        "token_id": f"cdt_{uuid.uuid4().hex}",
        "issued_at": issued_at.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "expires_at": expires_at.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "delegator": delegator_id,
        "delegate": delegate_id,
        "delegate_public_key": delegate_public_key,
        "constraints": {
            "capabilities": capabilities,
            "reversibility_tier": reversibility_tier
        },
        "intent_hash": intent_hash
    }
    
    if tools is not None:
        cdt["constraints"]["tools"] = tools
    if limits is not None:
        cdt["constraints"]["limits"] = limits
        
    canonical_str = canonicalize(cdt)
    canonical_bytes = canonical_str.encode("utf-8")
    
    signature_bytes = delegator_privkey.sign(canonical_bytes)
    cdt["signature"] = base64.b64encode(signature_bytes).decode("utf-8")
    
    return cdt

def verify_cdt(token: dict, delegator_pubkey_b64: str) -> tuple[bool, str]:
    """
    Verifies a single CDT signature, structure, and expiration.
    """
    required_keys = {"token_id", "issued_at", "expires_at", "delegator", "delegate", 
                     "delegate_public_key", "constraints", "intent_hash", "signature"}
    
    if not required_keys.issubset(token.keys()):
        return False, "Missing required fields"
        
    constraints = token["constraints"]
    if "capabilities" not in constraints or "reversibility_tier" not in constraints:
        return False, "Missing required constraints"
        
    try:
        expires_at = datetime.fromisoformat(token["expires_at"].replace("Z", "+00:00"))
        if datetime.now(timezone.utc) > expires_at:
            return False, "Token expired"
    except Exception:
        return False, "Invalid expiration timestamp"
        
    signature_b64 = token.get("signature")
    if not signature_b64:
        return False, "Missing signature"
        
    try:
        # Parse delegator public key
        if delegator_pubkey_b64.startswith("ed25519:"):
            delegator_pubkey_b64 = delegator_pubkey_b64.split(":", 1)[1]
            
        pubkey_bytes = base64.b64decode(delegator_pubkey_b64)
        
        try:
            pubkey = ed25519.Ed25519PublicKey.from_public_bytes(pubkey_bytes)
        except Exception:
            try:
                pubkey = serialization.load_pem_public_key(pubkey_bytes)
            except Exception:
                pubkey = serialization.load_der_public_key(pubkey_bytes)

        signature_bytes = base64.b64decode(signature_b64)

        obj_copy = token.copy()
        obj_copy.pop("signature", None)
        
        canonical_str = canonicalize(obj_copy)
        canonical_bytes = canonical_str.encode("utf-8")
        
        pubkey.verify(signature_bytes, canonical_bytes)
        return True, "Valid"
    except Exception as e:
        return False, f"Invalid signature or key: {str(e)}"

def verify_delegation_chain(chain: list[dict], root_pubkey_b64: str) -> tuple[bool, str]:
    """
    Verifies a multi-hop delegation chain, enforcing MAX_DELEGATION_DEPTH,
    cycle detection, and strict capability attenuation.
    """
    if not chain:
        return False, "Empty chain"
        
    if len(chain) > MAX_DELEGATION_DEPTH:
        return False, f"Chain exceeds MAX_DELEGATION_DEPTH of {MAX_DELEGATION_DEPTH}"
        
    seen_delegators = set()
    current_pubkey = root_pubkey_b64
    previous_capabilities = None
    
    tier_levels = {"READ_ONLY": 0, "REVERSIBLE": 1, "IRREVERSIBLE": 2}
    previous_tier = 2
    
    for i, token in enumerate(chain):
        is_valid, msg = verify_cdt(token, current_pubkey)
        if not is_valid:
            return False, f"Token {i} invalid: {msg}"
            
        delegator = token["delegator"]
        delegate = token["delegate"]
        
        # Cycle detection
        if delegator in seen_delegators or delegate in seen_delegators or delegate == delegator:
            return False, f"Cycle detected at token {i}"
        seen_delegators.add(delegator)
        
        # Attenuation checks
        constraints = token["constraints"]
        capabilities = set(constraints["capabilities"])
        tier = constraints["reversibility_tier"]
        
        tier_val = tier_levels.get(tier, -1)
        if tier_val > previous_tier:
            return False, f"Reversibility tier escalation at token {i}"
        previous_tier = tier_val
        
        if previous_capabilities is not None:
            if "*" not in previous_capabilities:
                if "*" in capabilities or not capabilities.issubset(previous_capabilities):
                    return False, f"Capability escalation at token {i}"
                    
        previous_capabilities = capabilities
        current_pubkey = token["delegate_public_key"]
        
    return True, "Chain valid"
