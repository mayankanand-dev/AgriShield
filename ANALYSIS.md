# AgriShield — Full Codebase Analysis
> **Smart VIT Hackathon 2026 | PS SVH26007**
> Generated: 2026-08-15

---

## PART 1 — Files Analyzed

### Root / Contracts
| File | Size | Notes |
|------|------|-------|
| `AGENTS.md` | 10 KB | Role assignments, architecture rules, deliverable checklists |
| `openapi.yaml` | 14 KB | 441-line API contract — single source of truth |
| `stitch_prompts.md` | 5 KB | UI design export prompts for Stitch |

---

### `ai/` — AI Inference Service (FastAPI microservice, port 8001)
| File | Purpose |
|------|---------|
| `ai/app/main.py` | FastAPI entrypoint, mounts 7 routers |
| `ai/app/config.py` | Env-driven config; MOCK_MODE, model paths, confidence threshold |
| `ai/app/routes/health.py` | GET /health — service uptime |
| `ai/app/routes/crop_health.py` | POST /v1/crop-health — returns hardcoded stub |
| `ai/app/routes/yield_prediction.py` | POST /v1/yield-prediction — returns hardcoded stub |
| `ai/app/routes/risk_score.py` | POST /v1/risk-score — returns hardcoded stub |
| `ai/app/routes/damage_assessment.py` | POST /v1/damage-assessment — stub |
| `ai/app/routes/soil_ocr.py` | POST /v1/soil-ocr — stub |
| `ai/app/routes/advisory.py` | POST /v1/advisory — stub |
| `ai/app/services/yield_service.py` | YieldService class, predict() is `pass` (not wired) |
| `ai/app/services/risk_service.py` | RiskService class, stub |
| `ai/app/services/crop_health_service.py` | CropHealthService, stub |
| `ai/app/services/damage_service.py` | DamageService, stub |
| `ai/app/services/soil_ocr_service.py` | SoilOcrService, stub |
| `ai/app/services/advisory_service.py` | AdvisoryService, stub |
| `ai/inference/yield_prediction.py` | Inference wrapper, stub |
| `ai/inference/risk_scoring.py` | Inference wrapper, stub |
| `ai/inference/crop_health.py` | Inference wrapper, stub |
| `ai/inference/damage_assessment.py` | Inference wrapper, stub |
| `ai/inference/soil_ocr.py` | Inference wrapper, stub |
| `ai/inference/advisory.py` | Inference wrapper, stub |
| `ai/models/yield/yield_model.pkl` | **TRAINED** — saved during this session |
| `ai/models/risk/risk_model.pkl` | **TRAINED** — saved during this session |
| `ai/models/crop_health/` | Directory exists, model not confirmed trained |
| `ai/models/damage/` | Directory exists, model not confirmed trained |
| `ai/training/generate_dataset.py` | 29 KB synthetic dataset generator |
| `ai/training/yield/train.py` | Trains yield_model.pkl |
| `ai/training/risk/train.py` | Trains risk_model.pkl |
| `ai/Dockerfile` | Container definition |
| `ai/requirements.txt` | Python dependencies |

---

### `backend/` — Integration API (FastAPI, port 8000)
| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI root; mounts /api/v1 sub-app, CORS, generic error handler |
| `backend/core/config.py` | Pydantic settings; DATABASE_URL, JWT, AI_MODE, blockchain config |
| `backend/core/security.py` | JWT helpers |
| `backend/db/models.py` | SQLAlchemy ORM: User, Farm, Claim, InsurancePolicy, enums |
| `backend/db/session.py` | AsyncSession + Base |
| `backend/schemas/contract.py` | Pydantic: Envelope, GeoPolygon, Farm, Claim, AIPredictionBase |
| `backend/schemas/insurance.py` | QuoteRequest, PolicyCreate |
| `backend/api/auth.py` | /auth/* routes — register, login (dummy token), refresh, me |
| `backend/api/farms.py` | /farms — list, create (validates boundary), get, validate-boundary |
| `backend/api/claims.py` | /claims — list, create, get, assess (hardcoded AI), review, verify |
| `backend/api/insurance.py` | /insurance/quote, /policies CRUD, verification |
| `backend/api/weather.py` | GET /weather?lat&lon — proxies weather_client |
| `backend/api/ai.py` | **EMPTY router — zero routes** |
| `backend/api/admin.py` | **Empty stub** |
| `backend/api/soil.py` | **Empty stub** |
| `backend/api/satellite.py` | **Empty stub** |
| `backend/api/notifications.py` | **Empty stub** |
| `backend/services/ai_client.py` | MockAIClient + HttpAIClient; HttpAIClient methods = `pass` |
| `backend/services/blockchain_service.py` | SHA-256 hash + Polygon chain record |
| `backend/services/polygon_validator.py` | Shapely-based polygon checks |
| `backend/services/pricing_service.py` | calculate_premium() |
| `backend/services/weather_client.py` | HTTP call to external weather API |
| `backend/services/storage_service.py` | File upload helper |
| `backend/.env` | **Contains real secrets (DATABASE_URL, POLYGON_PRIVATE_KEY)** |

---

### `web/` — React Admin Dashboard (Vite + TypeScript, port 5173)
| File | Purpose |
|------|---------|
| `web/src/App.tsx` | Router: Landing, Login, Register + Layout-wrapped dashboard routes |
| `web/src/api/index.ts` | Single typed API module; IS_DEMO toggle; mock data fallback |
| `web/src/pages/Dashboard.tsx` | Stats (policies, claims, farmers) + Leaflet map |
| `web/src/pages/Claims.tsx` | Claims table; approve/reject wired to api.reviewClaim() |
| `web/src/pages/Policies.tsx` | Policies list; blockchain verification badge |
| `web/src/pages/FarmsMap.tsx` | Farm boundary map |
| `web/src/pages/Farmers.tsx` | Farmer list |
| `web/src/pages/Verification.tsx` | Blockchain status view |
| `web/src/pages/Reports.tsx` | Reports placeholder |
| `web/src/pages/Landing.tsx` | Public landing page |
| `web/src/pages/Login.tsx` | Login form |
| `web/src/pages/Register.tsx` | Registration form |
| `web/src/pages/Profile.tsx` | User profile |
| `web/.env` | VITE_API_BASE_URL, VITE_DEMO_MODE |
| `web/package.json` | Vite + React + Leaflet + Lucide + Axios |

---

## PART 2 — Logical Inferences

### Architecture Flow (Intended)
```
Web/App  →  backend /api/v1  →  ai/ microservice
                  ↓
               PostgreSQL (Supabase)
                  ↓
               Polygon blockchain
```

### Current Operational State

| Component | Status |
|-----------|--------|
| AI routes (7 endpoints) | Exist, return **hardcoded stubs** |
| AI trained models (yield + risk) | **Saved on disk** but NOT wired to routes |
| AI inference wrappers | Exist but **never imported** in routes |
| AI service layer (services/) | All predict() are `pass` |
| Backend auth | Dummy JWT — accepts any token, no validation |
| Backend farms CRUD | **Functional** with real DB + polygon validation |
| Backend claims assessment | **Hardcoded** (damage_pct=0.45, no AI call) |
| Backend insurance CRUD | **Functional** with real DB + blockchain hash |
| Backend → AI integration | **Zero calls** — backend/api/ai.py is empty |
| Backend soil/satellite/notifications | All **empty stubs** |
| HttpAIClient | All methods return `None` (pass body) |
| Web in DEMO mode | **Working** — mock data renders correctly |
| Web in live mode | **Partial** — farms/claims/policies load; AI fields fail |
| Web map coordinates | **Hardcoded US lat/lng** — wrong for India farms |

### Key Logical Inferences

1. **AI developer trained models but didn't wire them.** `yield_model.pkl` and `risk_model.pkl` exist but `/v1/yield-prediction` still serves `{"yield_value": 5000}`. The `inference/` layer and `services/` layer exist but are imported nowhere.

2. **Backend never calls AI service.** `backend/api/ai.py` is empty. The farm-level AI endpoints in `openapi.yaml` (`/farms/{id}/crop-health`, `/farms/{id}/yield-predict`, etc.) have no backend implementation.

3. **Web dashboard renders farms at fake US coordinates.** `Dashboard.tsx` L92-101 uses `38.0 + index*2, -97.0 + index*2`. Real Indian farms won't appear on the map.

4. **Auth is a universal bypass.** `get_current_user()` fetches the first DB row with no token check. Any string passes as "authentication."

5. **Claims assessment is entirely fabricated.** `POST /claims/{id}/assess` sets `damage_pct=0.45` unconditionally with no AI call.

6. **Soil OCR is a dead path.** The AI endpoint exists; the backend stub is empty; there's no route connecting them.

7. **Weather route path doesn't match contract.** Backend: `GET /api/v1/weather?lat&lon`. Contract: `GET /farms/{farm_id}/weather/current`.

8. **Private wallet key and DB password committed in source.** `config.py` hardcodes both, violating AGENTS.md.

9. **`PolicyStatus` enum mismatch.** DB: `ACTIVE|EXPIRED|CANCELLED`. Web type: `ACTIVE|EXPIRED|PENDING`.

10. **`/auth/me` response shape mismatch.** Backend returns `{user_id, name, roles[]}`. Web expects `{id, email, name, role}`.

---

## PART 3 — Implementation Problems

### CRITICAL — End-to-End Flow Is Broken

#### P1: Trained Models Not Connected to Routes
- **Files**: `ai/app/routes/yield_prediction.py:16`, `ai/app/routes/risk_score.py:16`, `ai/app/routes/crop_health.py:14`
- `yield_model.pkl` and `risk_model.pkl` are trained and saved but routes return static stubs.
- The `ai/inference/` wrappers and `ai/app/services/` exist but are imported nowhere in routes.
- **Fix**: Each route must load model via inference wrapper → call service.predict() → return real result.

#### P2: Backend Has Zero AI Calls (HttpAIClient All `pass`)
- **Files**: `backend/api/ai.py` (empty), `backend/services/ai_client.py:45-50`
- `/farms/{id}/crop-health`, `/farms/{id}/yield-predict`, `/farms/{id}/risk-score`, `/farms/{id}/advisory` — all defined in contract, none exist in backend.
- HttpAIClient methods have `pass` bodies — calling them in live mode returns `None`.
- **Fix**: Implement all 5 methods in HttpAIClient; add farm-scoped routes that call `get_ai_client()`.

#### P3: Claim Assessment Hardcodes Fake AI Results
- **File**: `backend/api/claims.py:136-137`
- `claim.damage_pct = 0.45` and `claim.ai_confidence = 0.92` are literals — no AI service call.
- **Fix**: `assess_claim()` must call `ai_client.get_damage_assessment()` with evidence images.

#### P4: HttpAIClient Has Only 2 of 5 Required Methods
- **File**: `backend/services/ai_client.py`
- Only `get_crop_health()` and `get_damage_assessment()` declared (both `pass`).
- Missing: `get_yield_prediction()`, `get_risk_score()`, `get_soil_ocr()`, `get_advisory()`.
- **Fix**: Add all missing abstract + mock + HTTP methods.

---

### HIGH — Data Shape Mismatches Break Real Integration

#### P5: Farm Response Missing `sowing_date`, `boundary`, `centroid`
- **File**: `backend/api/farms.py:30-38` and `99-129`
- Backend returns `{id, user_id, name, crop, area_m2, status}` only.
- Contract and web type require `sowing_date`, `boundary` (GeoPolygon), `centroid {lat, lon}`.
- **Fix**: Serialize full Farm including PostGIS geometry as WGS84 GeoPolygon + computed centroid.

#### P6: Web Map Uses Fake US Coordinates
- **File**: `web/src/pages/Dashboard.tsx:92-101`
- `lat = 38.0 + (index * 2)` — hardcoded US geography.
- **Fix**: Backend must return `centroid`; web must use `farm.centroid.lat / farm.centroid.lon`.

#### P7: `PolicyStatus` Enum Mismatch
- DB: `ACTIVE | EXPIRED | CANCELLED` (models.py:17-19)
- Web type: `ACTIVE | EXPIRED | PENDING` (api/index.ts:70)
- Contract: not defined
- **Fix**: Agree on canonical set, update contract, sync DB enum + web type.

#### P8: `/auth/me` Response Shape Mismatch
- **File**: `backend/api/auth.py:84`
- Backend: `{"user_id": ..., "name": ..., "roles": [...]}`
- Web expects: `{id, email, name, role}` (singular `id`, `email` present, `role` is string)
- **Fix**: Return `id`, add `email`, change `roles` array to `role` string.

#### P9: Status Bug in Web Claim Review
- **File**: `web/src/pages/Claims.tsx:19`
- `{...c, status: action}` sets status to `"APPROVE"` or `"REJECT"` (verbs).
- Correct values are `"APPROVED"` or `"REJECTED"` (past tense enums).
- **Fix**: `status: action === 'APPROVE' ? 'APPROVED' : 'REJECTED'`

---

### MEDIUM — Missing Routes / Stubs Never Implemented

#### P10: Soil OCR Has No Backend Route
- `backend/api/soil.py` is a 52-byte empty stub.
- Contract: `POST /farms/{farm_id}/soil/analyze`
- AI service: `POST /v1/soil-ocr` exists
- **Fix**: Implement soil route; accept multipart PDF/image; call AI client; return OCR result.

#### P11: Satellite Endpoints Entirely Missing
- `backend/api/satellite.py` is empty.
- Contract: `GET /farms/{farm_id}/satellite/latest` and `/history`
- **Fix**: Implement or return graceful `UNAVAILABLE` fallback per AGENTS.md rules.

#### P12: Notifications Are Dead
- `backend/api/notifications.py` is empty.
- Contract: `GET /notifications`, `POST /notifications/{id}/read`, `POST /devices/register`
- Web: `api.getNotifications()` only works in demo mode.
- **Fix**: Add notifications table + CRUD.

#### P13: Weather Route Path Mismatch
- Backend: `GET /api/v1/weather?lat&lon`
- Contract: `GET /farms/{farm_id}/weather/current` and `/forecast`
- Web does not call weather endpoints at all.
- **Fix**: Restructure router to be farm-scoped, lookup centroid by farm_id, call weather_client.

#### P14: `/farms/{farm_id}/validate-boundary` Never Called by Flutter
- Backend correctly auto-validates in `POST /farms` (internal call).
- AGENTS.md: Flutter app must also do client-side pre-check offline.
- No confirmation this exists in app/.
- **Fix**: Flutter `app/` must implement client-side polygon validation before submit.

---

### SECURITY

#### P15: Secrets Hardcoded in Source Code
- **File**: `backend/core/config.py:8,20,21`
- Violations (AGENTS.md explicitly forbids all):
  - Full `DATABASE_URL` with real Supabase password
  - `POLYGON_PRIVATE_KEY` = real wallet key (40b5ad...)
  - Alchemy API key in `POLYGON_RPC_URL`
  - `SECRET_KEY = "supersecretkey"`
- **Fix**: Remove all defaults, require env vars, verify `.env` is gitignored.

#### P16: No Real JWT Authentication
- **File**: `backend/api/auth.py:13-20`
- `get_current_user()` fetches first DB row — accepts any request as authenticated.
- Login returns static `"dummy_token"` with no signature.
- **Fix**: Implement real JWT sign/verify using `core/security.py`; validate token in `get_current_user`.

---

### STRUCTURAL

#### P17: AI Service Does Not Return Contract Envelope
- All AI routes return plain dicts `{}` not `{success, data, meta, error}`.
- This is acceptable for an internal microservice, but must be documented.
- **Fix**: Document in README that AI service uses flat JSON; `HttpAIClient` handles unwrapping.

#### P18: Route Mount Collision Risk
- `backend/app/main.py:48` defines root-level `GET /health`.
- `api_router` is mounted at `/api/v1`.
- If a reverse proxy routes `/health` to backend it works; but the backend `GET /health` is NOT inside `/api/v1` — this means `openapi.yaml` `GET /health` path is ambiguous.
- **Fix**: Clarify in deployment docs which service owns `/health`.

#### P19: Web API Cache Never Invalidated for Farms/Policies
- **File**: `web/src/api/index.ts:112-116`
- `_cache.farms` and `_cache.policies` are module-level and never cleared after mutations.
- Creating a new farm/policy won't reflect without page refresh.
- **Fix**: Nullify relevant cache entries after successful POST mutations.

#### P20: `ai_client.py` MockAIClient Only Mocks 2 Endpoints
- **File**: `backend/services/ai_client.py`
- Mock only covers `get_crop_health()` and `get_damage_assessment()`.
- When backend tries to call yield/risk/advisory/soil in mock mode: `AttributeError`.
- **Fix**: Add mock implementations for all 5 required methods.

---

## PART 4 — App & Blockchain Analysis

### App Issues
#### P21: Plain Text Token Storage
- **File**: `app/lib/api/api_client.dart`
- Tokens are stored using `SharedPreferences`, violating the rule to never store access tokens in plain text.
- **Fix**: Replaced with `FlutterSecureStorage`.

#### P22: Missing Client-Side Geometry Validation
- **File**: `app/lib/ui/screens/add_farm_screen.dart`
- Lacks proper geometry validation (e.g., closed ring, self-intersection) before saving boundaries.
- **Fix**: Added basic self-intersection logic.

#### P23: Offline Queue Not Integrated
- **File**: `app/lib/repositories/offline_queue.dart` & `app/lib/repositories/farm_repository.dart`
- OfflineQueue exists but isn't integrated in the repositories.
- **Fix**: Updated `FarmRepository` to enqueue requests on `NETWORK_ERROR`.

#### P24: File Claim Endpoint Missing
- **File**: `app/lib/ui/screens/file_claim_screen.dart`
- Submit button does nothing (`onPressed: () {}`).
- **Fix**: Wired to `/claims` endpoint via `ClaimRepository.createClaim`.

### Blockchain Issues
#### P25: Hardcoded Secrets in Config
- **File**: `blockchain/.env`
- Contains real `POLYGON_PRIVATE_KEY` and Alchemy URL. 
- **Fix**: `blockchain/.env` cleared of secrets.
