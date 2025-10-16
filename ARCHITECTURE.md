# PyArmor Licensing System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           SUBSCRIPTION SERVER                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────────────┐ │
│  │   User Input    │    │  Plan Database   │    │    PyArmor License Gen      │ │
│  │                 │    │                  │    │                             │ │
│  │ • Plan: Starter │───▶│ • Plans & Limits │───▶│ pyarmor licenses            │ │
│  │ • Agents: 2     │    │ • Agent Lists    │    │ --expired 2025-10-25        │ │
│  │ • Duration: 10d │    │ • Rate Limits    │    │ --data '{"plan":"starter"}' │ │
│  └─────────────────┘    └──────────────────┘    └─────────────────────────────┘ │
│                                                              │                   │
│                                                              ▼                   │
│                                                  ┌─────────────────────────────┐ │
│                                                  │     license.lic File        │ │
│                                                  │                             │ │
│                                                  │ • Encrypted & Signed        │ │
│                                                  │ • Machine Binding           │ │
│                                                  │ • Embedded Plan Data        │ │
│                                                  │ • Expiry Date               │ │
│                                                  └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
                                                              │
                                                              │ Download/Transfer
                                                              ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            PRODUCT APPLICATION                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                        PyArmor Runtime                                      │ │
│  │                                                                             │ │
│  │  verify_license('license.lic') ──┐                                         │ │
│  │                                   │                                         │ │
│  │  get_license_info() ──────────────┼──▶ {"plan": "starter",                 │ │
│  │                                   │     "agents": 2,                       │ │
│  │  ✅ Valid & Not Expired           │     "rate_limit": 2}                   │ │
│  │  ✅ Machine Binding OK            │                                         │ │
│  │  ❌ Raises Exception if Invalid    │                                         │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                           │
│                                      ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                        Business Logic Layer                                 │ │
│  │                                                                             │ │
│  │  Rate Limiter ◄──────────────────── License Data                           │ │
│  │  • 2 requests/min                                                          │ │
│  │                                                                             │ │
│  │  Agent Manager ◄─────────────────── License Data                           │ │
│  │  • Max 2 agents: [agent1, agent2]                                          │ │
│  │                                                                             │ │
│  │  Plan Enforcer ◄─────────────────── License Data                           │ │
│  │  • Starter plan features only                                              │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                           │
│                                      ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           User Interface                                    │ │
│  │                                                                             │ │
│  │  • License Upload/Validation                                               │ │
│  │  • Agent Selection (limited by license)                                    │ │
│  │  • Chat Interface (rate limited)                                           │ │
│  │  • Plan Status Display                                                     │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘

## Data Flow

1. **Subscription Flow:**
   User → Plan Selection → License Generation → Download .lic file

2. **Validation Flow:**
   Upload .lic → PyArmor Verify → Extract Plan Data → Apply Business Rules

3. **Runtime Flow:**
   User Action → Check Rate Limit → Check Agent Access → Execute (if allowed)

## Responsibility Matrix

| Component | PyArmor Handles | Business Logic Handles |
|-----------|----------------|------------------------|
| License Generation | ✅ File creation, signing | Plan data preparation |
| License Validation | ✅ Signature, expiry, binding | Plan rule extraction |
| Code Protection | ✅ Obfuscation, runtime checks | N/A |
| Rate Limiting | ❌ | ✅ Request counting, timing |
| Agent Management | ❌ | ✅ Access control, selection |
| Plan Features | ❌ | ✅ Feature availability |
```