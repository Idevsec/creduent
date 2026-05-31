# Creduent: Quickstart Guide

Get an agent registered and verified in under 10 minutes.

---

## Prerequisites

- Python 3.9+ or Node.js 18+
- A domain you control (e.g. `example.com`)
- DNS access to add a TXT record
- A web server that can serve a static JSON file over HTTPS

---

## Step 1: Install the SDK

**Python:**
```bash
pip install creduent
```

**JavaScript / TypeScript:**
```bash
npm install @creduent/sdk
```

---

## Step 2: Generate an Ed25519 Keypair

**Python (CLI):**
```bash
creduent-sign generate-keys \
  --private-out private_key.pem \
  --public-out public_key.txt
```

**Python (SDK):**
```python
from creduent import generate_keys

private_key_pem, public_key_str = generate_keys()
print("Public key:", public_key_str)

# Save private key securely
with open("private_key.pem", "w") as f:
    f.write(private_key_pem)
```

> **Keep `private_key.pem` secret.** Never commit it to version control.

---

## Step 3: Create and Sign Your agent.json

Create a file called `draft_agent.json`:

```json
{
  "version": "1.0",
  "agent_id": "agent://example/mybot",
  "owner": "Example Corp",
  "public_key": "ed25519:<paste-your-public-key-here>",
  "endpoint": "https://api.example.com",
  "capabilities": ["chat", "search"]
}
```

Replace `example`, `mybot`, `Example Corp`, and the `public_key` value with your own.

**Sign it:**

```bash
creduent-sign sign \
  --key private_key.pem \
  --input draft_agent.json \
  --output agent.json
```

This produces `agent.json` with a `signature` field attached.

**Verify the signature locally:**
```bash
creduent-verify file --path agent.json
```

Expected output:
```
[+] Signature valid: True
```

---

## Step 4: Publish agent.json

Host the signed `agent.json` at the well-known path on your domain:

```
https://example.com/.well-known/agent.json
```

**Nginx example:**
```nginx
location /.well-known/agent.json {
    alias /var/www/agent.json;
    default_type application/json;
}
```

**Vercel / static host:** Upload `agent.json` to your `.well-known/` directory.

**Quick test:**
```bash
curl https://example.com/.well-known/agent.json
```

---

## Cloudflare Users — Required Configuration

If your domain is proxied through Cloudflare (orange cloud), you must add a WAF rule before registering. Without this, Cloudflare will block the Creduent registry server from fetching your agent.json and health-checking your endpoint, returning HTTP 403.

### Rule 1 — Allow Registry Fetch and Endpoint Health Check

Cloudflare Dashboard → Security → Security Rules → Custom Rules → Create Rule

Name: Allow Creduent Manifest and Endpoint
Field: URI Path
Operator: is in
Value:
- `/.well-known/agent.json`
- `/<your-agent-endpoint-path>` (e.g. `/agent` or `/api/agent`)
Action: Skip
Skip: All remaining custom rules + All rate limiting rules + All managed rules
Place at: First

### DNS TXT Record (Cloudflare)

When adding the _creduent TXT record in Cloudflare DNS:
- Make sure the orange cloud (proxy) is OFF for the TXT record
- TXT records do not need to be proxied
- TTL: Auto

### Common Cloudflare Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Failed to fetch agent.json: HTTP 403 | Cloudflare WAF blocking registry server | Add the WAF rule above |
| Failed to fetch agent.json: HTTP 403 (after adding rules) | Bot Fight Mode JS challenge | Disable JS Detections under Security → Bots |
| Registration succeeds but resolver shows 403 | CSP blocking api.idevsec.com | Add api.idevsec.com to connect-src in your site's CSP headers |

---

## Step 5: Add the DNS TXT Record

In your DNS provider, add a TXT record:

| Field | Value |
|:---|:---|
| Name | `_creduent.example.com` |
| Type | TXT |
| Value | `agent://example/mybot` |
| TTL | 3600 |

**Verify propagation:**
```bash
dig TXT _creduent.example.com +short
```

Expected output:
```
"agent://example/mybot"
```

> DNS records can take up to 48 hours to propagate globally. The registry query will fail until the record is visible.

---

## Step 6: Register with the Creduent Registry

**Using curl:**
```bash
curl -X POST https://api.idevsec.com/register \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent://example/mybot",
    "domain": "example.com",
    "agent_json_url": "https://example.com/.well-known/agent.json"
  }'
```

**Using the Python SDK:**
```python
from creduent import register

result = register(
    agent_id="agent://example/mybot",
    domain="example.com",
    agent_json_url="https://example.com/.well-known/agent.json"
)

print("Success:", result.success)
print("Attestation level:", result.attestation.get("level"))
```

**Using the JavaScript SDK:**
```typescript
import { registerAgent } from "@creduent/sdk";

const result = await registerAgent({
  agent_id: "agent://example/mybot",
  domain: "example.com",
  public_key: "ed25519:<your-public-key>"
});

console.log("Registered:", result.agent_id);
```

**Expected response:**
```json
{
  "success": true,
  "agent_id": "agent://example/mybot",
  "attestation": {
    "level": "verified",
    "issued_at": "2026-05-30T00:00:00Z",
    "expires_at": "2027-05-30T00:00:00Z"
  }
}
```

---

## Step 7: Verify Your Agent

**From command line:**
```bash
creduent-verify agent-id --uri agent://example/mybot
```

**From Python:**
```python
from creduent import attest

result = attest("agent://example/mybot")
print("Attested:", result.attested)
print("Level:", result.level)
```

**From JavaScript:**
```typescript
import { verifyAgent } from "@creduent/sdk";

const isVerified = await verifyAgent("agent://example/mybot");
console.log("Verified:", isVerified); // true
```

---

## Step 8: Challenge-Response Authentication

You can use the SDK's challenge-response features to cryptographically authenticate your agent's identity to other agents.

**Proving identity (Agent side):**
```python
from creduent import challenge

# Generate a signed proof using your private key
proof = challenge.create_proof(
    agent_id="agent://example/mybot",
    private_key_pem=open("private_key.pem").read()
)

# Send the proof dict (containing proof_token) to the receiver
# proof = {"verified": True, "level": "verified", "proof_token": "...", "valid_until": "..."}
```

**Verifying identity (Receiver side):**
```python
from creduent import challenge

# Verify the proof token received from the agent
is_valid = challenge.verify_proof(
    proof_token=proof["proof_token"],
    agent_id="agent://example/mybot"
)
print("Is agent identity authentic?", is_valid)  # True
```

---

## Step 9: Add the MCP Server (Optional)

To expose `verify_agent` as a tool in your agent host:

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

Your agent host can now call `verify_agent("agent://example/mybot")` to get a full attestation report.

---

## Troubleshooting

**Registration returns 400 - DNS TXT not found:**  
Wait for DNS propagation. Test with `dig TXT _creduent.yourdomain.com +short`. If empty, the record is not live yet.

**Registration returns 400 - Signature invalid:**  
Ensure `agent.json` was signed with the private key matching the `public_key` field in the document. Re-run `creduent-sign sign`.

**Registration returns 400 - Endpoint healthcheck failed:**  
The registry performs an HTTP GET to your declared `endpoint`. Confirm it returns 2xx when fetched from the internet.

**`creduent-sign` not found:**  
Run `pip install creduent` and confirm your Python scripts directory is on your `PATH`.

---

## Next Steps

- Read the full [Protocol Specification](SPEC.md)
- Explore [EXAMPLES.md](EXAMPLES.md) for complete integration examples
- Review [FAQ.md](FAQ.md) for common questions
- Set up [auto-renewal](SPEC.md#66-renewal) to avoid attestation expiry
