"""Builds source/cbse-g8-maths.json from the class 8 maths workbook (sheets Teaching Plan and
Gap Diagnosis section D) so the curriculum map reproduces it exactly: 14 chapters, 45 subtopics,
same order, weights, periods and prerequisites."""
import json, re
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parents[2]
WB = ROOT / "reference" / "cbse-class8-maths-assessment-v4.xlsx"
SID = "cbse-g8-maths"

def main():
    wb = openpyxl.load_workbook(WB, data_only=True)
    plan = [r for r in wb["Teaching Plan"].iter_rows(min_row=2, values_only=True) if isinstance(r[0], (int, float))]
    gap = list(wb["Gap Diagnosis"].iter_rows(values_only=True))
    start = next(i for i, r in enumerate(gap) if r[1] == "Subtopic" or r[0] == "Subtopic")
    prereq_text = {}
    for r in gap[start + 1:]:
        if r[1] and r[2]:
            prereq_text[r[1].strip()] = r[2].strip()
    chapters, ids = [], {}
    for r in plan:
        ch, chname, st, order, weight, periods = int(r[0]), r[1].strip(), r[2].strip(), int(r[3]), r[4], int(r[5])
        if len(chapters) < ch:
            chapters.append({"sheetName": chname, "name": chname, "subtopics": []})
        ids[st] = f"{SID}-ch{ch:02d}-st{order}"
        chapters[ch - 1]["subtopics"].append({"name": st, "weight": weight, "periods": periods})
    names = list(ids)
    alias = {"multiplying expressions (binomial x binomial)": "Multiplying expressions (monomial × binomial, binomial × binomial)",
             "algebraic expressions: like terms": "Algebraic expressions: terms, like terms, addition",
             "exponents (units squared/cubed)": None}
    def resolve(token):
        k = token.strip().lower()
        if k in alias:
            return alias[k]
        t = re.sub(r"\s*\((?:Cl|for|units).*?\)$", "", token).strip().lower().replace(" x ", " × ")
        if not t:
            return None
        exact = [n for n in names if n.lower() == t]
        if exact:
            return exact[0]
        pref = [n for n in names if n.lower().startswith(t)]
        return pref[0] if len(pref) == 1 else None
    for chap in chapters:
        for s in chap["subtopics"]:
            text = prereq_text[s["name"]]
            own = ids[s["name"]]
            pids = []
            for tok in text.split(";"):
                if "(Cl" in tok:
                    continue  # earlier-class skill, outside the map
                hit = resolve(tok)
                if hit and ids[hit] != own and ids[hit] not in pids:
                    pids.append(ids[hit])
            s["prereq"] = pids
            s["note"] = text
    out = {"subjectId": SID, "source": "reference/cbse-class8-maths-assessment-v4.xlsx (Teaching Plan; Gap Diagnosis D)",
           "chapters": chapters}
    p = Path(__file__).parent / "source" / f"{SID}.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    n = sum(len(c["subtopics"]) for c in chapters)
    print(f"{SID}: {len(chapters)} chapters, {n} subtopics, {sum(s['periods'] for c in chapters for s in c['subtopics'])} periods")

if __name__ == "__main__":
    main()
