# ScopeShield FastAPI — Sentry-traced audit endpoints + 1-click demo
from __future__ import annotations

import csv
import io
import uuid
from contextlib import nullcontext
from pathlib import Path

import sentry_sdk
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

try:
    from sentry_sdk.integrations.fastapi import FastApiIntegration
except ImportError:  # older sentry-sdk without fastapi extra
    FastApiIntegration = None  # type: ignore

from . import audit_service, sow_parser
from .config import settings
from .schemas import AuditReportResponse, HealthOut

DATA = Path(__file__).resolve().parent.parent / "data"

if settings.sentry_dsn:
    kwargs: dict = dict(dsn=settings.sentry_dsn, traces_sample_rate=settings.traces_sample_rate)
    if FastApiIntegration is not None:
        kwargs["integrations"] = [FastApiIntegration()]
    try:
        sentry_sdk.init(**kwargs)
    except TypeError:
        # ai_monitoring flag only on newer SDKs — core tracing still works
        sentry_sdk.init(**kwargs)


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


def _safe_filename(name: str | None, fallback_ext: str) -> str:
    if not name:
        return f"upload{fallback_ext}"
    return name


def _trace(name: str):
    """Sentry transaction that degrades to no-op locally (no DSN)."""
    try:
        return sentry_sdk.start_transaction(op="ai.agent.audit", name=name)
    except Exception:
        return nullcontext(None)


def _span(op: str, description: str):
    try:
        return sentry_sdk.start_span(op=op, name=description)
    except Exception:
        return nullcontext(None)


@app.post("/api/projects/{project_id}/sow")
async def upload_sow(project_id: str, file: UploadFile = File(...)):
    proj = _projects.get(project_id)
    if not proj:
        raise HTTPException(404, "project not found")
    fname = _safe_filename(file.filename, ".md")
    raw = await file.read()
    if not raw.strip():
        raise HTTPException(400, "empty file — upload a real SOW")
    if fname.lower().endswith(".pdf"):
        # PDFs need temp-file path for pypdf
        tmp = Path(f"/tmp/{uuid.uuid4()}.pdf")
        tmp.write_bytes(raw)
        try:
            text = sow_parser.load_sow_file(str(tmp))
        finally:
            tmp.unlink(missing_ok=True)
    else:
        text = raw.decode("utf-8", errors="ignore")
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
    try:
        from .engine_tabpfn import validate_csv_rows

        validate_csv_rows(rows)
    except ValueError as e:
        raise HTTPException(400, str(e))
    with _trace("ScopeShield_Full_Audit") as txn:
        with _span("db.vector.hybrid_rrf", "Tiger Hybrid Retrieval"):
            pass  # real spans live inside audit_service; kept flat for trace clarity
        trace_id = getattr(txn, "trace_id", None)
        result = await audit_service.run_audit(proj["project_name"], proj["client_name"], proj["clauses"], rows, trace_id=trace_id)
    return JSONResponse(result)


@app.get("/api/demo/audit", response_model=AuditReportResponse)
async def demo_audit():
    """1-click judge path — no upload, uses bundled demo SOW + CSV."""
    sow_text = (DATA / "demo_sow_contract.md").read_text(encoding="utf-8")
    clauses = sow_parser.chunk_sow_markdown(sow_text)
    with open(DATA / "demo_weekly_git_jira.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with _trace("ScopeShield_Demo_Audit") as txn:
        trace_id = getattr(txn, "trace_id", None)
        result = await audit_service.run_audit("BrightKart Website", "BrightKart Retail", clauses, rows, trace_id=trace_id)
    return JSONResponse(result)
