# ScopeShield SOW chunker — splits Markdown/PDF text on Section headings
from __future__ import annotations

import hashlib
import re

SECTION_RE = re.compile(r"^#?\s*Section\s+(\d+(?:\.\d+)*)\s*:\s*(.+)$", re.IGNORECASE | re.MULTILINE)
EXCLUSION_HINTS = ("out of scope", "exclusion", "excluded", "expressly excluded", "not included", "require a separate change order")


def chunk_sow_markdown(md_text: str) -> list[dict]:
    """Split SOW markdown into clause dicts with exclusion flags."""
    matches = list(SECTION_RE.finditer(md_text))
    clauses: list[dict] = []
    if not matches:
        # Fallback: whole doc as one clause
        return [{"section_number": "Section 1.0", "clause_text": md_text.strip()[:4000], "is_exclusion_clause": _is_exclusion(md_text)}]
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md_text)
        body = md_text[start:end].strip()
        sec = f"Section {m.group(1)}: {m.group(2).strip()}"
        clauses.append({"section_number": sec, "clause_text": body[:4000], "is_exclusion_clause": _is_exclusion(body)})
    return clauses


def _is_exclusion(text: str) -> bool:
    low = text.lower()
    return any(h in low for h in EXCLUSION_HINTS)


def load_sow_file(path: str) -> str:
    """Load .md as text, .pdf via pypdf. Keeps raw text in-memory only."""
    if path.lower().endswith(".pdf"):
        from pypdf import PdfReader

        reader = PdfReader(path)
        return "\n".join((p.extract_text() or "") for p in reader.pages)
    with open(path, encoding="utf-8") as f:
        return f.read()


def clause_hash(section: str, text: str) -> str:
    return hashlib.sha256(f"{section}|{text}".encode()).hexdigest()[:16]
