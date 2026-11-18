"""Copy the workbook's Interventions sheet to /data/catalogues/interventions.json.

Wording is generalised so it works for any board, grade and subject; the original
class 8 maths text is kept as `exampleCbseG8Maths`. Planning numbers (minutes per
session, sessions, weeks) are parsed from the sheet's "Time cost" column by hand
and listed in PLAN below so the timetable engine can size blocks.

Usage: python3 scripts/engines/export-interventions.py reference/cbse-class8-maths-assessment-v4.xlsx
"""
import json, sys, re
import openpyxl

wb = openpyxl.load_workbook(sys.argv[1], data_only=True)
ws = wb['Interventions']

GENERIC = {
 ('G1', 1): "Use the prerequisite listed for the subtopic. Teach only that earlier skill with 2 worked examples, give 10 items on it, then return to the failed subtopic.",
 ('G1', 2): "Free official video or open course for the earlier-grade chapter (NCERT/DIKSHA, Khan Academy, board-endorsed resources), then solve level-1 exemplar items; the teacher checks 5 of them.",
 ('G1', 3): "Structured peer session with a classmate at L4/L5: the peer explains one worked example, the learner explains it back, then 5 items each from a teacher-provided list.",
 ('G2', 1): "Learner reads a fully worked example and writes WHY each step is done, then a counter-example where the rule fails. Mark the explanations, not the answers.",
 ('G2', 2): "Re-teach with a concrete or visual model first (diagram, manipulative, simulation, timeline or flowchart as the subject suits), then the formal rule or symbol.",
 ('G2', 3): "Give two items that look alike but need different ideas. The learner must say what differs BEFORE solving.",
 ('G3', 1): "Item 1 fully worked; item 2 last step blank; item 3 last two steps blank; item 4 unaided. Same method, new values each time.",
 ('G3', 2): "12 items in 3 difficulty steps (4 at D1, 4 at D2, 4 at D3) from the wider bank, with feedback after each block; redo any block with an error.",
 ('G3', 3): "Learner writes the method as 3 to 5 numbered steps on a card and ticks them on every problem for a week.",
 ('G4', 1): "Before answering, write an estimate or expected form of the answer (size, sign, units, key term). Compare at the end. Applies to every application item for two weeks.",
 ('G4', 2): "Timed practice is paused; reach 95% accuracy on D1 to D2 items before timed work resumes.",
 ('G4', 3): "If sleep is short or a phone is in the study block, fix that first via the parent form (M2). Support context only, never a score.",
 ('G5', 1): "12 items shuffled across this and 2 earlier subtopics so the learner must CHOOSE the method. Ask 'which method and why?' before solving.",
 ('G5', 2): "Same method in 3 unfamiliar settings (everyday, another subject, current affairs). Use the C3-D4 items of the wider bank.",
 ('G5', 3): "Learner writes ONE item that combines two ideas, with its solution. The teacher or tutor solves it with the class.",
 ('G6', 1): "3 to 4 retrieval-probe items on each date, closed book, self-marked. Dates go into the planner (M15).",
 ('G6', 2): "Every wrong item goes into an error log with the correct reasoning and is re-attempted after 7 days without looking.",
 ('G6', 3): "5 items from earlier chapters every week; no marks recorded, just tallies.",
 ('G7', 1): "Learner rewrites each word or source-based question as a one-line 'given / find' in own words (home language allowed) before answering.",
 ('G7', 2): "Bilingual glossary of about 30 key terms and phrases per chapter, each with an example. Built once, reused all year.",
 ('G7', 3): "Learner reads 5 questions aloud to a partner who paraphrases them; then swap.",
 ('G8', 1): "Prove competence untimed; then build speed with 5-item timed sets, adding one item per week.",
 ('G8', 2): "Marks-per-minute guide on the paper and a 'skip and return' rule, practised on 3 mock papers.",
 ('G8', 3): "Two-minute breathing routine before tests; counsellor check-in if screened anxiety is elevated (T3, support only).",
 ('G9', 1): "Learner writes the expected score before marking; show the predicted-versus-actual trend weekly.",
 ('G9', 2): "Use the 1 to 5 confidence rating on every item; review only the 'confident and wrong' items together.",
 ('G9', 3): "Keep a 'solved without help' list and look at it before tests.",
 ('G10', 1): "Fixed time, fixed place, one goal: 20-minute blocks on 5 days, one subtopic. A planner event each day (M15); the parent only asks 'did you do the 20 minutes?'",
 ('G10', 2): "Learner picks which of 2 subtopics to start; the first task is at D1 so success comes within 5 minutes.",
 ('G10', 3): "If burnout or social difficulty is flagged, route to the counsellor (M3) before any academic push.",
 ('ANY', 1): "Buy targeted sessions (2 a week for 4 weeks) with a written list of the diagnosed gaps; re-test with the same paper after 4 weeks.",
 ('ANY', 2): "Only if device and internet are adequate; use it for practice sets and spaced retrieval, not for teaching.",
}

# minutesPerSession, sessions (over the plan), spreadWeeks, requiresDevice, kind
PLAN = {
 ('G1', 1): (40, 2, 1, False, 'lesson'), ('G1', 2): (30, 2, 1, True, 'video'), ('G1', 3): (30, 2, 1, False, 'peer'),
 ('G2', 1): (15, 3, 1, False, 'practice'), ('G2', 2): (25, 1, 1, False, 'lesson'), ('G2', 3): (10, 2, 1, False, 'practice'),
 ('G3', 1): (20, 2, 1, False, 'practice'), ('G3', 2): (30, 3, 1, False, 'practice'), ('G3', 3): (5, 6, 1, False, 'habit'),
 ('G4', 1): (5, 6, 2, False, 'habit'), ('G4', 2): (15, 6, 2, False, 'practice'), ('G4', 3): (0, 0, 0, False, 'wellbeing'),
 ('G5', 1): (30, 2, 1, False, 'practice'), ('G5', 2): (20, 1, 1, False, 'practice'), ('G5', 3): (20, 1, 1, False, 'practice'),
 ('G6', 1): (8, 4, 3, False, 'retrieval'), ('G6', 2): (10, 1, 1, False, 'retrieval'), ('G6', 3): (10, 1, 1, False, 'retrieval'),
 ('G7', 1): (10, 3, 1, False, 'habit'), ('G7', 2): (30, 1, 1, False, 'practice'), ('G7', 3): (15, 1, 1, False, 'peer'),
 ('G8', 1): (20, 6, 3, False, 'practice'), ('G8', 2): (40, 3, 2, False, 'mock'), ('G8', 3): (5, 1, 1, False, 'wellbeing'),
 ('G9', 1): (2, 3, 1, False, 'habit'), ('G9', 2): (10, 1, 1, False, 'review'), ('G9', 3): (5, 1, 1, False, 'habit'),
 ('G10', 1): (20, 5, 1, False, 'habit'), ('G10', 2): (5, 1, 1, False, 'habit'), ('G10', 3): (30, 1, 1, False, 'wellbeing'),
 ('ANY', 1): (60, 8, 4, False, 'tuition'), ('ANY', 2): (20, 5, 1, True, 'app'),
}

items = []
for r in range(2, ws.max_row + 1):
    code = ws.cell(r, 1).value
    if not code or not ws.cell(r, 2).value:
        continue
    rank = int(ws.cell(r, 2).value)
    v = [ws.cell(r, c).value for c in range(1, 12)]
    inr = str(v[7]).replace(',', '')
    lo, hi = (inr.split('–') + [inr])[:2] if '–' in inr else (inr, inr)
    mins, sessions, weeks, device, kind = PLAN[(code, rank)]
    params = sorted({f"p{int(n)}" for n in re.findall(r'#(\d+)', v[10] or '')}, key=lambda s: int(s[1:]))
    items.append({
        "id": f"int-{code.lower()}-{rank}", "gapCode": code, "rank": rank, "name": v[2],
        "whatToDo": GENERIC[(code, rank)], "exampleCbseG8Maths": v[3], "timeCost": v[4],
        "minutesPerSession": mins, "sessions": sessions, "spreadWeeks": weeks,
        "totalMinutes": mins * sessions, "effort": v[5].lower(), "money": v[6].lower(),
        "inrPerMonth": {"min": int(lo), "max": int(hi)}, "kind": kind, "requiresDevice": device,
        "alrIndices": [s.strip() for s in str(v[8]).split(',') if s.strip() not in ('–', '')],
        "evidence": v[9], "feasibilityParams": params,
    })

out = {"schemaVersion": 1, "generatedBy": "scripts/engines/export-interventions.py",
       "source": "CBSE Class 8 Maths Assessment v4, sheet Interventions",
       "orderOfOperations": ws.cell(35, 1).value, "items": items}
json.dump(out, open('data/catalogues/interventions.json', 'w'), indent=1, ensure_ascii=False)
print(len(items), 'interventions')
