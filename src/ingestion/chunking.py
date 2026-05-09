from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Chunk:
    chunk_id: str
    text: str
    metadata: dict


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

