# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2026-06-08

### Added
- Outbound IPv6 SSRF bypass protection checking all resolved IPv4 and IPv6 addresses.
- In-memory challenge store pruning fallback to prevent memory leaks.
- CSS classes, variables, and styling support for the `trusted` attestation level badge.

### Changed
- Standardized the specifications (`CREDUENT-002`, `CREDUENT-003`) to define JCS-canonicalized signature payloads as the modern standard format and pipe-delimited strings as deprecated fallback.
- Standardized the specifications to clearly separate **Trust Level** (unverified, verified, trusted, revoked) and **Lifecycle Status** (active, expiring, expired, revoked).
- Updated the registry reference implementation (`registry/main.py`) to correctly computed attestation status and map them to standard levels.
