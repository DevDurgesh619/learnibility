#!/usr/bin/env python3
"""Import the 430-parameter learner profile into JSON.

Source: reference/learnibility-430-parameter-profile-v2.xlsx
  sheet "430 Master Profile"        -> data/profile/parameters.json
  sheet "Collection Method Legend"  -> data/profile/collection-methods.json
  sheet "Sensitivity Tiers"         -> data/profile/sensitivity-tiers.json

Run from the repo root:  python3 scripts/foundations/import-430.py
Requires openpyxl. Output is deterministic (stable key order, sorted by ID).
"""
import json
import re
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "reference" / "learnibility-430-parameter-profile-v2.xlsx"
OUT = ROOT / "data" / "profile"
GENERATED_BY = "scripts/foundations/import-430.py"

TIER_MAP = {"T1 Standard": "T1", "T2 Elevated": "T2", "T3 Sensitive Health": "T3", "C Consent Artefact": "C"}
ORIGIN_MAP = {"Existing 277": "existing_277", "Proposed v2": "proposed_v2"}
CADENCES = {"Once", "Annual", "Term", "Monthly", "Weekly", "Continuous", "As needed"}
METHOD_RE = re.compile(r"\bM([1-9]|1[0-9]|20)\b")


def clean(v):
    if v is None:
        return None
    if isinstance(v, str):
        v = v.strip()
        return v or None
    return v


def methods_from(text):
    """Ordered, de-duplicated M-codes from text like '1. M14 ... → 2. M9 ...'."""
    seen = []
    for m in METHOD_RE.finditer(text or ""):
        code = f"M{m.group(1)}"
        if code not in seen:
            seen.append(code)
    return seen


def write(name, items):
    OUT.mkdir(parents=True, exist_ok=True)
    doc = {"schemaVersion": 1, "generatedBy": GENERATED_BY, "items": items}
    (OUT / name).write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote data/profile/{name}: {len(items)} items")


def import_parameters(wb):
    ws = wb["430 Master Profile"]
    rows = ws.iter_rows(values_only=True)
    header = [clean(h) for h in next(rows)]
    col = {h: i for i, h in enumerate(header) if h}
    params = []
    for r in rows:
        if r[col["ID"]] is None:
            continue
        g = lambda h: clean(r[col[h]])
        n = int(g("ID"))
        methods_text = g("Collection Methods (Preferential Order)") or ""
        methods = methods_from(methods_text)
        default = g("Phase-1 Default")
        default_codes = methods_from(default or "")
        if not methods:  # consent artefacts describe a flow, not a method code
            methods = default_codes
        cadence = g("Update Cadence")
        if cadence not in CADENCES:
            sys.exit(f"p{n}: unknown cadence {cadence!r}")
        tier = TIER_MAP.get(g("Sensitivity Tier"))
        if not tier:
            sys.exit(f"p{n}: unknown tier {g('Sensitivity Tier')!r}")
        refresh = g("State Refresh Target / Year")
        item = {
            "id": f"p{n}",
            "number": n,
            "origin": ORIGIN_MAP[g("Origin")],
            "section": g("Section"),
            "category": g("Category"),
            "name": g("Parameter"),
            "description": g("Description"),
            "dataType": g("Data Type"),
            "methods": methods,
            "methodsText": methods_text,
            "phase1Default": default_codes[0] if default_codes else None,
            "tier": tier,
            "handlingNote": g("Handling / Consent Note"),
            "cadence": cadence,
            "refreshesPerYear": int(refresh) if isinstance(refresh, (int, float)) else None,
            "aiUse": g("AI Use"),
            "evidenceDensity": g("Evidence Density"),
            "humanValidation": g("Human Validation"),
            "externalShareRule": g("External Share Rule"),
        }
        params.append({k: v for k, v in item.items() if v is not None or k in ("phase1Default", "refreshesPerYear")})
    params.sort(key=lambda p: p["number"])

    nums = [p["number"] for p in params]
    if nums != list(range(1, 431)):
        sys.exit(f"expected parameters 1..430, got {len(nums)} (first gap near {next((i for i, n in enumerate(nums, 1) if i != n), None)})")
    return params


def import_methods(wb):
    ws = wb["Collection Method Legend"]
    items, group = [], None
    for r in ws.iter_rows(min_row=3, values_only=True):
        code, name, intrusiveness, guidance = (clean(x) for x in r[:4])
        if code and code.startswith("TIER "):
            group = code
            continue
        if code and code.startswith("EXCLUDED"):
            break
        if code and re.fullmatch(r"M\d+", code):
            items.append({"code": code, "name": name, "intrusiveness": intrusiveness, "tierGroup": group, "guidance": guidance})
    if [m["code"] for m in items] != [f"M{i}" for i in range(1, 21)]:
        sys.exit("collection method legend: expected M1..M20")
    return items


def import_tiers(wb):
    ws = wb["Sensitivity Tiers"]
    items = []
    for r in ws.iter_rows(values_only=True):
        label = clean(r[0])
        if label in TIER_MAP:
            items.append({
                "tier": TIER_MAP[label],
                "label": label,
                "count": int(r[2]),
                "definition": clean(r[3]),
                "modelUseRule": clean(r[4]),
            })
    return items


def main():
    wb = openpyxl.load_workbook(SRC, data_only=True)
    params = import_parameters(wb)
    tiers = import_tiers(wb)
    for t in tiers:
        actual = sum(1 for p in params if p["tier"] == t["tier"])
        if actual != t["count"]:
            sys.exit(f"tier {t['tier']}: sheet says {t['count']}, master profile has {actual}")
    write("parameters.json", params)
    write("collection-methods.json", import_methods(wb))
    write("sensitivity-tiers.json", tiers)


if __name__ == "__main__":
    main()
