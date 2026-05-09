# RAG offline evaluation

## What runs

`run_rag_evaluation.py` loads **`data/evaluation_gold.csv`** (query + reference answer), then for each query evaluates two retrieval settings (**`top_k = 3`** vs **`top_k = 5`**):

1. Retrieve from Pinecone  
2. Apply the same guardrail rules as production (`retrieval_confidence_threshold`)  
3. If safe, generate an answer with **`LLMClient`** + **`PromptBuilder`**  
4. Score against the gold answer with **cosine similarity of OpenAI embeddings** and **lexical overlap** between reference tokens and retrieved context  

## Requirements

- `.env` with **`OPENAI_API_KEY`**, **`PINECONE_API_KEY`**, and index settings matching your ingested vectors  
- Dependencies: `pip install -r requirements.txt` (includes **`scipy`** for tests)  

## Command

From the repository root:

```bash
python experiments/run_rag_evaluation.py
```

## Outputs

| File | Description |
|------|-------------|
| `experiments/results/rag_eval_runs.csv` | One row per query × condition |
| `experiments/results/rag_eval_statistics.json` | Means, paired *t*-test, Wilcoxon |
| `experiments/results/RAG_EVAL_SUMMARY.md` | Short narrative for the report |

## RAGAS

The **`ragas`** package is listed in `requirements.txt` for future use but may **fail to import on Windows** (LangChain / `uuid_utils` native DLL issues). For **full RAGAS metrics**, run the same batch approach under **WSL2**, **Linux**, or **Docker**, then call `ragas.evaluate` on the saved question/answer/context rows.

## Extending

- Add rows to `evaluation_gold.csv` (keep `id,query,intent,reference_answer`).  
- Add more conditions (e.g. `top_k=7`) in `conditions` inside `run_rag_evaluation.py`.  
- Chunk-size experiments require **re-running ingestion** per chunk size before scoring.
