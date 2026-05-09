Chapter-by-Chapter Skeleton for MSc (Data Science) Project Report

Target: 60–80 pages, ~18,000–25,000 words

Preliminaries (not counted in chapters pages):
- Cover Page
- Bonafide Certificate
- Declaration
- Acknowledgement
- Abstract (150–250 words)
- Table of Contents
- List of Figures, Tables, Abbreviations

Implemented artifacts to cite in the report (current repo):
- API: `src/main.py` (FastAPI app) + Swagger at `/docs`
- Schemas: `src/api/schemas.py`
- Core RAG orchestration: `src/core/chat_orchestrator.py`
- Retrieval + vector store: `src/core/retriever.py`, `src/core/vector_store.py`
- Prompt + guardrails: `src/core/prompt_builder.py` and fallback behavior in orchestrator
- Intent + sentiment + handoff: `src/core/intent_classifier.py`, `src/core/sentiment_analyzer.py`, `src/core/handoff_detector.py`
- DB models + init/seed: `src/models/database.py`, `src/models/init_db.py`, `src/models/seed_db.py`
- Ingestion: `src/ingestion/ingest.py`, `src/ingestion/pipeline.py` + parsers/chunking
- Demo: `Dockerfile`, `docker-compose.yml`, `docs/DEMO_README.md`
- Tests/CI: `tests/test_smoke.py`, `.github/workflows/tests.yml`
- Sample data: `data/sample_faqs.csv`, `data/evaluation_queries.csv`
- Phase-2 scaffold: `src/core/ragas_evaluator.py`, `experiments/chunking_experiment.py`

Chapter 1 — Introduction (5–8 pages)
- Background and motivation for EmpowerTech RAG chatbot
- Problem statement and research questions
- Project objectives (technical + data science)
- Scope and limitations
- Overview of report structure
- Evidence to include:
  - System context diagram (users → API → retrieval → LLM → DB/analytics) (Figure 1.x)

Chapter 2 — Literature Review / System Study (8–12 pages)
- Survey of RAG systems, retrieval methods, vector DBs
- Prior work on hallucination detection, RAGAS, evaluation frameworks
- Comparative analysis of methods and gap identification (justify RAGAS + Performance Matrix)
- Required figures/tables: comparative table of related work (1–2)

Chapter 3 — System Analysis (8–10 pages)
- Functional and non-functional requirements
- Use cases and user stories
- Feasibility (technical, economic, operational)
- Data sources and privacy considerations
- Required diagrams: Use case diagram, DFD Level 0/1 (2–3)
- Evidence to include:
  - Requirements mapping table (spec → implementation module/file)
  - Privacy note: email is optional; user identity is `user_id` (aligns with minimal data collection)

Chapter 4 — System Design (10–15 pages)
- High-level architecture diagram (component diagram)
- Database schema (ER diagram) and table descriptions
- API design (endpoints, schemas)
- Prompt engineering & augmentation layer design
- Sequence diagrams for chat flow
- UML diagrams required by guideline: Use Case, Class, Sequence, Activity
- Required figures: ER diagram, architecture, sequence diagrams, class + activity diagrams (5–8)
- Evidence to include (tie to concrete files):
  - API contract: endpoints implemented in `src/main.py`, request/response in `src/api/schemas.py`
  - DB design: tables in `src/models/database.py` + init script `src/models/init_db.py`
  - Retrieval design: Pinecone + embeddings in `src/core/vector_store.py`, retrieval in `src/core/retriever.py`
  - Guardrail design: fallback message + threshold in `src/core/chat_orchestrator.py`

Chapter 5 — Implementation (12–20 pages)
- Development environment and stack
- Key modules (retriever, intent classifier, orchestrator, LLM client)
- Ingestion pipeline and chunking strategy
- Deployment/demo instructions (Docker Compose summary)
- Code structure (short excerpts) and version control practices
- Important code snippets (explain logic; do not paste large blocks)
- Evidence to include (screenshots/logs):
  - Swagger UI: `/docs` showing `/session`, `/chat`, `/history`, `/analytics`, `/health`
  - CLI demo commands + outputs:
    - `python -m src.models.init_db`
    - `python -m src.models.seed_db`
    - `python -m src.ingestion.ingest --source data/sample_faqs.csv --type csv`
  - Guardrail evidence: `/chat` response when no/low context (fallback message)
  - Demo artifacts: `Dockerfile`, `docker-compose.yml`, `docs/DEMO_README.md`

Chapter 6 — Testing (6–8 pages)
- Unit test strategy and sample test cases
- Integration & API tests
- Test coverage metrics and methodology (how coverage measured)
- Bug reports and fixes summary
- Required tables: sample test case table, coverage summary
- Evidence to include:
  - Smoke test: `tests/test_smoke.py` (imports app, creates tables, checks `/health`)
  - CI evidence (GitHub Actions): `.github/workflows/tests.yml` (screenshot of passing run)
  - Test case table: `/health`, `/session`, `/chat` (guardrail), `/history`, `/analytics`

Chapter 7 — Results, Experiments & Discussion (target 6–10 pages; keep core narrative concise)
- RAGAS evaluation framework description and setup
- Performance Matrix experiment
  - Experiment design (IVs, DVs, sample size justification)
  - Pilot (30 queries) and final (target 100 queries)
  - Baselines (LLM w/o retrieval, retrieval-only)
  - Manual annotation protocol (3 annotators, agreement metrics)
- Statistical analysis (ANOVA/Kruskal-Wallis, post-hoc tests, effect sizes, CIs)
- Visualizations: Chunk size vs metrics, boxplots, heatmaps
- Intent-stratified analysis and sentiment correlation
- Discussion: interpretation of results, threats to validity
- Required figures/tables: results tables, plots (6–10)
- Note: move detailed per-condition plots, raw experiment outputs, and full statistical printouts to Appendices to keep Chapter 7 within typical guideline page ranges.
- Evidence to include (current implementation status):
  - RAGAS integration point exists: `src/core/ragas_evaluator.py` (scaffold)
  - Experiment runner scaffold exists: `experiments/chunking_experiment.py`
  - Evaluation dataset starter: `data/evaluation_queries.csv`
  - Note: The full Performance Matrix (multi-index chunk sizes + statistical tests + plots) will be produced by extending the experiment scripts and exporting results (figures/tables) into Chapter 7 + Appendices.

Chapter 8 — Conclusion & Future Work (3–5 pages)
- Summary of contributions and findings
- Limitations
- Practical recommendations (chunk size, retrieval settings)
- Future research and deployment steps

Chapter 9 — References
- APA format, 20+ credible sources for MSc

Chapter 10 — Appendices
- Full source code (link to GitHub + essential files included)
- `db_dump.sql` and schema export
- Demo README with `docker-compose` instructions
- Evaluation datasets and annotation guidelines
- Additional plots and raw experiment outputs
- Evidence to include:
  - `docs/DEMO_README.md` (full step-by-step run instructions)
  - Example request/response transcripts (JSON outputs) for `/chat` and `/analytics`

Deliverables & Artifacts (place in repo root and `docs/`):
- `report.pdf` (final compiled PDF)
- `presentation.pptx` and `presentation.pdf`
- `docs/DEMO_README.md` (demo run instructions)
- `docs/PERFORMANCE_MATRIX_REPORT.md` and supporting notebooks
- GitHub repo with full source code and a small seeded dataset
- (Optional) Hosted demo URL and access instructions

Notes on word/page budgeting:
- Aim for denser experimental chapters (Ch5–Ch7) as they carry thesis value
- Use figures and tables to present experimental results concisely
- Keep code in appendices and reference snippets in main text

Recommended next steps:
1. Seed knowledge base to reach 100+ QA pairs for robust experiments
2. Draft Chapter 1–4 content and diagrams in parallel with implementation
3. Run pilot experiments (30 queries) to validate evaluation pipeline before full 100-query run

