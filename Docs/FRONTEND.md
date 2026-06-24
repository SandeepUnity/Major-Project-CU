# Frontend

Next.js 16 application providing the EmpowerTech chat UI, session history, and analytics dashboard.

## Pages

| Route | File | Description |
|-------|------|-------------|
| `/` | `app/page.tsx` | Main chat interface |
| `/history` | `app/history/page.tsx` | Past messages for current session |
| `/analytics` | `app/analytics/page.tsx` | Sessions, messages, sentiment, handoff rate |

## Local development

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000. The API client defaults to `http://localhost:8000`.

Override with environment variable:

```bash
# frontend/.env.local (optional)
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## API client (`lib/api.ts`)

Typed wrapper around FastAPI endpoints:

- `api.health()` → `GET /health`
- `api.createSession(userId)` → `POST /session`
- `api.chat({ user_id, session_id?, query })` → `POST /chat`
- `api.history(sessionId)` → `GET /history`
- `api.analytics()` → `GET /analytics`

All requests use `cache: "no-store"` for fresh data.

## Chat page behaviour

- **Session persistence** — `session_id` stored in `localStorage` (`empowertech_session_id`)
- **Health polling** — `/health` checked every 5 seconds; status shown in UI
- **Auto-scroll** — Message list scrolls on new messages
- **Response details** — Intent, confidence, handoff flag, and metadata expandable per assistant message
- **Cold start banner** — `ColdStartBanner` warns about Render free-tier sleep (hidden if `NEXT_PUBLIC_HIDE_COLD_START_HINT=true`)

## Styling

- Tailwind CSS v4 (`app/globals.css`, PostCSS)
- Layout shell in `app/layout.tsx`
- Credits component: `components/ProjectCredits.tsx`

## Production build

```bash
cd frontend
NEXT_PUBLIC_API_BASE_URL=https://your-api.onrender.com npm run build
npm start
```

Or use Docker / Render (see [Deploy (Render)](DEPLOY_RENDER.md)). The build arg `NEXT_PUBLIC_API_BASE_URL` is set in `docker-compose.yml` and `render.yaml`.

## Lint

```bash
npm run lint
```
