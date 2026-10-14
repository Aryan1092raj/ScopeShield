"""ScopeShield tests — offline, no keys needed (stub paths)."""
import pytest
from fastapi.testclient import TestClient

from backend import audit_service, sow_parser
from backend.engine_tabpfn import load_csv_rows
from backend.main import app

client = TestClient(app)


def test_sow_chunks_fourteen_sections():
    text = open("data/demo_sow_contract.md", encoding="utf-8").read()
    clauses = sow_parser.chunk_sow_markdown(text)
    assert len(clauses) >= 12
    assert any(c["is_exclusion_clause"] for c in clauses)


def test_demo_csv_has_four_leaks():
    rows = load_csv_rows("data/demo_weekly_git_jira.csv")
    assert len(rows) == 12
    assert sum(1 for r in rows if r["unplanned_flag"] == "1") == 3


@pytest.mark.asyncio
async def test_audit_flags_out_of_scope():
    text = open("data/demo_sow_contract.md", encoding="utf-8").read()
    clauses = sow_parser.chunk_sow_markdown(text)
    rows = load_csv_rows("data/demo_weekly_git_jira.csv")
    result = await audit_service.run_audit("BrightKart Website", "BrightKart Retail", clauses, rows)
    oos = [i for i in result["items"] if i["verdict"] == "OUT_OF_SCOPE"]
    assert len(oos) == 4, f"expected 4 OUT_OF_SCOPE, got {len(oos)}"
    assert result["total_recoverable_revenue_usd"] == 1845.0
    assert "Change Order" in result["change_order_markdown"]


def test_health_ok():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["gemma_model"] == "gemma-2-9b-tinker-sow-v1"


def test_demo_audit_endpoint():
    r = client.get("/api/demo/audit")
    assert r.status_code == 200
    body = r.json()
    assert body["out_of_scope_hours"] == 26.0
    assert len(body["items"]) == 12


def test_project_flow_upload_then_audit():
    pid = client.post("/api/projects", data={"project_name": "X", "client_name": "Y", "contracted_hourly_rate": "60"}).json()["project_id"]
    # audit before SOW must 400
    with open("data/demo_weekly_git_jira.csv", "rb") as f:
        assert client.post(f"/api/projects/{pid}/audit", files={"file": ("w.csv", f, "text/csv")}).status_code == 400
    with open("data/demo_sow_contract.md", "rb") as f:
        sow = client.post(f"/api/projects/{pid}/sow", files={"file": ("sow.md", f, "text/markdown")}).json()
    assert sow["clauses_indexed"] >= 12
    with open("data/demo_weekly_git_jira.csv", "rb") as f:
        aud = client.post(f"/api/projects/{pid}/audit", files={"file": ("w.csv", f, "text/csv")})
    assert aud.status_code == 200
    assert aud.json()["total_recoverable_revenue_usd"] == 1845.0


def test_unknown_project_404():
    r = client.post("/api/projects/nope/audit", files={"file": ("w.csv", b"a,b\n1,2", "text/csv")})
    assert r.status_code == 404


def test_bad_csv_missing_columns_400():
    pid = client.post("/api/projects", data={"project_name": "X", "client_name": "Y", "contracted_hourly_rate": "60"}).json()["project_id"]
    with open("data/demo_sow_contract.md", "rb") as f:
        client.post(f"/api/projects/{pid}/sow", files={"file": ("sow.md", f, "text/markdown")})
    r = client.post(f"/api/projects/{pid}/audit", files={"file": ("bad.csv", b"ticket_id,task_title\n1,hi", "text/csv")})
    assert r.status_code == 400
    assert "missing columns" in r.json()["detail"]


def test_empty_sow_rejected_400():
    pid = client.post("/api/projects", data={"project_name": "X", "client_name": "Y", "contracted_hourly_rate": "60"}).json()["project_id"]
    r = client.post(f"/api/projects/{pid}/sow", files={"file": ("empty.md", b"   ", "text/markdown")})
    assert r.status_code == 400


