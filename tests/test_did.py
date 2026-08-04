import pytest
from registry.did import generate_did_document

def test_generate_did_document_v2():
    attestation = {
        "version": "2.0",
        "identity": {
            "agent_id": "agent://example/myagent",
            "domain": "example.com",
            "endpoint": "https://api.example.com",
            "keys": [
                {
                    "id": "key-1",
                    "type": "ed25519",
                    "public_key": "ed25519:VGVzdEtleVB1YmxpY0Jhc2U2NA==",
                    "status": "active"
                }
            ]
        }
    }
    
    did_doc = generate_did_document("agent://example/myagent", attestation)
    assert did_doc["id"] == "did:creduent:example:myagent"
    assert did_doc["service"][0]["serviceEndpoint"] == "https://api.example.com"
    assert did_doc["verificationMethod"][0]["controller"] == "did:creduent:example:myagent"
    assert did_doc["verificationMethod"][0]["id"] == "did:creduent:example:myagent#key-1"
    assert did_doc["verificationMethod"][0]["type"] == "Ed25519VerificationKey2020"
    assert "publicKeyMultibase" in did_doc["verificationMethod"][0]

def test_generate_did_document_v1():
    attestation = {
        "agent_id": "agent://example/legacy",
        "domain": "legacy.com",
        "public_key": "ed25519:TGVnYWN5UHVibGljS2V5",
    }
    
    did_doc = generate_did_document("agent://example/legacy", attestation)
    assert did_doc["id"] == "did:creduent:example:legacy"
    assert did_doc["service"][0]["serviceEndpoint"] == "https://legacy.com"
    assert did_doc["verificationMethod"][0]["id"] == "did:creduent:example:legacy#key-1"
