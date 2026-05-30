# Creduent Protocol: Governance Model

**Status:** Active  
**Version:** 1.0  
**Maintained by:** Creduent Foundation  
**Last Updated:** 2026-05-30  

---

## 1. Purpose

This document defines the governance model for the Creduent Protocol, an open application-layer standard for cryptographic identity, verification, and federated attestation of autonomous AI agents.

The governance model exists to ensure that:
- Protocol evolution is open, transparent, and community-driven.
- Backward compatibility is preserved across versions.
- No single entity controls the standard unilaterally.
- Contributions from implementers, researchers, and operators are structurally welcomed.

---

## 2. Principles

1. **Openness:** All protocol proposals, discussions, and decisions are conducted publicly.
2. **Consensus:** Changes require broad agreement across stakeholder roles before adoption.
3. **Stability:** Breaking changes to the protocol core require a full Working Group vote and a minimum 90-day notice period.
4. **Separation of Concerns:** Protocol governance is distinct from the governance of any specific implementation (e.g., the reference registry at `api.idevsec.com`).
5. **Meritocracy:** Influence is earned through documented contributions, not organizational affiliation.

---

## 3. Roles

### 3.1 Foundation Steward

**Appointed by:** Creduent Foundation Board  
**Seats:** 3 (rotating annually)

Foundation Stewards hold ultimate responsibility for the protocol's direction, legal status, and long-term neutrality. They:
- Hold the final veto on any change that would compromise backward compatibility.
- Approve new Working Groups and dissolve inactive ones.
- Manage the Creduent trademark and licensing.
- Represent the protocol to external bodies (IETF, IANA, standards organizations).

### 3.2 Maintainer

**Appointed by:** Foundation Stewards, confirmed by Working Group vote  
**Minimum:** 2 active Maintainers required at all times

Maintainers are responsible for the day-to-day health of the protocol repositories. They:
- Merge pull requests after Reviewer approval.
- Triage incoming issues and proposals.
- Publish official releases.
- May reject proposals that violate backward compatibility without Working Group review.
- Serve a 12-month renewable term.

**Current Maintainers:**
- See [FOUNDATION.md](FOUNDATION.md) for the current maintainer list.

### 3.3 Reviewer

**Self-nominated or nominated by a Maintainer**  
**Confirmed by:** Existing Reviewers (simple majority)

Reviewers are subject-matter experts who evaluate specific proposals against technical correctness, security implications, and ecosystem impact. They:
- Review and approve/reject Creduent Improvement Proposals (CIPs) in their area of expertise.
- Do not have merge access to protocol repositories.
- May serve indefinitely as long as they review at least one proposal per quarter.

**Reviewer areas:**
- Cryptography & Signing
- Registry & Attestation
- DNS & URI Resolution
- SDK & Tooling
- Federation & Cross-Registry

### 3.4 Working Group Member

**Self-nominated via public GitHub issue**  
**Confirmed by:** A Maintainer

Working Group Members participate in the proposal and review process. They:
- Propose, comment on, and vote on Creduent Improvement Proposals (CIPs).
- Are expected to participate in at least one Working Group session per quarter.
- May be removed for prolonged inactivity (6+ months without participation).

**There is no organizational requirement.** Individual developers, researchers, and operators are equally eligible.

---

## 4. Decision Making

### 4.1 Consensus Model

All protocol changes follow a **lazy consensus** model:
- A proposal is assumed to pass if no Maintainer or Reviewer objects within the defined comment period.
- Objections must be technical, not procedural. "I don't like it" is not a blocking objection.
- Any Working Group Member may request a formal vote if consensus cannot be reached.

### 4.2 Voting

| Change Type | Required Approval |
|:---|:---|
| Editorial (typos, clarifications) | 1 Maintainer |
| Non-breaking protocol additions | 2 Reviewers + 1 Maintainer |
| New standards track document | Working Group majority + 2 Maintainers |
| Breaking protocol change | Foundation Steward vote (unanimous) + 90-day notice |
| Governance changes | Foundation Stewards + Working Group supermajority (2/3) |

Votes are conducted via GitHub issues or designated discussion threads. Each vote remains open for **14 days** unless urgency is declared by a Foundation Steward (minimum 72 hours).

---

## 5. Creduent Improvement Proposal (CIP) Process

All significant changes to the protocol MUST go through the CIP process.

### 5.1 Lifecycle

```
Draft → Review → Last Call → Accepted / Rejected → Active / Superseded
```

| Stage | Description | Duration |
|:---|:---|:---|
| **Draft** | Author publishes a CIP as a GitHub issue or PR. | Open-ended |
| **Review** | Reviewers and Working Group Members comment. At least 2 Reviewers must be assigned. | Minimum 14 days |
| **Last Call** | Maintainer announces no further objections are pending. | 7 days |
| **Accepted** | CIP is merged and scheduled for the next minor release. | N/A |
| **Active** | CIP is published in the standards track. | Ongoing |
| **Superseded** | A later CIP replaces this one. Original is kept for reference. | N/A |

### 5.2 CIP Template

Each CIP must include:

```markdown
# CIP-<number>: <Title>

**Status:** Draft | Review | Last Call | Accepted | Rejected | Active | Superseded
**Category:** Core | Registry | SDK | Governance | Informational
**Author(s):** <name(s)>
**Created:** <YYYY-MM-DD>
**Requires:** <CIP numbers if any>
**Replaces:** <CIP number if any>

## Summary
One-paragraph abstract.

## Motivation
Why is this change needed? What problem does it solve?

## Specification
Precise technical description of the proposed change.

## Backward Compatibility
Does this break existing implementations? If yes, how is migration handled?

## Security Considerations
Does this change affect the security model?

## Reference Implementation
Link to a reference implementation (optional for Draft, required for Last Call).

## Rejected Alternatives
What else was considered and why was it not chosen?
```

---

## 6. Versioning

The Creduent Protocol uses semantic versioning (`MAJOR.MINOR`):

- **MINOR version bump:** New fields, new optional behaviors, or new endpoints that do not break existing implementations.
- **MAJOR version bump:** Any change that requires existing implementations to update to remain compliant. Requires unanimous Foundation Steward approval and 90-day migration notice.

The `version` field in `agent.json` documents corresponds to the MAJOR protocol version. A v1.0 registry MUST continue to accept v1.0 `agent.json` documents indefinitely until a formal deprecation notice is issued.

---

## 7. Security Disclosure

Security vulnerabilities in the protocol specification or reference implementations must be disclosed responsibly:

1. **Do not open a public GitHub issue for security vulnerabilities.**
2. Email `security@creduent.org` with a description of the vulnerability.
3. Include steps to reproduce and potential impact.
4. Maintainers will acknowledge receipt within 48 hours and provide a resolution timeline.
5. Public disclosure will occur within 90 days, coordinated with the reporter.

---

## 8. Code of Conduct

All participants in the Creduent governance process are expected to follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Violations may be reported to `conduct@creduent.org`.

---

## 9. Amendment Process

This document itself may be amended following the same CIP process described in Section 5, requiring Working Group supermajority and Foundation Steward approval.

---

*For the current list of Maintainers, Stewards, and active Working Groups, see [FOUNDATION.md](FOUNDATION.md).*
