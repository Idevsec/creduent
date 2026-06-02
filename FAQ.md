# Creduent: Frequently Asked Questions

---

## General

### What is Creduent?

Creduent is an open application-layer protocol for cryptographic identity and trust verification of autonomous AI agents. It lets any agent publish a signed identity document (`agent.json`) and get that identity independently verified and attested by a registry.

### Who maintains Creduent?

IDevSec. The protocol specification is open-source, and the reference registry runs at `api.idevsec.com`.

### Is Creduent a SaaS product or an open protocol?

It is an open protocol. The specification documents (CREDUENT-001 through CREDUENT-005) are free to implement. Anyone can run a Creduent-compatible registry. The reference registry at `api.idevsec.com` is one implementation, not the only one.

### What problem does Creduent solve?

When an AI agent contacts another agent or service, there is no standard way to answer: "Who is this agent, who controls it, and can I trust its declared capabilities?" Creduent provides that answer using cryptographic signatures and DNS-based domain binding, without requiring a central authority to pre-approve every agent.

### Does Creduent replace TLS or OAuth?

No. Creduent operates above the existing web stack. It uses HTTPS for transport and focuses specifically on agent-level identity and capability attestation, not on session authentication or authorization. Think of it as the equivalent of `robots.txt` for agent identity, with cryptographic verification added.

---

## Protocol and Specification

### What is agent.json?

A JSON document published at `https://<domain>/.well-known/agent.json`. It contains the agent's ID, owner, public key, endpoint, declared capabilities, and a cryptographic signature. It is the agent's self-signed identity claim.

### What cryptographic algorithm does Creduent use?

Ed25519 for signing. Documents are canonicalized before signing using RFC 8785 (JSON Canonicalization Scheme, JCS) to ensure consistent byte representation across parsers.

### Why Ed25519 instead of RSA or ECDSA?

Ed25519 produces short, fast, and secure signatures. Keys are 32 bytes. Signatures are 64 bytes. The algorithm has no parameter choices that can be misconfigured (unlike RSA key size or ECDSA curve selection).

### Why RFC 8785 (JCS) for canonicalization?

JSON is not canonical by default. Two JSON parsers can produce different byte sequences for the same logical object. JCS defines a deterministic serialization: properties are sorted lexicographically, whitespace is removed, and number formatting is normalized. This ensures the signed byte sequence is reproducible across all conforming implementations.

### What is the agent:// URI scheme?

A URI scheme for globally unique agent identifiers:

```
agent://<namespace>/<agent-name>
```

For example: `agent://example/mybot`. The namespace typically corresponds to the organization or domain. The agent-name is unique within that namespace.

### Does Creduent have an expiry mechanism?

The `agent.json` document itself has no `expires_at` field by design. Expiry is handled at the attestation layer. Registry attestations have an `expires_at` timestamp and must be renewed annually (or at the interval set by the registry).

### What happens if the registry is offline?

The MCP `verify_agent` tool degrades gracefully. If the registry is unreachable, it returns:
- `self_verified: true` (if the agent's own signature is valid)
- `creduent_attested: false`
- `attestation_level: "registry_offline"`

Self-signed verification still works without any registry connectivity.

---

## Registration and Verification

### What does "verified" vs "unverified" mean?

| Level | Meaning |
|:---|:---|
| `verified` | Schema valid, Ed25519 signature valid, DNS TXT record matched, endpoint reachable. |
| `unverified` | Agent is registered but one or more checks were skipped (typically DNS and endpoint). |
| `revoked` | Agent registration was explicitly revoked. |

### How long does registration take?

The `/register` API call takes under 10 seconds when DNS is already propagated. The main delay is DNS propagation, which can take up to 48 hours after you add the TXT record.

### Can I register without a domain?

Yes. Use `POST /attest` directly with your `agent_id`, `domain`, and `public_key`. You will receive an `unverified` attestation without DNS or endpoint checks.

### Can I register without a public web server?

No for `verified` status. The `/register` flow fetches `agent.json` from a publicly accessible HTTPS URL. For development and testing, use `POST /attest` which skips this requirement.

### Do I need to re-register if I rotate my signing keys?

Yes. Key rotation requires re-publishing `agent.json` with the new public key (signed with the new private key) and then re-registering or re-attesting with the registry. The registry will overwrite the old public key record.

### How do I renew an attestation before it expires?

Send a `POST /renew` request with the agent ID, a new expiry date, and an Ed25519 signature over `agent_id|new_expires_at`. See [EXAMPLES.md](EXAMPLES.md) for a complete code example.

### Will I be notified before my attestation expires?

Yes, if you register a webhook via `POST /webhook/register`. The auto-renewal daemon will send a `POST` to your webhook URL 30 days before expiry.

---

## Security

### What happens if someone copies my agent.json?

Copying `agent.json` is harmless. Without the private key, an attacker cannot produce a valid signature for any modified document. The signature covers all fields (except `signature` itself), so the document cannot be tampered with undetected.

### What if my private key is leaked?

Immediately generate a new keypair, re-sign and re-publish a new `agent.json`, and re-register with the registry. The old public key will be replaced. Anyone holding the old signed document can still verify it against the old key, so notifying downstream consumers of the key rotation is recommended.

### Can someone register my agent ID before I do?

Yes, in the current v1.0 protocol, namespace squatting is possible. The DNS TXT verification step mitigates this for `verified` attestations: only the owner of `example.com` can get a `verified` attestation for `agent://example/mybot`. Namespace ownership enforcement is planned for a future CIP (see [CREDUENT-005](standards/CREDUENT-005-federation.md)).

### Is the registry API authenticated?

Read operations and registration are unauthenticated by design. Revocation requires the `CREDUENT-ADMIN-KEY` header. Renewal and webhook registration require a valid Ed25519 signature from the agent's own private key.

### Does Creduent prevent malicious agents?

No. Creduent verifies identity and ownership, not intent or behavior. A `verified` attestation means the agent's cryptographic identity is authentic. It does not guarantee the agent is safe, non-malicious, or compliant with any policy. Higher-level attestation layers (auditor attestations, compliance bodies) are planned in CREDUENT-005.

---

## SDK and Tooling

### Which SDKs are available?

| SDK | Install | Source |
|:---|:---|:---|
| Python | `pip install creduent` | [github.com/idevsec/creduent-python](https://github.com/idevsec/creduent-python) |
| JavaScript / TypeScript | `npm install @idevsec/creduent` | [github.com/idevsec/creduent-js](https://github.com/idevsec/creduent-js) |
| CLI Tool | `npm install -g @idevsec/creduent-cli` | [github.com/idevsec/creduent-cli](https://github.com/idevsec/creduent-cli) |

### What Python version is required?

Python 3.9 or higher.

### What Node.js version is required?

Node.js 18 or higher. The SDK uses the native `fetch()` API.

### Can I use the JavaScript SDK in the browser?

Yes. The SDK uses native `fetch()` which is supported in all modern browsers. Be aware that CORS headers must be enabled on the registry API, which they are on `api.idevsec.com`.

### What is the MCP server?

A Model Context Protocol server that exposes the `verify_agent` tool. It allows AI agent hosts (such as Claude, Cursor, or any MCP-compatible host) to verify another agent's identity as a tool call. See [SPEC.md](SPEC.md) section 7 for the full response schema.

### How do I configure the MCP server to point to a custom registry?

Set the `CREDUENT_REGISTRY_URL` environment variable in your MCP server configuration:

```json
{
  "env": {
    "CREDUENT_REGISTRY_URL": "https://registry.my-org.com"
  }
}
```

---

## Ecosystem and Federation

### Can I run my own Creduent registry?

Yes. The registry API specification is defined in [CREDUENT-003](standards/CREDUENT-003-registry-api.md). Any server implementing those endpoints is a Creduent-compatible registry. The reference implementation source is in the `registry/` directory.

### Will my agents work across different registries?

In v1.0, a registry only returns attestations it has issued. Cross-registry trust is the subject of [CREDUENT-005](standards/CREDUENT-005-federation.md), which is currently a Draft standard. Self-signed verification (CREDUENT-001) works with no registry at all.

### Is Creduent related to any blockchain or Web3 system?

No. Creduent uses standard web infrastructure: HTTPS, DNS, and Ed25519 cryptography. It does not require or use any blockchain. Cross-chain attestation bridges for Web3 ecosystems are noted as a long-term roadmap item but are not part of any current or planned standard.

### Where can I follow protocol development?

- GitHub: [github.com/idevsec/creduent](https://github.com/idevsec/creduent)
- Discussions & Contributions: GitHub Issues and Discussions on the repository.
- Roadmap: [ROADMAP.md](ROADMAP.md)
