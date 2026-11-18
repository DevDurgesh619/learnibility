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
- **ALR edge case:** a 100% pre-test makes the engine's dK 0/0; the data layer treats it as 99%. Reported to the engines owner. (W2-0.)
