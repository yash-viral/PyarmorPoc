"""
app/utils/crypto.py

RSA key utilities for signing and verifying licenses.
Used by license_service to generate cryptographically signed license payloads.
"""

import json
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from app.config import PRIVATE_KEY_PATH, PUBLIC_KEY_PATH


# ---------------------------------------------------------
# Load RSA keys
# ---------------------------------------------------------
def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None)


def load_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())


# ---------------------------------------------------------
# Sign data with private key
# ---------------------------------------------------------
def sign_license_data(data: dict) -> str:
    private_key = load_private_key()
    message = json.dumps(data, sort_keys=True).encode("utf-8")

    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature.hex()


# ---------------------------------------------------------
# Verify signature with public key
# ---------------------------------------------------------
def verify_license_signature(data: dict, signature_hex: str) -> bool:
    public_key = load_public_key()
    message = json.dumps(data, sort_keys=True).encode("utf-8")
    signature = bytes.fromhex(signature_hex)

    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False
