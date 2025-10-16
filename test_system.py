#!/usr/bin/env python3
"""
Test the complete system: server, client, and agents
"""

import subprocess
import time
import sys
from pathlib import Path

def test_unprotected_client():
    """Test the unprotected modular client"""
    print("🧪 Testing unprotected modular client...")
    
    # Change to client directory and run
    client_dir = Path("client")
    result = subprocess.run([sys.executable, "main.py"], 
                          cwd=client_dir, 
                          capture_output=True, 
                          text=True)
    
    if result.returncode == 0:
        print("✅ Unprotected client test passed!")
        print(result.stdout)
    else:
        print("❌ Unprotected client test failed:")
        print(result.stderr)
    
    return result.returncode == 0

def protect_and_test():
    """Protect client with PyArmor and test"""
    print("\n🔒 Protecting client with PyArmor...")
    
    # Run PyArmor protection
    result = subprocess.run([sys.executable, "pyarmor_config.py"], 
                          capture_output=True, 
                          text=True)
    
    if result.returncode != 0:
        print("❌ PyArmor protection failed:")
        print(result.stderr)
        return False
    
    print("✅ Client protected successfully!")
    
    # Test protected client
    print("\n🧪 Testing protected client...")
    result = subprocess.run([sys.executable, "run_protected_client.py"], 
                          capture_output=True, 
                          text=True)
    
    if result.returncode == 0:
        print("✅ Protected client test passed!")
        print(result.stdout)
    else:
        print("❌ Protected client test failed:")
        print(result.stderr)
    
    return result.returncode == 0

if __name__ == "__main__":
    print("🚀 Starting system tests...\n")
    
    # Test 1: Unprotected client
    success1 = test_unprotected_client()
    
    # Test 2: Protected client
    success2 = protect_and_test()
    
    print(f"\n📊 Test Results:")
    print(f"Unprotected client: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Protected client: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 All tests passed! System is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the output above.")