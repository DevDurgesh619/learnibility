# Cambridge question bank generator (QB-CAM)

`generate.py <subjectId>` writes `data/questions/<subjectId>/` (one file per chapter with the mastery bank and practice Forms A/B, `mocks.json`, `_status.json`). Counts come from `plan.json` (cost sheet); subtopics from `data/curriculum/<subjectId>.json`. Then run `node scripts/questions/validate.ts <subjectId> --write`.

The only thing a subject needs is a content module: `content/<gN_slug>.py` (e.g. `cambridge-g12-business` → `content/g12_business.py`). `content/g10_physics.py` is the worked example.

## Writing a content module

```python
from ._lib import topic, mcq, compose, relation, sf, sci, person, city
PROFILE = {'mark_scale': {'long': (1.5, 1.5)}, 'wordy': True}   # optional
CHAPTERS = {}                                                     # chapter order -> [Topic]

t = topic('Name shown in logs', 'keyword', 'another keyword')     # keywords match W2 subtopic names
t.fixed('C1', (1, 2), [(stem, answer, markingKey, [3+ distractors])])   # with distractors -> MCQ
t.fixed('C2', (2, 3, 4), [(stem, answer, markingKey)])                  # explain items

@t.add('C3', (2, 3, 4), 'numerical')       # parameterised template: (r: Random, D: int) -> dict
def calc(r, D):
    ...
    return {'stem': ..., 'answer': ..., 'key': ...}       # optional options/type/marks

relation(t, 'C2', (2, 3, 4), 'P = IV', 'power', {'current': 1, 'p.d.': 1}, contexts)   # proportional reasoning
CHAPTERS[1] = [t, ...]
```

- One Topic per W2 subtopic (read the subtopic names in the curriculum file first; give each topic keywords from its name).
- Demand per chapter is roughly bank + 2 forms + mock share (run `capacity.py <subjectId>`): about 15% C1, 30% C2, 35% C3, 20% C4. Every stem must be unique and not a near-duplicate (word 3-gram Jaccard ≥ 0.85 within a chapter), so fixed lists run out; parameterised templates and `compose` (multi-part structured questions from a scenario + random subset of parts, part marks as a trailing `[n]` in each part key) carry the volume. Fixed C1/C2 entries are also auto-paired into two-part items.
- Use the board's command words (State, Describe, Explain, Calculate, Suggest, Evaluate, Discuss, To what extent) and international contexts (`person`, `city`).
- MCQ answer must be exactly one of the 4 options (`mcq()` handles this).
