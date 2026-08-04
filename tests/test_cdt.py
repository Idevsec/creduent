import base64
import pytest
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

from registry.cdt import issue_cdt, verify_cdt, verify_delegation_chain, MAX_DELEGATION_DEPTH
from registry.main import app

def generate_keypair():
    privkey = ed25519.Ed25519PrivateKey.generate()
    pubkey = privkey.public_key()
    pub_bytes = pubkey.public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    )
    pub_b64 = base64.b64encode(pub_bytes).decode("utf-8")
    return privkey, pub_b64

def test_issue_and_verify_cdt():
    delegator_priv, delegator_pub = generate_keypair()
    delegate_priv, delegate_pub = generate_keypair()
    
    cdt = issue_cdt(
        delegator_privkey=delegator_priv,
        delegator_id="agent://alice",
        delegate_id="agent://bob",
        delegate_public_key=f"ed25519:{delegate_pub}",
        capabilities=["registry:read", "repo:commit"],
        reversibility_tier="REVERSIBLE",
        tools=["git"],
        limits={"rate": 10},
        intent_hash="abc123hash"
    )
    
    # Verify the CDT signature
    is_valid, msg = verify_cdt(cdt, delegator_pub)
    assert is_valid, msg
    
    # Tamper with the token
    tampered_cdt = cdt.copy()
    tampered_cdt["constraints"] = cdt["constraints"].copy()
    tampered_cdt["constraints"]["capabilities"] = ["*"]
    
    is_valid_tampered, _ = verify_cdt(tampered_cdt, delegator_pub)
    assert not is_valid_tampered
    
    # Test expiration
    expired_cdt = cdt.copy()
    expired_at = datetime.now(timezone.utc) - timedelta(hours=1)
    expired_cdt["expires_at"] = expired_at.isoformat(timespec="seconds").replace("+00:00", "Z")
    
    # Resign expired CDT
    from creduent.crypto import canonicalize
    obj_copy = expired_cdt.copy()
    obj_copy.pop("signature", None)
    sig_bytes = delegator_priv.sign(canonicalize(obj_copy).encode("utf-8"))
    expired_cdt["signature"] = base64.b64encode(sig_bytes).decode("utf-8")
    
    is_valid_expired, msg = verify_cdt(expired_cdt, delegator_pub)
    assert not is_valid_expired
    assert msg == "Token expired"

def test_verify_delegation_chain():
    alice_priv, alice_pub = generate_keypair()
    bob_priv, bob_pub = generate_keypair()
    charlie_priv, charlie_pub = generate_keypair()
    
    # Chain: Alice -> Bob -> Charlie
    # Alice gives Bob [*]
    cdt1 = issue_cdt(
        delegator_privkey=alice_priv,
        delegator_id="agent://alice",
        delegate_id="agent://bob",
        delegate_public_key=bob_pub,
        capabilities=["*"],
        reversibility_tier="REVERSIBLE"
    )
    
    # Bob gives Charlie ["repo:commit"]
    cdt2 = issue_cdt(
        delegator_privkey=bob_priv,
        delegator_id="agent://bob",
        delegate_id="agent://charlie",
        delegate_public_key=charlie_pub,
        capabilities=["repo:commit"],
        reversibility_tier="REVERSIBLE"
    )
    
    chain = [cdt1, cdt2]
    is_valid, msg = verify_delegation_chain(chain, alice_pub)
    assert is_valid, msg

def test_chain_capability_escalation():
    alice_priv, alice_pub = generate_keypair()
    bob_priv, bob_pub = generate_keypair()
    charlie_priv, charlie_pub = generate_keypair()
    
    # Alice gives Bob ["repo:read"]
    cdt1 = issue_cdt(
        delegator_privkey=alice_priv,
        delegator_id="agent://alice",
        delegate_id="agent://bob",
        delegate_public_key=bob_pub,
        capabilities=["repo:read"],
        reversibility_tier="REVERSIBLE"
    )
    
    # Bob tries to give Charlie ["repo:write"] (escalation!)
    cdt2 = issue_cdt(
        delegator_privkey=bob_priv,
        delegator_id="agent://bob",
        delegate_id="agent://charlie",
        delegate_public_key=charlie_pub,
        capabilities=["repo:write"],
        reversibility_tier="REVERSIBLE"
    )
    
    chain = [cdt1, cdt2]
    is_valid, msg = verify_delegation_chain(chain, alice_pub)
    assert not is_valid
    assert "Capability escalation" in msg

def test_chain_reversibility_escalation():
    alice_priv, alice_pub = generate_keypair()
    bob_priv, bob_pub = generate_keypair()
    charlie_priv, charlie_pub = generate_keypair()
    
    # Alice gives Bob REVERSIBLE
    cdt1 = issue_cdt(
        delegator_privkey=alice_priv,
        delegator_id="agent://alice",
        delegate_id="agent://bob",
        delegate_public_key=bob_pub,
        capabilities=["*"],
        reversibility_tier="REVERSIBLE"
    )
    
    # Bob tries to give Charlie IRREVERSIBLE (escalation from 1 to 2!)
    cdt2 = issue_cdt(
        delegator_privkey=bob_priv,
        delegator_id="agent://bob",
        delegate_id="agent://charlie",
        delegate_public_key=charlie_pub,
        capabilities=["*"],
        reversibility_tier="IRREVERSIBLE"
    )
    
    chain = [cdt1, cdt2]
    is_valid, msg = verify_delegation_chain(chain, alice_pub)
    assert not is_valid
    assert "Reversibility tier escalation" in msg

def test_chain_cycle_detection():
    alice_priv, alice_pub = generate_keypair()
    bob_priv, bob_pub = generate_keypair()
    
    cdt1 = issue_cdt(
        delegator_privkey=alice_priv,
        delegator_id="agent://alice",
        delegate_id="agent://bob",
        delegate_public_key=bob_pub,
        capabilities=["*"],
        reversibility_tier="REVERSIBLE"
    )
    
    # Bob delegates back to Alice (cycle!)
    cdt2 = issue_cdt(
        delegator_privkey=bob_priv,
        delegator_id="agent://bob",
        delegate_id="agent://alice",
        delegate_public_key=alice_pub,
        capabilities=["*"],
        reversibility_tier="REVERSIBLE"
    )
    
    chain = [cdt1, cdt2]
    is_valid, msg = verify_delegation_chain(chain, alice_pub)
    assert not is_valid
    assert "Cycle detected" in msg

def test_chain_max_depth():
    keys = [generate_keypair() for _ in range(MAX_DELEGATION_DEPTH + 2)]
    
    chain = []
    for i in range(MAX_DELEGATION_DEPTH + 1):
        cdt = issue_cdt(
            delegator_privkey=keys[i][0],
            delegator_id=f"agent://agent{i}",
            delegate_id=f"agent://agent{i+1}",
            delegate_public_key=keys[i+1][1],
            capabilities=["*"],
            reversibility_tier="REVERSIBLE"
        )
        chain.append(cdt)
        
    is_valid, msg = verify_delegation_chain(chain, keys[0][1])
    assert not is_valid
    assert "exceeds MAX_DELEGATION_DEPTH" in msg

client = TestClient(app)

def test_api_verify_delegation(monkeypatch):
    alice_priv, alice_pub = generate_keypair()
    bob_priv, bob_pub = generate_keypair()
    
    # Mock registry so it returns Alice's public key
    import registry.main
    original_get_attestation = registry.main.get_attestation
    
    def mock_get_attestation(agent_id):
        if agent_id == "agent://alice":
            return {
                "agent_id": "agent://alice",
                "public_key": f"ed25519:{alice_pub}"
            }
        return None
        
    monkeypatch.setattr(registry.main, "get_attestation", mock_get_attestation)
    
    cdt1 = issue_cdt(
        delegator_privkey=alice_priv,
        delegator_id="agent://alice",
        delegate_id="agent://bob",
        delegate_public_key=bob_pub,
        capabilities=["repo:write"],
        reversibility_tier="REVERSIBLE"
    )
    
    response = client.post("/registry/verify-delegation", json={
        "chain": [cdt1]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "valid"
    assert data["final_delegate"] == "agent://bob"
    assert data["granted_capabilities"] == ["repo:write"]
    
    # Test invalid root delegator
    cdt_invalid_root = issue_cdt(
        delegator_privkey=alice_priv,
        delegator_id="agent://unknown",
        delegate_id="agent://bob",
        delegate_public_key=bob_pub,
        capabilities=["repo:write"],
        reversibility_tier="REVERSIBLE"
    )
    
    response2 = client.post("/registry/verify-delegation", json={
        "chain": [cdt_invalid_root]
    })
    
    assert response2.status_code == 404
