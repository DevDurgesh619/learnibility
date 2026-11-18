# Learnibility

Hyper-personalised learning for grades 8 to 12 across CBSE, Cambridge and IB. Every student has one verified master record (430 profile parameters plus mastery, gaps and ALR) that drives a daily loop of assessment, gap diagnosis, interventions, timetable and career mapping. Students, parents, teachers, counsellors, tutors and mentors each see their own view of it.

This is a working prototype with realistic dummy personas, built to be demoed end to end.

## Run

```bash
npm install
npm run dev        # http://localhost:3000
npm test           # Vitest
npm run lint       # type check
npm run import:430 # regenerate data/profile/*.json from reference/ (needs python3 + openpyxl)
```

## Layout

```
/app                 Next.js App Router routes
/components          UI components and design system
/lib/types/          Shared TypeScript types (the contract)
/lib/ids.ts          ID builders and parsers
/lib/engines/        Pure engine functions + tests
/data/curriculum/    Curriculum map JSON
/data/catalogues/    Tutors, courses, careers, skills, universities
/data/questions/     Question bank
/data/personas/      Personas and history
/data/profile/       430-parameter profile definition
/scripts/            Generators and validators, one folder per workstream
/prisma/             Database schema and seed
/reference/          Copies of the uploaded source files
/docs/               Contracts and decisions
```

Read `docs/contracts.md` before adding data or types.
