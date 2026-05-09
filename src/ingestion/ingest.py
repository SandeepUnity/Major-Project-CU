from __future__ import annotations

import argparse

from src.ingestion.pipeline import IngestionPipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest documents into Pinecone")
    parser.add_argument("--source", required=True, help="Path to file")
    parser.add_argument("--type", required=True, choices=["csv", "pdf"], help="Source type")
    parser.add_argument("--chunk-size", type=int, default=None)
    parser.add_argument("--chunk-overlap", type=int, default=None)
    args = parser.parse_args()

    pipeline = IngestionPipeline()
    if args.type == "csv":
        stats = pipeline.ingest_csv(
            args.source,
            chunk_size=args.chunk_size or 800,
            chunk_overlap=args.chunk_overlap or 120,
        )
    else:
        stats = pipeline.ingest_pdf(
            args.source,
            chunk_size=args.chunk_size or 1000,
            chunk_overlap=args.chunk_overlap or 200,
        )
    print(f"Ingestion complete: sources={stats.sources}, chunks={stats.chunks}")


if __name__ == "__main__":
    main()

