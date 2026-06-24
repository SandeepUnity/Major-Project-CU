# Deploy on Render (Postgres + API + Next.js)

> Part of the [project documentation](README.md). Local setup: [Setup Guide](SETUP.md).

Use the repository root **`render.yaml`** as a **Blueprint** so Render creates three resources: free PostgreSQL, Docker **API**, and Docker **frontend**.

## Prerequisites

- GitHub repo connected to Render  
- **OpenAI** and **Pinecone** keys (billing may apply beyond free tiers on those vendors)  
- Pinecone index dimension **1536** for `text-embedding-3-small` (`PINECONE_INDEX_NAME`, e.g. `empowertech-rag-1536`)

## 1. Create the Blueprint

1. [Render Dashboard](https://dashboard.render.com/) → **New +** → **Blueprint**.  
2. Connect your repo and select the branch.  
3. Render detects **`render.yaml`**.  
4. When prompted, set **secret** env vars (marked `sync: false` in the file):
   - `OPENAI_API_KEY`
   - `PINECONE_API_KEY`  
5. Apply the Blueprint.

Predictable URLs (unless Render renames due to clashes):

| Service           | Intended public URL                                      |
|-------------------|----------------------------------------------------------|
| API               | `https://empowertech-api.onrender.com`                 |
| Frontend          | `https://empowertech-web.onrender.com`                   |

If URLs differ (suffix added), open each service → copy **Public URL**, then Update:

- **API** → `CORS_ORIGINS` = your **frontend** public URL (`https://...`)  
- **Frontend** → `NEXT_PUBLIC_API_BASE_URL` = your **API** public URL (`https://...`)  

Redeploy the **frontend** after changing `NEXT_PUBLIC_API_BASE_URL` (it is baked in at **build** time).

## 2. First-run database and vectors

After the API is **live**:

- **Tables:** On **free** web services Render does **not** support `preDeployCommand`. This app runs SQLAlchemy **`create_all()` once at API startup** (`lifespan` in `main.py`) so tables exist without a pre-deploy step.  
- **Ingest FAQs (run once)** — Render Shell for `empowertech-api`:
  ```bash
  python -m src.ingestion.ingest --source data/knowledge_base_faqs.csv --type csv
  ```
- Optional seed:  
  ```bash
  python -m src.models.seed_db
  ```

## 3. Free-tier behaviour

- **Web services spin down** when idle; first request after sleep can take **30–60+ seconds**.  
- The Next.js UI shows a **dismissible amber banner** automatically when `NEXT_PUBLIC_API_BASE_URL` contains `onrender.com` (set `NEXT_PUBLIC_HIDE_COLD_START_HINT=true` on the frontend to hide it).  
- **Free PostgreSQL** may have expiry / size limits ([Render docs](https://render.com/docs/free)).

## 4. Configuration reference

| Variable | Where | Purpose |
|---------|-------|---------|
| `DATABASE_URL` | API (from database) | Injected by Blueprint |
| `CORS_ORIGINS` | API | Comma-separated; must include frontend origin |
| `OPENAI_*`, `PINECONE_*` | API | RAG + embeddings |
| `NEXT_PUBLIC_API_BASE_URL` | Frontend (build) | Public API base URL, **no trailing slash** |

Local development is unchanged: `docker compose` and `.env` as in the main README.
