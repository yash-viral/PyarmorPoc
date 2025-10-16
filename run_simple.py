#!/usr/bin/env python3
"""
Simple server runner without uvicorn CLI
"""
import uvicorn
from app.main import app as subscription_app

def run_subscription_server():
    """Run subscription server directly"""
    print("🚀 Starting Subscription Server on port 8000...")
    uvicorn.run(subscription_app, host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    run_subscription_server()