from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


# ============================================================
# 🧩 USER SCHEMAS
# ============================================================

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2


# ============================================================
# 🧩 AGENT SCHEMAS
# ============================================================

class AgentBase(BaseModel):
    name: str = Field(..., description="Agent identifier (unique per user)")


class AgentCreate(AgentBase):
    pass


class AgentResponse(AgentBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# 🧩 LICENSE SCHEMAS
# ============================================================

class LicenseBase(BaseModel):
    plan: str = Field(..., description="Subscription plan name, e.g., starter or pro")
    agents: List[str] = Field(default_factory=list, description="List of agent names assigned to license")
    duration_days: float = Field(default=30, description="License validity in days")
    max_requests_per_min: int = Field(default=2, description="Rate limit per agent per minute")


class LicenseCreate(LicenseBase):
    user_id: int
    # optional numeric plan id (service looks up plans by id)
    plan_id: Optional[int] = None
    # optional machine binding
    machine_id: Optional[str] = None
    duration_days: float = Field(default=30, description="License validity in days (supports fractional for testing)")


class LicenseResponse(LicenseBase):
    id: int
    license_key: str
    expiry_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# 🧩 LICENSE ISSUE RESPONSE
# ============================================================

class LicenseIssuedResponse(BaseModel):
    license_key: str
    license_data: dict
    expires_at: datetime
    plan_name: str
    user_email: str

    class Config:
        from_attributes = True


# ============================================================
# 🧩 AUTH / TOKEN SCHEMAS (optional if you add login later)
# ============================================================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
