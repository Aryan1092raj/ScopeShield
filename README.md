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

