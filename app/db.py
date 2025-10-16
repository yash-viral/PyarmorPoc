# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import os

# ============================================================
# 🧩 DATABASE INITIALIZATION
# ============================================================

# Ensure the directory exists for SQLite database
os.makedirs(os.path.dirname(settings.DATABASE_URL.replace("sqlite:///", "")), exist_ok=True)

# Create the SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


# ============================================================
# 🧩 Dependency for FastAPI
# ============================================================

def get_db():
    """Provide a database session for FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# 🧩 Initialize DB (called on app startup)
# ============================================================

def init_db():
    """Initialize all database tables."""
    from app import models  # Import models here to register them
    Base.metadata.create_all(bind=engine)
