# Development Guide

## Repository structure

```
Major Project Cursor/
├── src/                    # Python backend
│   ├── main.py             # FastAPI app and routes
│   ├── api/                # Pydantic request/response schemas
│   ├── config/             # Settings (pydantic-settings)
│   ├── core/               # RAG pipeline, retrieval, NLP utilities
│   ├── ingestion/          # CSV/PDF → chunk → embed → Pinecone
│   ├── models/             # SQLAlchemy models, DB session, seeds
│   └── utils/              # Logging, safe imports
├── frontend/               # Next.js web UI
│   ├── app/                # Pages (chat, history, analytics)
│   ├── components/         # Shared React components
│   └── lib/api.ts          # Typed API client
├── data/                   # FAQ CSVs, evaluation gold set
├── tests/                  # pytest suite
├── experiments/            # RAG evaluation scripts and results
├── Docs/                   # Project documentation
├── docker-compose.yml
├── Dockerfile              # API container
├── render.yaml             # Render Blueprint
└── requirements.txt
```

## Running tests

```bash
pip install -r requirements.txt
python -m pytest -q
```

Tests use an in-memory SQLite database and do not require OpenAI or Pinecone keys.

| Test file | Coverage |
|-----------|----------|
| `test_smoke.py` | App import, `/health` endpoint |
| `test_small_talk.py` | Small-talk detection and routing |
| `test_analytics_sentiment.py` | Analytics and sentiment aggregation |

CI runs on every push/PR via `.github/workflows/tests.yml` (Python 3.11, Ubuntu).

## Key extension points

### Add FAQ content

1. Add rows to a CSV (see `data/sample_faqs.csv` format) or add PDFs.
2. Re-run ingestion:
   ```bash
   python -m src.ingestion.ingest --source data/your_file.csv --type csv
   ```

### Adjust prompts

Edit `src/core/prompt_builder.py` for system instructions and context formatting.

### Change handoff rules

Edit `src/core/handoff_detector.py` (keyword patterns, sentiment threshold, failure count).

### Change intent labels

Edit `src/core/intent_classifier.py` (keyword patterns and LLM classification prompt).

## Experiments and evaluation

| Script | Purpose |
|--------|---------|
| `experiments/run_rag_evaluation.py` | Batch eval: top_k=3 vs 5, guardrails, embedding similarity |
| `experiments/chunking_experiment.py` | Compare chunk sizes (requires re-ingestion per size) |

Outputs land in `experiments/results/`. See [README_EVALUATION.md](../experiments/README_EVALUATION.md).

## Logging

Configured in `src/utils/logger.py` using `LOG_LEVEL` from settings. The FastAPI app logger name is `app`.

## Code conventions

- Python 3.10+ type hints, `from __future__ import annotations` where used
- Pydantic v2 models for API I/O
- SQLAlchemy 2.0 declarative models
- Optional dependencies fail gracefully (`safe_optional.py`) so tests run without all API keys

## Docker builds

**API:** `Dockerfile` at repo root — Python 3.11-slim, exposes port 8000 (or `PORT` env).

**Frontend:** `frontend/Dockerfile` — multi-stage Next.js build with `NEXT_PUBLIC_API_BASE_URL` build arg.

## Report / thesis evidence

For MSc Chapters 5–7, capture:

- Swagger UI screenshots (`/docs`)
- Sample `/chat` responses with `metadata.retrieval.source_ids`
- `/analytics` JSON output
- Ingestion CLI logs
- `experiments/results/RAG_EVAL_SUMMARY.md`

Stored `retrieved_context` on each assistant message provides traceability for faithfulness analysis.
