"""
app/config.py

Global configuration settings for the FastAPI subscription system.

- Handles environment variables
- Defines file paths for RSA keys and database
- Provides centralized access to app-level constants
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------------------
# Load environment variables from .env (optional)
# ---------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------
# Base directories
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
KEYS_DIR = BASE_DIR / "keys"
DB_DIR = BASE_DIR / "data"
DB_DIR.mkdir(exist_ok=True)
KEYS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------
# Database configuration
# ---------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_DIR}/subscriptions.db")

# ---------------------------------------------------------
# RSA keys
# ---------------------------------------------------------
PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH", str(KEYS_DIR / "private_key.pem"))
PUBLIC_KEY_PATH = os.getenv("PUBLIC_KEY_PATH", str(KEYS_DIR / "public_key.pem"))

# ---------------------------------------------------------
# Application settings
# ---------------------------------------------------------
APP_NAME = os.getenv("APP_NAME", "PyArmor Subscription System")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() == "true"

# ---------------------------------------------------------
# License defaults
# ---------------------------------------------------------
DEFAULT_LICENSE_DURATION_DAYS = int(os.getenv("DEFAULT_LICENSE_DURATION_DAYS", 30))
DEFAULT_PLAN = os.getenv("DEFAULT_PLAN", "starter")
DEFAULT_RATE_LIMIT = int(os.getenv("DEFAULT_RATE_LIMIT", 2))  # requests/minute per agent

# ---------------------------------------------------------
# CORS settings
# ---------------------------------------------------------
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# ---------------------------------------------------------
# Print summary (optional)
# ---------------------------------------------------------
if DEBUG_MODE:
    print("Loaded Configuration:")
    print(f"  BASE_DIR:          {BASE_DIR}")
    print(f"  DATABASE_URL:      {DATABASE_URL}")
    print(f"  PRIVATE_KEY_PATH:  {PRIVATE_KEY_PATH}")
    print(f"  PUBLIC_KEY_PATH:   {PUBLIC_KEY_PATH}")
    print(f"  DEFAULT_PLAN:      {DEFAULT_PLAN}")
    print(f"  DEFAULT_DURATION:  {DEFAULT_LICENSE_DURATION_DAYS} days")
    print(f"  DEFAULT_RATE_LIMIT:{DEFAULT_RATE_LIMIT}/min per agent")


# ---------------------------------------------------------
# Export settings-like object for easy import
# ---------------------------------------------------------
class Settings:
    BASE_DIR = BASE_DIR
    DATABASE_URL = DATABASE_URL
    PRIVATE_KEY_PATH = PRIVATE_KEY_PATH
    PUBLIC_KEY_PATH = PUBLIC_KEY_PATH
    DEFAULT_PLAN = DEFAULT_PLAN
    DEFAULT_LICENSE_DURATION_DAYS = DEFAULT_LICENSE_DURATION_DAYS
    DEFAULT_RATE_LIMIT = DEFAULT_RATE_LIMIT

settings = Settings()
