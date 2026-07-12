# CREDUENT-006: Dynamic Prompt, Model, and Hardware Attestation

**Status:** Draft  
**Version:** 0.1  
**Author:** IDevSec  
**Date:** 2026-07-04  
**Related:** [CREDUENT-001](CREDUENT-001-agent-json.md), [CREDUENT-002](CREDUENT-002-attestation.md), [CREDUENT-003](CREDUENT-003-registry-api.md)

---

## 1. Introduction

Traditional workload identity (e.g., SPIFFE/SPIRE, mTLS) authenticates that a specific process is running inside a legitimate container on verified hardware. However, it cannot verify the **cognitive state** or **operational boundaries** of an autonomous AI agent. 

Unlike static code, an AI agent's behavior is driven by:
1. **System Prompts / Instructions:** Dynamic natural language templates that define the agent's persona, rules, and logic.
2. **Model Configurations:** The underlying LLM parameters (model name, temperature, context limits).
3. **Tool Access:** The schema of external tools and APIs the agent is authorized to call.

A minor, unauthorized tweak to a system prompt (e.g., prompt injection or stealthy instruction modification) can completely alter an agent's behavior while keeping the runtime container, network signatures, and binary code identical.

To establish **Hard-Power Governance** over autonomous agents, this specification defines the **Dynamic Cognitive Attestation Layer**, answering three key security questions:
1. **Verifiable State:** How to verify an agent's prompts, model, and tools have not been manipulated mid-session.
2. **Action Auditing:** How to cryptographically prove to an auditor which specific cognitive version of an agent took a specific action.
3. **Dynamic Lifecycle:** How to rotate, re-issue, or revoke an agent's identity when its prompt, model, or tools change.

---

## 2. The Agent Prompt Hash (APH)

To verify the integrity of the agent's cognitive state, we compute a cryptographically secure hash of its inputs, tools, and model metadata. This is the **Agent Prompt Hash (APH)** (also referred to as the Cognitive State Hash).

### 2.1 The Cognitive Manifest

An agent MUST define its cognitive bounds in a **Cognitive Manifest** dictionary. The dictionary contains the following fields:

| Field | Type | Required | Description |
|:---|:---|:---|:---|
| `system_prompt` | String | Yes | The exact base system instructions/prompt passed to the model. |
| `model` | String | Yes | The identifier of the LLM model (e.g., `"gemini-1.5-pro"`). |
| `temperature` | Float | Yes | The model's temperature parameter. |
| `tools` | Array | Yes | A list of JSON schema representations of the tools the agent is permitted to use. |
| `parent_identity` | String | No | The Creduent URI of the parent/orchestrator agent (if part of a multi-agent system). |

Each entry in `tools` MUST additionally declare a `reversibility` field describing how hard the tool's effect is to undo, one of `read-only`, `reversible`, `external-reversible`, or `irreversible` (the OWASP AISVS v1.0 reversibility classification, C9.2.3). This class is set at design time by the manifest author. Because the Cognitive Manifest is canonicalized and hashed into the APH (Section 2.2), the reversibility class is covered by the APH and the agent cannot assert or alter it at runtime.

### 2.2 Computing the APH

The APH is computed by serializing and hashing the Cognitive Manifest:

1. Canonicalize the Cognitive Manifest using the **RFC 8785 JSON Canonicalization Scheme (JCS)** to ensure deterministic serialization regardless of language parser or key ordering.
2. Compute the **SHA-256** hash of the canonical UTF-8 encoded bytes.
3. Format the result as `sha256:<hex_digest>`.

```
+--------------------------+
|    Cognitive Manifest    |
| (Prompt, Model, Tools)   |
+--------------------------+
             │
             ▼
┌──────────────────────────┐
│  JCS Canonicalization    │ (RFC 8785)
└──────────────────────────┘
             │
             ▼
┌──────────────────────────┐
│       SHA-256            │
└──────────────────────────┘
             │
             ▼
+--------------------------+
|  Agent Prompt Hash (APH) |
+--------------------------+
```

### 2.3 Example APH Calculation

For the following manifest:
```json
{
  "model": "gemini-1.5-pro",
  "system_prompt": "You are a DevOps assistant. Do not run destructive commands.",
  "temperature": 0.0,
  "tools": [
    {
      "name": "run_command",
      "description": "Execute a terminal command",
      "parameters": {
        "type": "object",
        "properties": {
          "command": { "type": "string" }
        },
        "required": ["command"]
      },
      "reversibility": "irreversible"
    }
  ]
}
```

Its canonical JCS string representation is hashed to produce the APH:
`sha256:d8b2d184...`

---

## 3. Hardware-Attested Execution Proofs

To prevent an attacker from modifying an agent's code or instructions on a compromised host while spoofing a valid APH, the agent's running instance MUST run within a **Trusted Execution Environment (TEE)** or be secured by a **Trusted Platform Module (TPM)**.

```
+-------------------------------------------------------+
|                 Atlas Secure Node (TEE)               |
|                                                       |
|   +------------------+         +------------------+   |
|   |     AI Agent     |         |    vTPM / TPM    |   |
|   |                  |         |                  |   |
|   |  - Code          |         |  PCR 10: IMA Log |   |
|   |  - Prompt/Tools  |         |  PCR 15: APH     |   |
|   +------------------+         +------------------+   |
|            │                            │             |
|            └─────── Generates Quote ────┘             |
|                            │                          |
+----------------------------┼────────────────----------+
                             │
                             ▼
              +──────────────────────────────+
              | Attested Execution Proof     |
              | (Signed Quote + APH Binding) |
              +──────────────────────────────+
```

### 3.1 TPM PCR Binding

When running on an Atlas Secure Node, the execution environment maps cognitive metrics to specific TPM Platform Configuration Registers (PCRs):

* **PCR 10 (System Integrity):** Stores Linux Integrity Measurement Architecture (IMA) digests of the agent's executable binaries, runtime scripts, and libraries.
* **PCR 15 (Cognitive Integrity):** Stores the extended value of the **Agent Prompt Hash (APH)**.

During startup or session handshake, the runtime extends the APH into PCR 15:
$$\text{PCR}_{15} = \text{SHA256}(\text{PCR}_{15} \parallel \text{APH})$$

### 3.2 TEE Attestation Quote

To verify the agent's identity, the host TPM/TEE generates an **Attestation Quote** containing:
1. The values of PCR 10 (System/Binary state) and PCR 15 (Cognitive state).
2. A random challenge `nonce` provided by the verifier to prevent replay attacks.
3. The signature of the TPM's hardware-backed Attestation Identity Key (AIK).

Verifiers crosscheck this quote against the known registry and the golden PCR values of the hardware node. If any instruction is altered, PCR 15 will diverge, causing the attestation to fail.

---

## 4. Cryptographic Execution Receipts

Every action taken by an autonomous agent (e.g., executing a system command, making an outbound API call, modifying data) MUST be recorded by the securing runtime (e.g., Atlas Proxy) in a cryptographically signed **Execution Receipt**.

This receipt allows auditors to prove retroactively that a specific version of an agent (defined by its APH) executed a specific command in a verified hardware environment.

### 4.1 Receipt Structure

```json
{
  "receipt_id": "urn:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
  "timestamp": "2026-07-04T08:42:00Z",
  "agent_id": "agent://example/mybot",
  "agent_public_key": "ed25519:hArTvbITJ2jirL...",
  "aph": "sha256:d8b2d184...",
  "observability": {
    "provider": "langfuse",
    "trace_id": "trace_b7c2d9a1-...",
    "trace_hash": "sha256:a1b2c3d4..."
  },
  "host_attestation": {
    "node_id": "node://atlas-grid/us-east-1",
    "pcrs": {
      "10": "d3a246...",
      "15": "f48c1b..."
    },
    "signature": "base64_aik_signature_here"
  },
  "action": {
    "type": "tool_call",
    "target": "execute_command",
    "payload": {
      "command": "git push origin main"
    },
    "reversibility": "irreversible"
  },
  "result": {
    "status": "success",
    "output_hash": "sha256:a94a8fe5ccb19ba61c4c0873d391e987982fbbd3"
  },
  "signature": "base64_proxy_signature_here"
}
```

The securing runtime MUST populate `action.reversibility` by copying the `reversibility` class declared on the invoked tool in the Cognitive Manifest (Section 2.1). The runtime MUST NOT accept a reversibility class supplied by the agent at runtime. If the invoked tool declares no reversibility class, the runtime MUST record `action.reversibility` as `irreversible` (fail-closed). Because `action.reversibility` is part of the signed receipt payload, it is covered by the proxy `signature` and cannot be stripped or downgraded after the fact.

### 4.2 Merkle Audit Ledger

The Atlas Proxy aggregates execution receipts into a local append-only Merkle Tree.
* The root hash of this tree is periodically published to the Creduent Registry or a public ledger.
* This makes the history of agent actions completely tamper-proof. An auditor can verify the inclusion of any receipt using a standard Merkle proof.

Where receipts are linked into a call chain, a verifier over the ledger MUST compute the chain's governing reversibility class as the worst-case (least-reversible) `action.reversibility` present across the linked receipts, under the order `read-only` < `reversible` < `external-reversible` < `irreversible`. Individually reversible steps that compose into an irreversible end state are therefore governed as `irreversible` from the start of the chain. Any human-approval or gating policy keyed on reversibility MUST evaluate against this worst-case class, not the per-receipt class.

### 4.3 Reversibility Conformance

An implementation conforms to the reversibility requirements of this section if:
1. every entry in a Cognitive Manifest's `tools` carries a `reversibility` value in `{read-only, reversible, external-reversible, irreversible}`;
2. every Execution Receipt's `action.reversibility` equals the invoked tool's declared class, or `irreversible` when the tool declares none;
3. no receipt's `action.reversibility` is derived from agent-supplied input;
4. a chain verifier returns the worst-case class across linked receipts, per Section 4.2.

Test vectors SHOULD include: a receipt whose `action.reversibility` was downgraded relative to the invoked tool's declared class (which MUST be rejected), and a chain of individually reversible receipts that reaches an `irreversible` step (which MUST be governed as `irreversible`).

---

## 5. Dynamic Identity Lifecycle & Revocation

Since agents are dynamic, their identity and permissions must support real-time rotation and instantaneous revocation.

```
                  +──────────────────────────+
                  |  Admin / Security Node   |
                  +──────────────────────────+
                               │
                1. Detect anomaly or update prompt
                               │
                               ▼
                  +──────────────────────────+
                  |    Creduent Registry     |
                  |                          |
                  |    - Level -> "revoked"  |
                  |    - Notify Hook         |
                  +──────────────────────────+
                               │
                  2. Webhook / Polling Sync
                               │
                               ▼
                  +──────────────────────────+
                  |    Atlas Proxy / Node    |
                  |                          |
                  |   - Server connection    |
                  |   - Reject agent calls   |
                  +──────────────────────────+
```

### 5.1 Re-attesting on Prompt Upgrades

When a developer updates an agent's system prompt or toolset:
1. The SDK automatically computes the new APH.
2. The agent submits a signed renewal payload to `POST /renew` containing the new APH.
3. The registry verifies the signature, validates that the changes match the developer's authorized scope, and issues an updated attestation containing the new APH.

### 5.2 Real-time Revocation API

If an agent is compromised, hijacked via prompt injection, or behaves maliciously, its identity MUST be revoked instantly.

#### 5.2.1 Registry Revocation Command
```http
DELETE /revoke/{agent_id}
Headers:
  CREDUENT-ADMIN-KEYS: <comma-separated-admin-public-keys>
  CREDUENT-ADMIN-SIGNATURES: <comma-separated-signatures>
  CREDUENT-ADMIN-TIMESTAMP: <iso8601-timestamp>
```

#### 5.2.2 Downstream Enforcement
On receiving a revocation request:
1. The Registry sets the agent's attestation status to `"revoked"`.
2. The Registry publishes an instant notification to all registered webhooks for that agent, notifying the hosting Atlas Nodes.
3. Atlas Proxy intercepts this signal:
   - It severs any active SSH/API sessions associated with the `agent_id`.
   - It rejects any incoming requests signed by the revoked agent's public key.
   - It denies the agent access to any secured APIs.

---

## 6. Security Considerations

* **SSRF Protection:** When validating external cognitive manifests, registries MUST block resolution of private, loopback, or cloud metadata IP addresses to prevent Server-Side Request Forgery.
* **Prompt Replay Attacks:** Attestations must include a cryptographically random, registry-generated challenge nonce. If an agent tries to replay a previous attestation or quote, the mismatch in the challenge nonce will cause verification to fail.
* **Side-channel and Timing Attacks:** Canonicalization and signature verification MUST execute in constant-time to prevent timing-based extraction of private keys.

---

## 7. Changelog

| Version | Date | Notes |
|:---|:---|:---|
| 0.1 | 2026-07-04 | Initial draft. Introduced Agent Prompt Hash (APH), hardware attestation mapping, execution receipts, and active revocation flow. |
| 0.2 | 2026-07-12 | Added action reversibility class: design-time tool declaration (folded into APH), proxy-copied receipt field (fail-closed on unclassified), worst-case-across-chain ledger rule (Section 4.2), and conformance vectors (Section 4.3). |
