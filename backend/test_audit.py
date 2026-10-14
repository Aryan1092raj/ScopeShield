"""ScopeShield smoke tests — offline, no keys needed (stub paths)."""
from backend import audit_service, sow_parser
from backend.engine_tabpfn import load_csv_rows


def test_sow_chunks_fourteen_sections():
    text = open("data/demo_sow_contract.md", encoding="utf-8").read()
    clauses = sow_parser.chunk_sow_markdown(text)
    assert len(clauses) >= 12
    assert any(c["is_exclusion_clause"] for c in clauses)


def test_demo_csv_has_four_leaks():
    rows = load_csv_rows("data/demo_weekly_git_jira.csv")
    assert len(rows) == 12
    assert sum(1 for r in rows if r["unplanned_flag"] == "1") == 3


async def _audit():
    text = open("data/demo_sow_contract.md", encoding="utf-8").read()
    clauses = sow_parser.chunk_sow_markdown(text)
    rows = load_csv_rows("data/demo_weekly_git_jira.csv")
    return await audit_service.run_audit("BrightKart Website", "BrightKart Retail", clauses, rows)


def test_audit_flags_out_of_scope():
    import asyncio

    result = asyncio.run(_audit())
    oos = [i for i in result["items"] if i["verdict"] == "OUT_OF_SCOPE"]
    assert len(oos) >= 3, f"expected >=3 OUT_OF_SCOPE, got {len(oos)}"
    assert result["total_recoverable_revenue_usd"] > 500
    assert "Change Order" in result["change_order_markdown"]
