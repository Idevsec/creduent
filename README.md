# Creduent: Open Standard for AI Agent Identity & Trust

[![Protocol Version](https://img.shields.io/badge/protocol-v2.0.0-cyan)](https://idevsec.com/creduent)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](https://idevsec.com/creduent/licensing)
[![Registry](https://img.shields.io/badge/registry-live-brightgreen)](https://creduent.idevsec.com)
[![Python SDK](https://img.shields.io/pypi/v/creduent.svg?label=pip%20install%20creduent&color=blue)](https://pypi.org/project/creduent/)
[![JS SDK](https://img.shields.io/npm/v/@idevsec/creduent.svg?label=npm%20install%20%40idevsec%2Fcreduent&color=blue)](https://www.npmjs.com/package/@idevsec/creduent)

**Creduent** is the open standard for cryptographic identity and trust verification of autonomous AI agents.
It defines how agents publish signed identity documents (`agent.json`), bind them to internet domains via DNS TXT records, and register with a public attestation registry.

Originated and stewarded by [IDevSec](https://idevsec.com). Open source under Apache 2.0.

- **Protocol overview**: [idevsec.com/creduent](https://idevsec.com/creduent)
- **Technical docs**: [idevsec.com/creduent/docs](https://idevsec.com/creduent/docs)
- **Reference registry**: [creduent.idevsec.com](https://creduent.idevsec.com)
- **Licensing**: [idevsec.com/creduent/licensing](https://idevsec.com/creduent/licensing)

> **GitHub Topics**: `ai-agent` `agent-identity` `ed25519` `open-standard` `mcp` `attestation` `agent-trust` `cryptographic-signing` `dns-verification` `autonomous-agent`

## The Problem

Autonomous agents lack a native, decentralized mechanism to verify their identities, ownership, and endpoint capabilities. Traditional web security relies on human-centric authentication systems. Without a machine-readable protocol-native trust infrastructure, automated machine-to-machine interactions are vulnerable to identity spoofing, unauthorized access, and lack of capability discovery.

## How It Works

```
+------------------+             +----------------------+             +------------------+
|   Agent Domain   |             |   Creduent Registry  |             |   Agent Client   |
|   (agent.json)   |             |                      |             |    (MCP Host)    |
+------------------+             +----------------------+             +------------------+
         |                                |                                |
         |---- 1. Serve agent.json ------>|                                |
         |                                |-- 2. Verify identity & DNS --->|
         |                                |      and sign attestation      |
         |                                |                                |
         |<--- 3. Query agent endpoint ------------------------------------|  (verify_agent tool)
         |                                |                                |
         |                                |<--- 4. Fetch attestation ------|  (registry validation)
```

## The agent.json Document

Every agent publishes its cryptographic identity at `https://<domain>/.well-known/agent.json`. The document contains 8 fields:

```json
{
  "version": "1.0",
  "issued_at": "2026-05-27T02:41:21Z",
  "agent_id": "agent://example/agent",
  "owner": "Example Corp",
  "public_key": "ed25519:hArTvbITJ2jirL170IOSjcVvEvstC4s+RjYLu4chCwg=",
  "endpoint": "https://api.example.com/assistant",
  "capabilities": ["scan", "query"],
  "signature": "base64_signature_here"
}
```

## Quickstart

### 1. Generate Keys & Sign agent.json
Use the signing CLI to generate keypairs and sign your draft identity payload using RFC 8785 JSON Canonicalization Scheme (JCS) and Ed25519:
```bash
python cli/creduent-sign.py generate-keys
python cli/creduent-sign.py sign --key private_key.pem --input examples/draft_agent.json --output agent.json
```

### 2. Expose Metadata and Configure DNS
Host `agent.json` on your web server at `https://<domain>/.well-known/agent.json`. Then, publish a DNS TXT record under your domain to bind the domain identity to the agent ID:
```
_creduent.example.com TXT "agent://example/agent"
```

### 3. Register with Creduent Registry
Submit your agent's registration to the registry:
```bash
curl -X POST https://creduent.idevsec.com/register \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "agent://example/agent", "domain": "example.com", "agent_json_url": "https://example.com/.well-known/agent.json"}'
```

## SDKs & Tooling

### Python SDK
```bash
pip install creduent
```

### JavaScript / TypeScript SDK
```bash
npm install @idevsec/creduent
```

### CLI Tool
```bash
npm install -g @idevsec/creduent-cli
```

## MCP Integration

Creduent exposes a Model Context Protocol (MCP) server with the `verify_agent` tool to enable verification in agent hosts. Configure it in your MCP settings:

```json
{
  "mcpServers": {
    "creduent": {
      "command": "python",
      "args": ["/path/to/creduent/mcp/creduent_mcp_server.py"],
      "env": {
        "CREDUENT_REGISTRY_URL": "https://creduent.idevsec.com"
      }
    }
  }
}
```

Call `verify_agent` with target agent ID or domain to receive structural, cryptographic signature, and registry-attested status.

## Agent Framework Integrations

Creduent provides native verification tools and classes for the leading AI agent frameworks:

- **CrewAI**: Import `CreduentVerifyTool` from `creduent.integrations.crewai` to verify external agents within your Crew definitions dynamically.
- **LangGraph**: Add the `verify_agent_node` node function from `creduent.integrations.langgraph` to your state graph to validate agent identities before executing next nodes.
- **AutoGen**: Subclass your agents using `CreduentConversableAgent` from `creduent.integrations.autogen` to enforce cryptographic sender identity checks on incoming messages.

## Registry API

- `POST /register` - Verifies the agent's identity via signature and DNS TXT checks, then issues a signed attestation.
- `POST /attest` - Developer direct agent registration (no agent_json_url required).
- `GET /attest/{agent_id}` - Retrieves the active Creduent-signed attestation for the specified agent.
- `GET /agents` - Lists all registered agent metadata and attestations in the registry.
- `DELETE /revoke/{agent_id}` - Revokes an agent attestation from the registry (requires multisig headers or legacy `CREDUENT-ADMIN-KEY`).
- `POST /recovery/override` - Key override using domain DNS TXT record checks.
- `POST /renew` - Renew agent attestation with a new expiry date.
- `POST /webhook/register` - Register a webhook URL for expiry notifications.
- `GET /webhook/{agent_id}` - Retrieve the registered webhook URL for an agent.
- `GET /stats` - Registry telemetry (total, verified, unverified, revoked, expiring soon).
- `GET /challenge/{agent_id}` - Generates a secure challenge and nonce for identity verification.
- `POST /verify-challenge` - Verifies a signed challenge response and issues a short-lived proof token.
- `GET /public-key` - Retrieves the registry public key used to verify proof tokens.
- `GET /dashboard` - Developer dashboard UI at `creduent.idevsec.com/dashboard`.
- `GET /resolver` - Agent:// URI resolver UI at `creduent.idevsec.com/resolver`.

## Protocol Standards & Specification

The Creduent Protocol is structured as a series of formal standards-track documents maintained by IDevSec:

* **[Standards Index](standards/README.md)** - Main index of all protocol standards
* **[CREDUENT-001: agent.json](standards/CREDUENT-001-agent-json.md)** (based on canonical **[SPEC.md](SPEC.md)**) - Base identity specification
* **[CREDUENT-002: Attestation](standards/CREDUENT-002-attestation.md)** - Signed attestation schemas and verification pipelines
* **[CREDUENT-003: Registry API](standards/CREDUENT-003-registry-api.md)** - Registry HTTP API endpoints and security controls
* **[CREDUENT-004: Agent URI Resolution](standards/CREDUENT-004-uri-resolution.md)** - DNS-bound `agent://` URI scheme resolution
* **[CREDUENT-005: Federation](standards/CREDUENT-005-federation.md)** - Federated Root-and-Node trust model
* **[CREDUENT-006: Dynamic Attestation](standards/CREDUENT-006-dynamic-attestation.md)** - Dynamic prompt and hardware attestation (Draft)

## Origin and Stewardship

Kashish Kanojia is the creator of the Creduent Protocol, stewarded by [IDevSec](https://idevsec.com).

Creduent is an open protocol intended for community adoption, interoperability, and federated trust. Long-term governance and stewardship are managed by IDevSec to ensure it remains a neutral, open standard for the entire AI agent ecosystem.

For details on the project's history, please see:
* [AUTHORS.md](AUTHORS.md) - Founding details and references

The reference registry, SDKs, and protocol tooling serve as the initial implementation of the protocol.

## Contributing

Contributions to the Creduent Protocol standards and reference implementations are welcome.
- Open an issue or discussion on GitHub to propose protocol changes
- All specification changes follow the CIP (Creduent Improvement Proposal) process defined in [CREDUENT-005](standards/CREDUENT-005-federation.md)
- Join the consortium: [idevsec.com/creduent](https://idevsec.com/creduent)

## Useful Links

| Resource | URL |
|---|---|
| Protocol Showcase | https://idevsec.com/creduent |
| Technical Documentation | https://idevsec.com/creduent/docs |
| Licensing Details | https://idevsec.com/creduent/licensing |
| Reference Registry | https://creduent.idevsec.com |
| Registry Dashboard | https://creduent.idevsec.com/dashboard |
| Python SDK (PyPI) | https://pypi.org/project/creduent/ |
| JavaScript SDK (npm) | https://www.npmjs.com/package/@idevsec/creduent |
| CLI Tool (npm) | https://www.npmjs.com/package/@idevsec/creduent-cli |

## Security & Hardening

The Creduent Registry includes several security guarantees and resilience safeguards built-in:

- **Fail-Closed Validation:** If an agent's attestation timestamp or expiration date fails to parse due to corruption or malicious payload tempering, the verification pipeline defaults to marking the attestation as `expired` (`expired = True`).
- **Serverless Rate Limiting Guard:** To prevent clients from bypassing rate limits in stateless environments (like Vercel serverless functions where in-memory fallback databases are wiped during container cold starts), the registry explicitly raises an `HTTP 500` error if Upstash Redis credentials are not configured.
- **Canonical JCS Serialization:** All cryptographic signature validations use unified JSON Canonicalization Scheme (JCS) encoding wrappers compliant with RFC 8785 to avoid formatting discrepancies.
- **SSRF Prevention in Webhooks:** All outbound webhook alerts go through rigorous IP validation filters (`safe_requests_post`) that drop private, loopback, and local IP ranges, preventing Server-Side Request Forgery.
- **Authorized Webhook Queries:** Retrieval of registered webhook URLs via `/webhook/{agent_id}` is restricted to authorized administrators (requiring the `CREDUENT-ADMIN-KEY` token) to prevent metadata information leaks.
- **CLI Admin Integration:** The developer CLI automatically forwards administrative credentials from the environment, ensuring seamless operation for authorized operators without exposing public lookup endpoints.
- **Decoupled Security Audits:** Agent capability scans (DNS, OSINT headers, and Clickjacking/HSTS verification) are separated from the main registry controllers into isolated services, allowing independent code auditing.

---

## Licensing

Creduent's licensing model is designed to maximize community adoption and interoperability:

* **Protocol Specification:** The Creduent Protocol specifications (including standard documents `CREDUENT-001` through `CREDUENT-006` located in the `standards/` directory) are open, public-domain standards. Anyone is free to implement the protocol, build custom registries, or design compatible clients without any license restrictions or royalties.

* **Reference Implementation, SDKs & CLIs:** All Creduent software assets (including the Python SDK, JavaScript/TypeScript SDK (`@idevsec/creduent`), CLI Tool (`@idevsec/creduent-cli`), MCP Server, and reference registry source code) are licensed under the **[Apache License 2.0](LICENSE)**.