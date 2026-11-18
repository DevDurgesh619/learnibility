# Learnibility shared contract

Every workstream honours this contract. W1 Foundations owns it. Any change after the first foundations commit needs a change that updates this file, agreed with the coordinator.

The TypeScript source of truth is `/lib/types/*` and `/lib/ids.ts`. If this file and the code ever disagree, raise it; do not silently pick one.

## Shared contract

### Folder layout

```
/app                      Next.js App Router routes (W1 owns shell; later waves add role areas)
/components               UI components (W1: design system)
/lib/types/               Shared TypeScript types (W1 owns; others propose changes by PR)
/lib/ids.ts               ID builders and parsers (W1 owns)
/lib/engines/             Pure engine functions + tests (W3 owns)
/data/curriculum/         Curriculum map JSON (W2 owns)
/data/catalogues/         Tutors, courses, careers, skills, universities JSON (W4 owns)
/data/questions/          Question bank JSON (Wave 2)
/data/personas/           Personas and history (Wave 3)
/scripts/                 Generators and validators, one subfolder per workstream
/prisma/schema.prisma     DB schema (W1)
/reference/               Copies of the uploaded source files
/docs/                    Blueprint excerpt, contracts, decisions log
```

Data files are JSON, one file per natural unit (one per subject for curriculum, one per catalogue). Every JSON file has a top-level `{ "schemaVersion": 1, "generatedBy": "<script path>", "items": [...] }`.

### Enums

```ts
type Board = 'cbse' | 'cambridge' | 'ib';
type Grade = 8 | 9 | 10 | 11 | 12;
type Stream = 'none' | 'science' | 'commerce' | 'humanities';   // 'none' for grades 8-10
type Weight = 'L' | 'S' | 'H';                                    // subtopic weight
type ConceptGroup = 'C1' | 'C2' | 'C3' | 'C4';
type Difficulty = 'D1' | 'D2' | 'D3' | 'D4' | 'D5';
type AlrRole = 'practised' | 'retention_probe' | 'transfer_probe';
type Level = 0 | 1 | 2 | 3 | 4 | 5;                               // L0-L5 ladder
type GapCode = 'G1'|'G2'|'G3'|'G4'|'G5'|'G6'|'G7'|'G8'|'G9'|'G10';
type Band = 'below_avg' | 'average' | 'above_avg' | 'excellent';
type Role = 'student' | 'parent' | 'teacher' | 'counsellor' | 'tutor' | 'mentor';
type SourceMethod = `M${1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20}`;
type Tier = 'T1' | 'T2' | 'T3' | 'C';
```

Gap code meanings, level ladder and band parameters are exactly as in the class 8 maths workbook (sheets Gap Diagnosis, Mastery Inputs, ALR Method).

### ID conventions (lowercase, kebab, stable; never reuse)

| Thing | Pattern | Example |
| --- | --- | --- |
| Subject | `{board}-g{grade}-{subjectSlug}` | `cbse-g8-maths`, `cambridge-g11-physics`, `ib-g12-economics` |
| Chapter | `{subjectId}-ch{NN}` | `cbse-g8-maths-ch01` |
| Subtopic | `{chapterId}-st{N}` | `cbse-g8-maths-ch01-st2` |
| Question | `{subtopicId}-q{NN}`; practice tests `{chapterId}-pf{A|B}-q{NN}`; mocks `{subjectId}-mock{N}-q{NN}`; onboarding `onb-{board}-g{grade}-{stream}-q{NN}` | `cbse-g8-maths-ch01-st2-q03` |
| Learner | `lrn_{firstname}_{lastname}` | `lrn_kabir_singh` |
| Staff and parents | `par_`, `tch_`, `csl_`, `tut_`, `mnt_` + `{firstname}_{lastname}` | `tut_rahul_verma` |
| Catalogue items | `career-{slug}`, `skill-{slug}`, `uni-{country}-{slug}`, `course-{slug}`, `res-{slug}` | `uni-us-yale`, `career-data-analyst` |
| Profile parameter | `p{ID}` from the 430 file | `p279` |

Subject slugs are a fixed list owned by W2 Curriculum map, published in `/docs/curriculum.md`. Slugs follow the cost-sheet seat, so for example IB Global Politics is `ib-g11-political-science`. The class 8 maths workbook keeps its own question IDs (M8-001...) as `legacyId`.

### Core types (Foundations commits these to /lib/types)

```ts
interface Subject { id; board: Board; grade: Grade; stream: Stream; slug; name; programme;  // e.g. "IGCSE Physics 0625"
  textbook?; examPattern?; chapterCount; questionTarget: number;  // from cost sheet
}
interface Chapter { id; subjectId; order: number; name; teachingPeriods: number; subtopicIds: string[]; }
interface Subtopic { id; chapterId; order: number; name; weight: Weight; teachingPeriods: number;
  prerequisiteIds: string[]; prerequisiteNote?: string;               // earlier-grade skill in words when not in the map
  learnHours: Record<Band, number>; masterHours: Record<Band, number>; // computed by W3's mastery-time engine
}
interface Question { id; legacyId?; subtopicId; chapterId; subjectId; conceptGroup: ConceptGroup; difficulty: Difficulty;
  type: 'mcq'|'short'|'explain'|'numerical'|'multi_step'|'case'|'long'; stem; options?: string[];
  answer; markingKey; marks: number; minutes: number; alrRole: AlrRole; likelyGapOnWrong?: GapCode;
  set: 'mastery_bank'|'practice_form_a'|'practice_form_b'|'mock'|'onboarding';
}
interface EvidenceEvent { eventId; learnerId; timestampUtc; sourceMethod: SourceMethod; type: string; payload: Record<string, unknown>; }
interface ItemResponse { questionId; correct: boolean; secondsTaken: number; confidence?: 1|2|3|4|5; answer?: string; }
interface MasteryState { learnerId; subtopicId; level: Level; pMastery: number; lastTestedUtc; retention?: number; }
interface AlrSnapshot { learnerId; chapterId; dK; R; TQ; CE; ECV; MCI; LRS; band: Band; }
interface Gap { id; learnerId; subtopicId; code: GapCode; secondaryFlags: GapCode[]; level: Level; size: number;
  hoursToClose: number; status: 'suspected'|'confirmed'|'in_progress'|'closed'; }
interface ProfileValue { learnerId; paramId; value: unknown; source: SourceMethod; asOfUtc; confidence: 'low'|'medium'|'high'; tier: Tier; }
```

Untyped fields above are `string`. Timestamps are ISO UTC strings. Money is integer rupees (`inr`). Hours are decimals rounded to 0.1.

## Implementation notes (W1, 2026-11-18)

- Practice-test question IDs are lowercase like every other ID: form A is `pfa`, form B is `pfb`, e.g. `cbse-g8-maths-ch01-pfa-q01`. `practiceQuestionId(chapterId, 'A', 1)` builds it.
- Question numbers are zero-padded to at least two digits (`q03`, `q123`). Chapter numbers likewise (`ch01`). Subtopic, mock and practice-form numbers are not padded (`st2`, `mock1`).
- Onboarding IDs use stream `none` for grades 8 to 10 and a real stream for 11 and 12; the builder rejects other combinations.
- Person IDs strip everything but letters and digits from each name part: `D'Souza` becomes `dsouza`. Use the first word of a compound first name.
- University country codes are two lowercase letters. Use `in`, `us`, `uk`, `ca`, `au` (note `uk`, not `gb`).
- Profile parameters live in `/data/profile/parameters.json` (430 items, type `ProfileParameter` in `/lib/types/profile.ts`). `methods` is the ordered list of M-codes parsed from the source column; `methodsText` keeps the original wording. `tier` is `T1`, `T2`, `T3` or `C`. Collection methods M1 to M20 and tier definitions are in `collection-methods.json` and `sensitivity-tiers.json`.
- Every data file is a `DataFile<T>` (`/lib/types/data-file.ts`).
- Catalogue types (`/lib/types/catalogue.ts`) are owned by W4 and consumed by W3; they are re-exported from `/lib/types/index.ts`.
- Import shared types from `@/lib/types` and ID helpers from `@/lib/ids`.
- Entrance exams (approved addition, 2026-11-18) live in `/data/catalogues/exams.json` with plain slug IDs such as `jee-main`, `neet-ug`, `clat`, `cuet-ug`, `sat`. The fixed list is in W4's `/mnt/project-files/build/w4-catalogue-ids.md`.
- Interventions (approved addition, 2026-11-18) live in `/data/catalogues/interventions.json` with IDs `int-{gapcode}-{rank}`, lowercase, e.g. `int-g1-1`, `int-any-1` for the rows that apply to any gap.

## App foundations (W1 milestone 2)

- **Design system.** `@/components/ui` (Button, Card/CardHeader/CardBody/CardFooter, Badge, BandBadge, GapBadge, TierBadge, Table/THead/TBody/TR/TH/TD, Progress, Avatar, StatTile, EmptyState, PageHeader), `@/components/charts` (RadarChart, TrendChart, BarChart; pass `format="percent"|"decimal"|"hours"|"inr"|"number"`, never a function), `@/components/shell`. Live gallery at `/design`. Colours are semantic tokens in `app/globals.css` (`bg-surface`, `text-muted`, `border-line`, `brand-*`, `band-*`, `chart-1..5`).
- **Role areas.** `app/{student,parent,teacher,counsellor,tutor,mentor}/`. Sidebars live in `lib/nav.ts`. To build a section, add `app/<role>/<slug>/page.tsx`; it replaces the placeholder served by `app/<role>/[section]/page.tsx`. Pages get the signed-in persona with `currentPersona()` from `@/lib/session`.
- **Personas.** `/data/personas/index.json` is a `DataFile<PersonaSummary>` (`/lib/types/persona.ts`). W1 ships a 6-person stub, one per role; Wave 3 replaces it.
- **Visibility.** Any screen that shows profile values filters them with `visibleProfile(values, role, opts)` from `@/lib/visibility`; any engine that scores people filters inputs with `valuesForPurpose(values, purpose)`.
- **Formatting.** `@/lib/format` (`formatInr`, `formatHours`, `formatPercent`, `formatValue`). Money shows as ₹1,25,000 (Indian grouping).
- **Database.** `npm run db:setup` (push schema + seed from `/data`). The seed reads profile, curriculum, questions, catalogues, plans and personas; Wave 3 extends `seedPersonaHistory` in `scripts/foundations/seed.ts`.
