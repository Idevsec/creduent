import os
import time
import json
import contextlib
import sys

# Add parent directory to path to allow importing from creduent package
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
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
        if os.name == 'nt':
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
            if os.name == 'nt':
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

def get_redis_client():
    url = os.environ.get("UPSTASH_REDIS_REST_URL")
    token = os.environ.get("UPSTASH_REDIS_REST_TOKEN")
    from upstash_redis import Redis  # type: ignore
    return Redis(url=url, token=token)

def save_attestation(agent_id: str, attestation_obj: dict):
    """
    Saves or updates an agent attestation in Vercel KV (Upstash Redis) or falls back to local file.
    """
    if is_redis_configured():
        client = get_redis_client()
        client.hset("creduent:agents", agent_id, json.dumps(attestation_obj))
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
        client = get_redis_client()
        client.hdel("creduent:agents", agent_id)
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

