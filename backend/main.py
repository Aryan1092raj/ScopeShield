# ScopeShield FastAPI — Sentry-traced audit endpoints + 1-click demo
from __future__ import annotations

import csv
import io
import uuid
from pathlib import Path

import sentry_sdk
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sentry_sdk.integrations.fastapi import FastApiIntegration

from . import audit_service, sow_parser
from .config import settings
from .schemas import AuditReportResponse, HealthOut

DATA = Path(__file__).resolve().parent.parent / "data"

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=settings.traces_sample_rate,
        integrations=[FastApiIntegration()],
        ai_monitoring=True,
    )

app = FastAPI(title="ScopeShield", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "https://scopeshield.tech"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_projects: dict[str, dict] = {}


@app.get("/api/health", response_model=HealthOut)
async def health() -> HealthOut:
    return HealthOut(
        tiger_ok=bool(settings.database_url),
        tabpfn_ok=bool(settings.tabpfn_api_key),
        gemma_model=settings.gemma_model,
        serp_ok=bool(settings.serpapi_api_key),
    )


@app.post("/api/projects")
async def create_project(project_name: str = Form(...), client_name: str = Form(...), contracted_hourly_rate: float = Form(...)):
    pid = str(uuid.uuid4())
    _projects[pid] = {"project_name": project_name, "client_name": client_name, "rate": contracted_hourly_rate, "clauses": []}
    return {"project_id": pid, **_projects[pid], "clauses": []}


def _parse_csv_bytes(raw: bytes) -> list[dict]:
    try:
        return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    except Exception as e:
        raise HTTPException(400, f"CSV parse failed: {e}")


@app.post("/api/projects/{project_id}/sow")
async def upload_sow(project_id: str, file: UploadFile = File(...)):
    proj = _projects.get(project_id)
    if not proj:
        raise HTTPException(404, "project not found")
    raw = await file.read()
    text = raw.decode("utf-8", errors="ignore") if file.filename.endswith(".md") else raw.decode("utf-8", errors="ignore")
    if file.filename.lower().endswith(".pdf"):
        # PDFs need temp-file path for pypdf
        tmp = Path(f"/tmp/{uuid.uuid4()}.pdf")
        tmp.write_bytes(raw)
        text = sow_parser.load_sow_file(str(tmp))
    clauses = sow_parser.chunk_sow_markdown(text)
    proj["clauses"] = clauses
    return {"clauses_indexed": len(clauses), "sections": [c["section_number"] for c in clauses]}


@app.post("/api/projects/{project_id}/audit", response_model=AuditReportResponse)
async def audit_project(project_id: str, file: UploadFile = File(...)):
    proj = _projects.get(project_id)
    if not proj:
        raise HTTPException(404, "project not found")
    if not proj["clauses"]:
        raise HTTPException(400, "upload SOW first")
    rows = _parse_csv_bytes(await file.read())
    with sentry_sdk.start_transaction(op="ai.agent.audit", name="ScopeShield_Full_Audit") as txn:
        with sentry_sdk.start_span(op="db.vector.hybrid_rrf", description="Tiger Hybrid Retrieval"):
            pass  # real spans live inside audit_service; kept flat for trace clarity
        result = await audit_service.run_audit(proj["project_name"], proj["client_name"], proj["clauses"], rows, trace_id=txn.trace_id if txn else None)
    return JSONResponse(result)


@app.get("/api/demo/audit", response_model=AuditReportResponse)
async def demo_audit():
    """1-click judge path — no upload, uses bundled demo SOW + CSV."""
    sow_text = (DATA / "demo_sow_contract.md").read_text(encoding="utf-8")
    clauses = sow_parser.chunk_sow_markdown(sow_text)
    with open(DATA / "demo_weekly_git_jira.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with sentry_sdk.start_transaction(op="ai.agent.audit", name="ScopeShield_Demo_Audit") as txn:
        result = await audit_service.run_audit("BrightKart Website", "BrightKart Retail", clauses, rows, trace_id=txn.trace_id if txn else None)
    return JSONResponse(result)
