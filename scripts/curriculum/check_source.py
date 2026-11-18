"""Checks curriculum source files (scripts/curriculum/source/*.json) against the cost sheet and the
authoring rules. Usage: python3 scripts/curriculum/check_source.py [subjectId ...]  (no args = all files)
Exit code 1 on any error. Prerequisite IDs must resolve to subtopics in source files that exist."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import sheet

SRC = Path(__file__).parent / "source"
ID_RE = re.compile(r"^(cbse|cambridge|ib)-g(8|9|10|11|12)-[a-z0-9-]+-ch\d{2}-st\d$")

def load_all():
    out = {}
    for p in sorted(SRC.glob("*.json")):
        out[p.stem] = json.loads(p.read_text())
    return out

def subtopic_ids(src):
    ids = []
    for ci, ch in enumerate(src["chapters"], 1):
        for si, _ in enumerate(ch["subtopics"], 1):
            ids.append(f"{src['subjectId']}-ch{ci:02d}-st{si}")
    return ids

def check(sid, src, rows, known, errors):
    e = lambda m: errors.append(f"{sid}: {m}")
    row = rows.get(sid)
    if row is None or not row["counted"]:
        return e("not a counted subject in the cost sheet")
    if src.get("subjectId") != sid:
        e("subjectId field does not match file name")
    chs = src.get("chapters", [])
    if len(chs) != row["chapterCount"]:
        e(f"{len(chs)} chapters, cost sheet says {row['chapterCount']}")
    names = row["chapterNames"]
    seen = set()
    for ci, ch in enumerate(chs, 1):
        tag = f"ch{ci:02d}"
        if names and ci <= len(names) and ch.get("sheetName") != names[ci - 1]:
            e(f"{tag} sheetName {ch.get('sheetName')!r} != sheet {names[ci - 1]!r}")
        if not ch.get("name"):
            e(f"{tag} missing name")
        sts = ch.get("subtopics", [])
        if not 3 <= len(sts) <= 5:
            e(f"{tag} has {len(sts)} subtopics (need 3-5)")
        for si, st in enumerate(sts, 1):
            own = f"{sid}-{tag}-st{si}"
            if not st.get("name"):
                e(f"{own} missing name")
            if st.get("name", "").lower() in seen:
                e(f"{own} duplicate subtopic name {st['name']!r}")
            seen.add(st.get("name", "").lower())
            if st.get("weight") not in ("L", "S", "H"):
                e(f"{own} weight must be L/S/H")
            if not st.get("note"):
                e(f"{own} missing note (prerequisite to probe, in words)")
            for p in st.get("prereq", []):
                if not ID_RE.match(p):
                    e(f"{own} bad prereq id {p!r}"); continue
                if p == own:
                    e(f"{own} lists itself as prereq"); continue
                pb, pg = p.split("-")[0], int(p.split("-")[1][1:])
                if pb != row["board"]:
                    e(f"{own} prereq {p} is another board")
                if pg > row["grade"]:
                    e(f"{own} prereq {p} is a later grade")
                if p.startswith(sid + "-") and p >= own:
                    e(f"{own} prereq {p} must come earlier in the same subject")
                if p not in known:
                    e(f"{own} prereq {p} does not resolve (target file missing or index out of range)")

def find_cycles(all_src):
    graph = {}
    for src in all_src.values():
        for ci, ch in enumerate(src["chapters"], 1):
            for si, st in enumerate(ch["subtopics"], 1):
                graph[f"{src['subjectId']}-ch{ci:02d}-st{si}"] = st.get("prereq", [])
    state, cyc = {}, []
    def dfs(n, path):
        state[n] = 1
        for m in graph.get(n, []):
            if state.get(m) == 1:
                cyc.append(" -> ".join(path + [m]))
            elif not state.get(m):
                dfs(m, path + [m])
        state[n] = 2
    sys.setrecursionlimit(100000)
    for n in graph:
        if not state.get(n):
            dfs(n, [n])
    return cyc

def main(argv):
    rows = {r["id"]: r for r in sheet.read_rows() if r["counted"]}
    all_src = load_all()
    known = {i for s in all_src.values() for i in subtopic_ids(s)}
    targets = argv or list(all_src)
    errors = []
    for sid in targets:
        if sid not in all_src:
            errors.append(f"{sid}: no source file"); continue
        check(sid, all_src[sid], rows, known, errors)
    errors += [f"cycle: {c}" for c in find_cycles(all_src)]
    for m in errors:
        print("ERROR", m)
    n_st = sum(len(c["subtopics"]) for s in targets if s in all_src for c in all_src[s]["chapters"])
    print(f"checked {len(targets)} subject(s), {n_st} subtopics, {len(errors)} error(s)")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
