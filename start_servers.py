#!/usr/bin/env python3
"""
Start both subscription server and client application
"""
import subprocess
import sys
import time
from pathlib import Path

def start_subscription_server():
    """Start the subscription server"""
    print("🚀 Starting Subscription Server...")
    subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "app.main:app", 
        "--reload", 
        "--port", "8000"
    ])

def start_client_app():
    """Start the client application"""
    print("🚀 Starting Client Application...")
    client_path = Path("client-app")
    subprocess.Popen([
        sys.executable, "run_protected.py"
    ], cwd=client_path)

def main():
    print("🔧 PyArmor Licensing System")
    print("=" * 40)
    
    try:
        start_subscription_server()
        time.sleep(2)
        start_client_app()
        
        print("\n✅ Servers started!")
        print("📊 Subscription Server: http://localhost:8000 (API) + http://localhost:3000 (UI)")
        print("🤖 Client Application: http://localhost:8001 (API) + http://localhost:3001 (UI)")
        print("\n🔄 Flow:")
        print("1. Go to localhost:3000 → Generate license")
        print("2. Go to localhost:3001 → Upload license → Chat")
        print("\nPress Ctrl+C to stop all servers")
        
        # Keep script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        sys.exit(0)

if __name__ == "__main__":
    main()