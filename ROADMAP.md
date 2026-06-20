# Creduent Protocol - Full Roadmap v1.1

This document outlines the development phases, adoption targets, and infrastructure path for the Creduent Protocol.

---

## Protocol Origins

Originally designed and developed by Kashish Kanojia through IDevSec, the Creduent Protocol reference registry, signing utilities, and SDKs were established to solve core agent identity challenges. The stewardship of the protocol and its future development roadmap are maintained by IDevSec. Under this model, the roadmap represents a collaborative effort among autonomous system developers, security practitioners, and open standards organizations.

---

## Phase 1 - Foundation ✅ Complete
**Timeline:** May 2026
* [x] `agent.json` schema + Ed25519 + JCS signing standard
* [x] DNS TXT domain ownership verification
* [x] Attestation registry with signed attestations (Upstash Redis)
* [x] MCP server integration (`verify_agent` tool)
* [x] SSRF protection, rate limiting, and expiry enforcement
* [x] Vercel production deployment (`registry.idevsec.com`)
* [x] v1.0 security hardening + full regression test suite

---

## Phase 2 - Ecosystem ✅ Complete
**Goal:** Drop integration friction to zero. Make adoption a 3-minute decision.  
**Target:** 50 registered agents by end of August 2026.
* [x] **`pip install creduent`**: Python SDK with `sign()`, `verify()`, `register()`, and `attest()` as first-class methods.
* [x] **`agent://` URI public resolver**: Any client can resolve `agent://<namespace>/<name>` to a live `agent.json` without knowing the host domain.
* [x] **JavaScript/TypeScript SDK**: `npm install @idevsec/creduent` for MCP hosts running Node.
* [x] **Auto-renewal daemon**: Lightweight background process for agents to automatically re-attest 30 days before expiry.
* [x] **Webhook notifications**: POST notifications to a configured URL on registration, revocation, and expiry.
* [x] **Developer dashboard**: Web UI at `registry.idevsec.com/dashboard` to manage registered agents, view attestation status, and rotate keys.
* [x] **GitHub Action**: `creduent-attest` action to register/re-attest automatically on every deploy.

---

## Phase 3 - Scale ✅ Complete
**Goal:** Make Creduent the default trust layer in major agent frameworks.  
**Target:** 500 registered agents, 3 framework integrations.
* [x] **CrewAI integration**: Native `creduent_verify` step in Crew definitions.
* [x] **LangGraph integration**: Creduent verification node in graph pipelines.
* [x] **AutoGen integration**: Agent identity verification middleware.
* [x] **Multi-key support**: Rotate signing keys without losing historical attestation data.
* [x] **Capability-level attestations**: Attest specific capabilities separately (e.g. `osint: verified`, `code_execution: unverified`).
* [x] **Agent discovery API**: `GET /agents?capability=osint` returns all verified agents exposing that capability.
* [x] **Organization namespaces**: `agent://<org_name>/*` namespaces owned and managed under one organizational account.
* [x] **Creduent CLI v2**: `creduent register`, `creduent verify`, `creduent revoke` packaged as a native command-line tool.
* [x] **CRD shorthand**: If the team wants something terse for technical contexts, introduce CRD as a short tag alongside Creduent (e.g., header X-CRD-Version), without renaming the protocol itself.
* [x] **Native Ed25519 JS SDK**: Zero-dependency cryptographic verification via `globalThis.crypto.subtle` and RFC 8785 JCS canonicalization — compatible with Vercel Edge, Cloudflare Workers, Deno, and Node.js 18+.
* [x] **CLI native verification**: `creduent verify` now performs local Ed25519 signature validation using the native SDK instead of querying the registry API.

---

## Phase 4 - Standard 🔴 January -> June 2027
**Goal:** Creduent becomes the RFC. Establishing universal infrastructure.  
**Target:** RFC submitted, 5,000+ registered agents, 1 enterprise customer.
* [ ] **Federated attestation**: Support third-party attesters (e.g., security auditors, compliance bodies, LLM providers) issuing custom attestations.
* [ ] **Cross-registry trust**: Multiple registries recognize each other's attestations.
* [ ] **Formal RFC**: Submit CREDUENT-001 as a formal open RFC to the IETF or equivalent standard bodies.
* [ ] **Creduent Verification Badge**: Embeddable trust badge for agent dashboards and landing pages.
* [ ] **Enterprise registry**: Private hosted Creduent registry for internal enterprise agent fleets (SOC2 compliant).
* [ ] **`agent://` IANA registration**: Formal IANA registration of the `agent://` URI scheme.
* [ ] **MCP marketplace integration**: Verification requirement integration with major MCP marketplaces.

---

## Phase 5 - Infrastructure 🌐 2027 and beyond
**Goal:** Creduent is to agents what TLS is to HTTPS, invisible, universal, assumed.
* [ ] Creduent becomes a standard requirement in enterprise AI procurement checklists.
* [ ] LLM providers (Anthropic, OpenAI, Google) reference Creduent in their agent hosting documentation.
* [ ] **Cross-chain attestation bridges**: On-chain verifiable agent identity for Web3/decentralized agent ecosystems.
* [ ] **Community Stewardship**: Establish an independent governance body, open membership, and transition protocol stewardship from IDevSec to the community.

---

## The Number That Matters

| Milestone | Agents | What it proves |
| :--- | :--- | :--- |
| **Today** | 1+ | Protocol works, ecosystem live |
| **August 2026** | 50 | Developers will adopt |
| **December 2026** | 500 | Frameworks will integrate |
| **June 2027** | 5,000 | Standard in the making |
| **2028+** | 50,000+ | Infrastructure |