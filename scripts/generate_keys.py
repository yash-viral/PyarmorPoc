#!/usr/bin/env python3
"""
scripts/generate_keys.py

Generate an RSA keypair for signing/verifying licenses.

- private_key.pem → kept on the FastAPI server (NEVER share)
- public_key.pem  → distributed with the client app

Usage:
    python scripts/generate_keys.py
"""

import os
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# === Configuration ===
BASE_DIR = Path(__file__).resolve().parent.parent
KEYS_DIR = BASE_DIR / "keys"
PRIVATE_KEY_PATH = KEYS_DIR / "private_key.pem"
PUBLIC_KEY_PATH = KEYS_DIR / "public_key.pem"

def generate_keys():
    KEYS_DIR.mkdir(exist_ok=True)
    
    print(f"🔐 Generating RSA keypair in {KEYS_DIR}...")

    # Generate private key (2048-bit RSA)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Serialize private key (no encryption for PoC)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,  # PKCS#1
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize public key
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Write keys
    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(private_pem)
    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(public_pem)

    try:
        PRIVATE_KEY_PATH.chmod(0o600)
    except Exception:
        pass

    print(f"✅ Keys generated successfully:")
    print(f"   Private key: {PRIVATE_KEY_PATH}")
    print(f"   Public key:  {PUBLIC_KEY_PATH}")

if __name__ == "__main__":
    generate_keys()
