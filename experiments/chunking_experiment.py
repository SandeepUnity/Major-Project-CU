"""
Chunking experiment scaffold.

Runs a small evaluation set across multiple chunk sizes and stores results in the DB.
This is intentionally minimal; expand for thesis runs (N=100 queries, multiple namespaces).
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
    print("TODO: implement experiment runner (see Docs/IMPLEMENTATION_PLAN.md Phase 2).")


if __name__ == "__main__":
    main()

