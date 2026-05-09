"""
Offline RAG evaluation: retrieval + generation per gold query, descriptive metrics,
and paired statistical tests comparing two retrieval settings (top_k).

Outputs (under experiments/results/):
  - rag_eval_runs.csv          — one row per query × condition
  - rag_eval_statistics.json — means, paired t-test, Wilcoxon
  - RAG_EVAL_SUMMARY.md       — human-readable summary for reports

Uses OpenAI embeddings (same model as production) for answer–reference cosine similarity.

Note: Full RAGAS scores require a working `ragas` install (often fails on Windows due to
native langchain dependencies). Run under WSL2/Linux/Docker if you need RAGAS explicitly.
"""

from __future__ import annotations

import csv
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def tokens(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", s.lower()))


def ref_context_token_recall(reference: str, context_blob: str) -> float:
    rt, ct = tokens(reference), tokens(context_blob)
    if not rt:
        return 0.0
    return len(rt & ct) / len(rt)


def load_gold(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    sys.path.insert(0, str(ROOT))
    os.chdir(ROOT)

    from scipy.stats import ttest_rel, wilcoxon

    from src.config.settings import settings
    from src.core.chat_orchestrator import FALLBACK_MESSAGE
    from src.core.llm_client import LLMClient
    from src.core.prompt_builder import PromptBuilder
    from src.core.retriever import Retriever
    from src.core.vector_store import OpenAIEmbedder

    gold_path = ROOT / "data" / "evaluation_gold.csv"
    out_dir = ROOT / "experiments" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not settings.openai_api_key:
        print("OPENAI_API_KEY required in environment or .env", file=sys.stderr)
        sys.exit(1)

    gold_rows = load_gold(gold_path)
    conditions = [{"name": "top_k_3", "top_k": 3}, {"name": "top_k_5", "top_k": 5}]

    retriever = Retriever()
    builder = PromptBuilder()
    llm = LLMClient()
    embedder = OpenAIEmbedder()

    runs: list[dict[str, Any]] = []

    for row in gold_rows:
        qid = row["id"]
        query = row["query"]
        reference = row["reference_answer"]
        intent = row.get("intent", "")
        ref_emb = embedder.embed(reference[:8000])

        for cond in conditions:
            k = cond["top_k"]
            rr = retriever.retrieve(query, top_k=k)
            chunk_texts = [c.text for c in rr.chunks]
            context_blob = "\n".join(chunk_texts)
            max_score = max((c.score for c in rr.chunks), default=0.0)
            lex_rec = ref_context_token_recall(reference, context_blob)

            no_ctx = not rr.chunks
            low_conf = rr.confidence is not None and rr.confidence < settings.retrieval_confidence_threshold
            guardrail = no_ctx or low_conf

            if guardrail:
                answer = FALLBACK_MESSAGE
                used_llm = False
            else:
                sys_p, usr_p = builder.build(query, [], rr.chunks)
                gen = llm.chat(sys_p, usr_p)
                answer = gen.text
                used_llm = True

            ans_emb = embedder.embed(answer[:8000])
            sim = cosine_similarity(ref_emb, ans_emb)

            runs.append(
                {
                    "condition": cond["name"],
                    "top_k": k,
                    "query_id": qid,
                    "query": query,
                    "intent": intent,
                    "retrieval_max_score": round(max_score, 4),
                    "ref_context_token_recall": round(lex_rec, 4),
                    "answer_reference_embedding_similarity": round(sim, 4),
                    "used_llm": used_llm,
                    "guardrail": guardrail,
                    "no_context": no_ctx,
                    "low_confidence": bool(low_conf and not no_ctx),
                }
            )

    csv_out = out_dir / "rag_eval_runs.csv"
    fieldnames = [
        "condition",
        "top_k",
        "query_id",
        "query",
        "intent",
        "retrieval_max_score",
        "ref_context_token_recall",
        "answer_reference_embedding_similarity",
        "used_llm",
        "guardrail",
        "no_context",
        "low_confidence",
    ]
    with csv_out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(runs)

    by_q: dict[str, dict[str, float]] = {}
    for r in runs:
        qid = str(r["query_id"])
        by_q.setdefault(qid, {})[str(r["condition"])] = float(r["answer_reference_embedding_similarity"])

    sim_3: list[float] = []
    sim_5: list[float] = []
    for qid in sorted(by_q.keys(), key=int):
        d = by_q[qid]
        if "top_k_3" in d and "top_k_5" in d:
            sim_3.append(d["top_k_3"])
            sim_5.append(d["top_k_5"])

    stats_summary: dict[str, Any] = {
        "n_pairs": len(sim_3),
        "similarity_mean_top_k_3": round(sum(sim_3) / len(sim_3), 4) if sim_3 else None,
        "similarity_mean_top_k_5": round(sum(sim_5) / len(sim_5), 4) if sim_5 else None,
        "difference_mean_top5_minus_top3": round(sum(s5 - s3 for s3, s5 in zip(sim_3, sim_5)) / len(sim_3), 4)
        if sim_3
        else None,
        "paired_ttest": None,
        "wilcoxon_signed_rank": None,
        "methodology": (
            "Paired comparisons on answer_reference_embedding_similarity — cosine similarity of OpenAI embeddings "
            f"({settings.openai_embedding_model}) between gold reference_answer and generated answer. "
            "ref_context_token_recall = |reference tokens ∩ context tokens| / |reference tokens|."
        ),
    }

    if len(sim_3) >= 2:
        t_stat, p_t = ttest_rel(sim_5, sim_3)
        stats_summary["paired_ttest"] = {
            "statistic": float(t_stat),
            "pvalue": float(p_t),
            "null_hypothesis": "mean(similarity_top_k_5 - similarity_top_k_3) = 0",
        }
        diff = [a - b for a, b in zip(sim_5, sim_3)]
        try:
            w_stat, p_w = wilcoxon(diff, alternative="two-sided")
            stats_summary["wilcoxon_signed_rank"] = {"statistic": float(w_stat), "pvalue": float(p_w)}
        except ValueError as e:
            stats_summary["wilcoxon_signed_rank"] = {"error": str(e)}

    json_out = out_dir / "rag_eval_statistics.json"
    with json_out.open("w", encoding="utf-8") as f:
        json.dump(stats_summary, f, indent=2)

    md_lines = [
        "# RAG offline evaluation summary",
        "",
        "| Artifact | Path |",
        "|----------|------|",
        f"| Per-run CSV | `{csv_out.relative_to(ROOT).as_posix()}` |",
        f"| Statistics JSON | `{json_out.relative_to(ROOT).as_posix()}` |",
        f"| Gold labels | `{gold_path.relative_to(ROOT).as_posix()}` |",
        "",
        "## Conditions",
        "",
        "- Compared **top_k = 3** vs **top_k = 5** on the same queries (paired design).",
        "",
        "## Descriptive statistics",
        "",
        f"- Pairs **N** = {stats_summary['n_pairs']}",
        f"- Mean answer–reference embedding similarity (**top_k=3**): **{stats_summary['similarity_mean_top_k_3']}**",
        f"- Mean answer–reference embedding similarity (**top_k=5**): **{stats_summary['similarity_mean_top_k_5']}**",
        f"- Mean paired difference (**top_k_5 − top_k_3**): **{stats_summary['difference_mean_top5_minus_top3']}**",
        "",
        "## Inference (paired)",
        "",
    ]
    if stats_summary.get("paired_ttest"):
        pt = stats_summary["paired_ttest"]
        md_lines.append(
            f"- **Paired t-test** on similarities (top_k 5 vs 3): statistic = {pt['statistic']:.4f}, "
            f"*p*-value = {pt['pvalue']:.6g}"
        )
    if isinstance(stats_summary.get("wilcoxon_signed_rank"), dict):
        wr = stats_summary["wilcoxon_signed_rank"]
        if "statistic" in wr:
            md_lines.append(
                f"- **Wilcoxon signed-rank** on paired differences: statistic = {wr['statistic']:.4f}, "
                f"*p*-value = {wr['pvalue']:.6g}"
            )
        elif "error" in wr:
            md_lines.append(f"- **Wilcoxon** skipped: {wr['error']}")
    md_lines.extend(
        [
            "",
            "## Chapter 7 reporting hints",
            "",
            "- Embedding similarity proxies **semantic alignment** with the gold FAQ answer; cite limitations (no entailment judgment).",
            "- For **true RAGAS** (faithfulness, etc.), replicate this batch under Linux/WSL2 with `pip install ragas` working, ",
            "  then add a second exports file from `ragas.evaluate`.",
            "- Increase **sample size** and add **multiple annotators** if you promise human-subjective evaluation.",
            "",
        ]
    )
    md_path = out_dir / "RAG_EVAL_SUMMARY.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Wrote {csv_out}")
    print(f"Wrote {json_out}")
    print(f"Wrote {md_path}")
    print(json.dumps(stats_summary, indent=2))


if __name__ == "__main__":
    main()
