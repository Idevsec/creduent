# Contributing to the Creduent Open Protocol

Thank you for your interest in contributing to the Creduent Open Protocol! This guide covers how to contribute to the protocol specification, reference implementations, schemas, and documentation.

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

---

## Contributor Licensing (DCO)

By submitting a Pull Request, you certify that your contribution is made under the terms of the [Developer Certificate of Origin](https://developercertificate.org). Add a sign-off to every commit:

```bash
git commit -s -m "your commit message"
```

This adds a `Signed-off-by: Your Name <your@email.com>` line to your commit. Pull Requests without a sign-off on every commit will not be merged.

---

## Ways to Contribute

- **Protocol Specification:** Propose changes or clarifications to `SPEC.md` or `schemas/`
- **Documentation:** Improve `README.md`, `FAQ.md`, `QUICKSTART.md`, `EXAMPLES.md`, or `ROADMAP.md`
- **Registry & API:** Contribute to the reference registry implementation in `registry/` or `api/`
- **Bug Reports:** Report inconsistencies or errors in the specification or reference code

---

## Development Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/idevsec/creduent.git
    cd creduent
    ```

2. **Install Python Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Test Suite:**

    ```bash
    python -m pytest --tb=short
    ```

---

## Code Guidelines & Protocol Integrity

Please ensure all contributions align with the core Creduent protocol security guarantees:

- **Ed25519 Signatures:** All credential signing and verification must use Ed25519 keypairs.
- **Canonicalization:** All payloads must be serialized using RFC 8785 JSON Canonicalization Scheme (JCS) before signing or verifying.
- **Decentralized Verification:** Verification must work locally without trusting a remote server's assertion.
- **Schema Compliance:** Any new credential types must include corresponding JSON Schema definitions in `schemas/`.

---

## Git Workflow & Branching Strategy

### Branch Naming Conventions

- **Features:** `feature/` (e.g., `feature/federation-v2-support`)
- **Bugfixes:** `bugfix/` (e.g., `bugfix/schema-validation-edge-case`)
- **Documentation:** `docs/` (e.g., `docs/faq-update`)
- **Refactoring:** `refactor/` (e.g., `refactor/registry-api-cleanup`)

### Pull Request Process

1. Create a branch from `main` following the naming conventions above.
2. Make your changes and verify them locally with the test suite.
3. Push your branch to GitHub.
4. Open a Pull Request against the `main` branch.
5. Fill out the Pull Request template completely.
6. Ensure all CI checks pass and request review from maintainers.

---

## Specification Change Process

Changes to the protocol specifications (files in the `standards/` directory and schemas in the `schemas/` directory) follow a strict review process to maintain backward compatibility:

1. **Open an Issue First:** Do not submit a Pull Request for a specification change without a linked discussion issue.
2. **Review Cycle:** Specification Pull Requests require review and approval from at least two core maintainers.
3. **Backward Compatibility:** Proposals must not break existing attestation formats or registry endpoints unless a new specification version is explicitly declared.

---

## Commit Message Conventions

We follow the Conventional Commits specification. Commit messages must be structured as follows:

```text
<type>(<scope>): <description>

[optional body]
```

Allowed types include:
- `feat`: A new protocol feature or SDK capability.
- `fix`: A bug fix in the reference implementation or schema.
- `docs`: Documentation updates.
- `spec`: Changes to specification drafts.
- `refactor`: Code changes that do not alter behavior.

---

## Ecosystem Contribution Directory

Because the Creduent Protocol is split across multiple specialized repositories, we maintain a centralized roadmap but distribute active development tasks across the respective codebases. If you want to contribute, identify your preferred language/tool and refer to the hotspots below:

### Creduent CLI (`creduent-cli`)
* **Focus:** Developer utilities, registry command interfaces, and local validation tools.
* **Active Tasks:**
  * **[Good First Issue] Output Formatting:** Add `--format json` and `--format table` options to `creduent discover` and `creduent resolve` commands.
  * **[Intermediate] Shell Autocomplete:** Write shell autocomplete generator scripts for bash, zsh, and powershell.
  * **[Intermediate] Interactive Sign Wizard:** Build an interactive prompt runner for the `creduent init` and signing steps to guide developers visually.

### JS/TS SDK (`creduent-js`)
* **Focus:** Zero-dependency edge-compatible client verification, JS/TS framework integrations.
* **Active Tasks:**
  * **[Intermediate] Framework Integrations:** Author native helper middleware/tools for **LangChain JS** and **LlamaIndex TS** (similar to our Python integration adapters).
  * **[Intermediate] Local Cache Tuning:** Implement local LRU caching (5-min default TTL) inside the verification pipeline in `src/verifier.ts` to minimize registry roundtrips.
  * **[Advanced] Delegation (CREDUENT-007):** Help implement recursive chain validation in `verifyDelegationChain()` mapping delegates to parent delegator key verification.

### Python SDK (`creduent-python`)
* **Focus:** Core python client tools, agentic AI frameworks integrations (CrewAI, AutoGen).
* **Active Tasks:**
  * **[Intermediate] Framework Integrations:** Expand support for LlamaIndex Python, Google ADK (Agent Development Kit), and Semantic Kernel.
  * **[Intermediate] Verifier Caching:** Implement thread-safe local caching wrappers for agent attestation lookups.
  * **[Advanced] Delegation (CREDUENT-007):** Implement the `sign_delegation` reference method to generate JCS-signed delegation tokens and bind to trace contexts.

To begin, clone the respective child repository and refer to their local `CONTRIBUTING.md` for specific environment setup and local verification/testing guidelines.

