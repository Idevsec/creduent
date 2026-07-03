# Creduent Protocol - Full Roadmap v1.1

This document outlines the development phases, adoption targets, and infrastructure path for the Creduent Protocol.

> [!NOTE]
> **Status:** Early Developer Preview / Public Beta (Active Development).
> In preparation for the launch on July 11, 2026, the core protocol components are in dynamic beta. We continuously refine the specifications, CLI, and SDKs based on community feedback, issues, and security reviews.

---

## Protocol Origins

Originally designed and developed by Kashish Kanojia through IDevSec, the Creduent Protocol reference registry, signing utilities, and SDKs were established to solve core agent identity challenges. The stewardship of the protocol and its future development roadmap are maintained by IDevSec. Under this model, the roadmap represents a collaborative effort among autonomous system developers, security practitioners, and open standards organizations.

---

## Phase 1 - Foundation - Complete
**Timeline:** May 2026
* [x] `agent.json` schema + Ed25519 + JCS signing standard
* [x] DNS TXT domain ownership verification
* [x] Attestation registry with signed attestations (Upstash Redis)
* [x] MCP server integration (`verify_agent` tool)
* [x] SSRF protection, rate limiting, and expiry enforcement
* [x] Vercel production deployment (`creduent.idevsec.com`)
* [x] v1.0 security hardening + full regression test suite

---

## Phase 2 - Ecosystem - Complete
**Goal:** Drop integration friction to zero. Make adoption a 3-minute decision.  
**Target:** 50 registered agents by end of August 2026.
* [x] **`pip install creduent`**: Python SDK with `sign()`, `verify()`, `register()`, and `attest()` as first-class methods.
* [x] **`agent://` URI public resolver**: Any client can resolve `agent://<namespace>/<name>` to a live `agent.json` without knowing the host domain.
* [x] **JavaScript/TypeScript SDK**: `npm install @idevsec/creduent` for MCP hosts running Node.
* [x] **Auto-renewal daemon**: Lightweight background process for agents to automatically re-attest 30 days before expiry.
* [x] **Webhook notifications**: POST notifications to a configured URL on registration, revocation, and expiry.
* [x] **Developer dashboard**: Web UI at `creduent.idevsec.com/dashboard` to manage registered agents, view attestation status, and rotate keys.
* [x] **GitHub Action**: `creduent-attest` action to register/re-attest automatically on every deploy.

---

## Phase 3 - Scale - Complete
**Goal:** Make Creduent the default trust layer in major agent frameworks.  
**Target:** 500 registered agents, 3 framework integrations.
* [x] **CrewAI integration**: Native `creduent_verify` step in Crew definitions.
* [x] **LangGraph integration**: Creduent verification node in graph pipelines.
* [x] **AutoGen integration**: Agent identity verification middleware.
* [x] **JavaScript integrations**: Native Vercel AI SDK tool wrapper and LangGraph JS node.
* [x] **Multi-key support**: Rotate signing keys without losing historical attestation data.
* [x] **Capability-level attestations**: Attest specific capabilities separately (e.g. `osint: verified`, `code_execution: unverified`).
* [x] **Agent discovery API**: `GET /agents?capability=osint` returns all verified agents exposing that capability.
* [x] **Organization namespaces**: `agent://<org_name>/*` namespaces owned and managed under one organizational account.
* [x] **Creduent CLI v2**: `creduent register`, `creduent verify`, `creduent revoke`, `creduent renew`, `creduent webhook`, and `creduent discover` packaged as a native command-line tool.
* [x] **CRD shorthand**: If the team wants something terse for technical contexts, introduce CRD as a short tag alongside Creduent (e.g., header X-CRD-Version), without renaming the protocol itself.
* [x] **Native Ed25519 JS SDK**: Zero-dependency cryptographic verification via `globalThis.crypto.subtle` and RFC 8785 JCS canonicalization — compatible with Vercel Edge, Cloudflare Workers, Deno, and Node.js 18+.
* [x] **CLI native verification**: `creduent verify` now performs local Ed25519 signature validation using the native SDK instead of querying the registry API.

---

## Phase 4 - Expansion & Hardening - July -> December 2026
**Goal:** Expand framework coverage, introduce local developer tooling, and harden core cryptography/revocation infrastructure.  
**Target:** 1,000+ registered agents, 5 framework integrations, security audit completed.
* [ ] **More Framework Integrations**: Native integrations for LlamaIndex, LangChain (Python & JS), Semantic Kernel, and Google ADK (Agent Development Kit).
* [ ] **Creduent Playground**: Interactive sandbox on the developer dashboard to cryptographically sign, verify, and debug `agent.json` files live in-browser.
* [ ] **Key Revocation & Cache Tuning**: Implement edge-native cached endpoints (Vercel/Cloudflare KV) and local SDK LRU cache hooks (5-min TTL) to protect registry origin under live check workloads.
* [x] **Short-Lived Attestation Windows**: Transition the default attestation TTL from 1 year to 30 days, supported by background SDK auto-renewal workers that refresh keys 7 days before expiry.
* [x] **DNS-Based Emergency Recovery Flow**: Build an out-of-band recovery path that bypasses compromised-key signatures by allowing owners to overwrite public keys via temporary DNS TXT records (`creduent-override:<hash>`).
* [x] **Multisig Admin Quorum**: Deprecate the symmetric `CREDUENT_ADMIN_KEY` for the `trusted` tier, replacing it with an asymmetric multisig threshold verification (e.g., 2-of-3 signatures from admin public keys).
* [ ] **HMAC Webhook Signatures**: Add HMAC-SHA256 signing headers (`X-Creduent-Signature256`) to the daemon’s alert notifications so endpoints can verify webhook authenticity.
* [x] **Schema Decoupling (v2.0)**: Release the v2.0 schema structure separating cryptographic identity (version, keys, owner) from transient policy declarations (endpoint, capabilities), introducing incremental version parsing to avoid breaking v1.x flat documents.
* [x] **Formal Security Audit**: Completed thorough cryptographic, SSRF, file permission, and dependency audit of the core registry, CLI, and SDKs (June 2026).
* [ ] **DID Interoperability**: Resolve `agent://` URIs as Decentralized Identifiers (e.g., standardizing `did:creduent` or integrating with `did:web`).
* [ ] **Identity-Based Rate Limiting (IBRL)**: Standardize and implement middleware that rate-limits and blocks request flows by verified `agent_id` (rather than transient IPs), preventing rapid API scanning/probing.

---

## Phase 5 - Cryptographic Delegation & Gateway Integration - January -> June 2027
**Goal:** Build verifiable provenance and delegation capabilities directly solving the inter-agent security boundaries.  
**Target:** 3 gateway integrations, 5,000+ registered agents, 1 enterprise POC.
* [ ] **Creduent Delegation Token (CDT) Specification (CREDUENT-006)**: Draft the formal specification defining attenuated capability delegation payload structure.
* [ ] **Verifiable Audit Logging Standard**: Draft specification for linking agent-to-agent call chains and identities into cryptographically signed trace logs, enabling machine-speed correlation for compliance audits.
* [ ] **Intent-to-Action Cryptographic Binding**: Bind delegation policies (CDT) directly to historical execution trace hashes, enabling downstream gateways to verify that the agent's behavior did not deviate from its authorized intent.
* [ ] **Instruction & Prompt Integrity Attestation (CREDUENT-007)**: Draft specification for hashing and cryptographically signing active system prompts, model versions, and tool boundaries to prevent mid-session prompt hijacking.
* [ ] **Confidential Computing & TPM Attestation**: Design registry workflows to verify virtual Trusted Platform Module (vTPM) quotes and Intel SGX/AWS Nitro enclave measurements, introducing a "Hardware-Attested" trust level.
* [ ] **SDK Cryptographic Delegation Verification**: Implement recursive client-side delegation verification (`sign_delegation` and `verify_delegation_chain`) in both JS/TS and Python SDKs.
* [ ] **Zero-Trust Gateway Integration**: Implement reference middlewares for LLM Gateways (Bifrost, CyberArk) and MCP Gateways to dynamically scope API keys and policies based on CDTs.
* [ ] **Federated attestation**: Support third-party attesters (e.g., security auditors, compliance bodies, LLM providers) issuing custom attestations.
* [ ] **Cross-registry trust**: Multiple registries recognize each other's attestations.
* [ ] **Formal RFC**: Submit CREDUENT-001/006 as formal open RFCs to the IETF or equivalent standard bodies.
* [ ] **Enterprise registry**: Private hosted Creduent registry for internal enterprise agent fleets (SOC2 compliant).
* [ ] **`agent://` IANA registration**: Formal IANA registration of the `agent://` URI scheme.
* [ ] **MCP marketplace integration**: Verification requirement integration with major MCP marketplaces.

---

## Phase 6 - Infrastructure - 2027 and beyond
**Goal:** Creduent is to agents what TLS is to HTTPS, invisible, universal, assumed.
* [ ] Creduent becomes a standard requirement in enterprise AI procurement checklists.
* [ ] **Cyber Insurance Compliance Standard**: Partner with security underwriters to validate compliance boundaries, reducing liability premiums for Creduent-certified agent deployments.
* [ ] LLM providers (Anthropic, OpenAI, Google) reference Creduent in their agent hosting documentation.
* [ ] **Cross-chain attestation bridges**: On-chain verifiable agent identity for Web3/decentralized agent ecosystems.
* [ ] **Community Stewardship**: Establish an independent governance body, open membership, and transition protocol stewardship from IDevSec to the community.