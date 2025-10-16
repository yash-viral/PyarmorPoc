#!/usr/bin/env python3
"""
PyArmor protection script for the client code
"""

import os
import subprocess
from pathlib import Path

def protect_client():
    """Protect client code with PyArmor"""
    client_dir = Path("client")
    dist_dir = Path("dist/client")
    
    # Create dist directory
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    # PyArmor command to obfuscate the client
    cmd = [
        "pyarmor", "gen",
        "--output", str(dist_dir),
        "--recursive",
        str(client_dir)
    ]
    
    print("🔒 Protecting client code with PyArmor...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Client code protected successfully!")
        print(f"Protected files saved to: {dist_dir}")
    else:
        print("❌ PyArmor protection failed:")
        print(result.stderr)
        
    return result.returncode == 0

if __name__ == "__main__":
    protect_client()