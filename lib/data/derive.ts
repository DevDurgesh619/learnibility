/**
 * The engine pipeline shared by the fixture builder (scripts/fixtures/build.ts) and recomputeLearner:
 * attempt → diagnoseGaps → gaps + mastery → ALR → intervention plan → timetable → next best action.
 * Pure apart from curriculum reads; never re-implements an engine rule.
 */
import {
  alrInputsFromResponses,
  buildTimetable,
  computeAlr,
  diagnoseGaps,
  nextBestAction,
  planInterventions,
  type Diagnosis,
  type FixedSession,
  type NextAction,
  type SubtopicLike,
  type Timetable,
  type TimetableInput,
} from '@/lib/engines';
import type { Question } from '@/lib/types';
import { getQuestion, getSubject, namesFor, subjectIdOf } from './catalogue';
import type { AlrRecord, AlrSummary, Application, Attempt, CareerMatches, GapRecord, LocalDate, MasteryRecord, PlanRecord, Session, Student, Task, TimetableWeek } from './types';

export const TZ_OFFSET = 330;

/** Local date (YYYY-MM-DD) of a UTC instant. */
export function localDateOf(iso: string, off = TZ_OFFSET): LocalDate {
  return new Date(Date.parse(iso) + off * 60_000).toISOString().slice(0, 10);
}

/** Monday of the week containing a local date. */
export function weekStartOf(date: LocalDate): LocalDate {
  const d = new Date(date + 'T00:00:00Z');
  const back = (d.getUTCDay() + 6) % 7;
  return new Date(d.getTime() - back * 86_400_000).toISOString().slice(0, 10);
}

export function addDaysLocal(date: LocalDate, days: number): LocalDate {
  return new Date(Date.parse(date + 'T00:00:00Z') + days * 86_400_000).toISOString().slice(0, 10);
}

function subtopicsFor(subjectIds: Iterable<string>): Record<string, SubtopicLike> {
  const out: Record<string, SubtopicLike> = {};
  for (const sid of new Set(subjectIds)) for (const s of getSubject(sid)?.subtopics ?? []) out[s.id] = s;
  return out;
}

export function weeklyHoursPerSubject(student: Student): number {
  const full = student.subjects.filter((s) => s.depth === 'full').length || 1;
  return Math.round((student.weeklyHours / full) * 10) / 10;
}

export interface LearnerState {
  gaps: Map<string, GapRecord>; // by subtopicId
  mastery: Map<string, MasteryRecord>; // by subtopicId
  alr: AlrRecord[];
}

export function emptyState(): LearnerState {
  return { gaps: new Map(), mastery: new Map(), alr: [] };
}

export function stateFrom(gaps: GapRecord[], mastery: MasteryRecord[], alr: AlrRecord[]): LearnerState {
  return { gaps: new Map(gaps.map((g) => [g.subtopicId, g])), mastery: new Map(mastery.map((m) => [m.subtopicId, m])), alr: [...alr] };
}

export interface AttemptEffect {
  diagnoses: Diagnosis[];
  gaps: GapRecord[]; // new or updated (closed ones included with status closed)
  mastery: MasteryRecord[];
  alr: AlrRecord[];
}

/**
 * Apply one submitted attempt to a learner state (mutates `state`, returns what changed).
 * `allAttempts` (time-ordered, including this one) supplies chapter-check and retention evidence for ALR.
 */
export function applyAttempt(student: Student, attempt: Attempt, state: LearnerState, allAttempts: Attempt[], questionsById?: (id: string) => Question | undefined): AttemptEffect {
  const getQ = questionsById ?? getQuestion;
  const questions = attempt.questionIds.map(getQ).filter((q): q is Question => !!q);
  const effect: AttemptEffect = { diagnoses: [], gaps: [], mastery: [], alr: [] };
  if (!questions.length || attempt.status !== 'submitted') return effect;
  const subs = subtopicsFor(questions.map((q) => q.subjectId));
  const known = questions.filter((q) => subs[q.subtopicId]);
  const diagnoses = diagnoseGaps(attempt.responses, known, {
    learnerId: student.id,
    band: student.band,
    subtopics: subs,
    weeklyHours: weeklyHoursPerSubject(student),
  });
  effect.diagnoses = diagnoses;
  const now = attempt.submittedUtc;
  for (const d of diagnoses) {
    if (d.flags.insufficientEvidence) continue;
    const subjectId = subjectIdOf(d.subtopicId);
    const m: MasteryRecord = {
      learnerId: student.id, subtopicId: d.subtopicId, chapterId: d.chapterId, subjectId,
      level: d.level, pMastery: Math.round(d.scorePct) / 100, lastTestedUtc: now,
      ...(state.mastery.get(d.subtopicId)?.retention !== undefined ? { retention: state.mastery.get(d.subtopicId)!.retention } : {}),
    };
    if (attempt.kind === 'retention_probe') m.retention = Math.round(d.scorePct) / 100;
    state.mastery.set(d.subtopicId, m);
    effect.mastery.push(m);

    const prev = state.gaps.get(d.subtopicId);
    if (d.gap) {
      const keepProgress = prev && prev.status === 'in_progress' && prev.code === d.gap.code;
      const g: GapRecord = {
        ...d.gap,
        status: keepProgress ? 'in_progress' : d.gap.status,
        chapterId: d.chapterId,
        subjectId,
        attemptId: attempt.id,
        detectedUtc: prev && prev.status !== 'closed' ? prev.detectedUtc : now,
        updatedUtc: now,
        band: student.band,
        weeks: d.weeksToClose,
        scorePct: d.scorePct,
        confirmingProbe: d.confirmingProbe,
        likelyCauses: d.likelyCauses,
        prerequisiteToProbe: d.prerequisiteToProbe,
        ...(prev?.validation && prev.code === d.gap.code ? { validation: prev.validation } : {}),
      };
      state.gaps.set(d.subtopicId, g);
      effect.gaps.push(g);
    } else if (prev && prev.status !== 'closed') {
      const g: GapRecord = { ...prev, status: 'closed', closedUtc: now, updatedUtc: now, level: d.level, scorePct: d.scorePct, hoursToClose: 0, attemptId: attempt.id };
      state.gaps.set(d.subtopicId, g);
      effect.gaps.push(g);
    }
  }

  // ALR for the chapter this attempt finishes (chapter checks, and retention probes re-score R).
  const chapterIds = attempt.chapterId ? [attempt.chapterId] : [];
  for (const chapterId of chapterIds) {
    if (!['chapter_check', 'retention_probe', 'practice_form', 'assigned'].includes(attempt.kind)) continue;
    const upto = allAttempts.filter((a) => a.submittedUtc <= attempt.submittedUtc && a.status === 'submitted');
    const posts = upto.filter((a) => a.chapterId === chapterId && a.kind !== 'retention_probe' && a.kind !== 'onboarding');
    const post = posts[posts.length - 1];
    if (!post) continue;
    const pre = upto.find((a) => a.kind === 'onboarding' || (a.chapterId === chapterId && a.kind === 'weekly'));
    const delayed = upto.filter((a) => a.chapterId === chapterId && a.kind === 'retention_probe').pop();
    const qIds = new Set([...post.questionIds, ...(pre?.questionIds ?? []), ...(delayed?.questionIds ?? [])]);
    const qs = [...qIds].map(getQ).filter((q): q is Question => !!q);
    const inputs = alrInputsFromResponses({
      learnerId: student.id,
      chapterId,
      questions: qs,
      pre: pre?.responses.filter((r) => getQ(r.questionId)?.chapterId === chapterId),
      post: post.responses,
      delayed: delayed?.responses,
      minutesAllotted: post.minutesAllotted,
    });
    const res = computeAlr(inputs);
    if (!res.snapshot) continue;
    const rec: AlrRecord = { ...res.snapshot, subjectId: subjectIdOf(chapterId), asOfUtc: now, missing: res.missing, action: res.action };
    state.alr.push(rec);
    effect.alr.push(rec);
  }
  return effect;
}

/** Year-to-date ALR summary from all snapshots. */
export function summariseAlr(history: AlrRecord[]): AlrSummary {
  const sorted = [...history].sort((a, b) => a.asOfUtc.localeCompare(b.asOfUtc));
  const latest = new Map<string, AlrRecord>();
  for (const r of sorted) latest.set(r.chapterId, r);
  const chapters = [...latest.values()];
  const mean = (k: 'dK' | 'R' | 'TQ' | 'CE' | 'ECV' | 'MCI' | 'LRS') => {
    const xs = chapters.map((c) => c[k]).filter((x) => typeof x === 'number' && !Number.isNaN(x));
    return xs.length ? Math.round((xs.reduce((a, b) => a + b, 0) / xs.length) * 100) / 100 : null;
  };
  const LRS = mean('LRS');
  const band = LRS === null ? null : LRS >= 0.8 ? 'excellent' : LRS >= 0.65 ? 'above_avg' : LRS >= 0.5 ? 'average' : 'below_avg';
  return { chapters, history: sorted, overall: { dK: mean('dK'), R: mean('R'), TQ: mean('TQ'), CE: mean('CE'), ECV: mean('ECV'), MCI: mean('MCI'), LRS, band } };
}

/** New intervention plan from the open gaps. */
export function planFor(student: Student, gaps: GapRecord[], now: string, freePlanWeeks: number, profile?: Parameters<typeof planInterventions>[1]): PlanRecord {
  const open = gaps.filter((g) => g.status !== 'closed');
  const plan = planInterventions(open, profile, { now, weeklyHours: weeklyHoursPerSubject(student), freePlanWeeks });
  return {
    id: `plan_${student.id}_${now.slice(0, 16).replace(/[-:T]/g, '')}`,
    learnerId: student.id,
    createdUtc: now,
    status: 'active',
    freePlanWeeks,
    gapIds: open.map((g) => g.id),
    plan,
    ...(plan.paidTuition.recommended ? { paidTrigger: 'any1_rule' as const } : {}),
  };
}

const hhmm = (iso: string, off = TZ_OFFSET) => new Date(Date.parse(iso) + off * 60_000).toISOString().slice(11, 16);

export function fixedSessions(sessions: Session[], weekStart: LocalDate): FixedSession[] {
  const end = addDaysLocal(weekStart, 7);
  return sessions
    .filter((s) => s.status === 'scheduled' || s.status === 'completed')
    .map((s) => ({ s, date: localDateOf(s.startUtc) }))
    .filter(({ date }) => date >= weekStart && date < end)
    .map(({ s, date }) => ({ id: s.id, title: s.title, date, start: hhmm(s.startUtc), end: hhmm(new Date(Date.parse(s.startUtc) + s.minutes * 60_000).toISOString()) }));
}

export interface TimetableContext {
  gaps: GapRecord[];
  mastery: MasteryRecord[];
  sessions: Session[];
  now: string;
}

export function timetableInput(student: Student, weekStart: LocalDate, ctx: TimetableContext): TimetableInput {
  const subjectIds = student.subjects.map((s) => s.subjectId);
  const names = namesFor(subjectIds);
  const open = ctx.gaps.filter((g) => g.status !== 'closed');
  const chapterId = student.currentChapterIds?.[0];
  return {
    learnerId: student.id,
    weekStart,
    now: ctx.now,
    tzOffsetMinutes: student.tzOffsetMinutes ?? TZ_OFFSET,
    availability: student.availability,
    sessions: fixedSessions(ctx.sessions, weekStart),
    masteryStates: ctx.mastery.map((m) => ({ subtopicId: m.subtopicId, lastTestedUtc: m.lastTestedUtc, level: m.level })),
    gaps: open.map((g) => ({ id: g.id, subtopicId: g.subtopicId, code: g.code, hoursToClose: g.hoursToClose, status: g.status, title: names[g.subtopicId], weeks: g.weeks })),
    ...(chapterId ? { currentChapter: { chapterId, title: names[chapterId] ?? chapterId, hoursThisWeek: 2 } } : {}),
    weeklyTest: { minutes: 30, day: 'sat', title: 'Weekly test' },
    names,
  };
}

export function buildWeek(student: Student, weekStart: LocalDate, ctx: TimetableContext, reason = 'initial'): TimetableWeek {
  const t: Timetable = buildTimetable(timetableInput(student, weekStart, ctx));
  return { ...t, generatedUtc: ctx.now, reason };
}

export interface NbaContext {
  now: string;
  gaps: GapRecord[];
  mastery: MasteryRecord[];
  attempts: Attempt[];
  tasks: Task[];
  applications: Application[];
  careers?: CareerMatches;
}

/** Next best actions from the learner's current state (computed on every read). */
export function nbaFor(student: Student, c: NbaContext, limit = 5): NextAction[] {
  const off = student.tzOffsetMinutes ?? TZ_OFFSET;
  const today = localDateOf(c.now, off);
  const names = namesFor(student.subjects.map((s) => s.subjectId));
  const ws = weekStartOf(today);
  const saturday = addDaysLocal(ws, 5);
  const deadlines = [
    ...c.applications
      .filter((a) => a.status !== 'submitted' && a.status !== 'decision')
      .map((a) => ({ id: a.id, title: `Application due: ${a.universityId.replace(/^uni-\w\w-/, '').toUpperCase()}`, dueUtc: `${a.deadline}T12:00:00.000Z`, href: `/student/applications/${a.id}` })),
    ...c.tasks
      .filter((t) => t.status === 'todo' && (t.kind === 'test' || t.kind === 'homework' || t.kind === 'application') && t.dueDate <= addDaysLocal(today, 3))
      .map((t) => ({ id: t.id, title: t.title, dueUtc: `${t.dueDate}T12:00:00.000Z`, href: t.href })),
  ];
  const reviewsDue = c.mastery
    .filter((m) => m.level >= 4)
    .map((m) => ({ id: `rev_${m.subtopicId}`, title: `Quick review: ${names[m.subtopicId] ?? m.subtopicId}`, dueUtc: new Date(Date.parse(m.lastTestedUtc) + 7 * 86_400_000).toISOString() }))
    .filter((r) => localDateOf(r.dueUtc, off) <= today);
  const takenThisWeek = c.attempts.some((a) => a.kind === 'weekly' && localDateOf(a.submittedUtc, off) >= ws);
  return nextBestAction(
    {
      learnerId: student.id,
      now: c.now,
      tzOffsetMinutes: off,
      grade: student.grade,
      deadlines,
      reviewsDue,
      weeklyTest: { dueUtc: `${saturday}T04:30:00.000Z`, taken: takenThisWeek, href: '/student/assessments' },
      gaps: c.gaps.filter((g) => g.status !== 'closed').map((g) => ({ id: g.id, subtopicId: g.subtopicId, code: g.code, hoursToClose: g.hoursToClose, status: g.status, title: `Fix ${names[g.subtopicId] ?? g.subtopicId}` })),
      profileCompletionPct: student.profileCompletionPct,
      careersShortlisted: c.careers?.shortlist.length ?? 0,
    },
    limit,
  );
}
