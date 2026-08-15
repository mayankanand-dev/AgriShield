# AGENTS.md — AgriShield (Smart VIT Hackathon 2026, PS SVH26007)

This file is read by AI coding agents (Claude Code, Cursor, Codex, etc.) before
they touch this repo. Every one of the three parallel workstreams (AI, Web,
Integration/App) should keep a copy of this file at the root of their own repo
so all AI-assisted work stays consistent with the shared contract.

## What this project is

AgriShield: AI-powered crop insurance & farm-risk platform for PMFBY.
Farmers register land via GPS, get satellite/weather/soil-based monitoring,
AI crop-health + yield + risk scoring, dynamic insurance pricing, and
blockchain-audited policy/claim records.

## Non-negotiable architecture rule

The Flutter app and React website **only** call the Integration API
(`agrishield-backend`). Neither ever calls the AI service directly, and
neither ever connects to Postgres directly. The Integration API is the single
source of business truth. Do not generate code that bypasses this.

## Source of truth for API shape

`agrishield-contracts/openapi.yaml` is the single source of truth for every
endpoint, request/response shape, and error code. **Before generating any
client code, server route, or mock, read that file.** Never invent an
endpoint name or response field — if something you need isn't in the
contract, stop and flag it instead of guessing, since the other two repos are
building against the same file in parallel.

Response envelope (always):
```json
{ "success": true, "data": {}, "meta": {"request_id": "uuid", "timestamp": "..."}, "error": null }
```

Error codes are the enum in `openapi.yaml#/components/schemas/ErrorCode`
(`AUTH_REQUIRED`, `VALIDATION_ERROR`, `FARM_BOUNDARY_INVALID`,
`AI_LOW_CONFIDENCE`, etc.) — reuse these, don't invent new ones.

## Repos

| Repo | Owner | Contents |
|---|---|---|
| `agrishield-ai` | AI Developer | FastAPI inference service: crop-health, damage, yield, risk-score, soil-ocr, advisory |
| `agrishield-web` | Web Developer | React admin/insurer website |
| `agrishield-app` | Integration Owner | Flutter farmer app |
| `agrishield-backend` | Integration Owner | FastAPI Integration API + Postgres/PostGIS |
| `agrishield-contracts` | Shared | `openapi.yaml`, sample payloads, error codes — **source of truth, edit via PR only** |

## Mock-first rule (this is how three people build in parallel without blocking)

- **AI Developer**: every endpoint must work with `MOCK_MODE=true` returning
  realistic sample JSON, before the real model is wired in.
- **Website**: ship with `VITE_DEMO_MODE=true` pointing the API client at
  local mock JSON matching `openapi.yaml` response shapes.
- **App**: use a repository interface (`FarmRepository`, `ClaimRepository`,
  `AIRepository`) with a `LocalMockRepository` implementation, so UI work
  never waits on a live backend.
- Never hardcode a mock response inline in a component — put it in a single
  `mocks/` module so swapping to the real API is a one-line change.

## Conventions an agent must follow

- **IDs**: UUID v4 strings. **Time**: ISO-8601 UTC. **Coordinates**: WGS84
  lon/lat decimal degrees. **Area**: store m², display ha/acres in UI only.
- **Polygons**: validate client-side before submit — closed ring, ≥3 unique
  vertices, no self-intersection — via a lightweight geometry check, then
  call `POST /farms/{id}/validate-boundary` before `POST /farms`. Never rely
  on server-side PostGIS validation as the only check; that's a UX bug for
  offline users (see integration spec §7).
- **Idempotency-Key header is required** on policy purchase and claim
  creation — generate it client-side, reuse on retry.
- **Never fabricate an insurance decision.** AI endpoints return evidence and
  scores only; approval/denial is always a backend/human decision.
- **Never commit** `.env`, API keys, private keys, wallet seed phrases,
  service-account JSON, or real farmer documents/images.
- **Every PR** states: what changed, API changes (if any), how to run,
  screenshots/tests. Don't rename a response field without updating
  `agrishield-contracts` first.

## Commands (fill in per repo as they're set up)

```bash
# agrishield-backend
uvicorn app.main:app --reload --port 8000
pytest

# agrishield-ai
uvicorn app:app --reload --port 8001
pytest

# agrishield-web
npm run dev
npm run test

# agrishield-app
flutter run
flutter test
```

## Security / secrets an agent must never inline

`DATABASE_URL`, `JWT_SECRET`, `AI_SERVICE_TOKEN`, `WEATHER_API_KEY`,
`SATELLITE_API_KEY`, `STORAGE_BUCKET` credentials, `FIREBASE_*`,
`POLYGON_PRIVATE_KEY` (test wallet only). All read from environment
variables, never hardcoded, never logged.

## When an agent is unsure

If a task requires an endpoint, field, or behavior not defined in
`agrishield-contracts/openapi.yaml` or the integration spec, stop and ask
rather than inventing a contract the other two repos won't match.
