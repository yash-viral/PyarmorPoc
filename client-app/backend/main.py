from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from license_validator import LicenseValidator
from agents import AgentManager
import json
import time
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone

app = FastAPI(title="Client Chat App", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

license_validator = LicenseValidator()
agent_manager = AgentManager()
current_license = None
agent_timestamps = defaultdict(list)

class LicenseInput(BaseModel):
    license_data: dict

class ChatMessage(BaseModel):
    agent: str
    message: str

@app.post("/validate-license")
async def validate_license(license_input: LicenseInput):
    global current_license
    try:
        result = license_validator.validate_license_data(license_input.license_data)
        current_license = result
        return {"status": "success", "license": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/upload-license")
async def upload_license_file(file: UploadFile = File(...)):
    global current_license
    try:
        # Save uploaded license file
        license_path = Path("license.lic")
        with open(license_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate the license file
        result = license_validator.validate_license_file(str(license_path))
        current_license = result
        return {"status": "success", "license": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/validate-license-file")
async def validate_existing_license_file():
    global current_license
    try:
        result = license_validator.validate_license_file()
        current_license = result
        return {"status": "success", "license": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/license-status")
async def get_license_status():
    if not current_license:
        raise HTTPException(status_code=400, detail="No valid license")
    return current_license

@app.post("/chat")
async def chat_with_agent(chat: ChatMessage):
    if not current_license:
        raise HTTPException(status_code=400, detail="No valid license")
    
    # Check if license is expired
    from datetime import datetime, timezone
    try:
        expires_str = current_license["expires_at"]
        print(f"DEBUG: Checking expiry: {expires_str}")
        
        # Handle different datetime formats
        if expires_str.endswith('+00:00'):
            expires_at = datetime.fromisoformat(expires_str)
        elif 'T' in expires_str and not expires_str.endswith('Z'):
            expires_at = datetime.fromisoformat(expires_str + '+00:00')
        else:
            expires_at = datetime.fromisoformat(expires_str.replace('Z', '+00:00'))
        
        current_time = datetime.now(timezone.utc)
        print(f"DEBUG: Current time: {current_time}")
        print(f"DEBUG: Expires at: {expires_at}")
        
        if current_time > expires_at:
            print("DEBUG: License is EXPIRED")
            raise HTTPException(status_code=401, detail="License expired. Please renew your subscription.")
        else:
            print("DEBUG: License is still valid")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG: License expiry check failed: {e}")
        print(f"DEBUG: expires_at value: {current_license.get('expires_at')}")
    
    if chat.agent not in current_license["agents"]:
        raise HTTPException(status_code=403, detail=f"Agent '{chat.agent}' not available in your {current_license['plan']} plan")
    
    # Check rate limit
    limit = current_license["rate_limit"]
    now = time.time()
    
    # Remove timestamps older than 1 minute
    timestamps = [
        t for t in agent_timestamps[chat.agent] if now - t < 60
    ]
    agent_timestamps[chat.agent] = timestamps
    
    if len(timestamps) >= limit:
        raise HTTPException(
            status_code=429, 
            detail=f"Rate limit exceeded for {current_license['plan']} plan ({limit}/min). Please wait."
        )
    
    # Add current timestamp
    agent_timestamps[chat.agent].append(now)
    
    response = agent_manager.chat_with_agent(chat.agent, chat.message)
    return {
        "agent": chat.agent, 
        "response": response,
        "rate_limit_info": {
            "count": len(agent_timestamps[chat.agent]),
            "limit": limit
        }
    }

@app.get("/available-agents")
async def get_available_agents():
    if not current_license:
        return {"agents": []}
    return {"agents": agent_manager.get_available_agents(current_license["agents"])}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)