"""
Chunking experiment scaffold (multi chunk-size sweeps require re-ingestion).

For **offline RAG evaluation + statistical tests** on the current index, run:

    python experiments/run_rag_evaluation.py

See experiments/README_EVALUATION.md and experiments/results/RAG_EVAL_SUMMARY.md.
"""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunk-sizes", default="256,512,1024,2048")
    parser.add_argument("--queries-path", default="data/evaluation_queries.csv")
    args = parser.parse_args()

    chunk_sizes = [int(x.strip()) for x in args.chunk_sizes.split(",") if x.strip()]
    print("Planned chunk sizes:", chunk_sizes)
    print("Queries file:", args.queries_path)
    print("Chunk-size matrix: re-ingest per size, then score — see Docs/IMPLEMENTATION_PLAN.md Phase 2.")
    print("Ready-to-run eval + stats: python experiments/run_rag_evaluation.py")


if __name__ == "__main__":
    main()

