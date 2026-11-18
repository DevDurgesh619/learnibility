/**
 * W3-P personas: the shared simulator (lifted from scripts/fixtures/build.ts and generalised).
 *
 *   trait model    → per-subtopic true mastery + slip, blanks, confidence bias, time pressure, forgetting,
 *                    concept-group / question-type penalties, growth while a gap is being worked on
 *   timeline       → starting test, chapter checks on the school's pace, 7-day retention probes, Saturday
 *                    weekly tests on open gaps, practice Form B after remediation, mocks
 *   answers        → P(correct) from mastery vs item demand; time and confidence from traits
 *   engines        → lib/data/derive.ts (applyAttempt → diagnoseGaps, computeAlr; planFor → planInterventions;
 *                    buildWeek → buildTimetable), in time order, after every test
 *
 * Randomness: one seeded generator per learner ("learnibility-2026:{learnerId}"), so adding a persona never
 * changes another persona's numbers, and a rerun is byte-identical.
 */
import fs from 'node:fs';
import path from 'node:path';
import type { ConceptGroup, Difficulty, EvidenceEvent, ItemResponse, Question, QuestionType, Weight } from '@/lib/types';
import { getSubject } from '@/lib/data/catalogue';
import { addDaysLocal, applyAttempt, buildWeek, emptyState, planFor, summariseAlr, weekStartOf, type LearnerState } from '@/lib/data/derive';
import type { Attempt, GapRecord, PlanRecord, Student, Task, TimetableWeek, AlrRecord, MasteryRecord } from '@/lib/data/types';

export const ROOT = process.cwd();
export const NOW = '2026-11-18T03:30:00.000Z'; // DEMO_NOW (09:00 IST)
export const TODAY = '2026-11-18';
export const SEED = 'learnibility-2026';

// ------------------------------------------------------------------ seeded random

function hashSeed(s: string): number {
  let h = 1779033703 ^ s.length;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 3432918353), (h = (h << 13) | (h >>> 19));
  return h >>> 0;
}
export function rng(seed: string) {
  let a = hashSeed(seed);
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
export type Rand = () => number;
export const clamp = (x: number, a: number, b: number) => Math.max(a, Math.min(b, x));
export const round1 = (x: number) => Math.round(x * 10) / 10;
export const round2 = (x: number) => Math.round(x * 100) / 100;
export const istUtc = (date: string, hhmm: string) => new Date(Date.parse(`${date}T${hhmm}:00+05:30`)).toISOString();

// ------------------------------------------------------------------ questions: real bank when validated, else fixture items

/** Check path per weight (workbook: L 5, S 6, H 8) plus one extra retention probe. Same as W2-0. */
const PATH: Record<Weight, [ConceptGroup, Difficulty, QuestionType][]> = {
  L: [['C1', 'D1', 'mcq'], ['C2', 'D2', 'short'], ['C3', 'D2', 'numerical'], ['C3', 'D3', 'multi_step'], ['C4', 'D3', 'case']],
  S: [['C1', 'D1', 'mcq'], ['C1', 'D2', 'mcq'], ['C2', 'D2', 'short'], ['C3', 'D2', 'numerical'], ['C3', 'D3', 'multi_step'], ['C4', 'D3', 'case']],
  H: [['C1', 'D1', 'mcq'], ['C1', 'D2', 'mcq'], ['C2', 'D2', 'short'], ['C3', 'D2', 'numerical'], ['C3', 'D3', 'multi_step'], ['C3', 'D4', 'multi_step'], ['C4', 'D3', 'case'], ['C4', 'D4', 'case']],
};
export const PATH_LENGTH: Record<Weight, number> = { L: 5, S: 6, H: 8 };
const GAP_ON_WRONG: Record<ConceptGroup, Question['likelyGapOnWrong']> = { C1: 'G1', C2: 'G2', C3: 'G3', C4: 'G5' };
const STEM: Record<ConceptGroup, (n: string) => string> = {
  C1: (n) => `Which of these statements about ${n.toLowerCase()} is correct?`,
  C2: (n) => `In one or two lines, explain the key idea behind ${n.toLowerCase()}.`,
  C3: (n) => `Apply ${n.toLowerCase()} to solve the routine problem shown, giving each step.`,
  C4: (n) => `A new situation: use ${n.toLowerCase()} to decide what to do, and justify your answer.`,
};

/** W2-0 fixture items ({subtopicId}-q9NN): used only where the subject's real bank is not validated yet. */
export function fixtureQuestionsFor(subjectId: string): Question[] {
  const b = getSubject(subjectId)!;
  const out: Question[] = [];
  for (const s of b.subtopics) {
    const items: [ConceptGroup, Difficulty, QuestionType][] = [...PATH[s.weight], ['C1', 'D2', 'mcq']];
    items.forEach(([cg, d, type], i) => {
      const isProbe = i === items.length - 1 || (cg === 'C2' && d === 'D2');
      const transfer = (cg === 'C3' && Number(d[1]) >= 4) || (cg === 'C4' && Number(d[1]) >= 3);
      out.push({
        id: `${s.id}-q9${String(i + 1).padStart(2, '0')}`, legacyId: 'fixture',
        subtopicId: s.id, chapterId: s.chapterId, subjectId, conceptGroup: cg, difficulty: d, type,
        stem: STEM[cg](s.name),
        ...(type === 'mcq' ? { options: ['The statement in option A', 'The statement in option B', 'The statement in option C', 'The statement in option D'] } : {}),
        answer: type === 'mcq' ? 'The statement in option B' : 'See marking key',
        markingKey: type === 'mcq' ? 'B. Fixture item: option B is correct.' : `Fixture item: award marks for a correct method and answer on ${s.name}.`,
        marks: cg === 'C4' ? 4 : cg === 'C3' ? 3 : cg === 'C2' ? 2 : 1,
        minutes: cg === 'C4' ? 5 : cg === 'C3' ? 3 : cg === 'C2' ? 2 : 1,
        alrRole: transfer ? 'transfer_probe' : isProbe ? 'retention_probe' : 'practised',
        likelyGapOnWrong: GAP_ON_WRONG[cg], set: 'mastery_bank',
      });
    });
  }
  return out;
}

export interface Bank {
  subjectId: string;
  source: 'bank' | 'fixture';
  questions: Question[];
  byId: Map<string, Question>;
  /** Student-check path of a subtopic (first N mastery-bank items by id, as components/assessment/catalog.ts). */
  path: (subtopicId: string) => Question[];
  probes: (chapterId: string) => Question[];
  baseline: (chapterId: string, perSubtopic: number) => Question[];
  formB: (chapterId: string) => Question[];
  mock: (n: number, chapterIds: string[]) => Question[];
}

const bankCache = new Map<string, Bank>();
export function bankStatus(subjectId: string): { validated: boolean; generated?: number } {
  const f = path.join(ROOT, 'data', 'questions', subjectId, '_status.json');
  try {
    const st = JSON.parse(fs.readFileSync(f, 'utf8'));
    return { validated: st.validated === true, generated: st.generated };
  } catch {
    return { validated: false };
  }
}

export function bankFor(subjectId: string): Bank {
  const hit = bankCache.get(subjectId);
  if (hit) return hit;
  const subj = getSubject(subjectId);
  if (!subj) throw new Error(`unknown subject ${subjectId}`);
  let questions: Question[];
  let source: Bank['source'];
  if (bankStatus(subjectId).validated) {
    const dir = path.join(ROOT, 'data', 'questions', subjectId);
    questions = fs.readdirSync(dir).filter((f) => f.endsWith('.json') && !f.startsWith('_')).sort()
      .flatMap((f) => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')).items as Question[]);
    source = 'bank';
  } else {
    questions = fixtureQuestionsFor(subjectId);
    source = 'fixture';
  }
  const byId = new Map(questions.map((q) => [q.id, q]));
  const mb = questions.filter((q) => q.set === 'mastery_bank').sort((a, b) => a.id.localeCompare(b.id));
  const bySub = new Map<string, Question[]>();
  for (const q of mb) bySub.set(q.subtopicId, [...(bySub.get(q.subtopicId) ?? []), q]);
  const weight = new Map(subj.subtopics.map((s) => [s.id, s.weight]));
  const pathOf = (sid: string) => (bySub.get(sid) ?? []).slice(0, PATH_LENGTH[weight.get(sid) ?? 'S']);
  const b: Bank = {
    subjectId, source, questions, byId,
    path: pathOf,
    probes: (chapterId) => {
      const subs = subj.subtopics.filter((s) => s.chapterId === chapterId);
      return subs.flatMap((s) => {
        const all = bySub.get(s.id) ?? [];
        const pr = all.filter((q) => q.alrRole === 'retention_probe');
        return (pr.length ? pr : all.filter((q) => q.conceptGroup === 'C1')).slice(-2);
      });
    },
    baseline: (chapterId, per) => {
      const subs = subj.subtopics.filter((s) => s.chapterId === chapterId);
      return subs.flatMap((s) => {
        const all = bySub.get(s.id) ?? [];
        const inPath = new Set(pathOf(s.id).map((q) => q.id));
        const pool = source === 'bank' ? all.filter((q) => !inPath.has(q.id)) : all.filter((q) => q.alrRole === 'practised');
        const pick = pool.filter((q) => (q.conceptGroup === 'C1' || q.conceptGroup === 'C3') && (q.difficulty === 'D2' || q.difficulty === 'D1'));
        return (pick.length >= per ? pick : [...pick, ...pool.filter((q) => !pick.includes(q))]).slice(0, per);
      });
    },
    formB: (chapterId) => questions.filter((q) => q.chapterId === chapterId && q.set === 'practice_form_b'),
    mock: (n, chapterIds) => {
      const real = questions.filter((q) => q.set === 'mock' && q.id.startsWith(`${subjectId}-mock${n}-`));
      if (real.length) return real;
      // no mock paper yet: a full-syllabus paper from the covered chapters' banks (C1-C3, one per subtopic)
      const covered = new Set(chapterIds);
      return subj.subtopics.filter((s) => covered.has(s.chapterId)).map((s, i) => (bySub.get(s.id) ?? [])[(n + i) % Math.max(1, Math.min(4, (bySub.get(s.id) ?? []).length))]).filter(Boolean) as Question[];
    },
  };
  bankCache.set(subjectId, b);
  return b;
}

/** Any question known to the simulator (all banks loaded so far). */
export function anyQuestion(id: string): Question | undefined {
  for (const b of bankCache.values()) {
    const q = b.byId.get(id);
    if (q) return q;
  }
  return undefined;
}
export function loadedBanks(): Bank[] {
  return [...bankCache.values()];
}

// ------------------------------------------------------------------ trait model

/** A number, or a piecewise-linear schedule [[date, value], ...] (flat before the first and after the last point). */
export type Sched = number | [string, number][];
export function at(s: Sched | undefined, date: string, dflt = 0): number {
  if (s === undefined) return dflt;
  if (typeof s === 'number') return s;
  if (date <= s[0][0]) return s[0][1];
  for (let i = 1; i < s.length; i++) {
    if (date <= s[i][0]) {
      const [d0, v0] = s[i - 1];
      const [d1, v1] = s[i];
      const t = (Date.parse(date) - Date.parse(d0)) / (Date.parse(d1) - Date.parse(d0));
      return v0 + (v1 - v0) * t;
    }
  }
  return s[s.length - 1][1];
}

export interface Traits {
  /** Mean true mastery of a taught subtopic (0..1). */
  base: number;
  spread: number;
  /** Slip on easy items (careless, G4). */
  slip: Sched;
  /** Probability of leaving an item blank (engagement, G10). */
  blank: Sched;
  /** Confidence bias: + over-confident (G9 when wrong answers are rated ≥ 4), − under-confident. */
  overconf: Sched;
  /** Weekly mastery gain on subtopics with an open gap (the plan working). */
  growth: Sched;
  /** Extra item demand by concept group (C2 = rote learner, G2; C4 = transfer/reasoning, G5). */
  cgPenalty?: Partial<Record<ConceptGroup, number>>;
  /** Extra item demand by question type (word-heavy types → G7 language). */
  typePenalty?: Partial<Record<QuestionType, number>>;
  /** True mastery of named subtopics (overrides base). */
  weak?: Record<string, number>;
  /** Time used vs allotted (> 1.2 with a wrong last item → G8 time pressure). */
  speed: number;
  /** Share of timetable blocks done. */
  doneRate: Sched;
  /** Mastery lost by the 7-day probe (forgetting; R < 0.7 → G6). */
  forget?: Sched;
  /** How much of a chapter is already known before it is taught (pre-test). */
  prior?: number;
  /** Calibration: 1 = confidence follows the real chance of being right; 0 = the same guess every time (low MCI). */
  calib?: Sched;
}

export interface SubjectSim {
  subjectId: string;
  depth: 'full' | 'light';
  /** Chapter checks taken so far (chapters 1..n in curriculum order). */
  chapters: number;
  /** Explicit chapter-check dates (Thursdays), else spread evenly over the history. */
  checkDates?: string[];
  /** Saturday weekly tests on open gaps (default: full subjects only). */
  weekly?: boolean;
  /** Per-subject trait overrides. */
  traits?: Partial<Traits>;
  /** Mocks taken: [date, mock number]. */
  mocks?: [string, number][];
}

export interface SimInput {
  student: Student;
  start: string; // first day of history (starting test)
  subjects: SubjectSim[];
  traits: Traits;
  profile: { paramId: string; value: unknown; asOfUtc: string }[];
  /** Last date a chapter check may fall on. */
  lastCheck?: string;
  /** Seed variant chosen by `simulate.ts --search` so the story holds (part of the persona definition). */
  seed?: string;
}

export interface SimOutput {
  attempts: Attempt[];
  gaps: GapRecord[];
  mastery: MasteryRecord[];
  alr: AlrRecord[];
  plans: PlanRecord[];
  timetable: TimetableWeek[];
  tasks: Task[];
  events: EvidenceEvent[];
  band: Student['band'];
  checks: { subjectId: string; chapterId: string; date: string }[];
}

function pCorrect(m: number, q: Question, t: Traits, date: string): number {
  const req = 0.12 + 0.11 * (Number(q.difficulty[1]) - 1) + 0.08 * (Number(q.conceptGroup[1]) - 1) + (t.cgPenalty?.[q.conceptGroup] ?? 0) + (t.typePenalty?.[q.type] ?? 0);
  const p = 1 / (1 + Math.exp(-9 * (m - req)));
  const slip = at(t.slip, date);
  return p * (1 - slip * (q.difficulty === 'D2' || q.difficulty === 'D1' ? 1 : 0.5));
}

// ------------------------------------------------------------------ the simulation

const THU_SLOT: Record<number, [number, string]> = { 0: [3, '17:30'], 1: [1, '17:30'], 2: [4, '17:30'], 3: [2, '17:30'] };

export function simulate(inp: SimInput): SimOutput {
  const s = inp.student;
  const R = rng(`${SEED}:${s.id}${inp.seed ? `:${inp.seed}` : ''}`);
  const pick = <T>(xs: T[]) => xs[Math.floor(R() * xs.length)];
  const subjTraits = (sim: SubjectSim): Traits => ({ ...inp.traits, ...(sim.traits ?? {}) });
  const banks = new Map(inp.subjects.map((x) => [x.subjectId, bankFor(x.subjectId)]));
  const getQ = (id: string) => {
    for (const b of banks.values()) { const q = b.byId.get(id); if (q) return q; }
    return undefined;
  };

  // true mastery per subtopic (after teaching), and what is known before the chapter is taught
  const truth = new Map<string, number>();
  const traitsOfSub = new Map<string, Traits>();
  for (const sim of inp.subjects) {
    const t = subjTraits(sim);
    for (const st of getSubject(sim.subjectId)!.subtopics) {
      truth.set(st.id, clamp(t.weak?.[st.id] ?? t.base + (R() - 0.5) * 2 * t.spread, -0.3, 0.98));
      traitsOfSub.set(st.id, t);
    }
  }
  const taught = new Set<string>(); // chapterIds taught so far

  // chapter-check schedule
  const lastCheck = inp.lastCheck ?? addDaysLocal(TODAY, -6);
  const checks: SimOutput['checks'] = [];
  inp.subjects.forEach((sim, k) => {
    const chs = getSubject(sim.subjectId)!.chapters.slice(0, sim.chapters);
    let dates = sim.checkDates;
    if (!dates) {
      const first = addDaysLocal(inp.start, 9);
      const span = (Date.parse(lastCheck) - Date.parse(first)) / 86_400_000;
      const [dow] = THU_SLOT[k % 4];
      // chapter i finishes at (i+1)/n of the way through the term, on the subject's weekday
      dates = chs.map((_, i) => {
        let d = addDaysLocal(weekStartOf(addDaysLocal(first, Math.round((span * (i + 1)) / chs.length))), dow);
        if (d > lastCheck) d = addDaysLocal(d, -7);
        return d;
      });
      for (let i = 1; i < dates.length; i++) if (dates[i] <= dates[i - 1]) dates[i] = addDaysLocal(dates[i - 1], 7);
    }
    chs.forEach((ch, i) => checks.push({ subjectId: sim.subjectId, chapterId: ch.id, date: dates![i] }));
  });

  const state: LearnerState = emptyState();
  const attempts: Attempt[] = [];
  const plans: PlanRecord[] = [];
  const events: EvidenceEvent[] = [];
  const timetable: TimetableWeek[] = [];
  const tasks: Task[] = [];
  let n = 0;

  const answer = (qs: Question[], date: string, kind: Attempt['kind'], forgetDays = 0): ItemResponse[] => {
    const out: ItemResponse[] = [];
    for (const q of qs) {
      const t = traitsOfSub.get(q.subtopicId) ?? inp.traits;
      if (R() < at(t.blank, date)) continue;
      let m = truth.get(q.subtopicId) ?? t.base;
      if (!taught.has(q.chapterId)) m = m - (1 - (t.prior ?? 0.55)) * 0.6; // not taught yet
      // forget = share of the chance of recalling an item lost per week since it was last checked
      const p = pCorrect(m, q, t, date) * (forgetDays ? 1 - at(t.forget, date, 0.04) * Math.min(2, forgetDays / 7) : 1);
      const correct = R() < p;
      const cal = at(t.calib, date, 1);
      const noise = R();
      const felt = clamp(cal * (p + (noise - 0.5) * 0.2) + (1 - cal) * noise + at(t.overconf, date), 0, 1);
      out.push({
        questionId: q.id, correct,
        secondsTaken: Math.round(q.minutes * 60 * t.speed * (0.7 + R() * 0.6)),
        confidence: clamp(Math.round(1 + felt * 4), 1, 5) as 1 | 2 | 3 | 4 | 5,
        ...(q.type === 'mcq' && q.options?.length ? { answer: correct ? q.answer : pick(q.options.filter((o) => o !== q.answer)) } : {}),
      });
    }
    void kind;
    return out;
  };
  const take = (kind: Attempt['kind'], title: string, subjectId: string, date: string, time: string, items: Question[], chapterId?: string, forgetDays = 0) => {
    if (!items.length) return undefined;
    n += 1;
    const responses = answer(items, date, kind, forgetDays);
    const ok = new Set(responses.filter((r) => r.correct).map((r) => r.questionId));
    const startedUtc = istUtc(date, time);
    const mins = items.reduce((a, q) => a + q.minutes, 0);
    const speed = (traitsOfSub.get(items[0].subtopicId) ?? inp.traits).speed;
    const a: Attempt = {
      id: `att_${s.id.slice(4)}_${String(n).padStart(3, '0')}`, learnerId: s.id, kind, title, subjectId, ...(chapterId ? { chapterId } : {}),
      questionIds: items.map((q) => q.id), responses, startedUtc,
      submittedUtc: new Date(Date.parse(startedUtc) + Math.round(mins * 60_000 * Math.min(speed, 1.2))).toISOString(),
      minutesAllotted: Math.round(mins), score: items.filter((q) => ok.has(q.id)).reduce((x, q) => x + q.marks, 0), maxScore: items.reduce((x, q) => x + q.marks, 0), status: 'submitted',
    };
    attempts.push(a);
    const eff = applyAttempt(s, a, state, attempts, getQ);
    events.push({
      eventId: `evt_${a.id}`, learnerId: s.id, timestampUtc: a.submittedUtc, sourceMethod: 'M14', type: 'assessment_submitted',
      payload: { attemptId: a.id, kind: a.kind, subjectId, score: a.score, maxScore: a.maxScore, gaps: eff.gaps.map((g) => `${g.code}:${g.subtopicId}`), parameterIds: ['p8', 'p20', 'p60'] },
    });
    return a;
  };
  const chapterName = (id: string) => getSubject(id.replace(/-ch\d+$/, ''))?.chapters.find((c) => c.id === id)?.name ?? id;

  // starting test: a short baseline across every simulated subject (before teaching)
  const baseItems = inp.subjects.flatMap((sim) => checks.filter((c) => c.subjectId === sim.subjectId).flatMap((c) => banks.get(sim.subjectId)!.baseline(c.chapterId, sim.depth === 'full' ? 2 : 1)));
  take('onboarding', 'Starting test', inp.subjects[0].subjectId, inp.start, '17:30', baseItems);

  const pendingProbes: { date: string; subjectId: string; chapterId: string }[] = [];
  const ws0 = weekStartOf(inp.start);
  const thisWeek = weekStartOf(TODAY);
  const fullSubjects = inp.subjects.filter((x) => x.weekly !== false).map((x) => x.subjectId);
  for (let ws = ws0, w = 0; ws <= thisWeek; ws = addDaysLocal(ws, 7), w++) {
    // learning: open gaps improve with the plan
    for (const g of state.gaps.values()) {
      if (g.status === 'closed') continue;
      const t = traitsOfSub.get(g.subtopicId) ?? inp.traits;
      truth.set(g.subtopicId, clamp(truth.get(g.subtopicId)! + at(t.growth, ws), -0.3, 0.98));
      if (g.status === 'suspected' || g.status === 'confirmed') state.gaps.set(g.subtopicId, { ...g, status: 'in_progress' });
    }
    // timetable for the week, from Monday's state
    const cur = checks.filter((c) => c.date >= ws).sort((a, b) => a.date.localeCompare(b.date))[0];
    const st: Student = { ...s, currentChapterIds: ws === thisWeek ? s.currentChapterIds : cur ? [cur.chapterId] : s.currentChapterIds };
    const tw = buildWeek(st, ws, { gaps: [...state.gaps.values()], mastery: [...state.mastery.values()], sessions: [], now: istUtc(ws, '00:05') }, w === 0 ? 'initial' : 'weekly');
    const weekNow = ws === thisWeek ? NOW : istUtc(addDaysLocal(ws, 7), '00:00');
    for (const b of tw.blocks) {
      if (b.kind === 'buffer') continue;
      if (b.endUtc <= weekNow) b.status = R() < at(inp.traits.doneRate, b.date) ? 'done' : 'missed';
    }
    tw.generatedUtc = istUtc(ws, '00:05');
    timetable.push(tw);
    for (const b of tw.blocks) {
      if (b.kind === 'buffer' || b.kind === 'session') continue;
      const kind: Task['kind'] = b.kind === 'gap' || b.kind === 'carry_over' ? 'practise' : b.kind === 'review' ? 'retrieve' : b.kind === 'weekly_test' ? 'test' : 'learn';
      tasks.push({
        id: `task_${b.id.slice(4)}`, learnerId: s.id, title: b.title, kind, dueDate: b.date, minutes: b.minutes, source: 'timetable', refId: b.refId ?? b.id,
        status: b.status === 'done' ? 'done' : b.status === 'missed' ? 'skipped' : 'todo', createdUtc: tw.generatedUtc,
        ...(b.status === 'done' ? { completedUtc: b.endUtc } : {}),
        ...(b.kind === 'weekly_test' ? { href: '/student/assessments' } : {}),
      });
    }

    // the week's tests, day by day (history ends yesterday)
    for (let d = 0; d < 7; d++) {
      const date = addDaysLocal(ws, d);
      if (date < inp.start || date >= TODAY) continue;
      for (const p of pendingProbes.filter((x) => x.date === date)) {
        take('retention_probe', `7-day review: ${chapterName(p.chapterId)}`, p.subjectId, date, '17:00', banks.get(p.subjectId)!.probes(p.chapterId), p.chapterId, 7);
      }
      for (const c of checks.filter((x) => x.date === date)) {
        taught.add(c.chapterId);
        const b = banks.get(c.subjectId)!;
        const subs = getSubject(c.subjectId)!.subtopics.filter((x) => x.chapterId === c.chapterId);
        take('chapter_check', `Chapter check: ${chapterName(c.chapterId)}`, c.subjectId, date, '17:30', subs.flatMap((x) => b.path(x.id)), c.chapterId);
        if (addDaysLocal(date, 7) < TODAY) pendingProbes.push({ date: addDaysLocal(date, 7), subjectId: c.subjectId, chapterId: c.chapterId });
      }
      for (const sim of inp.subjects) for (const [md, mn] of sim.mocks ?? []) {
        if (md !== date) continue;
        const covered = checks.filter((c) => c.subjectId === sim.subjectId && c.date < date).map((c) => c.chapterId);
        take('mock', `${getSubject(sim.subjectId)!.subject.name} · Mock ${mn}`, sim.subjectId, date, '09:30', banks.get(sim.subjectId)!.mock(mn, covered));
      }
      if (d === 5) {
        // Saturday weekly test: up to 6 open gaps per subject with their full paths; G6 (retention) gets a spaced review instead
        for (const sid of fullSubjects) {
          const open = [...state.gaps.values()].filter((g) => g.status !== 'closed' && g.subjectId === sid).sort((a, b) => b.size - a.size || a.subtopicId.localeCompare(b.subtopicId));
          const full = open.filter((g) => g.code !== 'G6').slice(0, 6);
          const probe = open.filter((g) => g.code === 'G6').slice(0, 4);
          const b = banks.get(sid)!;
          if (full.length) take('weekly', `Weekly test, week of ${ws}`, sid, date, '10:00', full.flatMap((g) => b.path(g.subtopicId)));
          if (probe.length) take('retention_probe', `Spaced review, week of ${ws}`, sid, date, '11:00', probe.flatMap((g) => b.probes(g.chapterId).filter((q) => q.subtopicId === g.subtopicId)), undefined, 7);
        }
        // plan after the week's tests
        const gapsNow = [...state.gaps.values()];
        if (gapsNow.some((g) => g.status !== 'closed')) {
          const prev = plans[plans.length - 1];
          if (prev) prev.status = 'replaced';
          const oldest = gapsNow.filter((g) => g.status !== 'closed' && g.size >= 2).map((g) => g.detectedUtc).sort()[0];
          const freeWeeks = oldest ? Math.floor((Date.parse(istUtc(date, '18:00')) - Date.parse(oldest)) / (7 * 86_400_000)) : 0;
          plans.push(planFor(s, gapsNow, istUtc(date, '18:00'), freeWeeks, inp.profile));
        } else if (plans.length && plans[plans.length - 1].status === 'active') {
          plans[plans.length - 1].status = 'succeeded';
        }
      }
    }
  }

  const alr = state.alr;
  return {
    attempts, plans, timetable, tasks, events, checks,
    gaps: [...state.gaps.values()], mastery: [...state.mastery.values()], alr,
    band: summariseAlr(alr).overall.band ?? s.band,
  };
}
