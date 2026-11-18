# QA report (W3-QA integration pass)

**Result: ready to demo end to end.** Everything below was run on a clean export of `main` at 9f63a3d (18 Nov 2026, about 09:45 to 10:30 UTC) with a fresh `npm install`, against a production build (`next build && next start`), plus the integration fixes listed at the end, re-checked after a rebuild.

## Checks

| Check | Command | Result |
| --- | --- | --- |
| Type check | `npm run lint` | pass |
| Unit tests | `npm test` | 222 of 222 pass (19 files) |
| Production build | `npm run build` | pass |
| Curriculum | `node scripts/curriculum/validate.ts` | 157 subjects, 1,982 chapters, 7,288 subtopics, 0 errors |
| Question banks (finished subjects) | `node scripts/questions/validate.ts <id>` for every subject whose `_status.json` says validated | 82 of 82 valid (one subject was still being generated and is not counted) |
| Onboarding forms | `node scripts/onboarding/validate.ts` | 27 of 27 forms, 15 of 15 designs |
| Catalogues | `npx tsx scripts/catalogues/validate.ts` | pass (tutors 41, careers 40, skills 65, resources 85, universities 62, exams 32) |
| Persona stories | `npx tsx scripts/personas/check-stories.ts` | 13 student stories hold, Zoya is new, IDs resolve across 14 students, 20 adults and 7 classes, no T3 value in parent, teacher, tutor or mentor-facing data |
| Smoke specs (8) | `node scripts/smoke/{w2-a,w2-c,w2-p,w2-s1,w2-s2,w2-t,w2-te,w3-crm}.spec.ts` with `FLOW=1` | all pass, on persona data |
| Cross-role journey | `npx tsx scripts/e2e/journey.spec.ts` | 9 of 9 hops: CRM convert → onboarding test → gaps and timetable → tutor demo booked → tutor accepts and files a report → homework in Zoya's tasks → parent sees booking and spend → counsellor caseload → sales won +1 |
| Consistency | `npx tsx scripts/e2e/consistency.spec.ts` | 194 checks pass for Kabir, Rohan, Ishita, Sara and Vihaan: open gaps, hours to close, learning rate, band, gap names, timetable blocks and spend read the same on student, parent, teacher (scoped to the section's subject), counsellor and tutor screens |
| Privacy | `npx tsx scripts/e2e/privacy.spec.ts` | 498 pages across 26 parent, teacher, tutor, mentor and sales personas: no T3 parameter name and no wellbeing check-in wording |
| Guided demo | `npx tsx scripts/e2e/demo.spec.ts` | all 12 scenarios, 120 step visits at 1440 and 390 px: no errors, guide panel present, no overflow |
| Every sidebar link | `npx tsx scripts/e2e/routes.spec.ts` | 42 personas, 1,198 page loads at 1440 and 390 px: no HTTP errors, no placeholder pages, no console errors, all under 2 s (slowest 301 ms, counsellor Student 360). 12 phone overflows found and fixed (below) |
| Copy | grep and review | rupees are `₹` with Indian grouping everywhere; dates come from the IST demo clock; names match the persona list |

## Fixed during the pass

- **Silent reversion on main.** Commit 318a9ab (a question-bank commit) swept stale index entries in and put 11 counsellor and teacher files back to older versions, and deleted the W2-C and W2-TE screenshots. Restored byte for byte in 42caea0.
- **Orphaned commit.** d648c3a (Cambridge curriculum check-path fit) was not on main; re-landed as 09d8dd3. The other 20 unreachable commits were superseded by later commits and lost nothing.
- **One band everywhere** (coordinator decision): every role shows `student.band`, the planning band that drives hours. The teacher's page labels a chapter's band "Latest chapter"; a test result says "band on this test" (54cc868).
- **Copy:** counsellor Home said "1 students with a high flag" (54cc868).
- **About form** is prefilled from the learner record after the CRM's Convert to platform (54cc868).
- **Phone layout:** parent Sessions and payments and tutor student and session-prep pages overflowed at 390 px for the new persona families (long session titles in a grid with no column template). Seven grids now use `grid-cols-1` on phones.
- Reported to and fixed by the owning threads: new demo requests now show on the tutor's Home (57aaf79); every catalogue tutor can sign in, so any recommended tutor can be followed (d0f560b); Zoya's mother Maria Fernandes is a parent persona (W3-P).

## Open items

- **Shared-repo commits.** Some commits still bypass `build/safe-commit.sh` (it lost the HEAD race several times during the pass). It does no harm once the work stops, but if more threads commit, re-run `git fsck --unreachable --no-reflogs` and check new commits for reverted files before the GitHub push.
- **Question bank** is still growing; the validator count above covers the 82 subjects finished at 9f63a3d. Personas notes: after big bank landings rerun `npx tsx scripts/personas/simulate.ts` and `check-stories.ts`.
- **Load time** was measured on a production build. A first visit on `npm run dev` compiles each route once and can take a few seconds; warm the demo routes before presenting (opening `/demo` and starting each scenario once does it).
