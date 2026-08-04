import base64
import base58

def generate_did_document(agent_id_or_uri: str, attestation_data: dict) -> dict:
    """
    Generates a W3C DID Document from a Creduent agent attestation.
    """
    if agent_id_or_uri.startswith("agent://"):
        parts = agent_id_or_uri[len("agent://"):].split("/")
        if len(parts) == 2:
            namespace, name = parts
            did_uri = f"did:creduent:{namespace}:{name}"
        else:
            did_uri = agent_id_or_uri
    elif agent_id_or_uri.startswith("did:creduent:"):
        did_uri = agent_id_or_uri
    else:
        did_uri = f"did:creduent:{agent_id_or_uri}"
        
    # Handle v2 or v1 format
    identity = attestation_data.get("identity", {}) if attestation_data.get("version") == "2.0" else attestation_data
    endpoint = identity.get("endpoint") or identity.get("domain")
    if endpoint and not endpoint.startswith("http"):
        endpoint = f"https://{endpoint}"
    
    did_doc = {
        "@context": [
            "https://www.w3.org/ns/did/v1",
            "https://w3id.org/security/suites/ed25519-2020/v1"
        ],
        "id": did_uri,
        "verificationMethod": [],
        "authentication": [],
        "assertionMethod": []
    }
    
    if endpoint:
        did_doc["service"] = [
            {
                "id": f"{did_uri}#agent-endpoint",
                "type": "CreduentAgentService",
                "serviceEndpoint": endpoint
            }
        ]
    
    keys = identity.get("keys", [])
    if not keys and "public_key" in identity:
        keys = [
            {
                "id": "key-1",
                "type": "ed25519",
                "public_key": identity.get("public_key"),
                "status": "active"
            }
        ]

    for key in keys:
        if key.get("type") == "ed25519" and key.get("status", "active") == "active":
            key_id = key.get("id", "key-1")
            verification_method_id = f"{did_uri}#{key_id}"
            
            pub_key_str = key.get("public_key", "")
            if pub_key_str.startswith("ed25519:"):
                pub_key_b64 = pub_key_str[len("ed25519:"):]
            else:
                pub_key_b64 = pub_key_str
                
            try:
                # Add padding if necessary
                pub_key_b64_padded = pub_key_b64 + "=" * ((4 - len(pub_key_b64) % 4) % 4)
                pub_key_bytes = base64.b64decode(pub_key_b64_padded)
                # Multicodec for ed25519-pub is 0xed01. In varint, that's \xed\x01
                multicodec_bytes = b"\xed\x01" + pub_key_bytes
                multibase_str = "z" + base58.b58encode(multicodec_bytes).decode('utf-8')
            except Exception:
                # Fallback if decoding fails
                multibase_str = "zFallback"
                
            verification_method = {
                "id": verification_method_id,
                "type": "Ed25519VerificationKey2020",
                "controller": did_uri,
                "publicKeyMultibase": multibase_str
            }
            did_doc["verificationMethod"].append(verification_method)
            did_doc["authentication"].append(verification_method_id)
            did_doc["assertionMethod"].append(verification_method_id)
            
    return did_doc
