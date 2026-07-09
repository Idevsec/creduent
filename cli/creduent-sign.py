#!/usr/bin/env python3
import sys
import os
import json
import base64
import argparse
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

# Add parent directory to path to allow importing from creduent package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from creduent.crypto import canonicalize


def generate_keys():
    print("[+] Generating new Ed25519 key pair...")
    private_key = ed25519.Ed25519PrivateKey.generate()

    # Save Private Key in PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open("private_key.pem", "wb") as f:
        f.write(private_pem)
    print("[SUCCESS] Private key saved to private_key.pem (KEEP THIS SECRET!)")

    # Extract Public Key and print in Creduent format
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    )
    public_b64 = base64.b64encode(public_bytes).decode("utf-8")
    print("\n" + "=" * 50)
    print("YOUR PUBLIC KEY (Add this to your agent.json):")
    print(f"ed25519:{public_b64}")
    print("=" * 50)


def sign_document(key_path, input_path, output_path):
    if not os.path.exists(key_path):
        print(f"[-] Error: Key file not found at {key_path}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(input_path):
        print(f"[-] Error: Input document not found at {input_path}", file=sys.stderr)
        sys.exit(1)

    # Read Ed25519 private key
    print(f"[+] Loading private key from {key_path}...")
    with open(key_path, "rb") as f:
        key_bytes = f.read()

    try:
        private_key = serialization.load_pem_private_key(key_bytes, password=None)
        if not isinstance(private_key, ed25519.Ed25519PrivateKey):
            raise ValueError("Key is not an Ed25519 private key")
    except Exception as e:
        print(f"[-] Error parsing private key: {e}", file=sys.stderr)
        sys.exit(1)

    # Read draft agent.json
    print(f"[+] Reading draft document from {input_path}...")
    with open(input_path, "r", encoding="utf-8") as f:
        try:
            doc = json.load(f)
        except Exception as e:
            print(f"[-] Error: Invalid JSON in input file: {e}", file=sys.stderr)
            sys.exit(1)

    # Normalize fields
    if "version" not in doc:
        doc["version"] = "1.0"
    if doc["version"] == "1.0" and "issued_at" not in doc:
        doc["issued_at"] = (
            datetime.now(timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z")
        )

    # Remove signature before signing
    doc.pop("signature", None)

    # Canonicalize document
    print("[+] Canonicalizing document using JCS...")
    try:
        canonical_str = canonicalize(doc)
        canonical_bytes = canonical_str.encode("utf-8")
    except Exception as e:
        print(f"[-] Error during JCS canonicalization: {e}", file=sys.stderr)
        sys.exit(1)

    # Sign payload
    print("[+] Cryptographically signing canonical bytes...")
    signature_bytes = private_key.sign(canonical_bytes)
    signature_b64 = base64.b64encode(signature_bytes).decode("utf-8")

    # Append signature and save
    doc["signature"] = signature_b64

    print(f"[+] Writing signed document to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    print("[SUCCESS] Successfully signed and generated agent.json!")


def main():
    parser = argparse.ArgumentParser(
        description="Creduent Protocol - agent.json Signing CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommand to execute")

    # generate-keys parser
    subparsers.add_parser(
        "generate-keys", help="Generate Ed25519 private key and public key string"
    )

    # sign parser
    sign_parser = subparsers.add_parser("sign", help="Sign a draft agent.json payload")
    sign_parser.add_argument(
        "--key", required=True, help="Path to Ed25519 private_key.pem"
    )
    sign_parser.add_argument(
        "--input", required=True, help="Path to unsigned draft JSON file"
    )
    sign_parser.add_argument(
        "--output", required=True, help="Path to write the signed JSON output file"
    )

    args = parser.parse_args()

    if args.command == "generate-keys":
        generate_keys()
    elif args.command == "sign":
        sign_document(args.key, args.input, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
