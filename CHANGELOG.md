# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- CORS: updated `Access-Control-Allow-Origin` in `vercel.json` from `https://api.idevsec.com` to `*` for broader client compatibility.

## [1.0.2] - 2026-06-08

### Added
- Outbound IPv6 SSRF bypass protection checking all resolved IPv4 and IPv6 addresses.
- In-memory challenge store pruning fallback to prevent memory leaks.
- CSS classes, variables, and styling support for the `trusted` attestation level badge.

### Changed
- Standardized the specifications (`CREDUENT-002`, `CREDUENT-003`) to define JCS-canonicalized signature payloads as the modern standard format and pipe-delimited strings as deprecated fallback.
- Standardized the specifications to clearly separate **Trust Level** (unverified, verified, trusted, revoked) and **Lifecycle Status** (active, expiring, expired, revoked).
- Updated the registry reference implementation (`registry/main.py`) to correctly computed attestation status and map them to standard levels.
