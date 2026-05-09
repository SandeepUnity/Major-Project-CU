from __future__ import annotations

from dataclasses import dataclass

from openai import OpenAI

from src.config.settings import settings


@dataclass
class RetrievedChunk:
    id: str
    score: float
    text: str
    metadata: dict


class OpenAIEmbedder:
    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        self._client = OpenAI(api_key=settings.openai_api_key)

    def embed(self, text: str) -> list[float]:
        resp = self._client.embeddings.create(model=settings.openai_embedding_model, input=text)
        return list(resp.data[0].embedding)


class PineconeVectorStore:
    def __init__(self) -> None:
        if not settings.pinecone_api_key:
            raise RuntimeError("PINECONE_API_KEY not set")
        try:
            from pinecone import Pinecone  # type: ignore
        except Exception as e:  # pragma: no cover
            raise RuntimeError("pinecone package not installed") from e

        pc = Pinecone(api_key=settings.pinecone_api_key)
        self._index = pc.Index(settings.pinecone_index_name)

    def upsert(self, vectors: list[tuple[str, list[float], dict]]) -> None:
        # vectors: (id, embedding, metadata)
        items = [{"id": vid, "values": values, "metadata": metadata} for (vid, values, metadata) in vectors]
        self._index.upsert(vectors=items, namespace=settings.pinecone_namespace)

    def query(self, embedding: list[float], top_k: int) -> list[RetrievedChunk]:
        res = self._index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True,
            namespace=settings.pinecone_namespace,
        )
        out: list[RetrievedChunk] = []
        matches = getattr(res, "matches", []) or []
        for m in matches:
            meta = dict(getattr(m, "metadata", {}) or {})
            text = str(meta.get("text", ""))
            out.append(RetrievedChunk(id=str(m.id), score=float(m.score), text=text, metadata=meta))
        return out

