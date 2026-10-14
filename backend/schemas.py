# ScopeShield Pydantic v2 contracts — mirrors README §7.4
from __future__ import annotations

from typing import List, Literal, Optional
from pydantic import BaseModel, Field

Verdict = Literal["IN_SCOPE", "GREY_AREA", "OUT_OF_SCOPE"]


class SOWClauseMatch(BaseModel):
    section_number: str
    clause_text: str
    semantic_distance: float = Field(ge=0.0, le=2.0)
    rrf_score: float = Field(ge=0.0)


class AuditedWorkItem(BaseModel):
    ticket_id: str
    task_title: str
    task_category: str = "backend"
    actual_hours: float = Field(ge=0.0)
    tabpfn_leakage_probability: float = Field(ge=0.0, le=1.0)
    verdict: Verdict
    violated_or_matched_clause: str
    contractual_reasoning: str
    market_hourly_rate_usd: float = Field(ge=0.0)
    recoverable_amount_usd: float = Field(ge=0.0)


class AuditReportResponse(BaseModel):
    project_name: str
    total_hours_logged: float
    out_of_scope_hours: float
    total_recoverable_revenue_usd: float
    items: List[AuditedWorkItem]
    change_order_markdown: str
    telemetry: dict


class ProjectCreate(BaseModel):
    project_name: str = Field(min_length=2, max_length=120)
    client_name: str = Field(min_length=2, max_length=120)
    contracted_hourly_rate: float = Field(gt=0, le=1000)


class ProjectOut(ProjectCreate):
    project_id: str


class HealthOut(BaseModel):
    ok: bool = True
    tiger_ok: bool = False
    tabpfn_ok: bool = False
    gemma_model: str = "gemma-2-9b-tinker-sow-v1"
    serp_ok: bool = False


class AuditTelemetry(BaseModel):
    sentry_trace_id: Optional[str] = None
    latency_ms: dict = Field(default_factory=dict)
    token_savings_vs_gpt4o_pct: float = 35.0
    model: str = "gemma-2-9b-tinker-sow-v1"
