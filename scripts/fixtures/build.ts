/**
 * W2-0 fixtures: hand-built learners whose history is simulated answer by answer and then run through the
 * real engines (lib/data/derive.ts → diagnoseGaps, computeAlr, planInterventions, buildTimetable, mapCareers),
 * so gaps, bands, timetables and plans agree on every screen. Wave 3 personas replace these per learner.
 *
 *   npx tsx scripts/fixtures/build.ts        writes data/fixtures/** (deterministic: seed "learnibility-2026")
 *
 * Fixture questions (data/fixtures/questions/{subjectId}.json) use ids {subtopicId}-q9NN so they never clash
 * with the real bank; screens draw new tests from the real bank once it exists.
 */
import fs from 'node:fs';
import path from 'node:path';
import { careerGap, mapCareers } from '@/lib/engines';
import type { Career, ConceptGroup, Difficulty, EvidenceEvent, ItemResponse, ProfileParameter, ProfileValue, Question, QuestionType, Subtopic, Weight } from '@/lib/types';
import { getSubject } from '@/lib/data/catalogue';
import { addDaysLocal, applyAttempt, buildWeek, emptyState, localDateOf, planFor, weekStartOf, type LearnerState } from '@/lib/data/derive';
import type {
  Adult, AlrRecord, Attempt, BackgroundStudent, CareerMatches, Consent, DocumentRecord, GapRecord, Invoice, MasteryRecord, MeetingNote,
  Message, PlanRecord, Section, Session, Student, Task, TimetableRequest, TimetableWeek,
} from '@/lib/data/types';
import type { PersonaSummary } from '@/lib/types';

const ROOT = process.cwd();
const OUT = path.join(ROOT, 'data', 'fixtures');
const GEN = 'scripts/fixtures/build.ts';
const NOW = '2026-11-18T03:30:00.000Z'; // DEMO_NOW (09:00 IST)
const TODAY = '2026-11-18';
const HISTORY_DAYS = 42;

// ------------------------------------------------------------------ seeded random

function hashSeed(s: string): number {
  let h = 1779033703 ^ s.length;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 3432918353), (h = (h << 13) | (h >>> 19));
  return h >>> 0;
}
function rng(seed: string) {
  let a = hashSeed(seed);
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const R = rng('learnibility-2026');
const pick = <T>(xs: T[]) => xs[Math.floor(R() * xs.length)];
const clamp = (x: number, a: number, b: number) => Math.max(a, Math.min(b, x));
const round1 = (x: number) => Math.round(x * 10) / 10;

// ------------------------------------------------------------------ write helpers

function write(rel: string, items: unknown[], extra: Record<string, unknown> = {}) {
  const f = path.join(OUT, rel);
  fs.mkdirSync(path.dirname(f), { recursive: true });
  fs.writeFileSync(f, JSON.stringify({ schemaVersion: 1, generatedBy: GEN, ...extra, items }, null, 1) + '\n');
}
const istUtc = (date: string, hhmm: string) => new Date(Date.parse(`${date}T${hhmm}:00+05:30`)).toISOString();

// ------------------------------------------------------------------ fixture questions

/** Check path per weight (workbook: L 5, S 6, H 8) plus one extra retention probe. */
const PATH: Record<Weight, [ConceptGroup, Difficulty, QuestionType][]> = {
  L: [['C1', 'D1', 'mcq'], ['C2', 'D2', 'short'], ['C3', 'D2', 'numerical'], ['C3', 'D3', 'multi_step'], ['C4', 'D3', 'case']],
  S: [['C1', 'D1', 'mcq'], ['C1', 'D2', 'mcq'], ['C2', 'D2', 'short'], ['C3', 'D2', 'numerical'], ['C3', 'D3', 'multi_step'], ['C4', 'D3', 'case']],
  H: [['C1', 'D1', 'mcq'], ['C1', 'D2', 'mcq'], ['C2', 'D2', 'short'], ['C3', 'D2', 'numerical'], ['C3', 'D3', 'multi_step'], ['C3', 'D4', 'multi_step'], ['C4', 'D3', 'case'], ['C4', 'D4', 'case']],
};
const GAP_ON_WRONG: Record<ConceptGroup, Question['likelyGapOnWrong']> = { C1: 'G1', C2: 'G2', C3: 'G3', C4: 'G5' };
const STEM: Record<ConceptGroup, (n: string) => string> = {
  C1: (n) => `Which of these statements about ${n.toLowerCase()} is correct?`,
  C2: (n) => `In one or two lines, explain the key idea behind ${n.toLowerCase()}.`,
  C3: (n) => `Apply ${n.toLowerCase()} to solve the routine problem shown, giving each step.`,
  C4: (n) => `A new situation: use ${n.toLowerCase()} to decide what to do, and justify your answer.`,
};

function questionsFor(subjectId: string): Question[] {
  const b = getSubject(subjectId)!;
  const out: Question[] = [];
  for (const s of b.subtopics) {
    const p = PATH[s.weight];
    const items: [ConceptGroup, Difficulty, QuestionType][] = [...p, ['C1', 'D2', 'mcq']];
    items.forEach(([cg, d, type], i) => {
      const isProbe = i === items.length - 1 || (cg === 'C2' && d === 'D2');
      const transfer = (cg === 'C3' && Number(d[1]) >= 4) || (cg === 'C4' && Number(d[1]) >= 3);
      const q: Question = {
        id: `${s.id}-q9${String(i + 1).padStart(2, '0')}`,
        legacyId: 'fixture',
        subtopicId: s.id, chapterId: s.chapterId, subjectId,
        conceptGroup: cg, difficulty: d, type,
        stem: STEM[cg](s.name),
        ...(type === 'mcq' ? { options: ['The statement in option A', 'The statement in option B', 'The statement in option C', 'The statement in option D'] } : {}),
        answer: type === 'mcq' ? 'The statement in option B' : 'See marking key',
        markingKey: type === 'mcq' ? 'B. Fixture item: option B is correct.' : `Fixture item: award marks for a correct method and answer on ${s.name}.`,
        marks: cg === 'C4' ? 4 : cg === 'C3' ? 3 : cg === 'C2' ? 2 : 1,
        minutes: cg === 'C4' ? 5 : cg === 'C3' ? 3 : cg === 'C2' ? 2 : 1,
        alrRole: transfer ? 'transfer_probe' : isProbe ? 'retention_probe' : 'practised',
        likelyGapOnWrong: GAP_ON_WRONG[cg],
        set: 'mastery_bank',
      };
      out.push(q);
    });
  }
  return out;
}

// ------------------------------------------------------------------ cast

interface Traits {
  base: number; spread: number; slip: number; blank: number; overconf: number; overconfDrift: number;
  growth: number; cgPenalty?: Partial<Record<ConceptGroup, number>>; weak?: Record<string, number>; speed: number;
  doneRate: number;
}
interface Cast {
  student: Student;
  depthSubject: string;
  chapters: number; // chapters covered in the 6 weeks
  traits: Traits;
  parent: { id: string; name: string; relation: 'mother' | 'father' };
  persona: Omit<PersonaSummary, 'id' | 'role' | 'name'>;
  profile: Record<string, unknown>;
}

const weekdays = (start: string, end: string) => (['mon', 'tue', 'wed', 'thu', 'fri'] as const).map((day) => ({ day, start, end }));
const avail = (wk: [string, string], sat: [string, string], sun?: [string, string]) => [
  ...weekdays(wk[0], wk[1]),
  { day: 'sat' as const, start: sat[0], end: sat[1] },
  ...(sun ? [{ day: 'sun' as const, start: sun[0], end: sun[1] }] : []),
];

function student(p: Partial<Student> & Pick<Student, 'id' | 'firstName' | 'lastName' | 'board' | 'grade' | 'stream' | 'programme' | 'school' | 'city' | 'band' | 'plan' | 'subjects'>): Student {
  return {
    role: 'student', name: `${p.firstName} ${p.lastName}`, availability: avail(['17:00', '19:00'], ['10:00', '12:30']), weeklyHours: 8,
    tzOffsetMinutes: 330, joinedUtc: '2026-04-06T04:30:00.000Z', parentIds: [], counsellorIds: ['csl_heena_qureshi'], mentorIds: [], tutorIds: [], sectionIds: [],
    profileCompletionPct: 62, medium: 'English', ...p,
  } as Student;
}

const CAST: Cast[] = [
  {
    student: student({
      id: 'lrn_kabir_singh', firstName: 'Kabir', lastName: 'Singh', board: 'cbse', grade: 9, stream: 'none', programme: 'CBSE Class 9', school: 'Delhi Public School, Dwarka', city: 'New Delhi',
      band: 'average', plan: 'free', subjects: [{ subjectId: 'cbse-g9-maths', depth: 'full' }, { subjectId: 'cbse-g9-science', depth: 'light' }], parentIds: ['par_harpreet_singh'],
      sectionIds: ['sec-cbse-g9-maths-a'], weeklyHours: 7, goal: 'Score 90% in Class 10 boards', currentChapterIds: ['cbse-g9-maths-ch07'], story: 'Quick but careless, and more confident than his marks.', profileCompletionPct: 58,
      availability: avail(['17:30', '19:30'], ['10:00', '12:30'], ['17:00', '18:00']),
    }),
    depthSubject: 'cbse-g9-maths', chapters: 6,
    traits: { base: 0.85, spread: 0.03, slip: 0.08, blank: 0.01, overconf: 0.4, overconfDrift: -0.05, growth: 0.08, speed: 0.75, doneRate: 0.8, weak: { 'cbse-g9-maths-ch05-st3': 0.4, 'cbse-g9-maths-ch06-st2': 0.45 } },
    parent: { id: 'par_harpreet_singh', name: 'Harpreet Singh', relation: 'father' },
    persona: { story: 'Quick but careless, and more confident than his marks.', grade: 9, board: 'cbse', stream: 'none', programme: 'CBSE Class 9', order: 1 },
    profile: { p31: 1.5, p178: 'medium', p193: 'Laptop + broadband', p212: 'B2', p230: 2, p163: 3, p150: 4, p8: 71 },
  },
  {
    student: student({
      id: 'lrn_rohan_das', firstName: 'Rohan', lastName: 'Das', board: 'cbse', grade: 10, stream: 'none', programme: 'CBSE Class 10', school: 'Kendriya Vidyalaya, Salt Lake', city: 'Kolkata',
      band: 'below_avg', plan: 'free', subjects: [{ subjectId: 'cbse-g10-maths', depth: 'full' }, { subjectId: 'cbse-g10-science', depth: 'light' }, { subjectId: 'cbse-g10-social-science', depth: 'light' }],
      parentIds: ['par_anita_das'], sectionIds: ['sec-cbse-g10-maths-b'], weeklyHours: 6, goal: 'Pass Class 10 boards with 75%', currentChapterIds: ['cbse-g10-maths-ch07'], profileCompletionPct: 44,
      story: 'Struggling in Maths; skips homework when it gets hard. Parents worried about boards.',
    }),
    depthSubject: 'cbse-g10-maths', chapters: 6,
    traits: { base: 0.7, spread: 0.06, slip: 0.08, blank: 0.06, overconf: 0, overconfDrift: 0, growth: 0.02, speed: 1.1, doneRate: 0.55, weak: { 'cbse-g10-maths-ch02-st2': 0.3, 'cbse-g10-maths-ch03-st2': 0.35, 'cbse-g10-maths-ch03-st3': 0.4, 'cbse-g10-maths-ch04-st1': 0.32, 'cbse-g10-maths-ch04-st3': 0.38 } },
    parent: { id: 'par_anita_das', name: 'Anita Das', relation: 'mother' },
    persona: { story: 'Struggling in Maths; free plan has run 3 weeks without closing his gaps.', grade: 10, board: 'cbse', stream: 'none', programme: 'CBSE Class 10', order: 2 },
    profile: { p31: 1, p178: 'medium', p193: 'Shared phone + broadband', p212: 'B1', p163: 2, p150: 2, p8: 54 },
  },
  {
    student: student({
      id: 'lrn_ishita_rao', firstName: 'Ishita', lastName: 'Rao', board: 'cambridge', grade: 8, stream: 'none', programme: 'Cambridge Lower Secondary Stage 9', school: 'Indus International School', city: 'Bengaluru',
      band: 'average', plan: 'free', subjects: [{ subjectId: 'cambridge-g8-maths', depth: 'full' }, { subjectId: 'cambridge-g8-english', depth: 'light' }], parentIds: ['par_sunita_rao'],
      weeklyHours: 8, goal: 'Get comfortable with Maths before IGCSE', currentChapterIds: ['cambridge-g8-maths-ch07'], joinedUtc: '2026-08-17T04:30:00.000Z', profileCompletionPct: 66,
      story: 'Strong in English and History; Maths gaps go back to grade 7 fractions and integers.',
    }),
    depthSubject: 'cambridge-g8-maths', chapters: 6,
    traits: { base: 0.8, spread: 0.06, slip: 0.05, blank: 0.01, overconf: -0.1, overconfDrift: 0, growth: 0.04, speed: 0.9, doneRate: 0.85, weak: { 'cambridge-g8-maths-ch01-st1': -0.25, 'cambridge-g8-maths-ch01-st2': -0.25, 'cambridge-g8-maths-ch03-st1': -0.2 } },
    parent: { id: 'par_sunita_rao', name: 'Sunita Rao', relation: 'mother' },
    persona: { story: 'Strong in English; Maths gaps from grade 7 fractions and integers.', grade: 8, board: 'cambridge', stream: 'none', programme: 'Cambridge Lower Secondary', order: 3 },
    profile: { p31: 1.5, p178: 'high', p193: 'Laptop + broadband', p212: 'C1', p163: 4, p150: 3, p8: 74 },
  },
  {
    student: student({
      id: 'lrn_sara_khan', firstName: 'Sara', lastName: 'Khan', board: 'cbse', grade: 11, stream: 'commerce', programme: 'CBSE Class 11 Commerce', school: 'St. Xavier’s Senior Secondary', city: 'Mumbai',
      band: 'above_avg', plan: 'free', subjects: [{ subjectId: 'cbse-g11-economics', depth: 'full' }, { subjectId: 'cbse-g11-accountancy', depth: 'light' }, { subjectId: 'cbse-g11-business', depth: 'light' }],
      parentIds: ['par_farida_khan'], mentorIds: ['mnt_kelvin_thomas'], weeklyHours: 9, goal: 'Chartered Accountant or Data Analyst?', currentChapterIds: ['cbse-g11-economics-ch07'], profileCompletionPct: 74,
      story: 'Strong in Accountancy; learns Economics by rote. Choosing between CA and Data Analyst.',
    }),
    depthSubject: 'cbse-g11-economics', chapters: 6,
    traits: { base: 0.84, spread: 0.05, slip: 0.04, blank: 0, overconf: 0.05, overconfDrift: 0, growth: 0.06, speed: 0.85, doneRate: 0.9, cgPenalty: { C2: 0.22 }, weak: { 'cbse-g11-economics-ch05-st2': 0.42, 'cbse-g11-economics-ch05-st3': 0.45, 'cbse-g11-economics-ch06-st1': 0.42 } },
    parent: { id: 'par_farida_khan', name: 'Farida Khan', relation: 'mother' },
    persona: { story: 'Strong in Accountancy; rote gaps in Economics; CA vs Data Analyst.', grade: 11, board: 'cbse', stream: 'commerce', programme: 'CBSE Commerce', order: 4 },
    profile: { p31: 2, p178: 'medium', p180: 'medium', p193: 'Laptop + broadband', p200: 'CEI', p212: 'C1', p230: 2, p163: 4, p8: 82, p268: 3 },
  },
  {
    student: student({
      id: 'lrn_nikhil_reddy', firstName: 'Nikhil', lastName: 'Reddy', board: 'cambridge', grade: 12, stream: 'commerce', programme: 'Cambridge A Level (Commerce)', school: 'Oakridge International School', city: 'Hyderabad',
      band: 'average', plan: 'application_support', subjects: [{ subjectId: 'cambridge-g12-business', depth: 'full' }, { subjectId: 'cambridge-g12-accountancy', depth: 'light' }, { subjectId: 'cambridge-g12-economics', depth: 'light' }],
      parentIds: ['par_lakshmi_reddy'], counsellorIds: ['csl_farah_siddiqui', 'csl_heena_qureshi'], weeklyHours: 10, goal: 'BSc Business in the UK or Canada', currentChapterIds: ['cambridge-g12-business-ch04'],
      joinedUtc: '2026-08-17T04:30:00.000Z', profileCompletionPct: 81, story: 'Average student, full Application Support subscriber applying to UK and Canada business programmes.',
    }),
    depthSubject: 'cambridge-g12-business', chapters: 3,
    traits: { base: 0.8, spread: 0.06, slip: 0.06, blank: 0.01, overconf: 0.05, overconfDrift: 0, growth: 0.05, speed: 0.95, doneRate: 0.8 },
    parent: { id: 'par_lakshmi_reddy', name: 'Lakshmi Reddy', relation: 'mother' },
    persona: { story: 'Application Support subscriber: UK and Canada business programmes.', grade: 12, board: 'cambridge', stream: 'commerce', programme: 'Cambridge A Level', order: 5 },
    profile: { p16: 'AAB predicted', p25: 'SAT not taken', p212: 'IELTS 7.0', p268: 3, p178: 'high', p181: 'high', p230: 5, p31: 2, p8: 76 },
  },
  {
    student: student({
      id: 'lrn_ananya_kapoor', firstName: 'Ananya', lastName: 'Kapoor', board: 'cambridge', grade: 10, stream: 'none', programme: 'Cambridge IGCSE', school: 'The Shri Ram School, Moulsari', city: 'Gurugram',
      band: 'excellent', plan: 'free', subjects: [{ subjectId: 'cambridge-g10-maths', depth: 'full' }, { subjectId: 'cambridge-g10-physics', depth: 'light' }, { subjectId: 'cambridge-g10-chemistry', depth: 'light' }, { subjectId: 'cambridge-g10-english', depth: 'light' }],
      parentIds: ['par_neha_kapoor'], counsellorIds: ['csl_heena_qureshi', 'csl_farah_siddiqui'], weeklyHours: 10, goal: 'Economics or Engineering at a top US university', currentChapterIds: ['cambridge-g10-maths-ch04'],
      joinedUtc: '2026-08-17T04:30:00.000Z', profileCompletionPct: 77, story: 'IGCSE topper aiming at US universities; used the free University Fit.',
    }),
    depthSubject: 'cambridge-g10-maths', chapters: 3,
    traits: { base: 0.92, spread: 0.04, slip: 0.03, blank: 0, overconf: 0, overconfDrift: 0, growth: 0.05, speed: 0.7, doneRate: 0.95 },
    parent: { id: 'par_neha_kapoor', name: 'Neha Kapoor', relation: 'mother' },
    persona: { story: 'IGCSE topper aiming at US universities; free University Fit used.', grade: 10, board: 'cambridge', stream: 'none', programme: 'Cambridge IGCSE', order: 6 },
    profile: { p16: '8 A* predicted', p25: 'SAT 1520 (practice)', p212: 'C2', p268: 4, p178: 'very_high', p181: 'very_high', p230: 5, p31: 2.5, p8: 94, p200: 'IAE' },
  },
];

// ------------------------------------------------------------------ simulation

function pCorrect(m: number, q: Question, t: Traits): number {
  const req = 0.12 + 0.11 * (Number(q.difficulty[1]) - 1) + 0.08 * (Number(q.conceptGroup[1]) - 1) + (t.cgPenalty?.[q.conceptGroup] ?? 0);
  const p = 1 / (1 + Math.exp(-9 * (m - req)));
  return p * (1 - t.slip * (q.difficulty === 'D2' || q.difficulty === 'D1' ? 1 : 0.5));
}

function answer(qs: Question[], mastery: Map<string, number>, t: Traits, overconf: number): ItemResponse[] {
  const out: ItemResponse[] = [];
  for (const q of qs) {
    if (R() < t.blank) continue;
    const p = pCorrect(mastery.get(q.subtopicId) ?? t.base, q, t);
    const correct = R() < p;
    const felt = clamp(p + overconf + (R() - 0.5) * 0.2, 0, 1);
    out.push({
      questionId: q.id, correct,
      secondsTaken: Math.round(q.minutes * 60 * t.speed * (0.7 + R() * 0.6)),
      confidence: clamp(Math.round(1 + felt * 4), 1, 5) as 1 | 2 | 3 | 4 | 5,
      ...(q.type === 'mcq' ? { answer: correct ? q.answer : pick(q.options!.filter((o) => o !== q.answer)) } : {}),
    });
  }
  return out;
}

function scoreOf(qs: Question[], rs: ItemResponse[]) {
  const ok = new Set(rs.filter((r) => r.correct).map((r) => r.questionId));
  return { score: qs.filter((q) => ok.has(q.id)).reduce((a, q) => a + q.marks, 0), maxScore: qs.reduce((a, q) => a + q.marks, 0) };
}

interface Built {
  cast: Cast;
  attempts: Attempt[];
  gaps: GapRecord[];
  mastery: MasteryRecord[];
  alr: AlrRecord[];
  plans: PlanRecord[];
  timetable: TimetableWeek[];
  tasks: Task[];
  events: EvidenceEvent[];
  questions: Question[];
}

function simulate(c: Cast): Built {
  const s = c.student;
  const qs = questionsFor(c.depthSubject);
  const qById = new Map(qs.map((q) => [q.id, q]));
  const getQ = (id: string) => qById.get(id);
  const subj = getSubject(c.depthSubject)!;
  const chapters = subj.chapters.slice(0, c.chapters);
  const truth = new Map<string, number>();
  for (const st of subj.subtopics) truth.set(st.id, clamp(c.traits.weak?.[st.id] ?? c.traits.base + (R() - 0.5) * 2 * c.traits.spread, -0.3, 0.98));

  const start = addDaysLocal(TODAY, -HISTORY_DAYS); // Wednesday 2026-10-07
  const ws0 = weekStartOf(start);
  const state: LearnerState = emptyState();
  const attempts: Attempt[] = [];
  const plans: PlanRecord[] = [];
  const events: EvidenceEvent[] = [];
  let n = 0;
  const att = (kind: Attempt['kind'], title: string, date: string, time: string, items: Question[], chapterId?: string, overconf = 0): Attempt => {
    n += 1;
    const responses = answer(items, truth, c.traits, overconf);
    const sc = scoreOf(items, responses);
    const startedUtc = istUtc(date, time);
    const mins = items.reduce((a, q) => a + q.minutes, 0);
    const a: Attempt = {
      id: `att_${s.id.slice(4)}_${String(n).padStart(2, '0')}`, learnerId: s.id, kind, title, subjectId: c.depthSubject, ...(chapterId ? { chapterId } : {}),
      questionIds: items.map((q) => q.id), responses, startedUtc, submittedUtc: new Date(Date.parse(startedUtc) + mins * 60_000 * c.traits.speed).toISOString(),
      minutesAllotted: Math.round(mins), ...sc, status: 'submitted',
    };
    attempts.push(a);
    return a;
  };
  const record = (a: Attempt) => {
    const eff = applyAttempt(s, a, state, attempts, getQ);
    events.push({
      eventId: `evt_${a.id}`, learnerId: s.id, timestampUtc: a.submittedUtc, sourceMethod: 'M14', type: 'assessment_submitted',
      payload: { attemptId: a.id, kind: a.kind, score: a.score, maxScore: a.maxScore, gaps: eff.gaps.map((g) => `${g.code}:${g.subtopicId}`), parameterIds: ['p8', 'p20', 'p60'] },
    });
    return eff;
  };
  const pathOf = (sid: string) => qs.filter((q) => q.subtopicId === sid && !q.id.endsWith(`-q9${String(PATH[subj.subtopics.find((x) => x.id === sid)!.weight].length + 1).padStart(2, '0')}`));
  const probesOf = (chapterId: string) => qs.filter((q) => q.chapterId === chapterId && q.alrRole === 'retention_probe');

  // baseline (pre-test items C1-D2 and C3-D2 of the chapters ahead)
  const baseItems = qs.filter((q) => chapters.some((ch) => ch.id === q.chapterId) && (q.conceptGroup === 'C1' || q.conceptGroup === 'C3') && q.difficulty === 'D2' && q.alrRole === 'practised');
  record(att('onboarding', 'Baseline check', start, '17:30', baseItems));

  const timetable: TimetableWeek[] = [];
  const tasks: Task[] = [];
  const weeks = Math.ceil(HISTORY_DAYS / 7) + 1;
  for (let w = 0; w < weeks; w++) {
    const ws = addDaysLocal(ws0, 7 * w);
    const thu = addDaysLocal(ws, 3);
    const sat = addDaysLocal(ws, 5);
    const ch = chapters[w];
    // learning: open gaps improve with the plan; everything else drifts up a little with teaching
    for (const g of state.gaps.values()) if (g.status !== 'closed') truth.set(g.subtopicId, clamp(truth.get(g.subtopicId)! + c.traits.growth, 0, 0.98));
    for (const g of state.gaps.values()) if (g.status === 'suspected' || g.status === 'confirmed') state.gaps.set(g.subtopicId, { ...g, status: 'in_progress' });

    // timetable for this week from the state on Monday
    const weekNow = ws === weekStartOf(TODAY) ? NOW : istUtc(ws, '00:05');
    const tw = buildWeek(s, ws, { gaps: [...state.gaps.values()], mastery: [...state.mastery.values()], sessions: [], now: istUtc(ws, '00:05') }, w === 0 ? 'initial' : 'weekly');
    for (const b of tw.blocks) {
      if (b.kind === 'buffer') continue;
      if (b.endUtc <= weekNow) b.status = R() < c.traits.doneRate ? 'done' : 'missed';
    }
    tw.generatedUtc = istUtc(ws, '00:05');
    if (ws <= weekStartOf(TODAY)) timetable.push(tw);
    if (ws <= weekStartOf(TODAY)) {
      for (const b of tw.blocks) {
        if (b.kind === 'buffer' || b.kind === 'session') continue;
        const kind: Task['kind'] = b.kind === 'gap' || b.kind === 'carry_over' ? 'practise' : b.kind === 'review' ? 'retrieve' : b.kind === 'weekly_test' ? 'test' : 'learn';
        tasks.push({
          id: `task_${b.id.slice(4)}`, learnerId: s.id, title: b.title, kind, dueDate: b.date, minutes: b.minutes, source: 'timetable', refId: b.refId ?? b.id,
          status: b.status === 'done' ? 'done' : b.status === 'missed' ? 'skipped' : 'todo', createdUtc: tw.generatedUtc,
          ...(b.status === 'done' ? { completedUtc: b.endUtc } : {}), subjectId: c.depthSubject,
          ...(b.kind === 'weekly_test' ? { href: '/student/assessments' } : {}),
        });
      }
    }
    if (thu > TODAY || (thu === TODAY)) continue;

    // retention probe for last week's chapter, then this week's chapter check
    const prevCh = chapters[w - 1];
    if (prevCh) record(att('retention_probe', `7-day review: ${prevCh.name}`, thu, '17:00', probesOf(prevCh.id), prevCh.id, c.traits.overconf + c.traits.overconfDrift * w));
    if (ch) {
      const items = ch.subtopicIds.flatMap(pathOf);
      const eff = record(att('chapter_check', `Chapter check: ${ch.name}`, thu, '17:30', items, ch.id, c.traits.overconf + c.traits.overconfDrift * w));
    }
    // Saturday weekly test re-checks up to 3 open gaps with their full paths
    if (sat < TODAY) {
      const open = [...state.gaps.values()].filter((g) => g.status !== 'closed').sort((a, b) => b.size - a.size);
      const full = open.filter((g) => g.code !== 'G6' && g.code !== 'G4').slice(0, 6);
      const probe = open.filter((g) => g.code === 'G6' || g.code === 'G4');
      if (full.length) record(att('weekly', `Weekly test, week of ${ws}`, sat, '10:00', full.flatMap((g) => pathOf(g.subtopicId)), undefined, c.traits.overconf + c.traits.overconfDrift * w));
      if (probe.length) record(att('retention_probe', `Spaced review, week of ${ws}`, sat, '11:00', qs.filter((q) => q.alrRole === 'retention_probe' && probe.some((g) => g.subtopicId === q.subtopicId)), undefined, c.traits.overconf + c.traits.overconfDrift * w));
    }
    // plan after the week's tests
    const gapsNow = [...state.gaps.values()];
    if (gapsNow.some((g) => g.status !== 'closed')) {
      const prev = plans[plans.length - 1];
      if (prev) prev.status = 'replaced';
      const oldest = gapsNow.filter((g) => g.status !== 'closed' && g.size >= 2).map((g) => g.detectedUtc).sort()[0];
      const freeWeeks = oldest ? Math.floor((Date.parse(istUtc(sat, '18:00')) - Date.parse(oldest)) / (7 * 86_400_000)) : 0;
      plans.push(planFor(s, gapsNow, istUtc(sat, '18:00'), freeWeeks, Object.entries(c.profile).map(([paramId, value]) => ({ paramId, value, asOfUtc: s.joinedUtc }))));
    }
  }

  return {
    cast: c, attempts, questions: qs, plans, timetable, tasks, events,
    gaps: [...state.gaps.values()], mastery: [...state.mastery.values()], alr: state.alr,
  };
}

// ------------------------------------------------------------------ profile values

let PARAMS: ProfileParameter[] = [];
function profileFor(c: Cast, b: Built): ProfileValue[] {
  const s = c.student;
  const r = rng(`profile-${s.id}`);
  const out: ProfileValue[] = [];
  const subjects = s.subjects.map((x) => x.subjectId);
  const lastPct = b.attempts.length ? Math.round((b.attempts.reduce((a, x) => a + x.score / Math.max(1, x.maxScore), 0) / b.attempts.length) * 100) : 0;
  const fixed: Record<string, unknown> = {
    p1: `Grade ${s.grade}`, p2: `${s.school}, ${s.city}`, p3: s.board.toUpperCase(), p5: s.stream === 'none' ? subjects.join(', ') : `${s.stream} stream`,
    p8: lastPct, p20: Math.min(100, Math.round((c.chapters / (getSubject(c.depthSubject)?.chapters.length ?? 14)) * 100)), p60: Math.round(c.traits.doneRate * 100),
    ...c.profile,
  };
  const generic = (p: ProfileParameter): unknown => {
    const t = p.dataType.toLowerCase();
    if (t.includes('scale 1-5')) return 1 + Math.floor(r() * 5);
    if (t.includes('%') || t.includes('0-100')) return 40 + Math.floor(r() * 55);
    if (t.includes('number') || t.includes('minutes') || t.includes('hours')) return round1(1 + r() * 4);
    if (t.includes('bool') || t.includes('y/n')) return r() < 0.6;
    return pick(['Low', 'Moderate', 'High']);
  };
  const chosen = PARAMS.filter((p) => p.tier !== 'C' && (p.number % 3 === 0 || ['Academic Profile', 'Learning Behaviour'].includes(p.section)) && p.number <= 300).slice(0, 70);
  const ids = new Set([...chosen.map((p) => p.id), ...Object.keys(fixed)]);
  for (const id of ids) {
    const p = PARAMS.find((x) => x.id === id);
    if (!p) continue;
    const fromEvidence = ['p8', 'p20', 'p60'].includes(id);
    out.push({
      learnerId: s.id, paramId: id, value: id in fixed ? fixed[id] : generic(p),
      source: fromEvidence ? 'M14' : p.phase1Default ?? p.methods[0] ?? 'M1',
      asOfUtc: fromEvidence ? NOW : s.joinedUtc,
      confidence: fromEvidence ? 'high' : id in fixed ? 'medium' : 'low', tier: p.tier,
    });
  }
  return out;
}

// ------------------------------------------------------------------ adults, classes, extras

const BG_NAMES = ['Aditi Verma', 'Arnav Gupta', 'Diya Malhotra', 'Ishaan Chawla', 'Kavya Nair', 'Manav Bhatia', 'Naina Joshi', 'Pranav Iyer', 'Riya Sethi', 'Siddharth Rao', 'Tanvi Mehra', 'Vivaan Kapoor', 'Yash Agarwal', 'Zara Sheikh', 'Aryan Saxena', 'Meher Gill', 'Kunal Bajaj', 'Sneha Pillai'];

function backgroundStudents(subjectId: string, chapters: number, cluster: { subtopicId: string; code: 'G3' }, count: number, offset: number): BackgroundStudent[] {
  const subj = getSubject(subjectId)!;
  const covered = new Set(subj.chapters.slice(0, chapters).map((c) => c.id));
  const subs = subj.subtopics.filter((s) => covered.has(s.chapterId));
  return Array.from({ length: count }, (_, i) => {
    const name = BG_NAMES[(i + offset) % BG_NAMES.length];
    const id = `lrn_bg_${name.toLowerCase().replace(/[^a-z ]/g, '').replace(' ', '_')}_${subjectId.split('-')[1]}`;
    const ability = 0.45 + R() * 0.45;
    const mastery: BackgroundStudent['mastery'] = {};
    const gaps: BackgroundStudent['gaps'] = [];
    for (const s of subs) {
      let lvl = clamp(Math.round(ability * 5 + (R() - 0.5) * 2.2), 0, 5);
      if (s.id === cluster.subtopicId && i < 5) lvl = 2; // the class cluster
      const level = lvl as 0 | 1 | 2 | 3 | 4 | 5;
      mastery[s.id] = { level, pMastery: round1(clamp(level / 5 + (R() - 0.5) * 0.1, 0, 1) * 10) / 10, lastTestedUtc: istUtc(addDaysLocal(TODAY, -Math.floor(R() * 40) - 1), '17:30') };
      const code = ({ 0: 'G1', 1: 'G2', 2: 'G3', 3: 'G5' } as Record<number, 'G1' | 'G2' | 'G3' | 'G5'>)[level];
      if (code) gaps.push({ subtopicId: s.id, code, level, hoursToClose: round1((5 - level) * 0.9), status: 'suspected' });
    }
    const testScores = subj.chapters.slice(0, chapters).map((c, k) => ({ title: `Chapter check: ${c.name}`, date: addDaysLocal(TODAY, -HISTORY_DAYS + 1 + 7 * k), pct: Math.round(clamp(ability * 100 + (R() - 0.5) * 20, 20, 99)) }));
    return { id, name, mastery, gaps, testScores };
  });
}

function main() {
  PARAMS = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'profile', 'parameters.json'), 'utf8')).items;
  const careers: Career[] = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'catalogues', 'careers.json'), 'utf8')).items;
  fs.rmSync(path.join(OUT, 'students'), { recursive: true, force: true });
  fs.rmSync(path.join(OUT, 'classes'), { recursive: true, force: true });
  fs.rmSync(path.join(OUT, 'adults'), { recursive: true, force: true });

  const built = CAST.map(simulate);
  for (const b of built) {
    const s = b.cast.student;
    const id = s.id;
    write(`questions/${b.cast.depthSubject}.json`, b.questions);
    const profile = profileFor(b.cast, b);
    const alrLatest = b.alr.length ? b.alr[b.alr.length - 1] : undefined;
    const st: Student = { ...s, band: alrLatest?.band ?? s.band };
    write(`students/${id}/student.json`, [st]);
    write(`students/${id}/profile.json`, profile);
    const seedEvents: EvidenceEvent[] = [
      { eventId: `evt_${id}_signup`, learnerId: id, timestampUtc: s.joinedUtc, sourceMethod: 'M1', type: 'account_created', payload: { parameterIds: ['p1', 'p2', 'p3'] } },
      { eventId: `evt_${id}_onboarding_form`, learnerId: id, timestampUtc: s.joinedUtc, sourceMethod: 'M2', type: 'onboarding_form', payload: { parameterIds: profile.filter((p) => p.source !== 'M14').map((p) => p.paramId) } },
    ];
    if (id === 'lrn_rohan_das') seedEvents.push({ eventId: `evt_${id}_wellbeing_1`, learnerId: id, timestampUtc: istUtc('2026-11-06', '15:00'), sourceMethod: 'M11', type: 'wellbeing_checkin', payload: { flag: true, summary: 'Reports exam stress and pressure at home; support plan agreed.', parameterIds: ['p150'], tier: 'T3', by: 'csl_heena_qureshi' } });
    write(`students/${id}/events.json`, [...seedEvents, ...b.events].sort((a, z) => a.timestampUtc.localeCompare(z.timestampUtc)));
    write(`students/${id}/attempts.json`, b.attempts);
    write(`students/${id}/mastery.json`, b.mastery);
    write(`students/${id}/alr.json`, b.alr);
    write(`students/${id}/gaps.json`, b.gaps);
    write(`students/${id}/plans.json`, b.plans);
    write(`students/${id}/timetable.json`, b.timetable);

    // careers
    const prof = profile.filter((p) => p.tier !== 'T3' && p.tier !== 'C');
    const fits = mapCareers(prof, careers, { grade: s.grade, stream: s.stream, limit: 8 });
    const shortlist = id === 'lrn_sara_khan' ? ['career-chartered-accountant', 'career-data-analyst'] : id === 'lrn_ananya_kapoor' ? ['career-economist'] : id === 'lrn_nikhil_reddy' ? ['career-management-consultant', 'career-business-analyst'] : [];
    const cm: CareerMatches = {
      learnerId: id, computedUtc: NOW, fits, shortlist,
      gaps: Object.fromEntries(shortlist.map((cid) => [cid, careerGap(prof, careers.find((c) => c.id === cid)!, { grade: s.grade, stream: s.stream })])),
    };
    write(`students/${id}/careers.json`, [cm]);

    // tasks: timetable tasks + a teacher-assigned check for Kabir
    const tasks = [...b.tasks];
    if (id === 'lrn_kabir_singh') {
      tasks.push({ id: `task_${id.slice(4)}_tch_1`, learnerId: id, title: 'Re-teach set: ' + (getSubject('cbse-g9-maths')!.subtopics.find((x) => x.id === 'cbse-g9-maths-ch05-st3')?.name ?? 'Chapter 5'), kind: 'test', dueDate: '2026-11-20', status: 'todo', source: 'teacher', createdBy: 'tch_suresh_pillai', createdUtc: istUtc('2026-11-16', '13:00'), minutes: 20, subjectId: 'cbse-g9-maths', refId: 'cbse-g9-maths-ch05-st3', questionIds: b.questions.filter((q) => q.subtopicId === 'cbse-g9-maths-ch05-st3' && q.alrRole !== 'retention_probe').map((q) => q.id), href: `/student/assessments/task.task_${id.slice(4)}_tch_1` });
    }
    write(`students/${id}/tasks.json`, tasks);

    // sessions and meeting notes with Heena (and Kelvin for Sara)
    const sessions: Session[] = [];
    const meetings: MeetingNote[] = [];
    const past = istUtc(addDaysLocal(TODAY, -9), '16:00');
    sessions.push({ id: `ses_${id.slice(4)}_csl_1`, code: 'C-1', learnerId: id, learnerIds: [id], hostId: 'csl_heena_qureshi', hostRole: 'counsellor', kind: 'counselling', title: 'Monthly check-in with Heena', startUtc: past, minutes: 30, status: 'completed', mode: 'online', meetingNoteId: `mtg_${id.slice(4)}_1` });
    meetings.push({ id: `mtg_${id.slice(4)}_1`, learnerId: id, staffId: 'csl_heena_qureshi', date: addDaysLocal(TODAY, -9), kind: 'academic', tier: 'T1', summary: `Reviewed ${s.firstName}'s gaps and timetable; agreed to keep the free plan steps and re-test after the weekly test.`, decisions: ['Keep current study windows', 'Re-test gaps on Saturday'], actionItems: [{ id: `ai_${id.slice(4)}_1`, title: 'Finish the gap practice blocks this week', dueOn: addDaysLocal(TODAY, -2), done: true }] });
    sessions.push({ id: `ses_${id.slice(4)}_csl_2`, code: 'C-2', learnerId: id, learnerIds: [id], hostId: 'csl_heena_qureshi', hostRole: 'counsellor', kind: 'counselling', title: 'Check-in with Heena', startUtc: istUtc(addDaysLocal(TODAY, 6), '16:30'), minutes: 30, status: 'scheduled', mode: 'online', joinUrl: 'https://meet.learnibility.demo/heena' });
    if (id === 'lrn_sara_khan') {
      sessions.push({ id: 'ses_sara_khan_mnt_1', code: 'M-1', learnerId: id, learnerIds: [id], hostId: 'mnt_kelvin_thomas', hostRole: 'mentor', kind: 'career', title: 'Career session: CA vs Data Analyst', startUtc: istUtc('2026-11-12', '18:00'), minutes: 45, status: 'completed', mode: 'online', meetingNoteId: 'mtg_sara_khan_career_1' });
      sessions.push({ id: 'ses_sara_khan_mnt_2', code: 'M-2', learnerId: id, learnerIds: [id], hostId: 'mnt_kelvin_thomas', hostRole: 'mentor', kind: 'career', title: 'Career session: skill plan review', startUtc: istUtc('2026-11-26', '18:00'), minutes: 45, status: 'scheduled', mode: 'online', joinUrl: 'https://meet.learnibility.demo/kelvin' });
      meetings.push({ id: 'mtg_sara_khan_career_1', learnerId: id, staffId: 'mnt_kelvin_thomas', date: '2026-11-12', kind: 'career', tier: 'T1', summary: 'Compared Chartered Accountant (ICAI route, 4.5 to 5 years) with Data Analyst (BSc + SQL/Python skills). Sara enjoys accounting logic but wants more variety; both stay open.', decisions: ['Keep both careers shortlisted', 'Try a free SQL course before deciding'], actionItems: [{ id: 'ai_sara_career_1', title: 'Finish the first 3 modules of a free SQL course', dueOn: '2026-11-25', taskId: 'task_sara_khan_mnt_1' }, { id: 'ai_sara_career_2', title: 'Read the ICAI Foundation syllabus', dueOn: '2026-11-22', taskId: 'task_sara_khan_mnt_2' }] });
      tasks.push(
        { id: 'task_sara_khan_mnt_1', learnerId: id, title: 'Finish the first 3 modules of a free SQL course', kind: 'action_item', dueDate: '2026-11-25', status: 'todo', source: 'mentor', createdBy: 'mnt_kelvin_thomas', createdUtc: istUtc('2026-11-12', '19:00'), refId: 'mtg_sara_khan_career_1' },
        { id: 'task_sara_khan_mnt_2', learnerId: id, title: 'Read the ICAI Foundation syllabus', kind: 'action_item', dueDate: '2026-11-22', status: 'todo', source: 'mentor', createdBy: 'mnt_kelvin_thomas', createdUtc: istUtc('2026-11-12', '19:00'), refId: 'mtg_sara_khan_career_1' },
      );
      write(`students/${id}/tasks.json`, tasks);
    }
    if (id === 'lrn_rohan_das') meetings.push({ id: 'mtg_rohan_das_wellbeing_1', learnerId: id, staffId: 'csl_heena_qureshi', date: '2026-11-06', kind: 'wellbeing', tier: 'T3', summary: 'Rohan reports exam stress and pressure at home. Agreed shorter study blocks and a weekly 10-minute check-in.', decisions: ['Shorter 25-minute blocks', 'Weekly check-in'], actionItems: [{ id: 'ai_rohan_wb_1', title: 'Weekly 10-minute check-in with Heena', dueOn: '2026-11-20' }] });
    write(`students/${id}/sessions.json`, sessions);
    write(`students/${id}/meetings.json`, meetings);

    // timetable requests (Kabir: one approved, one pending)
    const reqs: TimetableRequest[] = [];
    if (id === 'lrn_kabir_singh') {
      const cur = b.timetable[b.timetable.length - 1];
      const thuBlock = cur.blocks.find((x) => x.date === '2026-11-19' && x.kind !== 'buffer');
      reqs.push({ id: 'req_kabir_singh_1', learnerId: id, createdUtc: istUtc('2026-10-27', '20:10'), weekStart: '2026-10-26', blockIds: [], kind: 'move', reason: 'Cricket practice on Wednesdays this month.', proposed: 'Move Wednesday study to Sunday 17:00', status: 'approved', counsellorId: 'csl_heena_qureshi', decidedBy: 'csl_heena_qureshi', decidedUtc: istUtc('2026-10-28', '11:00'), decisionNote: 'Approved; Sunday window added.' });
      reqs.push({ id: 'req_kabir_singh_2', learnerId: id, createdUtc: istUtc('2026-11-17', '21:05'), weekStart: '2026-11-16', blockIds: thuBlock ? [thuBlock.id] : [], kind: 'move', reason: 'School science exhibition runs late on Thursday.', proposed: { date: '2026-11-22', start: '17:00', end: '18:00' }, status: 'pending', counsellorId: 'csl_heena_qureshi' });
    }
    write(`students/${id}/requests.json`, reqs);

    // documents: report card + auto-filed test results
    const docs: DocumentRecord[] = [
      { id: `doc_${id.slice(4)}_rc`, learnerId: id, folder: 'academics', title: s.board === 'cbse' ? 'Term 1 report card' : 'Mid-year report', fileName: 'report-card-term1.pdf', kind: 'report_card', uploadedUtc: istUtc('2026-10-03', '18:00'), source: 'M5', sizeKb: 412 },
      ...b.attempts.filter((a) => a.kind === 'chapter_check').map((a) => ({ id: `doc_${a.id}`, learnerId: id, folder: 'academics' as const, title: `${a.title} result`, fileName: `${a.id}.pdf`, kind: 'test_result' as const, uploadedUtc: a.submittedUtc, source: 'auto' as const, sizeKb: 96, refId: a.id })),
      { id: `doc_${id.slice(4)}_cert`, learnerId: id, folder: 'activities', title: id === 'lrn_sara_khan' ? 'Commerce quiz, 2nd place' : 'Inter-school sports certificate', fileName: 'certificate.pdf', kind: 'certificate', uploadedUtc: istUtc('2026-09-12', '18:00'), source: 'M6', sizeKb: 220 },
    ];
    if (s.grade >= 12) docs.push({ id: `doc_${id.slice(4)}_passport`, learnerId: id, folder: 'application_documents', title: 'Passport (bio page)', fileName: 'passport.pdf', kind: 'id_proof', uploadedUtc: istUtc('2026-09-02', '18:00'), source: 'M5', sizeKb: 640, requiresPlan: 'application_support' });
    write(`students/${id}/documents.json`, docs);

    // consents
    const consents: Consent[] = [
      { id: `cns_${id.slice(4)}_1`, learnerId: id, grantedById: b.cast.parent.id, scope: 'edu_personalisation', version: 'v1.2', grantedUtc: s.joinedUtc },
      { id: `cns_${id.slice(4)}_2`, learnerId: id, grantedById: b.cast.parent.id, scope: 'share_with_school', version: 'v1.2', grantedUtc: s.joinedUtc },
      { id: `cns_${id.slice(4)}_3`, learnerId: id, grantedById: b.cast.parent.id, scope: 'wellbeing_screening', version: 'v1.0', grantedUtc: s.joinedUtc },
      { id: `cns_${id.slice(4)}_4`, learnerId: id, grantedById: b.cast.parent.id, scope: 'marketing', version: 'v1.0', grantedUtc: s.joinedUtc, revokedUtc: istUtc('2026-09-20', '10:00') },
    ];
    write(`students/${id}/consents.json`, consents);

    // invoices and messages
    const invoices: Invoice[] = [];
    if (s.plan === 'application_support') {
      for (const [k, d] of ['2026-09-01', '2026-10-01', '2026-11-01'].entries()) invoices.push({ id: `inv_${id.slice(4)}_${k + 1}`, learnerId: id, payerId: b.cast.parent.id, issuedUtc: istUtc(d, '09:00'), dueDate: addDaysLocal(d, 7), status: 'paid', paidUtc: istUtc(addDaysLocal(d, 2), '12:00'), lines: [{ title: 'Application Support, monthly', amountInr: 4999, planId: 'application_support' }], amountInr: 4999 });
    }
    if (id === 'lrn_rohan_das') {
      invoices.push({ id: 'inv_rohan_das_1', learnerId: id, payerId: 'par_anita_das', issuedUtc: istUtc('2026-10-05', '09:00'), dueDate: '2026-10-12', status: 'paid', paidUtc: istUtc('2026-10-06', '19:30'), lines: [{ title: 'Board-exam revision workshop (4 group sessions)', amountInr: 1400 }], amountInr: 1400 });
      invoices.push({ id: 'inv_rohan_das_2', learnerId: id, payerId: 'par_anita_das', issuedUtc: istUtc('2026-11-15', '09:00'), dueDate: '2026-11-22', status: 'due', lines: [{ title: 'Mock test series, Class 10 Maths', amountInr: 600 }], amountInr: 600 });
    }
    write(`students/${id}/invoices.json`, invoices);
    const msgs: Message[] = [];
    const t = `${id}:${b.cast.parent.id}:csl_heena_qureshi`;
    msgs.push({ id: `msg_${id.slice(4)}_1`, threadId: t, learnerId: id, from: 'csl_heena_qureshi', toIds: [b.cast.parent.id], text: `Hello ${b.cast.parent.name.split(' ')[0]}, ${s.firstName}'s weekly summary is ready on your Home page. Happy to talk if anything looks off.`, sentUtc: istUtc('2026-11-15', '18:00'), readBy: [b.cast.parent.id] });
    if (id === 'lrn_rohan_das') {
      msgs.push({ id: 'msg_rohan_das_2', threadId: t, learnerId: id, from: 'par_anita_das', toIds: ['csl_heena_qureshi'], text: 'Thank you. His Maths still looks weak after three weeks. Should we get him a tutor?', sentUtc: istUtc('2026-11-15', '21:10'), readBy: ['csl_heena_qureshi'] });
      msgs.push({ id: 'msg_rohan_das_3', threadId: t, learnerId: id, from: 'csl_heena_qureshi', toIds: ['par_anita_das'], text: 'Yes, the plan now suggests a paid Maths tutor: his gaps span three chapters and the free steps have run three weeks. You can see the reason and approve it under Plan and spend.', sentUtc: istUtc('2026-11-16', '10:05'), readBy: [] });
    }
    if (id === 'lrn_sara_khan') msgs.push({ id: 'msg_sara_khan_kelvin', threadId: `${id}:mnt_kelvin_thomas`, learnerId: id, from: 'mnt_kelvin_thomas', toIds: [id], text: 'Great session today, Sara. Start the SQL modules and tell me how they feel next time.', sentUtc: istUtc('2026-11-12', '19:05'), readBy: [id] });
    write(`students/${id}/messages.json`, msgs);
    write(`students/${id}/shortlist.json`, []);
  }

  // adults
  const parents: Adult[] = CAST.map((c) => {
    const [firstName, lastName] = c.parent.name.split(' ');
    const kids = c.parent.id === 'par_neha_kapoor' ? ['lrn_aarav_kapoor', 'lrn_ananya_kapoor'] : [c.student.id];
    return { id: c.parent.id, role: 'parent', firstName, lastName, name: c.parent.name, city: c.student.city, learnerIds: kids, relation: Object.fromEntries(kids.map((k) => [k, c.parent.relation])) } as Adult;
  });
  write('adults/parents.json', parents);
  write('adults/teachers.json', [
    { id: 'tch_suresh_pillai', role: 'teacher', firstName: 'Suresh', lastName: 'Pillai', name: 'Suresh Pillai', city: 'New Delhi', headline: 'CBSE Maths teacher, grades 9 and 10', school: 'Delhi Public School, Dwarka', learnerIds: ['lrn_kabir_singh', 'lrn_rohan_das'], sectionIds: ['sec-cbse-g9-maths-a', 'sec-cbse-g10-maths-b'], subjectIds: ['cbse-g9-maths', 'cbse-g10-maths'] },
  ] satisfies Adult[]);
  const all = CAST.map((c) => c.student.id);
  write('adults/counsellors.json', [
    { id: 'csl_heena_qureshi', role: 'counsellor', firstName: 'Heena', lastName: 'Qureshi', name: 'Heena Qureshi', headline: 'Academic and wellbeing counsellor', focus: 'academic_wellbeing', learnerIds: all },
    { id: 'csl_farah_siddiqui', role: 'counsellor', firstName: 'Farah', lastName: 'Siddiqui', name: 'Farah Siddiqui', headline: 'University applications counsellor (UK, US, Canada)', focus: 'applications', learnerIds: ['lrn_ananya_kapoor', 'lrn_nikhil_reddy', 'lrn_tara_menon', 'lrn_arjun_nair'] },
  ] satisfies Adult[]);
  write('adults/mentors.json', [
    { id: 'mnt_kelvin_thomas', role: 'mentor', firstName: 'Kelvin', lastName: 'Thomas', name: 'Kelvin Thomas', headline: 'Career mentor', focus: 'careers', learnerIds: ['lrn_sara_khan', 'lrn_arjun_nair', 'lrn_kunal_verma'] },
  ] satisfies Adult[]);

  // classes: Kabir's 9A and Rohan's 10B, each persona + 9 background learners
  const kabir = built.find((b) => b.cast.student.id === 'lrn_kabir_singh')!;
  const rohan = built.find((b) => b.cast.student.id === 'lrn_rohan_das')!;
  const sec9 = backgroundStudents('cbse-g9-maths', kabir.cast.chapters, { subtopicId: 'cbse-g9-maths-ch05-st3', code: 'G3' }, 9, 0);
  const sec10 = backgroundStudents('cbse-g10-maths', rohan.cast.chapters, { subtopicId: 'cbse-g10-maths-ch04-st1', code: 'G3' }, 9, 9);
  write('classes/sec-cbse-g9-maths-a.json', [{ id: 'sec-cbse-g9-maths-a', name: '9A Maths', teacherId: 'tch_suresh_pillai', subjectId: 'cbse-g9-maths', board: 'cbse', grade: 9, school: 'Delhi Public School, Dwarka', learnerIds: ['lrn_kabir_singh', ...sec9.map((x) => x.id)], background: sec9 } satisfies Section]);
  write('classes/sec-cbse-g10-maths-b.json', [{ id: 'sec-cbse-g10-maths-b', name: '10B Maths', teacherId: 'tch_suresh_pillai', subjectId: 'cbse-g10-maths', board: 'cbse', grade: 10, school: 'Delhi Public School, Dwarka', learnerIds: ['lrn_rohan_das', ...sec10.map((x) => x.id)], background: sec10 } satisfies Section]);

  // login picker entries for fixture people not in the persona index
  const personas: PersonaSummary[] = [
    ...CAST.map((c) => ({ id: c.student.id, role: 'student' as const, name: c.student.name, ...c.persona })),
    ...parents.map((p, i) => ({ id: p.id, role: 'parent' as const, name: p.name, story: `Parent of ${p.learnerIds.map((l) => CAST.find((c) => c.student.id === l)?.student.firstName ?? l.split('_')[1].replace(/^./, (x) => x.toUpperCase())).join(' and ')}.`, linkedLearnerIds: p.learnerIds, order: i + 1 })),
    { id: 'lrn_zoya_fernandes', role: 'student', name: 'Zoya Fernandes', story: 'Signed up today; onboarding test not taken yet (live demo).', grade: 9, board: 'cbse', stream: 'none', programme: 'CBSE Class 9', order: 7 },
    { id: 'csl_heena_qureshi', role: 'counsellor', name: 'Heena Qureshi', story: 'Academic and wellbeing counsellor for every student.', linkedLearnerIds: all, order: 1 },
    { id: 'csl_farah_siddiqui', role: 'counsellor', name: 'Farah Siddiqui', story: 'Applications counsellor: Ananya, Nikhil, Tara and Arjun.', linkedLearnerIds: ['lrn_ananya_kapoor', 'lrn_nikhil_reddy', 'lrn_tara_menon', 'lrn_arjun_nair'], order: 2 },
    { id: 'tch_suresh_pillai', role: 'teacher', name: 'Suresh Pillai', story: 'CBSE Maths teacher, 9A and 10B.', linkedLearnerIds: ['lrn_kabir_singh', 'lrn_rohan_das'], order: 1 },
    { id: 'mnt_kelvin_thomas', role: 'mentor', name: 'Kelvin Thomas', story: 'Career mentor for Sara, Arjun and Kunal.', linkedLearnerIds: ['lrn_sara_khan', 'lrn_arjun_nair', 'lrn_kunal_verma'], order: 1 },
  ];
  fs.writeFileSync(path.join(OUT, 'personas.json'), JSON.stringify({ schemaVersion: 1, generatedBy: GEN, items: personas }, null, 1) + '\n');

  // summary
  for (const b of built) {
    const open = b.gaps.filter((g) => g.status !== 'closed');
    const plan = b.plans[b.plans.length - 1];
    console.log(
      `${b.cast.student.id.padEnd(20)} attempts ${String(b.attempts.length).padStart(2)}  gaps open ${String(open.length).padStart(2)} [${[...new Set(open.map((g) => g.code))].join(',')}]` +
        `  chapters w/ gaps ${new Set(open.map((g) => g.chapterId)).size}  ALR ${b.alr.length ? b.alr[b.alr.length - 1].LRS : '-'} ${b.alr.length ? b.alr[b.alr.length - 1].MCI : ''}` +
        `  plan: freeWeeks ${plan?.freePlanWeeks ?? '-'} paid ${plan?.plan.paidTuition.recommended ?? '-'}  weeks ${b.timetable.length}`,
    );
  }
}

main();
