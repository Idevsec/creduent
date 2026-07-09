# Creduent: Examples

Complete, runnable integration examples for common Creduent use cases.

---

## Example 1: Minimal agent.json

The smallest valid signed agent.json document:

```json
{
  "version": "1.0",
  "agent_id": "agent://example/mybot",
  "owner": "Example Corp",
  "public_key": "ed25519:hArTvbITJ2jirL170IOSjcVvEvstC4s+RjYLu4chCwg=",
  "endpoint": "https://api.example.com",
  "capabilities": ["chat"],
  "signature": "base64_signature_here"
}
```

---

## Example 2: Full agent.json with Timestamp

```json
{
  "version": "1.0",
  "issued_at": "2026-05-30T00:00:00Z",
  "agent_id": "agent://example/mybot",
  "owner": "Example Corp",
  "public_key": "ed25519:hArTvbITJ2jirL170IOSjcVvEvstC4s+RjYLu4chCwg=",
  "endpoint": "https://api.example.com",
  "capabilities": ["chat", "search", "summarize"],
  "signature": "base64_signature_here"
}
```

---

## Example 2a: Minimal agent.json (Version 2.0)

The v2.0 schema splits identity configuration, keys, and capabilities into distinct namespace blocks:

```json
{
  "version": "2.0",
  "identity": {
    "agent_id": "agent://example/mybot",
    "owner": "Example Corp",
    "keys": [
      {
        "id": "key-1",
        "type": "ed25519",
        "public_key": "ed25519:MI0YrgwrpBd21mfwWi5Kyme8J32JBpRStfLeTjrYZVU=",
        "status": "active"
      }
    ],
    "endpoint": "https://api.example.com"
  },
  "policy": {
    "capabilities": ["chat"]
  },
  "signature": "749+ElO3Cua0/xQDL0npagjR9gTwJVA6oGP5rGq3qtXnbv7ziap1mA0xH4yipLV299UEzcjnenQB2dK5KdtrDQ=="
}
```

---

## Example 3: Generate Keys and Sign (Python)

```python
from creduent import generate_keys, sign
import json

# Generate a new Ed25519 keypair
private_key_pem, public_key_str = generate_keys()
print("Public key:", public_key_str)

# Build an unsigned draft document
draft = {
    "version": "1.0",
    "agent_id": "agent://example/mybot",
    "owner": "Example Corp",
    "public_key": public_key_str,
    "endpoint": "https://api.example.com",
    "capabilities": ["chat", "search"]
}

# Sign the draft - returns a dict with the signature field added
signed = sign(draft, private_key_pem)
print(json.dumps(signed, indent=2))
```

---

## Example 4: Verify a Local File (Python)

```python
from creduent import verify

result = verify("path/to/agent.json")
print("Valid:", result.valid)
print("Agent ID:", result.agent_id)
```

---

## Example 5: Verify by Domain (Python)

```python
from creduent import verify

# Fetches https://example.com/.well-known/agent.json and verifies it
result = verify("example.com")
print("Valid:", result.valid)
```

---

## Example 6: Verify by agent:// URI (Python)

```python
from creduent import verify

# Resolves via registry, then verifies the fetched document
result = verify("agent://example/mybot")
print("Valid:", result.valid)
print("Agent ID:", result.agent_id)
```

---

## Example 7: Full Registration Flow (Python)

```python
import os
from creduent import generate_keys, sign, register, attest

# 1. Generate keys
private_key_pem, public_key_str = generate_keys()

# 2. Sign the draft document
draft = {
    "version": "1.0",
    "agent_id": "agent://example/mybot",
    "owner": "Example Corp",
    "public_key": public_key_str,
    "endpoint": "https://api.example.com",
    "capabilities": ["chat"]
}
signed = sign(draft, private_key_pem)

# 3. Host signed at https://example.com/.well-known/agent.json
# (deployment step omitted)

# 4. Register with the Creduent registry
result = register(
    agent_id="agent://example/mybot",
    domain="example.com",
    agent_json_url="https://example.com/.well-known/agent.json"
)
print("Registration success:", result.success)
print("Attestation level:", result.attestation.get("level"))

# 5. Verify attestation
att = attest("agent://example/mybot")
print("Attested:", att.attested)
print("Expires at:", att.expires_at)
```

---

## Example 8: Resolve and Verify (JavaScript / TypeScript)

```typescript
import { resolveAgent, verifyAgent, AgentNotFoundError, CreduentError } from "@idevsec/creduent";

async function checkAgent(uri: string) {
  try {
    // Get the full attestation record
    const record = await resolveAgent(uri);
    console.log("Agent ID:", record.agent_id);
    console.log("Issuer:", record.issuer);
    console.log("Level:", record.level);
    console.log("Domain:", record.domain);
    console.log("Public Key:", record.public_key);
    console.log("Expires:", record.expires_at);

    // Quick boolean check
    const isVerified = await verifyAgent(uri);
    console.log("Is verified:", isVerified);

  } catch (err) {
    if (err instanceof AgentNotFoundError) {
      console.error("Agent not found in registry.");
    } else if (err instanceof CreduentError) {
      console.error(`Registry error (${err.statusCode}):`, err.message);
    } else {
      throw err;
    }
  }
}

checkAgent("agent://idevsec/steward");
```

---

## Example 9: Register Agent (JavaScript / TypeScript)

```typescript
import { registerAgent } from "@idevsec/creduent";

const result = await registerAgent({
  agent_id: "agent://example/mybot",
  domain: "example.com",
  public_key: "ed25519:hArTvbITJ2jirL170IOSjcVvEvstC4s+RjYLu4chCwg=",
  metadata: {
    description: "My example agent"
  }
});

console.log("Registered:", result.agent_id);
console.log("Level:", result.level);
```

---

## Example 10: Custom Registry Endpoint (JavaScript)

```typescript
import { resolveAgent } from "@idevsec/creduent";

// Point to a private or alternative registry
const record = await resolveAgent("agent://example/mybot", {
  baseUrl: "https://registry.my-org.internal",
  headers: {
    "Authorization": "Bearer <token>"
  }
});
```

---

## Example 11: MCP Tool Usage

Once `creduent_mcp_server.py` is configured in your MCP host, call the `verify_agent` tool:

**Input:**
```json
{
  "target": "agent://idevsec/steward"
}
```

**Output:**
```json
{
  "agent_id": "agent://idevsec/steward",
  "self_verified": true,
  "creduent_attested": true,
  "attestation_level": "verified",
  "attestation_issued_at": "2026-05-29T00:00:00Z",
  "attestation_expires_at": "2027-05-29T00:00:00Z",
  "public_key": "ed25519:hArTvbITJ2jirL170IOSjcVvEvstC4s+RjYLu4chCwg=",
  "endpoint": "https://creduent.idevsec.com",
  "capabilities": ["query", "resolve", "verify"],
  "checked_at": "2026-05-30T07:00:00Z"
}
```

---

## Example 12: Attestation Renewal (Python)

```python
from creduent import generate_keys
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import base64
import requests

agent_id = "agent://example/mybot"
new_expires_at = "2028-05-30T00:00:00Z"

# Load existing private key
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Sign the renewal payload
message = f"{agent_id}|{new_expires_at}".encode("utf-8")
signature_bytes = private_key.sign(message)
signature_b64 = base64.b64encode(signature_bytes).decode("utf-8")

# Submit renewal
resp = requests.post("https://creduent.idevsec.com/renew", json={
    "agent_id": agent_id,
    "new_expires_at": new_expires_at,
    "signature": signature_b64
})
print(resp.json())
```

---

## Example 13: Webhook Registration (curl)

```bash
# Compute signature over "agent_id|webhook_url" first
# Then submit:

curl -X POST https://creduent.idevsec.com/webhook/register \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent://example/mybot",
    "webhook_url": "https://example.com/hooks/creduent",
    "signature": "<base64_signature>"
  }'
```

**Webhook payload you will receive 30 days before expiry:**
```json
{
  "event": "agent.expiry_warning",
  "agent_id": "agent://example/mybot",
  "domain": "example.com",
  "expires_at": "2027-05-30T00:00:00Z",
  "days_remaining": 28,
  "action_url": "https://creduent.idevsec.com/renew"
}
```

---

## Example 14: DNS Record Configuration

**For `example.com` binding `agent://example/mybot`:**

```
Record type:  TXT
Record name:  _creduent.example.com
Record value: agent://example/mybot
TTL:          3600
```

Verify with:
```bash
dig TXT _creduent.example.com +short
```

Expected:
```
"agent://example/mybot"
```

---

## Example 15: GitHub Actions Auto-Attest

Trigger re-attestation on every deploy using the `creduent-attest` GitHub Action:

```yaml
# .github/workflows/deploy.yml
name: Deploy and Attest

on:
  push:
    branches: [main]

jobs:
  attest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Creduent SDK
        run: pip install creduent

      - name: Register / Re-attest agent
        run: |
          python -c "
          from creduent import register
          result = register(
              agent_id='agent://example/mybot',
              domain='example.com',
              agent_json_url='https://example.com/.well-known/agent.json'
          )
          print('Attestation level:', result.attestation.get('level'))
          "
        env:
          CREDUENT_REGISTRY_URL: https://creduent.idevsec.com
```

---

For more details, see:
- [QUICKSTART.md](QUICKSTART.md)
- [SPEC.md](SPEC.md)
- [FAQ.md](FAQ.md)
