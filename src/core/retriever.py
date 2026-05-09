from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.config.settings import settings
from src.core.vector_store import OpenAIEmbedder, PineconeVectorStore, RetrievedChunk


@dataclass
class RetrievalResult:
    chunks: list[RetrievedChunk]
    confidence: Optional[float]


class Retriever:
    def __init__(self) -> None:
        self._embedder: Optional[OpenAIEmbedder] = None
        self._store: Optional[PineconeVectorStore] = None

    def retrieve(self, query: str, top_k: Optional[int] = None) -> RetrievalResult:
        top_k = top_k or settings.retrieval_top_k
        try:
            if self._embedder is None:
                self._embedder = OpenAIEmbedder()
            if self._store is None:
                self._store = PineconeVectorStore()
        except Exception:
            return RetrievalResult(chunks=[], confidence=None)

        emb = self._embedder.embed(query)
        chunks = self._store.query(embedding=emb, top_k=top_k)
        conf = max((c.score for c in chunks), default=0.0) if chunks else 0.0
        return RetrievalResult(chunks=chunks, confidence=float(conf))

