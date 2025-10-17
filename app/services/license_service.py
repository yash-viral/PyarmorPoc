"""
app/services/license_service.py

Service layer responsible for generating and validating licenses.
"""

import uuid
import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from sqlalchemy.orm import Session
from app import models, schemas
from app.utils.crypto import sign_license_data, encrypt_license_data
from app.config import DEFAULT_LICENSE_DURATION_DAYS


def create_pyarmor_license(db: Session, request: schemas.LicenseCreate) -> schemas.LicenseIssuedResponse:
    # Plan definitions
    PLANS = {
        1: {"name": "starter", "rate_limit_per_min": 2, "max_agents": 2},
        2: {"name": "growth", "rate_limit_per_min": 5, "max_agents": 3},
        3: {"name": "pro", "rate_limit_per_min": 15, "max_agents": 4},
        4: {"name": "enterprise", "rate_limit_per_min": 50, "max_agents": 4}
    }
    
    # Get plan info
    plan_info = PLANS.get(request.plan_id)
    if not plan_info:
        raise ValueError(f"Invalid plan_id: {request.plan_id}")
    
    # Validate agents
    if len(request.agents) > plan_info["max_agents"]:
        raise ValueError(f"Too many agents for {plan_info['name']} plan (max {plan_info['max_agents']})")
    
    # Create user if not exists
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user:
        user = models.User(id=request.user_id, email=f"user{request.user_id}@example.com", name=f"User {request.user_id}")
        db.add(user)
        db.commit()

    # Determine expiry
    duration = float(request.duration_days) if request.duration_days else DEFAULT_LICENSE_DURATION_DAYS
    print(f"DEBUG: Duration received: {duration}, type: {type(duration)}")
    
    # Handle testing duration (2 minutes = 0.0014 days)
    if duration == 0.0014:
        print("DEBUG: Using 2-minute expiry")
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=2)
    else:
        print(f"DEBUG: Using {duration} days expiry")
        expires_at = datetime.now(timezone.utc) + timedelta(days=duration)
    
    print(f"DEBUG: Current time: {datetime.now(timezone.utc)}")
    print(f"DEBUG: Expires at: {expires_at}")

    # License payload
    license_data = {
        "plan": plan_info["name"],
        "agents": request.agents,
        "duration_days": duration,
        "rate_limit_per_min": plan_info["rate_limit_per_min"],
        "expires_at": expires_at.isoformat(),
        "machine_id": request.machine_id,
    }
    print(f"DEBUG: License data expires_at: {license_data['expires_at']}")

    # Generate PyArmor license
    license_key = str(uuid.uuid4())
    
    # Create PyArmor license with embedded data
    if duration == 0.0014:  # 2 minutes testing
        expiry_date = expires_at.strftime("%Y-%m-%d %H:%M:%S")
    elif duration < 1:  # Less than 1 day
        expiry_date = expires_at.strftime("%Y-%m-%d %H:%M:%S")
    else:
        expiry_date = expires_at.strftime("%Y-%m-%d")
    print(f"DEBUG: PyArmor expiry_date: {expiry_date}")
    
    # Always encrypt license data with RSA
    encrypted_data = encrypt_license_data(license_data)
    print(f"DEBUG: Encrypted license data: {encrypted_data[:100]}...")
    
    try:
        # Generate PyArmor license file with encrypted data
        cmd = [
            "pyarmor", "licenses",
            "--expired", expiry_date,
            "--data", encrypted_data,
            license_key
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())
        
        if result.returncode != 0:
            print(f"DEBUG: PyArmor command failed: {result.stderr}")
            print(f"DEBUG: PyArmor stdout: {result.stdout}")
            # Fallback: create directory structure manually with encrypted data
            license_dir = Path(f"licenses/{license_key}")
            license_dir.mkdir(parents=True, exist_ok=True)
            
            license_file = license_dir / "license.lic"
            license_file.write_text(f"# PyArmor License\n# Key: {license_key}\n# EncryptedData: {encrypted_data}\n# Expires: {expiry_date}")
            print(f"DEBUG: Created fallback encrypted license file")
        else:
            print(f"DEBUG: PyArmor license created successfully")
            
    except Exception as e:
        print(f"DEBUG: Exception during license creation: {e}")
        # Fallback for development with encryption
        license_dir = Path(f"licenses/{license_key}")
        license_dir.mkdir(parents=True, exist_ok=True)
        license_file = license_dir / "license.lic"
        license_file.write_text(f"# PyArmor License\n# Key: {license_key}\n# EncryptedData: {encrypted_data}\n# Expires: {expiry_date}")
        print(f"DEBUG: Created exception fallback encrypted license file")
    
    # Create license record
    license_record = models.License(
        user_id=user.id,
        plan_id=request.plan_id,
        license_key=license_key,
        license_data=license_data,
        expires_at=expires_at,
        machine_id=request.machine_id,
        is_active=True
    )
    db.add(license_record)
    db.commit()
    db.refresh(license_record)

    # Create agent records
    for agent_name in request.agents:
        db.add(models.Agent(license_id=license_record.id, agent_name=agent_name))
    db.commit()

    # Create response with encrypted data for preview
    encrypted_preview = encrypt_license_data(license_data)
    
    return schemas.LicenseIssuedResponse(
        license_key=license_key,
        license_data={
            "encrypted_data": encrypted_preview,
            "plan": license_data["plan"],
            "agents": license_data["agents"],
            "expires_at": license_data["expires_at"]
        },
        expires_at=expires_at,
        plan_name=plan_info["name"],
        user_email=user.email
    )


def create_license(db: Session, request: schemas.LicenseCreate) -> schemas.LicenseIssuedResponse:
    """Backward compatibility wrapper"""
    return create_pyarmor_license(db, request)

def get_license_info(db: Session, license_key: str) -> dict:
    """
    Get license information including download details.
    """
    lic = db.query(models.License).filter(models.License.license_key == license_key).first()
    if not lic:
        return None
    
    print(f"DEBUG: License data from DB: {lic.license_data}")
    print(f"DEBUG: License data type: {type(lic.license_data)}")
    
    return {
        "license_key": license_key,
        "plan_name": lic.license_data.get("plan"),
        "agents": lic.license_data.get("agents", []),
        "expires_at": lic.expires_at.isoformat(),
        "is_active": lic.is_active and lic.expires_at.replace(tzinfo=timezone.utc) > datetime.now(timezone.utc)
    }

def verify_license(db: Session, license_key: str) -> bool:
    """
    Verify if a license exists, is active, and not expired.
    """
    lic = db.query(models.License).filter(models.License.license_key == license_key).first()
    if not lic:
        return False
    if not lic.is_active or lic.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        return False
    return True
