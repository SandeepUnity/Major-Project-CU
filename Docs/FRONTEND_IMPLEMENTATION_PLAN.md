# Frontend Implementation Plan: EmpowerTech RAG Chatbot

This plan adds a **modern web frontend** for the existing FastAPI backend so reviewers can interact with the chatbot, view session history, and (optionally) view analytics outputs for report screenshots.

## Goals

- Provide a **clean chat UI** that works with the current backend endpoints:
  - `POST /session`
  - `POST /chat`
  - `GET /history?session_id=...`
  - `GET /analytics`
  - `GET /health`
- Enable **report evidence**: screenshots of chat, guardrails/handoff behavior, and analytics.
- Be demo-friendly: **dockerized**, easy to run locally, optionally deployable as a live demo.

## Non-goals (initial)

- Full user authentication/roles (can be added later)
- Payment/enrollment transactions (chat can guide; no payments handled in UI)
- Complex admin portal (keep analytics view minimal)

---

## Recommended Tech Stack

- **Framework**: Next.js (React) + TypeScript
- **UI**: Tailwind CSS + shadcn/ui (or Material UI if preferred)
- **State**: React state + lightweight store (Zustand) only if needed
- **API**: `fetch` to FastAPI base URL (configurable via env)
- **Testing**: Playwright (E2E) + Vitest/React Testing Library (unit, optional)

Why Next.js: fast dev, easy deployment, SSR optional, good for demos and clean routing.

---

## UX / Screens

### 1) Chat Screen (Primary)

**Core components**
- Header: project title + backend status indicator (`GET /health`)
- Conversation panel: message bubbles (user/assistant), timestamps
- Input box with send button, enter-to-send
- Session controls:
  - Create new session
  - Copy session id
  - Load session by id (for report/demo repeatability)

**Data shown per message (for research/report)**
- Show small “Details” drawer per assistant message:
  - retrieval confidence
  - intent
  - handoff flag
  - source ids list (from `metadata.retrieval.source_ids`)

**Guardrail + handoff UX**
- If assistant returns the fallback advisor message, show a “Escalate” callout.
- If `handoff_trigger=true`, show “Talk to advisor” callout (static in demo; link/contact in later phase).

### 2) History Screen (Secondary)

- Input: session id
- Render full history from `GET /history?session_id=...`
- Provide export buttons:
  - Copy JSON (for appendix)
  - Save transcript text (for appendix)

### 3) Analytics Screen (Optional but helpful for Chapter 7 evidence)

- Show output of `GET /analytics`
- Minimal charts:
  - total sessions/messages (cards)
  - handoff rate (progress bar)
  - avg session sentiment (card)

---

## Frontend ↔ Backend Contract

### Configuration
- `NEXT_PUBLIC_API_BASE_URL` (e.g., `http://localhost:8000`)

### Requests
- Create session:
  - `POST /session` body: `{ "user_id": "..." }`
  - response: `{ "session_id": "..." }`
- Chat:
  - `POST /chat` body: `{ "user_id": "...", "session_id": "...", "query": "..." }`
  - response includes `response`, `metadata`, `handoff_trigger`, `confidence`, `intent`
- History:
  - `GET /history?session_id=...`
- Analytics:
  - `GET /analytics`

### Error handling
- Show toast/banner for 4xx/5xx
- If backend unreachable, show offline indicator and disable send button

---

## Implementation Steps

### Phase F1 — Project setup (0.5–1 day)
- Create `frontend/` Next.js app (TypeScript)
- Add Tailwind + UI component library
- Add `.env.local.example` with `NEXT_PUBLIC_API_BASE_URL`
- Add basic layout + routing (`/`, `/history`, `/analytics`)

### Phase F2 — Chat UI + session persistence (1–2 days)
- Implement `ChatPage`:
  - create session on first load or on “New session”
  - store `session_id` in `localStorage`
  - optimistic UI (append user message immediately)
  - show loading indicator while awaiting response
- Render assistant details drawer from response metadata
- Implement `/health` status indicator

### Phase F3 — History + Analytics pages (0.5–1.5 days)
- History page wired to `GET /history`
- Analytics page wired to `GET /analytics`

### Phase F4 — Testing + hardening (0.5–1.5 days)
- Add Playwright smoke tests:
  - load home page
  - create session
  - send a message and receive a response (requires backend running)
- Add unit tests for API client + basic components (optional)
- Add rate-limit UX (disable send for rapid-fire inputs)

---

## Docker + Demo Setup (Frontend)

### Local (recommended)
- Run backend stack: `docker compose up -d`
- Run frontend dev server separately:
  - `npm install`
  - `npm run dev`

### Full dockerized demo (optional)
- Add a frontend Dockerfile and update compose to include:
  - `frontend` service exposing port 3000
  - env var `NEXT_PUBLIC_API_BASE_URL=http://app:8000` (or proxy through Next.js)

---

## Live Demo Deployment (Frontend)

Choose one:
- **Vercel**: easiest for Next.js frontend; point API base URL to hosted backend
- **Render/Railway/Fly.io**: host both services; configure env vars

Deployment checklist:
- `NEXT_PUBLIC_API_BASE_URL` points to your backend
- CORS is configured in backend if frontend is on a different domain
- Health endpoint accessible

---

## Report Evidence Mapping (Ch 5–7)

- **Chapter 5 (Implementation screenshots)**:
  - Chat UI (normal response)
  - Guardrail fallback response
  - “Details” panel showing retrieval sources + intent
- **Chapter 6 (Testing)**:
  - Playwright run output (or GitHub Actions)
- **Chapter 7 (Results/Discussion)**:
  - Use frontend to run a repeatable test script (same prompts), capture outputs and source ids
  - Export chat transcripts via History page for appendices

