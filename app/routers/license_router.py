"""
app/controllers/license_controller.py

FastAPI endpoints for managing licenses.
Connects the service layer (business logic) to HTTP routes.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import License
from app.schemas import LicenseCreate, LicenseIssuedResponse
from app.services import license_service
from app.utils.crypto import encrypt_license_data
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import uuid

# router is included in app.main with prefix '/api/licenses'
# keep the router itself un-prefixed so endpoints become '/api/licenses/'
router = APIRouter(tags=["Licenses"])


@router.post("/", response_model=LicenseIssuedResponse)
def issue_license(request: LicenseCreate, db: Session = Depends(get_db)):
    try:
        # Generate PyArmor license with embedded plan data
        license_issued = license_service.create_pyarmor_license(db, request)
        return license_issued
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@router.get("/download/{license_key}")
def download_license(license_key: str, db: Session = Depends(get_db)):
    try:
        # Check multiple possible locations
        license_paths = [
            Path(f"licenses/{license_key}/license.lic"),
            Path(f"licenses/{license_key}.lic"),
            Path(f"{license_key}.lic")
        ]
        
        license_file = None
        for path in license_paths:
            if path.exists():
                license_file = path
                break
        
        if not license_file:
            # Create a fallback license file
            license_dir = Path(f"licenses/{license_key}")
            license_dir.mkdir(parents=True, exist_ok=True)
            license_file = license_dir / "license.lic"
            
            # Get license data from database
            lic = db.query(License).filter(License.license_key == license_key).first()
            if lic:
                # Encrypt the license data
                encrypted_data = encrypt_license_data(lic.license_data)
                license_content = f"# PyArmor License\n# Key: {license_key}\n# EncryptedData: {encrypted_data}\n# Expires: {lic.expires_at}"
            else:
                license_content = f"# PyArmor License\n# Key: {license_key}\n# Fallback license file"
            
            license_file.write_text(license_content)
            
        return FileResponse(
            path=str(license_file),
            filename=f"{license_key}.lic",
            media_type="application/octet-stream"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@router.get("/{license_key}")
def verify_license(license_key: str, db: Session = Depends(get_db)):
    license_data = license_service.get_license_info(db, license_key)
    if not license_data:
        raise HTTPException(status_code=404, detail="License not found")
    
    # Get full license data from database for encryption
    lic = db.query(License).filter(License.license_key == license_key).first()
    if lic:
        # Encrypt the license data for preview
        encrypted_preview = encrypt_license_data(lic.license_data)
        preview_data = {
            "encrypted_data": encrypted_preview,
            "plan": license_data["plan_name"],
            "agents": license_data["agents"],
            "expires_at": license_data["expires_at"],
            "is_active": license_data["is_active"]
        }
    else:
        preview_data = license_data
    
    return {
        "message": "License found", 
        "license_key": license_key,
        "download_url": f"/api/licenses/download/{license_key}",
        "license_data": {
            "plan_name": license_data["plan_name"],
            "agents": license_data["agents"],
            "expires_at": license_data["expires_at"],
            "is_active": license_data["is_active"]
        }
    }
