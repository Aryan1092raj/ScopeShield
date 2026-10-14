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

