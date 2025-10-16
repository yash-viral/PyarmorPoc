#!/usr/bin/env python3
"""
Complete PyArmor Licensing System Setup
Demonstrates the full flow from subscription to license validation
"""
import subprocess
import sys
from pathlib import Path
import json
from datetime import datetime, timedelta

def check_pyarmor():
    """Check if PyArmor is installed"""
    try:
        result = subprocess.run(["pyarmor", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ PyArmor is installed")
            return True
        else:
            print("❌ PyArmor not working properly")
            return False
    except FileNotFoundError:
        print("❌ PyArmor not found")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    # Backend dependencies
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # Frontend dependencies
    frontend_path = Path("frontend/react-app")
    if frontend_path.exists():
        subprocess.run(["npm", "install"], cwd=frontend_path, check=True)
    
    client_frontend_path = Path("client-app/frontend")
    if client_frontend_path.exists():
        subprocess.run(["npm", "install"], cwd=client_frontend_path, check=True)

def setup_directories():
    """Create necessary directories"""
    print("📁 Setting up directories...")
    
    directories = [
        "licenses",
        "client-app/backend/licenses",
        "app/licenses"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  Created: {dir_path}")

def create_sample_data():
    """Create sample plans and users in database"""
    print("🗄️ Setting up sample data...")
    
    # This would typically be done through the API or database migrations
    sample_plans = [
        {"id": 1, "name": "starter", "rate_limit_per_min": 2, "duration_days": 30},
        {"id": 2, "name": "pro", "rate_limit_per_min": 10, "duration_days": 90},
        {"id": 3, "name": "enterprise", "rate_limit_per_min": 50, "duration_days": 365}
    ]
    
    sample_users = [
        {"id": 1, "email": "user@example.com", "name": "Test User"}
    ]
    
    print("  Sample plans and users ready for database initialization")

def demonstrate_flow():
    """Demonstrate the complete licensing flow"""
    print("\n🚀 PyArmor Licensing System Flow")
    print("=" * 50)
    
    print("\n1. SUBSCRIPTION SERVER")
    print("   - User selects plan (starter, pro, enterprise)")
    print("   - Server generates PyArmor license with embedded data")
    print("   - License file (.lic) is created with plan restrictions")
    
    print("\n2. LICENSE GENERATION")
    print("   Command: pyarmor licenses --expired 2025-12-31 --data '{\"plan\":\"starter\"}' user_license")
    print("   Output: licenses/user_license/license.lic")
    
    print("\n3. PRODUCT APPLICATION")
    print("   - User uploads license.lic file")
    print("   - PyArmor validates signature, expiry, machine binding")
    print("   - App extracts plan data and enforces business rules")
    
    print("\n4. BUSINESS LOGIC ENFORCEMENT")
    print("   - Rate limiting based on plan")
    print("   - Agent access control")
    print("   - Feature restrictions")

def main():
    print("🔧 PyArmor Licensing System Setup")
    print("=" * 40)
    
    # Check PyArmor
    if not check_pyarmor():
        print("\n⚠️  PyArmor not found. Install with:")
        print("   pip install pyarmor")
        print("\n   The system will work in fallback mode for development.")
    
    # Setup
    try:
        setup_directories()
        install_dependencies()
        create_sample_data()
        
        print("\n✅ Setup completed successfully!")
        
        # Demonstrate flow
        demonstrate_flow()
        
        print("\n🎯 Next Steps:")
        print("1. Start subscription server: python -m uvicorn app.main:app --reload")
        print("2. Start client app: cd client-app && python run_protected.py")
        print("3. Open frontend: http://localhost:3000 (subscription) + http://localhost:3001 (client)")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)