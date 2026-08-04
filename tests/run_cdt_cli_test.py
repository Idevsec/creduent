import json
import subprocess
from tests.test_cdt import generate_keypair, issue_cdt

alice_priv, alice_pub = generate_keypair()
bob_priv, bob_pub = generate_keypair()

# Create dummy registry
registry = {
    "agent://alice/agent": "tests/dummy_alice.json"
}
with open("tests/dummy_registry.json", "w") as f:
    json.dump(registry, f)

# Create dummy agent.json for Alice
alice_agent = {
    "version": "1.0",
    "agent_id": "agent://alice/agent",
    "owner": "Alice",
    "public_key": f"ed25519:{alice_pub}",
    "endpoint": "http://localhost",
    "capabilities": ["*"],
    "signature": "dummy" 
}
with open("tests/dummy_alice.json", "w") as f:
    json.dump(alice_agent, f)

cdt = issue_cdt(
    delegator_privkey=alice_priv,
    delegator_id="agent://alice/agent",
    delegate_id="agent://bob/agent",
    delegate_public_key=bob_pub,
    capabilities=["*"],
    reversibility_tier="REVERSIBLE"
)

with open("tests/dummy_cdt.json", "w") as f:
    json.dump(cdt, f)

# Run CLI
result = subprocess.run([".venv/bin/python", "cli/creduent-verify.py", "verify", "tests/dummy_cdt.json", "--cdt", "--registry", "tests/dummy_registry.json"], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(result.stderr)
    exit(1)
