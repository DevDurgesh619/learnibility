# Onboarding test forms (QB-ONB)

The starting test every new student takes (about 50 minutes). It seeds about 110 of the 430 profile parameters
at low confidence and opens suspected gaps for the first plan.

## Files

| Path | What |
| --- | --- |
| `data/questions/onboarding/{formId}.json` | One form per board, grade and stream: `{schemaVersion, generatedBy, form, items}` |
| `data/questions/onboarding/index.json` | List of forms with item counts |
| `data/questions/onboarding/_status.json` | Validator result (`validated: true` only when all 27 files from 15 designs pass) |
| `lib/types/onboarding.ts` | `OnboardingForm`, `OnboardingFormFile`, item types, `LadderRule`, `OnboardingScoringMap` |
| `lib/onboarding/ladder.ts` | `nextDifficulty`, `nextItem`, `pickAtLevel`, `runGroup` (pure) |
| `lib/onboarding/score.ts` | `scoreOnboarding(file, responses, ctx)` → group bands, suspected gaps, reasoning, RIASEC, `ProfileValue[]` |
| `scripts/onboarding/` | Builder, content, validator and authoring aids (below) |

Form ids: `onb-{board}-g{grade}-{stream}`, stream `none` for grades 8-10, else `science`, `commerce`, `humanities`.
Item ids: `{formId}-qNN`. 15 designs (3 boards x grades 8-10, plus 3 streams x grades 11-12) give **27 files**: each
senior design is emitted once per board with that board's refs and swaps.

## Parts

- **A, academic (8 items per subject group, 21 in the pool).** Slots 1-4 probe last year's prerequisites
  (grade 8 probes grade 8 foundations and carries a `prerequisiteNote`), slots 5-8 this year's early chapters.
  Slot 1 holds a D2 item, slot 2 D1+D2, slots 3-8 D1+D2+D3. Ladder: start D2, one level down after a miss,
  one up after two hits in a row, within D1-D3. One item per slot is shown. Every item has `subtopicId`
  (linked to `data/curriculum`) and `likelyGapOnWrong`: prerequisite misses G1; this-year D1 G1, D2 G2, D3 G3.
  At scoring time `G4` (D2 wrong while a D3 in the group was right), `G8` (over twice the target time) and
  `G9` (confidence 4-5 and wrong) are added as secondary flags. Groups: 4 for grades 8-10 and most senior forms;
  IB Commerce has 3 (no Accountancy).
- **B, reasoning (16):** numerical, verbal, abstract, spatial, 4 each; band by grade (8, 9-10, 11-12).
- **C, self-report (30):** study habits, wellbeing (stress items are T3, screened and optional), interests,
  12 RIASEC items (2 per letter) → `p200`.
- **P, parent (16):** family context, budgets (with INR ranges), abroad budget, consent `p30` (required).

Score percent = earned weight (1/2/3) ÷ (items seen x 3). Bands: <45 below_avg, 45-64 average, 65-79 above_avg,
≥80 excellent.

## Commands

```bash
python3 scripts/onboarding/build-forms.py          # regenerate all forms
node scripts/onboarding/validate.ts [--write]      # validate (uses scripts/questions/validate.ts); --write updates _status.json
python3 scripts/onboarding/refs.py content.g11_science   # show which subtopic each slot resolves to, per board
python3 scripts/onboarding/outline.py cbse-g10-maths --chapters 3   # print a subject outline
npx vitest run lib/onboarding                      # ladder and scoring tests
```

## Authoring

Content lives in `scripts/onboarding/content/`. `dsl.S(ref, hint, items)` is one slot; `dsl.G(group, label, pre, cur)`
a group. An item is `(stem, correct, [3 wrong], why)`. A ref is `"subjectId:chapter:subtopic"`, a `{board: ref}` dict,
or a keyword ref from `dsl.K(grade, subject, keywords)` that resolves to the first subtopic (in chapter order) whose name
contains a keyword; the builder fails if nothing matches. A slot can also be `{board: S(...)}` for a board swap
(used where one board has no matching topic that year, e.g. CBSE Class 12 Biology opens with reproduction).
Senior banks: `senior_sci.py`, `senior_com.py`, `senior_hum.py`.
