import os
import sys
import json
import logging
import urllib.request
import urllib.error
from datetime import datetime, timezone

# Resolve paths relative to the script location for robustness
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

REGISTRY_DB_PATH = os.path.join(BASE_DIR, "registry_db.json")
WEBHOOKS_DB_PATH = os.path.join(BASE_DIR, "registry", "webhooks_db.json")


# Set up logging to stdout instead of daemon.log
class CustomStdoutLogger:
    def info(self, msg):
        print(f"{datetime.now().isoformat()} [INFO] {msg}", file=sys.stdout)

    def warning(self, msg):
        print(f"{datetime.now().isoformat()} [WARNING] {msg}", file=sys.stdout)

    def error(self, msg):
        print(f"{datetime.now().isoformat()} [ERROR] {msg}", file=sys.stdout)


logging = CustomStdoutLogger()


# ---------------------------------------------------------------------------
# Storage helpers — Redis-first, local JSON fallback
# ---------------------------------------------------------------------------


def _is_redis_configured() -> bool:
    url = os.environ.get("UPSTASH_REDIS_REST_URL", "")
    token = os.environ.get("UPSTASH_REDIS_REST_TOKEN", "")
    return bool(url and token and "YOUR_" not in url and "YOUR_" not in token)


def _get_redis_client():
    from upstash_redis import Redis  # type: ignore

    return Redis(
        url=os.environ["UPSTASH_REDIS_REST_URL"],
        token=os.environ["UPSTASH_REDIS_REST_TOKEN"],
    )


def load_registry() -> dict:
    """Return {agent_id: record} from Redis or local JSON."""
    if _is_redis_configured():
        try:
            client = _get_redis_client()
            raw = client.hgetall("creduent:agents")
            if not raw:
                return {}
            result = {}
            for k, v in raw.items():
                key = k.decode("utf-8") if isinstance(k, bytes) else k
                val = v.decode("utf-8") if isinstance(v, bytes) else v
                try:
                    result[key] = json.loads(val) if isinstance(val, str) else val
                except Exception:
                    result[key] = val
            return result
        except Exception as e:
            logging.error(f"Redis error loading registry: {e}")
            return {}
    else:
        return _load_json_file(REGISTRY_DB_PATH)


def load_webhooks() -> dict:
    """Return {agent_id: webhook_url} from Redis or local JSON."""
    if _is_redis_configured():
        try:
            client = _get_redis_client()
            raw = client.hgetall("creduent:webhooks")
            if not raw:
                return {}
            result = {}
            for k, v in raw.items():
                key = k.decode("utf-8") if isinstance(k, bytes) else k
                val = v.decode("utf-8") if isinstance(v, bytes) else v
                result[key] = val
            return result
        except Exception as e:
            logging.error(f"Redis error loading webhooks: {e}")
            return {}
    else:
        return _load_json_file(WEBHOOKS_DB_PATH)


def _load_json_file(file_path: str) -> dict:
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load JSON file at {file_path}: {e}")
        return {}


# ---------------------------------------------------------------------------
# Webhook fire
# ---------------------------------------------------------------------------


def send_webhook(agent_id, webhook_url, domain, expires_at, days_remaining):
    action_url = (
        f"https://{domain}/renew" if domain else "https://creduent.idevsec.com/renew"
    )

    payload = {
        "event": "agent.expiry_warning",
        "agent_id": agent_id,
        "domain": domain or "creduent.idevsec.com",
        "expires_at": expires_at,
        "days_remaining": days_remaining,
        "action_url": action_url,
    }

    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.getcode()
            logging.info(f"Webhook fired for '{agent_id}' → {webhook_url} [{status}]")
            return True
    except urllib.error.HTTPError as e:
        logging.error(
            f"HTTP error for '{agent_id}' → {webhook_url}: {e.code} {e.reason}"
        )
    except urllib.error.URLError as e:
        logging.error(f"Network error for '{agent_id}' → {webhook_url}: {e.reason}")
    except Exception as e:
        logging.error(f"Unexpected error for '{agent_id}' → {webhook_url}: {e}")
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    # Load local .env when not running inside Vercel
    if os.environ.get("VERCEL") != "1":
        try:
            from creduent.utils import load_dotenv

            load_dotenv()
        except Exception:
            pass

    logging.info("--- Creduent Registry Renewal Daemon started ---")
    storage = "Redis" if _is_redis_configured() else "local JSON"
    logging.info(f"Storage backend: {storage}")

    registry = load_registry()
    webhooks = load_webhooks()

    if not registry:
        logging.info("No agent records found in registry database.")
        logging.info("--- Daemon execution finished successfully (idle) ---")
        return

    now = datetime.now(timezone.utc)
    expiring_count = 0
    webhook_sent_count = 0

    for agent_id, record in registry.items():
        if record.get("level") == "revoked":
            logging.info(f"Skipping agent '{agent_id}' (REVOKED status).")
            continue

        expires_at_str = record.get("expires_at")
        if not expires_at_str:
            logging.warning(f"Agent '{agent_id}' missing 'expires_at'. Skipping.")
            continue

        try:
            expires_at_dt = datetime.fromisoformat(
                expires_at_str.replace("Z", "+00:00")
            )
        except Exception as e:
            logging.error(f"Bad 'expires_at' for '{agent_id}': {e}")
            continue

        diff = expires_at_dt - now
        days_remaining = diff.days

        if 0 <= days_remaining <= 30:
            expiring_count += 1
            logging.warning(
                f"Agent '{agent_id}' expires in {days_remaining} days ({expires_at_str})"
            )

            webhook_url = webhooks.get(agent_id)
            if webhook_url:
                logging.info(f"Firing warning webhook for '{agent_id}' → {webhook_url}")
                if send_webhook(
                    agent_id,
                    webhook_url,
                    record.get("domain"),
                    expires_at_str,
                    days_remaining,
                ):
                    webhook_sent_count += 1
            else:
                logging.info(f"No webhook for expiring agent '{agent_id}'.")
        elif days_remaining < 0:
            logging.warning(
                f"Agent '{agent_id}' already EXPIRED {abs(days_remaining)} days ago."
            )
        else:
            logging.info(f"Agent '{agent_id}' active, {days_remaining} days remaining.")

    logging.info(
        f"Scan complete. Expiring: {expiring_count}, Webhooks sent: {webhook_sent_count}"
    )
    logging.info("--- Daemon execution finished successfully ---")


if __name__ == "__main__":
    main()
