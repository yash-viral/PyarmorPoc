#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path

def run_protected_client():
    dist_dir = Path("dist")
    
    # Auto-protect if not already protected
    if not dist_dir.exists():
        print("🔒 Protecting client first...")
        result = subprocess.run([sys.executable, "protect_client.py"])
        if result.returncode != 0:
            print("❌ Protection failed")
            return False
    
    print("🚀 Starting PyArmor-protected client backend...")
    
    # Run the protected main.py without reload (PyArmor doesn't support reload)
    cmd = [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8001"]
    
    try:
        subprocess.run(cmd, cwd=dist_dir)
    except KeyboardInterrupt:
        print("\n👋 Client backend stopped.")
    
    return True

if __name__ == "__main__":
    run_protected_client()