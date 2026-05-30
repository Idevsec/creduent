# CREDUENT-001: agent.json Specification

**Status:** Active  
**Version:** 0.3  
**Author:** Creduent Protocol Working Group  
**Date:** 2026-05-30  
**Canonical Source:** [SPEC.md](../SPEC.md)  
**Related:** [CREDUENT-002](CREDUENT-002-attestation.md), [CREDUENT-004](CREDUENT-004-uri-resolution.md)

---

## Note on Canonical Source

The full normative text of CREDUENT-001 is maintained in [SPEC.md](../SPEC.md) at the root of this repository. That file carries the `# CREDUENT-001: agent.json Specification` heading and is the authoritative reference for:

- Section 2: The `agent.json` Document and core field definitions
- Section 3: Cryptographic signing and RFC 8785 canonicalization
- Section 4: Verification workflow (schema, signature, endpoint check)
- Section 5: Security and liability boundaries
- Section 6: Registry and attestation layer (see also CREDUENT-002)
- Section 7: MCP integration and `verify_agent` tool schema
- Section 8: Official SDK references

This file exists as a standards-track entry point to maintain consistency with the CREDUENT numbering system. All implementers should read [SPEC.md](../SPEC.md) for the full normative text.

---

## Summary

CREDUENT-001 defines the `agent.json` identity document format for autonomous AI agents. Every participating agent publishes a machine-readable identity file at:

```
https://<domain>/.well-known/agent.json
```

### Required Fields

| Field | Type | Description |
|:---|:---|:---|
| `version` | String | Protocol version. MUST be `"1.0"`. |
| `agent_id` | String | Global URI: `agent://<namespace>/<agent-name>`. |
| `owner` | String | Human-readable owner name. |
| `public_key` | String | Ed25519 public key: `ed25519:<base64>`. |
| `endpoint` | String | HTTPS URL of the agent's API endpoint. |
| `capabilities` | Array of Strings | Semantic capability tags. |
| `signature` | String | Ed25519 signature over JCS-canonicalized payload. |

### Optional Fields

| Field | Type | Description |
|:---|:---|:---|
| `issued_at` | String | RFC 3339 UTC timestamp of document creation. |

### Signing Algorithm Summary

1. Construct the document with all fields except `signature`.
2. Canonicalize using RFC 8785 (JCS): sort keys lexicographically, remove whitespace, normalize numbers.
3. Sign the UTF-8 bytes of the canonical string using Ed25519.
4. Base64-encode the 64-byte signature.
5. Append `"signature"` to the document.

### Verification Algorithm Summary

1. Fetch `agent.json` from `/.well-known/agent.json`.
2. Validate against the JSON schema in `schemas/agent.schema.json`.
3. Extract and remove the `signature` field.
4. JCS-canonicalize the remaining document.
5. Verify the Ed25519 signature against the embedded `public_key`.
6. Optionally check endpoint reachability.

---

## Schema

The machine-readable JSON schema is at [`schemas/agent.schema.json`](../schemas/agent.schema.json).

---

## Changelog

| Version | Date | Notes |
|:---|:---|:---|
| 0.3 | 2026-05-30 | Formally entered into standards track. Standards index entry created. |
| 0.2 | 2026-05-27 | Added `issued_at` optional field. |
| 0.1 | 2026-05-01 | Initial specification. |
