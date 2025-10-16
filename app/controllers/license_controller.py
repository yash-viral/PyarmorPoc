"""
app/controllers/license_controller.py

FastAPI endpoints for managing licenses.
Connects the service layer (business logic) to HTTP routes.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app import schemas, models
from app.services import license_service
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import uuid

# router is included in app.main with prefix '/api/licenses'
# keep the router itself un-prefixed so endpoints become '/api/licenses/'
router = APIRouter(tags=["Licenses"])


@router.post("/", response_model=schemas.LicenseIssuedResponse)
def issue_license(request: schemas.LicenseCreate, db: Session = Depends(get_db)):
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
            lic = db.query(models.License).filter(models.License.license_key == license_key).first()
            if lic:
                license_content = f"# PyArmor License\n# Key: {license_key}\n# Data: {json.dumps(lic.license_data)}\n# Expires: {lic.expires_at}"
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
    
    return {
        "message": "License found", 
        "license_key": license_key,
        "download_url": f"/api/licenses/download/{license_key}",
        "license_data": license_data
    }
