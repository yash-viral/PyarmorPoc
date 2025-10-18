from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class LicenseBase(BaseModel):
    plan: str = Field(..., description="Subscription plan name, e.g., starter or pro")
    agents: List[str] = Field(default_factory=list, description="List of agent names assigned to license")
    duration_days: float = Field(default=30, description="License validity in days")
    max_requests_per_min: int = Field(default=2, description="Rate limit per agent per minute")


class LicenseCreate(LicenseBase):
    user_id: int
    plan_id: Optional[int] = None
    machine_id: Optional[str] = None
    duration_days: float = Field(default=30, description="License validity in days (supports fractional for testing)")


class LicenseResponse(LicenseBase):
    id: int
    license_key: str
    expiry_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class LicenseIssuedResponse(BaseModel):
    license_key: str
    license_data: dict
    expires_at: datetime
    plan_name: str
    user_email: str

    class Config:
        from_attributes = True