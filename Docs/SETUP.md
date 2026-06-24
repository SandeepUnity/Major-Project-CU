# Setup Guide

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.10+ (3.11 recommended) |
| Node.js | 20+ (for frontend dev) |
| Docker Desktop | Optional but recommended for PostgreSQL |
| OpenAI API key | Required for chat and embeddings |
| Pinecone API key | Required for retrieval |
| Pinecone index | Dimension **1536** (`text-embedding-3-small`) |

Create a Pinecone serverless index named e.g. `empowertech-rag` before ingesting documents.

---

## Option A: Local Python development

### 1. Virtual environment

```bash
python -m venv .venv
.\.venv\Scripts\activate        # Windows PowerShell
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

### 2. Environment file

```bash
copy .env.example .env          # Windows
# cp .env.example .env          # macOS / Linux
```

Edit `.env` and set at minimum:

- `OPENAI_API_KEY`
- `PINECONE_API_KEY`
- `PINECONE_INDEX_NAME` (must match your Pinecone index)
- `DATABASE_URL` (default works with compose Postgres below)

### 3. PostgreSQL

**Docker (recommended):**

```bash
docker compose up -d postgres
```

Default connection: `postgresql://postgres:postgres@localhost:5432/empowertech_chatbot`

### 4. Initialize database

```bash
python -m src.models.init_db
python -m src.models.seed_db      # optional demo users
```

Tables are also auto-created when the API starts, but running `init_db` explicitly is fine for first setup.

### 5. Ingest knowledge base

```bash
# Sample FAQs (quick test)
python -m src.ingestion.ingest --source data/sample_faqs.csv --type csv

# Full knowledge base
python -m src.ingestion.ingest --source data/knowledge_base_faqs.csv --type csv

# PDF (if you have course/policy PDFs)
python -m src.ingestion.ingest --source path/to/document.pdf --type pdf
```

Optional chunk tuning:

```bash
python -m src.ingestion.ingest --source data/sample_faqs.csv --type csv --chunk-size 600 --chunk-overlap 100
```

### 6. Run API

```bash
uvicorn src.main:app --reload
```

- Swagger UI: http://localhost:8000/docs
- Health: http://localhost:8000/health

### 7. Run frontend (separate terminal)

```bash
cd frontend
npm install
npm run dev
```

UI: http://localhost:3000 (defaults to API at `http://localhost:8000`)

---

## Option B: Full-stack Docker Compose

Runs **frontend + API + PostgreSQL** together.

### 1. Configure `.env`

For compose networking, set:

```
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/empowertech_chatbot
```

Plus `OPENAI_API_KEY` and `PINECONE_API_KEY`.

### 2. Start all services

```bash
docker compose up --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |

### 3. Initialize DB (from host, with venv active)

```bash
python -m src.models.init_db
python -m src.models.seed_db
```

Use `localhost` in `DATABASE_URL` when running scripts from the host (port 5432 is published).

### 4. Ingest vectors (from host)

```bash
python -m src.ingestion.ingest --source data/knowledge_base_faqs.csv --type csv
```

See [Demo (Docker)](DEMO_README.md) for curl walkthrough.

---

## Verify installation

```bash
# Health check
curl http://localhost:8000/health

# Run tests (uses in-memory SQLite, no external keys needed)
python -m pytest -q
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `postgres` connection refused | Ensure `docker compose up -d postgres` is running |
| Empty / fallback answers | Run ingestion; confirm Pinecone index name and namespace |
| CORS errors from frontend | API allows localhost:3000 by default; set `CORS_ORIGINS` in production |
| Slow first request on Render | Free tier cold start; see [Deploy (Render)](DEPLOY_RENDER.md) |
| RAGAS import fails on Windows | Use WSL2/Docker for full RAGAS evaluation (see [experiments README](../experiments/README_EVALUATION.md)) |

---

## Production deployment

See [Deploy (Render)](DEPLOY_RENDER.md) for the `render.yaml` Blueprint (Postgres + API + Next.js).
