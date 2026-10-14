"""Build Tinker JSONL: (row + clauses + leakage) -> strict JSON verdict.
Writes data/tinker_sow_pairs.jsonl (local only, never commit real client rows).
Usage: python scripts/generate_tinker_dataset.py --n-train 250 --n-test 50
"""
from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

TITLES = {
    "frontend": ["landing hero tweak", "catalog filter polish", "dark mode rework", "checkout CTA copy"],
    "backend": ["SSO Google OAuth", "audit log pipeline", "CSV export endpoint", "webhook retry queue"],
    "devops": ["K8s prod deploy", "CDN cache purge", "staging env refresh", "uptime monitor"],
    "design": ["hero revision round", "icon set redraw", "mobile nav mock", "brand palette pass"],
    "compliance": ["SOC2 log retention", "DPA redline review", "access audit export", "cookie consent banner"],
    "database": ["Hindi locale pack", "Tamil translations", "CMS migration script", "search index rebuild"],
}

EXCLUSION_CLAUSES = [
    ("Section 5.2: Exclusions — Identity and Compliance", "Single sign-on (SSO), OAuth, MFA, and SOC2 audit logging are expressly excluded."),
    ("Section 7.1: Exclusions — Infrastructure and Localisation", "Production DevOps, Kubernetes, uptime SLAs, and additional language packs are expressly excluded."),
]

IN_SCOPE_CLAUSES = [
    ("Section 3.1: Deliverables — Marketing Pages", "5-page responsive React marketing site with hero and up to 3 revision rounds."),
    ("Section 3.2: Deliverables — CMS", "Headless CMS wiring so staff can edit text and images."),
]


def make_pair(rng: random.Random, idx: int, split: str) -> dict:
    cat = rng.choice(list(TITLES))
    out = rng.random() < 0.4  # 40% OUT to teach exclusion enforcement
    title = rng.choice(TITLES[cat])
    leakage = round(rng.uniform(0.7, 0.97) if out else rng.uniform(0.03, 0.45), 3)
    clause = rng.choice(EXCLUSION_CLAUSES) if out else rng.choice(IN_SCOPE_CLAUSES)
    verdict = "OUT_OF_SCOPE" if out else "IN_SCOPE"
    return {
        "input": {
            "ticket_id": f"SYN-{split[:2].upper()}-{idx:03d}",
            "task_title": title,
            "task_category": cat,
            "actual_hours": round(rng.uniform(1, 12), 1),
            "tabpfn_leakage": leakage,
            "clauses": [{"section_number": clause[0], "clause_text": clause[1]}],
        },
        "output": {
            "verdict": verdict,
            "violated_or_matched_clause": clause[0],
            "contractual_reasoning": f"Cited {clause[0]} with leakage {leakage}.",
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-train", type=int, default=250)
    ap.add_argument("--n-test", type=int, default=50)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    out = DATA / "tinker_sow_pairs.jsonl"
    with open(out, "w", encoding="utf-8") as f:
        for i in range(args.n_train):
            f.write(json.dumps(make_pair(rng, i, "train")) + "\n")
        for i in range(args.n_test):
            f.write(json.dumps(make_pair(rng, i, "test")) + "\n")
    print(f"wrote {args.n_train + args.n_test} pairs -> {out}")


if __name__ == "__main__":
    main()
