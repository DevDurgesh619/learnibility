# Decisions log

Newest first. Each entry: date, decision, who decided, why.

## 2026-11-18

- **Stack.** Next.js 16 App Router, TypeScript (strict), Tailwind CSS 4, shadcn/ui conventions (`components.json`, `lib/utils.ts`), Recharts, Vitest. Prisma with SQLite locally and a Postgres-compatible schema (W1 milestone 2). Persona-picker login, no real auth. (Blueprint, "Suggested stack".)
- **Boards.** CBSE, Cambridge (Lower Secondary Stage 9, IGCSE, AS and A Level) and IB. No ICSE. (User.)
- **Streams for grades 11 and 12.** Science, Commerce, Humanities. No Arts stream. (User.)
- **Question bank.** Full bank of 180,015 questions across 1,982 chapters, per the cost sheet (CBSE 63,582; Cambridge 62,540; IB 53,893). Generated in Wave 2. (User.)
- **Platform.** Web first, responsive. CRM is a dummy flow added after the core app; no real Zoho integration. (User.)
- **Repository.** No GitHub repo yet. The shared codebase is a local git repo at `/mnt/project-files/learnibility/`; commits to `main` stand in for merged PRs until the user attaches GitHub. (Coordinator.)
- **Lowercase practice-form IDs.** `pfa` / `pfb`, because all IDs are lowercase. (W1.)
- **430-parameter provenance.** Parameters 1 to 277 are imported unchanged from the user's 277-parameter workbook; 278 to 430 are v2 design proposals. Kept as `origin` on every parameter. (Source workbook READ ME.)

## 2026-11-18 (question bank, QB-CBSE)

- **Question-bank targets file.** `data/questions/targets.json` holds, per counted subject, bank questions per chapter, questions per practice form, mocks and questions per mock, from the cost sheet (rows marked Y; 157 subjects, 180,015 questions). The shared validator reads it. Built by `scripts/questions/build-targets.py`. (QB-CBSE.)
- **MCQ answer field.** For `type: 'mcq'`, `answer` is the exact text of the correct option; the option letter and reasoning go in `markingKey`. Options live in `options`, not in the stem. (QB-CBSE.)
- **Transfer probes.** Only C3-D4/D5 and C4-D3+ items carry `alrRole: 'transfer_probe'`, as in the class 8 maths workbook. (QB-CBSE, from the workbook.)

## 2026-11-18 (W1 Foundations, milestone 2)

- **Prisma 7 with the better-sqlite3 adapter.** Schema in `prisma/schema.prisma`, config in `prisma.config.ts`, client generated to `lib/generated/prisma` (git-ignored; `npm install` runs `prisma generate`). Swap the adapter for `@prisma/adapter-pg` when hosting on Postgres. (W1.)
- **JSON stays the source of truth.** The app reads `/data/**` JSON directly so the demo works without a database; `npm run db:setup` loads the same files into SQLite for screens that need live writes. Catalogue and persona rows keep their full record in a `data` Json column. (W1.)
- **Demo login.** Persona picker at `/login` sets a `learnibility_persona` cookie; each role area redirects to `/login` without one and to the persona's own role otherwise. Six role areas: student, parent, teacher, counsellor, tutor, mentor. (W1.)
- **Role visibility per tier** (`lib/visibility.ts`): student and counsellor see all tiers; parent sees T1 and C in full and T2/T3 as summaries only; teacher and mentor T1 only; tutor only parameters the student shared. T3 and consent records never feed ranking, admissions fit, career fit, tutor matching or work allocation. (W1, from the 430 file's Sensitivity Tiers sheet and the blueprint tier rule.)
- **Dummy plan prices** (user, 07:45: "use dummy pricing we will change it later") (Free ₹0, Application Support ₹4,999/month, Full package ₹7,999/month) until the user sets pricing. (W1.)
- **Demo clock.** `DEMO_NOW` = 2026-11-18 09:00 IST in `lib/demo-clock.ts`. (Personas brief.)

## 2026-11-18 (W2-0 Data layer)

- **Demo writes go to their own SQLite overlay, not the Prisma schema.** `lib/store/overlay.ts` keeps one table of `(collection, key, learnerId, data)` rows in `.data/overlay.sqlite` (better-sqlite3, already installed for Prisma's adapter), with a memory fallback for read-only hosting and tests. The Prisma schema's foreign keys need a fully seeded database that fixtures and contributed demo content are not in; a generic overlay lets every screen write without seeding and makes "Reset demo" a single delete. (W2-0.)
- **Source priority per learner:** `data/personas/students/{id}/` wins over `data/fixtures/students/{id}/`; `data/fixtures/contrib/*.json` adds demo content authored by screen threads; the overlay wins over both. (W2-0.)
- **Next best actions are computed on every read** from the current gaps, tasks, mastery and applications, so they change immediately after any write. (W2-0.)
- **Fixture learners use real persona ids** (Kabir, Rohan, Ishita, Sara, Nikhil, Ananya) so screens switch to Wave 3 data without code changes. Fixture questions use ids `{subtopicId}-q9NN` to avoid clashing with the real bank. (W2-0.)
- **Retention probes re-diagnose the last full check** with the probe's retention as the signal (L4 → L5, or G6 under 70%), because a 2-item probe alone is "insufficient evidence" for the engine. (W2-0.)

## 2026-11-18 (W2-S2 Student daily loop)

- **One data seam.** Every daily-loop screen reads through `components/student/load.ts`, which calls `@/lib/data` and `@/lib/engines` only; components render view models from `components/student/model.ts`. (W2-S2.)
- **Request change shows for any student with a counsellor** (`counsellorIds` not empty), not by plan, because Heena counsels all 14 students and `PlanId` has no counselling-only plan. Requests are `TimetableRequest` records (`kind: 'move'`, `proposed` slot, reason "task · repeat · why"); Undo marks them `declined` with note "Withdrawn by the student". (W2-S2.)
- **Ticking a timetable block** re-stores that week (`putRecord('timetable', …)`) with the block's status; tasks use `putRecord('tasks', …)`. Both append an M16 event. (W2-S2, per W2-0.)
- **Metric definitions (PDF 2b/2d).** Learning rate = mean latest LRS per chapter; retention = mean latest R per chapter; discipline = study blocks done ÷ planned so far this week (last week early in the week); task completion = non-timetable tasks done ÷ due in the last 7 days. The metric detail is `/student?metric=…` so it stays inside S2's routes. (W2-S2.)
- **Inventory folders.** `DocumentRecord` carries only the shelf, so the folder is derived: academics by school year (April to March) relative to the current grade, others by title and kind; uploads pin their folder with `refId: "folder:{slug}"`. (W2-S2.)
- **Next best action links** are remapped to final routes (engine's `/student/profile` → Inventory, `/student/careers` → `/student/career`). (W2-S2.)

## 2026-11-18 (W2-S1 student onboarding and assessments)

- **Routes.** Landing `/welcome` (1a), `/signup` (1b), `/signup/verify` (1c), `/signup/role` (1d), `/onboarding/{about,needs,profile,test,setup}` (1e-1g, starting test, 1i). Assessments: `/student/assessments` (8a), `/{testId}` (8b), `/{testId}/instructions` (8c), `/{testId}/take` (8d-8e), `/results/{attemptId}` (8f), `/gaps` (8g), `/topics/{subtopicOrChapterId}` (8h). (W2-S1.)
- **Test IDs.** `chk.{chapterId}` chapter check, `pfa.`/`pfb.{chapterId}` practice forms, `mock.{subjectId}.{n}` (paid, Full package), `onb.{formId}.{section}` initial tests, `task.{taskId}` any test task carrying `questionIds`. Submitting a test whose task is due marks the task done and sets `taskId`/`assignedBy` on the attempt. (W2-S1.)
- **Chapter check = the workbook student-check path.** Per subtopic, the first 5 / 6 / 8 mastery-bank items (L / S / H weight) in bank order, so `diagnoseGaps` sees C1-C4 on every subtopic. (W2-S1, from the class 8 maths workbook.)
- **Demo sign-in.** No SMS: OTP is always 246810 (shown on screen). 98110 00001/2/3 are returning Kabir, Ishita and Nikhil (skip to Home); any other number is the new student and logs in as Zoya. Only "Student" continues in 1d; other roles go to the persona picker. (W2-S1.)
- **1g option A ships** (profile questions with Skip, no paywall), as the PDF recommends; 1h is not built. A fourth onboarding step, the starting test, sits between 1g and 1i and can be deferred to Assessments. (W2-S1.)
- **Starting test UX.** Part A runs one subject group at a time on the adaptive ladder (no going back, "I don't know" option, confidence 1-5); Part B reasoning is timed; Part C is paged. The parent form (Part P) is left for the parent app. Answers stay on the device until 1i, where the server re-marks Part A and writes: Student record (subjects, default study windows, band from mean Part A percent, current chapter by school-year progress), profile values from `scoreOnboarding`, suspected gaps with hours (`masterHours[band] × level fraction`), one onboarding attempt per group, a first plan, then `recomputeLearner`. Each section has an "Answer the rest for me (demo)" shortcut with deterministic answers. (W2-S1.)
- **Marking.** MCQ exact; numerical and short compare the final number or normalised text; explain, multi-step, case and long use a demo stand-in for AI marking (final number matches, or at least half the key's content words). Answers are never sent to the browser for normal tests; the onboarding ladder marks in the browser because the next item depends on it, and the server re-marks. (W2-S1.)
- **Result bands on 8g** use the PDF words Strong (75%+), Medium (50-74%), Weak (<50%); the overall band on 8f uses the onboarding cut-offs. Gap codes come from `recomputeLearner`'s diagnosis (or the live engine when evidence was too thin). Cause text drops the 430-file parameter numbers for students. (W2-S1.)

## 2026-11-18 (W2-C Counsellor)

- **One rule set for counsellor risk flags.** Caseload and Risk flags both use `components/counsellor/risk.ts` (deadline under 14 days with open items, high under 7; wellbeing check-in 2 or below, burnout flag, stress or anxiety in the high band, no check-in for 35+ days; profile under 25% complete, sparse core sections, no assessment for 21+ days; learning rate below average, G10, 3+ skipped tasks in 7 days; request waiting over 48 hours). `getCaseload` supplies the students; its own flags are replaced so the two screens never disagree. (W2-C.)
- **Approving a timetable request** moves (or drops) the requested blocks, locks them in the new slot under the id `{blockId}_moved`, then calls `recomputeLearner(id, { reason: 'request_approved' })` so the rest of the week re-plans around them. Block length only changes for `more_time` / `less_time`. The student gets a message with the decision. (W2-C.)
- **Career session save** writes a `MeetingNote` (kind career, T1), a completed counsellor `Session`, one `Task` per action item (kind `action_item`, source `counsellor`, link `/student/career`) and an M3 `career_session` event. (W2-C.)
- **Student 360 staleness** uses the parameter cadence: Weekly/Continuous 10 days, Monthly 45, Term 140, Annual 400; Once and As needed never go stale. (W2-C.)
