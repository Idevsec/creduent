# Creduent: Agent Identity & Trust Protocol

Creduent is an open application-layer protocol that enables cryptographic identity verification and federated attestation for autonomous AI agents.

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
  "agent_id": "agent://example/reconbot",
  "owner": "Example Corp",
  "public_key": "ed25519:hArTvbITJ2jirL170IOSjcVvEvstC4s+RjYLu4chCwg=",
  "endpoint": "https://api.example.com/recon",
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
_creduent.example.com TXT "agent://example/reconbot"
```

### 3. Register with Creduent Registry
Submit your agent's registration to the registry:
```bash
curl -X POST https://api.idevsec.com/register \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "agent://example/reconbot", "domain": "example.com", "agent_json_url": "https://example.com/.well-known/agent.json"}'
```

## SDKs

### Python
```bash
pip install creduent
```

### JavaScript / TypeScript
```bash
npm install @creduent/sdk
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
        "CREDUENT_REGISTRY_URL": "https://api.idevsec.com"
      }
    }
  }
}
```

Call `verify_agent` with target agent ID or domain to receive structural, cryptographic signature, and registry-attested status.

## Registry API

- `POST /register` - Verifies the agent's identity via signature and DNS TXT checks, then issues a signed attestation.
- `POST /attest` - Developer direct agent registration (no agent_json_url required).
- `GET /attest/{agent_id}` - Retrieves the active Creduent-signed attestation for the specified agent.
- `GET /agents` - Lists all registered agent metadata and attestations in the registry.
- `DELETE /revoke/{agent_id}` - Revokes an agent attestation from the registry (requires `CREDUENT-ADMIN-KEY` header).
- `POST /renew` - Renew agent attestation with a new expiry date.
- `POST /webhook/register` - Register a webhook URL for expiry notifications.
- `GET /webhook/{agent_id}` - Retrieve the registered webhook URL for an agent.
- `GET /stats` - Registry telemetry (total, verified, unverified, revoked, expiring soon).
- `GET /dashboard` - Developer dashboard UI at `api.idevsec.com/dashboard`.
- `GET /resolver` - Agent:// URI resolver UI at `api.idevsec.com/resolver`.

## Protocol Specification

For full protocol rules, signing details, and schema definitions, refer to [SPEC.md](SPEC.md).

## License

This project is licensed under the [MIT License](LICENSE).