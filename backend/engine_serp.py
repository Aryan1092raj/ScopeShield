# ScopeShield SerpApi engine — live rate grounding with 24h cache + fallback
from __future__ import annotations

import re
import time

FALLBACK_RATES = {
    "frontend": 55.0,
    "backend": 70.0,
    "devops": 85.0,
    "design": 50.0,
    "compliance": 90.0,
    "database": 75.0,
}

_RATE_RE = re.compile(r"\$(\d{2,3})(?:\s*[–-]\s*\$?(\d{2,3}))?\s*(?:/|per\s+)?h", re.IGNORECASE)
_cache: dict[str, tuple[float, float]] = {}  # key -> (rate, expiry_ts)


def _cached(key: str) -> float | None:
    hit = _cache.get(key)
    if hit and hit[1] > time.time():
        return hit[0]
    return None


def _put(key: str, rate: float, ttl_s: int = 86400) -> None:
    _cache[key] = (rate, time.time() + ttl_s)


def _parse_rate(snippets: list[str], fallback: float) -> float:
    found: list[float] = []
    for s in snippets:
        for m in _RATE_RE.finditer(s):
            lo = float(m.group(1))
            hi = float(m.group(2)) if m.group(2) else lo
            found.append((lo + hi) / 2)
    if not found:
        return fallback
    found.sort()
    return round(found[len(found) // 2], 2)


def fetch_market_rate(task_category: str, api_key: str = "", region: str = "United States") -> tuple[float, str]:
    """Return (hourly_rate_usd, source). Source is serpapi | cache | fallback."""
    cat = task_category.lower()
    fallback = FALLBACK_RATES.get(cat, 65.0)
    key = f"rate:{cat}:{region}"
    hit = _cached(key)
    if hit is not None:
        return hit, "cache"
    if not api_key:
        return fallback, "fallback"
    try:
        from serpapi import GoogleSearch  # type: ignore

        res = GoogleSearch({"q": f"freelance {cat} developer hourly rate 2026 {region}", "api_key": api_key}).get_dict()
        snippets = [r.get("snippet", "") for r in res.get("organic_results", [])[:5]]
        rate = _parse_rate(snippets, fallback)
        _put(key, rate)
        return rate, "serpapi"
    except Exception:
        return fallback, "fallback"
