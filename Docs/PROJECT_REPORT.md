# EmpowerTech RAG Chatbot — Academic Project Report

**Document type:** Draft for conversion to PDF (Times New Roman, 12 pt, 1.5 line spacing, 1 in margins per institute guidelines).

**Note:** Paste official logo and Qollabb certificate in the Word version. Replace bracketed placeholders (`[...]`) with your details.

---

## Cover Page (preliminary)

| Field | Content |
|-------|---------|
| **Project Title** | EmpowerTech RAG Chatbot: A Retrieval-Augmented Generation System for Student Support |
| **Subtitle** | Submitted in partial fulfillment of the requirements for the award of the degree of **[BCA / MCA / MSc (Data Science)]** |
| **Student Name** | [Student Name] |
| **Enrollment No.** | [Enrollment Number] |
| **Guide/Mentor** | [Guide Name] |
| **Institution** | [Institution Name] |
| **Academic Year** | [Year] |

---

## Bonafide Certificate

*Institute and Guide bonafide certificate as per prescribed format — attach original.*

---

## Declaration

I, **[Student Name]**, hereby solemnly declare that the project report titled **"EmpowerTech RAG Chatbot: A Retrieval-Augmented Generation System for Student Support"** submitted in partial fulfillment of the requirements for the award of the degree of **[BCA / MCA / MSc (Data Science)]** is my original work.

I further declare that:

- This project has been carried out by me during the academic year **[Year]** under the supervision of **[Guide Name]**.
- The work has not been submitted previously to any other university, institution, or examination body for the award of any degree, diploma, or certification.
- All sources of information used in this report have been duly acknowledged and referenced in accordance with academic ethics and plagiarism norms.
- The data presented in this report is authentic to the best of my knowledge and has not been fabricated or manipulated.

Place: [City]  Date: [Date]  

Student Signature: _______________  Student Name: [Student Name]  Enrollment No.: [Number]

---

## Acknowledgement

I express sincere gratitude to my project guide, **[Guide Name]**, for continuous guidance, technical feedback, and encouragement throughout this work. I thank the faculty of **[Department / Institution]** for foundational training in software engineering, databases, and machine learning. I acknowledge the use of official documentation and research literature cited in Chapter 9. Finally, I thank my family and peers for their support during the development and evaluation of this system.

---

## Abstract

**EmpowerTech RAG Chatbot** is a retrieval-augmented generation (RAG) system designed to answer student and learner queries for an online education context (EmpowerTech Solutions) using a curated knowledge base, a vector index for semantic retrieval, and a large language model for grounded responses. The project implements a **FastAPI** backend with **PostgreSQL** for sessions and message audit trails, **Pinecone** for vector storage of embedded FAQ and document chunks, and **OpenAI** APIs for embeddings (`text-embedding-3-small`, 1536 dimensions) and chat completion (`gpt-4o` by configuration). Guardrails restrict answers when retrieval is empty or below a confidence threshold, reducing hallucination risk and encouraging human handoff. The system classifies query intent, analyzes sentiment (VADER-based path), and detects handoff conditions. A **Next.js** web frontend provides chat, history, and analytics views, with **Docker Compose** orchestrating the API, database, and UI for reproducible deployment. Development followed an iterative approach (prototype → integration → testing). Automated smoke tests and GitHub Actions CI validate API health. The knowledge base includes **110+** structured FAQ rows (`data/knowledge_base_faqs.csv`) ingested through a chunking and embedding pipeline; evaluation query sets scaffold future RAGAS-style assessment. The work demonstrates a working end-to-end RAG service suitable for academic demonstration and extension toward formal retrieval evaluation.

*(Word count for abstract body: approximately 230 words.)*

---

## Table of Contents

0. [Detailed descriptions of figures and tables](#detailed-descriptions-of-figures-and-tables)  
1. [Chapter 1 — Introduction](#chapter-1--introduction)  
2. [Chapter 2 — Literature Review / System Study](#chapter-2--literature-review--system-study)  
3. [Chapter 3 — System Analysis](#chapter-3--system-analysis)  
4. [Chapter 4 — System Design](#chapter-4--system-design)  
5. [Chapter 5 — System Implementation](#chapter-5--system-implementation)  
6. [Chapter 6 — Testing](#chapter-6--testing)  
7. [Chapter 7 — Results and Discussion](#chapter-7--results-and-discussion)  
8. [Chapter 8 — Conclusion and Future Scope](#chapter-8--conclusion-and-future-scope)  
9. [Chapter 9 — References](#chapter-9--references)  
10. [Chapter 10 — Appendices](#chapter-10--appendices)  

*(Regenerate page numbers in Microsoft Word: References → Table of Contents.)*

---

## List of Figures

| Fig. | Title (planned / in document) |
|------|--------------------------------|
| 1.1 | System context: users, API, RAG stack, persistence |
| 3.1 | Data Flow Diagram (Level 0) |
| 3.2 | Data Flow Diagram (Level 1) |
| 3.3 | Use case diagram (learner, system, admin) |
| 4.1 | High-level component architecture |
| 4.2 | ER diagram (users, sessions, messages, feedback) |
| 4.3 | Sequence diagram — chat request |
| 4.4 | Activity diagram — guardrail and handoff |
| 4.5 | Simplified UML class diagram — core services |
| 5.1 | Code: FastAPI app CORS middleware and REST routes (`main.py`) |
| 5.2 | Code: environment-driven settings (`settings.py`) |
| 5.3 | Code: guardrail branch in chat orchestrator |
| 5.4 | Code: CSV ingestion pipeline and batched Pinecone upsert |
| 5.5 | Code: text chunking (LangChain with Windows fallback) |
| 5.6 | Code: Next.js typed API client (`frontend/lib/api.ts`) |
| 5.7 | Code: chat send path and session handling (`frontend/app/page.tsx`) |
| 5.8 | Runtime: Swagger UI `/docs` |
| 5.9 | Runtime: Swagger `POST /chat` JSON (successful RAG) |
| 5.10 | Runtime: Swagger or UI showing guardrail / fallback reply |
| 5.11 | Terminal: successful CSV ingestion log |
| 5.12 | Terminal: API server startup (`uvicorn`) |
| 5.13 | Browser: EmpowerTech chat page with transcript |
| 5.14 | Browser: Analytics page summary metrics |
| 6.1 | Optional: CI passing run and Swagger `/docs` evidence |
| 7.1 | Example analytics conceptual view (session/message counts) |

*(Capture screenshots of Mermaid renders or redraw in draw.io for final submission.)*

---

## List of Tables

| Table | Title |
|-------|--------|
| 3.1 | Functional requirements vs implementation mapping |
| 3.2 | Non-functional requirements |
| 4.1 | REST API endpoints summary |
| 4.2 | Database tables summary |
| 6.1 | API functional and integration test cases |
| 6.2 | Error handling validation and boundary tests |
| 6.3 | RAG retrieval guardrails and ingestion tests |
| 6.4 | Frontend and manual end-to-end tests |
| 6.5 | Automation continuous integration and tooling |
| 7.1 | Pilot RAG offline evaluation (paired *top_k* summary) |
| — | *Supplementary:* Technology stack (§1.6); comparative approaches (§2.6)—see [detailed descriptions](#detailed-descriptions-of-figures-and-tables), Part III |

---

## List of Abbreviations

| Abbreviation | Expansion |
|--------------|-----------|
| API | Application Programming Interface |
| CI | Continuous Integration |
| CORS | Cross-Origin Resource Sharing |
| DFD | Data Flow Diagram |
| ER | Entity–Relationship |
| FAQ | Frequently Asked Question |
| JSON | JavaScript Object Notation |
| JWT | JSON Web Token *(if adopted later)* |
| LLM | Large Language Model |
| ORM | Object–Relational Mapping |
| RAG | Retrieval-Augmented Generation |
| RAGAS | Retrieval Augmented Generation Assessment *(framework)* |
| REST | Representational State Transfer |
| SQL | Structured Query Language |
| UI | User Interface |
| UML | Unified Modeling Language |
| UX | User Experience |
| UPI | Unified Payments Interface *(domain context)* |
| VADER | Valence Aware Dictionary and sEntiment Reasoner |

---

## Detailed descriptions of figures and tables {#detailed-descriptions-of-figures-and-tables}

Academic guidelines require that every **figure and table be numbered, titled, and explained in the body** of the report. The subsections below summarize **what each artifact shows**, **how to read it**, and **how it supports the argument** of the corresponding chapter. When converting to Word/PDF, paste the short paragraph under the same number **immediately below** the figure or table caption, or consolidate this section as an early appendix if your institution prefers all extended commentary in one place.

---

### Part I — Figure descriptions

**Figure 1.1 — System context diagram** depicts the **boundary** of the solution: the learner acts through a **browser** running the Next.js client; all business logic and orchestration run in the **FastAPI** application, which is the only component that talks directly to **PostgreSQL** (relational state), **Pinecone** (vector search), and **OpenAI** (embedding and chat APIs). Arrows indicate **direction of dependency or call flow** (not batch data volume). The diagram answers *who uses what* at the highest level without internal module detail.

**Figure 3.1 — DFD Level 0 (context)** is a **data-flow** view: a single process bubble represents the entire “EmpowerTech RAG System.” The **User** exchanges queries and answers with that process; the system reads and writes **PostgreSQL**, retrieves from the **Vector DB**, and ingests from **Knowledge Base files**. Unlike the component diagram, emphasis is on **data stores** and **flows** rather than technology brands.

**Figure 3.2 — DFD Level 1** **decomposes** the context process into five numbered subprocesses: manage session, process chat, retrieve context, generate answer, and persist messages. It shows how chat processing **calls** retrieval and how both **read/write** paths hit the databases. Use it to explain **order of operations** to non-programmer stakeholders.

**Figure 3.3 — Use case diagram** places the **Learner** outside the system boundary and connects the actor to four **oval** use cases: create session, ask question, view history, and view summary statistics. It defines **functional scope from a user perspective** and supports test-case traceability in Chapter 6.

**Figure 4.1 — Component architecture** organizes the software into **presentation** (Next.js), **application** (FastAPI, orchestrator, retriever, LLM client, intent/sentiment/handoff/prompt components), and **data** (PostgreSQL, Pinecone). Internal arrows show **Orchestrator** as the integration hub. It bridges high-level design with file-level packages in Chapter 5.

**Figure 4.2 — ER diagram** specifies **cardinality**: one user has many chat sessions; each session has many messages; each message has at most one feedback row. Attribute lists summarize **primary keys** and **foreign keys**. Examiners use it to verify normalization and to relate ORM classes in `database.py` to the schema.

**Figure 4.3 — Sequence diagram (successful RAG)** shows the **time order** of synchronous calls for a happy path: HTTP post, orchestration, history load, retrieval, guardrail pass, LLM completion, persistence, JSON response. Lifelines are **User, API, Orchestrator, DB, Retriever, LLM** (Pinecone activity is implicit inside Retriever unless expanded). The `alt` fragment would state the **fallback** branch when retrieval fails.

**Figure 4.4 — Activity diagram** is a **flowchart** parallel to orchestration code: classify → retrieve → **decision** diamond on empty/low-confidence context → fallback **or** build prompt → LLM → evaluate handoff → save. It makes guardrail logic auditable without reading Python.

**Figure 4.5 — Class diagram** shows **structural dependency** among `ChatOrchestrator`, `Retriever`, `LLMClient`, and `ConversationManager` (method names abbreviated). Dependency edges mean “uses”; they do not imply inheritance.

**Figures 5.1–5.7 — Code listings** are **screenshots of source** (not diagrams). Each illustrates one **implementation artifact**: routing and CORS (5.1), configuration knobs (5.2), guardrail branch (5.3), ingestion batching (5.4), chunking fallback (5.5), client API helpers (5.6), React send path (5.7). Captions should repeat **file path and approximate line span** so reviewers can locate the excerpt in Git.

**Figure 5.8 — Swagger `/docs`** is a **runtime** capture of generated OpenAPI documentation: expandable operation groups, schemas, “Try it out” buttons. It proves **discoverability** of the REST contract.

**Figure 5.9 — Swagger `POST /chat` response** should show **request JSON** (user id, session id, query) and **response JSON** including `response`, `intent`, `confidence`, `handoff_trigger`, nested `metadata` when present. Validates successful RAG for viva/demo.

**Figure 5.10 — Guardrail / fallback** depicts either Swagger or UI showing the **canonical fallback string** or `metadata.guardrail` set to `no_context` or `low_confidence`. Demonstrates **safety behaviour**.

**Figures 5.11–5.12 — Terminal transcripts** capture **CLI evidence**: ingestion completion counts and server startup (host/port) **without leaking API keys**.

**Figures 5.13–5.14 — Browser UI** show **end-user polish**: conversational transcript and sticky layout (5.13); analytics KPIs aligning with `/analytics` (5.14).

**Figure 6.1 — CI / Swagger evidence (optional)** duplicates or zooms **automation success** (GitHub Actions green check) with API docs—useful if Chapter 5 figures are trimmed in print.

**Figure 7.1 — Analytics conceptual view** is a **planned illustrative chart** (e.g. Mermaid `xychart-beta` or exported plot) of **sessions or messages over time buckets**. The live product may only expose **aggregate** counts today; the figure clarifies **intended operational monitoring** for results discussion.

---

### Part II — Table descriptions

**Table 3.1 — Functional requirements mapping** has three columns: **requirement ID**, **short requirement statement**, and **implementation locus** (route, module, or table). It answers *where in the repo* each FR is realized and supports **traceability** to test cases in Chapter 6.

**Table 3.2 — Non-functional requirements** lists **NFR IDs**, **category** (performance, reliability, security, maintainability, portability), **statement**, and **design tactic**. It documents **how** quality attributes are addressed without mixing them into functional prose.

**Table 4.1 — REST endpoints summary** enumerates **HTTP method**, **path**, and **short description** for each public API. It is the **contract summary** aligned with OpenAPI; examiners cross-check against `main.py` and Swagger.

**Table 4.2 — Database tables summary** maps each **relation name** to its **purpose** (users, sessions, messages, feedback). It complements the ER figure for readers who prefer **tabular** schema narration over diagrams.

**Table 6.1 — API functional and integration test cases** is the **largest executable checklist**: columns include **TC ID**, **requirement trace**, **preconditions**, **procedure**, **expected result**, and placeholders for **Actual** and **Status**. Preconditions (`P0`, `P1`, `P2`) encode whether keys and DB are required so manual runs are reproducible.

**Table 6.2 — Error handling and boundary tests** focuses on **negative paths**: huge payloads, bad config, missing keys, concurrency notes. It shows the system **fails safely** (validation errors, degraded health) rather than undefined behaviour.

**Table 6.3 — RAG retrieval, guardrails, ingestion** ties **data-plane** behaviour to **TC-G** and **TC-I** IDs: retrieval quality, threshold experiments, ingest CLI, PDF path, embedding dimension consistency.

**Table 6.4 — Frontend and manual E2E tests** records **browser-level** checks (navigation, session persistence across reload, Docker bring-up, responsive layout). **Actual** column should reference **screenshot figure numbers** where applicable.

**Table 6.5 — Automation and CI tooling** is a **short workflow script** (checkout, Python setup, install, pytest). It supports claims about **continuous integration** without pasting YAML in the narrative body.

**Table 7.1 — Pilot aggregate results** aggregates **offline evaluation** across *N* = 10 paired queries: means of **embedding similarity** for two `top_k` settings, mean paired difference, and **inferential statistics** (*p*-values). Rows must be **refreshed** from `rag_eval_statistics.json` after each experiment run. The table is **not** RAGAS; the caption in Chapter 7 states the metric definition.

---

### Part III — Supplementary tabular material (unnumbered in body)

**§1.6 — Technology stack overview (table)** lists **architectural layer** (API, Data, Retrieval, Generation, UI, DevOps) against **concrete products** (FastAPI, PostgreSQL, Pinecone, OpenAI, Next.js, Docker). It is a **single-page technology map** for casual readers before deep design.

**§2.6 — Comparative perspective (table)** contrasts **Static FAQ**, **LLM-only**, **RAG (this work)**, and **Fine-tuned only** on **strengths** and **limitations**. It supports the **research gap** argument and justifies design choices without duplicating full literature review prose.

---

# Chapter 1 — Introduction

### 1.1 Background

Online education platforms process large volumes of repetitive support requests regarding enrollment, payments, schedules, technical access, and policies. Purely generative chatbots without authoritative sources risk incorrect or inconsistent answers—unacceptable for institutional trust. **Retrieval-Augmented Generation (RAG)** combines document retrieval with language generation so responses can be grounded in approved knowledge bases (FAQs, handbooks, policies).

This project builds **EmpowerTech RAG Chatbot**, a domain-specific assistant framed around EmpowerTech Solutions–style programs (courses, payments, refunds, certificates). The system prioritizes traceability (stored retrieval context), safety (guardrails when evidence is weak), and operability (REST API, web UI, Docker deployment).

### 1.2 Problem Statement

Traditional FAQ pages require manual search; generic LLM chat lacks verifiable sources. The problem addressed is: **how to deliver accurate, traceable, session-aware support answers grounded in institutional knowledge**, with detection of when a human advisor should take over.

### 1.3 Objectives

**Primary objectives**

1. Design and implement a RAG pipeline: ingest structured FAQs (CSV), chunk text, embed, store in a vector database, retrieve by semantic similarity, and generate answers with explicit grounding behavior.

2. Persist conversations (users, sessions, messages, optional feedback fields for future RAGAS metrics) in a relational database.

3. Provide guardrails when retrieval is empty or low-confidence; trigger handoff hints aligned with sentiment and repeated failure patterns.

4. Expose a documented REST API and a modern web frontend for demonstration and usability testing.

5. Package the stack with Docker Compose for repeatable deployment.

**Secondary objectives**

- Record intent (transactional / informational / general) and sentiment features for analytics.  
- Scaffold evaluation hooks (`evaluation_queries.csv`, RAGAS-related fields on feedback).  

### 1.4 Scope

**In scope:** FAQ and document ingestion paths (CSV implemented; PDF path in codebase), vector retrieval, OpenAI chat completion under policy constraints, PostgreSQL persistence, basic analytics endpoint, Next.js UI (chat, history, analytics), CORS for local dev, health checks, automated smoke tests.

**Out of scope (current phase):** Production payment gateway integration, role-based admin console, SSO, multilingual models, full-scale RAGAS batch experiments with statistical analysis (scaffold only), mobile native apps.

### 1.5 Existing vs Proposed System

**Existing (manual / static):** Static FAQ pages and email support—high latency, inconsistent wording, poor scalability.

**Proposed:** A **RAG-backed** assistant with **session memory**, **retrieval trace storage**, **guardrails**, and **API-first** integration for future channels (widget, LMS).

### 1.6 Technologies (overview)

| Layer | Technology |
|-------|------------|
| API | Python 3.x, FastAPI, Uvicorn |
| Data | PostgreSQL, SQLAlchemy ORM |
| Retrieval | Pinecone, OpenAI embeddings |
| Generation | OpenAI Chat Completions |
| UI | Next.js (React), TypeScript |
| DevOps | Docker, Docker Compose, GitHub Actions |

### 1.7 Report Organization

Chapter 2 reviews RAG and related work. Chapter 3 analyzes requirements and feasibility. Chapter 4 presents design diagrams and schema. Chapter 5 details implementation. Chapter 6 covers testing. Chapter 7 discusses results and limitations. Chapter 8 concludes. References and appendices follow.

### 1.8 System Context

**Figure 1.1 — System context diagram**

```mermaid
flowchart LR
  subgraph Users
    L[Learner / Student]
  end
  subgraph Client
    W[Web Browser — Next.js UI]
  end
  subgraph Backend
    API[FastAPI — RAG Orchestrator]
    PG[(PostgreSQL)]
    PC[(Pinecone Vector Index)]
    OAI[OpenAI — Embeddings & Chat]
  end
  L --> W
  W -->|HTTPS REST| API
  API --> PG
  API --> PC
  API --> OAI
```

*Figure 1.1 situates the learner at the browser, the API as the orchestration hub, and external services for persistence, vectors, and LLM calls.*

---

# Chapter 2 — Literature Review / System Study

### 2.1 Retrieval-Augmented Generation

Lewis *et al.* introduced RAG as a mechanism to combine parametric knowledge (language model) with non-parametric memory (retrieved passages), improving factual grounding for knowledge-intensive tasks. Subsequent surveys synthesize indexing strategies, retrievers, and fusion methods. For domain FAQs, dense retrieval using neural embeddings is standard: queries and documents share an embedding space; **cosine similarity** (or dot product in normalized setups) ranks chunks.

### 2.2 Vector Databases and Embeddings

Pinecone and similar systems provide managed **approximate nearest neighbor** search at scale. OpenAI’s `text-embedding-3-small` offers a balance of cost and quality with **1536-dimensional** vectors—index dimension must match embedding size to avoid runtime errors.

### 2.3 Evaluation of RAG

**RAGAS** and related frameworks score faithfulness, answer relevance, and context recall. This project stores optional metric columns on the feedback model for future batch evaluation; a full study is reserved for extension.

### 2.4 Sentiment and Intent

Rule-based sentiment (**VADER**) suits short, informal queries. Intent categories (transactional vs informational) support routing and analytics; lightweight classification may use LLM or keyword heuristics depending on configuration.

### 2.5 Web APIs and Frontends

**REST**-style JSON APIs (FastAPI) integrate cleanly with **Next.js** SPAs. **CORS** must be configured when browsers call APIs on another origin/port.

### 2.6 Comparative Perspective

| Approach | Strengths | Limitations |
|----------|-----------|-------------|
| Static FAQ | Simple | No dialogue, no personalization |
| LLM-only | Fluent | Hallucination risk |
| RAG (this work) | Grounded, auditable | Depends on KB quality and retrieval thresholds |
| Fine-tuned only | Domain tone | Expensive; still needs freshness |

### 2.7 Research Gap Addressed

Many demos omit **persistent traceability** and **explicit guardrails**. This work stores retrieved-context metadata per assistant message (when available) and applies a **confidence threshold** to refuse unsupported answers—reducing unchecked generation.

### 2.8 Software Process

An **iterative / agile** loop was used: vertical slice (ingest → query → chat) followed by UI, Docker, and tests—aligned with academic project timelines.

---

# Chapter 3 — System Analysis

### 3.1 Functional Requirements

**Table 3.1 — Functional requirements mapping**

| ID | Requirement | Implementation |
|----|-------------|----------------|
| FR1 | Create user and chat session | `POST /session`, `ConversationManager`, `users`, `chat_sessions` |
| FR2 | Submit query and receive grounded reply | `POST /chat`, `ChatOrchestrator`, `Retriever`, `LLMClient` |
| FR3 | View session history | `GET /history` |
| FR4 | Platform analytics summary | `GET /analytics` |
| FR5 | Ingest FAQs/documents into vector store | `src/ingestion/ingest.py`, `IngestionPipeline` |
| FR6 | Health status for demo | `GET /health` |
| FR7 | Web UI for chat | `frontend/app/page.tsx`, `lib/api.ts` |

### 3.2 Non-Functional Requirements

**Table 3.2 — Non-functional requirements**

| ID | Category | Requirement | Approach |
|----|----------|-------------|----------|
| NFR1 | Performance | Responsive API under modest load | Async-friendly FastAPI; vector batch upsert |
| NFR2 | Reliability | Graceful degradation | Health check; guardrail path without LLM when no context |
| NFR3 | Security | No secrets in source | Environment variables (`.env`); keys not committed |
| NFR4 | Maintainability | Modular packages | `core`, `ingestion`, `models`, `api` |
| NFR5 | Portability | Reproducible demo | Docker Compose |

### 3.3 Users

- **Learner:** asks questions, reads answers, may escalate implicitly via handoff flag.  
- **Developer/Admin (offline):** runs ingestion, monitors logs (future admin UI out of scope).

### 3.4 Feasibility

- **Technical:** Mature APIs (OpenAI, Pinecone, SQLAlchemy) — feasible within student budget using low-cost embedding model and controlled traffic.  
- **Economic:** Pay-per-use cloud APIs; Pinecone free/low tier may apply.  
- **Operational:** Docker Compose reduces install friction for evaluators.

### 3.5 Data and Privacy

`user_id` is a string identifier; **email is optional**. Conversation content may include personal study questions—production deployments would add retention policies and consent text.

### 3.6 Data Flow — Level 0

**Figure 3.1 — DFD Level 0 (context)**

```mermaid
flowchart LR
  U[User]
  S[EmpowerTech RAG System]
  K[(Knowledge Base Files)]
  V[(Vector DB)]
  D[(PostgreSQL)]
  U <-->|Queries / Answers| S
  S <-->|Read / Write| D
  S <-->|Retrieve| V
  S <-->|Ingest from| K
```

### 3.7 Data Flow — Level 1

**Figure 3.2 — DFD Level 1 (major processes)**

```mermaid
flowchart TB
  User([User])
  P1[1.0 Manage session]
  P2[2.0 Process chat]
  P3[3.0 Retrieve context]
  P4[4.0 Generate answer]
  P5[5.0 Persist messages]
  D[(DB)]
  V[(Pinecone)]
  User --> P1 --> D
  User --> P2
  P2 --> P3 --> V
  P2 --> P4
  P2 --> P5 --> D
```

### 3.8 Use Case Overview

**Figure 3.3 — Use case diagram (essential actors)**

```mermaid
flowchart TB
  Learner((Learner))
  System[EmpowerTech Chatbot System]
  Learner -->|Create session| System
  Learner -->|Ask question| System
  Learner -->|View history| System
  Learner -->|View summary stats| System
```

---

# Chapter 4 — System Design

### 4.1 Architectural Design

**Figure 4.1 — Component architecture**

```mermaid
flowchart TB
  subgraph Presentation
    FE[Next.js Frontend]
  end
  subgraph Application
    APP[FastAPI Application]
    ORCH[ChatOrchestrator]
    RET[Retriever]
    LLM[LLMClient]
    INTENT[IntentClassifier]
    SENT[SentimentAnalyzer]
    HO[HandoffDetector]
    PM[PromptBuilder]
  end
  subgraph Data
    PG[(PostgreSQL)]
    PC[(Pinecone)]
  end
  FE -->|REST JSON| APP
  APP --> ORCH
  ORCH --> RET --> PC
  ORCH --> LLM
  ORCH --> INTENT
  ORCH --> SENT
  ORCH --> HO
  ORCH --> PM
  ORCH --> PG
```

The orchestrator coordinates retrieval, optional generation, guardrails, and persistence.

### 4.2 Database Design — ER Diagram

**Figure 4.2 — Entity–Relationship diagram (conceptual)**

```mermaid
erDiagram
  USER ||--o{ CHAT_SESSION : has
  CHAT_SESSION ||--o{ CHAT_MESSAGE : contains
  CHAT_MESSAGE ||--o| FEEDBACK : may_have
  USER {
    int id PK
    string user_id UK
    string email "nullable"
    json enrolled_courses
    datetime created_at
  }
  CHAT_SESSION {
    int id PK
    string session_id UK
    int user_id FK
    datetime start_time
    int message_count
    float avg_sentiment
    boolean handoff_triggered
  }
  CHAT_MESSAGE {
    int id PK
    string message_id UK
    int session_id FK
    enum role
    text content
    string intent
    float confidence
    json retrieved_context
    json metadata
  }
  FEEDBACK {
    int id PK
    int message_id FK
    float ragas_faithfulness
    float ragas_average
    int chunking_size_used
  }
```

**Table 4.2 — Table summary**

| Table | Purpose |
|-------|---------|
| `users` | Stable learner identity (`user_id`), optional email, JSON profile hints |
| `chat_sessions` | Conversation threads, handoff flags, aggregates |
| `chat_messages` | User/assistant turns; retrieval and metadata for audit |
| `feedback` | Optional ratings and RAGAS-related experiment fields |

### 4.3 API Design

**Table 4.1 — REST endpoints**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | App status; Postgres probe; key configuration flags |
| POST | `/session` | Create session for `user_id` (optional email) |
| POST | `/chat` | RAG chat; returns intent, confidence, handoff, metadata |
| GET | `/history?session_id=` | Message list for session |
| GET | `/analytics` | Total sessions/messages aggregates |
| GET | `/docs` | Swagger UI |

Request/response models live in `src/api/schemas.py`.

### 4.4 Sequence Design — Chat Flow

**Figure 4.3 — Sequence diagram (simplified successful RAG path)**

```mermaid
sequenceDiagram
  participant U as User
  participant API as FastAPI
  participant O as Orchestrator
  participant R as Retriever
  participant L as LLM
  participant DB as PostgreSQL
  U->>API: POST /chat
  API->>O: chat(db, user_id, session_id, query)
  O->>DB: load history / persist user message
  O->>R: retrieve(query)
  R-->>O: chunks + confidence
  alt no context or low confidence
    O->>DB: persist fallback assistant message
    O-->>API: fallback text + metadata
  else sufficient context
    O->>L: generate(prompt)
    L-->>O: answer
    O->>DB: persist assistant + retrieved_context
    O-->>API: response + metadata
  end
  API-->>U: JSON
```

### 4.5 Activity — Guardrails and Handoff

**Figure 4.4 — Activity diagram**

```mermaid
flowchart TD
  A[Receive query] --> B[Classify intent & sentiment]
  B --> C[Retrieve chunks]
  C --> D{Chunks empty or confidence low?}
  D -->|Yes| E[Reply with fallback message]
  E --> F[Set handoff hint true]
  D -->|No| G[Build prompt & call LLM]
  G --> H[Evaluate handoff rules]
  H --> I[Save messages & optional feedback stub]
  F --> I
```

### 4.6 Class Diagram — Core Services

**Figure 4.5 — Simplified class-level view**

```mermaid
classDiagram
  class ChatOrchestrator {
    +chat(db, user_id, session_id, query) ChatResult
  }
  class Retriever {
    +retrieve(query) RetrievalResult
  }
  class LLMClient {
    +complete(messages) str
  }
  class ConversationManager {
    +create_session(db, user)
    +add_message(...)
    +load_history(...)
  }
  ChatOrchestrator --> Retriever
  ChatOrchestrator --> LLMClient
  ChatOrchestrator --> ConversationManager
```

### 4.7 UI/UX Design

The frontend uses a **card-based** layout: sticky header, chat transcript, message input, navigation to **History** and **Analytics**. Environment variable `NEXT_PUBLIC_API_BASE_URL` targets the API (e.g. `http://localhost:8000`). Wireframes can be exported from the running UI as screenshots for Chapter 5/7.

### 4.8 Retrieval and Guardrail Parameters

Configurable via settings (environment): `retrieval_top_k` (default 5), `retrieval_confidence_threshold` (default 0.3), `chat_history_limit` (default 10). These tie directly to design trade-offs between recall and precision.

---

# Chapter 5 — System Implementation

### 5.1 Development Environment

- **OS:** Windows 10/11 (development); Linux containers for deployment.  
- **IDE:** VS Code / Cursor.  
- **Python:** Virtual environment recommended (`python -m venv .venv`).  
- **Node.js:** For Next.js frontend build.  
- **Version control:** Git; remote optional (GitHub).

### 5.2 Toolchain and Libraries

| Component | Role |
|-----------|------|
| FastAPI | HTTP routing, validation, OpenAPI |
| SQLAlchemy | ORM, migrations via app init |
| Pydantic / pydantic-settings | Settings and schemas |
| OpenAI Python SDK | Embeddings and chat |
| Pinecone client | Vector upsert and query |
| `vaderSentiment` | Sentiment (import path hardened for container) |
| Next.js 15+ | Frontend application |

### 5.3 Hardware and Software Requirements

**Minimum (demo):** Multi-core CPU, 8 GB RAM, Docker Desktop; internet for APIs.  
**Software:** Docker Compose v2, modern browser.

### 5.4 Repository Layout (high level)

```
src/
  main.py              # FastAPI app, CORS, routes
  api/schemas.py       # Pydantic models
  config/settings.py   # Environment-driven settings
  core/                # RAG orchestration, retrieval, LLM, guardrails
  ingestion/           # CSV/PDF loaders, chunking, pipeline
  models/              # ORM entities, DB session
frontend/
  app/                 # Next.js App Router pages
  lib/api.ts           # Fetch helpers
data/
  knowledge_base_faqs.csv
  evaluation_queries.csv
docker-compose.yml
```

### 5.5 Ingestion Pipeline

1. **Parse** CSV FAQs (`load_faq_csv`) into question/answer/category/tags.  
2. **Chunk** FAQ text (`chunk_text`) — prefer LangChain recursive splitter when importable; **fallback** character-window splitter avoids native DLL issues on some Windows setups.  
3. **Embed** each chunk via `OpenAIEmbedder`.  
4. **Upsert** to Pinecone in batches (e.g. 50).  

Command:

```bash
python -m src.ingestion.ingest --source data/knowledge_base_faqs.csv --type csv
```

A successful run reports sources and chunk counts (e.g. 110 sources, 110 chunks for the current FAQ set). **Evidence:** paste terminal output under **Figure 5.11** in §5.12; listing for the pipeline appears as **Figure 5.4** in §5.11.

### 5.6 Chat Orchestration Logic

`ChatOrchestrator.chat` (conceptual order):

1. Resolve user and session.  
2. Load short history for repetition detection (counts prior fallback replies).  
3. Classify intent; analyze sentiment.  
4. Run retrieval; compute guardrail condition (`no_context` or `confidence < threshold`).  
5. On guardrail: store user message, persist assistant **fallback** string, set metadata — **no LLM** call for the answer body.  
6. Otherwise: build augmented prompt (`PromptBuilder`), call `LLMClient`, persist assistant message with `retrieved_context` for traceability.  
7. Update handoff-related session fields as implemented.

The authoritative guardrail implementation is excerpted under **Figure 5.3** in §5.11 for report screenshots.

### 5.7 Frontend Implementation

- `POST /session` obtains `session_id` stored in React state/local storage pattern as implemented.  
- `POST /chat` sends `user_id`, `session_id`, `query`.  
- **CORS** allows `http://localhost:3000` and `http://127.0.0.1:3000`.

Typed fetch helpers live in **`frontend/lib/api.ts`** (**Figure 5.6**); the **`send`** / **`ensureSession`** path is excerpted as **Figure 5.7** in §5.11—capture IDE screenshots there for implementation evidence.

### 5.8 Deployment

**Docker Compose** services:

- `frontend` — port 3000, build arg for API base URL.  
- `app` — FastAPI on 8000, loads `.env`.  
- `postgres` — port 5432, named volume for data.

Database URL in container context typically uses hostname `postgres`.

### 5.9 Security Considerations

- API keys read from environment only.  
- No plaintext secrets in repository (use `.env.example` as template).  
- Guardrails reduce unsupported medical/legal-style overreach when KB lacks coverage—**not** a replacement for domain compliance review.

### 5.10 Version Control Practice

Feature work committed with meaningful messages; CI runs on push (see Chapter 6).

### 5.11 Code listings for examiner figures (IDE screenshots)

*Instructions for the submitted PDF:* In **VS Code / Cursor**, enable **editor line numbers** (Settings → Editor: Line Numbers → `on`). Set a readable theme and zoom so print is legible (≈12–13 pt equivalent). Crop each screenshot to the relevant lines; paste **below** the figure caption in Word. Keep **exact file paths** in captions so reviewers can correlate with the repository.

Below, line ranges reference the project as committed; Git line numbers may shift slightly after edits—in that case, recapture from the cited file header.

---

**Figure 5.1 — FastAPI bootstrap, CORS, and REST route handlers**

*Screenshot target:* `src/main.py`, approximately lines **29–84** (extend through **≈109** if the report should include the `/analytics` handler).

```29:84:src/main.py
app = FastAPI(title="EmpowerTech RAG Chatbot", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = ChatOrchestrator()
conv = ConversationManager()


@app.get("/health", response_model=HealthResponse)
def health(db: Session = Depends(get_db)):
    deps: dict[str, str] = {"postgres": "unknown", "openai": "unknown", "pinecone": "unknown"}
    try:
        db.execute(select(func.now()))
        deps["postgres"] = "ok"
    except Exception as e:  # pragma: no cover
        deps["postgres"] = f"error: {e.__class__.__name__}"
    deps["openai"] = "configured" if bool(settings.openai_api_key) else "not_configured"
    deps["pinecone"] = "configured" if bool(settings.pinecone_api_key) else "not_configured"
    status = "healthy" if deps["postgres"] == "ok" else "degraded"
    return HealthResponse(status=status, dependencies=deps)


@app.post("/session", response_model=SessionCreateResponse)
def create_session(payload: SessionCreateRequest, db: Session = Depends(get_db)):
    user = conv.get_or_create_user(db, user_id=payload.user_id, email=payload.email)
    session = conv.create_session(db, user)
    db.commit()
    return SessionCreateResponse(session_id=session.session_id)


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    try:
        result = orchestrator.chat(db, user_id=payload.user_id, session_id=payload.session_id, query=payload.query)
        return ChatResponse(
            response=result.response,
            session_id=result.session_id,
            confidence=result.confidence,
            handoff_trigger=result.handoff_trigger,
            intent=result.intent,
            metadata=result.metadata,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:  # pragma: no cover
        logger.exception("chat failed")
        raise HTTPException(status_code=500, detail="Internal server error") from e
```

---

**Figure 5.2 — Environment-driven runtime settings (retrieval thresholds, models)**

*Screenshot target:* `src/config/settings.py`, class **`Settings`**.

```8:31:src/config/settings.py
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"
    openai_embedding_model: str = "text-embedding-3-small"

    # Pinecone
    pinecone_api_key: Optional[str] = None
    pinecone_index_name: str = "empowertech-rag"
    pinecone_namespace: str = "default"

    # PostgreSQL
    database_url: str = "postgresql://postgres:postgres@localhost:5432/empowertech_chatbot"

    # App
    debug: bool = False
    log_level: str = "INFO"
    chat_history_limit: int = 10
    retrieval_top_k: int = 5
    retrieval_confidence_threshold: float = 0.3
```

---

**Figure 5.3 — Guardrail branch: fallback without LLM when retrieval is missing or weak**

*Screenshot target:* `src/core/chat_orchestrator.py`, guardrail block after user message persistence.

```78:117:src/core/chat_orchestrator.py
        # Guardrails: if no context or low confidence, return fallback without LLM call.
        no_context = not retrieval.chunks
        low_conf = retrieval_conf is not None and retrieval_conf < settings.retrieval_confidence_threshold
        if no_context or low_conf:
            assistant_text = FALLBACK_MESSAGE
            handoff = True  # treat as handoff hint when KB lacks answer
            reason = "no_context" if no_context else "low_confidence"
            meta = {
                "guardrail": reason,
                "retrieval": {"confidence": retrieval_conf, "top_k": settings.retrieval_top_k, "chunks": []},
                "intent": {"intent": intent.intent, "confidence": intent.confidence},
            }
            assistant_msg = self._conv.add_message(
                db,
                session,
                role=MessageRole.assistant,
                content=assistant_text,
                intent=intent.intent,
                confidence=retrieval_conf,
                retrieved_context=[],
                metadata=meta,
            )
            db.add(
                Feedback(
                    message_id=assistant_msg.id,
                    sentiment_score=sentiment.score,
                    sentiment_label=sentiment.label,
                    retrieval_top_k=settings.retrieval_top_k,
                    notes="guardrail_fallback",
                )
            )
            db.commit()
            return ChatResult(
                response=assistant_text,
                session_id=session.session_id,
                intent=intent.intent,
                confidence=retrieval_conf,
                handoff_trigger=handoff,
                metadata=meta,
            )

        if decision.should_handoff:
```

---

**Figure 5.4 — Ingestion pipeline: CSV FAQs → chunks → embeddings → batched Pinecone upsert**

*Screenshot target:* `src/ingestion/pipeline.py`, class **`IngestionPipeline`**.

```17:47:src/ingestion/pipeline.py
class IngestionPipeline:
    def __init__(self) -> None:
        self._embedder = OpenAIEmbedder()
        self._store = PineconeVectorStore()

    def ingest_csv(self, path: str, *, chunk_size: int = 800, chunk_overlap: int = 120) -> IngestionStats:
        faqs = load_faq_csv(path)
        all_chunks: list[Chunk] = []
        for item in faqs:
            all_chunks.extend(chunk_text(item.as_text(), source_id=f"faq:{item.source_id}", chunk_size=chunk_size, chunk_overlap=chunk_overlap))
        self._upsert(all_chunks)
        return IngestionStats(sources=len(faqs), chunks=len(all_chunks))

    def ingest_pdf(self, path: str, *, chunk_size: int = 1000, chunk_overlap: int = 200) -> IngestionStats:
        pages = load_pdf(path)
        all_chunks: list[Chunk] = []
        for p in pages:
            source_id = f"pdf:{path}#p{p.page_number}"
            all_chunks.extend(chunk_text(p.text, source_id=source_id, chunk_size=chunk_size, chunk_overlap=chunk_overlap))
        self._upsert(all_chunks)
        return IngestionStats(sources=len(pages), chunks=len(all_chunks))

    def _upsert(self, chunks: list[Chunk]) -> None:
        vectors: list[tuple[str, list[float], dict]] = []
        for c in chunks:
            emb = self._embedder.embed(c.text)
            vectors.append((c.chunk_id, emb, c.metadata))
        # simple batch upsert
        batch_size = 50
        for i in range(0, len(vectors), batch_size):
            self._store.upsert(vectors[i : i + batch_size])
```

---

**Figure 5.5 — Chunking: RecursiveCharacterTextSplitter when available; deterministic fallback splitter**

*Screenshot target:* `src/ingestion/chunking.py`.

```13:53:src/ingestion/chunking.py
def _fallback_chunk_strings(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Character-window split without LangChain (e.g. Windows DLL issues with optional native deps)."""
    t = text.strip()
    if not t:
        return []
    if len(t) <= chunk_size:
        return [t]
    parts: list[str] = []
    start = 0
    step = max(1, chunk_size - chunk_overlap)
    while start < len(t):
        end = min(start + chunk_size, len(t))
        parts.append(t[start:end])
        if end >= len(t):
            break
        start += step
    return parts


def chunk_text(text: str, *, source_id: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[Chunk]:
    texts: list[str]
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = splitter.create_documents([text])
        texts = [d.page_content for d in docs]
    except Exception:  # pragma: no cover - optional chain; fallback always available
        texts = _fallback_chunk_strings(text, chunk_size, chunk_overlap)

    out: list[Chunk] = []
    for idx, page_content in enumerate(texts):
        cid = f"{source_id}::chunk_{idx}"
        out.append(
            Chunk(
                chunk_id=cid,
                text=page_content,
                metadata={"source_id": source_id, "chunk_index": idx, "chunk_size": chunk_size, "text": page_content},
            )
        )
    return out
```

---

**Figure 5.6 — Next.js typed client: base URL resolution and REST helpers**

*Screenshot target:* `frontend/lib/api.ts`.

```31:64:frontend/lib/api.ts
function apiBase(): string {
  return (process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000").replace(/\/+$/, "");
}

async function jsonFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${apiBase()}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    cache: "no-store",
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(text || `Request failed: ${res.status}`);
  }
  return (await res.json()) as T;
}

export const api = {
  health: () => jsonFetch<HealthResponse>("/health"),

  createSession: (userId: string) =>
    jsonFetch<SessionCreateResponse>("/session", {
      method: "POST",
      body: JSON.stringify({ user_id: userId }),
    }),

  chat: (payload: { user_id: string; session_id?: string; query: string }) =>
    jsonFetch<ChatResponse>("/chat", { method: "POST", body: JSON.stringify(payload) }),

  history: (sessionId: string) =>
    jsonFetch<HistoryResponse>(`/history?session_id=${encodeURIComponent(sessionId)}`),

  analytics: () => jsonFetch<AnalyticsResponse>("/analytics"),
};
```

---

**Figure 5.7 — Chat page: ensure session then call `POST /chat`**

*Screenshot target:* `frontend/app/page.tsx`, **`ensureSession`** and **`send`**.

```69:115:frontend/app/page.tsx
  async function ensureSession() {
    if (sessionId) return sessionId;
    const s = await api.createSession(userId);
    setSessionId(s.session_id);
    return s.session_id;
  }

  async function send() {
    const q = input.trim();
    if (!q) return;
    setInput("");
    setLoading(true);

    const msgId = crypto.randomUUID();
    setMessages((prev) => [
      ...prev,
      { id: msgId, role: "user", content: q, timestamp: nowIso() },
    ]);

    try {
      const sid = await ensureSession();
      const res = await api.chat({ user_id: userId, session_id: sid, query: q });
      setSessionId(res.session_id);
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: res.response,
          timestamp: nowIso(),
          details: res,
        },
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "system",
          content: e instanceof Error ? e.message : "Request failed",
          timestamp: nowIso(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  }
```

---

### 5.12 Runtime and browser screenshots (figures 5.8–5.14)

These figures are **not** reproduced as source code in Word; capture them from a running demo and insert images with the same captions.

| Fig. | What to capture | How to reproduce |
|------|----------------|------------------|
| **5.8** | Swagger **OpenAPI** UI listing operations | Browse `http://localhost:8000/docs` |
| **5.9** | **Try it out**: `POST /chat` — request + **200** JSON (`response`, `metadata`, `handoff_trigger`) | After `POST /session`, run FAQ-aligned query |
| **5.10** | **`POST /chat`** or UI showing **fallback** text (`metadata.guardrail`) | Ask an out-of-domain question or empty index |
| **5.11** | Terminal after **`python -m src.ingestion.ingest ...`** | Show `sources=` and `chunks=` line |
| **5.12** | Terminal **`uvicorn src.main:app --reload`** or Docker **app** logs listening on **8000** | Startup banner without leaked keys |
| **5.13** | Browser chat: header, health strip, transcript with user + assistant | `http://localhost:3000` |
| **5.14** | **Analytics** view with KPIs (`total_sessions`, `total_messages`) | Navigate to `/analytics` in the frontend |

**Quality checklist:** JPEG/PNG readable when printed; no blurred 4K downscale; caption every figure (**Figure X.Y — …**); do **not** include API keys in any screenshot—redact `.env`, Authorization headers, and terminal env dumps.

Optional **Docker** evidence (not numbered separately unless needed): **`docker compose ps`** or Compose Desktop showing `frontend`, `app`, `postgres` healthy.

---

# Chapter 6 — Testing

This chapter documents how the EmpowerTech RAG chatbot was validated at multiple levels—from automated checks that run in CI to structured manual and system-level scenarios. The guiding principle is **risk-based testing**: areas with the highest impact on user trust (correct retrieval, safe answers when evidence is weak, and durable session history) receive the densest test coverage in the tables below. Academic project constraints mean **formal coverage percentages** are not generated by a commercial coverage tool across the whole codebase; instead, the project combines a **repeatable smoke test**, **documented manual API checks**, and **pilot RAG evaluation** (Chapter 7). Before final submission, each row’s **Actual result** and **Status** columns should be filled from a fresh test pass and initialed or dated in the PDF version of the report.

### 6.1 Testing Objectives and Scope

The primary objectives of testing for this system are: (1) to verify that REST contracts documented in Chapter 4 behave as implemented; (2) to confirm that conversational data is **persisted consistently** in PostgreSQL (users, sessions, messages, optional feedback fields); (3) to exercise **retrieval and guardrail** paths so that empty or low-confidence context does not silently produce ungrounded fluent answers; (4) to ensure the **Next.js** client can communicate with the API when CORS and base URL are configured; and (5) to keep a **regression log** of defects discovered during integration (Docker, ORM, embeddings, and frontend build). Out of scope for automated CI are **billable calls** to OpenAI and Pinecone—those are exercised in **manual / system** passes with keys present, or via the **offline evaluation script** that records batch metrics.

### 6.2 Levels and Types of Testing

**Unit testing** is minimal in the repository: the critical business logic (orchestration, retrieval thresholds) is deterministic only when external services are mocked; the team prioritized a single **integration smoke test** under `tests/` to avoid flakiness from network calls. **Integration testing** focuses on the FastAPI application bound to an **in-memory SQLite** database via environment override, verifying that routing, dependency injection for `get_db`, and the health endpoint respond without live Postgres. **System testing** is performed manually or via Docker Compose: Postgres, API, optional Pinecone/OpenAI, and the frontend are run together; testers use Swagger UI, curl, or the browser. **User acceptance–style checks** are reflected in the frontend table (navigation, session continuity, analytics visibility). **Data pipeline testing** covers CSV ingestion and Pinecone upsert semantics (dimension match, namespace). **Security-related checks** in this chapter are limited to **negative API cases** and configuration hygiene (no secrets in repo); penetration testing is not claimed.

### 6.3 Test Environment and Entry Criteria

**Automated run:** Python 3.11 on **GitHub Actions** (`ubuntu-latest`) per workflow file; dependencies from `requirements.txt`. **Local developer run:** Python virtual environment on Windows or Linux; `DATABASE_URL` pointed at SQLite for smoke test or Postgres for full stack. **Manual system run:** `.env` supplies `OPENAI_API_KEY`, `PINECONE_*`, and `DATABASE_URL` (e.g. Docker hostname `postgres`). **Entry criteria** for a “full pass” manual cycle: database migrations/init completed (`init_db` / `seed_db` as applicable), knowledge base ingested for RAG checks, API listening on port 8000, frontend on 3000 if UI tests are executed. **Exit criteria** for thesis demo: all applicable rows in Tables 6.1–6.4 marked Pass with Actual values recorded, smoke test green on CI, and no open **critical** defects affecting data loss or silent wrong answers without guardrail.

### 6.4 Traceability to Functional Requirements

Functional requirements **FR1–FR7** from Chapter 3 map to the test case prefixes below: **S** = session, **C** = chat, **H** = history, **A** = analytics, **G** = guardrail/RAG, **I** = ingestion, **U** = UI, **E** = error/negative. This mapping supports audit-style report review.

| FR ID | Requirement summary | Primary test IDs (Tables 6.1–6.4) |
|-------|---------------------|-------------------------------------|
| FR1 | Create session / user | TC-S01, TC-S02, TC-E04, TC-U01 |
| FR2 | Chat with RAG | TC-C01–TC-C04, TC-G01–TC-G05, TC-E01–TC-E03 |
| FR3 | Session history | TC-H01–TC-H03 |
| FR4 | Analytics summary | TC-A01–TC-A02 |
| FR5 | Ingest knowledge base | TC-I01–TC-I04 |
| FR6 | Health / ops | TC-HL01–TC-HL03 |
| FR7 | Web UI | TC-U01–TC-U05 |

### 6.5 Automated Smoke Test and Fixtures

`tests/test_smoke.py` programmatically **reloads** `src.config.settings` and `src.models.db` after setting `DATABASE_URL=sqlite+pysqlite:///:memory:` and **unsetting** cloud API keys. It creates ORM metadata, instantiates `TestClient`, and asserts `GET /health` returns HTTP **200** with top-level keys **`status`** and **`dependencies`**. This proves the application module graph imports correctly and the health route executes a database round-trip when SQLite is available. Extending smoke tests to `POST /chat` would either require **mocks** for `ChatOrchestrator` or live keys; the project intentionally keeps CI **free of external billable calls**.

### 6.6 Continuous Integration Workflow

The workflow **`.github/workflows/tests.yml`** triggers on **push** and **pull_request** to the default branch logic. It checks out the repository, configures **Python 3.11**, upgrades `pip`, installs `requirements.txt`, and runs **`pytest -q`**. A passing run provides evidence of **buildability** and **non-regression** on the smoke test. The table below summarizes CI intent; **screenshot** attachment in the PDF appendix is recommended.

**Table 6.5 — Automation, CI, and tooling**

| Step | Tool / action | Success criterion |
|------|----------------|-------------------|
| AW1 | Checkout repository | Latest commit available |
| AW2 | Python 3.11 setup | Interpreter available |
| AW3 | `pip install -r requirements.txt` | Exit code 0 |
| AW4 | `pytest -q` | All tests pass (currently 1 smoke test) |
| AW5 | Future: `ruff` / `mypy` (optional) | Not mandatory in current repo |

### 6.7 API Functional and Integration Test Cases

The following table is the **primary API regression checklist**. Preconditions **P0** = API up; **P1** = Postgres (or agreed DB) initialized; **P2** = valid OpenAI+Pinecone keys and ingested index for RAG rows. **Actual** and **Status** should be completed per submission.

**Table 6.1 — API functional and integration test cases**

| TC ID | Req | Precondition | Procedure (input) | Expected result | Actual | Status |
|-------|-----|--------------|-------------------|-----------------|--------|--------|
| TC-HL01 | FR6 | P0 | `GET /health` | HTTP 200; JSON includes `status`, `dependencies`; Postgres probe `ok` when DB reachable | | |
| TC-HL02 | FR6 | P0, keys unset (CI) | Same on SQLite-only smoke | HTTP 200; `dependencies.openai`/`pinecone` indicate configured or not | | |
| TC-HL03 | FR6 | P0 | OpenAPI | `GET /docs` returns Swagger UI | | |
| TC-S01 | FR1 | P0, P1 | `POST /session` body `{"user_id":"u_test_001"}` | HTTP 200; response contains non-empty `session_id` | | |
| TC-S02 | FR1 | P0, P1 | `POST /session` with optional `email` | Session created; user row consistent (manual DB inspect or repeat) | | |
| TC-S03 | FR1 | P0, P1 | Two consecutive `POST /session` same `user_id` | Two distinct `session_id` values returned | | |
| TC-C01 | FR2 | P0, P1, P2 | `POST /chat` with valid `user_id`, `session_id`, FAQ-like query (e.g. enrollment) | HTTP 200; `response` natural language; metadata includes intent; `handoff_trigger` boolean | | |
| TC-C02 | FR2 | P0, P1, P2 | Same session second `POST /chat` related follow-up | Session id stable; history considered (qualitative) | | |
| TC-C03 | FR2 | P0, P1 | `POST /chat` invalid `session_id` | New session behavior or 400 per implementation (record observed) | | |
| TC-C04 | FR2 | P0, P1, P2 | On-topic query with known FAQ | `retrieved_context` or metadata indicates chunks when inspection available | | |
| TC-H01 | FR3 | After TC-C01–C02 | `GET /history?session_id=<sid>` | HTTP 200; messages array includes user and assistant turns in order | | |
| TC-H02 | FR3 | P0, P1 | `GET /history?session_id=nonexistent` | HTTP **404** session not found | | |
| TC-H03 | FR3 | — | `GET /history` missing `session_id` | HTTP **422** validation error (FastAPI) | | |
| TC-A01 | FR4 | P0, P1, data present | `GET /analytics` | HTTP 200; non-negative session and message counts | | |
| TC-A02 | FR4 | Empty DB (optional) | `GET /analytics` | HTTP 200; zeros or consistent baseline | | |
| TC-E01 | — | P0, P1 | `POST /chat` empty `query` string | HTTP **422** or safe rejection | | |
| TC-E02 | — | P0, P1 | `POST /chat` missing `user_id` | HTTP **422** | | |
| TC-E03 | — | P0 | `POST /session` invalid JSON | HTTP **422** | | |
| TC-E04 | — | P0, P1 | `POST /chat` with typo field names | HTTP **422** (Pydantic) | | |
| TC-NF01 | NFR | P0 sustained | 20 sequential `/health` | All 200 within reasonable latency (record ms) | | |
| TC-NF02 | NFR | CORS configured | Browser preflight from `localhost:3000` | Allowed per `CORSMiddleware` settings | | |

### 6.8 Error Handling Validation and Boundary Tests

**Table 6.2 — Error handling validation and boundary tests**

| TC ID | Category | Procedure | Expected | Actual | Status |
|-------|----------|-----------|----------|--------|--------|
| TC-B01 | Boundary | Extremely long `query` (e.g. 8k chars) | 422 / 413 / truncation per config; no 500 | | |
| TC-B02 | Boundary | Unicode and punctuation in query | 200 acceptable path; persisted correctly | | |
| TC-B03 | Security | JWT not used | No auth endpoints to bypass (document N/A if applicable) | | |
| TC-B04 | Config | Wrong `DATABASE_URL` | `/health` shows postgres error string; status degraded | | |
| TC-B05 | Config | Missing Pinecone key at runtime | Retriever returns empty; guardrail/fallback path | | |
| TC-B06 | Config | Wrong Pinecone index dimension | Upsert/import fails fast (document ingestion error message) | | |
| TC-B07 | Concurrency | Two parallel `/chat` same session | Last-write wins acceptable; no DB crash | | |
| TC-B08 | Idempotency | Duplicate `POST /session` semantics | Distinct sessions (not idempotent by design)—document behavior | | |
| TC-B09 | Rate | Rapid `/chat` burst | Graceful degradation; note if no rate limit | | |
| TC-B10 | Log | Trigger controlled 400/404 | Structured log line / no secret leak | | |

### 6.9 RAG Retrieval Guardrails and Ingestion Tests

**Table 6.3 — RAG retrieval guardrails and ingestion tests**

| TC ID | Focus | Procedure | Expected | Actual | Status |
|-------|-------|-----------|----------|--------|--------|
| TC-G01 | Retrieval | Known FAQ query after ingest | Retrieved chunk text aligns with FAQ domain | | |
| TC-G02 | Guardrail | Nonsense or off-domain query | Fallback phrase or metadata `guardrail` | | |
| TC-G03 | Guardrail | Query with no index data (empty namespace) | No LLM hallucination bypass; fallback | | |
| TC-G04 | Threshold | Tune `RETRIEVAL_CONFIDENCE_THRESHOLD` low vs high | Observed flip between answer path and fallback | | |
| TC-G05 | Top-k | Compare `top_k` in retrieval (manual or eval script) | Consistent IDs in metadata / eval CSV | | |
| TC-I01 | Ingest | `python -m src.ingestion.ingest --source data/knowledge_base_faqs.csv --type csv` | Completes; chunk count printed | | |
| TC-I02 | Ingest | Re-run ingest idempotently | Upsert updates or duplicates per Pinecone policy (document) | | |
| TC-I03 | PDF | If PDF used: ingest `--type pdf` small file | Chunks nonzero; smoke query | | |
| TC-I04 | Embedding | Embedding model mismatch | Document 1536-d index for `text-embedding-3-small` | | |

### 6.10 Frontend and Manual End-to-End Tests

**Table 6.4 — Frontend and manual end-to-end tests**

| TC ID | Focus | Procedure | Expected | Actual | Status |
|-------|-------|-----------|----------|--------|--------|
| TC-U01 | Load | Open `http://localhost:3000` | Shell renders without console errors | | |
| TC-U02 | Session | Start chat flow (create session in UI) | Messages send; assistant reply visible | | |
| TC-U03 | History | Navigate to History page | Past messages or empty state coherent | | |
| TC-U04 | Analytics | Navigate to Analytics page | KPIs mirror API or placeholder copy | | |
| TC-U05 | API base | Wrong `NEXT_PUBLIC_API_BASE_URL` | User-visible error or empty state—document mitigation | | |
| TC-U06 | Docker | `docker compose up --build` | All services healthy after startup | | |
| TC-U07 | Responsive | Narrow viewport | Usable layout (qualitative screenshot) | | |
| TC-U08 | Refresh | Reload mid-session | Behavior per client storage—document | | |

### 6.11 Defect Log and Resolution History

Issues encountered during integration are summarized for examiner transparency. **Regression:** after each fix, relevant rows from Tables **6.1–6.3** should be re-executed.

| Issue | Symptom | Resolution |
|-------|---------|------------|
| ORM reserved name `metadata` | SQLAlchemy mapping conflict | ORM attribute `message_metadata` mapped to column `"metadata"` |
| Pinecone dimension mismatch | Upsert rejects vectors | Index dimension **1536** aligned with `text-embedding-3-small` |
| Container sentiment import | Import error for VADER | Direct `SentimentIntensityAnalyzer` import in `sentiment_analyzer.py` |
| Next.js Docker build | Remote font fetch failure | Removed blocking remote font dependency in layout/build |
| LangChain/`uuid_utils` on Windows | Ingest evaluation import failure | Character-window **fallback chunker** in `chunking.py` |
| Pinecone hostname in `.env` | API cannot reach index from laptop | Clarify Docker vs localhost hostnames in `.env.example` docs |

---

**Figure 6.1 (optional)** — Paste a screenshot of GitHub Actions **pytest** job green checkmark and Swagger `/docs` in the appendix for viva preparation.

---

# Chapter 7 — Results and Discussion

### 7.1 Functional Outcomes

The implemented system satisfies core academic demo goals: **ingestion → retrieval → grounded response** with **session persistence** and a **browser UI**. Analytics exposes aggregate session and message counts for inspection.

### 7.2 Qualitative Observations

- On-topic questions aligned with the **110-row** FAQ set yield coherent answers when retrieval hits the correct chunk.  
- Off-topic or unsupported queries trigger the **fallback** message—demonstrating conservative behavior suitable for institutional disclaimers.  
- **Handoff flags** support UX messaging (“speak with an advisor”)—exact product copy can be tuned without architecture changes.

### 7.3 Evaluation Scaffold and Pilot Quantitative Run

**Datasets and code locations**

- **`data/evaluation_queries.csv`** — labeled queries (id, query, intent) for batch and stratified analysis.  
- **`data/evaluation_gold.csv`** — same ten queries with **reference answers** drawn from the curated FAQ knowledge base, used to score system outputs in offline runs.  
- **`experiments/run_rag_evaluation.py`** — scripted batch: retrieve (Pinecone) → production guardrails → generate (when allowed) → score each run; writes results under **`experiments/results/`**.  
- **`experiments/README_EVALUATION.md`** — how to reproduce the run (`python experiments/run_rag_evaluation.py` from repository root, with `.env` keys set).  
- **`src/core/ragas_evaluator.py`** — integration hook for **RAGAS**; full RAGAS scores are **not** used in the pilot below on environments where the `ragas` stack fails to import (e.g. some Windows builds). RAGAS should be run under Linux/WSL2/Docker when required for formal faithfulness/relevancy reporting (Es *et al.*, 2023).

**Procedure (pilot)** A **paired design** compared **`top_k = 3`** vs **`top_k = 5`** on the same *N* = 10 gold queries. For each query and condition, the script recorded retrieval scores, whether the guardrail path fired, and **answer–reference embedding similarity** (cosine similarity between `text-embedding-3-small` vectors of the gold answer and the generated answer). It also recorded **reference–context token recall** (fraction of reference word tokens present in concatenated retrieved context). **Paired** inference used SciPy: **paired *t*-test** and **Wilcoxon signed-rank** on the 10 paired similarity values (5 vs 3).

**Table 7.1 — Pilot aggregate results** *(regenerate numbers after re-running the script; snapshot below from `experiments/results/rag_eval_statistics.json` at time of report update)*

| Quantity | Value |
|----------|--------|
| Paired queries *N* | 10 |
| Mean answer–reference embedding similarity (*top_k* = 3) | 0.9213 |
| Mean answer–reference embedding similarity (*top_k* = 5) | 0.8975 |
| Mean paired difference (5 − 3) | −0.0238 |
| Paired *t*-test *p*-value (two-sided) | 0.200 |
| Wilcoxon signed-rank *p*-value (two-sided) | 0.176 |

**Interpretation (pilot only)** With *N* = 10, no reliable difference was found between *top_k* = 3 and *top_k* = 5 on this **embedding-similarity proxy**; both *p*-values are well above conventional 0.05. This does **not** replace RAGAS faithfulness or human rubrics—it measures semantic closeness to a short gold answer.

**Artifacts to attach or cite** Per-row details: **`experiments/results/rag_eval_runs.csv`**. Machine-readable aggregates: **`experiments/results/rag_eval_statistics.json`**. Short narrative: **`experiments/results/RAG_EVAL_SUMMARY.md`**.

**Annotator studies (future)** Human ratings (e.g. usefulness, factual agreement) with inter-rater agreement (κ or Krippendorff’s α) are **not** part of this pilot; add a protocol and table when conducted.

### 7.4 Limitations

- **RAGAS** and multi-factor designs (e.g. chunk-size matrix with ANOVA) are **not** fully reported here; the pilot uses an **embedding-based** answer–reference metric. Faithfulness-to-context should be evaluated with RAGAS or human judgment when the tooling environment allows.  
- Sample size (*N* = 10) is small for generalization; expand `evaluation_gold.csv` and re-run for thesis-scale evidence.  
- Retrieval quality depends on **FAQ phrasing** and chunk boundaries.  
- API costs scale with traffic; rate limiting is not implemented.  

### 7.5 Comparison with Naive Baseline

Compared to **LLM-only** chat, the RAG design improves **traceability** (stored chunks) and **refusal behavior** when evidence is missing—appropriate for compliance-aware education support.

---

# Chapter 8 — Conclusion and Future Scope

### 8.1 Conclusion

The project delivered an **end-to-end RAG chatbot** with PostgreSQL session storage, Pinecone vector retrieval, OpenAI embeddings and chat completion, guardrails, intent/sentiment/handoff plumbing, a Next.js client, Docker Compose packaging, and automated smoke testing. Objectives related to **implementation and demonstration** are met; a **small pilot offline evaluation** (paired *top_k* comparison with statistical tests and exported CSV/JSON) is documented in §7.3. **Large-scale** studies (more queries, chunking matrix, full RAGAS, annotator panels) remain for extension.

### 8.2 Learning Outcomes

- Practical integration of LLM APIs with vector search.  
- Schema design for conversational audit and optional RAG quality fields.  
- Production-minded defaults: health checks, CORS, environment-based configuration.

### 8.3 Future Enhancements

- **Run RAGAS (or similar) systematically** (e.g. on Linux/WSL2) alongside the existing **`run_rag_evaluation.py`** outputs; expand **`evaluation_gold.csv`** beyond ten items.  
- **Add role-based admin** for KB editing and ingestion jobs.  
- **Hybrid retrieval** (keyword + dense) for acronym-heavy policies.  
- **Rate limiting** and **OAuth2** for public deployment.  
- **Mobile app** or LMS LTI integration.  
- **Multilingual** embeddings and answers for regional learners.

---

# Chapter 9 — References

*(APA 7th edition style; hanging indent in Word. 20+ sources for MSc — examples below; verify access dates for web docs at submission time.)*

Es, S., James, J., Şevgi Gönül, H., & Klabbers, J. H. (2023). RAGAS: Automated evaluation of retrieval augmented generation. *arXiv*. https://arxiv.org/abs/2309.15217  

Gao, Y., Xiong, Y., Gao, X., et al. (2023). Retrieval-augmented generation for large language models: A survey. *arXiv*. https://arxiv.org/abs/2312.10997  

Hutto, C., & Gilbert, E. (2014). VADER: A parsimonious rule-based model for sentiment analysis of social media text. *Proceedings of the International AAAI Conference on Web and Social Media*, 8(1), 216–225.  

Lewis, P., Perez, E., Piktus, A., et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. In *Advances in Neural Information Processing Systems*, 33.  

Fielding, R. T. (2000). *Architectural styles and the design of network-based software architectures* (Doctoral dissertation, University of California, Irvine).  

OpenAI. (n.d.). *OpenAI API reference: Embeddings*. OpenAI. Retrieved from https://platform.openai.com/docs/guides/embeddings  

OpenAI. (n.d.). *OpenAI API reference: Chat completions*. OpenAI. Retrieved from https://platform.openai.com/docs/guides/text-generation  

Pinecone Systems. (n.d.). *Pinecone documentation*. Retrieved from https://docs.pinecone.io/  

FastAPI. (n.d.). *FastAPI documentation*. Retrieved from https://fastapi.tiangolo.com/  

SQLAlchemy. (n.d.). *SQLAlchemy documentation*. Retrieved from https://docs.sqlalchemy.org/  

PostgreSQL Global Development Group. (n.d.). *PostgreSQL documentation*. Retrieved from https://www.postgresql.org/docs/  

Docker Inc. (n.d.). *Docker documentation*. Retrieved from https://docs.docker.com/  

Vercel. (n.d.). *Next.js documentation*. Retrieved from https://nextjs.org/docs  

GitHub. (n.d.). *GitHub Actions documentation*. Retrieved from https://docs.github.com/en/actions  

Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.  

Sommerville, I. (2016). *Software engineering* (10th ed.). Pearson.  

Pressman, R. S., & Maxim, B. R. (2020). *Software engineering: A practitioner’s approach* (9th ed.). McGraw-Hill.  

Richardson, L., & Ruby, S. (2013). *RESTful web APIs*. O’Reilly Media.  

Bird, S., Klein, E., & Loper, E. (2009). *Natural language processing with Python*. O’Reilly Media.  

Jurafsky, D., & Martin, J. H. (2024). *Speech and language processing* (3rd ed. draft). https://web.stanford.edu/~jurafsky/slp3/  

Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to information retrieval*. Cambridge University Press.  

Baeza-Yates, R., & Ribeiro-Neto, B. (2011). *Modern information retrieval* (2nd ed.). Addison-Wesley.  

ISO/IEC/IEEE 24765:2017. (2017). *Systems and software engineering—Vocabulary*.  

NIST. (n.d.). *Software assurance*. National Institute of Standards and Technology. Retrieved from https://csrc.nist.gov/projects/ssdf  

---

# Chapter 10 — Appendices

### Appendix A — Installation and Runbook (summary)

1. `python -m venv .venv` and activate.  
2. `pip install -r requirements.txt`  
3. Copy `.env.example` to `.env`; set `OPENAI_API_KEY`, `PINECONE_API_KEY`, `PINECONE_INDEX_NAME` (1536-d index), `DATABASE_URL`.  
4. Start PostgreSQL (`docker compose up -d postgres` or local).  
5. `python -m src.models.init_db` and `python -m src.models.seed_db`.  
6. `python -m src.ingestion.ingest --source data/knowledge_base_faqs.csv --type csv`.  
7. `uvicorn src.main:app --reload` — Open `http://127.0.0.1:8000/docs`.  
8. Frontend: `cd frontend`, `npm install`, `npm run dev` — configure `.env.local` from `frontend/.env.local.example`.  
9. Full stack: `docker compose up --build`.

### Appendix B — Environment Variables (non-secret names)

`OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_EMBEDDING_MODEL`, `PINECONE_API_KEY`, `PINECONE_INDEX_NAME`, `PINECONE_NAMESPACE`, `DATABASE_URL`, `RETRIEVAL_TOP_K`, `RETRIEVAL_CONFIDENCE_THRESHOLD`, `CHAT_HISTORY_LIMIT`, `LOG_LEVEL`.

### Appendix C — Source Code Location

Full source resides in the project repository under `src/` and `frontend/` as implemented. For submission, zip the repository or provide a GitHub link per institute rules **without** embedding API keys.

### Appendix D — User Guide (short)

1. Open the web UI.  
2. Start a session (UI flow).  
3. Ask FAQs about enrollment, refunds, or technical access.  
4. Use History to review turns; Analytics for aggregate stats.  

### Appendix E — Evaluation Query Set and Gold Labels

- `data/evaluation_queries.csv` — id, query, intent (batch driver).  
- `data/evaluation_gold.csv` — id, query, intent, **reference_answer** (offline scoring).  
- Latest pilot exports: `experiments/results/rag_eval_runs.csv`, `rag_eval_statistics.json`, `RAG_EVAL_SUMMARY.md`.

---

**End of draft report body**   *(Expand each chapter in Word to meet program page targets; insert figures from rendered Mermaid or redrafted diagrams; add institute cover and signed certificate pages.)*
