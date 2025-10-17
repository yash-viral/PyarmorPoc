#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path
import os

def run_protected_client():
    dist_dir = Path("dist") / "backend" / "backend"

    # Auto-protect if not already protected
    if not dist_dir.exists() or not (dist_dir / "main.py").exists():
        print("🔒 Protecting client first...")
        result = subprocess.run([sys.executable, "protect_client.py"])
        if result.returncode != 0:
            print("❌ Protection failed")
            return False

    print("🚀 Starting PyArmor-protected client backend...")

    # Locate the pyarmor runtime folder
    runtime_dirs = list(dist_dir.parent.glob("pyarmor_runtime_*"))
    if not runtime_dirs:
        raise FileNotFoundError(f"❌ Could not find pyarmor_runtime folder inside {dist_dir.parent}/")
    runtime_dir = runtime_dirs[0]
    
    # Copy runtime to backend directory if not exists
    target_runtime = dist_dir / runtime_dir.name
    if not target_runtime.exists():
        import shutil
        shutil.copytree(runtime_dir, target_runtime)
        print(f"📁 Copied {runtime_dir.name} to backend directory")

    # Prepare PYTHONPATH so Python can find pyarmor runtime
    pythonpath = os.pathsep.join([str(dist_dir), str(dist_dir.parent), str(runtime_dir), *sys.path])

    env = os.environ.copy()
    env["PYTHONPATH"] = pythonpath

    # Check if main.py exists
    main_py = dist_dir / "main.py"
    if not main_py.exists():
        print(f"❌ Protected main.py not found at {main_py}")
        print("🔄 Re-running protection...")
        result = subprocess.run([sys.executable, "protect_client.py"])
        if result.returncode != 0 or not main_py.exists():
            print("❌ Protection failed or main.py still missing")
            return False
    
    # Run the protected main.py directly
    try:
        subprocess.run([sys.executable, "main.py"], cwd=dist_dir, env=env, check=True)
    except KeyboardInterrupt:
        print("\n👋 Client backend stopped.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running backend: {e}")

    return True

if __name__ == "__main__":
    run_protected_client()
