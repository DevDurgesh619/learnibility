# Learnibility curriculum map: authoring rules (W2)

You are a subject-matter expert writing the syllabus map that a whole edtech app (question bank,
mastery engine, gap diagnosis, tutor matching) is built on. It must read like the real board syllabus
and textbook, not like generic filler. Boards: CBSE (NCERT), Cambridge (Lower Secondary Stage 9,
IGCSE, AS & A Level), IB (MYP 3-5, DP). Grades 8-12. Session 2026-27.

Repository root: the repository root   (work only inside scripts/curriculum/source/)

## What you write
One JSON file per subject: `scripts/curriculum/source/{subjectId}.json`

```json
{
  "subjectId": "cbse-g10-maths",
  "chapters": [
    {
      "sheetName": "Real Numbers",            // REQUIRED when your brief gives sheet chapter names: copy EXACTLY, same order
      "name": "Real Numbers",                 // full official chapter / unit / topic title as students see it
      "subtopics": [
        { "name": "Fundamental Theorem of Arithmetic and prime factorisation",
          "weight": "H",
          "prereq": ["cbse-g9-maths-ch03-st2"],
          "note": "Prime factorisation and HCF/LCM (Cl 6-7); The World of Numbers: irrational numbers" }
      ]
    }
  ]
}
```

Rules
1. Chapter count must equal the brief exactly. Where the brief lists sheet chapter names, use one
   chapter per sheet name in that order, with `sheetName` copied character for character and `name`
   the full official title (expand abbreviations: "EMI" -> "Electromagnetic Induction"; drop notes
   like "(PA only)" from `name` only). Where the brief gives only a description, design the chapter
   list yourself from the real syllabus guide / endorsed coursebook so the count matches; omit `sheetName`.
2. 3 to 5 subtopics per chapter (aim ~3.5 average; big chapters 4-5, small 3). A subtopic is one
   teachable, testable idea that takes 1-4 lessons, worded like the gold standard below. No duplicates
   inside a subject. Use real syllabus terminology (e.g. IB "B.2 Greenhouse effect", Cambridge
   learning-objective wording, NCERT section titles). Hindi subjects: write subtopic names in Hindi
   (Devanagari), e.g. "पाठ का भाव और संदेश", "व्याकरण: समास (पाठ से उदाहरण)".
3. weight: H = high exam weight or hard core skill, S = standard, L = light / introductory /
   enrichment. Target mix per subject ~30% H, ~55% S, ~15% L.
4. prereq: IDs of subtopics this one directly builds on. Allowed targets: earlier subtopics of the
   same subject, subtopics of earlier grades of the SAME board, or same-grade subjects in your own
   group (no cycles). Only IDs inside your own group's subjects (listed in your brief, plus any file
   your brief says already exists). ID = `{subjectId}-ch{NN}-st{N}` where NN is the 2-digit chapter
   position and N the subtopic position, both 1-based, in that file. 0-3 IDs per subtopic.
   The first chapters of grade 8 usually have none.
5. note: ALWAYS present. The prerequisite to probe when a student fails this subtopic, in plain words,
   like the gold standard: name the earlier skill and grade, e.g. "Angle sum of a triangle (Cl 7)",
   or "Moles and molar mass (IGCSE ch 5); rearranging formulae". If something outside the map is
   needed (earlier class, another board, a maths skill used in physics), say it here.
6. Do not set periods; the build script computes teaching periods from weights.
7. Write each subject file as soon as it is done (persona/priority subjects first, in the order in
   your brief). After each file run:
       python3 scripts/curriculum/check_source.py {subjectId}
   and fix every ERROR. A prereq to a subject you have not written yet will show as unresolved until
   you write it; run the check again for all your subjects at the end and leave zero errors.
8. Valid JSON, UTF-8, no comments. Do not edit files outside your own subject list.

## Gold standard (CBSE class 8 maths, from the client's workbook; file already exists:
scripts/curriculum/source/cbse-g8-maths.json). Excerpt:

| Chapter | Subtopic | Weight | Prerequisite to probe |
|---|---|---|---|
| A Square and a Cube | Perfect squares and their patterns | S | Multiplication tables to 20; square of a number (Cl 7) |
| A Square and a Cube | Square roots: prime factorisation and estimation | H | Prime factorisation (Cl 6-7); Perfect squares and their patterns |
| A Square and a Cube | Perfect cubes and cube roots | S | Prime factorisation; Perfect squares and their patterns |
| A Square and a Cube | Pythagorean triplets and square-number puzzles | S | Perfect squares and their patterns; Square roots |
| Power Play | Exponent notation and laws of exponents | H | Exponents as repeated multiplication (Cl 7) |
| Power Play | Zero and negative exponents | S | Exponent notation and laws of exponents |
| Power Play | Standard form for very large / small numbers | S | Zero and negative exponents; decimal place value |
| A Story of Numbers | Evolution of number systems and place value | L | Place value of whole numbers (Cl 6) |
| Proportional Reasoning-2 | Profit, loss, discount and tax | H | Percentages and percentage change |
| Area | Surface area and volume of cube, cuboid, cylinder | H | Area of rectangle and circle; Exponents (units squared/cubed) |

## When done
Reply with: files written, total chapters and subtopics, the check_source result for all your
subjects, and any chapter lists you had to design yourself (one line each, with the source you used).
