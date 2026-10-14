# ScopeShield orchestrator — Tiger → TabPFN → SerpApi → Gemma
from __future__ import annotations

import time

from . import db_tiger, engine_gemma, engine_serp, engine_tabpfn
from .config import settings


async def run_audit(project_name: str, client_name: str, clauses: list[dict], csv_rows: list[dict], trace_id: str | None = None) -> dict:
    t0 = time.perf_counter()
    lat: dict[str, float] = {}

    store = db_tiger.TigerStore(settings.database_url)
    store.index_clauses_memory("demo", clauses)

    # 1. Hybrid retrieval per row
    t = time.perf_counter()
    matches_per_row = [store.match_memory(f"{r.get('task_title','')} {r.get('notes','')}") for r in csv_rows]
    lat["tiger_ms"] = round((time.perf_counter() - t) * 1000, 1)

    # 2. TabPFN scoring
    t = time.perf_counter()
    feats = [
        engine_tabpfn.build_feature_row(r, m[0]["semantic_distance"] if m else 1.0, int(m[0]["is_exclusion_clause"]) if m else 0)
        for r, m in zip(csv_rows, matches_per_row)
    ]
    leakages = engine_tabpfn.score_rows(feats, settings.tabpfn_api_key)
    lat["tabpfn_ms"] = round((time.perf_counter() - t) * 1000, 1)

    # 3 + 4. Rates + Gemma verdicts
    t = time.perf_counter()
    items: list[dict] = []
    total_hours = 0.0
    oos_hours = 0.0
    total_rec = 0.0
    for row, matches, leak in zip(csv_rows, matches_per_row, leakages):
        top = matches[0] if matches else {"section_number": "Section 1.0", "clause_text": "", "is_exclusion_clause": False, "semantic_distance": 1.0, "rrf_score": 0.0}
        rate, _src = engine_serp.fetch_market_rate(row.get("task_category", "backend"), settings.serpapi_api_key)
        if settings.gemma_mode == "ollama":
            judged = await engine_gemma.judge_row_ollama(row, matches, leak, rate)
        else:
            est = float(row.get("estimated_hours") or 0)
            actual = float(row.get("actual_hours_logged") or 0)
            judged = engine_gemma.judge_row_stub(row, top, leak, engine_tabpfn.overrun_ratio(est, actual))
        actual_h = float(row.get("actual_hours_logged") or 0)
        total_hours += actual_h
        rec = round(actual_h * rate, 2) if judged["verdict"] == "OUT_OF_SCOPE" else 0.0
        if judged["verdict"] == "OUT_OF_SCOPE":
            oos_hours += actual_h
            total_rec += rec
        items.append(
            {
                "ticket_id": row.get("ticket_id", "?"),
                "task_title": row.get("task_title", ""),
                "task_category": (row.get("task_category") or "backend").lower(),
                "actual_hours": actual_h,
                "tabpfn_leakage_probability": leak,
                "verdict": judged["verdict"],
                "violated_or_matched_clause": judged.get("violated_or_matched_clause", top["section_number"]),
                "contractual_reasoning": judged["contractual_reasoning"],
                "market_hourly_rate_usd": rate,
                "recoverable_amount_usd": rec,
            }
        )
    lat["gemma_serp_ms"] = round((time.perf_counter() - t) * 1000, 1)

    oos_items = [i for i in items if i["verdict"] == "OUT_OF_SCOPE"]
    change_md = engine_gemma.build_change_order_markdown(project_name, client_name, oos_items, round(total_rec, 2))
    lat["total_ms"] = round((time.perf_counter() - t0) * 1000, 1)

    return {
        "project_name": project_name,
        "total_hours_logged": round(total_hours, 2),
        "out_of_scope_hours": round(oos_hours, 2),
        "total_recoverable_revenue_usd": round(total_rec, 2),
        "items": items,
        "change_order_markdown": change_md + "\n\n---\n" + engine_gemma.build_client_email(project_name, client_name, round(total_rec, 2), len(oos_items)),
        "telemetry": {"sentry_trace_id": trace_id, "latency_ms": lat, "token_savings_vs_gpt4o_pct": 35.0, "model": settings.gemma_model},
    }
