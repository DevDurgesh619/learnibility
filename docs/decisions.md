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

## 2026-11-18 (W2-P Parent and mentor)

- **Child switcher by query string.** Every parent page takes `?child=lrn_...` (default: first child); the switcher shows only for families with 2+ children (the Kapoors). Helpers in `components/parent/context.ts`. (W2-P.)
- **Progress compares a child only with their own past.** The radar is now vs 4 weeks ago, the trend is LRS and MCI year to date; no class averages or ranks anywhere on parent screens. ALR indices the engine marked `missing` are left out of the means, as the LRS does. (W2-P.)
- **Paid tutor approval.** `lib/actions/parent.ts#approvePaidTutor` either approves a student-requested booking (`parentApproval.status` pending → approved) or, when the 3-week rule fired and nothing is booked, creates a regular booking for a matched tutor (`getTutorMatches`, subject with the most open hours) already parent-approved. Both write an `Approval` (kind `paid_tutor`), an `M2` event and `recomputeLearner(id, {reason:'session_booked'})`. The tutor still accepts. The gap snapshot goes to the tutor only when the family has an active `share_with_tutor` consent. (W2-P.)
- **Parent writes**: approve/decline tutor, pay invoice (demo success state, no gateway), give/withdraw consent (dated, versioned), send message. All check the learner is the signed-in parent's child. (W2-P.)
- **Privacy screen** uses `getProfile(id, 'parent')`, so T2 and T3 arrive as counts and dates only; it shows the `VISIBILITY` matrix from `lib/visibility.ts` as the "who sees what" table. (W2-P.)
- **Sample prices shown** (tutor rates, plan cost ranges, invoices, skill-plan paid routes) per the user's "use dummy pricing, we will change it later". (W2-P.)
- **Mentor writes live in `lib/actions/mentor.ts`** (new file, mentor-only): a career session saves a T1 `MeetingNote` (kind `career`) and turns each action item into a `Task` (source `mentor`, kind `action_item`); a skill-plan line can be sent as a task. Events use M18 (mentor rating) and M15 (planner). (W2-P.)
- **Skill plans are computed live** with `careerGap` plus the skills, resources and exams catalogues on the mentee's T1 profile, so routes name real resources; the stored `careers.json` gap is the fallback. (W2-P.)


## 2026-11-18 (W2-TE Teacher)

- **Assignments are one task per learner.** Assign and "Push re-teach set" write a `Task` (`kind: 'test'`, `source: 'teacher'`, id `{groupId}__{learnerId}`, `href: /student/assessments/task.{taskId}`) for every chosen learner, then `recomputeLearner(id, { reason: 'task_assigned' })` for persona learners. The "Assigned so far" list groups tasks by the id prefix. Chapter checks take the easiest item per subtopic and concept group (max 20); re-teach sets take C1 to C3 items at D1 to D3 (plus 2 C4 items for G5). (W2-TE.)
- **Gap validation writes three things.** The gap's `validation` (with `originalCode` kept when corrected), a `gap_validated` event (M15) and profile value `p430` (T1, M15). "Not a gap" closes the gap. Background learners' light gaps get a full record on first validation (id `gap_{learnerId}_{subtopicId}`). (W2-TE.)
- **Gap clusters are recomputed from gaps on the teacher side** (subtopic × code, open, rejected left out, 2+ students), so a correction shows at once; clusters of 3+ get a card (top 6), the rest a compact list. (W2-TE.)
- **Teacher student view is T1 only**, via `getProfile(id, 'teacher')`; background learners show heatmap mastery, gaps and test scores only. (W2-TE.)

## 2026-11-18 (W2-A Application support)
- Fit rule lives in `components/applications/fit.ts` (documented at the top): grades become a percent-equivalent, the margin over the offer plus SAT, activities and essay set an exponent (capped at 1); chance = admit rate x 2^exponent, clamped 1-95%. Admit rate under 10% or most-selective tier is always Reach; else under 30% Reach, under 65% Target, otherwise Safe. Uses only T1 profile parameters.
- Demo content is in `data/fixtures/contrib/w2a-applications.json` (applications, meetings, finance, shortlist, documents). Nikhil's Leeds deadline is the school's internal UCAS date (28 Nov 2026), so it shows a high risk flag on the demo clock.
- Prices are dummy placeholders (user, 2026-11-18): `SHOW_COSTS` and `APPLICATION_SUPPORT_PRICE_INR` in `components/applications/config.ts`; set `SHOW_COSTS = false` to hide every fee and tuition figure.
- Upgrading to Application Support writes an approvals record (`kind: 'plan_upgrade'`) plus `student.plan` when a student record exists; the plan is read from either.
- Essay versions and anchored comments live inside `Application.essays`; AI pre-pass comments are canned rule-based output (`components/applications/ai.ts`). Meeting action items become timetable tasks (`kind: 'action_item'`) and call `recomputeLearner`.
- Parent screens never show essays or T3 meeting notes.

## 2026-11-18 (QB-ONB Onboarding test forms)
- **15 designs, 27 files.** Grades 8-10 are one design per board (`onb-{board}-g{grade}-none`); each grade 11-12 stream design is emitted once per board (`onb-{board}-g{grade}-{stream}`) with board refs and board swaps, so every student has exactly one form. `_status.json` is `validated: true` only when all 27 pass. (QB-ONB.)
- **21-item pool per subject group** (slot 1 D2, slot 2 D1+D2, slots 3-8 D1-D3) so the D2-start ladder (down after a miss, up after two hits) never runs out; a student sees 8 per group. (QB-ONB.)
- **Gap mapping:** prerequisite miss G1; this-year D1 G1, D2 G2, D3 G3 (workbook Gap Diagnosis rule). G4, G8 and G9 are secondary flags computed in `lib/onboarding/score.ts`. All gaps start `status: 'suspected'`. (QB-ONB.)
- **New type file `lib/types/onboarding.ts`**, not re-exported from `lib/types/index.ts` (W1 owns it); import it by path. (QB-ONB.)
- **Grade 11 prerequisites point at grade 10 subjects** (CBSE and IB teach one Science and one Social Science in grade 10), so a Physics prerequisite links to e.g. `cbse-g10-science`. Where IB grade 10 lacks the topic (Ohm's law, refraction) the slot links to the closest IB grade 10 subtopic. (QB-ONB.)
- **IB Commerce has 3 groups** (no IB Accountancy); Cambridge grade 11 Commerce uses AS Mathematics, grade 12 uses Probability & Statistics 2. Humanities Economics reuses the Commerce economics bank. Cambridge's Political Science slot is Global Perspectives & Research (skills items), IB's is Global Politics. (QB-ONB.)
- **The onboarding validator loads `scripts/questions/validate.ts` with a runtime `import()`**, so tsc/next build never see a `.ts` specifier. (QB-ONB.)
- **Guided demo hook (W3-QA).** `app/layout.tsx` renders `<DemoGuide />` (components/demo), which shows the Demo guide panel only while a `/demo` scenario cookie (`learnibility_demo`) is set; `/login` links to `/demo`. Scenario steps navigate through `GET /demo/go?scenario=&step=` (switches persona, no reset); the Start button POSTs there and resets the demo first. Scenarios live in `components/demo/scenarios.ts`; `docs/demo-script.md` is generated from it (`npx tsx scripts/e2e/build-demo-script.ts`). (W3-QA.)

## 2026-11-18 (W2-T Tutor marketplace and tutor app)
- **Tutor Home keeps both layouts** (user, 2026-11-18: "both works with toggle or mode change"). 2a teaching-first is the default, 2b requests-first is one click away via the Home layout toggle. The choice is saved per tutor in the demo store (`tutorSettings` collection, reset with the demo), with the `learnibility_tutor_home` cookie as fallback until that collection exists. Profile edits use the same record. (W2-T.)
- **Tutors see learning data only in the subjects they teach** with that student (mastery, gaps, scores), plus T1 profile basics; never T3. Background (non-persona) students get light `student` records in `data/fixtures/contrib/w2t-tutors.json` so names resolve. (W2-T.)
- **Booking writes.** `requestDemo` creates a `Booking` (requested, with `sharedGapSnapshot` only when the student leaves the share toggle on) and a scheduled demo `Session`, posts a system message and calls `recomputeLearner(id, { reason: 'session_booked' })`. Declining drops the snapshot and cancels the session. Reschedule moves the session (student is messaged) or cancels it. (W2-T.)
- **Session report is the loop's hinge.** `submitSessionReport` completes the session, turns each homework line into a `Task` per attending learner (`source: 'tutor'`, `createdBy` tutor, `refId` session), files private notes as `tutorNotes`, moves "next focus" onto the next scheduled session, emits an M18 event and recomputes. Editing a filed report reuses tasks with the same title and skips removed ones, so nothing duplicates. Students see topics, homework and next focus, never the performance rating or notes. (W2-T.)
- **AI parts are pre-written rules.** Session focus = last report's next focus, else the biggest open gap (by hours to close) with a per-gap-code line, else the shared snapshot or the booking topic. The 60-minute plan scales to session length. Test drafts come from the real question bank filtered by subtopic, difficulty and type, topped up with templated items flagged for review. Onboarding reads free text with regex rules (`components/tutor/extract.ts`, 3 tests). (W2-T.)
- **Earnings.** Per-session net = rate × hours (× learners for group) minus the 15% platform fee; free demos are ₹0; sessions without a report are "report missing" and held; paid = in a `payouts` record; next payout is the coming Monday. Month-on-month compares the same days of the previous month. Prices are dummy sample values (user, 2026-11-18: "use dummy pricing we will change it later"). (W2-T.)
- **Profile, availability, pricing and payout edits are kept per browser** in the `lb_tutor_prefs_{tutorId}` cookie and laid over the catalogue record on the tutor's own screens; there is no shared collection for tutor profile edits yet, so Explore Tutors still shows catalogue values. Verification uploads are display only. (W2-T.)
- **Today has a day switcher** (`/tutor/today?day=`); a past day with every item done shows the 6b "all done" state. (W2-T.)

## W3-CRM (2026-11-18)
- New role `sales` in `ROLES` (lib/types/enums.ts), `ROLE_LABEL` "Sales rep" and the sales sidebar in lib/nav.ts, as the brief cleared. Adding the role also needed one line each in `lib/visibility.ts` (sales: every tier hidden; the CRM shows lead fields, never the 430 profile) and `components/shell/role-home.tsx` (TILES entry), or tsc fails on `Record<Role, …>`.
- Routes are `/sales/**` (app/sales) rather than app/crm, because `roleHome` and `navHref` build `/{role}` paths; code lives in components/crm, lib/data/crm.ts, lib/actions/crm.ts.
- CRM writes use the shared demo overlay directly under collections `crm_leads`, `crm_activities`, `crm_followups`, `crm_payments`, `crm_conversions`, `crm_subscriptions` (lib/data/crm.ts `crmPut`), so Reset demo covers them without touching `lib/store/collections.ts`.
- There is no Subscription record type in lib/data/types.ts; subscriptions live in `crm_subscriptions` and the plan is set on `Student.plan`, with an `invoices` record and a `crm_handoff` event on the learner.
- Sales persona ids use the prefix `sal_` (not in lib/ids PERSON_PREFIXES; nothing generates them).
- Prices: data/crm/packages.json, dummy values, one file.
