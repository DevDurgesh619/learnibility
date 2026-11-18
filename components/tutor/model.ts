import 'server-only';
import { addDaysLocal, demoNow, demoToday, getAttempts, getGaps, getMastery, getQuestion, getTasks, getTutorWorkspace, localDateOf, namesFor } from '@/lib/data';
import type { Assignment, Attempt, Booking, GapRecord, LocalDate, MasteryRecord, Session, Task, TutorWorkspace } from '@/lib/data/types';

/**
 * View models for the tutor app (HTML wireframes 2a to 8e), derived from getTutorWorkspace and the learner reads.
 * Every number on a tutor screen comes from here, so Home, Students, Today and Earnings agree.
 */

export type WsStudent = TutorWorkspace['students'][number];

export interface StudentIssue { kind: 'drop' | 'overdue' | 'inactive' | 'plateau' | 'review'; label: string; action: 'Review' | 'View' | 'Contact'; href: string }

export interface StudentRow extends WsStudent {
  status: 'new' | 'active' | 'inactive';
  nextSession?: Session;
  lastSession?: Session;
  pendingDemo?: Booking;
  sessionsDone: number;
  attendancePct: number | null;
  /** Mean score of the last 3 scored attempts or assignments in the tutor's subjects (0-100). */
  avgScorePct: number | null;
  /** Change between the latest 2 and the previous 2 scores, in points. */
  progressDelta: number | null;
  overdueTasks: Task[];
  pendingReview: Assignment[];
  issue?: StudentIssue;
  daysInactive: number;
}

const DAY = 86_400_000;
const now = () => demoNow();
const isTutorSubject = (ws: TutorWorkspace, subjectId: string) => {
  const slug = subjectId.split('-').slice(2).join('-');
  return ws.tutor.subjects.some((s) => s.subjectSlug === slug);
};

export function loadWorkspace(tutorId: string) {
  return getTutorWorkspace(tutorId);
}

export function sessionsFor(ws: TutorWorkspace, learnerId: string) {
  return ws.sessions.filter((s) => (s.learnerIds ?? [s.learnerId]).includes(learnerId));
}

/** Past sessions still marked scheduled have happened but have no report yet. */
export function reportMissing(s: Session, at = now()) {
  return s.status !== 'cancelled' && s.status !== 'no_show' && !s.report && Date.parse(s.startUtc) + s.minutes * 60_000 <= Date.parse(at);
}
export const isUpcoming = (s: Session, at = now()) => s.status === 'scheduled' && Date.parse(s.startUtc) + s.minutes * 60_000 > Date.parse(at);

/** Scored items in the tutor's subjects, oldest first, as percentages. */
export function scoreSeries(ws: TutorWorkspace, learnerId: string): { title: string; date: string; pct: number; source: 'platform' | 'assignment'; id: string; subjectId?: string; chapterId?: string }[] {
  const atts = getAttempts(learnerId)
    .filter((a) => a.maxScore > 0 && isTutorSubject(ws, a.subjectId))
    .map((a) => ({ id: a.id, title: a.title, date: a.submittedUtc, pct: Math.round((a.score / a.maxScore) * 100), source: (a.assignedBy === ws.tutor.id ? 'assignment' : 'platform') as 'platform' | 'assignment', subjectId: a.subjectId, chapterId: a.chapterId }));
  const asg = ws.assignments
    .filter((a) => a.learnerId === learnerId && a.score !== undefined && a.maxScore && !atts.some((x) => x.id === a.id))
    .map((a) => ({ id: a.id, title: a.title, date: `${a.dueOn}T12:00:00.000Z`, pct: Math.round(((a.score ?? 0) / (a.maxScore ?? 1)) * 100), source: 'assignment' as const }));
  return [...atts, ...asg].sort((a, b) => a.date.localeCompare(b.date));
}

export function studentRows(ws: TutorWorkspace): StudentRow[] {
  const today = demoToday();
  return ws.students.map((st) => {
    const ss = sessionsFor(ws, st.learnerId);
    const upcoming = ss.filter((s) => isUpcoming(s));
    const past = ss.filter((s) => Date.parse(s.startUtc) <= Date.parse(now()) && s.status !== 'cancelled');
    const done = past.filter((s) => s.status === 'completed' || s.report);
    const missed = past.filter((s) => s.status === 'no_show');
    const pendingDemo = ws.bookings.find((b) => b.learnerId === st.learnerId && b.status === 'requested');
    const scores = scoreSeries(ws, st.learnerId);
    const last3 = scores.slice(-3);
    const avg = last3.length ? Math.round(last3.reduce((s, x) => s + x.pct, 0) / last3.length) : null;
    const a = scores.slice(-2), b = scores.slice(-4, -2);
    const delta = a.length === 2 && b.length === 2 ? Math.round((a[0]!.pct + a[1]!.pct) / 2 - (b[0]!.pct + b[1]!.pct) / 2) : scores.length >= 2 ? scores.at(-1)!.pct - scores.at(-2)!.pct : null;
    const tasks = getTasks(st.learnerId, undefined, { createdBy: ws.tutor.id });
    const overdue = tasks.filter((t) => t.status === 'todo' && t.dueDate < today);
    const pendingReview = ws.assignments.filter((x) => x.learnerId === st.learnerId && (x.status === 'submitted' || x.status === 'ai_evaluated'));
    const daysInactive = Math.max(0, Math.floor((Date.parse(now()) - Date.parse(st.lastActivityUtc)) / DAY));
    const status: StudentRow['status'] = done.length === 0 ? 'new' : daysInactive >= 5 ? 'inactive' : 'active';
    const subj = st.subjectIds[0] ? namesFor([st.subjectIds[0]])[st.subjectIds[0]] : undefined;
    const href = `/tutor/students/${st.learnerId}`;
    let issue: StudentIssue | undefined;
    if (status === 'inactive' && daysInactive >= 7) issue = { kind: 'inactive', label: `No activity for ${daysInactive} days`, action: 'Contact', href: `${href}/messages` };
    else if (delta !== null && delta <= -8) issue = { kind: 'drop', label: `${subj ?? 'Score'} ↓ ${Math.abs(delta)}%`, action: 'Review', href: `${href}/learning` };
    else if (overdue.length >= 2) issue = { kind: 'overdue', label: `${overdue.length} tasks overdue`, action: 'View', href: `${href}/tasks` };
    else if (status === 'inactive') issue = { kind: 'inactive', label: `No activity for ${daysInactive} days`, action: 'Contact', href: `${href}/messages` };
    else if (scores.length >= 4 && delta !== null && Math.abs(delta) <= 2) issue = { kind: 'plateau', label: 'Improvement has plateaued', action: 'Review', href: `${href}/learning` };
    return {
      ...st, status, nextSession: upcoming[0], lastSession: past.at(-1), pendingDemo, sessionsDone: done.length,
      attendancePct: past.length ? Math.round(((past.length - missed.length) / past.length) * 100) : null,
      avgScorePct: avg, progressDelta: delta, overdueTasks: overdue, pendingReview, issue, daysInactive,
    };
  }).sort((x, y) => (x.nextSession?.startUtc ?? '9').localeCompare(y.nextSession?.startUtc ?? '9') || x.name.localeCompare(y.name));
}

export function needsAttention(rows: StudentRow[]) {
  return rows.filter((r) => r.issue);
}

/** Assignments with answers waiting for the tutor (review queue). */
export function reviewQueue(ws: TutorWorkspace) {
  return ws.assignments.filter((a) => a.status === 'submitted' || a.status === 'ai_evaluated').map((a) => ({
    a, waiting: (a.perQuestion ?? []).filter((q) => q.needsReview && q.tutorScore === undefined).length,
  }));
}

export function requests(ws: TutorWorkspace) {
  // Newest first, so a request made during the demo is the first thing the tutor sees.
  return ws.bookings.filter((b) => b.status === 'requested').sort((a, b) => b.requestedAt.localeCompare(a.requestedAt));
}

export function sessionsOn(ws: TutorWorkspace, date: LocalDate) {
  return ws.sessions.filter((s) => s.status !== 'cancelled' && localDateOf(s.startUtc) === date).sort((a, b) => a.startUtc.localeCompare(b.startUtc));
}

export function nameOf(ws: TutorWorkspace, learnerId: string) {
  return ws.students.find((s) => s.learnerId === learnerId)?.name ?? learnerId;
}
export const firstName = (n: string) => n.split(' ')[0] ?? n;
export function sessionWho(ws: TutorWorkspace, s: Session) {
  const ids = s.learnerIds?.length ? s.learnerIds : [s.learnerId];
  const first = firstName(nameOf(ws, ids[0]!));
  return ids.length > 1 ? `${first} + ${ids.length - 1}` : first;
}

// ------------------------------------------------------------------ Today (6a)

export interface TodayItem {
  id: string;
  at?: string; // ISO; untimed when absent
  kind: 'prep' | 'session' | 'report' | 'review' | 'request' | 'nudge';
  title: string;
  detail: string;
  href: string;
  cta: string;
  done: boolean;
}

/** 6a: the day's checklist. For another day only that day's sessions (prep, session, report) are listed. */
export function todayItems(ws: TutorWorkspace, day: LocalDate = demoToday()): TodayItem[] {
  const today = demoToday();
  const items: TodayItem[] = [];
  for (const s of sessionsOn(ws, day).filter((x) => x.status !== 'cancelled')) {
    const who = sessionWho(ws, s);
    const prepAt = new Date(Date.parse(s.startUtc) - 30 * 60_000).toISOString();
    items.push({ id: `prep-${s.id}`, at: prepAt, kind: 'prep', title: `Prepare ${who}'s ${s.kind === 'demo' ? 'demo' : 'session'}`, detail: `AI focus: ${aiFocus(ws, s).line}`, href: `/tutor/sessions/${s.id}/prep`, cta: 'Open prep', done: !!s.prepNotes || !!s.report });
    items.push({ id: `ses-${s.id}`, at: s.startUtc, kind: 'session', title: `${who} · ${s.title}`, detail: `${s.minutes} min · ${s.kind === 'group' ? 'group' : s.kind === 'demo' ? 'demo' : '1:1'}`, href: `/tutor/sessions/${s.id}/live`, cta: 'Join', done: !!s.report || s.status !== 'scheduled' || !isUpcoming(s) });
    if (s.kind !== 'demo') items.push({ id: `rep-${s.id}`, at: new Date(Date.parse(s.startUtc) + s.minutes * 60_000).toISOString(), kind: 'report', title: `Report for ${who}`, detail: '2 min after the session', href: `/tutor/sessions/${s.id}/report`, cta: 'Write report', done: !!s.report });
  }
  if (day !== today) return items.sort((a, b) => (a.at ?? 'z').localeCompare(b.at ?? 'z'));
  for (const s of ws.sessions.filter((x) => reportMissing(x) && localDateOf(x.startUtc) < today && x.kind !== 'demo')) {
    items.push({ id: `rep-${s.id}`, kind: 'report', title: `Report missing · ${sessionWho(ws, s)} ${s.code ?? ''}`.trim(), detail: 'Earnings are held until it is filed', href: `/tutor/sessions/${s.id}/report`, cta: 'Write report', done: false });
  }
  for (const { a, waiting } of reviewQueue(ws)) {
    items.push({ id: `rev-${a.id}`, kind: 'review', title: `Review ${firstName(nameOf(ws, a.learnerId))} · ${a.title}`, detail: waiting ? `${waiting} ${waiting === 1 ? 'answer' : 'answers'} waiting` : 'Ready to publish', href: `/tutor/students/${a.learnerId}/assignments/${a.id}`, cta: 'Evaluate', done: false });
  }
  for (const b of requests(ws)) {
    const hoursLeft = Math.max(0, 24 - Math.round((Date.parse(now()) - Date.parse(b.requestedAt)) / 3_600_000));
    items.push({ id: `req-${b.id}`, kind: 'request', title: `Reply to ${firstName(nameOf(ws, b.learnerId))}'s demo request`, detail: `${hoursLeft} h left to keep your response badge`, href: `/tutor/requests/${b.id}`, cta: 'Open', done: false });
  }
  for (const r of studentRows(ws).filter((x) => x.issue?.kind === 'inactive')) {
    items.push({ id: `nudge-${r.learnerId}`, kind: 'nudge', title: `Nudge ${firstName(r.name)}`, detail: `No activity for ${r.daysInactive} days`, href: `/tutor/students/${r.learnerId}/messages`, cta: 'Message', done: false });
  }
  return items.sort((a, b) => (a.at ?? 'z').localeCompare(b.at ?? 'z'));
}

// ------------------------------------------------------------------ earnings (7a-7c)

export interface EarningRow { session: Session; who: string; grossInr: number; netInr: number; status: 'paid' | 'pending' | 'report_missing' | 'free'; paidOn?: string }

export function earningRows(ws: TutorWorkspace): EarningRow[] {
  const fee = ws.tutor.platformFeeRate ?? 0.15;
  const paid = new Map<string, string>();
  for (const p of ws.payouts) for (const id of p.sessionIds) paid.set(id, p.paidOn);
  return ws.sessions
    .filter((s) => Date.parse(s.startUtc) <= Date.parse(now()) && s.status !== 'cancelled' && s.status !== 'no_show')
    .map((s) => {
      const n = s.learnerIds?.length || 1;
      const gross = Math.round(((s.rateInr ?? 0) * s.minutes) / 60) * (s.kind === 'group' ? n : 1);
      const net = gross - Math.round(gross * fee);
      const status: EarningRow['status'] = gross === 0 ? 'free' : paid.has(s.id) ? 'paid' : s.report ? 'pending' : 'report_missing';
      return { session: s, who: sessionWho(ws, s), grossInr: gross, netInr: net, status, paidOn: paid.get(s.id) };
    })
    .sort((a, b) => b.session.startUtc.localeCompare(a.session.startUtc));
}

export function nextPayoutDate(today = demoToday()): LocalDate {
  const d = new Date(`${today}T00:00:00Z`).getUTCDay();
  return addDaysLocal(today, ((8 - d) % 7) || 7);
}

// ------------------------------------------------------------------ one student (4a-4o)

export interface TopicCard { chapterId: string; name: string; state: 'strong' | 'medium' | 'weak' | 'not_started'; pct: number | null; delta: number | null }

/** Topic mastery per chapter for one subject (4b): mean pMastery of tested subtopics, change over 30 days from attempts. */
export function topicCards(learnerId: string, subjectId: string): TopicCard[] {
  const names = namesFor([subjectId]);
  const mastery = getMastery(learnerId, subjectId);
  const chapters = [...new Set(Object.keys(names).filter((k) => /-ch\d+$/.test(k) && k.startsWith(subjectId)))].sort();
  const attempts = getAttempts(learnerId, { subjectId });
  const cutoff = new Date(Date.parse(now()) - 30 * DAY).toISOString();
  return chapters.map((chapterId) => {
    const ms = mastery.filter((m: MasteryRecord) => m.chapterId === chapterId);
    const pct = ms.length ? Math.round((ms.reduce((s, m) => s + m.pMastery, 0) / ms.length) * 100) : null;
    const chAtt = attempts.filter((a: Attempt) => a.chapterId === chapterId && a.maxScore > 0);
    const recent = chAtt.filter((a) => a.submittedUtc >= cutoff), older = chAtt.filter((a) => a.submittedUtc < cutoff);
    const mean = (xs: Attempt[]) => xs.reduce((s, a) => s + a.score / a.maxScore, 0) / xs.length;
    const delta = recent.length && older.length ? Math.round((mean(recent) - mean(older)) * 100) : null;
    const state: TopicCard['state'] = pct === null ? 'not_started' : pct >= 80 ? 'strong' : pct >= 55 ? 'medium' : 'weak';
    return { chapterId, name: names[chapterId] ?? chapterId, state, pct, delta };
  });
}

export function openGapsFor(learnerId: string, subjectIds: string[]): GapRecord[] {
  return getGaps(learnerId, { status: 'open' }).filter((g) => !subjectIds.length || subjectIds.includes(g.subjectId));
}

// ------------------------------------------------------------------ AI focus (pre-written rules, no live model)

const GAP_FOCUS: Record<string, string> = {
  G1: 'rebuild the prerequisite first', G2: 'the idea behind the method, not more drills', G3: 'step-by-step method practice',
  G4: 'slow down and check each step', G5: 'apply it to unfamiliar problems', G6: 'spaced recall of what slipped',
  G7: 'reading the question carefully', G8: 'timed practice', G9: 'checking confidence against answers', G10: 'short wins to rebuild momentum',
};

/** One line the tutor sees before a session: last report's next focus, else the biggest open gap, else the booking topic. */
export function aiFocus(ws: TutorWorkspace, s: Session): { line: string; source: string } {
  const lid = s.learnerIds?.[0] ?? s.learnerId;
  const prev = sessionsFor(ws, lid).filter((x) => x.report && x.startUtc < s.startUtc).at(-1);
  if (prev?.report?.nextFocus) return { line: prev.report.nextFocus, source: `set after ${prev.code ?? 'the last session'}` };
  const subj = s.subjectId ? [s.subjectId] : [];
  const g = openGapsFor(lid, subj).sort((a, b) => b.hoursToClose - a.hoursToClose)[0];
  if (g) {
    const name = namesFor([g.subjectId])[g.subtopicId] ?? g.subtopicId;
    return { line: `${name}: ${GAP_FOCUS[g.code] ?? 'close the gap'}`, source: `open ${g.code} gap, ${g.hoursToClose} h to close` };
  }
  const b = ws.bookings.find((x) => x.id === s.bookingId);
  if (b?.sharedGapSnapshot?.gaps[0]) return { line: `${b.sharedGapSnapshot.gaps[0].name}: ${GAP_FOCUS[b.sharedGapSnapshot.gaps[0].code] ?? ''}`, source: 'from the shared gap snapshot' };
  return { line: b?.topic ?? s.focus ?? 'Get to know the student and agree goals', source: b?.topic ? "student's topic" : 'first session' };
}

/** Suggested 60-minute plan (5c), built from the focus, last homework and open gaps. */
export function sessionPlan(ws: TutorWorkspace, s: Session): { minutes: number; kind: 'Review' | 'Teach' | 'Practice' | 'Check'; text: string }[] {
  const focus = aiFocus(ws, s).line.split(':')[0]!;
  const lid = s.learnerIds?.[0] ?? s.learnerId;
  const prev = sessionsFor(ws, lid).filter((x) => x.report && x.startUtc < s.startUtc).at(-1);
  const scale = s.minutes / 60;
  const m = (x: number) => Math.max(5, Math.round((x * scale) / 5) * 5);
  if (s.kind === 'demo') return [
    { minutes: m(10), kind: 'Review', text: 'Hear what they want; look at the shared snapshot together' },
    { minutes: m(30), kind: 'Teach', text: `Try one short explanation on ${focus}` },
    { minutes: m(10), kind: 'Practice', text: 'One problem they solve aloud' },
    { minutes: m(10), kind: 'Check', text: 'Agree a weekly plan and price' },
  ];
  return [
    { minutes: m(5), kind: 'Review', text: prev ? `Homework from ${prev.code ?? 'last session'}: ${prev.report!.topics[0] ?? 'last topic'}` : 'Warm-up question from the last topic' },
    { minutes: m(20), kind: 'Teach', text: focus },
    { minutes: m(25), kind: 'Practice', text: `3 problems on ${focus.toLowerCase()}, rising difficulty` },
    { minutes: m(10), kind: 'Check', text: 'Exit question, then set homework' },
  ];
}

export function money(n: number) {
  return '₹' + Math.round(n).toLocaleString('en-IN');
}

/** The tutor's view of one of their students; undefined when the learner is not theirs. */
export function studentContext(tutorId: string, learnerId: string) {
  const ws = getTutorWorkspace(tutorId);
  if (!ws) return undefined;
  const row = studentRows(ws).find((r) => r.learnerId === learnerId);
  if (!row) return undefined;
  return { ws, row };
}

// ------------------------------------------------------------------ assignment questions (tutor-authored or bank)

/** A question as the tutor sees it. Tutor-made questions live on the assignment (`questions`); bank ones resolve by id. */
export interface TutorQuestion { id: string; type: string; subtopicId: string; stem: string; options?: string[] | null; answer: string; markingKey?: string; marks: number }
export type TutorAssignment = Assignment & {
  questions?: TutorQuestion[]; feedback?: { strength: string; weakness: string; nextStep: string };
  submittedUtc?: string; minutesTaken?: number; source?: 'ai' | 'bank' | 'upload'; evaluation?: 'ai_review' | 'manual'; timeLimitMin?: number; publishedUtc?: string;
};

export function questionsOf(a: TutorAssignment): TutorQuestion[] {
  if (a.questions?.length) return a.questions;
  return a.questionIds.map((id) => getQuestion(id)).filter((q) => !!q).map((q) => ({ id: q!.id, type: q!.type, subtopicId: q!.subtopicId, stem: q!.stem, options: q!.options, answer: String(q!.answer), markingKey: q!.markingKey, marks: q!.marks }));
}

export interface ItemReview {
  id: string; title: string; date: string; minutes?: number; pct: number; prevPct: number | null; kind: 'assignment' | 'attempt';
  rows: { subtopicId: string; name: string; n: number; pct: number; band: 'Strong' | 'Medium' | 'Weak' }[];
  questions: { n: number; q?: TutorQuestion; correct?: boolean; answer?: string; why?: string; seconds?: number; needsReview?: boolean; score?: number }[];
  strength: string; weakness: string; nextStep: string; weakest?: string;
}

/** 4d/4e: gap analysis of one assessment or assignment, per subtopic and per question. */
export function itemReview(ws: TutorWorkspace, learnerId: string, itemId: string): ItemReview | undefined {
  const series = scoreSeries(ws, learnerId);
  const idx = series.findIndex((s) => s.id === itemId);
  const prevPct = idx > 0 ? series[idx - 1]!.pct : null;
  const a = ws.assignments.find((x) => x.id === itemId && x.learnerId === learnerId) as TutorAssignment | undefined;
  let questions: ItemReview['questions'] = [];
  let title = '', date = '', minutes: number | undefined, pct = 0, subjectIds: string[] = [];
  if (a) {
    const qs = questionsOf(a);
    const pq = new Map((a.perQuestion ?? []).map((p) => [p.questionId, p]));
    questions = qs.map((q, i) => { const p = pq.get(q.id); return { n: i + 1, q, correct: p?.correct ?? undefined, answer: p?.answer, why: p?.aiFeedback, needsReview: p?.needsReview, score: p?.tutorScore ?? p?.aiScore }; });
    title = a.title; date = a.submittedUtc ?? `${a.dueOn}T12:00:00.000Z`; minutes = a.minutesTaken;
    pct = a.score !== undefined && a.maxScore ? Math.round((a.score / a.maxScore) * 100) : 0;
    subjectIds = [...new Set(a.subtopicIds.map((s) => s.replace(/-ch\d+-st\d+$/, '')))];
  } else {
    const at = getAttempts(learnerId).find((x) => x.id === itemId);
    if (!at) return undefined;
    title = at.title; date = at.submittedUtc; minutes = Math.round((Date.parse(at.submittedUtc) - Date.parse(at.startedUtc)) / 60_000); pct = Math.round((at.score / Math.max(1, at.maxScore)) * 100);
    subjectIds = [at.subjectId];
    const byId = new Map(at.responses.map((r) => [r.questionId, r]));
    questions = at.questionIds.map((id, i) => {
      const q = getQuestion(id); const r = byId.get(id);
      return { n: i + 1, q: q ? { id, type: q.type, subtopicId: q.subtopicId, stem: q.stem, options: q.options, answer: String(q.answer), markingKey: q.markingKey, marks: q.marks } : undefined, correct: r?.correct, answer: r?.answer, seconds: r?.secondsTaken, why: r && !r.correct && q?.likelyGapOnWrong ? `Likely ${q.likelyGapOnWrong} gap: ${q.markingKey}` : undefined };
    });
  }
  const names = namesFor(subjectIds);
  const groups = new Map<string, { n: number; ok: number }>();
  for (const x of questions) {
    if (!x.q) continue;
    const g = groups.get(x.q.subtopicId) ?? { n: 0, ok: 0 };
    g.n += 1; g.ok += x.correct ? 1 : x.correct === undefined && x.score !== undefined ? x.score / Math.max(1, x.q.marks) : 0;
    groups.set(x.q.subtopicId, g);
  }
  const rows = [...groups.entries()].map(([sid, g]) => {
    const p = Math.round((g.ok / g.n) * 100);
    return { subtopicId: sid, name: (names[sid] ?? sid).split(/[;:]/)[0]!, n: g.n, pct: p, band: (p >= 80 ? 'Strong' : p >= 55 ? 'Medium' : 'Weak') as 'Strong' | 'Medium' | 'Weak' };
  }).sort((x, y) => y.pct - x.pct);
  const best = rows[0], worst = rows.at(-1);
  return {
    id: itemId, title, date, minutes, pct, prevPct, kind: a ? 'assignment' : 'attempt', rows, questions,
    strength: a?.feedback?.strength ?? (best ? `${best.name}: ${best.pct}% correct.` : 'Too few marked questions to say.'),
    weakness: a?.feedback?.weakness ?? (worst && worst !== best ? `${worst.name}: ${worst.pct}% correct.` : 'No clear weak area.'),
    nextStep: a?.feedback?.nextStep ?? (worst ? `15-minute practice on ${worst.name.toLowerCase()}, then review it in the next session.` : 'Keep going with the plan.'),
    weakest: worst?.subtopicId,
  };
}

// ------------------------------------------------------------------ one session (5c to 5g)

/** Everything the session screens need: the session, who is in it, the last session with a report, the latest assignment and its homework. */
export function sessionContext(tutorId: string, sessionId: string) {
  const ws = getTutorWorkspace(tutorId);
  const s = ws?.sessions.find((x) => x.id === sessionId);
  if (!ws || !s) return undefined;
  const learners = s.learnerIds?.length ? s.learnerIds : [s.learnerId];
  const lid = learners[0]!;
  const prev = sessionsFor(ws, lid).filter((x) => x.report && x.startUtc < s.startUtc).sort((a, b) => a.startUtc.localeCompare(b.startUtc)).at(-1);
  const next = sessionsFor(ws, lid).filter((x) => x.status === 'scheduled' && x.startUtc > s.startUtc && x.id !== s.id).sort((a, b) => a.startUtc.localeCompare(b.startUtc))[0];
  const homework = (sess?: Session) => sess?.report ? getTasks(lid).filter((t) => t.refId === sess.id || sess.report!.homeworkTaskIds.includes(t.id)) : [];
  const series = scoreSeries(ws, lid).filter((x) => !s.subjectId || !x.subjectId || x.subjectId === s.subjectId);
  const latest = series.at(-1);
  const before = series.at(-2);
  const lastNote = ws.notes.filter((n) => n.learnerId === lid).sort((a, b) => b.createdUtc.localeCompare(a.createdUtc))[0];
  const earning = earningRows(ws).find((r) => r.session.id === s.id);
  return { ws, s, learners, lid, prev, next, prevHomework: homework(prev), ownHomework: homework(s), latest, latestDelta: latest && before ? latest.pct - before.pct : null, lastNote, earning, booking: ws.bookings.find((b) => b.id === s.bookingId) };
}

/** 5e: suggested next focus once this session is done; the next open gap after the one just taught. */
export function suggestNextFocus(ws: TutorWorkspace, s: Session): string {
  const lid = s.learnerIds?.[0] ?? s.learnerId;
  const current = aiFocus(ws, s).line.split(':')[0]!.toLowerCase();
  const gaps = openGapsFor(lid, s.subjectId ? [s.subjectId] : []).sort((a, b) => b.hoursToClose - a.hoursToClose);
  const names = namesFor([...new Set(gaps.map((g) => g.subjectId))]);
  const g = gaps.map((x) => ({ x, name: names[x.subtopicId] ?? x.subtopicId })).find((y) => !current.includes(y.name.toLowerCase().slice(0, 12)));
  return g ? `${g.name}: ${GAP_FOCUS[g.x.code] ?? 'close the gap'}` : `Consolidate ${current} with mixed practice`;
}
