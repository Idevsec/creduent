# CREDUENT-008: Identity-Based Rate Limiting (IBRL) Specification

**Status:** Draft  
**Version:** 0.1  
**Author:** IDevSec  
**Date:** 2026-09-10  
**Related:** [CREDUENT-001](CREDUENT-001-agent-json.md), [CREDUENT-002](CREDUENT-002-attestation.md), [CREDUENT-003](CREDUENT-003-registry-api.md)

---

## 1. Overview & Threat Model

Traditional IP-based rate limiting fails when defending against autonomous LLM agent swarms. A distributed agent cluster can rotate thousands of ephemeral IP addresses or proxy endpoints while maintaining execution state for a single target agent identity (`agent_id`).

**CREDUENT-008** defines **Identity-Based Rate Limiting (IBRL)**, shifting request throttling from transient network identifiers (IP addresses) to cryptographically verified agent identities. Incoming requests are authenticated via Creduent signatures (`X-Creduent-Signature` or `Authorization: Bearer <token>`). Once validated, rate limits apply directly to the verified `agent_id` or `did:creduent` URI.

---

## 2. Identity Trust Tiers

Requests processed by an IBRL-compliant middleware MUST be categorized into four distinct trust tiers:

| Tier | Condition | Default Limit | Window |
| :--- | :--- | :--- | :--- |
| **Tier 0: Anonymous / IP Fallback** | Unsigned request or missing identity header | 10 req | 60 sec |
| **Tier 1: Unverified Agent** | Identity header present, but signature unverified | 30 req | 60 sec |
| **Tier 2: Verified Agent** | Valid signature matching registered `agent_id` | 600 req | 60 sec |
| **Tier 3: Trusted / Attested Agent** | Valid signature with active registry attestation | 3,000 req | 60 sec |

---

## 3. Standardized HTTP Headers

### 3.1 Downstream Response Headers
Every HTTP response processed by IBRL middleware MUST include standardized rate limit headers:

```http
X-Creduent-Agent-ID: agent://idevsec/steward
X-RateLimit-Limit: 600
X-RateLimit-Remaining: 598
X-RateLimit-Reset: 1757454600
X-RateLimit-Tier: verified
```

### 3.2 Throttled Response (`HTTP 429`)
When an agent exceeds its quota, the service MUST respond with `HTTP 429 Too Many Requests`:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 42
X-RateLimit-Limit: 600
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1757454642

{
  "error": "rate_limit_exceeded",
  "message": "Rate limit exceeded for agent_id agent://idevsec/steward. Retry after 42 seconds.",
  "agent_id": "agent://idevsec/steward",
  "retry_after": 42
}
```

---

## 4. Sliding Window Algorithm & Storage

IBRL specifies a sliding window log algorithm for sub-millisecond rate enforcement.

### 4.1 Redis Data Schema
- **Key Format**: `ibrl:log:<agent_id_hash>`
- **Data Structure**: Sorted Set (ZSET)
- **Score**: Unix timestamp in milliseconds (`now_ms`)
- **Member**: Unique request identifier (`<now_ms>:<uuid_short>`)

### 4.2 Sliding Window Execution Logic:
1. Remove elements with score older than `now_ms - window_ms`.
2. Count remaining members in the sorted set.
3. If count exceeds `limit`, deny request with `HTTP 429`.
4. If count is within `limit`, add new request member and set TTL to `window_seconds`.

### 4.3 In-Memory Storage Fallback
If Redis storage is unavailable, IBRL implementations MUST gracefully fall back to an in-memory sliding window log using thread-safe per-agent timestamp arrays.

---

## 5. Middleware Conformance Requirements

An implementation claiming conformance with CREDUENT-008 MUST satisfy the following requirements:

- [ ] **IBRL-M01:** MUST extract `X-Creduent-Agent-ID` and verify cryptographic signatures before evaluating identity tiers.
- [ ] **IBRL-M02:** MUST fall back to IP-based rate limits (`Tier 0`) when identity headers or signatures are absent.
- [ ] **IBRL-M03:** MUST return `HTTP 429 Too Many Requests` with a valid `Retry-After` header when rate limits are exceeded.
- [ ] **IBRL-M04:** MUST include `X-Creduent-Agent-ID`, `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, and `X-RateLimit-Tier` on all HTTP responses.
- [ ] **IBRL-M05:** MUST use sliding-window time tracking to prevent burst boundary spikes.
