# PyArmor Licensing System

Complete licensing system using PyArmor for secure license generation and validation.

## 🏗️ Architecture

```
Subscription Server → PyArmor License (.lic) → Product Application
       ↓                      ↓                        ↓
   Plan Selection      Embedded Plan Data        Business Logic
   User Management     Signature & Expiry        Rate Limiting
   License Generation  Machine Binding           Agent Control
```

## 🚀 Quick Start

### 1. Setup System
```bash
python setup_pyarmor_system.py
```

### 2. Start Subscription Server
```bash
python -m uvicorn app.main:app --reload --port 8000
cd frontend/react-app && npm run dev -- --port 3000
```

### 3. Start Product Application
```bash
cd client-app
python run_protected.py
cd frontend && npm run dev -- --port 3001
```

## 📋 Usage Flow

### Generate License (Subscription Server)
1. Open http://localhost:3000
2. Select plan: starter/pro/enterprise
3. Choose agents and duration
4. Click "Issue License"
5. Download `.lic` file

### Validate License (Product App)
1. Open http://localhost:3001
2. Upload `.lic` file OR paste JSON data
3. License validates with PyArmor
4. Business rules applied based on plan

## 🔧 Components

### Subscription Server (`app/`)
- **License Generation**: Creates PyArmor licenses with embedded plan data
- **Plan Management**: Defines rate limits, agent access, duration
- **User Management**: Tracks subscriptions and licenses

### Product Application (`client-app/`)
- **License Validation**: Uses PyArmor runtime for verification
- **Business Logic**: Enforces rate limits and agent restrictions
- **Protected Code**: Obfuscated with PyArmor

## 📊 Plan Comparison

| Feature | Starter | Pro | Enterprise |
|---------|---------|-----|------------|
| Rate Limit | 2/min | 10/min | 50/min |
| Agents | 2 | 5 | Unlimited |
| Duration | 30 days | 90 days | 365 days |

## 🛡️ Security Features

### PyArmor Handles:
- ✅ License file encryption & signing
- ✅ Expiration enforcement
- ✅ Machine binding
- ✅ Code obfuscation

### Business Logic Handles:
- ✅ Rate limiting
- ✅ Agent access control
- ✅ Plan feature restrictions
- ✅ Usage tracking

## 🔄 Development Mode

Without PyArmor installed, the system runs in fallback mode:
- JSON license validation
- Mock license generation
- Full business logic testing

## 📁 Project Structure

```
├── app/                    # Subscription Server
│   ├── controllers/        # API endpoints
│   ├── services/          # Business logic
│   ├── models/            # Database models
│   └── main.py            # FastAPI app
├── client-app/            # Product Application
│   ├── backend/           # Protected Python app
│   ├── frontend/          # React client
│   └── protect_client.py  # PyArmor protection
├── frontend/              # Subscription UI
│   └── react-app/         # React frontend
└── licenses/              # Generated license files
```

## 🧪 Testing

1. **Generate Test License**:
   ```bash
   cd client-app
   python generate_sample_license.py
   ```

2. **Test License Validation**:
   - Upload generated `license.lic`
   - Verify plan restrictions work
   - Test rate limiting

3. **Test Business Logic**:
   - Try exceeding rate limits
   - Access restricted agents
   - Check expiry handling

## 🔗 API Endpoints

### Subscription Server (Port 8000)
- `POST /api/licenses/` - Generate license
- `GET /api/licenses/{key}` - Get license info
- `GET /api/licenses/download/{key}` - Download .lic file

### Product Application (Port 8001)
- `POST /validate-license` - JSON license validation
- `POST /upload-license` - .lic file upload
- `POST /validate-license-file` - Check existing license
- `POST /chat` - Protected chat endpoint

## 📝 License Data Format

```json
{
  "plan": "starter",
  "agents": ["agent1", "agent2"],
  "rate_limit_per_min": 2,
  "expires_at": "2025-12-31T23:59:59"
}
```

This data is embedded in PyArmor license files and extracted by the product application for business rule enforcement.