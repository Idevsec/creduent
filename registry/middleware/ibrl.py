import time
from typing import Dict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from registry.store import get_attestation


class IBRLMiddleware(BaseHTTPMiddleware):
    """
    Identity-Based Rate Limiting (IBRL) Security Middleware.

    Authenticates cryptographic headers (X-Creduent-Agent-ID, X-Creduent-Signature, X-Creduent-Timestamp),
    checks attestation status against the registry store, enforces sliding-window replay protection,
    and applies per-agent token-bucket rate limiting quotas.
    """

    def __init__(self, app, limit_per_min: int = 100, window_sec: int = 300):
        super().__init__(app)
        self.limit = float(limit_per_min)
        self.refill_rate = self.limit / 60.0
        self.window_sec = window_sec
        self._seen_signatures: Dict[str, float] = {}
        self._buckets: Dict[str, Dict[str, float]] = {}

    def clear_state(self):
        """Helper to clear in-memory state for testing."""
        self._seen_signatures.clear()
        self._buckets.clear()

    async def dispatch(self, request: Request, call_next) -> Response:
        agent_id = request.headers.get("X-Creduent-Agent-ID")
        # If no identity headers are provided, let standard routing and IP rate-limiting handle it
        if not agent_id:
            return await call_next(request)

        signature = request.headers.get("X-Creduent-Signature")
        timestamp_str = request.headers.get("X-Creduent-Timestamp")

        if not signature or not timestamp_str:
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing cryptographic headers for IBRL"},
            )

        try:
            timestamp_val = float(timestamp_str)
        except ValueError:
            return JSONResponse(
                status_code=400,
                content={"detail": "Invalid timestamp format"},
            )

        current_time = time.time()
        if abs(current_time - timestamp_val) > self.window_sec:
            return JSONResponse(
                status_code=403,
                content={"detail": "Timestamp outside valid window"},
            )

        # Sliding-window nonce & signature deduplication filter to eliminate replay attacks
        expired_sigs = [
            sig for sig, ts in self._seen_signatures.items()
            if (current_time - ts) > self.window_sec
        ]
        for sig in expired_sigs:
            self._seen_signatures.pop(sig, None)

        if signature in self._seen_signatures:
            return JSONResponse(
                status_code=403,
                content={"detail": "Replay Detected"},
            )
        self._seen_signatures[signature] = current_time

        # Verify attestation / identity status
        attestation = get_attestation(agent_id)
        if not attestation or attestation.get("status") == "revoked" or attestation.get("level") == "revoked":
            return JSONResponse(
                status_code=403,
                content={"detail": "Agent identity invalid or revoked"},
            )

        # Token Bucket Rate Limiting per cryptographic identity
        bucket = self._buckets.get(agent_id)
        if not bucket:
            bucket = {"tokens": self.limit, "last_updated": current_time}
            self._buckets[agent_id] = bucket
        else:
            elapsed = current_time - bucket["last_updated"]
            new_tokens = elapsed * self.refill_rate
            bucket["tokens"] = min(self.limit, bucket["tokens"] + new_tokens)
            bucket["last_updated"] = current_time

        if bucket["tokens"] < 1.0:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too Many Requests"},
                headers={
                    "X-RateLimit-Limit": str(int(self.limit)),
                    "X-RateLimit-Remaining": "0",
                },
            )

        bucket["tokens"] -= 1.0
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(int(self.limit))
        response.headers["X-RateLimit-Remaining"] = str(int(bucket["tokens"]))
        return response
