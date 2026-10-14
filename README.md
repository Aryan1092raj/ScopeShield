# 🛡️ ScopeShield — NDA-Safe Scope-Creep Auditor

> **Tagline:** Stop working for free. Turn SOWs + work-logs into paid change orders.
> **Domain:** `scopeshield.tech` (Render Static + FastAPI backend)
> **Theme fit:** DEV Side Hustle — open-source AI at its core that someone would pay $19/mo for.

[![Stack](https://img.shields.io/badge/stack-React%2019%20%7C%20FastAPI%20%7C%20TigerData-blue)]()
[![Open AI](https://img.shields.io/badge/open--AI-Gemma%20%2B%20Tinker%20%2B%20TabPFN-green)]()
[![License](https://img.shields.io/badge/license-MIT-lightgrey)]()

## 1. Why the name ScopeShield?

I needed a name that a freelancer would remember, trust, and put on an invoice.

- **Scope** = the exact pain — "is this in scope or not?"
- **Shield** = the promise — legal + financial protection, NDA-safe, non-confrontational.
- Alternatives I rejected: `Billable` (too generic), `CreepHunter` (sounds negative to clients), `ChangeOrderly` (hard to spell), `SOWLens` (too legal-jargony).
- **ScopeShield** wins because it's 2 syllables + 1 syllable, `.tech`-brandable, logo-friendly (🛡️), and explains itself in a demo: *"it shields your scope."*

Full product name for prizes / DEV post: **ScopeShield: NDA-Safe Freelance & Boutique Agency Scope-Creep Auditor and Change-Order Engine.**

## 2. One-line pitch

Upload a signed SOW PDF + weekly CSV (Jira / Linear / GitHub / Toggl) → get a line-by-line audit ledger (IN_SCOPE / GREY_AREA / OUT_OF_SCOPE with clause citations) + recoverable revenue + one-click client-ready change order grounded in live market rates — all without leaking NDA data to closed APIs.

## 3. Why this wins a 4.5-day hackathon

Generic wrappers lose. ScopeShield gives every sponsor tech a non-overlapping mathematical job:

| Sponsor | Job in ScopeShield | Why not a wrapper trick |
|---|---|---|
| **Tiger Data (pgvector + tsvector)** | Hybrid semantic + exact-clause retrieval over SOW | Judges see real RRF SQL, not just `pgvector` import |
| **TabPFN-3.5** | Tabular anomaly + overrun classifier on CSV numbers | LLMs hallucinate math — TabPFN doesn't |
| **Gemma + Tinker** | Local open-weight judge + change-order generator, LoRA-tuned for strict JSON | NDA-safe, $0 marginal cost, measurable F1 gain |
| **SerpApi** | Live freelance rate grounding for pricing | Change orders cite 2026 market data |
| **Render + .tech + Sentry** | Prod hosting, domain, span-level agent tracing | Real waterfall trace screenshot for DEV post |
| **Entire / Copilot** | Build telemetry | Ship faster in 4.5 days |

> Prize-pool coverage: Tiger ($100) + TabPFN ($200) + Gemma ($200) + Tinker ($200) + SerpApi ($100) + Sentry ($100) + Render ($200) + .tech ($100) = **~$1,200 eligibility surface.**

## 4. Problem Statement (ps)

### 4.1 The bleeding nobody invoices

Freelance developers, designers, and 2–10 person boutique agencies lose **15–28% of gross revenue** to unbilled scope creep.

The pattern is always the same:

1. A signed 12–15 page Statement of Work (SOW) says "3 revision rounds, React frontend, no DevOps."
2. Client then asks for "quick tweaks" in Slack, Jira comments, or PR reviews — extra pages, dark mode, SSO, infra fixes.
3. Freelancer does the work to stay likable, logs 150 commits + 60 tickets that week.
4. Cross-referencing those logs against the PDF takes 3–4 hours of admin nobody wants to do.
5. Confronting the client feels awkward → freelancer eats the cost.

One 2-hour out-of-scope ticket at $75/hr = $150 lost. At 8 such tickets/month = **$1,200/mo leakage**. A $19/mo tool that recovers even one ticket pays for 7 months.

### 4.2 Why existing tools fail

- **Harvest / Toggl / Clockify:** track time, but never tell you *if that time was contractually billable*.
- **ChatGPT wrappers:** you paste client contracts into OpenAI/Anthropic — violates most Master Services Agreements (MSAs) that forbid sharing client IP with third-party model vendors without written consent.
- **Jira/Linear reports:** show velocity, not contractual coverage. No clause citation.
- **Manual review:** 150 rows × 15-page PDF = half a day. Nobody does it weekly.

ScopeShield is not another tracker. It's a **post-hoc auditor + change-order engine**: prove what was out-of-scope, price it fairly, and ask for money politely.

### 4.3 Target user — User #1 in 10 minutes

**Primary buyer:** independent technical contractors + micro-agencies billing $40–$150/hr.

- Persona: "Priya, 27, React + Node freelancer in Pune, 3 retainer clients, bills via Razorpay/Stripe, lives in VS Code + Linear."
- Pain today: client #2 asked for "just add admin CSV export + role-based auth" — 11 hours, zero change order.
- Willingness to pay: $19/mo flat. One recovered ticket = 5–8 months ROI.
- Bonus-point path: I can get my *own* past SOW + git log as User #1 today. No need to beg a retail store for 90 days of CSVs. For judges: 1-click demo dataset ships in-repo.

**Secondary:** boutique design/dev shops (2–10 people) who need a non-confrontational paper trail for client finance teams.

### 4.4 Value proposition in 30 seconds

> Drop SOW PDF + weekly CSV → get (1) line-by-line ledger with IN_SCOPE / GREY_AREA / OUT_OF_SCOPE + exact clause quote, (2) revenue recovery summary ($ + hours), (3) copy-paste client email + PDF change order with live market rates.

Non-goals for trust: we never auto-send to clients, never store raw PDFs after embedding (hash + delete option), never call closed APIs with contract text.

### 4.5 Why open-source AI is the business model (not ideology)

This is the structural proof for the DEV "Side Hustle + Open Innovation" prompt:

| Dimension | Closed frontier API (GPT-4o / Claude 3.5) | ScopeShield open stack (Gemma + Tinker + TabPFN) | Why closed fails here |
|---|---|---|---|
| Legal / NDA compliance | Fails. Uploading SOWs, commit messages, Jira logs to third-party servers violates standard MSAs. | Passes. Quantized Gemma runs on laptop / isolated VPC. Zero retention. TabPFN sees only numbers, no text. | Freelancers can't legally use a cloud wrapper without client consent letters. |
| Unit economics at $19/mo | ~62% margin. 2,500 tickets + 40-page SOW/week ≈ 4.5M tokens/mo ≈ $7.20 API + vector DB. Power users kill you. | ~91% margin. $0 marginal token cost after LoRA. Only infra is Tiger Data + Render ($12–18/mo total). | Per-token pricing forces usage caps that kill conversion. |
| Tabular math vs text | Hallucinates arithmetic over 500 CSV rows. | Specialized: TabPFN-3.5 does numeric/categorical classification natively; Gemma does legal text only. Split = 3.4× lower latency, no math hallucination. | Mixing jobs in one LLM = slow + wrong. |
| Customization | Prompt-only. Can't fix "too agreeable, outputs markdown preamble breaks JSON." | Tinker LoRA on 250 contract pairs fixes strict JSON + enforces exclusion clauses. Swap Gemma-2-9B ↔ Gemma-3-4B freely. | Niche legal tone needs weights, not prompts. |
| Offline / laptop demo | Needs internet + key. | Ollama quantized run works on flight Wi-Fi, judge table, client office. | Demos die without this. |

**Bottom line:** open weights keep data off servers you don't control, make $19/mo viable, and let you fine-tune for a niche general APIs handle poorly.

---

## 5. PRD — Product Requirements Document

### 5.1 Goals / Non-goals

**Goals (4.5-day cut):**

- G1: Any freelancer can audit a real week in <30s without OAuth or signup.
- G2: Every verdict cites an exact SOW clause (section + quote) — no black-box "AI says so."
- G3: Every OUT_OF_SCOPE line shows math: hours × market rate = recoverable $.
- G4: One click copies a polite, non-confrontational change-order email + markdown PDF.
- G5: Judges can run full demo with zero uploads via preloaded sample data.

**Non-goals (explicitly cut):**

- No live OAuth (Jira/Slack/GitHub), no Stripe billing, no multi-tenant auth — zero prize points for login screens.
- No auto-sending emails to clients, no e-signature, no invoice generation.
- No multi-project analytics dashboard in v1 — single-project audit only.

### 5.2 Personas + user stories

- **P1 — Solo freelancer (Priya):** "As Priya, I upload my SOW + Linear CSV so I see which 11 hours were unbilled and send a polite change order without sounding greedy."
- **P2 — Micro-agency owner (2–10 people):** "As an owner, I review my team's weekly ledger so I can defend overages to client finance with clause citations."
- **P3 — Hackathon judge:** "As a judge with no CSV handy, I click 'Run Real Agency Audit' and see leakage + email in 20 seconds."

Acceptance: P3 path must work offline from preloaded `demo_*` files with no env keys.

### 5.3 Strict scope boundaries (ship order)

| Priority | Feature | Deadline | Justification |
|---|---|---|---|
| P0 Must ship | SOW ingestion + Tiger hybrid search | Thu night | Core RAG backbone, Tiger $100 |
| P0 Must ship | CSV ingestion + TabPFN overrun classifier | Thu night | Tabular differentiator, TabPFN $200 |
| P0 Must ship | Gemma + Tinker scope judge + generator | Fri noon | Open-AI core, Gemma $200 + Tinker $200 |
| P0 Must ship | SerpApi live rate lookup | Fri afternoon | Real pricing, SerpApi $100 |
| P0 Must ship | Sentry tracing + Render + .tech domain | Fri night | Sentry $100 + Render $200 + .tech $100 |
| P1 Polish | 1-click sample dataset loader | Sat noon | Judges won't have CSVs — critical |
| Cut | OAuth, Stripe, multi-tenant auth | Do not build | No points, kills velocity |

### 5.4 Functional requirements

- **FR-1 Contract indexing:** accept SOW PDF/Markdown, chunk by numbered clauses, embed 768-d, store dense + tsvector in Tiger Data.
- **FR-2 Hybrid retrieval:** for each CSV row, return top-3 clauses via RRF (vector cosine + ts_rank_cd).
- **FR-3 Tabular scoring:** build 9-feature vector per row → TabPFN-3.5 → `scope_leakage_probability` 0.0–1.0 + `predicted_fair_hours`.
- **FR-4 Rate grounding:** if leakage >0.65, query SerpApi (cached 24h) for hourly/fixed benchmark by task category + region.
- **FR-5 Verdict + change order:** Tinker-tuned Gemma outputs strict JSON: verdict, clause citation, reasoning, billable delta, email draft. No markdown preamble.
- **FR-6 Telemetry drawer:** collapsible UI shows per-stage latency, token savings vs GPT-4o, Sentry trace link, model id `gemma-2-9b-tinker-sow-v1`.
- **FR-7 Demo mode:** `/api/demo/audit` runs full pipeline on bundled sample SOW + CSV with 4 hidden leaks, no upload needed.
- **FR-8 Export:** download ledger CSV + change-order Markdown/PDF, copy-email button.

### 5.5 UX flow (3 screens max)

1. **Upload:** left = SOW PDF dropzone (shows clause count after parse), right = CSV dropzone (shows row count + column map). Big CTA: "Audit My Week →" + secondary: "Try Instant Demo."
2. **Ledger:** table with traffic-light verdict pill, hours, leakage bar, matched clause excerpt (expandable), market rate, recoverable $. Top summary cards: total logged, out-of-scope hrs, recoverable $.
3. **Recover:** generated email preview (editable textarea) + change-order markdown preview + [Copy Email] [Download PDF] + telemetry drawer at bottom.

Empty/error states: bad CSV columns → show expected header template + download sample. No SOW → block audit with friendly nudge.

### 5.6 Success metrics (judge-visible)

- Time-to-value <30s for demo dataset (upload → ledger).
- 4/4 hidden leaks flagged OUT_OF_SCOPE in demo.
- Strict JSON validity >95% on holdout (vs ~70% base Gemma).
- Telemetry shows full 4-span trace in Sentry.
- User #1 quote: "Would pay $19/mo if it saved one ticket" — capture for DEV post.

---

## 6. Architecture — System Design

### 6.1 High-level topology & pipeline

```text
+-------------------------------------------------------------------+
| CLIENT (scopeshield.tech)                                         |
| React 19 + Vite + Tailwind | SOW uploader | CSV dropzone | Ledger |
+----------------------------------+------------------------------+
                                   | HTTPS multipart / JSON
                                   v
+-------------------------------------------------------------------+
| API LAYER (Render Web Service)                                    |
| FastAPI async + Sentry tracing (span-level latency / tokens)      |
+-------+---------------------+-------------------+-----------------+
        | 1. Hybrid RAG       | 2. Tabular ML     | 3. Market comps
        v                     v                   v
+---------------+   +-----------------+   +-------------------------+
| TIGER DATA    |   | TABPFN-3.5      |   | SERPAPI                 |
| pgvector+tsv  |   | Prior Labs FM   |   | freelance rate lookup   |
| RRF fusion    |   | overrun risk    |   | cached 24h              |
+-------+-------+   +--------+--------+   +------------+------------+
        |                    |                         |
        +--------------------+-------------------------+
                             | 4. Enriched context
                             v
+-------------------------------------------------------------------+
| OPEN-WEIGHT LAYER (local / self-hosted)                           |
| Gemma-2-9B-IT (or Gemma-3-4B-IT) via Ollama/vLLM + Tinker LoRA    |
+-------------------------------------------------------------------+
```

**Execution order per audit:**

1. Parse SOW → chunk by `Section X.Y` → embed → upsert to Tiger.
2. Parse CSV → validate headers → build feature rows.
3. For each row: Tiger RRF top-3 clauses (semantic + keyword).
4. TabPFN-3.5 `predict_proba` on 9-feature vector + SOW distance.
5. If leakage >0.65: SerpApi rate lookup (cache-first).
6. Gemma+Tinker strict-JSON verdict + email + change-order markdown.
7. Return ledger + totals + telemetry (Sentry trace id).

### 6.2 Stack specification

- **Frontend:** React 19, Vite, Tailwind CSS, Lucide icons (Render Static Site on `.tech`).
- **Backend:** Python 3.11+, FastAPI, Pydantic v2, asyncpg / psycopg[binary] (Render Web Service).
- **DB:** Tiger Data Postgres + `pgvector` + `pg_trgm` (hybrid search, no external orchestrator).
- **Tabular FM:** `tabpfn-client` (Prior Labs API, free non-commercial key) — Classifier + Regressor.
- **LLM:** `google/gemma-2-9b-it` (fallback `gemma-3-4b-it`), served via Ollama / vLLM locally; Tinker LoRA adapter `gemma-2-9b-tinker-sow-v1`.
- **Embeddings:** `nomic-embed-text` 768-d (local via Ollama) to keep NDA text in-VPC.
- **Search grounding:** `google-search-results` (SerpApi) for `freelance <category> hourly rate 2026`.
- **Observability:** `sentry-sdk[fastapi]` with `ai_monitoring=True`, 4 named spans.
- **Build telemetry:** Entire / Copilot session export for DEV post appendix.

### 6.3 Planned repo layout (code phase, not yet committed)

```text
scopeshield/
├── backend/
│   ├── main.py            # FastAPI + Sentry init + CORS + /audit routes
│   ├── db_tiger.py        # pool + RRF hybrid search function caller
│   ├── engine_tabpfn.py   # feature builder + TabPFN predict_proba
│   ├── engine_serp.py     # SerpApi lookup with in-memory cache
│   ├── engine_gemma.py    # Ollama/vLLM client, strict-JSON retry
│   └── schemas.py         # Pydantic v2 contracts (see §8)
├── data/                  # local only, never commit real client data
│   ├── baseline_agency_tickets.csv
│   ├── demo_sow_contract.md
│   └── demo_weekly_git_jira.csv
├── scripts/
│   ├── generate_tinker_dataset.py
│   └── benchmark_tinker.py
├── frontend/              # React + Vite + Tailwind ledger UI
└── render.yaml            # 1-click Render blueprint
```

> Note: per current `.gitignore`, only `README.md` is tracked. Code/data dirs stay local until you explicitly lift the ignore.

---

## 7. TRD — Technical Requirements Document

### 7.1 Database schema + hybrid search (Tiger Data)

Run this DDL once on your Tiger Data Postgres instance. It gives you RRF in pure SQL — no LangChain needed.

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE projects (
  project_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_name TEXT NOT NULL,
  client_name TEXT NOT NULL,
  contracted_hourly_rate NUMERIC(10,2) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE sow_clauses (
  clause_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(project_id) ON DELETE CASCADE,
  section_number TEXT NOT NULL,
  clause_text TEXT NOT NULL,
  is_exclusion_clause BOOLEAN DEFAULT FALSE,
  embedding vector(768) NOT NULL,
  search_tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', clause_text)) STORED
);

CREATE INDEX idx_sow_embedding ON sow_clauses USING hnsw (embedding vector_cosine_ops);
CREATE INDEX idx_sow_tsv ON sow_clauses USING gin (search_tsv);

-- Hybrid: vector (semantic) + keyword (tsvector) via RRF
CREATE OR REPLACE FUNCTION match_sow_clauses_hybrid(
  p_project_id UUID, query_text TEXT, query_embedding vector(768),
  match_limit INT DEFAULT 3, rrf_k INT DEFAULT 60
)
RETURNS TABLE (clause_id UUID, section_number TEXT, clause_text TEXT,
  is_exclusion_clause BOOLEAN, semantic_distance FLOAT, rrf_score FLOAT)
LANGUAGE sql AS $$
WITH semantic_search AS (
  SELECT clause_id, embedding <=> query_embedding AS dist,
    ROW_NUMBER() OVER (ORDER BY embedding <=> query_embedding) AS rank_ix
  FROM sow_clauses WHERE project_id = p_project_id LIMIT match_limit * 3
),
keyword_search AS (
  SELECT clause_id,
    ROW_NUMBER() OVER (ORDER BY ts_rank_cd(search_tsv, plainto_tsquery('english', query_text)) DESC) AS rank_ix
  FROM sow_clauses WHERE project_id = p_project_id
    AND search_tsv @@ plainto_tsquery('english', query_text) LIMIT match_limit * 3
)
SELECT c.clause_id, c.section_number, c.clause_text, c.is_exclusion_clause,
  COALESCE(s.dist, 1.0)::FLOAT AS semantic_distance,
  (COALESCE(1.0/(rrf_k+s.rank_ix),0.0)+COALESCE(1.0/(rrf_k+k.rank_ix),0.0))::FLOAT AS rrf_score
FROM semantic_search s FULL OUTER JOIN keyword_search k USING (clause_id)
JOIN sow_clauses c ON c.clause_id = COALESCE(s.clause_id, k.clause_id)
ORDER BY rrf_score DESC LIMIT match_limit;
$$;
```

**Chunking rule:** split SOW Markdown/PDF text on `^Section \d+(\.\d+)*` headings. Mark `is_exclusion_clause=TRUE` if heading contains `out of scope / exclusion / not included / assumption`.

**Embedding rule:** 768-d via `nomic-embed-text`. Store once per clause. Query embedding per CSV row = `task_title + notes` (truncate 512 tokens).

---

### 7.2 TabPFN-3.5 tabular pipeline

Prior Labs rewards TabPFN *inside a wider agent* — not as a standalone notebook. Here TabPFN owns all numeric judgment; Gemma never does arithmetic.

**Input CSV contract (expected headers):**

```csv
ticket_id,task_title,task_category,estimated_hours,actual_hours_logged,client_revision_rounds,files_touched_count,unplanned_flag,notes
JIRA-101,Build landing hero,frontend,4,4.5,1,6,0,per Section 3.1
JIRA-102,Add SSO + audit logs,backend,0,11,3,28,1,client asked on Slack Tue
```

**Derived feature vector X per row (9 cols):**

| Feature | Type | How computed |
|---|---|---|
| task_category | categorical | frontend/backend/devops/design/compliance/database |
| estimated_hours | float | from CSV (0.0 if unplanned) |
| actual_hours_logged | float | from CSV |
| overrun_ratio | float | `actual / max(estimated, 0.5)` |
| client_revision_rounds | int | from CSV |
| files_touched_count | int | from CSV / git stat |
| unplanned_flag | 0/1 | from CSV (1 if added post-kickoff) |
| min_sow_semantic_distance | float 0–1 | cosine distance to closest Tiger clause |
| matched_exclusion_clause | 0/1 | 1 if top Tiger hit has `is_exclusion=TRUE` |

**Runtime logic:**

- Ship `data/baseline_agency_tickets.csv` with 120 labeled rows (0 = in-scope normal, 1 = creep/overrun) covering all 6 categories.
- At audit time: `TabPFNClassifier.fit(X_baseline, y_baseline)` in-context (<1s via Prior Labs API), then `predict_proba(X_uploaded)` → `scope_leakage_probability`.
- Companion `TabPFNRegressor` on same X predicts `predicted_fair_hours` for under-estimated tickets.
- Threshold: `>0.65` = route to SerpApi + Gemma OUT_OF_SCOPE candidate; `0.35–0.65` = GREY_AREA; `<0.35` = likely IN_SCOPE (still needs Gemma clause check).

Why this matters for judging: show a scatter (overrun_ratio vs leakage) where LLM-only baseline mis-scores math-heavy rows and TabPFN nails them.

---

### 7.3 Tinker + Gemma fine-tuning & benchmark

To win Gemma ($200) + Tinker ($200) you must *show measured improvement over baseline* — not just "we used Gemma."

**Base failure modes to fix:**

1. Raw `gemma-2-9b-it` wraps JSON in chatty preamble ("Sure! Here's your audit...") → breaks `json.loads`.
2. Raw model is sycophantic — labels clear exclusions as "GREY_AREA to be safe."

**Dataset protocol (2 hrs, huge payoff):**

- Generate 250 train + 50 holdout pairs: input = (work-log row + top-3 clauses + TabPFN score) → output = strict JSON verdict + change-order sentence.
- Cover: frontend/backend/devops/design/compliance/database × IN/GREY/OUT, with exclusion-clause traps (e.g., "SSO explicitly out of scope in §5.2").
- Script: `scripts/generate_tinker_dataset.py` → `data/tinker_sow_pairs.jsonl` (local only).

**LoRA via Tinker:**

- Base: `google/gemma-2-9b-it` (alt: `gemma-3-4b-it` if VRAM tight). Rank 16, 3 epochs, strict-JSON mask loss.
- Adapter id: `gemma-2-9b-tinker-sow-v1`. Serve via Ollama (`Modelfile` with `ADAPTER`) or vLLM `--enable-lora`.
- System prompt pins schema: "Output ONLY valid JSON matching AuditedWorkItem. No preamble. Cite section_number verbatim."

**Benchmark protocol — `scripts/benchmark_tinker.py` on 50 holdout:**

| Metric | Base Gemma | Tinker-tuned | Target delta |
|---|---|---|---|
| Strict JSON validity % | ~68–75% | ~96–99% | +25pp (parser breakage → ~0) |
| Macro F1 (IN/GREY/OUT) | ~0.71 | ~0.86 | +0.15 (esp. OUT recall) |
| Mean output tokens / audit | ~420 | ~270 | −35% (no preamble = faster + cheaper) |
| Mean latency / row (M1 / T4) | ~2.1s | ~1.4s | −33% |

Embed this table + confusion matrix in DEV post — it's your Gemma+Tinker prize evidence.

---

### 7.4 Strict API contract (Pydantic v2)

```python
from pydantic import BaseModel, Field
from typing import List, Literal

class SOWClauseMatch(BaseModel):
    section_number: str
    clause_text: str
    semantic_distance: float
    rrf_score: float

class AuditedWorkItem(BaseModel):
    ticket_id: str
    task_title: str
    actual_hours: float
    tabpfn_leakage_probability: float = Field(..., ge=0.0, le=1.0)
    verdict: Literal["IN_SCOPE", "GREY_AREA", "OUT_OF_SCOPE"]
    violated_or_matched_clause: str
    contractual_reasoning: str
    market_hourly_rate_usd: float
    recoverable_amount_usd: float

class AuditReportResponse(BaseModel):
    project_name: str
    total_hours_logged: float
    out_of_scope_hours: float
    total_recoverable_revenue_usd: float
    items: List[AuditedWorkItem]
    change_order_markdown: str
    telemetry: dict  # sentry trace id, latency, open vs closed cost math
```

**Endpoints:**

- `POST /api/projects` — create project (name, client, rate).
- `POST /api/projects/{id}/sow` — multipart PDF/md → returns `{clauses_indexed}`.
- `POST /api/projects/{id}/audit` — multipart CSV → returns `AuditReportResponse`.
- `GET /api/demo/audit` — no-upload judge path, runs bundled demo files.
- `GET /api/health` — `{tiger_ok, tabpfn_ok, gemma_model, serp_ok}` for Render checks.

### 7.5 Sentry agent tracing

Wrap each stage so the waterfall is screenshot-ready for the DEV post:

```python
import sentry_sdk

async def run_scopeshield_audit(project_id: str, csv_rows: list):
    with sentry_sdk.start_transaction(op="ai.agent.audit", name="ScopeShield_Full_Audit") as txn:
        with sentry_sdk.start_span(op="db.vector.hybrid_rrf", description="Tiger Hybrid Retrieval") as s1:
            matched = await retrieve_hybrid_sow_clauses(project_id, csv_rows)
            s1.set_data("rows_processed", len(csv_rows))
        with sentry_sdk.start_span(op="ai.tabular.tabpfn", description="TabPFN Scoring") as s2:
            scores = run_tabpfn_inference(csv_rows, matched)
            s2.set_data("flagged", sum(1 for s in scores if s > 0.65))
        with sentry_sdk.start_span(op="tool.serpapi.rates", description="SerpApi Rates") as s3:
            rates = await fetch_live_market_rates(csv_rows, scores)
            s3.set_data("queries", len(rates))
        with sentry_sdk.start_span(op="ai.llm.gemma_tinker", description="Gemma Synthesis") as s4:
            result = await synthesize_with_gemma(csv_rows, matched, scores, rates)
            s4.set_data("model", "gemma-2-9b-tinker-sow-v1")
        return build_final_response(result, txn.trace_id)
```

Init with `sentry_sdk.init(dsn=..., traces_sample_rate=1.0, ai_monitoring=True)`. UI drawer links `https://<org>.sentry.io/traces/{trace_id}`.

### 7.6 SerpApi rate grounding (cached)

- Query: `"freelance {category} developer hourly rate 2026"` + optional `location=United States` / `India`.
- Parse `organic_results[].snippet` for `$X–$Y/hr` via regex; median of top-3 = `market_hourly_rate_usd`.
- Cache key `rate:{category}:{region}` TTL 24h (in-memory dict v1, Redis later).
- Fallback table if quota hit: frontend 55, backend 70, devops 85, design 50, compliance 90, database 75 (USD/hr).
- Show citation link under each recoverable $ — judges love receipts.

---

