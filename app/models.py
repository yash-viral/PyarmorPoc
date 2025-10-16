"""
app/models.py

Defines database models for the PyArmor Subscription System.

Entities:
- User: End users who own licenses.
- Plan: Defines plan-based limits and features.
- License: Holds issued license data and metadata.
- Agent: Represents sub-accounts or client identifiers under a license.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from app.db import Base


# ---------------------------------------------------------
# User Model
# ---------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    licenses = relationship("License", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"


# ---------------------------------------------------------
# Plan Model
# ---------------------------------------------------------
class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # starter / pro / enterprise
    description = Column(String)
    max_agents = Column(Integer, default=1)
    rate_limit_per_min = Column(Integer, default=2)
    duration_days = Column(Integer, default=30)
    is_active = Column(Boolean, default=True)

    licenses = relationship("License", back_populates="plan")

    def __repr__(self):
        return f"<Plan {self.name}>"


# ---------------------------------------------------------
# License Model
# ---------------------------------------------------------
class License(Base):
    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    license_key = Column(String, unique=True, nullable=False)
    license_data = Column(JSON, nullable=False)  # Encoded rules: {plan, agents, duration, rate_limit}
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    machine_id = Column(String, nullable=True)  # optional machine binding
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="licenses")
    plan = relationship("Plan", back_populates="licenses")
    agents = relationship("Agent", back_populates="license")

    def __repr__(self):
        return f"<License {self.license_key[:6]}...>"


# ---------------------------------------------------------
# Agent Model
# ---------------------------------------------------------
class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    license_id = Column(Integer, ForeignKey("licenses.id"), nullable=False)
    agent_name = Column(String, nullable=False)
    last_request_time = Column(DateTime, nullable=True)
    request_count = Column(Integer, default=0)

    license = relationship("License", back_populates="agents")

    def __repr__(self):
        return f"<Agent {self.agent_name}>"
