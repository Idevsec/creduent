# Creduent Protocol — Full Roadmap v1.1

This document outlines the development phases, adoption targets, and infrastructure path for the Creduent Protocol.

---

## Phase 1 — Foundation ✅ Complete
**Timeline:** May 2026
* [x] `agent.json` schema + Ed25519 + JCS signing standard
* [x] DNS TXT domain ownership verification
* [x] Attestation registry with signed attestations (Upstash Redis)
* [x] MCP server integration (`verify_agent` tool)
* [x] SSRF protection, rate limiting, and expiry enforcement
* [x] Vercel production deployment (`api.idevsec.com`)
* [x] v1.0 security hardening + full regression test suite

---

## Phase 2 — Ecosystem 🔵 Now → August 2026
**Goal:** Drop integration friction to zero. Make adoption a 3-minute decision.  
**Target:** 50 registered agents by end of August 2026.
* [ ] **`pip install creduent`**: Python SDK with `sign()`, `verify()`, `register()`, and `attest()` as first-class methods.
* [ ] **`agent://` URI public resolver**: Any client can resolve `agent://<namespace>/<name>` to a live `agent.json` without knowing the host domain.
* [ ] **JavaScript/TypeScript SDK**: `npm install creduent-protocol` for MCP hosts running Node.
* [ ] **Auto-renewal daemon**: Lightweight background process for agents to automatically re-attest 30 days before expiry.
* [ ] **Webhook notifications**: POST notifications to a configured URL on registration, revocation, and expiry.
* [ ] **Developer dashboard**: Web UI at `api.idevsec.com/dashboard` to manage registered agents, view attestation status, and rotate keys.
* [ ] **GitHub Action**: `creduent-attest` action to register/re-attest automatically on every deploy.

---

## Phase 3 — Scale 🟡 September → December 2026
**Goal:** Make Creduent the default trust layer in major agent frameworks.  
**Target:** 500 registered agents, 3 framework integrations.
* [ ] **CrewAI integration**: Native `creduent_verify` step in Crew definitions.
* [ ] **LangGraph integration**: Creduent verification node in graph pipelines.
* [ ] **AutoGen integration**: Agent identity verification middleware.
* [ ] **Multi-key support**: Rotate signing keys without losing historical attestation data.
* [ ] **Capability-level attestations**: Attest specific capabilities separately (e.g. `osint: verified`, `code_execution: unverified`).
* [ ] **Agent discovery API**: `GET /agents?capability=osint` returns all verified agents exposing that capability.
* [ ] **Organization namespaces**: `agent://<org_name>/*` namespaces owned and managed under one organizational account.
* [ ] **Creduent CLI v2**: `creduent register`, `creduent verify`, `creduent revoke` packaged as a native command-line tool.

---

## Phase 4 — Standard 🔴 January → June 2027
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

## Phase 5 — Infrastructure 🌐 2027 and beyond
**Goal:** Creduent is to agents what TLS is to HTTPS — invisible, universal, assumed.
* [ ] Creduent becomes a standard requirement in enterprise AI procurement checklists.
* [ ] LLM providers (Anthropic, OpenAI, Google) reference Creduent in their agent hosting documentation.
* [ ] **Cross-chain attestation bridges**: On-chain verifiable agent identity for Web3/decentralized agent ecosystems.
* [ ] **Creduent Foundation**: Establish an independent governance body, open membership, and transfer protocol stewardship from IDevSec to the community.

---

## The Number That Matters

| Milestone | Agents | What it proves |
| :--- | :--- | :--- |
| **Today** | 1 | Protocol works |
| **August 2026** | 50 | Developers will adopt |
| **December 2026** | 500 | Frameworks will integrate |
| **June 2027** | 5,000 | Standard in the making |
| **2028+** | 50,000+ | Infrastructure |
