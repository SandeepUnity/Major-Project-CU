from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PDFPage:
    page_number: int
    text: str


def load_pdf(path: str) -> list[PDFPage]:
    try:
        import pdfplumber
    except Exception as e:  # pragma: no cover
        raise RuntimeError("pdfplumber not installed") from e

    pages: list[PDFPage] = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = (page.extract_text() or "").strip()
            if text:
                pages.append(PDFPage(page_number=i, text=text))
    return pages

