# ScopeShield Tiger engine — hybrid RRF with graceful in-memory fallback
# Uses Postgres match_sow_clauses_hybrid() when DATABASE_URL set,
# else keyword-overlap fallback so demo works with zero infra.
from __future__ import annotations

import hashlib
import math
import re
from typing import Any

_WORD = re.compile(r"[a-z0-9]+")


def _tokens(s: str) -> set[str]:
    return set(_WORD.findall(s.lower()))


def _pseudo_embedding(text: str, dim: int = 64) -> list[float]:
    """Deterministic hash-bucket embedding for local fallback (NOT for prod)."""
    vec = [0.0] * dim
    for tok in _tokens(text):
        h = int(hashlib.sha256(tok.encode()).hexdigest(), 16)
        vec[h % dim] += 1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def cosine_distance(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    dot = max(-1.0, min(1.0, dot))
    return round(1.0 - dot, 4)


class TigerStore:
    """Thin wrapper: real Tiger when configured, memory store otherwise."""

    def __init__(self, database_url: str = "") -> None:
        self.database_url = database_url
        self._pool: Any = None
        self._memory: list[dict] = []

    async def connect(self) -> None:
        if not self.database_url:
            return
        import asyncpg

        self._pool = await asyncpg.create_pool(self.database_url, min_size=1, max_size=5)

    def index_clauses_memory(self, project_id: str, clauses: list[dict]) -> int:
        self._memory = [
            {
                "project_id": project_id,
                "section_number": c["section_number"],
                "clause_text": c["clause_text"],
                "is_exclusion_clause": c.get("is_exclusion_clause", False),
                "embedding": _pseudo_embedding(c["section_number"] + " " + c["clause_text"]),
            }
            for c in clauses
        ]
        return len(self._memory)

    def match_memory(self, query_text: str, limit: int = 3) -> list[dict]:
        """RRF-ish fusion: keyword overlap rank + pseudo-cosine rank."""
        q_emb = _pseudo_embedding(query_text)
        q_tok = _tokens(query_text)
        scored = []
        for c in self._memory:
            kw = len(q_tok & _tokens(c["clause_text"])) / max(1, len(q_tok))
            dist = cosine_distance(q_emb, c["embedding"])
            scored.append((c, kw, dist))
        # Rank by keyword desc, distance asc → RRF fuse
        by_kw = sorted(scored, key=lambda t: t[1], reverse=True)
        by_vec = sorted(scored, key=lambda t: t[2])
        rank_kw = {id(t[0]): i + 1 for i, t in enumerate(by_kw)}
        rank_vec = {id(t[0]): i + 1 for i, t in enumerate(by_vec)}
        fused = []
        for c, kw, dist in scored:
            rrf = 1.0 / (60 + rank_kw[id(c)]) + 1.0 / (60 + rank_vec[id(c)])
            fused.append(
                {
                    "section_number": c["section_number"],
                    "clause_text": c["clause_text"],
                    "is_exclusion_clause": c["is_exclusion_clause"],
                    "semantic_distance": dist,
                    "rrf_score": round(rrf, 5),
                }
            )
        return sorted(fused, key=lambda d: d["rrf_score"], reverse=True)[:limit]

    async def match_tiger(self, project_id: str, query_text: str, query_embedding: list[float], limit: int = 3) -> list[dict]:
        """Call the SQL RRF function from README §7.1 on real Tiger Data."""
        assert self._pool is not None, "Tiger pool not connected"
        rows = await self._pool.fetch(
            "SELECT * FROM match_sow_clauses_hybrid($1, $2, $3::vector, $4)",
            project_id,
            query_text,
            str(query_embedding),
            limit,
        )
        return [dict(r) for r in rows]
