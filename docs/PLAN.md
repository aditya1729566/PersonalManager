# Project Plan (detailed)

This document breaks the high-level steps into explicit substeps, tests, and success criteria. Each Part is a milestone; the agent will mark checklist items as completed while working.

Part 1 — Plan & Approval
- Checklist:
	- [x] Review this plan with the user and confirm priorities.
	- [x] Break each Part into actionable tasks with tests and acceptance criteria.
	- [x] Create `frontend/AGENTS.md` describing frontend components and flows.
- Tests / Success:
	- Plan approved by the user.

Part 2 — Scaffolding (backend + Docker)
- Checklist:
	- [x] Scaffold `backend/` with a minimal FastAPI app and `backend/requirements.txt`.
	- [x] Add `scripts/start.sh` and `scripts/stop.sh` to run the app and container locally.
	- [x] Add a Dockerfile that builds the frontend static output and serves it from the backend container.
	- [x] Provide `.env.example` with required env vars (`DATABASE_URL`, `OPENROUTER_API_KEY`).
- Tests / Success:
	- `curl http://localhost:8000/api/hello` returns `{"message":"hello world"}` from inside container.
	- Container serves static `index.html` at `/`.

Part 3 — Frontend static export
- Checklist:
	- [x] Ensure Next config (`output: "export"`) produces a static `out/` with `next export`.
	- [x] Wire Docker build to run the Next build/export and copy `out/` into backend static dir.
	- [ ] Add unit tests for core components and a basic e2e test that loads `/`.
- Tests / Success:
	- `npm run build` and `npx next export` produce `out/` with `index.html`.
	- Playwright e2e verifies homepage loads and renders Kanban board.

Part 4 — Fake auth (user/password)
- Checklist:
	- [x] Add simple login route in `backend/auth.py` that sets a `session` cookie for `user`.
	- [x] Update frontend to require login to view Kanban (redirect to `/login` when not authenticated).
	- [x] Add logout endpoint and UI action.
- Tests / Success:
	- Unit tests for login/logout endpoints.
	- e2e verifies login flow and session persistence.

Part 5 — Database modeling
- Checklist:
	- [x] Define a simple schema: users table, kanban table storing JSON per user.
	- [x] Implement `backend/db.py` helpers: `init_db()`, `get_kanban(user)`, `save_kanban(user, data)`.
	- [ ] Document DB choice and paths in `docs/`.
- Tests / Success:
	- DB initializes if missing. Tests read/write JSON for a test user.

Part 6 — Backend API for Kanban
- Checklist:
	- [x] Add `/api/kanban` GET/PUT endpoints that use session to infer username.
	- [x] Add validation and basic error handling.
	- [x] Add unit tests for API behavior.
- Tests / Success:
	- Tests confirm GET returns an object and PUT persists changes.

Part 7 — Frontend + Backend integration
- Checklist:
	- [x] Replace frontend local mock with calls to `/api/kanban`.
	- [x] Update components to re-render after save.
	- [ ] Add integration tests covering create/edit/move card flows.
- Tests / Success:
	- e2e tests assert that changes persist across reloads.

Part 8 — AI connectivity
- Checklist:
	- [ ] Add `backend/ai.py` to call OpenRouter with robust error handling and mock fallback.
	- [ ] Add `/api/ai/test` endpoint for quick connectivity checks.
- Tests / Success:
	- Backend returns mock result when network/API unavailable; returns provider output when reachable and key present.

Part 9 — Structured AI integration
- Checklist:
	- [ ] Define structured output schema for responses (+ optional kanban update instructions).
	- [ ] Send full kanban JSON + user prompt to the model.
	- [ ] Apply model-suggested updates transactionally.
- Tests / Success:
	- Unit tests validate parsing structured responses and applying updates.

Notes & next steps
- Current state: core frontend exists; backend and Docker scaffold previously added. The AI sidebar will be disabled temporarily (removed from layout).
- Next action (code): finish Part 1 (this plan), create `frontend/AGENTS.md`, and proceed to Part 2 scaffolding tasks once you confirm.