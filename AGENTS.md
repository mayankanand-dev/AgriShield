# AGENTS.md — AgriShield (Smart VIT Hackathon 2026, PS SVH26007)

Single repo. All three of you branch off `main` and open PRs into it — nobody
pushes to `main` directly. This file is read by AI coding agents (Claude
Code, Cursor, Codex, etc.) before they touch this repo. Tell your agent which
role you are ("I'm the AI Developer") and it should be able to start from
just this file + `contracts/openapi.yaml`.

## Repo layout (one repo, folder-owned)

```
agrishield/
  ai/            # AI Developer owns this folder only
  backend/       # Integration Owner owns this folder only
  app/           # Integration Owner owns this folder only (Flutter)
  web/           # Website Developer owns this folder only
  contracts/     # openapi.yaml — shared, PR-and-review before editing
  design/        # Stitch exports (screenshots + Stitch prompt/spec files)
                 # dropped in here by App + Web devs — see "Design source" below
  AGENTS.md
  README.md
```

Stay inside your folder. If a change requires touching someone else's
folder (e.g. adding a field the backend needs to return), open the PR
against `contracts/openapi.yaml` first, tag it in the PR description, and
let that person pull it in — don't silently edit their code.

## What this project is

AgriShield: AI-powered crop insurance & farm-risk platform for PMFBY.
Farmers register land via GPS, get satellite/weather/soil-based monitoring,
AI crop-health + yield + risk scoring, dynamic insurance pricing, and
blockchain-audited policy/claim records.

## Non-negotiable architecture rule

`app/` and `web/` **only** call the Integration API in `backend/`. Neither
ever calls `ai/` directly, and neither ever connects to Postgres directly.
`backend/` is the single source of business truth. `ai/` is replaceable.

## Source of truth for API shape

`contracts/openapi.yaml` defines every endpoint, request/response shape, and
error code. Read it before generating any client, route, or mock. Never
invent an endpoint or field — if you need something not in the contract,
edit the contract in its own PR first.

Response envelope (always):
```json
{ "success": true, "data": {}, "meta": {"request_id": "uuid", "timestamp": "..."}, "error": null }
```
Error codes: the enum in `contracts/openapi.yaml#/components/schemas/ErrorCode`
(`AUTH_REQUIRED`, `VALIDATION_ERROR`, `FARM_BOUNDARY_INVALID`,
`AI_LOW_CONFIDENCE`, etc.) — reuse these, don't invent new ones.

## Design source (read before building any screen)

App and Website devs generate UI in Stitch first, then export it into
`design/app/` and `design/web/` (screenshots + the Stitch prompt used, see
`stitch_prompts.md`). **The agent's job is to implement pixel-faithful to
what's in `design/`, not to freelance a different layout.** If a screen
isn't in `design/` yet, build the simplest version that matches the existing
color/type system (deep green `#1B7A3D` primary, warm orange `#F5821F`
accent, off-white background) and flag it for a Stitch pass rather than
inventing a divergent style.

## Git / PR rules

- Branches: `feature/<role>-<name>` (e.g. `feature/app-claim-flow`),
  `fix/<name>` for bug fixes.
- Every PR description: what changed, contract changes (if any), how to run
  it, screenshot/video for anything UI, what tests were added.
- Never change an agreed `contracts/openapi.yaml` endpoint or field without
  that PR landing first and being pulled into your branch.
- Never commit `.env`, API keys, private keys, wallet seed phrases,
  service-account JSON, or real farmer documents/images.
- Definition of done: works locally, happy-path + one invalid-input test,
  response matches `contracts/openapi.yaml`, loading/empty/error/retry
  states exist in any UI, no secrets committed, README run instructions work
  from a clean checkout.

---

## ROLE: AI Developer

Own `ai/`. Independent FastAPI inference service, no auth/DB/insurance logic.

**Build these endpoints (exact shapes in `contracts/openapi.yaml`):**
1. `GET /health` — status + model versions.
2. `POST /v1/crop-health` — image, crop, growth_stage → label, severity, confidence, boxes.
3. `POST /v1/damage-assessment` — image(s), crop, event_type → damage_pct, severity, detections, confidence.
4. `POST /v1/yield-prediction` — crop, area_ha, sowing_date, optional history/weather → yield_value, unit, confidence.
5. `POST /v1/risk-score` — weather+crop+soil+history features → risk_score, risk_band, factors.
6. `POST /v1/soil-ocr` — PDF/image → N/P/K/pH + confidence + extracted text.
7. `POST /v1/advisory` — structured farm context → recommendations[], warnings[] (this also powers "recommend a crop type" for unsown farms — see backend §Soil OCR flow).

**Rules:**
- Always return `model_version` and `confidence` (0–1).
- Never return an insurance approval/denial — evidence and scores only.
- Below the configured confidence threshold, return a valid response with
  `low_confidence: true`, never an invented diagnosis.
- Ship `MOCK_MODE=true` returning realistic sample data for every endpoint
  first — this unblocks Backend before your real model is ready.
- Don't persist uploaded images unless the Integration API explicitly asks —
  storage is the backend's job.
- Stack: TensorFlow / YOLOv11 / OpenCV / EasyOCR / scikit-learn, Dockerfile, README with local run + curl examples for every endpoint.

**Deliverables checklist:** all 7 endpoints + health, MOCK_MODE, model
versioning, sample images + sample JSON responses, Dockerfile, README.

---

## ROLE: Website Developer

Own `web/`. React admin/insurer dashboard. Implements the pages exported to
`design/web/` from the Stitch website prompt (Dashboard, Farms map, Claims
dashboard, Claim review detail, Policy detail, Reports — see
`stitch_prompts.md` for the full page list and visual spec).

**Rules:**
- One typed API client module (`web/src/api/`). Components never call
  `fetch`/`axios` directly.
- All URLs from `VITE_API_BASE_URL`. Ship with `VITE_DEMO_MODE=true` pointing
  at local mock JSON (matching `contracts/openapi.yaml`) until Backend marks
  an endpoint READY.
- Every AI result on screen shows confidence % and model_version/timestamp.
- Every hackathon-only insurance decision gets a visible "Demo / AI-assisted"
  label.
- Loading, empty, error, and retry states on every data view — not just the
  happy path.
- Map rendering: any free map library/provider is fine; provider keys go
  through env vars.
- Never put service secrets in browser code.

**Deliverables checklist:** public landing page, login, farmer dashboard
consuming `GET /farms`, farm map, claims dashboard + review action wired to
`POST /claims/{id}/review`, policy detail with blockchain verification badge
wired to `GET /insurance/policies/{id}/verification`, notification center,
responsive desktop/tablet layout, README + `.env.example`.

---

## ROLE: Integration + App Owner

Own `backend/` and `app/`. You are the single source of business truth and
the final integrator.

**Backend (`backend/`) — FastAPI modules:**
```
app/main.py
api/  auth.py farms.py soil.py weather.py satellite.py ai.py insurance.py claims.py notifications.py admin.py
services/  ai_client.py weather_client.py satellite_client.py blockchain_service.py pricing_service.py notification_service.py storage_service.py
db/  models.py session.py migrations/
schemas/
core/  config.py security.py errors.py logging.py
tests/
```

**Backend responsibilities:** JWT/session validation + role-based auth,
Pydantic validation, PostGIS geometry validation + server-computed area
(never trust client-sent area), AI orchestration + persistence of model
outputs, insurance quote/policy/claim business rules, idempotency handling
(`Idempotency-Key` header on policy purchase + claim creation), audit
logging, SHA-256 hashing + blockchain adapter, notification dispatch,
external provider adapters (weather/satellite) with timeouts + graceful
fallback (`status=UNAVAILABLE`, cached+`stale=true`, never a hard crash).

**Polygon validation — do this properly, it was missing before:**
1. `POST /farms/{farm_id}/validate-boundary` must actually be called (by the
   app, or internally by `POST /farms`) before a farm is persisted — don't
   leave it as a dead endpoint.
2. Reject: unclosed ring, <3 unique vertices, self-intersecting polygon,
   area outside a sane min/max for a single field.
3. `ai_client.py` pattern: an interface with `MockAIClient` and
   `HttpAIClient` behind `AI_MODE=mock|live` — same interface, so nothing
   else in the backend changes when you swap.

**Flutter app (`app/`)** implements the screens exported to `design/app/`
from the Stitch app prompt (dashboard, add-farm map, farm detail tabs, crop
photo scan, soil report + fallback banner, insurance quote/purchase, file a
claim, claim status timeline, notifications — see `stitch_prompts.md`).

- Repository interface per domain (`FarmRepository`, `ClaimRepository`,
  `AIRepository`) with `LocalMockRepository` + `ApiRepository` — UI work
  never blocks on a live backend.
- Client-side polygon pre-check before submit (closed ring, ≥3 vertices, no
  self-intersection) — cheap geometry check, don't rely on the server round
  trip as the only validation, it breaks offline UX.
- Offline queue: local operation record with `local_id`, `operation`,
  `payload`, `idempotency_key`, `retry_count`, `status`; retried with the
  same `Idempotency-Key` header on reconnect.
- Never store access tokens in plain text local files.

**Deliverables checklist:** backend module tree above fully wired, Neon/
Supabase Postgres+PostGIS schema + migrations, auth + role checks, all
external adapters, Flutter app screens matching `design/app/`, offline
queue/sync, `ai_client.py` mock/live switch, blockchain adapter, deployment
config for all environments, final end-to-end test across all three folders.

---

## Security / secrets no agent should ever inline

`DATABASE_URL`, `JWT_SECRET`, `AI_SERVICE_TOKEN`, `WEATHER_API_KEY`,
`SATELLITE_API_KEY`, `STORAGE_BUCKET` credentials, `FIREBASE_*`,
`POLYGON_PRIVATE_KEY` (test wallet only). All from environment variables,
never hardcoded, never logged.

## When an agent is unsure

If a task needs an endpoint, field, or screen not defined in
`contracts/openapi.yaml` or `design/`, stop and ask rather than inventing
something the other two folders won't match.
