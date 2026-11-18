# Curriculum map (W2)

Owner: W2 Curriculum map. Files: `data/curriculum/` (generated, do not hand-edit), `scripts/curriculum/` (sources, build, validator).

## Files

- `subjects.json`: `DataFile<Subject>`, all 157 subjects the cost sheet counts (rows marked Y).
- `{subjectId}.json`: `{ schemaVersion, generatedBy, subject: Subject, items: Chapter[], subtopics: Subtopic[] }`.
- `streams.json`: one item per board, grade and stream with `offerings: [{ seat, subjectId, name, note? }]`. A subject shared by two streams (CBSE Economics in Science and Commerce) has one ID and appears under both. `subjectId: null` marks optional papers outside the question bank.
- `sheet-reference.json`: cost-sheet facts per subject (chapter count, sheet chapter names, question target and plan: bank per chapter, practice tests, mocks) plus board totals. The validator checks against it.

## Rules

- IDs: subject `{board}-g{grade}-{slug}`, chapter `{subjectId}-ch{NN}`, subtopic `{chapterId}-st{N}`; positions are 1-based and stable.
- 3 to 5 subtopics per chapter, weight L/S/H. Teaching periods are 40-minute periods: weight gives H 4, S 3, L 2 (the class 8 maths workbook ratios), scaled per subject to the programme's annual instruction time (CBSE 150/yr in grades 8-10 and 200 in 11-12; Cambridge Stage 9 150, IGCSE 100, AS/A Level 270; IB MYP 120, DP 180; languages 80% of that), with the scale factor kept between 0.6 and 1.5.
- `prerequisiteIds` point to earlier subtopics in the same subject or to subtopics in earlier grades (or same-grade subjects) of the same board; the graph is acyclic. `prerequisiteNote` always says, in words, which earlier skill to probe (the workbook's Prerequisite Map column), including skills outside the map.
- `cbse-g8-maths` reproduces the class 8 maths workbook exactly (14 chapters, 45 subtopics, 145 periods, same weights and prerequisites), via `scripts/curriculum/import_cbse_g8_maths.py`.
- `learnHours` and `masterHours` come from W3's mastery-time engine (`npx tsx scripts/engines/fill-mastery-hours.ts --write`); `build.py` keeps them when it regenerates. Re-run the fill after changing weights or periods.

## Subject slugs

Slugs follow the cost sheet's subject seat, the same on every board, so a stream's offer reads the same across boards. Where a board teaches a different real course in that seat, `name` and `programme` say which (for example `ib-g11-political-science` is IB Global Politics).

| Slug | Name(s) | Boards and grades | Cost-sheet row label |
| --- | --- | --- | --- |
| `accountancy` | Accountancy, Accounting | cbse 11,12; cambridge 11,12 | Accounts |
| `applied-maths` | Applied Mathematics, Mathematics: Applications & Interpretation, Probability & Statistics 2 | cbse 11,12; cambridge 12; ib 11,12 | Maths - stats |
| `biology` | Biology | cbse 11,12; cambridge 9,10,11,12; ib 11,12 | BIO, Biology |
| `business` | Business, Business Management, Business Studies | cbse 11,12; cambridge 11,12; ib 11,12 | bussiness studies |
| `chemistry` | Chemistry | cbse 11,12; cambridge 9,10,11,12; ib 11,12 | Chemistry |
| `computer-science` | Computer Science | cbse 11,12; cambridge 11,12; ib 11,12 | Comp science |
| `economics` | Economics | cbse 11,12; cambridge 11,12; ib 11,12 | ECO |
| `english` | English, Language & Literature (English) | cbse 8,9,10,11,12; cambridge 8,9,10,11,12; ib 8,9,10,11,12 | English, english |
| `entrepreneurship` | Entrepreneurship | cbse 11,12 | Enterprenuership |
| `environmental` | Environmental Management, Environmental Systems & Societies | cambridge 11; ib 11,12 | Enviormental science, enviormental science |
| `geography` | Geography | cbse 11,12; cambridge 9,10,11,12; ib 11,12 | Geography, Social science – Geography |
| `hindi` | Hindi, Language Acquisition (Hindi) | cbse 8,9,10,11,12; cambridge 8,9,10; ib 8,9,10,11,12 | Hindi, hindi, hindi (Course A) |
| `history` | History | cbse 11,12; cambridge 9,10,11,12; ib 11,12 | History, Social science – History |
| `informatics` | Digital Society, Informatics Practices, Information Technology | cbse 11,12; cambridge 11,12; ib 11,12 | IP and information practice |
| `legal-studies` | Law, Legal Studies | cbse 11,12; cambridge 11,12 | Legal studies |
| `maths` | Mathematics | cbse 8,9,10,11,12; cambridge 8,9,10,11,12; ib 8,9,10,11,12 | Maths, maths |
| `physics` | Physics | cbse 11,12; cambridge 9,10,11,12; ib 11,12 | Physics |
| `political-science` | Global Perspectives & Research, Global Politics, Political Science | cbse 11,12; cambridge 11,12; ib 11,12 | pol science |
| `psychology` | Psychology | cbse 11,12; cambridge 11,12; ib 11,12 | Psychology |
| `science` | Science, Sciences | cbse 8,9,10; cambridge 8; ib 8,9,10 | Science, science |
| `social-science` | Humanities (People, Past, Places), Individuals & Societies, Social Science | cbse 8,9,10; cambridge 8; ib 8,9,10 | Social science, social science |
| `sociology` | Social & Cultural Anthropology, Sociology | cbse 11,12; cambridge 11,12; ib 11,12 | Sociology |

Not subjects: Cambridge grade 11 commerce "Maths - stats" is the same course as `cambridge-g11-maths`; optional papers marked N (CBSE 9 Maths/Science at Advanced Level, CBSE 10 Hindi Course B) and rows "NOT OFFERED on this board".

## Commands

```
python3 scripts/curriculum/check_source.py [subjectId...]   # authoring checks on source files
python3 scripts/curriculum/build.py                         # regenerate data/curriculum/
npx tsx scripts/curriculum/validate.ts                      # contract + cost-sheet validation
```
