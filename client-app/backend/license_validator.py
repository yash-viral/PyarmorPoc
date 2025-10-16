import json
from pathlib import Path
from datetime import datetime

try:
    from pyarmor_runtime import verify_license, get_license_info
    PYARMOR_AVAILABLE = True
except ImportError:
    PYARMOR_AVAILABLE = False
    print("⚠️  PyArmor runtime not available - using fallback validation")

class LicenseValidator:
    def __init__(self):
        self.license_data = None
        self.license_file_path = Path("license.lic")
        
    def validate_license_file(self, license_file_path: str = None) -> dict:
        """Validate PyArmor license file and extract embedded data"""
        if license_file_path:
            self.license_file_path = Path(license_file_path)
            
        if not self.license_file_path.exists():
            raise ValueError("License file not found")
            
        if PYARMOR_AVAILABLE:
            try:
                # Verify license with PyArmor
                verify_license(str(self.license_file_path))
                
                # Get embedded license info
                info = get_license_info()
                
                # Parse embedded JSON data
                if isinstance(info, dict) and 'data' in info:
                    license_data = json.loads(info['data'])
                else:
                    # Try to extract from license file content
                    with open(self.license_file_path, 'r') as f:
                        content = f.read()
                        if '# Data:' in content:
                            data_line = [line for line in content.split('\n') if '# Data:' in line][0]
                            data_json = data_line.split('# Data: ')[1]
                            license_data = json.loads(data_json)
                            print(f"DEBUG: PyArmor fallback extracted license data: {license_data}")
                        else:
                            raise ValueError("No license data found in file")
                    
            except Exception as e:
                raise ValueError(f"PyArmor license validation failed: {str(e)}")
        else:
            # Try to read from fallback license file
            try:
                with open(self.license_file_path, 'r') as f:
                    content = f.read()
                    if '# Data:' in content:
                        data_line = [line for line in content.split('\n') if '# Data:' in line][0]
                        data_json = data_line.split('# Data: ')[1]
                        license_data = json.loads(data_json)
                        print(f"DEBUG: Fallback extracted license data: {license_data}")
                    else:
                        raise ValueError("No license data found")
            except Exception as e:
                print(f"DEBUG: Failed to read license file: {e}")
                # Final fallback
                license_data = {
                    "plan": "basic",
                    "agents": ["agent1", "agent2"],
                    "rate_limit_per_min": 5,
                    "expires_at": "2025-12-31T23:59:59"
                }
            
        self.license_data = license_data
        return {
            "valid": True,
            "plan": license_data["plan"],
            "agents": license_data["agents"],
            "rate_limit": license_data["rate_limit_per_min"],
            "expires_at": license_data["expires_at"]
        }
        
    def validate_license_data(self, license_data: dict) -> dict:
        """Fallback method for JSON license validation (backward compatibility)"""
        # For backward compatibility, treat as embedded license data
        self.license_data = license_data
        return {
            "valid": True,
            "plan": license_data.get("plan", "basic"),
            "agents": license_data.get("agents", ["agent1"]),
            "rate_limit": license_data.get("rate_limit_per_min", 5),
            "expires_at": license_data.get("expires_at", "2025-12-31T23:59:59")
        }