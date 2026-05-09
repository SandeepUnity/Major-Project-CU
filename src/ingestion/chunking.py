from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Chunk:
    chunk_id: str
    text: str
    metadata: dict


def chunk_text(text: str, *, source_id: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[Chunk]:
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except Exception as e:  # pragma: no cover
        raise RuntimeError("langchain-text-splitters not installed") from e

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = splitter.create_documents([text])
    out: list[Chunk] = []
    for idx, d in enumerate(docs):
        cid = f"{source_id}::chunk_{idx}"
        out.append(
            Chunk(
                chunk_id=cid,
                text=d.page_content,
                metadata={"source_id": source_id, "chunk_index": idx, "chunk_size": chunk_size, "text": d.page_content},
            )
        )
    return out

