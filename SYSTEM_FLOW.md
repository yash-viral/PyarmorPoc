# PyArmor Licensing System - Complete Flow

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        SUBSCRIPTION SERVER                                      │
│                     (Port 8000 + 3000)                                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Frontend (React - Port 3000)          Backend (FastAPI - Port 8000)          │
│  ┌─────────────────────────────────┐    ┌─────────────────────────────────────┐ │
│  │  Plan Selection UI              │    │  License Generation Service        │ │
│  │  • Starter (2 agents, 2/min)    │───▶│  • PyArmor license creation        │ │
│  │  • Growth (3 agents, 5/min)     │    │  • Embedded plan data              │ │
│  │  • Pro (4 agents, 15/min)       │    │  • Database storage                │ │
│  │  • Enterprise (4 agents, 50/min)│    │  • File download endpoint          │ │
│  └─────────────────────────────────┘    └─────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ license.lic file
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         PRODUCT APPLICATION                                     │
│                      (Port 8001 + 3001)                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Frontend (React - Port 3001)          Backend (FastAPI - Port 8001)          │
│  ┌─────────────────────────────────┐    ┌─────────────────────────────────────┐ │
│  │  License Upload UI              │    │  PyArmor Runtime Validation        │ │
│  │  • File upload (.lic)           │───▶│  • License verification            │ │
│  │  • Plan status display          │    │  • Plan data extraction            │ │
│  │  • Agent selection (restricted) │    │  • Rate limiting enforcement       │ │
│  │  • Chat interface               │    │  • Agent access control            │ │
│  └─────────────────────────────────┘    └─────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📋 Complete User Flow

### Step 1: Subscription (Port 3000)
1. User opens http://localhost:3000
2. Selects plan: **Starter** (2 agents, 2 req/min)
3. Chooses agents: **agent1, agent2**
4. Sets duration: **10 days**
5. Clicks "Generate License"
6. Downloads `license.lic` file

### Step 2: License Generation (Backend)
```bash
pyarmor licenses --expired 2025-01-15 --data '{"plan":"starter","agents":["agent1","agent2"],"rate_limit_per_min":2}' user_license
```

### Step 3: Product Usage (Port 3001)
1. User opens http://localhost:3001
2. Uploads `license.lic` file
3. System validates with PyArmor runtime
4. Plan restrictions applied:
   - Only agent1, agent2 available
   - Rate limit: 2 requests/minute
   - Expires in 10 days

### Step 4: Business Logic Enforcement
- **Agent Access**: Only licensed agents clickable
- **Rate Limiting**: Request counter per minute
- **Plan Display**: Shows current plan status
- **Expiry**: PyArmor handles automatically

## 🔧 Plan Specifications

| Plan | Rate Limit | Max Agents | Available Agents | Color |
|------|------------|------------|------------------|-------|
| Starter | 2/min | 2 | agent1, agent2 | Green |
| Growth | 5/min | 3 | agent1, agent2, agent3 | Blue |
| Pro | 15/min | 4 | All 4 agents | Orange |
| Enterprise | 50/min | 4 | All 4 agents | Purple |

## 🛡️ Security & Validation

### PyArmor Handles:
- ✅ License file encryption/signing
- ✅ Expiration enforcement
- ✅ Machine binding (optional)
- ✅ Tamper protection

### Business Logic Handles:
- ✅ Rate limiting per agent
- ✅ Agent access control
- ✅ Plan feature restrictions
- ✅ UI state management

## 🚀 Quick Start Commands

```bash
# 1. Setup
python setup_pyarmor_system.py

# 2. Start Subscription Server
python -m uvicorn app.main:app --reload --port 8000
cd frontend/react-app && npm run dev -- --port 3000

# 3. Start Product Application  
cd client-app
python run_protected.py
cd frontend && npm run dev -- --port 3001

# 4. Test Flow
# - Go to localhost:3000 → Generate license
# - Go to localhost:3001 → Upload license → Chat
```

## 📊 Sample License Data

```json
{
  "plan": "starter",
  "agents": ["agent1", "agent2"],
  "rate_limit_per_min": 2,
  "duration_days": 10,
  "expires_at": "2025-01-15T23:59:59"
}
```

This data is embedded in the PyArmor license file and extracted by the product application for enforcement.