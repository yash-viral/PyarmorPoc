#!/usr/bin/env python3
"""
Test current license file decryption
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "client-app" / "backend"))

from crypto_client import decrypt_license_data

def test_current_license():
    print("Testing current license file decryption")
    
    # Test with the encrypted data from our test
    encrypted_data = "eyJkYXRhIjogImV5SmhaMlZ1ZEhNaU9pQmJJbUZuWlc1ME1TSXNJQ0poWjJWdWRESWlYU3dnSW1SMWNtRjBhVzl1WDJSaGVYTWlPaUF6TUM0d0xDQWlaWGh3YVhKbGMxOWhkQ0k2SUNJeU1ESTFMVEV4TFRFMlZEQTNPak13T2pBMExqRXlNRFV3T1Nzd01Eb3dNQ0lzSUNKdFlXTm9hVzVsWDJsa0lqb2dJblJsYzNRdGJXRmphR2x1WlMweE1qTWlMQ0FpY0d4aGJpSTZJQ0p3Y204aUxDQWljbUYwWlY5c2FXMXBkRjl3WlhKZmJXbHVJam9nTVRWOSIsICJzaWduYXR1cmUiOiAiaVI5ODJtekp0eUIxRlhPNU9ic0ZYUy9RQ0dFemlDaVNCSDVQUFhnUjFyMkFldXZHR1grT0lDaHVPUzhUZlMyTCs1YUwxQ29tNUNQRVc3ZEtJMXNxR084cUo5SXhpLzliL0dqSnpQUmhETUJKdmRrS2IrTW9KL3FJT1ZmWnhsSEc4ekFxLzZOcFB0S2RsaVduVzZEbHdaRHZtVlBCMVEzbzg3UThJK1Uwd0tzUGNvOTRieDlBMVRySHBOK0xEaXVkRnEzbElJdlFhVDFiTjJMWEpYY1dUeEJnc3dNMkRQdVRHM2hCUjNhQzdrSWVpczRTUGRVN1JZZEY2WnRLb3RMT2dUOW5PNWhTVkI0Y2JlZWdVMFZ3d3JZa3VDaG50K242VDh6bGREMDRNdGxzdnZLTFM0T0xKdkJjcWJ4MkRVTnhySVZaTmRYdjV5V25EWHp3N2YyUGZBPT0ifQ=="
    
    try:
        decrypted_data = decrypt_license_data(encrypted_data)
        print(f"Successfully decrypted: {decrypted_data}")
        return True
    except Exception as e:
        print(f"Decryption failed: {e}")
        return False

if __name__ == "__main__":
    success = test_current_license()
    sys.exit(0 if success else 1)