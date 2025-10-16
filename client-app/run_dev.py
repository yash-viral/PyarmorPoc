#!/usr/bin/env python3
"""
Run the client backend in development mode (unprotected)
"""
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path("backend")
sys.path.insert(0, str(backend_dir.absolute()))

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)