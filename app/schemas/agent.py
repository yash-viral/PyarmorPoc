from datetime import datetime
from pydantic import BaseModel, Field


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