/**
 * Server-side view models for the counsellor screens. Every number comes from lib/data reads or engines;
 * nothing here holds persona data.
 */
import 'server-only';
import { redirect } from 'next/navigation';
import {
  addDaysLocal, demoNow, getAttempts, demoToday, getAdult, getAlr, getApplications, getCareer, getCareerMatches, getCaseload, getCurrentPlan,
  getEvents, getGaps, getMeetingNotes, getProfile, getSessions, getStudent, getTasks, getTimetable, getTimetableRequests,
  listCareers, listExams, listParameters, listResources, listSkills, localDateOf,
  type CaseloadEntry, type MeetingNote, type RiskFlag as CaseFlag, type Student, type TimetableRequest, type TimetableWeek,
} from '@/lib/data';
import { careerGap, mapCareers, type CareerFit, type CareerGapResult, type TimetableBlock } from '@/lib/engines';
import { getPersona } from '@/lib/data/personas';
import { currentPersona } from '@/lib/session';
import type { Career, ProfileValue } from '@/lib/types';
import { buildStudent360, overallCompleteness, type Value360 } from './profile360';
import { riskFlags, type RiskFlag } from './risk';

export async function counsellorId(): Promise<string> {
  const p = await currentPersona();
  if (!p || p.role !== 'counsellor') redirect('/login');
  return p.id;
}

function counsellorName(id: string) {
  return getAdult(id)?.name ?? getPersona(id)?.name ?? id;
}

const now = () => new Date(demoNow());

/** All risk flags for one learner, from the W2-C rules in risk.ts. */
export function flagsForLearner(student: Student, staffId: string): RiskFlag[] {
  const n = now();
  const values = getProfile(student.id, 'counsellor');
  const latest = new Map<string, Value360>();
  for (const v of values) { const c = latest.get(v.paramId); if (!c || (v.asOfUtc ?? '') > (c.asOfUtc ?? '')) latest.set(v.paramId, v); }
  const wb: NonNullable<Parameters<typeof riskFlags>[0]['wellbeing']> = {};
  for (const pid of ['p109', 'p110', 'p114', 'p149'] as const) {
    const v = latest.get(pid);
    if (v?.asOfUtc && v.mode === 'full') wb[pid] = { value: v.value, asOfUtc: v.asOfUtc };
  }
  // A check-in event counts as a check-in even when p149 has no value yet.
  const checkin = getEvents(student.id, { type: 'wellbeing_checkin' }).pop();
  if (checkin && (!wb.p149 || wb.p149.asOfUtc < checkin.timestampUtc)) {
    const score = typeof checkin.payload?.score === 'number' ? (checkin.payload.score as number) : checkin.payload?.flag ? 2 : 4;
    wb.p149 = { value: score, asOfUtc: checkin.timestampUtc };
  }
  const sections = buildStudent360(listParameters(), values, n);
  const plan = getCurrentPlan(student.id);
  const lastAttempt = getEventsLastAttempt(student.id);
  const today = demoToday();
  const missed = getTasks(student.id, undefined, { range: [addDaysLocal(today, -7), addDaysLocal(today, -1)] }).filter((t) => t.status === 'skipped').length;
  const flags = riskFlags({
    learnerId: student.id, now: n,
    applications: getApplications(student.id).applications
      .filter((a) => a.status !== 'submitted' && a.status !== 'decision')
      .map((a) => ({ id: a.id, title: a.universityId.replace(/^uni-[a-z]{2}-/, '').replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()), deadlineUtc: `${a.deadline}T18:29:00Z`, openItems: a.checklist.filter((c) => !c.done).length })),
    wellbeing: wb,
    completeness: overallCompleteness(sections),
    sparseSections: sections.filter((s) => s.density < 0.1 && ['Academic Profile', 'Learning Behaviour', 'Career & Future Skills'].includes(s.section)).map((s) => s.section),
    lastAssessmentUtc: lastAttempt,
    lrsBand: student.band,
    gapCodes: getGaps(student.id, { status: 'open' }).map((g) => g.code),
    missedTasks7d: missed,
    pendingRequests: getTimetableRequests({ learnerId: student.id, status: 'pending' }).map((r) => ({ id: r.id, createdUtc: r.createdUtc, summary: r.reason })),
  });
  if (plan?.plan.paidTuition.recommended) {
    flags.push({ id: `${student.id}-learn-paid`, learnerId: student.id, kind: 'learning', severity: 'low', title: 'Paid tutor rule met', detail: plan.plan.paidTuition.reason, href: `/counsellor/student-360?student=${student.id}` });
  }
  void staffId;
  return flags;
}

function getEventsLastAttempt(id: string): string | undefined {
  return getAttempts(id).map((a) => a.submittedUtc).sort().pop();
}

const SEV_MAP: Record<RiskFlag['kind'], CaseFlag['kind']> = { deadline: 'deadline', wellbeing: 'wellbeing', data: 'data_sparsity', learning: 'engagement', request: 'request_pending' };

export async function loadCaseload() {
  const id = await counsellorId();
  const n = now();
  const today = demoToday();
  const entries: CaseloadEntry[] = getCaseload(id).map((e) => {
    const flags = flagsForLearner(e.student, id).filter((f) => f.severity !== 'low' || f.kind === 'deadline');
    const caseFlags: CaseFlag[] = flags.map((f) => ({ kind: SEV_MAP[f.kind], severity: f.severity, text: f.title, refId: f.id }));
    const sessionToday = !!e.nextSession && localDateOf(e.nextSession.startUtc) === today;
    return { ...e, focus: e.student.story ?? e.student.programme, flags: caseFlags, needsYouToday: caseFlags.some((f) => f.severity === 'high') || e.pendingRequests > 0 || sessionToday };
  }).sort((a, b) => Number(b.needsYouToday) - Number(a.needsYouToday) || b.flags.length - a.flags.length || a.student.name.localeCompare(b.student.name));
  const sessionsToday = getSessions(id).filter((s) => s.status === 'scheduled' && localDateOf(s.startUtc) === today);
  return { counsellor: { id, name: counsellorName(id) }, entries, sessionsToday, now: n };
}

function pickerList(id: string) {
  return getCaseload(id).map((e) => ({ id: e.student.id, name: e.student.name, meta: e.student.programme }));
}

export async function loadStudent360(studentId?: string) {
  const id = await counsellorId();
  const students = pickerList(id);
  const sid = students.find((s) => s.id === studentId)?.id ?? students[0]?.id;
  const student = sid ? getStudent(sid) : undefined;
  if (!student) return undefined;
  const values: Value360[] = getProfile(student.id, 'counsellor');
  return {
    student, students, params: listParameters(), values, now: now(),
    alr: getAlr(student.id).overall.LRS, openGaps: getGaps(student.id, { status: 'open' }).length,
  };
}

export interface RequestItem {
  request: TimetableRequest;
  studentName: string;
  blocks: TimetableBlock[];
  after?: TimetableWeek;
  changedBlockIds: string[];
}

export async function loadRequests() {
  const id = await counsellorId();
  const students = pickerList(id);
  const items: RequestItem[] = getTimetableRequests({ counsellorId: id }).map((request) => {
    const week = getTimetable(request.learnerId, request.weekStart);
    // Pending: the blocks as they are now. Decided: where they ended up (moved blocks get the suffix _moved).
    const wanted = new Set(request.status === 'pending' ? request.blockIds : request.blockIds.map((x) => `${x}_moved`));
    const blocks = (week?.blocks ?? []).filter((b) => wanted.has(b.id));
    return { request, studentName: getStudent(request.learnerId)?.name ?? request.learnerId, blocks, after: week, changedBlockIds: request.status === 'pending' ? [] : blocks.map((b) => b.id) };
  });
  return { items, now: now(), students };
}

export interface CompareColumn {
  career: Career;
  fit?: CareerFit;
  gap?: CareerGapResult;
  suggested: { title: string; dueOn: string }[];
}

function profileForEngines(values: ProfileValue[] | Value360[]) {
  return (values as Value360[]).filter((v) => v.mode !== 'summary' && v.asOfUtc).map((v) => ({ paramId: v.paramId, value: v.value, asOfUtc: v.asOfUtc!, tier: v.tier }));
}

export async function loadCareerSession(studentId?: string, a?: string, b?: string) {
  const id = await counsellorId();
  const students = pickerList(id);
  const sid = students.find((s) => s.id === studentId)?.id ?? students[0]?.id;
  const student = sid ? getStudent(sid) : undefined;
  if (!student) return undefined;
  const profile = profileForEngines(getProfile(student.id, 'counsellor'));
  const careers = listCareers();
  const ctx = { grade: student.grade, stream: student.stream, skills: listSkills(), resources: listResources(), exams: listExams() };
  const stored = getCareerMatches(student.id);
  const skillNames = new Map(ctx.skills.map((x) => [x.id, x.name]));
  const fits = stored?.fits?.length ? stored.fits : mapCareers(profile, careers, { ...ctx, limit: 10 });
  const ids = [a, b].filter((x): x is string => !!x && !!getCareer(x));
  const defaults = [...(stored?.shortlist ?? []), ...fits.map((f) => f.careerId)];
  for (const d of defaults) if (ids.length < 2 && !ids.includes(d)) ids.push(d);
  const due = addDaysLocal(demoToday(), 14);
  const compare: CompareColumn[] = ids.slice(0, 2).map((cid) => {
    const career = getCareer(cid)!;
    const raw = stored?.gaps?.[cid] ?? careerGap(profile, career, ctx);
    const gap = { ...raw, skills: raw.skills.map((x) => ({ ...x, name: skillNames.get(x.skillId) ?? x.name })) };
    const top = [...gap.skills].filter((s) => s.levelsToClimb > 0).sort((x, y) => Number(y.importance === 'core') - Number(x.importance === 'core') || y.hours - x.hours)[0];
    const suggested = top ? [{ title: `${career.title}: try the first free ${top.name} module`, dueOn: due }] : [];
    return { career, fit: fits.find((f) => f.careerId === cid), gap, suggested };
  });
  const notes: MeetingNote[] = getMeetingNotes(student.id, { kind: 'career' });
  const latest = notes[0];
  const savedRecent = latest && latest.staffId === id && latest.date === demoToday() ? latest : undefined;
  return { student, students, fits, compare, notes, defaultDue: due, saved: savedRecent, careers: careers.length };
}

export async function loadRiskFlags() {
  const id = await counsellorId();
  const entries = getCaseload(id);
  const flags = entries.flatMap((e) => flagsForLearner(e.student, id));
  const order = { high: 0, medium: 1, low: 2 } as const;
  flags.sort((x, y) => order[x.severity] - order[y.severity] || (x.dueUtc ?? '9').localeCompare(y.dueUtc ?? '9'));
  return { flags, names: Object.fromEntries(entries.map((e) => [e.student.id, e.student.name])) };
}
