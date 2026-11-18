"""Extract the class 8 maths workbook examples the engine tests reproduce.

Usage: python3 scripts/engines/extract-fixtures.py reference/cbse-class8-maths-assessment-v4.xlsx
Writes lib/engines/__fixtures__/maths8.json
"""
import json, sys, re
import openpyxl

src = sys.argv[1]
wb = openpyxl.load_workbook(src, data_only=True)

def slug_ids():
    """Map chapter name -> chNN and subtopic name -> stN, in workbook order."""
    tp = wb['Teaching Plan']
    chapters, subtopics = {}, {}
    for r in range(2, tp.max_row + 1):
        ch, chn, st, order, w, periods = (tp.cell(r, c).value for c in range(1, 7))
        if not st or ch is None or not isinstance(ch, (int, float)):
            continue
        cid = f"cbse-g8-maths-ch{int(ch):02d}"
        chapters.setdefault(chn, {"id": cid, "order": int(ch), "name": chn, "subtopicIds": []})
        sid = f"{cid}-st{int(order)}"
        chapters[chn]["subtopicIds"].append(sid)
        subtopics[st] = {"id": sid, "chapterId": cid, "order": int(order), "name": st, "weight": w,
                         "teachingPeriods": periods, "testMinutes": tp.cell(r, 10).value}
    return chapters, subtopics

chapters, subtopics = slug_ids()

mt = wb['Mastery Time']
bands = ['below_avg', 'average', 'above_avg', 'excellent']
mastery_rows = []
for r in range(2, mt.max_row + 1):
    st = mt.cell(r, 3).value
    if not st or st not in subtopics:
        continue
    v = [mt.cell(r, c).value for c in range(1, 18)]
    mastery_rows.append({
        "subtopicId": subtopics[st]["id"], "name": st, "weight": v[3],
        "teachingPeriods": subtopics[st]["teachingPeriods"], "instructionHours": v[4],
        "learnHours": dict(zip(bands, v[5:9])), "masterHours": dict(zip(bands, v[9:13])),
        "practiceBeyondClassHours": dict(zip(bands, v[13:17])),
    })

ms = wb['Mastery Summary']
summary = []
for r in range(2, ms.max_row + 1):
    ch = ms.cell(r, 2).value
    if not ch or ch not in chapters:
        continue
    v = [ms.cell(r, c).value for c in range(1, 17)]
    summary.append({"chapterId": chapters[ch]["id"], "instructionHours": v[3],
                    "learnHours": dict(zip(bands, v[4:8])), "masterHours": dict(zip(bands, v[8:12])),
                    "suggestedWeeks": v[15]})

# Assessment questions (contract Question shape) for every subtopic
asm = wb['Assessment']
role_map = {'Retention probe (R)': 'retention_probe', 'Practised item (dK)': 'practised', 'Transfer probe (TQ)': 'transfer_probe'}
type_map = {'Worked numerical': 'numerical', 'Explain / reason (1-3 lines)': 'explain',
            'Multi-step problem': 'multi_step', 'Short answer / MCQ': 'short'}
questions = []
for r in range(2, asm.max_row + 1):
    qid = asm.cell(r, 1).value
    if not qid or asm.cell(r, 4).value not in subtopics:
        continue
    st = subtopics[asm.cell(r, 4).value]
    n = int(asm.cell(r, 6).value)
    questions.append({
        "id": f"{st['id']}-q{n:02d}", "legacyId": qid, "subtopicId": st["id"], "chapterId": st["chapterId"],
        "subjectId": "cbse-g8-maths", "conceptGroup": asm.cell(r, 7).value, "difficulty": asm.cell(r, 9).value,
        "type": type_map[asm.cell(r, 11).value], "stem": asm.cell(r, 12).value, "answer": asm.cell(r, 13).value,
        "markingKey": asm.cell(r, 13).value, "marks": asm.cell(r, 14).value, "minutes": asm.cell(r, 15).value,
        "alrRole": role_map[asm.cell(r, 16).value], "set": "mastery_bank"})

gc = wb['Gap Calculator']
g = lambda a: gc[a].value
gap_calc = {
    "learnerId": g('C4'), "subtopicName": g('C5'), "subtopicId": subtopics[g('C5')]["id"], "band": "average",
    "results": [g(f'C{r}') for r in range(10, 18)], "minutesTaken": g('C18'), "minutesAllotted": g('C19'),
    "meanConfidenceWrong": g('C20'), "retentionPct": g('C21'), "wordProblemPattern": g('C22') == 'Y',
    "prereqProbe": g('C23'), "weeklyHours": g('C24'), "monthlyBudgetInr": g('C25'), "deviceOk": g('C26') == 'Y',
    "expected": {"level": g('C37'), "size": g('C38'), "primary": g('C39'), "scorePct": g('C34'),
                 "overConfident": g('C47'), "careless": g('C44'),
                 "hoursByBand": dict(zip(bands, [g('C55'), g('D55'), g('E55'), g('F55')])),
                 "weeks": g('C57'), "practiceOpportunities": g('C58'),
                 "planNames": [g('C62'), g('C63'), g('C64')], "addOns": g('C65'), "moneyCheck": g('C66')},
}

at = wb['ALR Tracker']
row = [at.cell(4, c).value for c in range(1, 22)]
alr_row = {"chapterId": chapters[row[1]]["id"], "preWeightedPct": row[2], "postWeightedPct": row[3],
           "retentionPostPct": row[4], "retention7dPct": row[5], "practisedPct": row[6], "transferPct": row[7],
           "minutesTaken": row[8], "minutesAllotted": row[9], "hintRate": row[10], "meanAttemptsToMastery": row[11],
           "meanConfidenceError": row[12],
           "expected": dict(zip(['dK', 'R', 'TQ', 'CE', 'ECV', 'MCI', 'LRS'], row[13:20])), "expectedBand": row[20]}

gl = wb['Gap Log']
glr = [gl.cell(2, c).value for c in range(1, 18)]
gap_log = {"date": glr[0], "learnerId": glr[1], "subtopicId": subtopics[glr[3]]["id"], "band": glr[4], "level": glr[5],
           "primary": glr[6], "hours": glr[8], "weeks": glr[9]}

out = {"schemaVersion": 1, "generatedBy": "scripts/engines/extract-fixtures.py",
       "chapters": list(chapters.values()), "subtopics": list(subtopics.values()), "masteryTime": mastery_rows,
       "masterySummary": summary, "questions": questions, "gapCalculator": gap_calc, "alrTracker": alr_row,
       "gapLog": gap_log}
json.dump(out, open('lib/engines/__fixtures__/maths8.json', 'w'), indent=1, ensure_ascii=False, default=str)
print(len(mastery_rows), 'mastery rows;', len(questions), 'questions;', len(summary), 'chapters')
