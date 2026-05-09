from __future__ import annotations

from dataclasses import dataclass

from src.core.vector_store import OpenAIEmbedder, PineconeVectorStore
from src.ingestion.chunking import Chunk, chunk_text
from src.ingestion.csv_parser import load_faq_csv
from src.ingestion.pdf_parser import load_pdf


@dataclass
class IngestionStats:
    sources: int
    chunks: int


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

