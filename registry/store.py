import os
import time
import json
import contextlib
import sys
import traceback

# Add parent directory to path to allow importing from creduent package
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)
from creduent.utils import load_dotenv

# Load local environment variables if present
load_dotenv()

DB_PATH = "registry_db.json"


@contextlib.contextmanager
def file_lock(file_path):
    lock_path = file_path + ".lock"
    # Try opening the lock file
    f = open(lock_path, "w")
    try:
        # Cross-platform file locking:
        # On Windows: msvcrt.locking
        # On Unix: fcntl.flock
        if os.name == "nt":
            import msvcrt

            locked = False
            for _ in range(50):  # Retry for 5 seconds (50 * 0.1s)
                try:
                    f.seek(0)
                    msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                    locked = True
                    break
                except (OSError, IOError):
                    time.sleep(0.1)
            if not locked:
                raise IOError("Could not acquire registry file lock on Windows")
        else:
            import fcntl

            locked = False
            for _ in range(50):  # Retry for 5 seconds
                try:
                    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    locked = True
                    break
                except (OSError, IOError):
                    time.sleep(0.1)
            if not locked:
                raise IOError("Could not acquire registry file lock on Unix")

        yield f
    finally:
        try:
            if os.name == "nt":
                import msvcrt

                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(f, fcntl.LOCK_UN)
        except Exception:
            pass
        f.close()
        try:
            os.remove(lock_path)
        except Exception:
            pass


def is_redis_configured() -> bool:
    url = os.environ.get("UPSTASH_REDIS_REST_URL")
    token = os.environ.get("UPSTASH_REDIS_REST_TOKEN")
    if not url or not token:
        return False
    if "YOUR_" in url or "YOUR_" in token:
        return False
    return True


def diagnose_redis():
    """Logs Redis environment variable status to stderr for debugging."""
    url = os.environ.get("UPSTASH_REDIS_REST_URL", "")
    token = os.environ.get("UPSTASH_REDIS_REST_TOKEN", "")
    url_preview = (url[:30] + "...") if len(url) > 30 else url
    token_set = bool(token and len(token) > 10)
    print(
        f"[REDIS DIAG] URL set={bool(url)} url_preview={url_preview!r} "
        f"token_set={token_set} VERCEL={os.environ.get('VERCEL')}",
        file=sys.stderr,
    )


_redis_client_cache = None


def get_redis_client():
    global _redis_client_cache
    if _redis_client_cache is None:
        url = os.environ.get("UPSTASH_REDIS_REST_URL")
        token = os.environ.get("UPSTASH_REDIS_REST_TOKEN")
        from upstash_redis import Redis  # type: ignore

        _redis_client_cache = Redis(url=url, token=token)
    return _redis_client_cache


def save_attestation(agent_id: str, attestation_obj: dict):
    """
    Saves or updates an agent attestation in Vercel KV (Upstash Redis) or falls back to local file.
    """
    if is_redis_configured():
        try:
            client = get_redis_client()
            client.hset("creduent:agents", agent_id, json.dumps(attestation_obj))
        except Exception as e:
            print(f"[-] Redis error in save_attestation: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            raise
    else:
        with file_lock(DB_PATH):
            db = {}
            if os.path.exists(DB_PATH):
                with open(DB_PATH, "r", encoding="utf-8") as f:
                    try:
                        db = json.load(f)
                    except Exception:
                        db = {}
            db[agent_id] = attestation_obj
            with open(DB_PATH, "w", encoding="utf-8") as f:
                json.dump(db, f, indent=2, ensure_ascii=False)


def get_attestation(agent_id: str) -> dict:
    """
    Retrieves the attestation object for a given agent_id.
    """
    if is_redis_configured():
        try:
            client = get_redis_client()
            val = client.hget("creduent:agents", agent_id)
            if val:  # Truthy check: handles empty string "" or None
                if isinstance(val, dict):
                    return val
                try:
                    return json.loads(val)
                except Exception:
                    return val
        except Exception as e:
            print(f"[-] Redis storage error in get_attestation: {e}", file=sys.stderr)
        return None
    else:
        with file_lock(DB_PATH):
            if not os.path.exists(DB_PATH):
                return None
            with open(DB_PATH, "r", encoding="utf-8") as f:
                try:
                    db = json.load(f)
                    val = db.get(agent_id)
                    return val if val else None
                except Exception:
                    return None


def revoke_agent(agent_id: str):
    """
    Revokes (removes) an agent's attestation.
    """
    if is_redis_configured():
        try:
            client = get_redis_client()
            client.hdel("creduent:agents", agent_id)
        except Exception as e:
            print(f"[-] Redis error in revoke_agent: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            raise
    else:
        with file_lock(DB_PATH):
            if not os.path.exists(DB_PATH):
                return
            with open(DB_PATH, "r", encoding="utf-8") as f:
                try:
                    db = json.load(f)
                except Exception:
                    return
            if agent_id in db:
                del db[agent_id]
                with open(DB_PATH, "w", encoding="utf-8") as f:
                    json.dump(db, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Webhook storage — Redis hash "creduent:webhooks" or local webhooks_db.json
# ---------------------------------------------------------------------------

WEBHOOKS_DB_PATH = os.path.join(BASE_DIR, "registry", "webhooks_db.json")


def _derive_webhook_secret(agent_id: str) -> str:
    import hashlib
    salt = os.environ.get("CREDUENT_WEBHOOK_SALT", "default_creduent_salt_2026")
    h = hashlib.sha256(f"{agent_id}|{salt}".encode("utf-8"))
    return f"whsec_legacy_{h.hexdigest()[:32]}"


def save_webhook(agent_id: str, webhook_url: str) -> str:
    """Persist an agent -> webhook configuration mapping. Returns the webhook secret."""
    import secrets
    secret = f"whsec_{secrets.token_hex(24)}"
    config = {
        "url": webhook_url,
        "secret": secret
    }
    val = json.dumps(config)

    if is_redis_configured():
        try:
            client = get_redis_client()
            client.hset("creduent:webhooks", agent_id, val)
        except Exception as e:
            print(f"[-] Redis error in save_webhook: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            raise
    else:
        # Local-dev fallback: read-modify-write with file lock
        os.makedirs(os.path.dirname(WEBHOOKS_DB_PATH), exist_ok=True)
        if not os.path.exists(WEBHOOKS_DB_PATH):
            with open(WEBHOOKS_DB_PATH, "w", encoding="utf-8") as f:
                f.write("{}")
        with file_lock(WEBHOOKS_DB_PATH):
            with open(WEBHOOKS_DB_PATH, "r", encoding="utf-8") as f:
                try:
                    db = json.load(f)
                except Exception:
                    db = {}
            db[agent_id] = val
            with open(WEBHOOKS_DB_PATH, "w", encoding="utf-8") as f:
                json.dump(db, f, indent=2, ensure_ascii=False)
    return secret


def get_webhook_config(agent_id: str) -> dict:
    """Return the webhook configuration dict {"url": url, "secret": secret} or None."""
    val = None
    if is_redis_configured():
        try:
            client = get_redis_client()
            val = client.hget("creduent:webhooks", agent_id)
            if isinstance(val, bytes):
                val = val.decode("utf-8")
        except Exception as e:
            print(f"[-] Redis error in get_webhook_config: {e}", file=sys.stderr)
            return None
    else:
        if not os.path.exists(WEBHOOKS_DB_PATH):
            return None
        with file_lock(WEBHOOKS_DB_PATH):
            with open(WEBHOOKS_DB_PATH, "r", encoding="utf-8") as f:
                try:
                    db = json.load(f)
                    val = db.get(agent_id)
                except Exception:
                    return None

    if not val:
        return None

    # Attempt to parse as JSON config. If it fails, it's a legacy URL string.
    if isinstance(val, str):
        val = val.strip()
        if val.startswith("{") and val.endswith("}"):
            try:
                data = json.loads(val)
                if isinstance(data, dict) and "url" in data:
                    if "secret" not in data:
                        data["secret"] = _derive_webhook_secret(agent_id)
                    return data
            except Exception:
                pass
        
        # Legacy fallback
        return {
            "url": val,
            "secret": _derive_webhook_secret(agent_id)
        }
    elif isinstance(val, dict) and "url" in val:
        if "secret" not in val:
            val["secret"] = _derive_webhook_secret(agent_id)
        return val

    return None


def get_webhook(agent_id: str):
    """Return the webhook URL for an agent, or None (for backwards compatibility)."""
    cfg = get_webhook_config(agent_id)
    return cfg["url"] if cfg else None


def list_webhooks_configs() -> dict:
    """Return the full {agent_id: {"url": url, "secret": secret}} mapping."""
    raw_webhooks = {}
    if is_redis_configured():
        try:
            client = get_redis_client()
            raw = client.hgetall("creduent:webhooks")
            if raw:
                for k, v in raw.items():
                    key = k.decode("utf-8") if isinstance(k, bytes) else k
                    val = v.decode("utf-8") if isinstance(v, bytes) else v
                    raw_webhooks[key] = val
        except Exception as e:
            print(f"[-] Redis error in list_webhooks_configs: {e}", file=sys.stderr)
            return {}
    else:
        if not os.path.exists(WEBHOOKS_DB_PATH):
            return {}
        with file_lock(WEBHOOKS_DB_PATH):
            with open(WEBHOOKS_DB_PATH, "r", encoding="utf-8") as f:
                try:
                    raw_webhooks = json.load(f)
                except Exception:
                    return {}

    result = {}
    for agent_id, val in raw_webhooks.items():
        if isinstance(val, str):
            val = val.strip()
            if val.startswith("{") and val.endswith("}"):
                try:
                    data = json.loads(val)
                    if isinstance(data, dict) and "url" in data:
                        if "secret" not in data:
                            data["secret"] = _derive_webhook_secret(agent_id)
                        result[agent_id] = data
                        continue
                except Exception:
                    pass
            # Legacy fallback
            result[agent_id] = {
                "url": val,
                "secret": _derive_webhook_secret(agent_id)
            }
        elif isinstance(val, dict) and "url" in val:
            if "secret" not in val:
                val["secret"] = _derive_webhook_secret(agent_id)
            result[agent_id] = val
    return result


def list_webhooks() -> dict:
    """Return the full {agent_id: webhook_url} mapping (for backwards compatibility)."""
    configs = list_webhooks_configs()
    return {agent_id: cfg["url"] for agent_id, cfg in configs.items()}


def delete_webhook(agent_id: str):
    """Remove a webhook registration."""
    if is_redis_configured():
        try:
            client = get_redis_client()
            client.hdel("creduent:webhooks", agent_id)
        except Exception as e:
            print(f"[-] Redis error in delete_webhook: {e}", file=sys.stderr)
    else:
        if not os.path.exists(WEBHOOKS_DB_PATH):
            return
        with file_lock(WEBHOOKS_DB_PATH):
            with open(WEBHOOKS_DB_PATH, "r", encoding="utf-8") as f:
                try:
                    db = json.load(f)
                except Exception:
                    return
            if agent_id in db:
                del db[agent_id]
                with open(WEBHOOKS_DB_PATH, "w", encoding="utf-8") as f:
                    json.dump(db, f, indent=2, ensure_ascii=False)


def list_agents() -> list:
    """
    Lists all registered agents and their attestations.
    """
    if is_redis_configured():
        try:
            client = get_redis_client()
            vals = client.hvals("creduent:agents")
            agents = []
            for val in vals:
                if not val:  # Skip falsy/empty values
                    continue
                if isinstance(val, dict):
                    agents.append(val)
                else:
                    try:
                        parsed = json.loads(val)
                        if parsed:
                            agents.append(parsed)
                    except Exception:
                        agents.append(val)
            return agents
        except Exception as e:
            print(f"[-] Redis storage error in list_agents: {e}", file=sys.stderr)
            return []
    else:
        with file_lock(DB_PATH):
            if not os.path.exists(DB_PATH):
                return []
            with open(DB_PATH, "r", encoding="utf-8") as f:
                try:
                    db = json.load(f)
                    return [v for v in db.values() if v]
                except Exception:
                    return []


CHALLENGE_DB = {}


def _prune_expired_challenges():
    """Removes expired challenges from the in-memory CHALLENGE_DB fallback to prevent memory leaks."""
    now = time.time()
    expired = [k for k, (_, expiry) in CHALLENGE_DB.items() if now >= expiry]
    for k in expired:
        CHALLENGE_DB.pop(k, None)


def save_challenge(agent_id: str, nonce: str, challenge_obj: dict):
    """
    Saves a generated challenge object with a 5-minute TTL.
    """
    key = f"challenge:{agent_id}:{nonce}"
    if is_redis_configured():
        try:
            client = get_redis_client()
            client.set(key, json.dumps(challenge_obj), ex=300)
            return
        except Exception as e:
            print(f"[-] Redis error in save_challenge: {e}", file=sys.stderr)

    # Fallback to local memory
    _prune_expired_challenges()
    CHALLENGE_DB[key] = (challenge_obj, time.time() + 300)


def get_challenge(agent_id: str, nonce: str) -> dict:
    """
    Retrieves the challenge object if it exists and has not expired.
    """
    key = f"challenge:{agent_id}:{nonce}"
    if is_redis_configured():
        try:
            client = get_redis_client()
            val = client.get(key)
            if val:
                try:
                    return json.loads(val)
                except Exception:
                    return val
            return None
        except Exception as e:
            print(f"[-] Redis error in get_challenge: {e}", file=sys.stderr)

    # Fallback to local memory
    _prune_expired_challenges()
    if key in CHALLENGE_DB:
        val, expiry = CHALLENGE_DB[key]
        if time.time() < expiry:
            return val
        else:
            del CHALLENGE_DB[key]
    return None


def delete_challenge(agent_id: str, nonce: str):
    """
    Deletes the challenge object to ensure one-time use.
    """
    key = f"challenge:{agent_id}:{nonce}"
    if is_redis_configured():
        try:
            client = get_redis_client()
            client.delete(key)
            return
        except Exception as e:
            print(f"[-] Redis error in delete_challenge: {e}", file=sys.stderr)

    # Fallback to local memory
    _prune_expired_challenges()
    if key in CHALLENGE_DB:
        del CHALLENGE_DB[key]
