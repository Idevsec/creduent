# CREDUENT-005: Federation and Cross-Registry Trust

**Status:** Draft  
**Version:** 0.1  
**Author:** IDevSec  
**Date:** 2026-05-30  
**Related:** [CREDUENT-002](CREDUENT-002-attestation.md), [CREDUENT-003](CREDUENT-003-registry-api.md)

---

## 1. Introduction

This document defines the architecture for federated Creduent registries. It is a **Draft** standard describing the intended future-compatible design. No current protocol behavior is changed by this document.

The core protocol (CREDUENT-001 through CREDUENT-004) is deliberately designed around a single reference registry (`api.idevsec.com`). This simplifies initial adoption and reduces operational complexity for early implementers. However, the protocol's architecture must not permanently entrench this single point of trust.

This document describes:
- The trust model required for federation.
- How multiple registries can recognize each other's attestations.
- Forward-compatible design decisions already present in the v1.0 protocol.
- What needs to be built to enable federation without breaking the current protocol.

---

## 2. Current Trust Architecture

In v1.0, the trust chain is:

```
Agent (self-signed agent.json)
   |
   v
Creduent Registry (api.idevsec.com)
   |  verifies: schema, signature, DNS, endpoint
   v
Attestation (signed by registry private key)
   |
   v
Client (verifies attestation against CREDUENT_REGISTRY_PUBKEY)
```

**Single points of trust identified:**

| Item | Risk |
|:---|:---|
| `api.idevsec.com` is the only registry | If it goes offline, all verification fails unless clients hold attestation cache |
| `CREDUENT_REGISTRY_PUBKEY` is pinned by env var | Clients must be reconfigured when registry key rotates |
| `issuer` field is hardcoded to `"agent://creduent/registry"` | No structural space for multiple issuers in the current schema |
| Namespace squatting is unresolved | `agent://myorg/*` can be claimed by anyone |

---

## 3. Forward-Compatible Design in v1.0

Several decisions made in the v1.0 protocol already accommodate federation:

- **The `issuer` field exists in the attestation object.** In v1.0, it is always `"agent://creduent/registry"`. In a federated model, it would contain the URI of the issuing registry.
- **The `signature` in attestations uses Ed25519 with JCS canonicalization**, the same algorithm used for `agent.json`. A verifier that knows a registry's public key can independently verify any attestation that registry issues.
- **The `agent://` URI scheme is not registry-scoped.** An agent identity is globally unique and not tied to any specific registry.
- **The registry's own identity is expressed as an `agent.json`** at `/.well-known/agent.json`. A federated trust graph could verify registries using the same protocol used to verify agents.

---

## 4. Federated Architecture (Target Design)

### 4.1 Registry as an Agent

Each Creduent-compatible registry publishes its own `agent.json`:

```json
{
  "version": "1.0",
  "agent_id": "agent://my-org/registry",
  "owner": "My Organization",
  "public_key": "ed25519:<registry_public_key>",
  "endpoint": "https://registry.my-org.com",
  "capabilities": ["attest", "resolve", "revoke"],
  "signature": "..."
}
```

This allows any verifier to:
1. Resolve a registry's identity using the same protocol used for agents.
2. Verify the registry's signing key against its own self-signed document.
3. Build a trust chain: `agent --> registry attestation --> registry agent.json --> (optional) root registry attestation`.

### 4.2 Trust Anchor Model

Federation requires at least one trust anchor. Proposed options:

**Option A: Root Registry**  
IDevSec operates a root registry that attests other registries. A verifier that trusts the root registry transitively trusts all attested registries.

```
Root Registry (IDevSec)
    |
    +-- Attests: Registry A (my-org.com)
    +-- Attests: Registry B (enterprise.com)
    +-- Attests: Registry C (community.ai)
```

**Option B: Web of Trust**  
Registries mutually attest each other. Verifiers accumulate trusted keys over time. No root registry required.

**Option C: Explicit Allowlist**  
Verifiers maintain a local list of trusted registry public keys. Simpler to implement, less scalable.

The v1.0 protocol does not mandate any of these options. CREDUENT-005 will be updated when consensus is reached.

### 4.3 Cross-Registry Agent Lookup

When a verifier queries a registry for `agent://someorg/bot` and receives a 404, it SHOULD:
1. Check whether other trusted registries have an attestation for that agent.
2. Verify the attestation signature against the issuing registry's known public key.
3. Surface the attestation to the consumer with the `issuer` field clearly identified.

### 4.4 Attestation Portability

An attestation issued by Registry A is verifiable by any client that:
- Knows Registry A's public key.
- Can verify Ed25519 signatures over JCS-canonicalized JSON.

This is already achievable in v1.0. The missing piece is a standardized discovery mechanism for registry public keys.

---

## 5. Blockers to Federation (Current)

The following items are not yet specified and must be resolved before federation is production-ready:

| Blocker | Description | Resolution Path |
|:---|:---|:---|
| Registry discovery | No standard way to find other registries | A `/.well-known/creduent-registry.json` endpoint for registry metadata |
| Key rotation protocol | No standard for announcing registry key rotation | Future CIP |
| Namespace ownership | Namespace squatting is unresolved | Organization namespace registry or DNS-based namespace binding |
| Cross-registry revocation | Revocation in one registry is not propagated | Revocation list publication or signed revocation events |
| Trust anchor consensus | No agreement on root-of-trust model | Consensus required |

---

## 6. Proposed `/.well-known/creduent-registry.json` Format

To enable discovery, registries SHOULD publish a metadata document at:

```
https://<registry-domain>/.well-known/creduent-registry.json
```

Proposed structure (subject to revision):

```json
{
  "version": "1.0",
  "registry_id": "agent://my-org/registry",
  "name": "My Org Creduent Registry",
  "public_key": "ed25519:<base64>",
  "endpoint": "https://registry.my-org.com",
  "attested_by": "agent://creduent/registry",
  "attested_at": "2026-05-30T00:00:00Z"
}
```

---

## 7. Namespace Federation

In a multi-registry world, the question of who controls `agent://myorg/*` must be resolved.

**Proposed approach (future CIP):**

Namespace ownership is established by DNS. The entity controlling `myorg.com` also controls the `myorg` namespace, proven by a DNS TXT record:

```
_creduent-ns.myorg.com TXT "agent://myorg"
```

This does not require any changes to the current protocol and is backward-compatible with the existing `_creduent.<domain>` DNS record format.

---

## 8. What Changes Nothing in v1.0

Implementing this federation design in a future version will require:
- A new `CREDUENT-005`-compliant registry discovery mechanism.
- An update to attestation verification to accept `issuer` values other than `"agent://creduent/registry"` when the issuer is itself verified.

It does NOT require:
- Changes to the `agent.json` schema (CREDUENT-001).
- Changes to the attestation object structure (CREDUENT-002).
- Changes to the registry API endpoints (CREDUENT-003).
- Changes to the `agent://` URI syntax (CREDUENT-004).

All existing v1.0 agents and attestations remain valid in a federated world.

---

## 9. Changelog

| Version | Date | Notes |
|:---|:---|:---|
| 0.1 | 2026-05-30 | Initial draft. Captures existing architecture, single-trust blockers, and proposed federation design. No protocol changes. |
