# Security Policy

We take the security of the Creduent Open Protocol and its reference implementations very seriously. Creduent is a cryptographic credential protocol. Any vulnerabilities in its core design or implementations could have significant trust and security implications.

---

## Supported Versions

Only the latest release of the Creduent Protocol specification and reference implementation is actively supported with security patches.

| Version | Supported |
| ------- | --------- |
| 2.x     | Yes       |
| 1.x     | Limited   |
| < 1.0.0 | No        |

---

## Security Guarantees & Protocol Integrity

The Creduent Protocol implements strict cryptographic safety measures:

- **Ed25519 Signatures:** All credential signing and verification uses Ed25519 keypairs for strong, modern elliptic-curve cryptography.
- **Canonicalization:** All payloads are serialized using RFC 8785 JSON Canonicalization Scheme (JCS) before signing, preventing canonicalization attacks.
- **Decentralized Verification:** The verification process works locally without trusting a remote server's assertion, preventing MITM credential spoofing.
- **Key Isolation:** Private keys are never transmitted over the network and are handled exclusively on the credential issuer's machine.

---

## Reporting a Vulnerability

If you discover a security vulnerability in the Creduent Protocol specification, reference registry, or any official implementation, please report it responsibly using our **private vulnerability reporting** channel:

1. **Do NOT** open a public GitHub Issue detailing the vulnerability.
2. Use GitHub's **private vulnerability reporting** feature on this repository (Security tab > Report a vulnerability).
3. Alternatively, email your findings and a proof-of-concept (PoC) directly to: `security@idevsec.com`
4. Allow the maintainers reasonable time to analyze, reproduce, and release a coordinated patch before any public disclosure.

We aim to acknowledge all vulnerability reports within **48 hours** and provide a resolution timeline within **7 days**.
