# AgriShield — Agent Handoff & Model Switch Guide
> **Smart VIT Hackathon 2026 | PS SVH26007**
> Read this FIRST when resuming work with a new AI agent or after token expiry.

---

## What This Project Is

AgriShield is a 3-part project built by 3 developers simultaneously:

| Folder | Developer | Stack | Port |
|--------|-----------|-------|------|
| `ai/` | AI Developer | FastAPI + scikit-learn + OpenCV | 8001 |
| `backend/` | Integration Owner | FastAPI + PostgreSQL (Supabase) + Polygon blockchain | 8000 |
| `web/` | Website Developer | React + Vite + TypeScript + Leaflet | 5173 |
| `app/` | Integration Owner | Flutter | mobile |

**Golden rule:** `web/` and `app/` ONLY call `backend/`. `backend/` calls `ai/`. Neither web nor app ever calls `ai/` directly.

---

## Tell the Agent Your Role First

Paste ONE of these context starters at the top of your message:

### If you are the AI Developer
```
I'm the AI Developer on AgriShield (web/ai/ folder).
Read ANALYSIS.md and AGENTS.md for full context.
The core problem: trained models (yield_model.pkl, risk_model.pkl) exist in ai/models/
but the routes in ai/app/routes/ still return hardcoded stub values.
The inference/ wrappers and app/services/ exist but are not wired to the routes.
My next task is: [describe task].
```

### If you are the Integration / Backend Developer
```
I'm the Integration Owner on AgriShield (backend/ folder).
Read ANALYSIS.md and AGENTS.md for full context.
The core problem: backend/api/ai.py is empty, HttpAIClient methods all return None (pass body),
and backend/api/claims.py hardcodes fake AI results (damage_pct=0.45).
Farm-level AI endpoints in openapi.yaml have no backend implementation.
My next task is: [describe task].
```

### If you are the Website Developer
```
I'm the Website Developer on AgriShield (web/ folder).
Read ANALYSIS.md and AGENTS.md for full context.
The core problem: web map uses hardcoded US lat/lng instead of farm centroids,
PolicyStatus enum mismatches DB, /auth/me response shape is wrong, and
web/src/pages/Claims.tsx:19 sets status to 'APPROVE'/'REJECT' instead of 'APPROVED'/'REJECTED'.
My next task is: [describe task].
```

---

## Current State Snapshot (as of 2026-08-15)

### What Works
- [x] `ai/` — All 7 endpoints respond (hardcoded stubs, but no crashes)
- [x] `ai/` — `yield_model.pkl` and `risk_model.pkl` trained and saved
- [x] `backend/` — Farm CRUD (create/list/get) with real DB + polygon validation
- [x] `backend/` — Insurance quote + policy CRUD with blockchain hash
- [x] `backend/` — Claims list/create/review with real DB
- [x] `web/` — All pages render in demo mode (VITE_DEMO_MODE=true)
- [x] `web/` — Claims approve/reject flow wired to backend

### What Is Broken / Missing
- [ ] AI models not wired to routes (routes return stubs, not model predictions)
- [ ] Backend has zero calls to AI service (`backend/api/ai.py` is empty)
- [ ] Claims `assess` endpoint hardcodes fake values — no real AI call
- [ ] HttpAIClient.get_crop_health() and get_damage_assessment() both return None
- [ ] HttpAIClient missing 3 methods: yield, risk, advisory
- [ ] Backend `soil.py`, `satellite.py`, `notifications.py` are empty stubs
- [ ] `/auth/me` returns wrong shape (user_id vs id, roles[] vs role)
- [ ] Web map shows US lat/lng, not real Indian farm coordinates
- [ ] PolicyStatus ACTIVE|EXPIRED|CANCELLED in DB vs ACTIVE|EXPIRED|PENDING in web type
- [ ] Secrets committed in backend/core/config.py (POLYGON_PRIVATE_KEY, DATABASE_URL)
- [ ] No real JWT auth — any token is accepted
- [ ] File Claim submit button does nothing in app (`app/lib/ui/screens/file_claim_screen.dart`)

---

## Critical Files to Read Before Touching Anything

```
contracts/openapi.yaml          ← THE LAW. Read before any endpoint change.
AGENTS.md                       ← Architecture rules and role boundaries.
ANALYSIS.md                     ← Detailed sync audit (the file you're reading from).
backend/schemas/contract.py     ← Pydantic models that all 3 systems share.
backend/services/ai_client.py   ← The bridge between backend and AI service.
ai/app/config.py                ← Model paths and MOCK_MODE for AI service.
web/src/api/index.ts            ← Only API touchpoint for web — must match contract.
```

---

## Priority Fix Order (Ranked)

| Priority | Problem | Owner | Files |
|----------|---------|-------|-------|
| 1 | Wire trained models to AI routes | AI Dev | `ai/app/routes/yield_prediction.py`, `risk_score.py` |
| 2 | Implement HttpAIClient methods | Integration | `backend/services/ai_client.py` |
| 3 | Add farm-level AI routes in backend | Integration | `backend/api/farms.py` or new `ai.py` |
| 4 | Fix hardcoded claim assessment | Integration | `backend/api/claims.py:136` |
| 5 | Fix /auth/me response shape | Integration | `backend/api/auth.py:84` |
| 6 | Fix web map coordinates | Web Dev | `web/src/pages/Dashboard.tsx:92` |
| 7 | Fix ClaimStatus bug in web | Web Dev | `web/src/pages/Claims.tsx:19` |
| 8 | Fix PolicyStatus enum mismatch | All 3 | `backend/db/models.py`, `web/src/api/index.ts`, `openapi.yaml` |
| 9 | Implement backend soil route | Integration | `backend/api/soil.py` |
| 10 | Remove hardcoded secrets | Integration | `backend/core/config.py` |

---

## How to Run Each Service Locally

### AI Service
```bash
cd ai
pip install -r requirements.txt
MOCK_MODE=false uvicorn app.main:app --port 8001 --reload
# Test: curl http://localhost:8001/health
```

### Backend
```bash
cd backend
pip install -r requirements.txt
# Set DATABASE_URL in .env (do NOT hardcode)
uvicorn app.main:app --port 8000 --reload
# Test: curl http://localhost:8000/health
```

### Web
```bash
cd web
npm install
# Set VITE_API_BASE_URL=http://localhost:8000/api/v1 in .env
npm run dev
# Opens at http://localhost:5173
```

---

## Model Switch Checklist

When switching AI agents mid-session, verify the new agent understands:

- [ ] The 3-folder ownership rule (never touch another dev's folder without a PR)
- [ ] `openapi.yaml` is the contract — no inventing endpoints
- [ ] Response envelope: `{success, data, meta, error}` always (except AI microservice internals)
- [ ] Secrets: never hardcode, never commit — all from env vars
- [ ] AI service is internal-only — backend proxies all AI calls
- [ ] `MOCK_MODE=true` must keep working at all times (demo day backup)
- [ ] Every AI result shown to users needs `confidence %` and `model_version` displayed

---

## Quick Contract Reference

### Response Envelope (backend → web)
```json
{
  "success": true,
  "data": {},
  "meta": { "request_id": "uuid", "timestamp": "ISO8601" },
  "error": null
}
```

### AI Service Response (internal, no envelope)
```json
{
  "model_version": "v1.0",
  "confidence": 0.87,
  "low_confidence": false,
  "inference_ms": 120,
  ... domain fields ...
}
```

### Endpoint Map (backend base = /api/v1)
```
POST   /auth/register
POST   /auth/login
GET    /auth/me
GET    /farms
POST   /farms
GET    /farms/{id}
POST   /farms/{id}/validate-boundary
POST   /farms/{id}/soil/analyze        ← STUB — not implemented
POST   /farms/{id}/crop-health         ← STUB — not implemented
POST   /farms/{id}/yield-predict       ← STUB — not implemented
POST   /farms/{id}/risk-score          ← STUB — not implemented
POST   /farms/{id}/advisory            ← STUB — not implemented
GET    /farms/{id}/weather/current     ← WRONG PATH — needs fix
GET    /farms/{id}/satellite/latest    ← STUB
POST   /insurance/quote
GET    /insurance/policies
POST   /insurance/policies
GET    /insurance/policies/{id}
GET    /insurance/policies/{id}/verification
GET    /claims
POST   /claims
GET    /claims/{id}
POST   /claims/{id}/assess             ← FAKE — hardcoded values
POST   /claims/{id}/review             ← WORKING
GET    /claims/{id}/verification       ← WORKING
GET    /notifications                  ← STUB
POST   /devices/register               ← STUB
```

---

## AI Service Endpoint Map (base = http://localhost:8001)
```
GET    /health                         ← WORKING
POST   /v1/crop-health                 ← STUB (model exists for crop_health?)
POST   /v1/damage-assessment           ← STUB
POST   /v1/yield-prediction            ← STUB (yield_model.pkl exists, NOT wired)
POST   /v1/risk-score                  ← STUB (risk_model.pkl exists, NOT wired)
POST   /v1/soil-ocr                    ← STUB
POST   /v1/advisory                    ← STUB
```
