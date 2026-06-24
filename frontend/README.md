# EmpowerTech Chatbot — Frontend

Next.js web UI for the EmpowerTech RAG chatbot. See the main project docs in [`../Docs/`](../Docs/README.md).

## Quick start

```bash
npm install
npm run dev
```

Open http://localhost:3000. Requires the FastAPI backend at `http://localhost:8000` (see [Setup Guide](../Docs/SETUP.md)).

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_BASE_URL` | `http://localhost:8000` | Backend API URL (no trailing slash) |
| `NEXT_PUBLIC_HIDE_COLD_START_HINT` | unset | Set `true` to hide Render cold-start banner |

Create `frontend/.env.local` for local overrides.

## Pages

- `/` — Chat
- `/history` — Session message history
- `/analytics` — Usage and sentiment dashboard

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Development server |
| `npm run build` | Production build |
| `npm start` | Serve production build |
| `npm run lint` | ESLint |

Full frontend documentation: [Docs/FRONTEND.md](../Docs/FRONTEND.md).
