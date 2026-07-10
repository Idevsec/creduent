# CREDUENT-003: Registry API Specification

**Status:** Active  
**Version:** 0.4  
**Author:** IDevSec  
**Date:** 2026-05-31  
**Related:** [CREDUENT-001](../SPEC.md), [CREDUENT-002](CREDUENT-002-attestation.md)

---

## 1. Introduction

This document specifies the HTTP API exposed by a Creduent-compatible registry. It defines:
- All endpoints, request schemas, and response schemas.
- Authentication model.
- Error format.
- Rate limiting expectations.

Any registry implementation that exposes this API surface is considered a Creduent-compatible registry.

Base URL for the reference implementation: `https://creduent.idevsec.com`

---

## 2. Common Response Format

All API responses use JSON (`Content-Type: application/json`).

### 2.1 Error Response

```json
{
  "error": "human-readable error message",
  "code": "MACHINE_READABLE_CODE"
}
```

### 2.2 Standard HTTP Status Codes

| Code | Meaning |
|:---|:---|
| 200 | Success |
| 201 | Created (registration or attestation issued) |
| 400 | Bad Request (malformed payload or validation failure) |
| 401 | Unauthorized (admin key missing or wrong) |
| 404 | Not Found (agent not registered) |
| 409 | Conflict (agent already registered) |
| 429 | Too Many Requests (rate limited) |
| 500 | Internal Server Error |

---

## 3. Endpoints

### 3.1 POST /register

Register an agent and obtain a `verified` attestation.

**Request:**
```json
{
  "agent_id": "agent://example/mybot",
  "domain": "example.com",
  "agent_json_url": "https://example.com/.well-known/agent.json"
}
```

**Validation steps performed:**
1. SSRF check on `agent_json_url`.
2. Fetch and schema-validate `agent.json`.
3. Ed25519 signature verification.
4. DNS TXT record check: `_creduent.{domain}` must equal `agent_id`.
5. Endpoint healthcheck.

**Success Response (201):**
```json
{
  "success": true,
  "agent_id": "agent://example/mybot",
  "attestation": { ... }
}
```

**Error Responses:**

| Code | Reason |
|:---|:---|
| 400 | Missing fields, invalid agent.json, signature invalid |
| 400 | DNS TXT record not found or mismatch |
| 400 | Endpoint healthcheck failed |
| 409 | Agent already registered |

---

### 3.2 POST /attest

Direct registration without DNS or endpoint verification. Results in `level: "unverified"`.

**Request:**
```json
{
  "agent_id": "agent://example/mybot",
  "domain": "example.com",
  "public_key": "ed25519:hArTvbITJ2jirL170IOSjcVvEvstC4s+RjYLu4chCwg="
}
```

**Success Response (201):** Returns attestation object with `level: "unverified"`.

---

### 3.3 GET /attest/{agent_id}

Retrieve the active attestation for an agent.

**Path Parameter:** `agent_id` is the URI-encoded `agent://namespace/name` string.

**Success Response (200):**
```json
{
  "agent_id": "agent://example/mybot",
  "issuer": "agent://creduent/registry",
  "level": "verified",
  "issued_at": "2026-05-30T00:00:00Z",
  "expires_at": "2026-06-29T00:00:00Z",
  "public_key": "ed25519:hArTvbITJ2jirL170IOSjcVvEvstC4s+RjYLu4chCwg=",
  "domain": "example.com",
  "signature": "..."
}
```

**Error Responses:**

| Code | Reason |
|:---|:---|
| 404 | Agent not registered |

---

### 3.4 GET /agents

List all registered agents.

**Query Parameters:**

| Parameter | Type | Description |
|:---|:---|:---|
| `limit` | integer | Max results (default 100, max 500). |
| `offset` | integer | Pagination offset (default 0). |
| `level` | string | Filter by attestation level: `unverified`, `verified`, `trusted`, `revoked`. |
| `capability` | string | Filter agents by declared capability tag. |

**Success Response (200):**
```json
{
  "total": 42,
  "agents": [
    { "agent_id": "...", "domain": "...", "level": "verified", "expires_at": "..." }
  ]
}
```

---

### 3.5 DELETE /revoke/{agent_id}

Revoke an agent's attestation.

**Required Headers (Multisig Quorum):**
- `CREDUENT-ADMIN-KEYS`: Comma-separated list of administrative public keys
- `CREDUENT-ADMIN-SIGNATURES`: Comma-separated list of signatures computed over `METHOD|PATH|TIMESTAMP`
- `CREDUENT-ADMIN-TIMESTAMP`: ISO 8601 UTC timestamp of the request
- **Legacy Fallback Header**: `CREDUENT-ADMIN-KEY: <admin_secret>`

**Success Response (200):**
```json
{
  "success": true,
  "agent_id": "agent://example/mybot",
  "level": "revoked"
}
```

**Error Responses:**

| Code | Reason |
|:---|:---|
| 401 | Missing or invalid admin key |
| 404 | Agent not registered |

---

### 3.5a POST /admin/attest

Upgrade the attestation level of an existing agent.

**Required Headers (Multisig Quorum):** Same as `DELETE /revoke` (Multisig headers or legacy fallback).

**Request:**
```json
{
  "agent_id": "agent://example/mybot",
  "level": "verified"
}
```

Valid levels: `"unverified"`, `"verified"`, `"trusted"`.

**Success Response (200 OK):**
```json
{
  "agent_id": "agent://example/mybot",
  "issuer": "agent://creduent/registry",
  "level": "verified",
  "issued_at": "2026-05-30T00:00:00Z",
  "expires_at": "2027-05-30T00:00:00Z",
  "public_key": "ed25519:hArTvbITJ2jirL170IOSjcVvEvstC4s+RjYLu4chCwg=",
  "domain": "example.com",
  "signature": "...",
  "status": "upgraded"
}
```

**Error Responses:**

| Code | Reason |
|:---|:---|
| 400 | Invalid level value |
| 401 | Missing or invalid admin key |
| 404 | Agent not registered |

---

### 3.6 POST /renew

Renew an attestation before it expires.

**Request:**
```json
{
  "agent_id": "agent://example/mybot",
  "new_expires_at": "2028-05-30T00:00:00Z",
  "signature": "<base64_signature>"
}
```

The `signature` MUST be computed using one of the following formats:
- **JCS Canonicalized Dictionary (Modern Standard)**: The request fields `agent_id` and `new_expires_at` formatted as a JSON object and canonicalized via RFC 8785:
  ```json
  {"agent_id":"agent://example/mybot","new_expires_at":"2028-05-30T00:00:00Z"}
  ```
- **Pipe-Delimited String (Deprecated Fallback)**: The UTF-8 string `agent_id|new_expires_at`.

**Success Response (200):** Returns updated attestation object.

**Error Responses:**

| Code | Reason |
|:---|:---|
| 400 | Invalid signature |
| 404 | Agent not registered |

---

### 3.7 POST /webhook/register

Register a webhook URL for lifecycle event notifications.

**Request:**
```json
{
  "agent_id": "agent://example/mybot",
  "webhook_url": "https://example.com/hooks/creduent",
  "signature": "<base64_signature>"
}
```

The `signature` MUST be computed using one of the following formats:
- **JCS Canonicalized Dictionary (Modern Standard)**: The request fields `agent_id` and `webhook_url` formatted as a JSON object and canonicalized via RFC 8785:
  ```json
  {"agent_id":"agent://example/mybot","webhook_url":"https://example.com/hooks/creduent"}
  ```
- **Pipe-Delimited String (Deprecated Fallback)**: The UTF-8 string `agent_id|webhook_url` (e.g. `"agent://example/mybot|https://example.com/hooks/creduent"`).

**Success Response (200):**
```json
{
  "success": true,
  "agent_id": "agent://example/mybot",
  "webhook_url": "https://example.com/hooks/creduent"
}
```

---

### 3.8 GET /webhook/{agent_id}

Retrieve the registered webhook URL for an agent.

**Required Headers:** Same as `DELETE /revoke` (Multisig headers or legacy fallback).

**Success Response (200):**
```json
{
  "agent_id": "agent://example/mybot",
  "webhook_url": "https://example.com/hooks/creduent"
}
```

---

### 3.9 GET /stats

Registry telemetry.

**Success Response (200):**
```json
{
  "total": 100,
  "verified": 87,
  "unverified": 8,
  "revoked": 5,
  "expiring_soon": 3
}
```

---

### 3.10 GET /dashboard

Returns the developer dashboard HTML UI. Available at `creduent.idevsec.com/dashboard`.

---

### 3.11 GET /resolver

Returns the `agent://` URI resolver UI. Available at `creduent.idevsec.com/resolver`.

---

### 3.12 GET /challenge/{agent_id}

Generate a cryptographic challenge to initiate the authentication process.

**Path Parameter:** `agent_id` is the URI-encoded `agent://namespace/name` string.

**Success Response (200):**
```json
{
  "agent_id": "agent://cyberhavox/havox-ai",
  "challenge": "8f3a...b2c9",
  "nonce": "e4f8...1a2b",
  "expires_at": "2026-05-31T05:25:00Z",
  "issuer": "agent://creduent/registry"
}
```

---

### 3.13 POST /verify-challenge

Verify the signed challenge and return a short-lived proof token.

**Request:**
```json
{
  "agent_id": "agent://cyberhavox/havox-ai",
  "nonce": "e4f8...1a2b",
  "signature": "<base64_signature>"
}
```

*Note:* The signature is computed using the agent's private key over the `SHA-256` hash of the concatenated string `challenge + nonce` (UTF-8 encoded).

**Success Response (200):**
```json
{
  "agent_id": "agent://cyberhavox/havox-ai",
  "verified": true,
  "level": "verified",
  "proof_token": "<base64_proof_token>",
  "valid_until": "2026-05-31T06:20:00Z",
  "issuer": "agent://creduent/registry"
}
```

---

### 3.14 GET /public-key

Retrieve the registry's public key for signature verification.

**Success Response (200):**
```json
{
  "public_key": "ed25519:hArTvbITJ2jirL170IOSjcVvEvstC4s+RjYLu4chCwg="
}
```

---

### 3.15 POST /recovery/override

Emergency key rotation/recovery via out-of-band DNS verification.

**Request:**
```json
{
  "agent_id": "agent://example/mybot",
  "domain": "example.com",
  "new_public_key": "ed25519:new_public_key_base64"
}
```

**Validation steps performed:**
1. Checks that the agent exists in the registry and its registered domain matches `domain`.
2. Performs a live DNS TXT lookup at `_creduent_recovery.{domain}` and checks if it contains `new_public_key`.
3. If verified, overwrites the agent's public key with `new_public_key`, resets the attestation level to `unverified`, re-signs the attestation, and persists it.

**Success Response (200 OK):**
```json
{
  "agent_id": "agent://example/mybot",
  "issuer": "agent://creduent/registry",
  "level": "unverified",
  "issued_at": "2026-06-23T00:00:00Z",
  "expires_at": "2026-07-23T00:00:00Z",
  "public_key": "ed25519:new_public_key_base64",
  "domain": "example.com",
  "signature": "...",
  "status": "recovered"
}
```

---

## 4. Authentication

The registry uses admin-key authentication only for destructive operations (revocation). All read and registration endpoints are unauthenticated by design to support open, decentralized verification.

| Operation | Auth Required |
|:---|:---|
| POST /register | No |
| POST /attest | No |
| GET /attest/{id} | No |
| GET /agents | No |
| POST /admin/attest | Yes (Multisig headers / symmetric key fallback) |
| DELETE /revoke | Yes (Multisig headers / symmetric key fallback) |
| POST /recovery/override | DNS validation proof required |
| POST /renew | Signature required |
| POST /webhook/register | Signature required |
| GET /webhook/{id} | Yes (Multisig headers / symmetric key fallback) |
| GET /challenge/{id} | No |
| POST /verify-challenge | Signature required |
| GET /public-key | No |

---

## 5. Rate Limiting

Implementations SHOULD apply rate limiting to prevent abuse.

| Endpoint | Suggested Limit |
|:---|:---|
| POST /register | 10 requests/hour per IP |
| POST /attest | 20 requests/hour per IP |
| GET /attest/{id} | 300 requests/minute per IP |
| GET /agents | 60 requests/minute per IP |
| DELETE /revoke | 30 requests/hour per admin key |
| POST /recovery/override | 60 requests/minute per IP |
| GET /challenge/{id} | 10 requests/minute per IP |
| POST /verify-challenge | 60 requests/minute per IP |
| GET /public-key | 300 requests/minute per IP |

Rate limit responses use HTTP 429 with a `Retry-After` header.

---

## 6. SSRF Protection

The `/register` endpoint fetches external URLs. Implementations MUST:
- Resolve the hostname to an IP before connecting.
- Block requests to private IP ranges (RFC 1918): `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`.
- Block loopback: `127.0.0.0/8`.
- Block link-local: `169.254.0.0/16`.
- Block IPv6 private ranges: `::1`, `fc00::/7`.
- Set a connection timeout of 5 seconds maximum.

---

## 7. Changelog

| Version | Date | Notes |
|:---|:---|:---|
| 0.4 | 2026-05-31 | Added Challenge-Response Authentication endpoints (`/challenge`, `/verify-challenge`, `/public-key`). |
| 0.3 | 2026-05-30 | Extracted from README.md and SPEC.md into standalone standards document. |
| 0.2 | 2026-05-27 | Added webhook and renewal endpoints. |
| 0.1 | 2026-05-01 | Initial registry API. |
