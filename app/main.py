"""
app/main.py

Main entry point for the FastAPI application.
This file initializes the FastAPI app, includes routers,
and sets up middleware, CORS, and startup events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import license_controller
from app.db import init_db
import subprocess
from pathlib import Path

# ---------------------------------------------------------
# Initialize FastAPI app
# ---------------------------------------------------------
app = FastAPI(
    title="PyArmor Subscription Server",
    description="Generates PyArmor licenses with embedded plan data.",
    version="1.0.0"
)

# ---------------------------------------------------------
# Middleware (CORS, etc.)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------
app.include_router(license_controller.router, prefix="/api/licenses", tags=["Licenses"])

# ---------------------------------------------------------
# Startup / Shutdown Events
# ---------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    """
    Called when FastAPI starts up.
    Use this for one-time initialization (DB, keys, etc.)
    """
    init_db()
    
    # Ensure licenses directory exists
    licenses_dir = Path("licenses")
    licenses_dir.mkdir(exist_ok=True)
    
    # Check PyArmor availability
    try:
        result = subprocess.run(["pyarmor", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ PyArmor available for license generation")
        else:
            print("⚠️ PyArmor not available - using fallback mode")
    except FileNotFoundError:
        print("⚠️ PyArmor not installed - using fallback mode")
    
    print("✅ Database initialized successfully.")

@app.get("/", tags=["Health"])
async def root():
    """
    Health check endpoint.
    """
    return {"status": "ok", "message": "PyArmor Subscription Server is running."}

# ---------------------------------------------------------
# Run for local dev
# ---------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
