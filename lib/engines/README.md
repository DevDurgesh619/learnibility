# Learnibility engines (`/lib/engines`)

Eight rule-based engines as pure TypeScript functions. No database, no I/O, no clock: every function takes
`now` (ISO UTC) when it needs time. Every number comes from `config.ts`, which cites the sheet and cell of the
CBSE Class 8 Maths Assessment v4 workbook (`reference/cbse-class8-maths-assessment-v4.xlsx`) it was copied from.

```ts
import { masteryTime, diagnoseGaps, planInterventions, computeAlr, buildTimetable,
         matchTutors, mapCareers, careerGap, nextBestAction } from '@/lib/engines';
```

Tests: `npx vitest run lib/engines` (137 tests; 99.7% line coverage; engines 6 and 7 also run on the real W4 catalogues). The workbook examples are extracted to
`__fixtures__/maths8.json` by `scripts/engines/extract-fixtures.py` and the tests compare against them.

| # | Engine | File | Source sheets | Workbook check |
|---|--------|------|---------------|----------------|
| 1 | `masteryTime(subtopic, band)` | masteryTime.ts | Mastery Inputs, Mastery Time, Mastery Summary | All 45 subtopics × 4 bands and all 14 chapter totals reproduce **exactly** |
| 2 | `diagnoseGaps(responses, questions, ctx)` | diagnoseGaps.ts | Gap Diagnosis, Gap Calculator | Gap Calculator (lrn_example, square roots, Average → L3, G5, size 2, 2.2 h, 0.7 wk, 6 opportunities) and Gap Log row (L2, G3, 3.6 h, 1.2 wk) |
| 3 | `planInterventions(gaps, profile, ctx)` | planInterventions.ts | Interventions, Gap Calculator §4 | Same 3 ranked interventions, add-on text and money check as C62–C66 |
| 4 | `computeAlr(inputs, weights)` | alr.ts | ALR Method, ALR Tracker | Row 1 → dK 0.75, R 0.89, TQ 0.80, CE 0.77, ECV 0.67, MCI 0.75, LRS 0.79, Above average |
| 5 | `buildTimetable(input)`, `replanTimetable`, `toIcs` | timetable.ts | Mastery Inputs r16–17, Interventions G6-1, blueprint | Scenario tests |
| 6 | `matchTutors(gaps, profile, tutors, ctx)` | matchTutors.ts | W3 brief, PDF area 5, `Tutor` type | Scenario tests |
| 7 | `mapCareers(profile, careers, ctx)`, `careerGap(profile, career, ctx)` | careers.ts | W3 brief, 430 file "Sensitivity Tiers", `Career`/`Skill`/`Resource` types | Scenario tests |
| 8 | `nextBestAction(state)` | nextBestAction.ts | Blueprint daily loop | Scenario tests |

## 1. Mastery time (Mastery Inputs B4)

```
instruction   = teaching periods × 40 min           (weight default L 2, S 3, H 4 periods)
learn         = instruction × absorption + instruction × guided-practice fraction
opportunities = ROUNDUP((80 − start accuracy) ÷ 2.5)          → 20 / 14 / 10 / 6
master        = learn + opportunities × min-per-opportunity (L 2.5, S 3.5, H 5) × error-correction factor
                + retrieval sessions × 8 min
practice beyond class = master − instruction
```

| Band | start % | absorption | guided | error-corr. | retrievals |
|---|---|---|---|---|---|
| below_avg | 30 | 1.25 | 0.5 | 1.4 | 4 |
| average | 45 | 1.0 | 0.4 | 1.2 | 3 |
| above_avg | 55 | 0.9 | 0.35 | 1.1 | 2 |
| excellent | 65 | 0.8 | 0.3 | 1.0 | 2 |

Hours round to 0.1 (half away from zero, like Excel). `chapterTimeSummary` sums the rounded rows and adds
suggested weeks = periods ÷ 6 + 0.25. `masteryTime(sub, band, overrides)` accepts a learner's measured
parameters. `scripts/engines/fill-mastery-hours.ts --write` fills `learnHours`/`masterHours` in every
`data/curriculum/*.json` (checked on cbse-g8-maths: 45/45 equal to the workbook).

## 2. Gap diagnosis (Gap Diagnosis §A–C, Gap Calculator C29–C58)

The workbook's fixed path (L 5 items, S 6, H 8) is expressed by concept group and difficulty so it works on any subject:

- C1 passed = any C1 item right · C2 = easiest C2 item right · C3 = easiest C3 item right (C3-D2)
- C4 passed = easiest C4 right, or all other transfer probes right when there are ≥ 2 (sheet: Q7 OR (Q6 AND Q8))
- Level: !C1 → L0, !C2 → L1, !C3 → L2, !C4 → L3, mastery rule (≥ 80% and C3 and C4) and 7-day retention ≥ 70% → L5, else L4
- Primary: ≥ 2 blanks → G10; L0 → G1 (G2 if the prerequisite probe passed); L1 → G2; L2 → G3; L3 → G5; L4 → G6 if retention < 70% else G4
- Secondary flags: G4 careless (D2 wrong, D3 right, same group); G7 language (word-problem pattern; auto-detected from item types when no signal is given); G8 speed (> 1.2 × allotted time and last item wrong/blank); G9 calibration (mean confidence on wrong items ≥ 4; *added:* mean ≤ 2 on right items); G10 engagement (≥ 2 blanks)
- Fewer than 4 attempted → `insufficientEvidence`, no primary (except G10)
- Hours to close = MASTER hours × level fraction (L0 1.0 + 0.4 prerequisite repair if G1, L1 0.85, L2 0.65, L3 0.4, L4 0.15, L5 0); 35% with a teacher, 65% self; weeks = hours ÷ weekly hours; split advice above 2 weeks
- Gap status `suspected` until the confirming probe; `confirmed` when a G1 prerequisite probe fails

## 3. Interventions (Interventions sheet, Gap Calculator C62–C68)

Catalogue: `data/catalogues/interventions.json` (32 rows: 3 per gap code + ANY-1 paid tuition + ANY-2 app), wording
made subject-neutral with the maths text kept as `exampleCbseG8Maths`, plus planning minutes. IDs `int-{code}-{rank}`.

- G1 gaps first, then by hours to close. Each gap gets its 3 ranked free interventions (video/app ones dropped when
  `p193` device check fails) plus the rank-1 intervention of each secondary flag.
- Paid tuition (₹2,000–6,000 a month) only when gaps span **2+ chapters and the free plan has run 3+ weeks**, or a parent asked.
- Money check, device check and re-test rule texts are the workbook's. Re-test after the planned weeks (min 7 days), retention probe 7 days later.
- Budget from `p178` (rupees or band), weekly hours from `p31`; both can be passed in `ctx`.

## 4. ALR (ALR Method, ALR Tracker)

dK = (post − pre)/(100 − pre); R = min(1, 7-day/post on retention probes); TQ = transfer %/practised %;
CE = dK ÷ (taken/allotted) × (1 − hint rate); ECV = 1/mean attempts; MCI = 1 − mean|confidence − correct|.
LRS = weighted sum with dK, TQ, CE capped at 1 (weight sets `default`, `exam_oriented`, `deep_mastery` (default)).
Bands: ≥ 0.80 excellent, ≥ 0.65 above_avg, ≥ 0.45 average, else below_avg. Weighted % uses D1–D5 = 0.8–1.6 × marks.
**Deviation:** a missing index is left out and weights rescaled (the sheet counts blank as 0). Also `alrInputsFromResponses`,
`alrYearToDate`, `normaliseLrs` (cohort min-max, Tracker note B21).

## 5. Timetable

Places blocks into the learner's study windows (local time, `tzOffsetMinutes`, default 330 IST) in priority order:
fixed sessions and locked blocks → Saturday weekly test (45 min) → carried-over missed tasks → spaced reviews due
1/3/7/14/30 days after `lastTestedUtc`, on the due day (10 min: 8-min retrieval + marking) → gap blocks (30 min, 20 for G10;
hours to close ÷ planned weeks per week; G1 first; one block per gap per day before doubling) → current-chapter practice.
15% of each day's free time is a buffer block at the end. `replanTimetable(prev, input, change)` handles `missed`,
`test_result` and `lock`: past blocks are kept as done, missed ones carried over, work already done is not re-planned.
`toIcs(blocks)` exports RFC 5545 (buffers left out). Anything that does not fit is listed in `unscheduled`.

## 6. Tutor matching (weights from the W3 brief)

topic 40 (subject+board+grade 20; a `topicStrengths` tag in the chapter/subtopic name 40; hour-weighted over gaps) ·
style 20 (primary style is what the dominant gap needs, e.g. G2 concept-first/Socratic, G3 practice-first, G8 exam-focused; secondary 12; else 4) ·
price 15 (≤ hourly budget = 15, linear to 0 at 2×; unknown 8) · rating 10 (Bayesian, prior 4.0 × 10 reviews) ·
slots 10 (weekly overlap, 2 sessions = full; tutor slots are read in `tutor.timeZone`, learner windows in `tzOffsetMinutes`, default IST) · language 5. Filters mode/city/format; unverified −5; tutors who teach none of
the gap subjects are dropped. Each result has a one-line `reason`.

## 7. Career mapping

Fit = interests 35 (RIASEC `p200`) + aptitude & academics 35 (career `aptitudeParamIds` scores, class % vs pathway minimum)
+ skill evidence 15 (current/target, core ×2) + feasibility 15 (stream fit, best pathway's cost vs budget: `p180` India UG
ceiling × years for India pathways, `p181` total for abroad ones, else `p178` × years).
**T3 values are removed before anything is read.** Missing evidence = neutral 0.5 and a lower `confidence`.
`careerGap` gives per-skill hours from `Skill.hoursPerLevel` (or mastery-model hours for academic skills), a free route
(free resources, ₹0) and a paid route (cheapest course reaching the target, else tutor hours = 35% × hours × ₹600;
planned at 75% of the self-study hours), months at weekly hours, and each pathway's
cost, years to entry and exam prep hours/fees.

## 8. Next best action

deadline ≤ 14 days (100 − 3/day) · reviews due (85+) · weekly test on/after its day (82; 40 earlier) · biggest gap
(55 + 3 × hours, G1 +5, max 80; next two −10) · profile < 80% (30+) · career exploration when none shortlisted
(20; 10 in grade 8). Each action carries a reason and an optional `href`.

## Budgets in the profile

The 430 file defines `p178` as the **annual** education budget, `p180` as the annual India UG ceiling and `p181` as the
total abroad budget. Engines read integer rupees, text such as "₹75,000", "1.5 lakh", "50k" or a range (midpoint), or a
band label (`none`, `low`, `medium`, `high`, `very_high`; see `ANNUAL_BUDGET_BANDS`, `INDIA_UG_BANDS`,
`ABROAD_TOTAL_BANDS`). Tutoring and tuition use `p178 ÷ 12` per month; pass `monthlyBudgetInr` to override.
Persona data should store these as integer rupees.
