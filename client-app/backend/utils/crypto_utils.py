import json
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

PUBLIC_KEY_PEM = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArsScCPq95K943f8BvnFK
ntAOFVqXCsXKieizBaSAuf6ptqpZAJO67ADbZi2krt9AjcKfTMyDAG9t9C3seXXc
REv+gAyeh37dzT5BEQLIFYm4iBdb5LtIfiQeAXE2kQ39fAJoLW2oO4lGX/96VwAq
1AWq8ze0Ik/vWHJURC54tXpeebGILyRjZXDwztqmx2qNKlZT9IbbwBmBDxWE84Re
hJUdPAqM6+C0JHlzSYeOLIEYOyh5X9jbgNWsdGp1M09WbycMFCY6wUdM8xFFPTYC
BpNyLmh1e6rFxTeiNt+08JDKqTK9hZ5sGCsuap4MHg7phlQkcVhcSrb0O3Tbj/JI
QQIDAQAB
-----END PUBLIC KEY-----"""

class CryptoUtils:
    @staticmethod
    def load_public_key():
        return serialization.load_pem_public_key(PUBLIC_KEY_PEM.encode())
    
    @staticmethod
    def decrypt_license_data(encrypted_data: str) -> dict:
        public_key = CryptoUtils.load_public_key()
        
        try:
            combined_data = json.loads(base64.b64decode(encrypted_data))
            data_bytes = base64.b64decode(combined_data["data"])
            signature = base64.b64decode(combined_data["signature"])
            
            public_key.verify(
                signature,
                data_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            return json.loads(data_bytes.decode('utf-8'))
            
        except Exception as e:
            raise ValueError(f"License decryption failed: {str(e)}")
    
    @staticmethod
    def verify_license_signature(data: dict, signature_hex: str) -> bool:
        public_key = CryptoUtils.load_public_key()
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