# `did:creduent` DID Method Specification

- **Method Name:** `creduent`
- **Status:** Provisional / Active
- **Author / Maintainer:** Kashish Kanojia (`kashish@idevsec.com`)
- **Organization:** IDevSec (`https://idevsec.com`)
- **License:** [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Copyright 2026 IDevSec)
- **Related Specifications:** [CREDUENT-001](CREDUENT-001-agent-json.md), [CREDUENT-004](CREDUENT-004-uri-resolution.md), [`draft-kanojia-creduent-agent-uri`](https://datatracker.ietf.org/doc/draft-kanojia-creduent-agent-uri/)

---

## 1. Abstract

The `did:creduent` method defines a decentralized identifier (DID) method for autonomous AI agents, software services, and Model Context Protocol (MCP) endpoints under the Creduent Protocol. It anchors cryptographic identity directly to authoritative Internet domain ownership using HTTPS `.well-known` endpoints, DNS TXT verification records, JSON Canonicalization Scheme (JCS, RFC 8785), and Ed25519 digital signatures.

Unlike ledger-based DID methods, `did:creduent` requires no blockchain consensus, gas fees, or external trust anchors beyond the existing Web PKI (TLS) and DNS infrastructure.

---

## 2. Method Syntax (ABNF)

The `did:creduent` identifier syntax conforms to the W3C Decentralized Identifiers (DIDs) v1.0 core syntax and is defined in Augmented Backus-Naur Form (ABNF, RFC 5234) as follows:

```abnf
did-creduent-format = "did:creduent:" namespace ":" agent-name
namespace           = domain-label *( "." domain-label )
domain-label        = ALPHA / DIGIT *( *( ALPHA / DIGIT / "-" ) ( ALPHA / DIGIT ) )
agent-name          = 1*( ALPHA / DIGIT / "-" / "_" )
```

### 2.1 Syntax Rules
- `namespace` MUST be a lowercase DNS domain name (or registered Creduent namespace) normalized per IDNA (RFC 5890).
- `agent-name` is a case-sensitive, URL-safe identifier unique within the `namespace`.
- Whitespace, percent-encoding, and path traversal characters (`..`, `/`, `\`) are strictly prohibited in both `namespace` and `agent-name`.

### 2.2 Examples
- `did:creduent:idevsec.com:steward`
- `did:creduent:example.org:audit_bot_01`

---

## 3. Target System & Trust Model

`did:creduent` operates on two standard Internet planes:
1. **HTTPS Discovery Plane:** `https://<namespace>/.well-known/agent.json` (or `https://<namespace>/.well-known/agent/<agent-name>.json` for multi-agent domains) serves the signed Creduent identity document (`agent.json`).
2. **DNS Binding Plane:** `_creduent.<namespace>` TXT records publish the authoritative Ed25519 public key binding (`v=creduent1; agent=...; k=ed25519:...`), providing an independent out-of-band check against compromised web servers.

---

## 4. CRUD Operations

### 4.1 Create (Register)
Creating a `did:creduent` identifier requires control over the target domain (`<namespace>`):
1. Generate an **Ed25519** cryptographic keypair.
2. Construct a valid `agent.json` identity document per CREDUENT-001 containing `agent_id`, `public_key` (`ed25519:<base64>`), `owner`, `capabilities`, and `service_endpoint`.
3. Canonicalize the document payload using **JCS (RFC 8785)** and compute the Ed25519 signature over the canonical bytes.
4. Publish the signed `agent.json` over HTTPS (`TLS 1.2+`) at `https://<namespace>/.well-known/agent.json` (or `/.well-known/agent/<agent-name>.json`).
5. Publish a DNS TXT record at `_creduent.<namespace>`:
   ```text
   v=creduent1; agent=creduent://<namespace>/<agent-name>; k=ed25519:<base64_public_key>
   ```

### 4.2 Read (Resolve)
Resolving a `did:creduent:<namespace>:<agent-name>` identifier to a W3C DID Document proceeds deterministically:
1. **Parse & Validate:** Verify the DID matches the ABNF grammar in Section 2. Extract `<namespace>` and `<agent-name>`.
2. **HTTPS Fetch (SSRF-Protected):** Fetch `https://<namespace>/.well-known/agent/<agent-name>.json` (falling back to `https://<namespace>/.well-known/agent.json`). Resolvers MUST reject private/loopback IP targets and enforce TLS certificate validation.
3. **Signature Verification:** Canonicalize the fetched `agent.json` (excluding `signature`) using JCS (RFC 8785) and verify the Ed25519 signature against the embedded `public_key`.
4. **DNS Cross-Verification:** Query DNS TXT records for `_creduent.<namespace>` and confirm the published public key matches the `public_key` in `agent.json`.
5. **DID Document Construction:** Transform the verified identity into a W3C DID Document:

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/ed25519-2020/v1"
  ],
  "id": "did:creduent:idevsec.com:steward",
  "alsoKnownAs": [
    "creduent://idevsec.com/steward"
  ],
  "verificationMethod": [
    {
      "id": "did:creduent:idevsec.com:steward#key-1",
      "type": "Ed25519VerificationKey2020",
      "controller": "did:creduent:idevsec.com:steward",
      "publicKeyMultibase": "z6Mkh..."
    }
  ],
  "authentication": [
    "did:creduent:idevsec.com:steward#key-1"
  ],
  "assertionMethod": [
    "did:creduent:idevsec.com:steward#key-1"
  ],
  "service": [
    {
      "id": "did:creduent:idevsec.com:steward#endpoint",
      "type": "AgentServiceEndpoint",
      "serviceEndpoint": "https://api.idevsec.com"
    }
  ]
}
```

### 4.3 Update
Updating a `did:creduent` DID Document (for key rotation or service endpoint changes) is performed by the domain controller:
1. Generate a new Ed25519 keypair (if rotating keys) or update fields in `agent.json`.
2. Increment the document timestamp (`updated_at`) and re-sign the JCS-canonicalized document with the active key.
3. Replace the `agent.json` file at the HTTPS `.well-known` endpoint.
4. Update the `_creduent.<namespace>` DNS TXT record with the new public key (`k=ed25519:...`) and remove any superseded TXT records.

### 4.4 Deactivate (Revoke)
A `did:creduent` identifier can be permanently deactivated by the domain controller via either or both mechanisms:
1. **Explicit Tombstone:** Update `agent.json` with `"status": "revoked"` and `"revoked_at"` signed by the controller key, causing compliant resolvers to return `deactivated: true` in `didDocumentMetadata`.
2. **Infrastructure Removal:** Remove the `.well-known` `agent.json` document (returning HTTP `410 Gone` or `404 Not Found`) and delete the corresponding `_creduent.<namespace>` DNS TXT record.

---

## 5. Security Considerations

1. **Web Server vs. DNS Compromise:** Requiring both HTTPS `.well-known/agent.json` and DNS TXT (`_creduent.<namespace>`) verification ensures an attacker who compromises only an origin web server (without DNS access) cannot forge valid agent keys. Domain owners SHOULD enable DNSSEC on `<namespace>`.
2. **Canonicalization Attacks:** All signatures MUST be computed over JCS (RFC 8785) canonical JSON output to prevent JSON key-reordering, whitespace, or Unicode normalization malleability.
3. **SSRF & Redirect Abuse:** Resolvers MUST block resolution of RFC 1918 private networks, link-local addresses (`169.254.0.0/16`), and loopback interfaces (`127.0.0.0/8`, `::1`), and MUST NOT follow cross-origin HTTP redirects without re-validating target hosts.
4. **Key Rotation & Stale DNS Records:** When DNS providers append rather than overwrite TXT records during automated provisioning (e.g., Domain Connect), domain owners MUST remove superseded `_creduent` TXT records immediately after rotation.
5. **Cryptographic Agility:** While Ed25519 is mandatory in v1/v2, `verificationMethod` types allow future post-quantum suites without changing the `did:creduent` syntax.

---

## 6. Privacy Considerations

1. **Public Institutional Identifiers:** `did:creduent` is designed for organizational and autonomous software agent identities rather than natural-person PII. Deployers MUST NOT embed personal names, email addresses, or sensitive operational secrets inside `agent-name`, `agent.json`, or DNS TXT records.
2. **Correlation:** Because `did:creduent` identifiers are bound to public DNS domains, interactions using the same DID across multiple services are correlatable to the controlling domain. Pairwise or ephemeral interactions SHOULD use attenuated Creduent Delegation Tokens (CDTs) rather than exposing long-lived root identities.
3. **Minimal Disclosure:** Resolvers SHOULD only fetch public `.well-known` metadata and MUST NOT transmit client credentials or tracking headers during DID resolution.

---

## 7. References

- **W3C Decentralized Identifiers (DIDs) v1.0:** https://www.w3.org/TR/did-core/
- **RFC 8785 (JSON Canonicalization Scheme):** https://www.rfc-editor.org/rfc/rfc8785
- **RFC 8615 (Well-Known URIs):** https://www.rfc-editor.org/rfc/rfc8615
- **CREDUENT-001 (`agent.json` Specification):** [CREDUENT-001-agent-json.md](CREDUENT-001-agent-json.md)
- **CREDUENT-004 (URI Resolution & W3C DID Mapping):** [CREDUENT-004-uri-resolution.md](CREDUENT-004-uri-resolution.md)

