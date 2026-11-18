# Catalogues (W4)

Data in `data/catalogues/`, types in `lib/types/catalogue.ts`. Regenerate with `npx tsx scripts/catalogues/generate.ts`, check with `npx tsx scripts/catalogues/validate.ts`.

| File | Items | Notes |
| --- | --- | --- |
| tutors.json | 41 | Rahul Verma plus 40 tutors across 17 subject families and all three boards. ₹300 to ₹1,500 an hour. |
| careers.json | 40 | Science, Commerce, Humanities. India pathway on every career, abroad pathways on most. |
| skills.json | 65 | Academic, future (430-profile params), technical, domain. `resourceIds` is filled in from resources. |
| resources.json | 85 | `res-` free resources and `course-` paid courses with hours, rupees and the skill levels they reach. |
| universities.json | 62 | 21 India, 15 US, 12 UK, 8 Canada, 6 Australia. 2027-intake routes and deadlines. |
| exams.json | 32 | Entrance and admission tests (JEE, NEET, CLAT, CUET, SAT, IELTS, UCAT, LNAT ...). Ids are plain slugs. |
| fx.json | 1 | Rupee rates used for every conversion (USD 88.5, GBP 117, CAD 63.5, AUD 58; as of 2026-11-18). |

## How engines should read them

**Tutor matching (engine 5).** A tutor can take a gap when the gap's subject slug is in `tutor.subjects[].subjectSlug` and the student's board and grade are in that entry. Topic match: slugify the gap's chapter and subtopic names and count a hit when every word of a `topicStrengths` tag appears there (e.g. `rotational-motion` matches "System of Particles and Rotational Motion"). Style fit uses `teachingStyles[0]` as primary. Price: `pricing.oneToOnePerHourInr` or `groupPerStudentPerHourInr`. Slots: `availability` is in `timeZone` (three tutors are abroad). Reason line material: `headline`, `topicStrengths`, `pricing.demoInr === 0` ("free demo").

**Career mapping (engine 6).** Interests: compare the student's RIASEC profile (p200) with `career.riasec` (strongest first). Aptitude: `aptitudeParamIds`. Skill gap: for each `career.skills` entry compare the student's level with `targetLevel`; academic skills carry `subjectSlugs` so hours come from the mastery model, the rest use `skill.hoursPerLevel`. Free route = cheapest free resources in `skill.resourceIds`; paid route = paid courses plus tutor hours. Feasibility: `pathways[].costInr` against p180/p181 budgets.

**Universities.** Every checkable fact is a `Sourced<T>` with `sourceUrl`, `asOf` and `verified`. Show "Source · as of" on screen and a muted "estimate" tag when `verified` is false. Reach / Target / Safe: start from `selectivity` and compare the student's predicted percentage with `applicationRoutes[].requirements.minBoardPercent`.

## Accuracy

Universities were researched on 18 Nov 2026: 140 of the core facts (rank, acceptance rate, international share, tuition, deadlines) are marked verified; the rest are realistic estimates pointing at the official page. UCAS equal-consideration deadline for 2027 entry is 13 January 2027. JEE Main 2027 session 1 registration closes 22 November 2026; CLAT 2027 is on 6 December 2026. Career salaries and city shares are realistic bands drawn from public salary sites and the National Career Service, not a single dataset. Tutors, reviews and ratings are fictional.
