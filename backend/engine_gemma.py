# ScopeShield Gemma engine — strict-JSON scope judge with stub + Ollama paths
# Stub = deterministic rule-based judge so demo/tests run with no GPU.
# Ollama path = real Gemma-2-9B (+ Tinker LoRA) when GEMMA_MODE=ollama.
from __future__ import annotations

import json
import re

import httpx

from .config import settings


def classify_stub(leakage: float, matched_exclusion: bool, overrun: float, revisions: int) -> tuple[str, str]:
    if matched_exclusion or leakage >= 0.65:
        return "OUT_OF_SCOPE", "Top SOW clause is an exclusion or leakage exceeds 0.65 threshold."
    if leakage >= 0.35 or revisions > 3 or overrun > 1.5:
        return "GREY_AREA", "Signals conflict — needs client clarification before billing."
    return "IN_SCOPE", "Work matches an in-scope deliverable within revision policy."


def judge_row_stub(ticket: dict, clause: dict, leakage: float, overrun: float) -> dict:
    matched_excl = bool(clause.get("is_exclusion_clause"))
    verdict, reasoning = classify_stub(leakage, matched_excl, overrun, int(ticket.get("client_revision_rounds") or 0))
    return {"verdict": verdict, "contractual_reasoning": f"{reasoning} Cited {clause.get('section_number')}: “{clause.get('clause_text','')[:160]}…”"}


async def judge_row_ollama(ticket: dict, clauses: list[dict], leakage: float, rate: float) -> dict:
    """Call local Ollama Gemma with strict-JSON instruction + repair retry."""
    top = clauses[0] if clauses else {"section_number": "Section 1.0", "clause_text": "No clause found"}
    prompt = (
        "Output ONLY valid JSON with keys verdict (IN_SCOPE|GREY_AREA|OUT_OF_SCOPE), "
        "violated_or_matched_clause, contractual_reasoning. No preamble.\n"
        f"Ticket: {ticket.get('ticket_id')} {ticket.get('task_title')} "
        f"({ticket.get('actual_hours_logged')}h, leakage {leakage}, rate ${rate}/h).\n"
        f"Clauses: {json.dumps(clauses[:3])}\nJSON:"
    )
    async with httpx.AsyncClient(timeout=60) as client:
        last = ""
        for _ in range(2):
            r = await client.post(
                f"{settings.ollama_host}/api/generate",
                json={"model": settings.base_gemma_model, "prompt": prompt, "stream": False, "format": "json"},
            )
            r.raise_for_status()
            last = r.json().get("response", "{}")
            try:
                data = json.loads(last)
                v = data.get("verdict")
                if v in ("IN_SCOPE", "GREY_AREA", "OUT_OF_SCOPE"):
                    return {
                        "verdict": v,
                        "contractual_reasoning": data.get("contractual_reasoning", f"Cited {top['section_number']}."),
                        "violated_or_matched_clause": data.get("violated_or_matched_clause", top["section_number"]),
                    }
            except json.JSONDecodeError:
                prompt += "\nReturn ONLY the JSON object."
        # Repair fallback: extract verdict token, else stub
        m = re.search(r"OUT_OF_SCOPE|GREY_AREA|IN_SCOPE", last)
        v = m.group(0) if m else classify_stub(leakage, bool(top.get("is_exclusion_clause")), 1.0, 0)[0]
        return {"verdict": v, "contractual_reasoning": f"Cited {top['section_number']} (repaired).", "violated_or_matched_clause": top["section_number"]}


def build_change_order_markdown(project: str, client: str, items: list[dict], total: float) -> str:
    lines = [f"# Change Order — {project}", f"**Client:** {client}", "", "## Out-of-scope items", ""]
    for it in items:
        lines.append(f"- **{it['ticket_id']}** {it['task_title']} — {it['actual_hours']}h × ${it['market_hourly_rate_usd']}/h = **${it['recoverable_amount_usd']:.2f}**")
        lines.append(f"  - {it['verdict']} · {it['violated_or_matched_clause']}")
    lines += ["", f"**Total recoverable:** ${total:.2f}", "", "Please reply approved to proceed. Net-15 per SOW §4.1."]
    return "\n".join(lines)


def build_client_email(project: str, client: str, total: float, count: int) -> str:
    return (
        f"Subject: Quick change order for {project} — {count} items (${total:.2f})\n\n"
        f"Hi {client} team,\n\nAudited last week against our SOW and found {count} items outside scope "
        f"(${total:.2f} at current market rates, clause-cited in the attached order). "
        "Nothing confrontational — just want us aligned before the next sprint.\n\n"
        "Could you approve so we stay on schedule? Happy to trim or defer anything.\n\nThanks!\n"
    )
