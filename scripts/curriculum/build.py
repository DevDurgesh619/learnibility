"""Builds data/curriculum/ from the cost sheet and the authored source files.

  python3 scripts/curriculum/build.py

Writes:
  data/curriculum/subjects.json         every counted Subject (157), from the cost sheet
  data/curriculum/{subjectId}.json      chapters + subtopics for each subject with a source file
  data/curriculum/streams.json          what each board/grade/stream offers (incl. shared "same as" rows)
  data/curriculum/sheet-reference.json  cost-sheet facts the validator checks against
Teaching periods (40 min) come from subtopic weight (H 4, S 3, L 2, the class 8 maths workbook ratios),
scaled per subject to the programme's annual instruction time; cbse-g8-maths keeps the workbook's own periods.
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import sheet

ROOT = sheet.ROOT
OUT = ROOT / "data" / "curriculum"
SRC = Path(__file__).parent / "source"
GEN = "scripts/curriculum/build.py"
BASE = {"H": 4, "S": 3, "L": 2}

# Published slugs follow the cost-sheet seat for every board (agreed with the question-bank threads),
# so e.g. IB Global Politics is ib-g11-political-science. Source files still use the authoring slugs;
# this map is applied to every ID on output. TODO(W2): migrate source files and drop this map.
SLUG_RENAME = {"information-technology": "informatics", "digital-society": "informatics", "law": "legal-studies",
               "global-perspectives": "political-science", "global-politics": "political-science",
               "statistics": "applied-maths", "maths-ai": "applied-maths", "anthropology": "sociology"}
_ID = re.compile(r"^((?:cbse|cambridge|ib)-g\d{1,2}-)([a-z0-9-]+?)((?:-ch\d{2}(?:-st\d)?)?)$")

def rid(i):
    m = _ID.match(i)
    return f"{m.group(1)}{SLUG_RENAME.get(m.group(2), m.group(2))}{m.group(3)}" if m else i

def renamed(obj):
    if isinstance(obj, dict):
        return {k: (SLUG_RENAME.get(v, v) if k == "slug" else renamed(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [renamed(v) for v in obj]
    return rid(obj) if isinstance(obj, str) else obj
LANG = {"english", "hindi"}

def annual_periods(row):
    """Annual teaching periods (40 min) per subject, from official instruction time."""
    b, g = row["board"], row["grade"]
    if b == "cbse":
        t = 150 if g <= 10 else 200          # ~6 periods/week theory; 11-12 adds practical periods elsewhere
    elif b == "cambridge":
        t = 150 if g == 8 else 100 if g <= 10 else 270   # Stage 9 ~5/wk; IGCSE 130 GLH over 2 yrs; AS/A2 180 GLH each
    else:
        t = 120 if g <= 10 else 180          # MYP ~70-80 h/yr; DP HL 240 h over 2 yrs
    return round(t * 0.8) if row["slug"] in LANG else t

def assign_periods(row, src):
    sts = [st for ch in src["chapters"] for st in ch["subtopics"]]
    if all("periods" in st for st in sts):
        return [st["periods"] for st in sts]
    raw = sum(BASE[st["weight"]] for st in sts)
    f = min(1.5, max(0.6, annual_periods(row) / raw))
    return [max(1, round(BASE[st["weight"]] * f)) for st in sts]

def programme_fields(row):
    course = row["course"]
    if row["board"] == "cbse":
        m = re.search(r"\((\d{3})\)|[–-] (\d{3})\b|\b(\d{3})\b(?!.*\b\d{3}\b)", course)
        code = next((x for x in (m.groups() if m else []) if x), None)
        prog = f"CBSE Class {row['grade']} {row['name']}" + (f" ({code})" if code else "")
        return prog, course
    head, _, tail = course.partition(" · ")
    return head.strip(), (tail.strip() or None)

def subject_record(row):
    prog, book = programme_fields(row)
    rec = {"id": row["id"], "board": row["board"], "grade": row["grade"], "stream": row["stream"],
           "slug": row["slug"], "name": row["name"], "programme": prog}
    if book:
        rec["textbook"] = book
    rec.update({"examPattern": row["examPattern"], "chapterCount": row["chapterCount"],
                "questionTarget": row["questionTarget"]})
    return rec

def build_subject(row, src):
    sid = row["id"]
    periods = iter(assign_periods(row, src))
    chapters, subtopics = [], []
    for ci, ch in enumerate(src["chapters"], 1):
        cid = f"{sid}-ch{ci:02d}"
        ids, total = [], 0
        for si, st in enumerate(ch["subtopics"], 1):
            p = next(periods)
            total += p
            tid = f"{cid}-st{si}"
            ids.append(tid)
            rec = {"id": tid, "chapterId": cid, "order": si, "name": st["name"], "weight": st["weight"],
                   "teachingPeriods": p, "prerequisiteIds": st.get("prereq", [])}
            if st.get("note"):
                rec["prerequisiteNote"] = st["note"]
            rec["learnHours"] = {}
            rec["masterHours"] = {}
            subtopics.append(rec)
        chapters.append({"id": cid, "subjectId": sid, "order": ci, "name": ch["name"],
                         "teachingPeriods": total, "subtopicIds": ids})
    # items = Chapter[] (contract wrapper); subtopics = Subtopic[] for the same subject
    return {"schemaVersion": 1, "generatedBy": GEN, "subject": subject_record(row),
            "items": chapters, "subtopics": subtopics}

def streams(rows):
    counted = {r["id"]: r for r in rows if r["counted"]}
    groups = {}
    for r in rows:
        key = (r["board"], r["grade"], r["stream"])
        g = groups.setdefault(key, {"board": r["board"], "grade": r["grade"], "stream": r["stream"], "offerings": []})
        if r["chapterCount"] == 0:
            continue  # "NOT OFFERED on this board"
        if r["counted"]:
            sid, note = r["id"], None
        else:
            same = [c for c in counted.values() if c["board"] == r["board"] and c["grade"] == r["grade"]
                    and (c["slug"] == r["slug"] or (r["slug"] in ("statistics",) and c["slug"] == "maths"))]
            if same and re.search(r"same as|identical", r["course"], re.I):
                sid, note = same[0]["id"], "shared with another stream; counted once"
            else:
                sid, note = None, "optional paper, not in the question bank"
        o = {"seat": r["label"], "subjectId": sid, "name": counted[sid]["name"] if sid else r["name"]}
        if note:
            o["note"] = note
        g["offerings"].append(o)
    return list(groups.values())

def dump(path, obj):
    path.write_text(json.dumps(renamed(obj), ensure_ascii=False, indent=1) + "\n")

def main():
    rows = sheet.read_rows()
    counted = [r for r in rows if r["counted"]]
    OUT.mkdir(parents=True, exist_ok=True)
    wrap = lambda items: {"schemaVersion": 1, "generatedBy": GEN, "items": items}
    dump(OUT / "subjects.json", wrap([subject_record(r) for r in counted]))
    dump(OUT / "streams.json", wrap(streams(rows)))
    built, chapter_names = [], {}
    for r in counted:
        p = SRC / f"{r['id']}.json"
        if not p.exists():
            continue
        src = json.loads(p.read_text())
        data = build_subject(r, src)
        dump(OUT / f"{rid(r['id'])}.json", data)
        if r["chapterNames"]:
            got = [c.get("sheetName") for c in src["chapters"]]
            if got != r["chapterNames"]:
                sys.exit(f"{r['id']}: source sheetName list does not match the cost sheet")
        chapter_names[r["id"]] = [{"sheet": c.get("sheetName"), "name": c["name"]} for c in src["chapters"]]
        built.append(r["id"])
    ref = [{"subjectId": r["id"], "tab": r["tab"], "row": r["row"], "label": r["label"], "course": r["course"],
            "chapterCount": r["chapterCount"], "sheetChapterNames": r["chapterNames"],
            "chapterNames": chapter_names.get(r["id"]),
            "questionTarget": r["questionTarget"],
            "questionPlan": {k: r[k] for k in ("perChapter", "bankQuestions", "practiceTests", "questionsPerTest",
                                               "practiceQuestions", "mocks", "questionsPerMock", "mockQuestions")},
            "questionFormat": r["questionFormat"], "officialSource": r["officialSource"],
            "annualTeachingPeriods": annual_periods(r)} for r in counted]
    dump(OUT / "sheet-reference.json",
         {"schemaVersion": 1, "generatedBy": GEN, "source": "reference/assessment-cost-gr8-12.xlsx",
          "boardTotals": sheet.BOARD_TOTALS, "grandTotal": sheet.GRAND_TOTAL, "items": ref})
    print(f"subjects.json: {len(counted)} subjects; built {len(built)} subject files")

if __name__ == "__main__":
    main()
