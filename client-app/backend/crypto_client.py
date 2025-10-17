"""
client-app/backend/crypto_client.py

Client-side RSA decryption utilities with embedded public key.
This file will be protected by PyArmor to secure the public key.
"""

import json
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Embedded public key (protected by PyArmor)
PUBLIC_KEY_PEM = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu2NNaj5b5egBD4V8ZiY1
5/bNjmmP4Qeb4v8rUIHuwlK6GqIa5VuZRatDEiNOOnWb+FQahrBn2ZPZMmjLC2Zu
PbCiadCfetw9ZRk6Q31qRur6glVqM1V7vk4USEurfI4hgQ7X/yYkuXddCt//MIqy
e5pmYawpXNHaLwnC/U3uM+mEyB68zNFRXNorS2z4BN1CYINCugVMN6i7iRN7ix3q
Agah0zmNOlUBceo1Oa4dJi5LqFhEr5QDQpvV6d+ryvoBpJTlsDpdX/NSjM4eJHF0
7tMPAb/ZSjm5DC+yvv+2l44wtzf01dJv0YcyYkRzhpEuADiGB8QMibOPwXrYuXe4
lwIDAQAB
-----END PUBLIC KEY-----"""


def load_public_key():
    """Load the embedded public key"""
    return serialization.load_pem_public_key(PUBLIC_KEY_PEM.encode())


def decrypt_license_data(encrypted_data: str) -> dict:
    """Decrypt and verify license data with embedded public key"""
    public_key = load_public_key()
    
    try:
        # Decode the encrypted data
        combined_data = json.loads(base64.b64decode(encrypted_data))
        data_bytes = base64.b64decode(combined_data["data"])
        signature = base64.b64decode(combined_data["signature"])
        
        # Verify signature with public key
        public_key.verify(
            signature,
            data_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Return decrypted data
        return json.loads(data_bytes.decode('utf-8'))
        
    except Exception as e:
        raise ValueError(f"License decryption failed: {str(e)}")


def verify_license_signature(data: dict, signature_hex: str) -> bool:
    """Verify license signature with embedded public key"""
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