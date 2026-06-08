import os
import sys
import time
import secrets
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, HTTPException, Request, APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Add parent directory to path to allow importing from registry and creduent packages
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

from registry.store import save_attestation, get_attestation, revoke_agent, list_agents, is_redis_configured, get_redis_client, save_webhook, get_webhook, diagnose_redis, save_challenge, get_challenge, delete_challenge
from registry.signer import sign_attestation
from registry.verifier import verify_agent_registration
from registry.templates import RESOLVER_HTML, DASHBOARD_HTML
from creduent.utils import load_dotenv

# Load local environment variables if present
load_dotenv()

# Emit Redis diagnostics to Vercel function logs on cold start
diagnose_redis()

app = FastAPI(title="Creduent Attestation Registry", version="1.0")
router = APIRouter()

class RegisterRequest(BaseModel):
    agent_id: str
    domain: str
    agent_json_url: str

class RenewRequest(BaseModel):
    agent_id: str
    new_expires_at: str
    signature: str

class WebhookRegisterRequest(BaseModel):
    agent_id: str
    webhook_url: str
    signature: str

class AttestRequest(BaseModel):
    agent_id: str
    domain: str
    public_key: str

class AdminUpgradeRequest(BaseModel):
    agent_id: str
    level: str  # "unverified" | "verified" | "trusted"

class VerifyChallengeRequest(BaseModel):
    agent_id: str
    nonce: str
    signature: str

CHALLENGE_RATE_LIMIT_WINDOW = 60 # 1 minute
CHALLENGE_RATE_LIMIT_MAX = 10

def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

# Rate limiting for open /register endpoint: 5 registrations per hour per IP
REGISTER_RATE_LIMIT_WINDOW = 3600   # 1 hour
REGISTER_RATE_LIMIT_MAX = 5

def check_register_rate_limit(request: Request):
    """Rate limit open /register endpoint: max 5 per IP per hour."""
    client_ip = get_client_ip(request)
    if client_ip == "unknown":
        return

    now = int(time.time())
    key = f"reg_limit:{client_ip}"

    if is_redis_configured():
        try:
            client = get_redis_client()
            current = client.get(key)
            if current is not None:
                count = int(current)
                if count >= REGISTER_RATE_LIMIT_MAX:
                    raise HTTPException(
                        status_code=429,
                        detail="Too many registration requests. Max 5 per hour per IP."
                    )
                client.incr(key)
            else:
                client.set(key, "1", ex=REGISTER_RATE_LIMIT_WINDOW)
        except HTTPException:
            raise
        except Exception as e:
            print(f"[-] Rate limit Redis error: {e}", file=sys.stderr)
    else:
        if not hasattr(app, "reg_rate_db"):
            app.reg_rate_db = {}
        app.reg_rate_db = {k: v for k, v in app.reg_rate_db.items() if v["expiry"] > now}
        if key in app.reg_rate_db:
            entry = app.reg_rate_db[key]
            if entry["count"] >= REGISTER_RATE_LIMIT_MAX:
                raise HTTPException(
                    status_code=429,
                    detail="Too many registration requests. Max 5 per hour per IP."
                )
            entry["count"] += 1
        else:
            app.reg_rate_db[key] = {"count": 1, "expiry": now + REGISTER_RATE_LIMIT_WINDOW}

def check_challenge_rate_limit(request: Request):
    """Rate limit challenge requests: max 10 per IP per minute."""
    client_ip = get_client_ip(request)
    if client_ip == "unknown":
        return

    now = int(time.time())
    key = f"chal_limit:{client_ip}"

    if is_redis_configured():
        try:
            client = get_redis_client()
            current = client.get(key)
            if current is not None:
                count = int(current)
                if count >= CHALLENGE_RATE_LIMIT_MAX:
                    raise HTTPException(
                        status_code=429,
                        detail="Too many challenge requests. Max 10 per minute per IP."
                    )
                client.incr(key)
            else:
                client.set(key, "1", ex=CHALLENGE_RATE_LIMIT_WINDOW)
        except HTTPException:
            raise
        except Exception as e:
            print(f"[-] Rate limit Redis error: {e}", file=sys.stderr)
    else:
        if not hasattr(app, "chal_rate_db"):
            app.chal_rate_db = {}
        app.chal_rate_db = {k: v for k, v in app.chal_rate_db.items() if v["expiry"] > now}
        if key in app.chal_rate_db:
            entry = app.chal_rate_db[key]
            if entry["count"] >= CHALLENGE_RATE_LIMIT_MAX:
                raise HTTPException(
                    status_code=429,
                    detail="Too many challenge requests. Max 10 per minute per IP."
                )
            entry["count"] += 1
        else:
            app.chal_rate_db[key] = {"count": 1, "expiry": now + CHALLENGE_RATE_LIMIT_WINDOW}

def check_rate_limit(request: Request):
    """Generic rate limit (kept for existing endpoints that use it)."""
    check_register_rate_limit(request)


@router.post("/register")
def register(req: RegisterRequest, request: Request):
    """Open registration endpoint. Any developer can register an agent.
    DNS + agent.json verification is performed. Level is set to 'unverified'.
    Rate limited: max 5 registrations per IP per hour.
    """
    check_register_rate_limit(request)
    success, reason, doc = verify_agent_registration(
        agent_id=req.agent_id,
        domain=req.domain,
        agent_json_url=req.agent_json_url
    )
    if not success:
        raise HTTPException(status_code=400, detail=f"Verification failed: {reason}")
    agent_data = {
        "agent_id": doc["agent_id"],
        "public_key": doc["public_key"],
        "domain": req.domain
    }
    try:
        # Open registration always assigns level="unverified".
        # Use POST /admin/attest to upgrade to verified or trusted.
        attestation = sign_attestation(agent_data, level="unverified")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signing failed: {str(e)}")
    try:
        save_attestation(doc["agent_id"], attestation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database write failed: {str(e)}")
    return {**attestation, "status": "registered"}


@router.get("/attest/{agent_id:path}")
def get_attest(agent_id: str, request: Request):
    check_rate_limit(request)
    if agent_id.startswith("agent:/") and not agent_id.startswith("agent://"):

        agent_id = "agent://" + agent_id[7:]
    attestation = get_attestation(agent_id)
    if not attestation:
        raise HTTPException(status_code=404, detail="Attestation not found for agent.")
    
    expired = False
    expires_at_str = attestation.get("expires_at")
    if expires_at_str:
        try:
            expires_at = datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
            if datetime.now(timezone.utc) > expires_at:
                expired = True
        except Exception as e:
            print(f"[-] Error parsing expires_at: {e}", file=sys.stderr)
            
    level = attestation.get("level", "verified").lower()
    if level == "revoked":
        attestation["expired"] = False
        attestation["status"] = "revoked"
    elif expired:
        attestation["expired"] = True
        attestation["status"] = "expired"
    else:
        attestation["expired"] = False
        attestation["status"] = "active"
        
    return attestation

@router.get("/agents")
def get_agents():
    return list_agents()

@router.delete("/revoke/{agent_id:path}")
def revoke(agent_id: str, request: Request):
    check_rate_limit(request)
    if agent_id.startswith("agent:/") and not agent_id.startswith("agent://"):

        agent_id = "agent://" + agent_id[7:]
    admin_key_env = os.environ.get("CREDUENT_ADMIN_KEY")
    if not admin_key_env:
        raise HTTPException(status_code=500, detail="Admin revocation is not configured on server (CREDUENT_ADMIN_KEY env var missing).")
    admin_key_env = admin_key_env.strip()
    creduent_admin_key = request.headers.get("CREDUENT_ADMIN_KEY") or request.headers.get("CREDUENT-ADMIN-KEY")
    if not creduent_admin_key:
        raise HTTPException(status_code=403, detail="Forbidden: Missing CREDUENT_ADMIN_KEY header.")
    creduent_admin_key = creduent_admin_key.strip()
    if not secrets.compare_digest(creduent_admin_key.encode('utf-8'), admin_key_env.encode('utf-8')):
        raise HTTPException(status_code=403, detail="Forbidden: Invalid CREDUENT_ADMIN_KEY header.")
    revoke_agent(agent_id)
    return {"status": "revoked", "agent_id": agent_id}

@router.get("/health")
def health():
    redis_ok = is_redis_configured()
    diagnose_redis()
    return {"status": "healthy", "redis_configured": redis_ok}

# Webhook helpers moved to registry/store.py (Redis-backed)

@router.post("/renew")
def renew(req: RenewRequest, request: Request):
    check_rate_limit(request)
    import base64
    import jcs

    from cryptography.hazmat.primitives.asymmetric import ed25519
    from registry.signer import get_registry_private_key
    from creduent.crypto import canonicalize

    agent_id = req.agent_id
    if agent_id.startswith("agent:/") and not agent_id.startswith("agent://"):
        agent_id = "agent://" + agent_id[7:]

    attestation = get_attestation(agent_id)
    if not attestation:
        raise HTTPException(status_code=404, detail="Agent attestation not found")

    pk_str = attestation.get("public_key", "")
    if not pk_str.startswith("ed25519:"):
        raise HTTPException(status_code=400, detail="Unsupported public key format in attestation")

    try:
        pk_b64 = pk_str.split(":", 1)[1]
        public_key_bytes = base64.b64decode(pk_b64)
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)

        signature_bytes = base64.b64decode(req.signature)

        # 1. Try JCS canonicalized dictionary
        payload_dict = {
            "agent_id": req.agent_id,
            "new_expires_at": req.new_expires_at
        }
        canonical_bytes = jcs.canonicalize(payload_dict)

        verified = False
        try:
            public_key.verify(signature_bytes, canonical_bytes)
            verified = True
        except Exception:
            pass

        if not verified:
            # 2. Try delimited payload "agent_id|new_expires_at"
            delim_payload = f"{req.agent_id}|{req.new_expires_at}".encode('utf-8')
            try:
                public_key.verify(signature_bytes, delim_payload)
                verified = True
            except Exception:
                pass

        if not verified:
            raise HTTPException(status_code=400, detail="Invalid client signature for renewal")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Signature verification error: {str(e)}")

    private_key = get_registry_private_key()
    if not private_key:
        raise HTTPException(status_code=500, detail="Registry private key not configured")

    issued_at = datetime.now(timezone.utc).isoformat(timespec='seconds').replace("+00:00", "Z")

    renewed_attestation = {
        "agent_id": attestation["agent_id"],
        "issuer": "agent://creduent/registry",
        "level": attestation.get("level", "verified"),
        "issued_at": issued_at,
        "expires_at": req.new_expires_at,
        "public_key": attestation["public_key"],
        "domain": attestation["domain"]
    }

    try:
        canonical_str = canonicalize(renewed_attestation)
        canonical_bytes = canonical_str.encode('utf-8')
        signature_bytes = private_key.sign(canonical_bytes)
        signature_b64 = base64.b64encode(signature_bytes).decode('utf-8')
        renewed_attestation["signature"] = signature_b64
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to sign renewed attestation: {str(e)}")

    try:
        save_attestation(attestation["agent_id"], renewed_attestation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database write failed: {str(e)}")

    return renewed_attestation

@router.post("/webhook/register")
def register_webhook(req: WebhookRegisterRequest):
    import base64
    import jcs
    from cryptography.hazmat.primitives.asymmetric import ed25519

    agent_id = req.agent_id
    if agent_id.startswith("agent:/") and not agent_id.startswith("agent://"):
        agent_id = "agent://" + agent_id[7:]

    attestation = get_attestation(agent_id)
    if not attestation:
        raise HTTPException(status_code=404, detail="Agent not found in registry")

    pk_str = attestation.get("public_key", "")
    if not pk_str.startswith("ed25519:"):
        raise HTTPException(status_code=400, detail="Unsupported public key format in attestation")

    try:
        pk_b64 = pk_str.split(":", 1)[1]
        public_key_bytes = base64.b64decode(pk_b64)
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)

        signature_bytes = base64.b64decode(req.signature)

        verified = False
        
        # 1. Try JCS canonicalized dictionary
        payload_dict = {
            "agent_id": req.agent_id,
            "webhook_url": req.webhook_url
        }
        try:
            canonical_bytes = jcs.canonicalize(payload_dict)
            public_key.verify(signature_bytes, canonical_bytes)
            verified = True
        except Exception:
            pass

        if not verified:
            # 2. Try delimited payload "agent_id|webhook_url"
            delim_payload = f"{req.agent_id}|{req.webhook_url}".encode('utf-8')
            try:
                public_key.verify(signature_bytes, delim_payload)
                verified = True
            except Exception:
                pass

        if not verified:
            raise HTTPException(status_code=403, detail="Invalid client signature for webhook registration")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Signature verification error: {str(e)}")

    try:
        save_webhook(agent_id, req.webhook_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook storage failed: {str(e)}")

    return {"status": "registered", "agent_id": agent_id, "webhook_url": req.webhook_url}

@router.get("/webhook/{agent_id:path}")
def get_webhook_url(agent_id: str):
    if agent_id.startswith("agent:/") and not agent_id.startswith("agent://"):
        agent_id = "agent://" + agent_id[7:]

    webhook_url = get_webhook(agent_id)
    if not webhook_url:
        raise HTTPException(status_code=404, detail="Webhook not found for agent")

    return {"agent_id": agent_id, "webhook_url": webhook_url}

@router.post("/admin/attest")
def admin_upgrade_level(req: AdminUpgradeRequest, request: Request):
    """Admin-only: upgrade an existing agent's attestation level.
    Levels: unverified → verified → trusted.
    Requires CREDUENT_ADMIN_KEY header.
    """
    # Validate admin key
    admin_key_env = os.environ.get("CREDUENT_ADMIN_KEY")
    if not admin_key_env:
        raise HTTPException(
            status_code=500,
            detail="Admin key not configured on server (CREDUENT_ADMIN_KEY env var missing)."
        )
    admin_key_env = admin_key_env.strip()
    creduent_admin_key = (
        request.headers.get("CREDUENT_ADMIN_KEY")
        or request.headers.get("CREDUENT-ADMIN-KEY")
    )
    if not creduent_admin_key:
        raise HTTPException(status_code=403, detail="Forbidden: Missing CREDUENT_ADMIN_KEY header.")
    creduent_admin_key = creduent_admin_key.strip()
    if not secrets.compare_digest(
        creduent_admin_key.encode("utf-8"), admin_key_env.encode("utf-8")
    ):
        raise HTTPException(status_code=403, detail="Forbidden: Invalid CREDUENT_ADMIN_KEY header.")

    # Validate requested level
    VALID_LEVELS = {"unverified", "verified", "trusted"}
    level = req.level.lower().strip()
    if level not in VALID_LEVELS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid level '{req.level}'. Must be one of: {sorted(VALID_LEVELS)}"
        )

    # Normalize agent_id
    agent_id = req.agent_id
    if agent_id.startswith("agent:/") and not agent_id.startswith("agent://"):
        agent_id = "agent://" + agent_id[7:]

    # Fetch existing attestation to preserve public_key and domain
    existing = get_attestation(agent_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found in registry.")

    agent_data = {
        "agent_id": agent_id,
        "public_key": existing["public_key"],
        "domain": existing["domain"],
    }
    try:
        attestation = sign_attestation(agent_data, level=level)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signing failed: {str(e)}")
    try:
        save_attestation(agent_id, attestation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database write failed: {str(e)}")

    return {**attestation, "status": "upgraded"}

@router.post("/attest")
def attest(req: AttestRequest, request: Request):
    """Admin-only: directly create an attestation for an agent (bypasses DNS verification).
    Level is set to 'unverified'. Use POST /admin/attest to upgrade level after creation.
    """
    agent_id = req.agent_id
    if agent_id.startswith("agent:/") and not agent_id.startswith("agent://"):
        agent_id = "agent://" + agent_id[7:]

    admin_key_env = os.environ.get("CREDUENT_ADMIN_KEY")
    if not admin_key_env:
        raise HTTPException(status_code=500, detail="Admin attestation is not configured on server (CREDUENT_ADMIN_KEY env var missing).")
    admin_key_env = admin_key_env.strip()
    creduent_admin_key = request.headers.get("CREDUENT_ADMIN_KEY") or request.headers.get("CREDUENT-ADMIN-KEY")
    if not creduent_admin_key:
        raise HTTPException(status_code=403, detail="Forbidden: Missing CREDUENT_ADMIN_KEY header.")
    creduent_admin_key = creduent_admin_key.strip()
    if not secrets.compare_digest(creduent_admin_key.encode('utf-8'), admin_key_env.encode('utf-8')):
        raise HTTPException(status_code=403, detail="Forbidden: Invalid CREDUENT_ADMIN_KEY header.")

    agent_data = {
        "agent_id": agent_id,
        "public_key": req.public_key,
        "domain": req.domain
    }
    try:
        attestation = sign_attestation(agent_data, level="unverified")
    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Signing failed: {str(e)}")
    try:
        save_attestation(agent_id, attestation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database write failed: {str(e)}")
    return attestation

@router.get("/stats")
def get_stats():
    agents = list_agents()

    total = len(agents)
    verified = 0
    unverified = 0
    revoked = 0
    expiring_soon = 0

    now = datetime.now(timezone.utc)

    for agent in agents:
        level = agent.get("level", "verified").lower()
        if level == "verified" or level == "trusted":
            verified += 1
        elif level == "revoked":
            revoked += 1
        else:
            unverified += 1


        expires_at_str = agent.get("expires_at")
        if expires_at_str and level != "revoked":
            try:
                expires_at_normalized = expires_at_str.replace("Z", "+00:00")
                expires_at_dt = datetime.fromisoformat(expires_at_normalized)
                diff = expires_at_dt - now
                if 0 <= diff.days <= 30:
                    expiring_soon += 1
            except Exception:
                pass

    return {
        "total": total,
        "verified": verified,
        "unverified": unverified,
        "revoked": revoked,
        "expiring_soon": expiring_soon
    }

@router.get("/challenge/{agent_id:path}")
def get_challenge_endpoint(agent_id: str, request: Request):
    check_challenge_rate_limit(request)
    
    # Normalize agent_id
    if agent_id.startswith("agent:/") and not agent_id.startswith("agent://"):
        agent_id = "agent://" + agent_id[7:]
        
    # Check if the agent is registered
    attestation = get_attestation(agent_id)
    if not attestation:
        raise HTTPException(status_code=404, detail="Agent not registered")
        
    challenge_hex = secrets.token_hex(32)
    nonce_hex = secrets.token_hex(16)
    
    expires_dt = datetime.now(timezone.utc) + timedelta(minutes=5)
    expires_at = expires_dt.isoformat(timespec='seconds').replace("+00:00", "Z")
    
    challenge_obj = {
        "agent_id": agent_id,
        "challenge": challenge_hex,
        "nonce": nonce_hex,
        "expires_at": expires_at,
        "issuer": "agent://creduent/registry"
    }
    
    try:
        save_challenge(agent_id, nonce_hex, challenge_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store challenge: {e}")
        
    return challenge_obj

@router.post("/verify-challenge")
def verify_challenge(req: VerifyChallengeRequest, request: Request):
    import base64
    import hashlib
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.exceptions import InvalidSignature
    from registry.signer import get_registry_private_key
    from creduent.crypto import canonicalize
    import json

    # Normalize agent_id
    agent_id = req.agent_id
    if agent_id.startswith("agent:/") and not agent_id.startswith("agent://"):
        agent_id = "agent://" + agent_id[7:]
        
    # 1. Fetch challenge from Redis/Cache
    challenge_obj = get_challenge(agent_id, req.nonce)
    
    # 2. If not found or expired -> return 401 Unauthorized
    if not challenge_obj:
        raise HTTPException(status_code=401, detail="Challenge not found or expired")
        
    # Check manual expiration (safety fallback)
    expires_at_str = challenge_obj.get("expires_at")
    if expires_at_str:
        try:
            expires_at = datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
            if datetime.now(timezone.utc) > expires_at:
                delete_challenge(agent_id, req.nonce)
                raise HTTPException(status_code=401, detail="Challenge expired")
        except Exception:
            pass
            
    # 3. Fetch agent attestation from registry
    attestation = get_attestation(agent_id)
    if not attestation:
        raise HTTPException(status_code=404, detail="Agent not registered")
        
    # 4. Verify Ed25519 signature using agent's public_key
    pk_str = attestation.get("public_key", "")
    if not pk_str.startswith("ed25519:"):
        raise HTTPException(status_code=400, detail="Unsupported agent public key format")
        
    try:
        pk_b64 = pk_str.split(":", 1)[1]
        public_key_bytes = base64.b64decode(pk_b64)
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
        
        signature_bytes = base64.b64decode(req.signature)
        
        # Message to verify: SHA256(challenge + nonce) as bytes
        challenge_val = challenge_obj.get("challenge", "")
        message_str = challenge_val + req.nonce
        hashed_bytes = hashlib.sha256(message_str.encode('utf-8')).digest()
        
        public_key.verify(signature_bytes, hashed_bytes)
    except InvalidSignature:
        raise HTTPException(status_code=401, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Signature verification failed: {str(e)}")
        
    # 5. Delete challenge from Redis (one-time use)
    delete_challenge(agent_id, req.nonce)
    
    # 6. Generate proof token signed by registry private key
    valid_until_dt = datetime.now(timezone.utc) + timedelta(hours=1)
    valid_until = valid_until_dt.isoformat(timespec='seconds').replace("+00:00", "Z")
    
    level = attestation.get("level", "unverified")
    
    proof_payload = {
        "agent_id": agent_id,
        "verified": True,
        "level": level,
        "valid_until": valid_until
    }
    
    registry_private_key = get_registry_private_key()
    if not registry_private_key:
        raise HTTPException(status_code=500, detail="Registry private key not configured")
        
    try:
        canonical_str = canonicalize(proof_payload)
        canonical_bytes = canonical_str.encode('utf-8')
        sig_bytes = registry_private_key.sign(canonical_bytes)
        sig_b64 = base64.b64encode(sig_bytes).decode('utf-8')
        
        proof_obj = {
            **proof_payload,
            "signature": sig_b64
        }
        
        proof_token_str = base64.b64encode(json.dumps(proof_obj).encode('utf-8')).decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate proof token: {str(e)}")
        
    return {
        "agent_id": agent_id,
        "verified": True,
        "level": level,
        "proof_token": proof_token_str,
        "valid_until": valid_until,
        "issuer": "agent://creduent/registry"
    }

@router.get("/public-key")
def get_public_key():
    import base64
    from cryptography.hazmat.primitives import serialization
    from registry.signer import get_registry_public_key

    pubkey = get_registry_public_key()
    if not pubkey:
        raise HTTPException(status_code=500, detail="Registry public key not configured")
    pub_bytes = pubkey.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    pub_b64 = base64.b64encode(pub_bytes).decode('utf-8')
    return {"public_key": f"ed25519:{pub_b64}"}

app.include_router(router)
app.include_router(router, prefix="/registry")

@app.get("/resolver", response_class=HTMLResponse)
@app.get("/resolver/", response_class=HTMLResponse)
def serve_resolver_ui():
    return HTMLResponse(content=RESOLVER_HTML, status_code=200)

@app.get("/agent:/{agent_id:path}")
@app.get("/agent://{agent_id:path}")
def resolve_agent_directly(agent_id: str, request: Request):
    return get_attest("agent://" + agent_id, request)

@app.get("/registry")
@app.get("/registry/")
def serve_registry_landing():
    return {
        "protocol": "Creduent",
        "version": "1.0",
        "status": "operational",
        "endpoints": {
            "register": "https://api.idevsec.com/registry/register",
            "attest": "https://api.idevsec.com/registry/attest/{agent_id}",
            "revoke": "https://api.idevsec.com/registry/revoke"
        }
    }

@app.get("/dashboard", response_class=HTMLResponse)
@app.get("/dashboard/", response_class=HTMLResponse)
@app.get("/registry/dashboard", response_class=HTMLResponse)
@app.get("/registry/dashboard/", response_class=HTMLResponse)
def serve_dashboard_ui():
    return HTMLResponse(content=DASHBOARD_HTML, status_code=200)

@app.get("/{uri_path:path}")
def catch_all_uri_resolver(uri_path: str, request: Request):
    import urllib.parse
    decoded = urllib.parse.unquote(uri_path)
    # Check if this looks like an agent URI or starts with agent:
    if decoded.startswith("agent:/") or decoded.startswith("agent://") or decoded.startswith("agent:"):
        # Normalize agent:/ to agent://
        if decoded.startswith("agent:/") and not decoded.startswith("agent://"):
            decoded = "agent://" + decoded[7:]
        elif decoded.startswith("agent:") and not decoded.startswith("agent://") and not decoded.startswith("agent:/"):
            decoded = "agent://" + decoded[6:]
        return get_attest(decoded, request)
    raise HTTPException(status_code=404, detail="Not Found")