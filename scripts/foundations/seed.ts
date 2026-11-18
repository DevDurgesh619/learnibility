/**
 * Seed loader: reads every JSON data file under /data and loads it into the database.
 *
 *   npm run db:push   # create the SQLite schema (prisma/dev.db)
 *   npm run db:seed   # this script
 *
 * Tolerant by design: each data family is optional, so the seed runs at every stage of the build.
 * Wave 3 (Personas) extends `seedPersonaHistory` for per-student history files.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PrismaBetterSqlite3 } from '@prisma/adapter-better-sqlite3';
import { PrismaClient } from '../../lib/generated/prisma/client';
import { VISIBILITY } from '../../lib/visibility';
import { parsePersonId } from '../../lib/ids';
import type {
  Career, Chapter, DataFile, EntranceExam, PersonaSummary, ProfileParameter, Question, Resource, Skill, Subject, Subtopic, Tutor, University,
} from '../../lib/types';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const DATA = path.join(ROOT, 'data');
const url = process.env.DATABASE_URL ?? `file:${path.join(ROOT, 'prisma', 'dev.db')}`;
const prisma = new PrismaClient({ adapter: new PrismaBetterSqlite3({ url }) });

type Row = Record<string, unknown>;

function readData<T = Row>(rel: string): T[] | null {
  const file = path.join(DATA, rel);
  if (!fs.existsSync(file)) return null;
  const doc = JSON.parse(fs.readFileSync(file, 'utf8')) as DataFile<T>;
  if (doc.schemaVersion !== 1 || !Array.isArray(doc.items)) throw new Error(`${rel}: not a DataFile envelope`);
  return doc.items;
}

function jsonFiles(dir: string): string[] {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) return jsonFiles(p);
    return e.name.endsWith('.json') ? [p] : [];
  });
}

async function inChunks<T>(rows: T[], size: number, fn: (chunk: T[]) => Promise<unknown>) {
  for (let i = 0; i < rows.length; i += size) await fn(rows.slice(i, i + size));
}

const log = (label: string, n: number) => console.log(`  ${label.padEnd(28)} ${n}`);

// ---------------------------------------------------------------- profile

async function seedProfile() {
  const params = readData<ProfileParameter>('profile/parameters.json') ?? [];
  await inChunks(params, 200, (chunk) =>
    prisma.profileParameter.createMany({
      data: chunk.map((p) => ({ ...p, methods: p.methods, handlingNote: p.handlingNote ?? null })),
    }),
  );
  log('profile parameters', params.length);

  const rules = Object.entries(VISIBILITY).flatMap(([role, tiers]) =>
    Object.entries(tiers).map(([tier, mode]) => ({ role, tier, mode })),
  );
  await prisma.roleVisibilityRule.createMany({ data: rules });
  log('role visibility rules', rules.length);
}

// ---------------------------------------------------------------- curriculum

const EMPTY_HOURS = { below_avg: 0, average: 0, above_avg: 0, excellent: 0 };

async function seedCurriculum() {
  const subjects = readData<Subject>('curriculum/subjects.json') ?? [];
  await inChunks(subjects, 200, (chunk) => prisma.subject.createMany({ data: chunk.map(pickSubject) }));
  log('subjects', subjects.length);

  const chapters: Chapter[] = [];
  const subtopics: Subtopic[] = [];
  for (const file of jsonFiles(path.join(DATA, 'curriculum'))) {
    if (path.basename(file) === 'subjects.json') continue;
    const doc = JSON.parse(fs.readFileSync(file, 'utf8')) as DataFile<Row> & Row;
    // Accept chapters with nested subtopics, or a flat list of chapters and subtopics, or {chapters, subtopics}.
    const items: Row[] = [...(doc.items ?? []), ...((doc.chapters as Row[]) ?? []), ...((doc.subtopics as Row[]) ?? [])];
    for (const it of items) {
      if ('weight' in it && 'chapterId' in it) subtopics.push(it as unknown as Subtopic);
      else if ('subjectId' in it && 'order' in it) {
        chapters.push(it as unknown as Chapter);
        for (const st of (it.subtopics as Row[] | undefined) ?? []) subtopics.push(st as unknown as Subtopic);
      }
    }
  }
  const subjectIds = new Set(subjects.map((s) => s.id));
  const ch = chapters.filter((c) => subjectIds.has(c.subjectId));
  await inChunks(ch, 500, (chunk) =>
    prisma.chapter.createMany({
      data: chunk.map((c) => ({ id: c.id, subjectId: c.subjectId, order: c.order, name: c.name, teachingPeriods: c.teachingPeriods ?? 0 })),
    }),
  );
  const chapterIds = new Set(ch.map((c) => c.id));
  const st = subtopics.filter((s) => chapterIds.has(s.chapterId));
  await inChunks(st, 500, (chunk) =>
    prisma.subtopic.createMany({
      data: chunk.map((s) => ({
        id: s.id, chapterId: s.chapterId, order: s.order, name: s.name, weight: s.weight,
        teachingPeriods: s.teachingPeriods ?? 0, prerequisiteNote: s.prerequisiteNote ?? null,
        learnHours: s.learnHours ?? EMPTY_HOURS, masterHours: s.masterHours ?? EMPTY_HOURS,
      })),
    }),
  );
  const subtopicIds = new Set(st.map((s) => s.id));
  const links = st.flatMap((s) =>
    (s.prerequisiteIds ?? []).filter((p) => subtopicIds.has(p)).map((p) => ({ subtopicId: s.id, prerequisiteId: p })),
  );
  await inChunks(links, 500, (chunk) => prisma.prerequisiteLink.createMany({ data: chunk }));
  log('chapters', ch.length);
  log('subtopics', st.length);
  log('prerequisite links', links.length);
}

function pickSubject(s: Subject) {
  return {
    id: s.id, board: s.board, grade: s.grade, stream: s.stream, slug: s.slug, name: s.name, programme: s.programme,
    textbook: s.textbook ?? null, examPattern: s.examPattern ?? null, chapterCount: s.chapterCount, questionTarget: s.questionTarget,
  };
}

// ---------------------------------------------------------------- questions

async function seedQuestions() {
  const subjectIds = new Set((await prisma.subject.findMany({ select: { id: true } })).map((s) => s.id));
  const chapterIds = new Set((await prisma.chapter.findMany({ select: { id: true } })).map((s) => s.id));
  const subtopicIds = new Set((await prisma.subtopic.findMany({ select: { id: true } })).map((s) => s.id));
  let n = 0;
  let skipped = 0;
  for (const file of jsonFiles(path.join(DATA, 'questions'))) {
    const doc = JSON.parse(fs.readFileSync(file, 'utf8')) as DataFile<Row>;
    const qs = (doc.items ?? []).filter((q) => 'stem' in q) as unknown as Question[];
    const ok = qs.filter((q) => subjectIds.has(q.subjectId));
    skipped += qs.length - ok.length;
    await inChunks(ok, 500, (chunk) =>
      prisma.question.createMany({
        data: chunk.map((q) => ({
          id: q.id, legacyId: q.legacyId ?? null, subjectId: q.subjectId,
          chapterId: q.chapterId && chapterIds.has(q.chapterId) ? q.chapterId : null,
          subtopicId: q.subtopicId && subtopicIds.has(q.subtopicId) ? q.subtopicId : null,
          conceptGroup: q.conceptGroup, difficulty: q.difficulty, type: q.type, stem: q.stem,
          options: q.options ?? undefined, answer: String(q.answer), markingKey: q.markingKey ?? '',
          marks: q.marks, minutes: q.minutes, alrRole: q.alrRole, likelyGapOnWrong: q.likelyGapOnWrong ?? null, set: q.set,
        })),
      }),
    );
    n += ok.length;
  }
  log('questions', n);
  if (skipped) log('questions skipped (no subject)', skipped);
}

// ---------------------------------------------------------------- catalogues

async function seedCatalogues() {
  const exams = readData<EntranceExam>('catalogues/exams.json') ?? [];
  await prisma.entranceExam.createMany({ data: exams.map((e) => ({ id: e.id, name: e.name, kind: e.kind, data: asJson(e) })) });
  log('entrance exams', exams.length);

  const skills = readData<Skill>('catalogues/skills.json') ?? [];
  await prisma.skill.createMany({ data: skills.map((s) => ({ id: s.id, name: s.name, kind: s.kind, data: asJson(s) })) });
  log('skills', skills.length);

  const careers = readData<Career>('catalogues/careers.json') ?? [];
  await prisma.career.createMany({ data: careers.map((c) => ({ id: c.id, title: c.title, data: asJson(c) })) });
  const skillIds = new Set(skills.map((s) => s.id));
  const reqs = careers.flatMap((c) =>
    c.skills.filter((r) => skillIds.has(r.skillId)).map((r) => ({ careerId: c.id, skillId: r.skillId, targetLevel: r.targetLevel })),
  );
  await prisma.careerSkillRequirement.createMany({ data: reqs });
  log('careers', careers.length);
  log('career skill requirements', reqs.length);

  const tutors = readData<Tutor>('catalogues/tutors.json') ?? [];
  await prisma.tutor.createMany({
    data: tutors.map((t) => ({
      id: t.id, name: t.displayName, city: t.city,
      hourly1to1: t.pricing.oneToOnePerHourInr, hourlyGroup: t.pricing.groupPerStudentPerHourInr,
      rating: t.rating, verified: t.verified, data: asJson(t),
    })),
  });
  log('tutors', tutors.length);

  const resources = readData<Resource>('catalogues/resources.json') ?? [];
  await prisma.resource.createMany({
    data: resources.map((r) => ({ id: r.id, kind: r.kind, title: r.title, priceInr: r.priceInr, hours: r.hours, data: asJson(r) })),
  });
  log('resources', resources.length);

  const unis = readData<University>('catalogues/universities.json') ?? [];
  await prisma.university.createMany({
    data: unis.map((u) => ({ id: u.id, name: u.name, country: u.country, city: u.city, data: asJson(u) })),
  });
  log('universities', unis.length);
}

const asJson = (v: unknown) => JSON.parse(JSON.stringify(v)) as object;

// ---------------------------------------------------------------- commercial

async function seedPlans() {
  // Placeholder prices until the user decides pricing (blueprint open question).
  const plans = [
    { id: 'free', name: 'Free', priceInr: 0, period: 'month', features: ['Onboarding test', 'Gap analysis', 'Timetable', 'University Fit (explore)'] },
    { id: 'application_support', name: 'Application Support', priceInr: 4999, period: 'month', features: ['Application command center', 'Draft Studio', 'Counsellor reviews'] },
    { id: 'full_package', name: 'Full package', priceInr: 7999, period: 'month', features: ['Everything in Application Support', 'Career mapping sessions', 'Priority tutor matching'] },
  ];
  await prisma.plan.createMany({ data: plans });
  log('plans', plans.length);
}

// ---------------------------------------------------------------- personas

async function seedPersonas() {
  const personas = readData<PersonaSummary>('personas/index.json') ?? [];
  for (const p of personas) {
    const parts = parsePersonId(p.id);
    const [first, ...rest] = p.name.split(' ');
    await prisma.person.create({
      data: {
        id: p.id, role: p.role, firstName: first ?? parts?.first ?? '', lastName: rest.join(' ') || parts?.last || '',
        displayName: p.name, headline: p.story, avatar: p.avatar ?? null, data: asJson(p),
        learner: p.role === 'student' && p.board && p.grade
          ? { create: { board: p.board, grade: p.grade, stream: p.stream ?? 'none', programme: p.programme ?? null } }
          : undefined,
      },
    });
  }
  log('personas', personas.length);
  await seedPersonaHistory();
}

/** Wave 3 fills this in: data/personas/students/{learnerId}/*.json, adults, classes. */
async function seedPersonaHistory() {}

// ---------------------------------------------------------------- main

async function reset() {
  // Children before parents.
  const models = [
    'comment', 'essayVersion', 'essayDraft', 'checklistItem', 'application', 'meetingNote', 'document', 'review',
    'tutorSession', 'booking', 'skillGap', 'careerMatch', 'careerSkillRequirement', 'itemResponse', 'attempt',
    'assessment', 'evidenceEvent', 'profileValue', 'masteryState', 'alrSnapshot', 'gap', 'interventionPlan',
    'timetableBlock', 'task', 'retentionReview', 'subscription', 'invoice', 'consentRecord', 'sectionEnrollment',
    'classSection', 'caseAssignment', 'learnerSubject', 'parentLink', 'learner', 'person', 'question',
    'prerequisiteLink', 'subtopic', 'chapter', 'subject', 'profileParameter', 'roleVisibilityRule', 'tutor',
    'resource', 'skill', 'career', 'entranceExam', 'university', 'plan', 'lead',
  ] as const;
  for (const m of models) await (prisma[m] as unknown as { deleteMany: () => Promise<unknown> }).deleteMany();
}

async function main() {
  console.log(`Seeding ${url}`);
  await reset();
  await seedProfile();
  await seedCurriculum();
  await seedQuestions();
  await seedCatalogues();
  await seedPlans();
  await seedPersonas();
  console.log('Done.');
}

main()
  .catch((e) => {
    console.error(e);
    process.exitCode = 1;
  })
  .finally(() => prisma.$disconnect());
