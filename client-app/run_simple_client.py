#!/usr/bin/env python3
"""
Simple client runner without uvicorn CLI
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import uvicorn
from backend.main import app as client_app

def run_client_server():
    """Run client server directly"""
    print("🚀 Starting Client Server on port 8001...")
    uvicorn.run(client_app, host="127.0.0.1", port=8001, reload=False)

if __name__ == "__main__":
    run_client_server()