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
