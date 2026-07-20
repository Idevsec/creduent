# CREDUENT-002: Attestation Specification

**Status:** Active 
**Version:** 0.4 
**Author:** IDevSec 
**Date:** 2026-07-20 
**Supersedes:** N/A 
**Related:** [CREDUENT-001](SPEC.md), [CREDUENT-003](standards/CREDUENT-003-registry-api.md)

---

## 1. Introduction

A self-signed `agent.json` document (defined in CREDUENT-001) proves cryptographic ownership of an agent identity. It does not, however, prove that:
- The declared domain actually hosts the agent.
- The DNS configuration binds the domain to the agent ID.
- The agent's endpoint is reachable.
- Any third party has independently verified the agent's claims.

The **Attestation Layer** closes this gap. An attestation is a short-lived, third-party-signed assertion that a registry has independently verified the above claims.

This document specifies:
- The **Attestation Object** structure and semantics.
- The **Registration Flow** by which an agent earns an attestation.
- The **Revocation Model**.
- The **Renewal Protocol**.
- The **Webhook Notification** system for lifecycle events.

---

## 2. Attestation Object

A Creduent Attestation is a JSON document with the following fields:

| Field | Type | Required | Description |
|:---|:---|:---|:---|
| `agent_id` | String | | The agent's globally unique URI (`agent://namespace/name`). |
| `issuer` | String | | The attestation issuer's identity URI. MUST be `"agent://creduent/registry"` for official attestations. |
| `level` | String | | Trust level. One of: `"unverified"`, `"verified"`, `"trusted"`, `"revoked"`. |
| `issued_at` | String | | RFC 3339 UTC timestamp of attestation issuance. |
| `expires_at` | String | | RFC 3339 UTC timestamp when the attestation expires. |
| `public_key` | String | | The agent's public key, matching its `agent.json`. Format: `ed25519:<base64>`. |
| `domain` | String | | The domain under which the agent operates (e.g. `"example.com"`). |
| `signature` | String | | Ed25519 signature by the registry over the JCS-canonicalized attestation (excluding `signature`). |

### 2.1 Example Attestation Object

```json
{
 "agent_id": "agent://example/mybot",
 "issuer": "agent://creduent/registry",
 "level": "verified",
 "issued_at": "2026-05-30T00:00:00Z",
 "expires_at": "2026-06-29T00:00:00Z",
 "public_key": "ed25519:hArTvbITJ2jirL170IOSjcVvEvstC4s+RjYLu4chCwg=",
 "domain": "example.com",
 "signature": "base64_registry_signature_here"
}
```

### 2.2 Attestation Levels

| Level | Meaning |
|:---|:---|
| `unverified` | Agent is registered but one or more verification steps failed or were skipped (e.g., public registration before verification is completed). |
| `verified` | All verification steps passed: schema valid, Ed25519 signature valid, DNS TXT record matches agent_id, endpoint reachable. |
| `trusted` | Manually reviewed and escalated trust level assigned by registry administrators. |
| `revoked` | Agent registration was explicitly revoked by an administrator. |

### 2.3 Lifecycle Status

While **Trust Level** (`level`) represents the cryptographic verification tier of an agent, its **Lifecycle Status** is a dynamically computed state indicating whether the credential is active or expired.

Verifiers and dashboards resolve the lifecycle status as follows:
* **active**: The attestation has not expired (current time is before `expires_at`) and its level is not `revoked`.
* **expiring**: The attestation has not expired, but will expire within 30 days, and its level is not `revoked`.
* **expired**: The current time has surpassed the attestation's `expires_at` timestamp.
* **revoked**: The attestation's trust level is `revoked`, which supersedes all expiration-based status computations.

---

## 3. Registration Flow

To obtain a `verified` attestation, an agent owner submits a `POST /register` request. The registry executes the following verification pipeline in sequence:

```
POST /register
 │
 ├── 1. SSRF Guard ─── Block private/loopback IPs
 │
 ├── 2. Fetch agent.json ─── from agent_json_url
 │
 ├── 3. Schema Validation ─── against CREDUENT-001 schema
 │
 ├── 4. Signature Verification ─── Ed25519 over JCS payload
 │
 ├── 5. DNS TXT Check ─── _creduent.{domain} == agent_id
 │
 ├── 6. Endpoint Healthcheck ─── HTTP GET to declared endpoint
 │
 └── 7. Issue Attestation ─── Sign and store in registry
```

### 3.1 Request Body

```json
{
 "agent_id": "agent://example/mybot",
 "domain": "example.com",
 "agent_json_url": "https://example.com/.well-known/agent.json"
}
```

### 3.2 Success Response (201 Created)

```json
{
 "success": true,
 "agent_id": "agent://example/mybot",
 "attestation": {
 "agent_id": "agent://example/mybot",
 "issuer": "agent://creduent/registry",
 "level": "verified",
 "issued_at": "2026-05-30T00:00:00Z",
 "expires_at": "2026-06-29T00:00:00Z",
 "public_key": "ed25519:hArTvbITJ2jirL170IOSjcVvEvstC4s+RjYLu4chCwg=",
 "domain": "example.com",
 "signature": "..."
 }
}
```

### 3.3 Alternative: Direct Attestation (`POST /attest`)

For programmatic and dashboard use, agents may register directly without providing `agent_json_url`. The registry will not perform DNS or endpoint checks; the resulting attestation will have `level: "unverified"`.

**Request body:**
```json
{
 "agent_id": "agent://example/mybot",
 "domain": "example.com",
 "public_key": "ed25519:hArTvbITJ2jirL170IOSjcVvEvstC4s+RjYLu4chCwg="
}
```

---

## 4. Attestation Retrieval

```http
GET /attest/{agent_id}
```

URL-encodes the `agent://` URI. Returns the full attestation object for the specified agent.

**Error Responses:**
- `404 Not Found`: Agent not registered.
- `200 OK` with `level: "revoked"`: Agent has been revoked (attestation object still returned).

---

## 5. Attestation Verification

Clients MUST perform the following steps when validating an attestation received from a registry:

1. **Confirm `issuer`** is `"agent://creduent/registry"` (or the known issuer for a federated registry).
2. **Check `expires_at`:** Reject expired attestations.
3. **Verify the registry signature:** Decode the `signature` field, remove it from the object, JCS-canonicalize the remainder, and verify the Ed25519 signature against the registry's known public key.
4. **Cross-check `public_key`:** Confirm the attestation's `public_key` matches the public key in the agent's `agent.json`.

The registry's public key MUST be obtained out-of-band (environment variable, pinned configuration, or the registry's own `agent.json` at `/.well-known/agent.json`).

---

## 6. Revocation

```http
DELETE /revoke/{agent_id}
Headers:
 CREDUENT-ADMIN-KEYS: <comma-separated-admin-keys>
 CREDUENT-ADMIN-SIGNATURES: <comma-separated-signatures>
 CREDUENT-ADMIN-TIMESTAMP: <iso8601-timestamp>
 # Fallback for legacy administrative keys:
 # CREDUENT-ADMIN-KEY: <admin_secret>
```

On successful revocation:
- The attestation `level` is set to `"revoked"`.
- Subsequent `GET /attest/{agent_id}` calls return the attestation with `level: "revoked"`, returning a `410 Gone` HTTP status code.
- The attestation object is not deleted; it serves as a public revocation notice.

**Clients MUST treat a `revoked` attestation as a failed verification.** A `revoked` status MUST be surfaced to the consumer; it MUST NOT be silently treated as `unregistered`.

---

## 7. Renewal

Agents must renew their attestation before `expires_at`. Renewal is triggered via:

```http
POST /renew
Content-Type: application/json

{
 "agent_id": "agent://example/mybot",
 "new_expires_at": "2028-05-30T00:00:00Z",
 "signature": "<base64_signature>"
}
```

The `signature` field MUST be an Ed25519 signature computed over one of the following payload formats:

1. **JCS Canonicalized Dictionary (Recommended)**: A JSON object containing the renewal fields, canonicalized using RFC 8785 JSON Canonicalization Scheme (JCS):
 ```json
 {
 "agent_id": "agent://example/mybot",
 "new_expires_at": "2028-05-30T00:00:00Z"
 }
 ```
2. **Pipe-Delimited String (Alternative)**: The delimited concatenation UTF-8 bytes:
 ```
 agent_id|new_expires_at
 ```
 For example: `"agent://example/mybot|2028-05-30T00:00:00Z"`

The registry supports both formats during verification against the agent's registered `public_key`, then re-issues and re-signs the attestation with the updated `expires_at`.

---

## 8. Webhook Notifications

Agents may register a webhook URL to receive lifecycle event notifications.

### 8.1 Register Webhook

```http
POST /webhook/register
Content-Type: application/json

{
 "agent_id": "agent://example/mybot",
 "webhook_url": "https://example.com/hooks/creduent",
 "signature": "<base64_signature>"
}
```

The `signature` field MUST be computed over one of the following payload formats:

1. **JCS Canonicalized Dictionary (Recommended)**: A JSON object containing the webhook registration fields, canonicalized using RFC 8785 (JCS):
 ```json
 {
 "agent_id": "agent://example/mybot",
 "webhook_url": "https://example.com/hooks/creduent"
 }
 ```
2. **Pipe-Delimited String (Alternative)**: The delimited concatenation: `agent_id|webhook_url`.

### 8.2 Webhook Events

| Event | When |
|:---|:---|
| `agent.registered` | Agent successfully registers. |
| `agent.expiry_warning` | 30 days before `expires_at`. |
| `agent.expired` | On `expires_at` if not renewed. |
| `agent.revoked` | When the agent is revoked. |

### 8.3 Payload Format

```json
{
 "event": "agent.expiry_warning",
 "agent_id": "agent://example/mybot",
 "domain": "example.com",
 "expires_at": "2027-05-30T00:00:00Z",
 "days_remaining": 28,
 "action_url": "https://creduent.idevsec.com/renew"
}
```

### 8.4 Cryptographic Signatures (HMAC-SHA256)

To prevent spoofing and replay attacks, every webhook notification sent by the registry MUST contain verification headers:

*   `X-Creduent-Timestamp`: The Unix epoch timestamp (seconds) when the notification was dispatched.
*   `X-Creduent-Signature256`: The hex-encoded HMAC-SHA256 signature.

The signature is computed over the UTF-8 bytes of:
```
timestamp + "." + canonical_json_payload
```
using the webhook's pre-shared secret key (returned during webhook registration).

Recipients MUST verify the signature before processing the event payload. Additionally, recipients SHOULD reject notifications with a timestamp offset greater than 300 seconds (5 minutes) to prevent replay attacks.

---

## 9. Security Considerations

- **Short-lived attestations**: The default attestation TTL is 30 days. Implementations SHOULD allow operators to configure shorter TTLs.
- **Registry key compromise**: If the registry's signing key is compromised, all existing attestations must be reissued. A key rotation event MUST be announced via the registry's `agent.json` and `/.well-known/creduent-registry.json`.
- **Admin key protection**: Administrative endpoints require multisig signature threshold verification to mitigate symmetric key exposure risks.
- **DNS propagation delay**: DNS TXT records may take up to 48 hours to propagate globally. The registry MUST NOT cache negative DNS results longer than 5 minutes.

---

## 10. Changelog

| Version | Date | Notes |
|:---|:---|:---|
| 0.4 | 2026-07-20 | Added X-Creduent-Signature256 and X-Creduent-Timestamp verification headers to webhook payloads. |
| 0.3 | 2026-05-30 | Extracted from SPEC.md into standalone standards document. Webhook signature requirement documented. |
| 0.2 | 2026-05-27 | Added renewal and webhook notifications. |
| 0.1 | 2026-05-01 | Initial attestation model. |
