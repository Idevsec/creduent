# CREDUENT-004: Agent URI Resolution

**Status:** Active  
**Version:** 0.3  
**Author:** IDevSec  
**Date:** 2026-05-30  
**Related:** [CREDUENT-001](../SPEC.md), [CREDUENT-003](CREDUENT-003-registry-api.md)

---

## 1. Introduction

The `agent://` URI scheme provides a globally unique, human-readable identifier for autonomous AI agents. This document specifies:
- The syntax of `agent://` URIs.
- The resolution algorithm: how any verifier translates an `agent://` URI into a fetchable `agent.json` document.
- Fallback and offline resolution behaviour.

---

## 2. URI Syntax

```
agent://<namespace>/<agent-name>
```

| Component | Description | Constraints |
|:---|:---|:---|
| `namespace` | Identifies the owner or organization of the agent. | Alphanumeric, hyphens (`-`), underscores (`_`) only. No dots, slashes, or special characters. |
| `agent-name` | The agent's unique name within the namespace. | Same character constraints as namespace. |

**Valid examples:**
```
agent://idevsec/steward
agent://my-org/data-processor
agent://acme_corp/support_agent
```

**Invalid examples:**
```
agent://creduent.ai/bot        (dots not allowed in namespace)
agent://example/sub/path       (sub-paths not allowed)
agent://example/bot@v2         (special characters not allowed)
```

---

## 3. Resolution Algorithm

A resolver MUST attempt the following steps in order, stopping at the first successful result.

### Step 1: Registry Lookup (Recommended Primary Path)

Query the Creduent registry for a known agent record:

```
GET https://creduent.idevsec.com/attest/<uri-encoded-agent-id>
```

If the registry returns a 200 response with a valid attestation, extract the `domain` field and proceed to Step 2 for document retrieval. If the registry returns 404, proceed to Step 2 with namespace-derived domain heuristics.

### Step 2: Well-Known URL Construction

Construct the agent.json URL using the namespace as a domain heuristic:

```
https://api.<namespace>.ai/.well-known/agent.json
```

Or alternatively (if `namespace` looks like a domain):

```
https://<namespace>/.well-known/agent.json
```

If the registry returned a domain in Step 1, use that domain directly:

```
https://<domain>/.well-known/agent.json
```

### Step 3: Local Registry Lookup (Offline Fallback)

Check for a local `examples/registry.json` file mapping agent URIs to local file paths. This supports development and testing without network access.

```json
{
  "agent://idevsec/steward": "examples/reconbot.agent.json"
}
```

### Step 4: Fail

If all steps fail, the resolver MUST return a structured error indicating that the agent could not be resolved.

---

## 4. Resolution Flow Diagram

```
Resolver receives agent:// URI
          |
          v
   Query Registry API
          |
     +-----------+
     | 200 OK?   |
     +-----------+
       Yes  |  No
            |    |
            |    v
            |  Derive domain from namespace
            |  Try /.well-known/agent.json
            |         |
            |   +------+------+
            |   | Reachable?  |
            |   +------+------+
            |    Yes |  No
            v        |       v
      Fetch doc       |   Local registry
      Validate        |   lookup (offline)
      Return          |          |
                      |     Not found?
                      |          |
                      v          v
                   Resolution Error
```

---

## 5. DNS TXT Verification

To confirm that a domain actually claims a given `agent_id`, verifiers SHOULD perform a DNS TXT lookup:

**Record name:** `_creduent.<domain>`  
**Expected value:** The full `agent://namespace/agent-name` URI string.

Example:
```
_creduent.example.com TXT "agent://example/mybot"
```

This step is performed by the registry during `/register`. Client-side verifiers MAY perform it independently for additional assurance.

---

## 6. Resolver Reference Implementation

The reference implementation is at `creduent.idevsec.com/resolver`. It accepts an `agent://` URI and returns:
- The resolved `agent.json` document.
- The resolution path taken (registry, well-known, or local).
- Self-verification result.
- Registry attestation status.

The resolver UI is accessible in a browser at `creduent.idevsec.com/resolver`.

---

## 7. Python SDK Usage

```python
from creduent import verify

# Resolve and verify by agent:// URI
result = verify("agent://idevsec/steward")
print(result.valid)       # True/False
print(result.agent_id)    # "agent://idevsec/steward"
```

## 8. JavaScript SDK Usage

```typescript
import { resolveAgent } from "@idevsec/creduent";

const record = await resolveAgent("agent://idevsec/steward");
console.log(record.agent_id);
console.log(record.level); // "verified" | "unverified" | "revoked"
```

---

## 9. Security Considerations

- Resolvers MUST validate the Ed25519 signature of the fetched `agent.json` before trusting any fields.
- Resolvers MUST apply SSRF protections when fetching remote `agent.json` documents.
- The namespace-to-domain heuristic (`api.<namespace>.ai`) is a best-effort fallback and SHOULD NOT be trusted without signature verification.
- DNS TXT records are advisory. They cannot substitute for cryptographic verification.

---

## 10. Changelog

| Version | Date | Notes |
|:---|:---|:---|
| 0.3 | 2026-05-30 | Formalized from SPEC.md and MCP server logic into standalone document. |
| 0.2 | 2026-05-27 | Added local registry fallback. |
| 0.1 | 2026-05-01 | Initial URI syntax and resolution algorithm. |
