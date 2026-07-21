# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.10] - 2026-07-21

### Added
- **CREDUENT-007 (Delegation Token)**: Drafted the formal Creduent Delegation Token (CDT) specification (`standards/CREDUENT-007-delegation.md`). Defined the attenuated capability delegation payload structure, fields schema, and recursive delegation chain verification guidelines.

### Changed
- **Specifications Alignment**: Aligned sitemap, FAQ, index (`standards/README.md`), and main README files to cover standard specs `CREDUENT-001` through `CREDUENT-007`.

## [2.0.9] - 2026-07-20

### Added
- **HMAC Webhook Signatures**: Added HMAC-SHA256 signing headers (`X-Creduent-Signature256` and `X-Creduent-Timestamp`) to the attestation registry alert webhooks. Updated specs `CREDUENT-002` and `CREDUENT-003` to document payload signing over JCS canonical body concatenated with timestamp.
- **Registry Webhook Config Storage**: Upgraded `/webhook/register` response to yield hex-encoded pre-shared secret keys (`whsec_...`) and persist webhook metadata as nested JSON configurations in Upstash Redis. Added Legacy Webhook HMAC derivation fallback to preserve backwards compatibility for existing webhooks.

## [2.0.8] - 2026-07-13

### Changed
- **CREDUENT-006 (Dynamic Attestation)**: Merged PR #8 (resolves Issue #6) by @Mayur021. Added action reversibility class specifications (read-only, reversible, external-reversible, and irreversible) based on OWASP AISVS v1.0 (C9.2.3). Implemented dual-gate verification (build-time manifest schema gate and runtime proxy safety gate), Merkle chain worst-case logic, and compliance test vectors.

## [2.0.7] - 2026-07-10

### Changed
- **ROADMAP accuracy**: Corrected the Phase 2 GitHub Action entry from `creduent-attest` (implies a standalone marketplace action) to `GitHub Actions Workflow`, accurately reflecting the actual deliverable: a reference CI workflow that calls the Python SDK inline. Pointer added to `EXAMPLES.md` Example 15.

## [2.0.6] - 2026-07-09

### Changed
- **Capability Refinement:** Renamed and consolidated capability names in `api/index.py` and `api/services.py` from `osint`, `dns_lookup`, and `vulnerability_scan` to `scan` and `query` to match the frontend and specifications.
- **Removed Legacy Features:** Completely dropped the legacy `osint` capability logic and all references to banned legacy scanner terms.
- **Creator and Steward Realignment:** Standardized all documentation (`AUTHORS.md`, `README.md`, `SPEC.md`, `ROADMAP.md`, tool manuals) to clearly designate Kashish Kanojia as Creator/Original Author and IDevSec as Steward.

## [2.0.5] - 2026-07-08

### Added
- **DNS Recovery Override Endpoint:** Added the `/recovery/override` API route in the reference registry implementation for out-of-band key rotation overrides.

### Fixed
- **Version 2.0/1.1 Schema Key Array Validation:** Fixed registration pipeline to correctly extract active public keys from keys arrays in version 2.0 (nested `identity.keys`) and version 1.1 (top-level `keys`) agent documents.

## [2.0.4] - 2026-07-05

### Changed
- **Documentation & Examples:** Updated the canonical example agent identity in all documentation and docstrings. Replaced the `reconbot` test agent with `agent://idevsec/steward` to align with the authoritative registry.

## [2.0.2] - 2026-06-27

### Changed
- **Unified Domain Name Migration:** Standardized default registry URL on `creduent.idevsec.com` across all configuration files, templates, specifications, and reference registry endpoints.

## [2.0.1] - 2026-06-27

### Added
- **Decoupled Scanning Services:** Decoupled agent scan capability checks (DNS, OSINT headers, clickjacking/HSTS rules) from API endpoints in `index.py` into a modular `services.py` layer.

### Fixed
- **Fail-Closed Date Parsing:** Hardened attestation timestamp check inside `get_attest` route to default `expired = True` upon parsing exceptions.
- **Serverless Rate Limiting Guard:** Implemented explicit validation raising an `HTTP 500` error if Upstash Redis credentials are not configured when running in Vercel serverless contexts.
- **Unified Canonicalization:** Removed direct `jcs` module imports and standardized all cryptographic dictionary serialization on the project's canonical JCS wrapper.

## [2.0.0] - 2026-06-23

### Added
- **v2.0 Schema Split Support**: Added dynamic parsing and version-gating for the v2.0 schema structure separating `identity`, `policy`, and `signature` blocks.
- **DNS Recovery Override Endpoint**: Implemented the `/recovery/override` route for out-of-band identity recovery using DNS TXT record checks.
- **Multisig Quorum Authorization**: Implemented threshold signature verification over administrative routes utilizing multiple admin public keys in `CREDUENT_ADMIN_KEYS`.
- **Database Expiry Migration Script**: Included `migrate_attestations.py` to cap existing active expirations to 30 days.

### Changed
- **Attestation Expiration Window**: Shortened default attestation TTL from 365 days to 30 days, enforcing the 30-day cap on all new registrations and renewals.
- **Keys Array Extraction**: Enabled fallback lookup from the `keys` array in `agent.json` when the root-level `public_key` is not present.
- **Distinct Revocation Status Response**: Configured `/attest/{agent_id}` to yield `HTTP 410 Gone` if the attestation is revoked.

## [1.2.0] - 2026-06-21

### Added
- **Attestation Renewal**: Added `creduent renew` command to the CLI and native `renew` methods to the Node.js and Python SDKs.
- **Webhook Management**: Added `creduent webhook register` and `creduent webhook query` commands to the CLI, alongside `register_webhook` and `query_webhook` SDK methods.
- **Feature Parity**: Full parity of `discover`, `renew`, and `webhook` commands between Node.js and Python implementations.
- **Framework Integrations**: Web/SDK documentation updated with Vercel AI SDK and LangGraph JS integration guides.

## [1.1.0] - 2026-06-19

### Added
- **Multi-key Support**: Support for rotating signing keys via `keys` array in `agent.json` without losing historical attestation data.
- **Capability-level Attestations**: Support for `capabilities` defined as complex objects (`name` and `schema` properties).
- **Organization Namespaces**: Namespace validation allowing organizations to claim `agent://<org_name>/*` scopes.
- **Discovery API**: Native `discover()` API with support for authenticated, private capability sharing.
- **Creduent CLI v2**: Revamped CLI with `init`, `keygen`, `build`, and `discover` tools.
- **CRD Shorthand**: Support for declarative Kubernetes-style `agent.yaml` for generating `agent.json` documents.
- **Integrations**: Native verification tools/nodes for CrewAI, LangGraph, and AutoGen in `creduent.integrations`.

## [1.0.4] - 2026-06-13

### Changed
- Migrated default registry URL from `api.idevsec.com` to `creduent.idevsec.com`.

## [1.0.3] - 2026-06-11

### Added
- Premium agent info card header (favicon, agent name, domain, attestation badge) to **Level**, **Renew**, and **Revoke** modals, consistent with the View modal design.
- `populateModalCard(prefix, agent)` JavaScript helper for instant modal population from the local `window.loadedAgents` cache — no extra network round-trip.
- Responsive mobile card stack layout replacing the data table on small viewports, with async favicon rendering, level badges, and touch-optimised action buttons.

### Changed
- Removed plain `Agent ID` display input fields from Level, Renew, and Revoke modals; replaced by the premium agent info card.
- Register Agent, Webhook Manager, and Refresh toolbar buttons are now forced onto a single row (`flex-wrap: nowrap`, `white-space: nowrap`) to prevent unintended wrapping.
- `showRenewModal()`, `showUpgradeModal()`, and `showRevokeModal()` functions updated to call `populateModalCard()` and drop stale references to deleted display inputs.
- CORS: set `allow_credentials=False` in `api/index.py` to comply with wildcard origin restriction.
- CORS: updated `Access-Control-Allow-Origin` in `vercel.json` from `https://creduent.idevsec.com` to `*` for broader client compatibility.

## [1.0.2] - 2026-06-08

### Added
- Outbound IPv6 SSRF bypass protection checking all resolved IPv4 and IPv6 addresses.
- In-memory challenge store pruning fallback to prevent memory leaks.
- CSS classes, variables, and styling support for the `trusted` attestation level badge.

### Changed
- Standardized the specifications (`CREDUENT-002`, `CREDUENT-003`) to define JCS-canonicalized signature payloads as the modern standard format and pipe-delimited strings as deprecated fallback.
- Standardized the specifications to clearly separate **Trust Level** (unverified, verified, trusted, revoked) and **Lifecycle Status** (active, expiring, expired, revoked).
- Updated the registry reference implementation (`registry/main.py`) to correctly computed attestation status and map them to standard levels.
