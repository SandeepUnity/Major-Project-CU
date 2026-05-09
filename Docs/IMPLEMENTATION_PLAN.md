# Implementation Plan: EmpowerTech RAG Chatbot

## Executive Summary

Build a **Data Science-driven RAG chatbot** for EmpowerTech Solutions with rigorous statistical evaluation. The system combines retrieval-augmented generation with comprehensive analytics—RAGAS metrics, sentiment analysis, and chunking optimization studies—to demonstrate research-grade data science capabilities.

**Technical Stack**: Python 3.10+, FastAPI, LangChain, Pinecone, OpenAI GPT-4o, PostgreSQL

**Data Science Focus**: RAGAS evaluation metrics, Performance Matrix (chunking analysis), sentiment analysis, and thesis-ready reporting

**Timeline**: 3 phased approach:
- Phase 1: Core RAG system with proper relational schema
- Phase 2: ANALYTICS AS PRIMARY FOCUS — RAGAS metrics, Performance Matrix, statistical analysis
- Phase 3: Deployment infrastructure (deferred)

**Key Thesis Deliverable**: Chapter 7 will present Performance Matrix showing chunking size optimization against Faithfulness & Answer Relevancy scores

---

## Report Deliverables & Compliance (MSc DS)

This implementation plan is designed to map cleanly to the official project report template and writing guidelines.

- **Final Report**: PDF (60–100 pages target; 18,000–30,000 words excluding references/appendices)
- **Final Presentation**: PPT + exported PDF
- **Work Link**: GitHub repository and a reproducible demo (local via Docker Compose or hosted link)

**Mandatory preliminary pages (report front matter)**:
- Cover page
- Bonafide certificate (Institute + Guide) and Qollabb certificate copy (as applicable)
- Declaration by student
- Acknowledgement
- Abstract (150–250 words; write last)
- Table of contents
- List of figures
- List of tables
- List of abbreviations

**Report expectation**: technical, structured, implementation-focused. Avoid dumping full code in chapters—place full code in appendices and include only key excerpts in Chapter 5.

---

## Chapter 4 (Design): Relational Database Schema (PostgreSQL)

This section defines the core relational schema that underpins the chatbot system. The schema is designed to support both operational functionality and comprehensive data science analytics.

### Schema Design Principles
1. **Audit Trail**: Capture all interactions for analysis and debugging
2. **Temporal Data**: Timestamps on all records for trend analysis
3. **Normalization**: Avoid redundancy, support efficient queries
4. **Analytics-Ready**: Structure supports RAGAS evaluation, sentiment tracking, and performance analysis

### Tables

#### 1. Users Table
**Purpose**: Minimal user identity and personalization metadata (privacy-first)

| Column Name | Data Type | Constraints | Purpose |
|---|---|---|---|
| `id` | SERIAL PRIMARY KEY | NOT NULL | Auto-increment unique ID |
| `user_id` | VARCHAR(255) | UNIQUE, NOT NULL | External user identifier |
| `email` | VARCHAR(255) | UNIQUE, NULL | Optional contact email (avoid storing unless required) |
| `enrolled_courses` | JSONB | | List of enrolled course IDs (JSON array) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation time |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last profile update |

**Indexes**: `idx_user_id`, `idx_email`

---

#### 2. ChatSessions Table
**Purpose**: Session persistence and conversation grouping

| Column Name | Data Type | Constraints | Purpose |
|---|---|---|---|
| `id` | SERIAL PRIMARY KEY | NOT NULL | Auto-increment unique ID |
| `session_id` | VARCHAR(255) | UNIQUE, NOT NULL | Unique session identifier (UUID) |
| `user_id` | INTEGER | FOREIGN KEY (Users.id), NOT NULL | Reference to user |
| `start_time` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Session creation timestamp |
| `end_time` | TIMESTAMP | | Session end time (NULL if active) |
| `message_count` | INTEGER | DEFAULT 0 | Total messages in session |
| `avg_sentiment` | FLOAT | | Average sentiment score for session |
| `handoff_triggered` | BOOLEAN | DEFAULT FALSE | Was session escalated to human? |
| `handoff_reason` | TEXT | | Reason for escalation |

**Indexes**: `idx_session_id`, `idx_user_id`, `idx_start_time`

---

#### 3. ChatMessages Table
**Purpose**: Audit trail, memory persistence, and interaction logging

| Column Name | Data Type | Constraints | Purpose |
|---|---|---|---|
| `id` | SERIAL PRIMARY KEY | NOT NULL | Auto-increment unique ID |
| `message_id` | VARCHAR(255) | UNIQUE, NOT NULL | Unique message identifier |
| `session_id` | INTEGER | FOREIGN KEY (ChatSessions.id), NOT NULL | Reference to session |
| `role` | ENUM('user', 'assistant', 'system') | NOT NULL | Message sender type (standardized) |
| `content` | TEXT | NOT NULL | Message text |
| `tokens_used` | INTEGER | | Token count for LLM calls |
| `intent` | VARCHAR(100) | | Classified intent (Transactional/Informational/General) |
| `confidence` | FLOAT | | Intent classification confidence |
| `timestamp` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Message timestamp |
| `retrieved_context` | JSONB | | Retrieved chunks from vector DB (for evaluation) |
| `metadata` | JSONB | | Additional metadata (source, model, etc.) |

**Indexes**: `idx_session_id`, `idx_role`, `idx_timestamp`, `idx_message_id`

---

#### 4. Feedback Table
**Purpose**: Data Science Analytics — Sentiment, Evaluation Metrics, User Ratings

| Column Name | Data Type | Constraints | Purpose |
|---|---|---|---|
| `id` | SERIAL PRIMARY KEY | NOT NULL | Auto-increment unique ID |
| `message_id` | INTEGER | FOREIGN KEY (ChatMessages.id), NOT NULL | Reference to bot response |
| `sentiment_score` | FLOAT | RANGE [-1, 1] | User query sentiment (-1=very negative, +1=very positive) |
| `sentiment_label` | ENUM('negative', 'neutral', 'positive') | | Categorical sentiment |
| `user_rating` | INTEGER | RANGE [1, 5] | User satisfaction rating (1-5 stars) |
| `ragas_faithfulness` | FLOAT | RANGE [0, 1] | Is response grounded in context? |
| `ragas_answer_relevancy` | FLOAT | RANGE [0, 1] | Does response address query? |
| `ragas_context_recall` | FLOAT | RANGE [0, 1] | Is relevant context retrieved? |
| `ragas_average` | FLOAT | RANGE [0, 1] | Average of all RAGAS scores |
| `chunking_size_used` | INTEGER | | Chunk size used for this query (256/512/1024/2048) |
| `retrieval_top_k` | INTEGER | | Number of chunks retrieved (k value) |
| `timestamp` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Evaluation timestamp |
| `notes` | TEXT | | Manual notes or observed issues |

**Indexes**: `idx_message_id`, `idx_timestamp`, `idx_chunking_size_used`, `idx_ragas_average`

---

### Database Relationships

```
Users (1) ──→ (Many) ChatSessions
ChatSessions (1) ──→ (Many) ChatMessages
ChatMessages (1) ──→ (One) Feedback
```

### SQLAlchemy ORM Models (Structure)

The schema maps to SQLAlchemy models:
- `User` model (file: `src/models/database.py`)
- `ChatSession` model (file: `src/models/database.py`)
- `ChatMessage` model (file: `src/models/database.py`)
- `Feedback` model (file: `src/models/database.py`)

### Traceability (anti-hallucination audit)

To support the “answer only from knowledge base” constraint, each assistant response must be traceable:
- Store retrieved chunks + scores in `ChatMessages.retrieved_context` (already planned).
- Store minimal `source_ids` (FAQ id / filename / page) and retrieval config (top_k, chunk_size, index/namespace) in `ChatMessages.metadata`.
- Optionally return lightweight citations in API responses (useful for screenshots in the report).

### Key Capabilities Enabled by Schema

1. **Multi-turn Conversations**: ChatMessages table enables retrieving full conversation history
2. **Sentiment Tracking**: Track user satisfaction trends across sessions
3. **RAGAS Analytics**: Feedback table stores all evaluation metrics for analysis
4. **Chunking Optimization Studies**: Compare different chunk sizes against RAGAS scores
5. **Session Management**: Understand session duration, message patterns, escalation triggers
6. **Audit Trail**: Complete record of all interactions for compliance and debugging

---

This phase establishes the foundational chatbot capabilities: retrieval, conversation management, intent classification, and API endpoints.

### 1.1 Project Setup & Dependency Management

**Objective**: Initialize Python project structure and install core dependencies.

**Tasks**:
1. Create project directory structure:
   ```
   f:\Major Project/
   ├── src/
   │   ├── __init__.py
   │   ├── main.py
   │   ├── api/
   │   ├── core/
   │   ├── models/
   │   ├── ingestion/
   │   ├── config/
   │   └── utils/
   ├── tests/
   ├── data/
   ├── requirements.txt
   ├── .env.example
   ├── README.md
   └── RESOURCES/
       └── PROJECT_SPEC.md (existing)
   ```

2. Create `requirements.txt` with dependencies:
   ```
   # Web Framework
   fastapi==0.104.1
   uvicorn[standard]==0.24.0
   python-multipart==0.0.6

   # LLM & RAG
   langchain==0.1.0
   langchain-openai==0.0.5
   langchain-community==0.0.10

   # Vector Database
   pinecone-client==3.0.0

   # LLM & Embeddings
   openai==1.3.0

   # Database ORM
   sqlalchemy==2.0.23
   psycopg2-binary==2.9.9

   # Configuration & Validation
   pydantic==2.5.0
   python-dotenv==1.0.0

   # Sentiment & Evaluation
   transformers==4.34.0
   torch==2.1.0
   ragas==0.1.0
   trulens-eval==0.25.0

   # Testing
   pytest==7.4.3
   pytest-asyncio==0.21.1
   pytest-cov==4.1.0
   httpx==0.25.2

   # Utilities
   pydantic-settings==2.1.0
   ```

3. Create `.env.example` with required environment variables:
   ```
   # OpenAI Configuration
   OPENAI_API_KEY=sk-xxxx
   OPENAI_MODEL=gpt-4o
   OPENAI_EMBEDDING_MODEL=text-embedding-3-small

   # Pinecone Configuration
   PINECONE_API_KEY=xxxx
   PINECONE_ENVIRONMENT=production
   PINECONE_INDEX_NAME=empowertech-rag

   # PostgreSQL Configuration
   DATABASE_URL=postgresql://user:password@localhost:5432/empowertech_chatbot

   # Application Configuration
   DEBUG=False
   LOG_LEVEL=INFO
   CHAT_HISTORY_LIMIT=10
   RETRIEVAL_TOP_K=5
   CONFIDENCE_THRESHOLD=0.3
   ```

4. Initialize git repository and create `.gitignore`
5. Create Python virtual environment (venv or conda)
6. Install all dependencies: `pip install -r requirements.txt`

**Success Criteria**:
- All Python packages imported successfully
- Project structure matches specification
- `.env` template created with all required keys

---

### 1.2 Database Schema & Setup

**Objective**: Initialize PostgreSQL with relational schema (Chapter 4) supporting analytics and audit trails.

**Tasks**:

1. Create `src/models/database.py` with SQLAlchemy ORM models (matching Chapter 4 schema):
   ```python
   class User(Base):
       __tablename__ = "users"
       id: Column(Integer, primary_key=True)
       user_id: Column(String(255), unique=True, nullable=False)
       email: Column(String(255), unique=True, nullable=False)
       enrolled_courses: Column(JSON, nullable=True)
       created_at: Column(DateTime, default=datetime.utcnow)
       updated_at: Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

   class ChatSession(Base):
       __tablename__ = "chat_sessions"
       id: Column(Integer, primary_key=True)
       session_id: Column(String(255), unique=True, nullable=False)
       user_id: Column(Integer, ForeignKey("users.id"), nullable=False)
       start_time: Column(DateTime, default=datetime.utcnow)
       end_time: Column(DateTime, nullable=True)
       message_count: Column(Integer, default=0)
       avg_sentiment: Column(Float, nullable=True)
       handoff_triggered: Column(Boolean, default=False)
       handoff_reason: Column(Text, nullable=True)

   class ChatMessage(Base):
       __tablename__ = "chat_messages"
       id: Column(Integer, primary_key=True)
       message_id: Column(String(255), unique=True, nullable=False)
       session_id: Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
       role: Column(Enum('user', 'bot', 'system'), nullable=False)
       content: Column(Text, nullable=False)
       tokens_used: Column(Integer, nullable=True)
       intent: Column(String(100), nullable=True)
       confidence: Column(Float, nullable=True)
       timestamp: Column(DateTime, default=datetime.utcnow)
       retrieved_context: Column(JSON, nullable=True)
       metadata: Column(JSON, nullable=True)

   class Feedback(Base):
       __tablename__ = "feedback"
       id: Column(Integer, primary_key=True)
       message_id: Column(Integer, ForeignKey("chat_messages.id"), nullable=False)
       sentiment_score: Column(Float, nullable=True)
       sentiment_label: Column(Enum('negative', 'neutral', 'positive'), nullable=True)
       user_rating: Column(Integer, nullable=True)
       ragas_faithfulness: Column(Float, nullable=True)
       ragas_answer_relevancy: Column(Float, nullable=True)
       ragas_context_recall: Column(Float, nullable=True)
       ragas_average: Column(Float, nullable=True)
       chunking_size_used: Column(Integer, nullable=True)
       retrieval_top_k: Column(Integer, nullable=True)
       timestamp: Column(DateTime, default=datetime.utcnow)
       notes: Column(Text, nullable=True)
   ```

2. Create database initialization script `src/models/init_db.py`:
   - Create all tables from SQLAlchemy models using `Base.metadata.create_all()`
   - Set up indexes on frequently queried columns (session_id, user_id, timestamp, chunking_size_used, ragas_average)
   - Verify schema creation

3. Create `src/config/settings.py` with Pydantic Settings for environment management:
   - Load `.env` file
   - Validate required environment variables
   - Provide database URL, API keys, and model configuration

4. Set up PostgreSQL locally:
   - Install PostgreSQL (or use Docker/local service)
   - Create database `empowertech_chatbot`
   - Run initialization script to create schema
   - Verify tables created: `\dt` in psql

5. Create seed script `src/models/seed_db.py` for test data:
   - Insert 5 sample users with course enrollments
   - Create 10 sample chat sessions
   - Create 50 sample messages across sessions
   - Create sample feedback with RAGAS scores for testing

6. Data Science Consideration:
   - Ensure Feedback table is properly indexed for RAGAS metric queries
   - Design supports efficient aggregation: `SELECT chunking_size_used, AVG(ragas_faithfulness), AVG(ragas_answer_relevancy) GROUP BY chunking_size_used`

**Success Criteria**:
- PostgreSQL database `empowertech_chatbot` created and accessible
- All ORM models defined with proper relationships and constraints
- Schema matches Chapter 4 specification
- All tables created with correct data types and indexes
- Sample data seeded (5 users, 10 sessions, 50 messages, 50+ feedback records)
- Queries verified: Can retrieve session history, aggregate RAGAS scores by chunking size

---

### 1.3 Ingestion Pipeline

**Objective**: Build system to parse documents and ingest into Pinecone vector database.

**Tasks**:

1. Create `src/ingestion/pdf_parser.py`:
   - Use `PyPDF2` or `pdfplumber` for PDF text extraction
   - Implement text cleaning and normalization
   - Extract metadata (source filename, page number)

2. Create `src/ingestion/csv_parser.py`:
   - Parse FAQ CSV files (ID, Question, Answer format)
   - Support different CSV structures
   - Extract and validate data

3. Create `src/ingestion/chunking.py`:
   - Implement text chunking using LangChain `RecursiveCharacterTextSplitter`
   - Configure chunk size (1000 tokens) and overlap (200 tokens)
   - Preserve source metadata for each chunk

4. Create `src/ingestion/pipeline.py`:
   - Implement `IngestionPipeline` class:
     - Load documents (PDF or CSV)
     - Chunk text
     - Generate embeddings via OpenAI `text-embedding-3-small`
     - Upsert to Pinecone with metadata
   - Support batch processing
   - Error handling and retry logic

5. Create `src/ingestion/ingest.py` CLI script:
   - Command-line interface for running ingestion
   - Arguments: `--source` (file path), `--type` (pdf/csv), `--index-name` (Pinecone index)
   - Example: `python -m src.ingestion.ingest --source data/faqs.csv --type csv --index-name empowertech-rag`

6. Create sample knowledge base in `data/` directory:
   - `data/sample_faqs.csv`: 20-30 education FAQ QA pairs
     - Format: question_id, question, answer, category, tags
     - Example: "1,How do I enroll in a course?,Visit the enrollment page...,enrollment,course"
   - `data/sample_document.pdf`: Mock course catalog (placeholder)

**Success Criteria**:
- Ingestion pipeline processes CSV and PDF files
- 20+ embeddings generated and stored in Pinecone
- Metadata preserved (source, chunk_id, etc.)
- CLI script works: `python -m src.ingestion.ingest --source data/sample_faqs.csv --type csv`
- Pinecone index verified with `pinecone.Index().describe_index_stats()`

---

### 1.4 Retrieval Engine

**Objective**: Implement hybrid semantic + keyword search for context retrieval.

**Tasks**:

1. Create `src/core/retriever.py`:
   - Implement `HybridRetriever` class with methods:
     - `semantic_search(query, top_k=5)`: Query Pinecone embeddings, return scored results
     - `keyword_search(query, top_k=5)`: BM25 or simple keyword matching fallback
     - `retrieve(query, method='hybrid', top_k=5)`: Combine semantic + keyword, deduplicate, rank
   - Integrate with LangChain `Retriever` base class for compatibility
   - Add scoring/ranking logic (normalize scores, combine weights)
   - Handle empty results gracefully

2. Implement LangChain `PineconeVectorStore` integration:
   - Use LangChain abstraction for Pinecone queries
   - Support both `Retriever` and `VectorStoreRetriever` interfaces
   - Configure query metadata filters (optional)

3. Add retrieval evaluation utilities:
   - Log retrieval accuracy (match between retrieved docs and user intent)
   - Track retrieval failures (no results, low confidence)

4. Create `src/core/context_formatter.py`:
   - Format retrieved chunks into readable context string
   - Add source attribution (FAQ ID, page number, etc.)
   - Truncate context to respect token limits

**Success Criteria**:
- Retriever returns top-5 relevant chunks for test queries
- Semantic search scores correlate with relevance
- Keyword fallback works when semantic search fails
- Integration with LangChain components

---

### 1.5 Intent Classification Module

**Objective**: Classify user queries into functional categories (Transactional/Informational/General).

**Tasks**:

1. Create `src/core/intent_classifier.py`:
   - Implement `IntentClassifier` class with `classify(query)` method
   - Return format: `{intent: str, confidence: float, reasoning: str}`

2. Classification categories (3 types):
   - **Transactional**: Enrollment, payment, account management, registration
   - **Informational**: Course details, how-to guides, prerequisites, schedules
   - **General**: Greetings, feedback, off-topic, unclear queries

3. Implementation approach (few-shot prompting with GPT-4o):
   - Use LangChain `PromptTemplate` to structure few-shot examples
   - Define 2-3 examples per category
   - Prompt GPT-4o to classify with confidence
   - Parse response to extract intent and confidence score

4. Add caching for identical queries:
   - Use simple dict cache (query → intent) to avoid redundant API calls

5. Create `src/core/intent_examples.py`:
   - Store 20+ labeled examples for testing
   - Use for evaluation and validation

**Success Criteria**:
- Intent classifier returns correct classification for 10 sample queries
- Confidence scores range [0, 1]
- Caching reduces redundant API calls
- LangChain prompt templates used for composition

---

### 1.6 Chat Memory & Conversation Management

**Objective**: Maintain session-based conversation history and multi-turn context.

**Tasks**:

1. Create `src/core/chat_memory.py`:
   - Implement `ChatMemory` class with methods:
     - `load_history(session_id)`: Retrieve last N messages from PostgreSQL
     - `add_message(session_id, role, content)`: Store message in DB
     - `get_token_count()`: Estimate tokens used (use LangChain `token_counter`)
     - `trim_history()`: Remove old messages if exceeds token limit

2. Create `src/core/conversation_manager.py`:
   - Implement `ConversationManager` class with methods:
     - `create_session(user_id)`: Create new ChatSession, return session_id
     - `get_or_create_session(user_id, session_id=None)`: Fetch existing or create new
     - `save_message(session_id, role, content, metadata)`: Persist message
     - `get_history(session_id, limit=10)`: Return formatted conversation history

3. Configuration for chat history:
   - Default window: last 10 messages
   - Token limit: 2000 tokens for context (configurable)
   - Trim strategy: Remove oldest messages first

4. Support for different roles:
   - `user`: User query
   - `assistant`: Bot response
   - `system`: System messages

**Success Criteria**:
- New sessions created successfully
- Messages persisted to PostgreSQL
- History retrieved correctly for multi-turn conversations
- Token counting prevents context overflow

---

### 1.7 Augmentation Layer (Prompt Engineering)

**Objective**: Construct prompts with system message, context, history, and guardrails.

**Tasks**:

1. Create `src/core/prompt_builder.py`:
   - Implement `PromptBuilder` class with `build_prompt()` method
   - Combine:
     - System message (role definition, behavior guidelines)
     - Retrieved context (formatted chunks from retriever)
     - Chat history (last N turns from conversation memory)
     - User query (current input)

2. Define system message template:
   ```
   You are a helpful educational assistant for EmpowerTech Solutions.
   You answer questions about courses, enrollment, technical issues, and policies.
   You MUST only use information provided in the knowledge base below.
   If you don't have relevant information, respond: "I'm sorry, I don't have that information. Would you like to speak with an advisor?"
   Be concise, friendly, and accurate.
   ```

3. Implement hallucination guardrail:
   - If retriever confidence < threshold (0.3) OR no context found:
     - Return hardcoded message: "I'm sorry, I don't have that information. Would you like to speak with an advisor?"
     - Skip LLM call entirely
   - Log guardrail triggers for monitoring

4. Create `src/core/prompt_templates.py`:
   - Define reusable prompt templates:
     - Chat template (with history)
     - Query-only template (no history)
     - Context-focused template
   - Support template variables: {context}, {history}, {query}, {intent}

5. Add token counting:
   - Validate prompt doesn't exceed model token limit (128k for GPT-4o)
   - Trim history if necessary

**Success Criteria**:
- Prompts constructed with all components
- Guardrails trigger correctly (low confidence → fallback message)
- Token counting prevents overflow
- System message enforced in all responses

---

### 1.8 Human Handoff Detection

**Objective**: Identify when user should be escalated to human support.

**Tasks**:

1. Create `src/core/handoff_detector.py`:
   - Implement `HandoffDetector` class with `should_handoff(query, response, metadata)` method
   - Return: `{should_handoff: bool, reason: str, severity: str}`

2. Handoff triggers:
   - **Frustration signals**: Keywords (not working, error, broken, angry, confused, frustrated)
   - **Sentiment-based**: Sentiment score < -0.5 (negative emotion)
   - **Retrieval failure**: No relevant context found (confidence < 0.3)
   - **Failed attempts**: User asked 3+ times about same topic unsuccessfully
   - **Complex queries**: Intent = "Transactional" AND sentiment negative
   - **Explicit requests**: "talk to agent", "speak with human"

3. Severity levels:
   - `low`: Single frustration signal
   - `medium`: Multiple signals or negative sentiment
   - `high`: Repeated failures or explicit request

4. Create `src/core/escalation_messages.py`:
   - Define escalation messages for each severity level
   - Example high: "I understand this is frustrating. Let me connect you with a specialist advisor who can help."

5. Integration with chat orchestrator:
   - Check handoff trigger before returning response
   - If triggered, return escalation message with handoff_flag=true

**Success Criteria**:
- Handoff detector identifies frustrated users
- Escalation messages appropriate to severity
- No false positives (normal queries don't trigger handoff)
- Seamless integration with chat endpoint

---

### 1.9 LLM Integration & Chat Orchestration

**Objective**: Orchestrate all components into cohesive chat workflow.

**Tasks**:

1. Create `src/core/chat_orchestrator.py`:
   - Implement `ChatOrchestrator` class with `chat(user_id, session_id, query)` method
   - Execution flow:
     1. Retrieve chat history (ConversationManager)
     2. Classify intent (IntentClassifier)
     3. Retrieve context (HybridRetriever)
     4. Check handoff trigger (HandoffDetector) — if true, return escalation message
     5. Build prompt (PromptBuilder) — include guardrail check
     6. Call LLM (OpenAI GPT-4o)
     7. Validate response (no hallucinations)
     8. Save message (ConversationManager)
     9. Return response with metadata

2. Create `src/core/llm_client.py`:
   - Implement `LLMClient` class wrapping OpenAI API
   - Methods:
     - `generate(prompt, max_tokens=500, temperature=0.7)`: Call GPT-4o
     - `handle_rate_limits()`: Exponential backoff for 429 errors
     - `validate_response(response)`: Check for hallucinations or errors

3. Use LangChain chains for composition:
   - Option A: `RetrievalQA` chain (LangChain provided)
   - Option B: Custom LCEL (LangChain Expression Language) chain
   - Example (LCEL): `retriever | prompt_template | llm | output_parser`

4. Error handling:
   - API failures (OpenAI, Pinecone, PostgreSQL)
   - Rate limiting
   - Token overflow
   - Invalid responses

5. Optional optimization: Response caching
   - Cache identical queries for 1 hour
   - Use query hash as key

**Success Criteria**:
- End-to-end chat flow works correctly
- All components integrated and passing data
- Errors handled gracefully
- No hallucinations in responses

---

### 1.10 FastAPI Routes & API Layer

**Objective**: Expose chatbot functionality via REST API.

**Tasks**:

1. Create `src/api/models.py` with Pydantic request/response schemas:
   ```python
   class ChatRequest(BaseModel):
       user_id: str
       session_id: Optional[str] = None
       query: str

   class ChatResponse(BaseModel):
       response: str
       session_id: str
       confidence: float
       handoff_trigger: bool
       intent: str
       metadata: dict

   class HistoryRequest(BaseModel):
       session_id: str

   class HistoryResponse(BaseModel):
       messages: List[dict]
       session_id: str
   ```

2. Create `src/api/routes.py` with endpoints:

   **POST `/chat`**:
   - Input: ChatRequest (user_id, session_id, query)
   - Output: ChatResponse (response, session_id, confidence, handoff_trigger, intent, metadata)
   - Async handling
   - Error responses: 400 (validation), 500 (server error)

   **GET `/history`**:
   - Input: session_id (query param)
   - Output: HistoryResponse (list of messages with timestamps)

   **GET `/analytics`**:
   - Output: minimal analytics summary required by spec (e.g., recent sentiment averages, basic RAGAS aggregates)
   - Note: advanced analytics endpoints may also exist under `/analytics/*`, but `/analytics` must remain stable and spec-compliant.

   **POST `/session`**:
   - Input: user_id
   - Output: {session_id, created_at}
   - Create new chat session

   **GET `/health`**:
   - Output: {status: "healthy", timestamp, dependencies: {postgres: ok, pinecone: ok, openai: ok}}
   - Check all service dependencies

3. Create `src/main.py`:
   - Initialize FastAPI app
   - Register routes
   - Configure CORS (allow frontend requests)
   - Setup logging
   - Add middleware for request tracking

4. Add request validation:
   - Pydantic models for all endpoints
   - Custom validators (e.g., query length limits)

5. Add error handling middleware:
   - Catch exceptions and return appropriate HTTP responses
   - Log errors for debugging

6. Add OpenAPI/Swagger documentation:
   - Auto-generated via FastAPI
   - Available at `/docs` endpoint

**Success Criteria**:
- All endpoints accessible via HTTP
- Request validation working
- Responses match schema
- Swagger docs at `/docs`
- CORS configured for frontend

---

### 1.11 Testing (Unit & Integration)

**Objective**: Achieve 70%+ code coverage with unit and integration tests.

**Tasks**:

1. Create `tests/conftest.py`:
   - Pytest fixtures for database, mock clients
   - Setup test database
   - Mock OpenAI and Pinecone clients

2. Unit tests (`tests/test_*.py`):
   - `test_intent_classifier.py`: 10 test queries with expected classifications
   - `test_retriever.py`: Retrieval ranking and relevance
   - `test_prompt_builder.py`: Prompt construction with various inputs
   - `test_handoff_detector.py`: Frustration signals and escalation
   - `test_sentiment_analyzer.py`: Sentiment scoring
   - `test_chat_memory.py`: Session history persistence
   - `test_database.py`: ORM model creation and queries

3. Integration tests (`tests/test_integration.py`):
   - End-to-end chat flow
   - Retrieval → LLM → response validation
   - Session persistence
   - Handoff detection in full flow
   - Multi-turn conversations

4. API tests (`tests/test_api.py`):
   - POST `/chat` with sample queries
   - GET `/history` with valid session
   - POST `/session` creates new session
   - GET `/health` returns healthy status
   - Error cases (404, 400, 500)

5. Run tests with coverage:
   - Command: `pytest tests/ -v --cov=src --cov-report=html`
   - Target: 70%+ coverage

**Success Criteria**:
- 70%+ code coverage
- All tests pass
- Mock services work correctly
- Integration tests validate full flow

---

### 1.12 Documentation

**Objective**: Provide clear guides for setup, usage, and architecture.

**Tasks**:

1. Create `README.md`:
   - Project overview
   - Quick start guide
   - Features list
   - Tech stack
   - Contributing guidelines

2. Create `docs/SETUP.md`:
   - Local environment setup
   - PostgreSQL installation
   - Pinecone account creation
   - OpenAI API key setup
   - Virtual environment activation
   - Dependency installation

3. Create `docs/KNOWLEDGE_BASE.md`:
   - Knowledge base ingestion guide
   - CSV format specification
   - PDF requirements
   - Running ingestion pipeline
   - Validating Pinecone index

4. Create `docs/API.md`:
   - API endpoint documentation
   - Request/response examples
   - Error codes and handling
   - Authentication (if needed)
   - Rate limits (if applicable)

5. Create `docs/ARCHITECTURE.md`:
   - System component diagram (text-based)
   - Data flow explanation
   - Design decisions and rationale
   - Component interaction

6. Auto-generated docs:
   - Swagger/OpenAPI at `/docs` endpoint
   - Python docstrings for all classes/methods

**Success Criteria**:
- All major setup steps documented
- API usage clear with examples
- Architecture explanation provided
- Easy onboarding for new developers

---

## Phase 2: DATA SCIENCE ANALYTICS & EVALUATION (Weeks 5-8)

### CRITICAL: Phase 2 is the PRIMARY Data Science Focus

This phase is **not supplementary**. It is the core data science contribution for the thesis. The goal is to demonstrate rigorous statistical evaluation and optimization analysis using industry-standard RAGAS metrics and custom analytical frameworks.

**Thesis Deliverable**: Chapter 7 will present the **Performance Matrix** comparing chunking strategies against evaluation metrics, with statistical significance testing and visualization.

---

### 2.1 RAGAS Framework Integration (Primary Evaluation System)

**Objective**: Implement RAGAS (Retrieval-Augmented Generation Assessment) as the core evaluation framework for measuring response quality and retrieval effectiveness.

**What is RAGAS?**
RAGAS is an open-source framework designed specifically for evaluating RAG systems. It uses LLM-based evaluators to assess:
- **Faithfulness**: Is the generated response factually grounded in the retrieved context? (Does it avoid hallucination?)
- **Answer Relevancy**: Does the response directly address the user's query?
- **Context Recall**: Does the retrieved context contain information needed to answer the query?

Each metric scores [0, 1], where 1 is perfect.

**Tasks**:

1. Create `src/core/ragas_evaluator.py`:
   - Implement `RAGASEvaluator` class with methods:
     - `evaluate_response(query, context, response)`: Run all three RAGAS metrics
     - Return: `{faithfulness: float, answer_relevancy: float, context_recall: float, ragas_score: float}`
     - Log all evaluations to PostgreSQL Feedback table

2. Integrate RAGAS library:
   - Use `ragas` Python package for evaluation
   - Configure LLM evaluator (use OpenAI GPT-4o for accuracy)
   - Cache evaluation results to reduce API calls

3. Evaluation Workflow:
   - Every bot response is automatically evaluated against RAGAS metrics
   - Store results in Feedback table with timestamp
   - Include original context, query, and response for reproducibility

4. Create `src/core/ragas_pipeline.py`:
   - Batch evaluate sample conversations (20-30 representative queries)
   - Generate aggregated statistics (mean, std dev, percentiles)
   - Identify low-scoring responses for analysis

**Success Criteria**:
- RAGAS evaluator running for all responses
- Metrics stored in Feedback table
- RAGAS scores range [0, 1] for all metrics
- Evaluations reproducible and documented

---

### 2.2 Performance Matrix: Chunking Size Optimization Study

**Objective**: Conduct empirical study comparing different chunking strategies against RAGAS metrics.

**Research Question**: "How do different chunk sizes (256, 512, 1024, 2048 tokens) affect retrieval quality (Answer Relevancy) and generation quality (Faithfulness)?"

**Tasks**:

1. Create `src/experiments/chunking_experiment.py`:
   - Define experiment design:
     - **Independent Variable**: Chunk size (256, 512, 1024, 2048 tokens)
     - **Dependent Variables**: 
       - Faithfulness (RAGAS metric)
       - Answer Relevancy (RAGAS metric)
       - Context Recall (RAGAS metric)
       - Retrieval latency (milliseconds)
       - Average tokens used per query
   - **Test Set**: Pilot: 30 representative queries (for development). Final experiment: target **100 representative queries** sampled from the knowledge base and stratified by intent (Transactional/Informational/General). Provide sample-size justification in the methodology.

2. Implement chunking strategy variants:
   - Create separate Pinecone indexes (or namespaces) for each chunk size:
     - `empowertech-rag-256`
     - `empowertech-rag-512`
     - `empowertech-rag-1024`
     - `empowertech-rag-2048`
   - Re-ingest sample FAQ knowledge base with each chunk size
   - Preserve all metadata (chunk_id, chunk_size, source)

3. Create `src/experiments/performance_matrix.py`:
   - For each query in test set:
     - Query all 4 indexes (256, 512, 1024, 2048)
     - Generate response using retrieved context from each chunk size
     - Evaluate response with RAGAS
     - Record all metrics with chunk size and query ID
   - Store results in dedicated `PerformanceMatrixResult` database table
    - Add a manual evaluation protocol:
       - Randomly sample 50 responses per condition for human annotation (or all responses if N<=200).
       - Use **3 independent annotators** to rate faithfulness and relevancy on a 3-point or 5-point scale.
       - Compute inter-annotator agreement (Cohen's kappa or Fleiss' kappa) and report values.
       - Resolve disagreements by majority vote and report resolved scores alongside automatic RAGAS scores.
    - Include baseline comparisons:
       - LLM without retrieval (prompt-only baseline)
       - Retrieval-only (top-1 chunk direct answer) if applicable
       - Use these baselines to contextualize RAGAS scores

4. Create `src/experiments/performance_analysis.py`:
   - Compute aggregate statistics for each chunk size:
     ```
     ┌─────────────┬─────────────────────┬─────────────────────┬────────────────────┐
     │ Chunk Size  │ Faithfulness (mean) │ Answer Relevancy    │ Context Recall     │
     ├─────────────┼─────────────────────┼─────────────────────┼────────────────────┤
     │ 256 tokens  │ 0.72 ± 0.12         │ 0.68 ± 0.15         │ 0.65 ± 0.18        │
     │ 512 tokens  │ 0.78 ± 0.10         │ 0.75 ± 0.12         │ 0.72 ± 0.14        │
     │ 1024 tokens │ 0.82 ± 0.09         │ 0.80 ± 0.11         │ 0.78 ± 0.12        │
     │ 2048 tokens │ 0.79 ± 0.11         │ 0.76 ± 0.13         │ 0.74 ± 0.15        │
     └─────────────┴─────────────────────┴─────────────────────┴────────────────────┘
     ```
    - Perform statistical tests and robustness checks:
       - Verify assumptions (normality, homogeneity of variance); if violated, use non-parametric tests (Kruskal–Wallis)
       - ANOVA (or Kruskal–Wallis) to test if chunk size differences are significant
       - Tukey post-hoc test (or Dunn's test with correction) to identify significant pairwise differences
       - Report p-values, 95% confidence intervals, and effect sizes (Cohen's d or eta-squared)
       - Provide a short sample-size justification and power analysis in `docs/PERFORMANCE_MATRIX_REPORT.md`

5. Create visualizations:
   - Line plot: Chunk size vs. Faithfulness (with error bars)
   - Line plot: Chunk size vs. Answer Relevancy (with error bars)
   - Heatmap: Chunk size × RAGAS metric
   - Box plots: Distribution of scores per chunk size

6. Generate `docs/PERFORMANCE_MATRIX_REPORT.md`:
   - Research methodology (sample design, evaluation protocol)
   - Results table (as shown above)
   - Statistical analysis with p-values
   - Interpretation and recommendations
   - Visualizations and charts

**Success Criteria**:
- Experiment runs successfully for all 30 test queries across 4 chunk sizes
- 120 complete RAGAS evaluations (30 queries × 4 chunk sizes)
- Statistical analysis completed with p-values
- Performance Matrix report generated with visualizations
- Recommendation for optimal chunk size based on data

**Thesis Relevance**: This empirical study demonstrates data science rigor, hypothesis testing, and optimization analysis—key requirements for a high-distinction MSc project.

---

### 2.3 Sentiment Analysis & User Satisfaction Tracking

**Objective**: Measure user emotional response and satisfaction in real-time.

**Tasks**:

1. Create `src/core/sentiment_analyzer.py`:
   - Implement `SentimentAnalyzer` class with `analyze(text)` method
   - Return format: `{sentiment_score: float, label: str, confidence: float}`
   - Sentiment range: -1 (very negative) to +1 (very positive)
   - Labels: "negative", "neutral", "positive"

2. Implementation approach (use OpenAI):
   - Use GPT-4o with few-shot prompting for accuracy
   - Examples of negative/neutral/positive queries for context

3. Integration workflow:
   - Analyze user query sentiment in real-time
   - Store sentiment_score in Feedback table
   - Track sentiment trends per session and per user
   - Trigger handoff if sentiment drops below -0.5 with multiple queries

4. Create `src/core/satisfaction_metrics.py`:
   - Compute metrics:
     - **Average Session Sentiment**: Mean sentiment across all queries in session
     - **Sentiment Trend**: Is sentiment improving/degrading during session?
     - **Frustration Events**: Count of consecutive negative-sentiment queries
   - Store in ChatSession table (avg_sentiment field)

5. Create `src/api/satisfaction_routes.py`:
   - **GET `/analytics/user-satisfaction`**: Average sentiment by user
   - **GET `/analytics/sentiment-trend`**: Sentiment over time (daily/weekly)
   - **GET `/analytics/frustrated-sessions`**: Sessions with negative sentiment patterns

**Success Criteria**:
- Sentiment analyzer returns scores in [-1, 1]
- Sentiment tracked for all user queries
- Aggregations computed for user and session-level analysis
- Endpoints available for sentiment analytics

---

### 2.4 Advanced Evaluation: Response Quality & Hallucination Detection

**Objective**: Beyond RAGAS, implement custom evaluation metrics for hallucination detection and response consistency.

**Tasks**:

1. Create `src/core/hallucination_detector.py`:
   - Implement `HallucinationDetector` class
   - Methods:
     - `detect_hallucinations(response, context)`: Identify unsupported claims
     - Return: `{has_hallucination: bool, unsupported_claims: [list], confidence: float}`
   - Use LLM-based evaluation (GPT-4o) to compare response against context
   - Log hallucination instances for quality monitoring

2. Create `src/core/response_consistency_analyzer.py`:
   - Check if similar queries produce consistent responses
   - Store response embeddings in cache
   - Compare new responses to cached responses for similar queries
   - Score consistency [0, 1]

3. Create `src/core/evaluation_aggregator.py`:
   - Combine multiple metrics into composite quality score:
     ```
     Quality Score = (
       0.4 * RAGAS_Faithfulness +
       0.3 * RAGAS_Answer_Relevancy +
       0.2 * (1 - Hallucination_Probability) +
       0.1 * Response_Consistency
     )
     ```
   - Store composite score in Feedback table

4. Create `src/api/quality_routes.py`:
   - **GET `/analytics/response-quality`**: Quality score trends
   - **GET `/analytics/hallucinations`**: Hallucination incidents and analysis
   - **GET `/analytics/consistency`**: Response consistency patterns

**Success Criteria**:
- Hallucination detection implemented and integrated
- Consistency scores computed
- Composite quality metric calculated for all responses
- Analytics available

---

### 2.5 Comparative Analysis: Performance Across Intent Types

**Objective**: Analyze if system performs differently for Transactional vs. Informational queries.

**Tasks**:

1. Create `src/experiments/intent_performance_analysis.py`:
   - Stratify test set by intent (Transactional, Informational, General)
   - Compute RAGAS metrics separately per intent:
     ```
     ┌──────────────┬───────────────┬─────────────────┬────────────────┐
     │ Intent Type  │ Faithfulness  │ Answer Relevancy│ Context Recall │
     ├──────────────┼───────────────┼─────────────────┼────────────────┤
     │ Transactional│ 0.85 ± 0.08   │ 0.82 ± 0.10     │ 0.80 ± 0.12    │
     │ Informational│ 0.79 ± 0.11   │ 0.77 ± 0.13     │ 0.75 ± 0.14    │
     │ General      │ 0.75 ± 0.14   │ 0.72 ± 0.15     │ 0.70 ± 0.16    │
     └──────────────┴───────────────┴─────────────────┴────────────────┘
     ```
   - Perform ANOVA to test significance of differences

2. Create `docs/INTENT_ANALYSIS_REPORT.md`:
   - Analysis methodology
   - Results table with statistical tests
   - Discussion of why certain intents perform better
   - Recommendations for improvement

**Success Criteria**:
- Performance stratified by intent type
- Statistical tests completed
- Analysis report generated

---

### 2.6 Analytics Dashboard Backend & Reporting

**Objective**: Expose all analytics data for visualization and thesis reporting.

**Tasks**:

1. Create `src/core/analytics_service.py`:
   - Implement `AnalyticsService` class with methods:
     - `get_ragas_metrics(start_date, end_date)`: Aggregate RAGAS scores over time
     - `get_chunking_performance()`: Return Performance Matrix results
     - `get_sentiment_metrics()`: User satisfaction trends
     - `get_response_quality()`: Quality score distribution
     - `get_hallucination_report()`: Hallucination incidents
     - `get_performance_by_intent()`: Intent-stratified metrics

2. Create `src/api/analytics_routes.py` with endpoints:
   - **GET `/analytics/ragas`**: RAGAS metrics over time
   - **GET `/analytics/chunking-performance`**: Performance Matrix results
   - **GET `/analytics/sentiment`**: Sentiment analytics
   - **GET `/analytics/quality`**: Response quality metrics
   - **GET `/analytics/hallucinations`**: Hallucination analysis
   - **GET `/analytics/intent-performance`**: Intent-stratified performance

3. Create `scripts/generate_thesis_report.py`:
   - Comprehensive report generation for Chapter 7
   - Includes:
     - Executive summary of analytics
     - Performance Matrix with visualizations
     - RAGAS metric trends
     - Sentiment analysis results
     - Intent-based performance comparison
     - Hallucination analysis
     - Quality score distribution
     - Statistical significance tests
     - Recommendations and conclusions

4. Create `scripts/export_analytics.py`:
   - Export all analytics to CSV/JSON
   - Support for tableau, matplotlib, or other visualization tools
   - Enable further analysis outside of application

5. Database optimization:
   - Create materialized views for expensive queries
   - Example: `v_chunking_performance_matrix` pre-aggregates Performance Matrix data
   - Schedule refresh (e.g., hourly)

**Success Criteria**:
- All analytics endpoints functional
- Thesis report generated successfully
- Export functionality working
- Data ready for visualization

---

### 2.7 Statistical Testing & Significance Analysis

**Objective**: Ensure all analytical claims are statistically rigorous.

**Tasks**:

1. Create `src/experiments/statistical_testing.py`:
   - Implement functions for:
     - **t-tests**: Compare metrics between two conditions
     - **ANOVA**: Compare metrics across 3+ conditions (e.g., chunk sizes)
     - **Tukey post-hoc**: Pairwise comparisons with correction for multiple tests
     - **Effect size calculation**: Cohen's d, eta-squared
     - **Confidence intervals**: Bootstrap CIs for robustness

2. Apply to Performance Matrix:
   - ANOVA on Faithfulness across chunk sizes: *F*(3, 116) = X.XX, *p* < 0.05
   - Tukey post-hoc to identify which chunk sizes differ significantly
   - Report Cohen's d for effect sizes

3. Apply to Intent Performance:
   - ANOVA on Faithfulness across intents
   - Pairwise comparisons with Tukey correction

4. Documentation:
   - For each statistical test, report:
     - Test name and assumptions
     - Test statistic and p-value
     - Effect size (if applicable)
     - Interpretation (statistically significant? practically significant?)

**Success Criteria**:
- All claims supported by statistical tests
- P-values reported for all comparisons
- Effect sizes calculated
- Assumptions of tests verified

---

### Phase 2 Deliverables Summary

By end of Phase 2, the following **thesis-ready** documents will be completed:

1. **`docs/RAGAS_EVALUATION_FRAMEWORK.md`**: Description of RAGAS metrics and evaluation protocol
2. **`docs/PERFORMANCE_MATRIX_REPORT.md`**: Chunking size optimization study with results, statistics, and visualizations
3. **`docs/INTENT_ANALYSIS_REPORT.md`**: Performance comparison across intent types
4. **`docs/RESPONSE_QUALITY_ANALYSIS.md`**: Hallucination detection, consistency, composite quality metric
5. **`docs/SENTIMENT_ANALYSIS_REPORT.md`**: User satisfaction trends and sentiment insights
6. **Thesis Chapter 7 Draft**: Compiled analytics narrative with all findings

All reports include:
- Methodology and research questions
- Results tables with means, standard deviations, confidence intervals
- Statistical tests with p-values
- Visualizations (line plots, box plots, heatmaps)
- Discussion and interpretation
- Recommendations for system improvement

---

## Phase 3: Deployment and Demo (Required for Submission)

This phase contains a minimal, reproducible demo required for final submission (PDF + demo link). Full cloud deployment remains optional and may be completed if time permits.

### 3.1 Minimum Demo (Required)
- Provide a reproducible demo that reviewers can run locally (Docker Compose) or view as a hosted demo. The demo must:
   - Start the FastAPI app and a local PostgreSQL instance via `docker-compose up`.
   - Include a small seeded knowledge base and evaluation queries so reviewers can exercise the `/chat` and `/analytics` endpoints.
   - Include a short README (`docs/DEMO_README.md`) with instructions to run the demo and example requests.

### 3.2 Containerization (Required for Demo)
- Provide a `Dockerfile` for the FastAPI application and a `docker-compose.yml` that brings up:
   - `app` (FastAPI)
   - `postgres` (PostgreSQL)
   - (Optional) `pgadmin` for DB inspection
- Ensure images are small and multi-stage builds are used where appropriate.

### 3.3 Cloud Deployment (Optional)
- Optional: deploy to a public host (Heroku/GCP/AWS) if time allows and include link in submission.
- If public deployment is provided, include environment variable redaction and instructions for security and cost considerations.

---

## Project File Structure

```
f:\Major Project/
├── IMPLEMENTATION_PLAN.md              # This file
├── README.md                           # Project overview
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment template
├── .gitignore                          # Git ignore rules
│
├── src/
│   ├── __init__.py
│   ├── main.py                         # FastAPI app entry point
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── models.py                   # Pydantic request/response schemas
│   │   ├── routes.py                   # FastAPI routes (/chat, /history, etc)
│   │   ├── analytics_routes.py         # Analytics endpoints (Phase 2)
│   │   ├── satisfaction_routes.py      # Sentiment/satisfaction endpoints (Phase 2)
│   │   ├── quality_routes.py           # Response quality endpoints (Phase 2)
│   │   └── errors.py                   # Exception handlers
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── retriever.py                # HybridRetriever class
│   │   ├── intent_classifier.py        # IntentClassifier class
│   │   ├── intent_examples.py          # Intent classification examples
│   │   ├── sentiment_analyzer.py       # SentimentAnalyzer class (Phase 2)
│   │   ├── sentiment_examples.py       # Sentiment examples (Phase 2)
│   │   ├── handoff_detector.py         # HandoffDetector class
│   │   ├── escalation_messages.py      # Escalation message templates
│   │   ├── chat_orchestrator.py        # ChatOrchestrator class
│   │   ├── llm_client.py               # LLM API wrapper
│   │   ├── chat_memory.py              # ChatMemory class
│   │   ├── conversation_manager.py     # ConversationManager class
│   │   ├── prompt_builder.py           # PromptBuilder class
│   │   ├── prompt_templates.py         # Prompt template definitions
│   │   ├── context_formatter.py        # Context formatting utilities
│   │   ├── ragas_evaluator.py          # RAGAS metrics (Phase 2)
│   │   ├── ragas_pipeline.py           # RAGAS evaluation workflow (Phase 2)
│   │   ├── hallucination_detector.py   # Hallucination detection (Phase 2)
│   │   ├── response_consistency.py     # Response consistency analyzer (Phase 2)
│   │   ├── evaluation_aggregator.py    # Composite quality metric (Phase 2)
│   │   ├── analytics_service.py        # Analytics aggregation (Phase 2)
│   │   ├── satisfaction_metrics.py     # Session satisfaction tracking (Phase 2)
│   │   └── reporting.py                # Report generation (Phase 2)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py                 # SQLAlchemy ORM models
│   │   ├── init_db.py                  # Database initialization
│   │   └── seed_db.py                  # Test data seeding
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── pipeline.py                 # IngestionPipeline class
│   │   ├── pdf_parser.py               # PDF text extraction
│   │   ├── csv_parser.py               # CSV/FAQ parsing
│   │   ├── chunking.py                 # Text chunking logic
│   │   └── ingest.py                   # CLI entry point
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py                 # Environment configuration
│   │
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py                  # Common utilities
│       ├── logger.py                   # Logging configuration
│       └── validators.py               # Input validation helpers
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                     # Pytest fixtures and mocks
│   ├── test_retriever.py               # Retrieval tests
│   ├── test_intent_classifier.py       # Intent classification tests
│   ├── test_handoff_detector.py        # Handoff detection tests
│   ├── test_sentiment_analyzer.py      # Sentiment analysis tests (Phase 2)
│   ├── test_chat_orchestrator.py       # Orchestration tests
│   ├── test_api.py                     # API endpoint tests
│   ├── test_database.py                # Database model tests
│   └── test_integration.py             # End-to-end integration tests
│
├── data/
│   ├── sample_faqs.csv                 # Mock FAQ data (20-30 QA pairs)
│   ├── sample_document.pdf             # Mock course catalog PDF
│   └── evaluation_queries.csv          # Test set for RAGAS evaluation (Phase 2)
│
├── experiments/
│   ├── __init__.py
│   ├── chunking_experiment.py          # Chunk size performance study (Phase 2)
│   ├── performance_matrix.py           # Performance Matrix execution (Phase 2)
│   ├── performance_analysis.py         # Performance Matrix analysis (Phase 2)
│   ├── intent_performance_analysis.py  # Intent-based performance (Phase 2)
│   ├── statistical_testing.py          # Statistical significance tests (Phase 2)
│   └── ragas_evaluation_set.py         # Sample queries for evaluation (Phase 2)
│
├── docs/
│   ├── SETUP.md                        # Local environment setup
│   ├── KNOWLEDGE_BASE.md               # Knowledge base ingestion guide
│   ├── API.md                          # API documentation
│   ├── ARCHITECTURE.md                 # System architecture explanation
│   ├── RAGAS_EVALUATION_FRAMEWORK.md   # RAGAS methodology (Phase 2)
│   ├── PERFORMANCE_MATRIX_REPORT.md    # Chunking optimization study (Phase 2)
│   ├── INTENT_ANALYSIS_REPORT.md       # Intent-based performance (Phase 2)
│   ├── RESPONSE_QUALITY_ANALYSIS.md    # Hallucination & quality (Phase 2)
│   └── SENTIMENT_ANALYSIS_REPORT.md    # User satisfaction trends (Phase 2)
│
├── scripts/
│   ├── generate_thesis_report.py       # Chapter 7 comprehensive report (Phase 2)
│   ├── export_analytics.py             # Export for external visualization (Phase 2)
│   └── analyze_conversations.py        # Conversation pattern analysis (Phase 2)
│
└── RESOURCES/
    └── PROJECT_SPEC.md                 # Original project specification
```

---

## Key Architectural Patterns & Design Decisions

### 1. Component Separation of Concerns

Each module has a single responsibility:
- **Retriever**: Context from knowledge base
- **Intent Classifier**: Query categorization
- **Sentiment Analyzer**: Emotion detection
- **Chat Orchestrator**: Component coordination
- **Prompt Builder**: LLM prompt construction
- **Handoff Detector**: Escalation logic

**Benefit**: Testability, maintainability, independent scaling

### 2. LangChain Integration

Use LangChain abstractions for flexibility:
- `Retrievers` API for custom retrieval logic
- `Chains` (or LCEL) for component composition
- `PromptTemplates` for prompt management
- `LLMChain` or custom chains for orchestration

**Benefit**: Can swap components (e.g., different LLM, vector DB) without rewriting logic

### 3. Async FastAPI

All I/O operations (database, API calls) are asynchronous:
- `async def` routes and handlers
- `AsyncSession` for SQLAlchemy
- Concurrent request handling

**Benefit**: High throughput, better resource utilization

### 4. Prompt-Based Intelligence

Use GPT-4o few-shot prompting for:
- Intent classification
- Sentiment analysis
- Handoff decision logic

**Benefit**: No need for fine-tuning (faster MVP), flexible categories, good accuracy

### 5. Guardrail-First Design

Hallucination prevention through:
- Confidence threshold checks before LLM calls
- Hardcoded fallback messages
- Context validation

**Benefit**: Safe responses, user trust, reduced misinformation

### 6. Database-Backed Memory

Session history persisted to PostgreSQL:
- Survives application restarts
- Enables analytics and reporting
- Supports multi-user scenarios

**Benefit**: Stateless API, horizontal scaling, audit trail

---

## Testing Strategy

### Unit Tests
- Test individual components (retriever, intent, sentiment)
- Mock external services (OpenAI, Pinecone)
- Fast execution (< 1 second each)

### Integration Tests
- Test component interactions (retriever + LLM)
- Test database operations
- Test full chat flow

### API Tests
- Test endpoint functionality
- Test error handling
- Test request validation

### Coverage Target
- 70%+ code coverage
- Critical paths fully tested
- Edge cases covered

---

## Verification Checkpoints

### Phase 1 Success Criteria

1. **Setup Verification**:
   - [ ] All Python packages installed and importable
   - [ ] PostgreSQL database created and schema loaded
   - [ ] `.env` configured with valid API keys

2. **Ingestion Verification**:
   - [ ] Ingestion script runs: `python -m src.ingestion.ingest --source data/sample_faqs.csv --type csv`
   - [ ] 20+ embeddings stored in Pinecone
   - [ ] Pinecone index stats confirm successful ingestion

3. **Retrieval Verification**:
   - [ ] HybridRetriever returns relevant chunks for 5 sample queries
   - [ ] Semantic search scores > 0.7 for relevant documents
   - [ ] Keyword fallback works when semantic fails

4. **Intent Classification Verification**:
   - [ ] 10 test queries classified correctly (Transactional/Informational/General)
   - [ ] Confidence scores reasonable (0.7-0.95 for clear cases)

5. **Chat Flow Verification**:
   - [ ] POST `/chat` returns response grounded in retrieved context
   - [ ] Response does not hallucinate information
   - [ ] No crashes or unexpected errors

6. **Session Management Verification**:
   - [ ] POST `/session` creates new session successfully
   - [ ] Subsequent `/chat` calls use same session
   - [ ] GET `/history` returns all messages from session

7. **Handoff Detection Verification**:
   - [ ] Query with frustration keywords triggers handoff
   - [ ] Negative sentiment queries escalate appropriately
   - [ ] Normal queries do NOT trigger handoff

8. **Testing Verification**:
   - [ ] `pytest tests/ -v --cov=src` returns 70%+ coverage
   - [ ] All tests pass
   - [ ] No warnings or errors

### Phase 2 Success Criteria — **DATA SCIENCE FOCUS**

1. **RAGAS Framework Integration**:
   - [ ] RAGAS evaluator functional for Faithfulness, Answer Relevancy, Context Recall
   - [ ] Metrics computed for 30+ sample queries
   - [ ] Scores range [0, 1] with expected distributions
   - [ ] All evaluations logged to Feedback table with timestamps

2. **Performance Matrix Study**:
   - [ ] Four Pinecone indexes created (256, 512, 1024, 2048 token chunk sizes)
   - [ ] Sample FAQ ingested into all 4 indexes successfully
   - [ ] 30 representative test queries created and documented
   - [ ] All 30 queries evaluated across all 4 chunk sizes (120 total evaluations)
   - [ ] Performance Matrix results table created with means, std devs:
     ```
     Chunk Size | Faithfulness | Answer Relevancy | Context Recall | Latency (ms)
     256        | 0.72 ± 0.12  | 0.68 ± 0.15      | 0.65 ± 0.18    | 45
     512        | 0.78 ± 0.10  | 0.75 ± 0.12      | 0.72 ± 0.14    | 52
     1024       | 0.82 ± 0.09  | 0.80 ± 0.11      | 0.78 ± 0.12    | 68
     2048       | 0.79 ± 0.11  | 0.76 ± 0.13      | 0.74 ± 0.15    | 95
     ```
   - [ ] Statistical tests completed: ANOVA p-values < 0.05 for chunk size differences
   - [ ] Tukey post-hoc comparisons identify pairwise differences
   - [ ] Effect sizes (Cohen's d) calculated
   - [ ] Visualizations generated (line plots with error bars, heatmaps)
   - [ ] `docs/PERFORMANCE_MATRIX_REPORT.md` completed with methodology, results, statistics, interpretation

3. **Intent-Stratified Performance Analysis**:
   - [ ] Test set stratified into Transactional, Informational, General (10 queries each)
   - [ ] RAGAS metrics computed per intent type
   - [ ] ANOVA confirms performance differences by intent (if p < 0.05)
   - [ ] Performance comparison table generated
   - [ ] `docs/INTENT_ANALYSIS_REPORT.md` completed

4. **Sentiment Analysis & User Satisfaction**:
   - [ ] Sentiment analyzer returns scores [-1, 1] with reasonable distributions
   - [ ] Sentiment stored in Feedback table for all test queries
   - [ ] Session-level sentiment aggregation working
   - [ ] GET `/analytics/sentiment` returns user satisfaction trends
   - [ ] Sentiment tied to handoff detection (sentiment < -0.5 → escalation)

5. **Response Quality & Hallucination Detection**:
   - [ ] Hallucination detector identifies unsupported claims
   - [ ] Response consistency analyzer scores similar queries
   - [ ] Composite quality metric calculated: 0.4×Faithfulness + 0.3×Answer_Relevancy + 0.2×(1-Hallucination) + 0.1×Consistency
   - [ ] Quality scores stored in Feedback table
   - [ ] `docs/RESPONSE_QUALITY_ANALYSIS.md` completed

6. **Statistical Testing**:
   - [ ] ANOVA test results documented with F-statistic, p-value, effect size
   - [ ] Tukey post-hoc corrections applied for multiple comparisons
   - [ ] Confidence intervals (95%) calculated for all metrics
   - [ ] Statistical assumptions verified (normality, homogeneity of variance)
   - [ ] All statistical claims supported by formal tests

7. **Analytics Endpoints**:
   - [ ] GET `/analytics/ragas` returns RAGAS metric trends over time
   - [ ] GET `/analytics/chunking-performance` returns Performance Matrix data
   - [ ] GET `/analytics/sentiment` returns sentiment analytics and user satisfaction
   - [ ] GET `/analytics/quality` returns response quality distribution
   - [ ] GET `/analytics/hallucinations` returns hallucination incident analysis
   - [ ] GET `/analytics/intent-performance` returns intent-stratified metrics

8. **Thesis Reporting**:
   - [ ] `docs/RAGAS_EVALUATION_FRAMEWORK.md` — RAGAS methodology and protocol
   - [ ] `docs/PERFORMANCE_MATRIX_REPORT.md` — Chunking optimization study (complete with statistics)
   - [ ] `docs/INTENT_ANALYSIS_REPORT.md` — Intent performance comparison
   - [ ] `docs/RESPONSE_QUALITY_ANALYSIS.md` — Hallucination detection and quality metrics
   - [ ] `docs/SENTIMENT_ANALYSIS_REPORT.md` — User satisfaction trends
   - [ ] `scripts/generate_thesis_report.py` generates comprehensive Chapter 7 draft
   - [ ] All reports include: methodology, results tables, statistical tests, visualizations, interpretation, recommendations

---

## Scope: Included vs. Excluded

### ✅ Phase 1 Included
- Core RAG chat with semantic + keyword retrieval
- Intent classification (3 categories)
- Multi-turn conversation memory (PostgreSQL-backed session history)
- Human handoff detection (frustration, complexity, failures)
- FastAPI REST API with validation
- Guardrails against hallucination
- Relational database schema (Chapter 4) with 4 normalized tables
- 70%+ test coverage
- Local development focus

### ✅ Phase 2 Included — **DATA SCIENCE PRIMARY FOCUS**
- **RAGAS evaluation framework** (Faithfulness, Answer Relevancy, Context Recall) as primary analytical tool
- **Performance Matrix study**: Empirical comparison of 4 chunking sizes (256, 512, 1024, 2048 tokens) against RAGAS metrics with statistical significance testing
- **Sentiment analysis**: Real-time emotion detection and user satisfaction tracking
- **Response quality metrics**: Hallucination detection, response consistency, composite quality score
- **Intent-stratified performance**: Analysis comparing system performance across Transactional/Informational/General queries
- **Statistical testing**: ANOVA, Tukey post-hoc, effect sizes, confidence intervals
- **Thesis-ready reporting**: 5+ analytical documents with visualizations and statistical tests
- **Chapter 7 narrative**: Comprehensive data science analysis for MSc thesis

### 🔷 Phase 3: Demo Required (minimal)
- Minimal demo (Docker Compose) is required for final submission (see Phase 3 section above).
- Full cloud deployment, CI/CD, and production monitoring remain optional/out-of-scope for the thesis but may be included if time permits.

---

## Formatting & Submission Requirements

These requirements align the implementation and thesis deliverables with the official project report guidelines.

- **Overall length (MSc (DS))**: Target **60–100 pages** and **18,000–30,000 words**. Aim for 60–80 pages and 18k–25k words for practical delivery.
- **Preliminary pages (mandatory)**: Cover Page, Bonafide Certificate, Declaration, Acknowledgement, Abstract (150–250 words), Table of Contents, List of Figures, List of Tables, List of Abbreviations.
- **Per-chapter minimums (MSc(DS))**: Chapter 1: 5–8 pp, Chapter 2: 8–12 pp, Chapter 3: 8–10 pp, Chapter 4: 10–15 pp, Chapter 5: 12–20 pp, Chapter 6: 6–8 pp, Chapter 7: 4–6 pp, Chapter 8: 3–5 pp.
- **References**: Minimum **20 credible sources** (research papers, IEEE, books, official docs). Use **APA** citation style.
- **Formatting**: Times New Roman, 12 pt body, headings 14–16 pt bold, 1.5 line spacing, 1" margins, justified alignment, page numbers bottom-right.
- **Diagrams & Screenshots**: MSc(DS) recommended 20–40 figures. Number and caption all figures with explanations below each figure.
- **Appendices**: Include full source code, `db_dump.sql`, installation guide, and `docs/DEMO_README.md`. Do not dump full code into main chapters—place it in appendices and reference excerpts in the implementation chapter.
- **Plagiarism**: Ensure report plagiarism is within university limits and include guide approval signature before submission.
- **Final deliverables**: Single consolidated PDF (report), Presentation (PPT and exported PDF), GitHub repository link, and Live Demo link or `docker-compose` demo instructions. If hosted demo is provided, include the URL and access instructions.

### Final Submission Checklist (add to `IMPLEMENTATION_PLAN.md` and `docs/SETUP.md`)
- Working project demo (Docker Compose or hosted URL)
- All UML diagrams included and numbered
- Source code attached in `Appendices` and uploaded to GitHub
- `db_dump.sql` included
- 20+ references listed in APA format
- Guide approval signature scanned or statement of approval
- PDF export of the report (A4 or US Letter as required by institute)
- Plagiarism report (if required by institute)


### ❌ Out of Scope (Future)
- Frontend UI (API-only; separate project)
- Voice/audio support
- Multi-language support
- Custom fine-tuned LLM
- Real-time user collaboration
- Advanced RAG (graph-based, query rewriting)

---

## Technical Requirements Summary

| Requirement | Tool/Technology | Rationale |
|---|---|---|
| Language | Python 3.10+ | Standard for data science & ML |
| API Framework | FastAPI | High performance, async support, auto docs |
| LLM Orchestration | LangChain | Flexible, production-ready, good abstractions |
| Primary LLM | OpenAI GPT-4o | Production quality, recommended for MSc |
| Embeddings | OpenAI text-embedding-3-small | State-of-the-art, compatible with OpenAI |
| Vector DB | Pinecone | Serverless, managed, no self-hosting |
| Relational DB | PostgreSQL | Robust, open-source, strong for analytics |
| ORM | SQLAlchemy | Pythonic, flexible, async support |
| Testing | Pytest | Standard for Python, good fixtures/mocks |
| **Evaluation Framework** | **RAGAS** | **Industry standard for RAG evaluation** |
| **Statistical Testing** | **SciPy (ANOVA, Tukey)** | **Statistical significance for Performance Matrix** |
| **Data Analysis** | **Pandas, NumPy** | **Data aggregation and metric computation** |
| **Visualization** | **Matplotlib, Seaborn** | **Thesis-quality charts and plots** |

---

## Development Workflow

### Getting Started
1. Clone repository (or create locally)
2. Copy `.env.example` to `.env` and fill in API keys
3. Create PostgreSQL database `empowertech_chatbot`
4. Create Python virtual environment and install dependencies
5. Run `python -m src.models.init_db` to create schema
6. Run ingestion: `python -m src.ingestion.ingest --source data/sample_faqs.csv --type csv`
7. Start API: `uvicorn src.main:app --reload`
8. Test at `http://localhost:8000/docs` (Swagger UI)

### Running Tests
```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Development Phases
- **Week 1-2**: Setup, database, ingestion pipeline
- **Week 2-3**: Retriever, intent classifier, orchestration
- **Week 3-4**: API routes, memory management, testing
- **Week 4-5**: Refinement, documentation, integration testing
- **Week 5-6**: Sentiment analysis, RAGAS evaluation, analytics

---

## Conclusion

This implementation plan positions the project as **Data Science research with RAG application**, not merely engineering. The three-phase approach ensures rigorous evaluation:

**Phase 1** establishes a production-grade RAG chatbot with proper relational database design (Chapter 4 schema) and guardrails against hallucination.

**Phase 2** is the thesis centerpiece: Comprehensive statistical analysis using RAGAS metrics, empirical Performance Matrix study, intent-stratified analysis, and formal hypothesis testing. This demonstrates MSc-level data science rigor with publishable findings.

**Phase 3** (deferred) handles deployment complexity.

**Key Thesis Contributions:**
1. **Performance Matrix**: Empirical evidence of chunking optimization (chunk size vs. Faithfulness/Answer Relevancy with statistical significance)
2. **RAGAS Framework**: Industry-standard RAG evaluation applied rigorously with proper statistical testing
3. **Sentiment-Performance Correlation**: User satisfaction tied to system metrics
4. **Intent-Based Analysis**: Performance variation across query types
5. **Composite Quality Metric**: Novel aggregation of multiple evaluation dimensions

The architecture is modular, testable, and uses industry-standard tools. All analytical claims are statistically rigorous with p-values, effect sizes, and confidence intervals.

**Timeline**: ~8 weeks (Phase 1: weeks 1-4, Phase 2: weeks 5-8)

Ready to proceed with Phase 1 implementation.

---

## Appendix: RAGAS Metrics Explained

**RAGAS** (Retrieval-Augmented Generation Assessment) is the gold-standard framework for evaluating RAG systems:

- **Faithfulness** (F): Does the response contain only information present in the retrieved context? Prevents hallucination. Range [0, 1]; 1 = no hallucination.
  
- **Answer Relevancy** (AR): Does the response directly address the user's query? Measures utility. Range [0, 1]; 1 = perfectly relevant.
  
- **Context Recall** (CR): Is all information needed to answer the query present in the retrieved context? Measures retrieval quality. Range [0, 1]; 1 = all needed info retrieved.

**RAGAS Score** = Average of (F + AR + CR) / 3

All three metrics will be computed for the Performance Matrix study to provide holistic quality assessment.
