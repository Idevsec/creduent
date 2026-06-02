# Creduent Protocol: Federation Architecture

**Status:** Forward-looking design document. No current protocol behavior is changed.  
**Version:** 0.1  
**Date:** 2026-05-30  
**Formal Standard:** [CREDUENT-005](standards/CREDUENT-005-federation.md)

---

## What This Document Is

This document describes how the Creduent Protocol is designed to support multiple independent registries operating in a trust-federated network, without requiring a single global authority.

It is written for:
- Protocol architects evaluating long-term design decisions.
- Organizations considering running a private or enterprise Creduent registry.
- Contributors to [CREDUENT-005](standards/CREDUENT-005-federation.md).

**No current protocol behavior is changed by anything described here.** All existing `agent.json` documents, attestations, and registry deployments remain fully valid.

---

## The Core Design Insight

The Creduent v1.0 protocol already contains the structural foundations for federation. This is not accidental.

### What v1.0 already has:

**1. The `issuer` field in attestations**

Every attestation object contains:
```json
{
  "issuer": "agent://creduent/registry",
  ...
}
```

In v1.0, this is always the Creduent reference registry. In a federated world, this field identifies which registry issued the attestation. The field is already in the schema. No schema change is needed.

**2. The registry signs using Ed25519 over JCS**

The same algorithm used to verify `agent.json` documents is used to verify attestations. Any verifier that knows a registry's public key can independently verify any attestation that registry issued. This is already working in v1.0.

**3. The `agent://` URI is not registry-scoped**

An agent's identity (`agent://example/mybot`) is independent of which registry attested it. The same agent can be attested by multiple registries, or migrate between registries, without changing its identity.

**4. A registry's own identity is expressed as an `agent.json`**

The reference registry at `api.idevsec.com` publishes its own identity at `/.well-known/agent.json`. A federated trust chain can verify registries using the exact same mechanism used to verify agents.

---

## Current Single Points of Trust

The following items in v1.0 would need to be addressed to enable production federation:

| Item | Current State | Federation Path |
|:---|:---|:---|
| Registry URL | Hardcoded to `api.idevsec.com` in SDKs | SDKs accept configurable `baseUrl` option (already supported) |
| Registry public key | Provided via `CREDUENT_REGISTRY_PUBKEY` env var | Discoverable via `/.well-known/creduent-registry.json` |
| `issuer` in attestations | Always `"agent://creduent/registry"` | Already a variable field; verifiers must check dynamically |
| Namespace ownership | No enforcement | DNS-based namespace binding (future CIP) |
| Cross-registry revocation | Not propagated | Signed revocation events or revocation list endpoint |

---

## The Target Architecture

```
IDevSec Root Registry
          |
          +-- Attests Registry A (my-org.com)
          |         |
          |         +-- Attests agents: agent://my-org/*
          |
          +-- Attests Registry B (enterprise.com)
          |         |
          |         +-- Attests agents: agent://enterprise/*
          |
          +-- Attests Registry C (community.ai)
                    |
                    +-- Attests agents: agent://community/*
```

A verifier that trusts the IDevSec root registry can transitively trust attestations from any registry IDevSec has attested. The verification chain is:

```
agent.json (self-signed)
    |
    v
Registry attestation (signed by Registry A key)
    |
    v
Registry A's own agent.json (signed by Registry A)
    |
    v
Root attestation of Registry A (signed by IDevSec key)
    |
    v
IDevSec's own agent.json (self-verified trust anchor)
```

---

## Registry Discovery: Proposed `/.well-known/creduent-registry.json`

To make registries discoverable without out-of-band configuration, registries will publish a metadata document:

```
https://<registry-domain>/.well-known/creduent-registry.json
```

Proposed structure:
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

Verifiers can bootstrap trust by fetching this document and verifying `attested_by` against a known root.

---

## Namespace Federation: DNS-Based Ownership

In a multi-registry world, `agent://myorg/*` should only be controllable by the owner of `myorg.com`. Proposed enforcement:

```
_creduent-ns.myorg.com  TXT  "agent://myorg"
```

Any registry that issues attestations for agents in the `myorg` namespace SHOULD verify this DNS record before accepting the registration. This mirrors the per-agent DNS TXT verification already in CREDUENT-002.

This change requires:
- No changes to CREDUENT-001 or CREDUENT-002.
- A new registry implementation behavior (future CIP).

---

## Running a Private Registry

Organizations can deploy a private Creduent registry today using the reference implementation. The registry API specification is in [CREDUENT-003](standards/CREDUENT-003-registry-api.md).

Point your SDKs and MCP server at your private registry:

**Python:**
```python
import os
os.environ["CREDUENT_REGISTRY_URL"] = "https://registry.my-org.internal"

from creduent import register
result = register(agent_id="agent://my-org/mybot", ...)
```

**JavaScript:**
```typescript
import { resolveAgent } from "@idevsec/creduent";
const record = await resolveAgent("agent://my-org/mybot", {
  baseUrl: "https://registry.my-org.internal"
});
```

**MCP Server:**
```json
{
  "env": {
    "CREDUENT_REGISTRY_URL": "https://registry.my-org.internal",
    "CREDUENT_REGISTRY_PUBKEY": "ed25519:<your-registry-public-key>"
  }
}
```

Agents registered with a private registry are self-verifiable (CREDUENT-001) regardless of registry federation status.

---

## Participation

Federation design is actively being developed under [CREDUENT-005](standards/CREDUENT-005-federation.md). To contribute:

1. Read the full draft in `standards/CREDUENT-005-federation.md`.
2. Join the discussions or open an issue on the repository.
3. Propose changes via a pull request.
