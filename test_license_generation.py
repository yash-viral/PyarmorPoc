#!/usr/bin/env python3
"""
Test license generation with RSA encryption
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from app.utils.crypto import encrypt_license_data
from datetime import datetime, timezone, timedelta

def test_license_generation():
    print("Testing License Generation with RSA Encryption")
    
    # Sample license data
    license_data = {
        "plan": "pro",
        "agents": ["agent1", "agent2"],
        "duration_days": 30.0,
        "rate_limit_per_min": 15,
        "expires_at": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
        "machine_id": "test-machine-123"
    }
    
    print(f"Original license data: {license_data}")
    
    try:
        # Encrypt license data
        encrypted_data = encrypt_license_data(license_data)
        print(f"Encrypted data: {encrypted_data[:100]}...")
        
        # Create test license file
        license_dir = Path("test_licenses")
        license_dir.mkdir(exist_ok=True)
        
        license_file = license_dir / "test_license.lic"
        license_content = f"""# PyArmor License
# Key: test-license-key
# EncryptedData: {encrypted_data}
# Expires: 2025-11-16"""
        
        license_file.write_text(license_content)
        print(f"Created encrypted license file: {license_file}")
        
        # Show file content
        print(f"\nLicense file content:")
        print(license_file.read_text()[:200] + "...")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_license_generation()
    sys.exit(0 if success else 1)