# CREDUENT-009: Automated DNS Provisioning via Domain Connect

**Status:** Draft  
**Version:** 0.1  
**Author:** IDevSec  
**Date:** 2026-11-14  
**Related:** [CREDUENT-001](CREDUENT-001-agent-json.md), [CREDUENT-002](CREDUENT-002-attestation.md), [CREDUENT-003](CREDUENT-003-registry-api.md), [CREDUENT-008](CREDUENT-008-ibrl.md)

---

## 1. Overview & Motivation

To bind an autonomous agent's identity (`agent_id`) to a verified internet domain, [CREDUENT-001](CREDUENT-001-agent-json.md) and [CREDUENT-002](CREDUENT-002-attestation.md) require publishing a DNS TXT record at `_creduent.<domain>`.

Historically, this required human operators to manually log into registrar dashboards, navigate complex DNS zone editors, and copy-paste long cryptographic strings. This manual process introduces:
1. **High Onboarding Friction**: Typical setup times of 10 to 20 minutes.
2. **Configuration Errors**: Copy-paste corruptions, missing subdomains, erroneous trailing dots, and string-escaping issues.
3. **Drop-Off Rates**: High friction during early-stage agent scaffolding and CLI initialization.

**CREDUENT-009** defines the standardized protocol for **Automated DNS Provisioning** using the open **Domain Connect** standard (`domainconnect.org`). It specifies how Creduent clients (such as `creduent-cli` and the reference web registry) discover domain registrar capabilities and programmatically provision `_creduent` TXT verification records via a 1-click user authorization flow.

---

## 2. DNS Discovery Flow (`_domainconnect`)

Before initiating automated provisioning, a Creduent client MUST perform discovery to determine if the target domain's authoritative DNS provider supports Domain Connect.

### 2.1 Discovery Query
The client executes a DNS TXT or CNAME lookup for:
```text
_domainconnect.<domain>
```

#### Example Discovery Record:
```text
_domainconnect.example.com. 300 IN TXT "domainconnect.cloudflare.com/api/v2"
```

### 2.2 Provider Endpoint Discovery
The client queries the discovery endpoint over HTTPS:
```http
GET https://domainconnect.cloudflare.com/api/v2/domainTemplates/providers/idevsec.com/services/creduent-agent-identity HTTP/1.1
Host: domainconnect.cloudflare.com
Accept: application/json
```

The DNS provider returns its API capabilities, including:
* `urlAPI`: Direct REST API base URL.
* `urlAsyncUX`: Web UX base URL for interactive user consent.

---

## 3. Creduent Domain Connect Service Template

The normative service template for Creduent agent identity provisioning is identified by:
* **Provider ID**: `idevsec.com`
* **Service ID**: `creduent-agent-identity`
* **Version**: `1`

### 3.1 Template Definition Schema (`creduent-agent-identity.json`)
```json
{
  "providerId": "idevsec.com",
  "providerName": "Creduent Protocol",
  "serviceId": "creduent-agent-identity",
  "serviceName": "Creduent AI Agent Verification",
  "version": 1,
  "logoUrl": "https://idevsec.com/icon.png",
  "description": "Cryptographically binds autonomous AI agents to this domain via the Creduent open protocol.",
  "variableDescription": "%agent_id%: The canonical agent URI (e.g. agent://domain.com/bot); %public_key%: The Ed25519 public key in format ed25519:<key>",
  "syncPubKeyDomain": "idevsec.com",
  "syncRedirectDomain": "creduent.idevsec.com,idevsec.com,127.0.0.1",
  "records": [
    {
      "type": "TXT",
      "host": "_creduent",
      "data": "v=creduent1; agent=%agent_id%; k=%public_key%",
      "ttl": 300,
      "txtConflictMatchingMode": "Prefix",
      "txtConflictMatchingPrefix": "v=creduent1;"
    }
  ]
}
```

> **Note on Host Attribute:** Per the official Domain Connect Specification (Rule 9 / DCTL1024), the protocol automatically appends the user's `host` parameter to the record's `host` attribute. Therefore, specifying `"_creduent"` produces `_creduent.<domain>` for apex requests (`host=@`), and `_creduent.<subdomain>.<domain>` for subdomain requests without duplicate labels.

### 3.2 Template Variables
| Variable | Description | Example |
| :--- | :--- | :--- |
| `%host%` | Subdomain or apex host. For apex domains, providers map to empty string or `@`. | `@` or `sub` |
| `%agent_id%` | URI-encoded Creduent agent identifier. | `agent%3A%2F%2Fexample.com%2Fmybot` |
| `%public_key%` | Agent Ed25519 public key in standard base64 or prefixed hex string. | `ed25519%3AhArTvb...` |

---

## 4. Client Execution Flows

### 4.1 CLI Local Loopback Flow (`creduent init` / `creduent register`)
For interactive CLI workflows, clients MUST implement the ephemeral local loopback pattern:

```text
[ Developer Terminal ]            [ Local HTTP Server ]         [ Web Browser ]         [ DNS Registrar ]
         |                                  |                          |                        |
         |-- 1. creduent register --------->|                          |                        |
         |   (spins up localhost:PORT)      |                          |                        |
         |                                  |                          |                        |
         |-- 2. Open Domain Connect URL ------------------------------>|                        |
         |                                                             |-- 3. Consent Page ---->|
         |                                                             |                        | (User clicks "Approve")
         |                                                             |                        | (Registrar sets TXT)
         |                                                             |<-- 4. Redirect --------|
         |<-- 5. Captured Callback (http://localhost:PORT/callback) ---|
         |
         |-- 6. Verify DNS TXT & Complete Attestation ----------------------------------------->
```

1. **Port Selection**: CLI binds to an ephemeral local port on `127.0.0.1` (e.g. `127.0.0.1:0`).
2. **State Parameter Generation**: CLI generates a cryptographically random `state` nonce to prevent cross-site request forgery.
3. **URL Construction**: CLI constructs the `apply` consent URL:
   ```text
   https://dash.cloudflare.com/domainconnect/v2/domainTemplates/providers/idevsec.com/services/creduent-agent-identity/apply?domain=example.com&agent_id=agent%3A%2F%2Fexample.com%2Fbot&public_key=ed25519%3A...&redirect_uri=http%3A%2F%2F127.0.0.1%3A48219%2Fcallback&state=nonce123
   ```
4. **Browser Auto-Launch**: CLI invokes the default OS browser.
5. **Callback Reception**: Upon registrar approval, the browser is redirected to `http://127.0.0.1:<port>/callback?state=nonce123`.
6. **Graceful Teardown**: CLI validates `state`, renders an HTML success message to the browser, closes the local server, and completes registration.

### 4.2 Web Dashboard Flow
In web interfaces (e.g., `creduent.idevsec.com/dashboard`):
* `redirect_uri` points directly to `https://creduent.idevsec.com/domains/callback`.
* Registry validates the DNS modification in real-time and issues the attestation certificate without manual copy-pasting.

### 4.3 Headless / CI/CD Environments
When standard input is non-interactive (`!isatty`) or running within CI pipelines:
* Clients MUST NOT attempt to launch a local browser.
* Clients MUST print the manual TXT record payload and the 1-click Domain Connect URL for out-of-band operator activation.
* Clients MAY accept a direct DNS API token via environment variable or flag (e.g., `--cloudflare-token` or `CLOUDFLARE_API_TOKEN`) for zero-interaction automated provisioning.

---

## 5. Security & Validation Requirements

Implementations claiming conformance with CREDUENT-009 MUST enforce the following safeguards:

1. **Anti-CSRF Nonces (`state`)**: All asynchronous redirect requests MUST include a high-entropy `state` parameter generated by the initiating client and verified upon callback.
2. **Signature & DNSSEC Verification**: Following callback receipt, the client or registry MUST verify that the `_creduent.<domain>` TXT record is resolvable and matches the expected public key before issuing any attestation.
3. **TTL Minimization**: Auto-configured records SHOULD specify a short TTL (e.g., 300 seconds) to facilitate rapid key rotation and recovery overrides per CREDUENT-002.
4. **Subdomain Isolation**: When provisioning agents on subdomains (`agent://sub.example.com/bot`), the TXT record MUST be isolated to `_creduent.sub.example.com` to prevent unauthorized cross-subdomain identity assertions.

---

## 6. Conformance Requirements

An implementation claiming conformance with CREDUENT-009 MUST satisfy the following checklist:

- [ ] **DC-M01:** MUST perform `_domainconnect.<domain>` discovery before falling back to manual instructions.
- [ ] **DC-M02:** MUST format `_creduent` TXT data strictly conforming to `v=creduent1; agent=<agent_id>; k=<public_key>`.
- [ ] **DC-M03:** MUST validate the `state` parameter upon loopback or callback redirect.
- [ ] **DC-M04:** MUST shut down ephemeral local HTTP servers immediately after receiving the callback or timing out (max timeout 120 seconds).
- [ ] **DC-M05:** MUST provide manual DNS fallback and non-interactive output when executed in headless or CI environments.

