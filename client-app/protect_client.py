#!/usr/bin/env python3
import subprocess
from pathlib import Path
import shutil

def protect_client():
    backend_dir = Path("backend")
    dist_dir = Path("dist")
    
    # Clean and create dist directory
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir(exist_ok=True)
    
    cmd = [
        "pyarmor", "gen",
        "--output", str(dist_dir),
        "--recursive",
        str(backend_dir)
    ]
    
    print("🔒 Protecting client backend with PyArmor...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Client backend protected successfully!")
        print(f"Protected files saved to: {dist_dir}")
        print("\n📝 Protected files:")
        for file in dist_dir.rglob("*.py"):
            print(f"  - {file}")
    else:
        print("❌ PyArmor protection failed:")
        print(result.stderr)
        
    return result.returncode == 0

if __name__ == "__main__":
    protect_client()