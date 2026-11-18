/**
 * Server-side loaders for the student daily loop (W2-S2). The one seam between data and screens:
 * reads come from `@/lib/data` (W2-0), derived numbers from `@/lib/engines`. Components only render view models.
 */
import 'server-only';
import { careerGap, mapCareers, type CareerFit, type CareerGapResult, type TimetableBlock } from '@/lib/engines';
import {
  addDaysLocal, demoNow, demoToday, getAlr, getApplications, getCareer, getCareerMatches, getDocuments, getGaps,
  getNextBestActions, getPersonName, getProfileValues, getSessions, getStudent, getSubject, getSubtopic, getTasks, getTimetable,
  getTimetableRequests, getUniversity, listCareers, listExams, listResources, listSkills, listTutors, listUniversities, weekStartOf,
  type DocumentRecord, type Session, type Student, type Task, type TimetableRequest, type TimetableWeek,
} from '@/lib/data';
import { currentPersona } from '@/lib/session';
import type { Career } from '@/lib/types';
import {
  METRICS, type ApplicationCard, type GapView, type MetricKey, type MetricPoint, type MetricSummary, type NextActionView,
  type PersonCard, type SessionItem, type StudentPlan, type TaskItem, type TodoItem,
} from './model';

export const TZ_OFFSET = 330;
export const nowUtc = () => demoNow();
export const todayLocal = () => demoToday();
export const addDaysStr = addDaysLocal;
export const mondayOf = weekStartOf;

// ------------------------------------------------------------------ time helpers

/** Local (IST) date and HH:MM for an ISO UTC time. */
export function toLocal(isoUtc: string): { date: string; time: string } {
  const d = new Date(Date.parse(isoUtc) + TZ_OFFSET * 60_000).toISOString();
  return { date: d.slice(0, 10), time: d.slice(11, 16) };
}
export function fmtTime(hhmm: string): string {
  const [h, m] = hhmm.split(':').map(Number) as [number, number];
  return `${((h + 11) % 12) + 1}:${String(m).padStart(2, '0')} ${h < 12 ? 'am' : 'pm'}`;
}
export function fmtDay(date: string): string {
  return new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', timeZone: 'UTC' }).format(new Date(date + 'T00:00:00Z'));
}
export function whenLabel(isoUtc: string): string {
  const { date, time } = toLocal(isoUtc);
  const today = todayLocal();
  const day = date === today ? 'Today' : date === addDaysStr(today, 1) ? 'Tomorrow'
    : new Intl.DateTimeFormat('en-IN', { weekday: 'short', day: 'numeric', month: 'short', timeZone: 'UTC' }).format(new Date(date + 'T00:00:00Z'));
  return `${day} ${fmtTime(time)}`;
}
const shortName = (name: string) => name.split(/[:;]/)[0]!.trim();

// ------------------------------------------------------------------ context

export interface StudentCtx {
  learnerId: string;
  name: string;
  firstName: string;
  grade?: number;
  stream?: string;
  plan: StudentPlan;
  /** Has a counsellor, so may request a timetable change (PDF 3a/3b). */
  hasCounsellor: boolean;
  /** No assessment and no history yet (PDF 2a). */
  firstVisit: boolean;
  student?: Student;
}

export async function studentCtx(): Promise<StudentCtx> {
  const persona = await currentPersona();
  const learnerId = persona?.id ?? 'lrn_unknown';
  const student = getStudent(learnerId);
  const firstVisit = !student?.onboardedUtc && getGaps(learnerId).length === 0 && getAlr(learnerId).history.length === 0;
  return {
    learnerId,
    name: student?.name ?? persona?.name ?? 'Student',
    firstName: student?.firstName ?? persona?.name.split(' ')[0] ?? 'there',
    grade: student?.grade ?? persona?.grade,
    stream: student?.stream ?? persona?.stream,
    plan: student?.plan ?? 'free',
    hasCounsellor: (student?.counsellorIds?.length ?? 0) > 0,
    firstVisit,
    student,
  };
}

export const isSubscriber = (ctx: StudentCtx) => ctx.plan === 'application_support' || ctx.plan === 'full_package';

// ------------------------------------------------------------------ gaps

export function gapViews(ctx: StudentCtx): GapView[] {
  return getGaps(ctx.learnerId, { status: 'open' }).map((g) => {
    const st = getSubtopic(g.subtopicId);
    return {
      id: g.id, subtopicId: g.subtopicId, code: g.code, status: g.status, hoursToClose: g.hoursToClose,
      subject: getSubject(g.subjectId)?.subject.name ?? g.subjectId, title: st ? shortName(st.name) : g.subtopicId,
    };
  });
}

// ------------------------------------------------------------------ timetable and tasks

export function weekTimetable(ctx: StudentCtx, weekStart = mondayOf(todayLocal())): TimetableWeek | null {
  if (ctx.firstVisit) return null;
  return getTimetable(ctx.learnerId, weekStart) ?? null;
}

const BLOCK_HREF: Partial<Record<TimetableBlock['kind'], string>> = { weekly_test: '/student/assessments', session: '/student/sessions' };

export function blockToTask(b: TimetableBlock): TaskItem {
  return {
    id: b.id, title: b.title.replace(/^Review \d\/\d: /, 'Review · '), kind: b.kind, done: b.status === 'done',
    meta: b.kind === 'session' ? fmtTime(b.start) : `${fmtTime(b.start)} · ${b.minutes} min`,
    href: BLOCK_HREF[b.kind],
  };
}

const TASK_TAG: Partial<Record<Task['source'], string>> = { tutor: 'tutor', teacher: 'teacher', counsellor: 'to-do', mentor: 'mentor', meeting: 'to-do' };

export function taskToItem(t: Task, subscriber: boolean): TaskItem {
  const app = t.kind === 'application';
  return {
    id: t.id, title: t.title, kind: app ? 'application' : t.kind === 'homework' ? 'homework' : 'todo', done: t.status === 'done',
    meta: t.minutes ? `${t.minutes} min` : undefined, href: t.href,
    tag: app && subscriber ? 'app' : TASK_TAG[t.source] ?? (t.kind === 'homework' ? 'homework' : undefined),
  };
}

/** One day's list: timetable blocks (minus buffers) then tasks due that day (homework, to-dos, application items). */
export function tasksFor(ctx: StudentCtx, date: string, tt = weekTimetable(ctx, mondayOf(date))): TaskItem[] {
  const blocks = (tt?.blocks ?? []).filter((b) => b.date === date && b.kind !== 'buffer').sort((a, b) => a.start.localeCompare(b.start));
  const tasks = getTasks(ctx.learnerId, date).filter((t) => t.status !== 'skipped' && t.source !== 'timetable');
  return [...blocks.map(blockToTask), ...tasks.map((t) => taskToItem(t, isSubscriber(ctx)))];
}

/** First-visit draft plan (PDF 2a) until the first assessment. */
export function starterTasks(): TaskItem[] {
  return [
    { id: 'starter_assessment', title: 'Take your free assessment', meta: '20 min', kind: 'weekly_test', done: false, href: '/student/assessments' },
    { id: 'starter_profile', title: 'Add your subjects and school marks', meta: '5 min', kind: 'todo', done: false, href: '/student/inventory' },
  ];
}

// ------------------------------------------------------------------ next best action

const NBA_HREF: Record<string, string> = {
  gap: '/student/timetable', review: '/student/timetable', weekly_test: '/student/assessments', career: '/student/career', profile: '/student/inventory',
};
const NBA_CTA: Record<string, string> = {
  gap: 'Open in timetable', review: 'Start review', weekly_test: 'Take the test', career: 'Explore careers', profile: 'Complete profile', deadline: 'Open',
};

export function nextActions(ctx: StudentCtx): NextActionView[] {
  if (ctx.firstVisit) {
    return [{ kind: 'assessment', title: 'Take your free assessment', reason: 'Three short tests, about 20 minutes each. They unlock your gap analysis and a smarter timetable.', href: '/student/assessments', cta: 'Start' }];
  }
  return getNextBestActions(ctx.learnerId, 3).map((a) => ({
    kind: a.kind, title: a.title, reason: a.reason,
    // the engine's own profile and career hrefs predate the final routes
    href: a.kind === 'deadline' ? a.href ?? '/student/applications' : NBA_HREF[a.kind] ?? a.href,
    cta: NBA_CTA[a.kind] ?? 'Open',
  }));
}

// ------------------------------------------------------------------ metrics (PDF 2b, 2d)

/** Each metric as of a local date, so the cards and the week, month and year graphs share one definition. */
function metricAt(ctx: StudentCtx, key: MetricKey, asOf: string): number | null {
  const id = ctx.learnerId;
  if (key === 'learning-rate' || key === 'retention') {
    const latest = new Map<string, number>();
    for (const r of getAlr(id).history) {
      if (toLocal(r.asOfUtc).date > asOf) continue;
      const v = key === 'learning-rate' ? r.LRS : r.R;
      if (typeof v === 'number' && !Number.isNaN(v)) latest.set(r.chapterId, v);
    }
    const vals = [...latest.values()];
    return vals.length ? vals.reduce((s, v) => s + v, 0) / vals.length : null;
  }
  if (key === 'task-completion') {
    const due = getTasks(id, undefined, { range: [addDaysStr(asOf, -6), asOf] }).filter((t) => t.source !== 'timetable');
    return due.length ? due.filter((t) => t.status === 'done').length / due.length : null;
  }
  // discipline: study blocks done ÷ blocks planned, Monday to asOf of that week
  const tt = getTimetable(id, mondayOf(asOf));
  const past = (tt?.blocks ?? []).filter((b) => b.kind !== 'buffer' && b.kind !== 'session' && b.date <= asOf && b.endUtc <= nowUtc());
  // a week built live has no recorded outcomes; only weeks with ticks or misses count
  if (!past.some((b) => b.status !== 'planned')) return null;
  return past.length >= 3 ? past.filter((b) => b.status === 'done').length / past.length : null;
}

export function metricSummaries(ctx: StudentCtx): MetricSummary[] {
  return METRICS.map(({ key, label }) => {
    if (ctx.firstVisit) return { key, label, value: null, delta: null, emptyReason: 'After your first assessment' };
    const today = todayLocal();
    const lastSunday = addDaysStr(mondayOf(today), -1);
    let value = metricAt(ctx, key, today);
    if (value === null && key === 'discipline') value = metricAt(ctx, key, lastSunday);
    const prev = metricAt(ctx, key, key === 'discipline' ? addDaysStr(lastSunday, -7) : addDaysStr(today, -7));
    const delta = value !== null && prev !== null ? Math.round((value - prev) * 100) / 100 : null;
    return { key, label, value, delta, emptyReason: value === null ? 'Not enough evidence yet' : undefined };
  });
}

export type MetricRange = 'week' | 'month' | 'year';

export function metricSeries(ctx: StudentCtx, key: MetricKey, range: MetricRange): MetricPoint[] {
  if (ctx.firstVisit) return [];
  const today = todayLocal();
  if (range === 'week') {
    const mon = mondayOf(today);
    return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((x, i) => {
      const d = addDaysStr(mon, i);
      return { x, value: d <= today ? metricAt(ctx, key, d) : null };
    });
  }
  const weeks = range === 'month' ? 5 : 32;
  const pts: MetricPoint[] = [];
  for (let i = weeks - 1; i >= 0; i--) {
    const end = addDaysStr(mondayOf(today), -7 * i + 6);
    const asOf = end > today ? today : end;
    pts.push({ x: fmtDay(mondayOf(asOf)), value: metricAt(ctx, key, asOf) });
  }
  const first = pts.findIndex((p) => p.value !== null);
  return first < 0 ? [] : pts.slice(first);
}

// ------------------------------------------------------------------ sessions and people (PDF 10a to 10c)

const ROLE_LABEL: Record<Session['hostRole'], string> = { tutor: 'Tutor', counsellor: 'Counsellor', mentor: 'Mentor', teacher: 'Teacher' };

export function sessionsOf(ctx: StudentCtx): SessionItem[] {
  const count = new Map<string, number>();
  return getSessions(ctx.learnerId).map((s) => {
    const n = (count.get(s.hostId) ?? 0) + (s.kind === 'demo' ? 0 : 1);
    count.set(s.hostId, n);
    return {
      id: s.id, personId: s.hostId, personName: getPersonName(s.hostId)?.name ?? s.hostId,
      role: s.hostRole === 'teacher' ? 'tutor' : s.hostRole,
      roleLabel: ROLE_LABEL[s.hostRole], title: s.title, label: s.kind === 'demo' ? 'Free demo' : `Session ${n}`,
      startUtc: s.startUtc, endUtc: new Date(Date.parse(s.startUtc) + s.minutes * 60_000).toISOString(),
      platform: s.mode === 'offline' ? 'In person' : 'Google Meet', topic: s.focus ?? undefined,
      status: s.status === 'no_show' ? 'missed' : s.status,
      summary: s.report ? summaryOf(s.report) : undefined,
    };
  });
}
function summaryOf(r: NonNullable<Session['report']>): string {
  const o = r as unknown as Record<string, unknown>;
  for (const k of ['summary', 'notes', 'covered', 'text']) if (typeof o[k] === 'string' && o[k]) return o[k] as string;
  return 'Session report available.';
}

export function joinState(s: SessionItem): 'open' | 'soon' | 'ended' {
  const now = Date.parse(nowUtc());
  if (now >= Date.parse(s.endUtc)) return 'ended';
  return now >= Date.parse(s.startUtc) - 10 * 60_000 ? 'open' : 'soon';
}

export function people(ctx: StudentCtx): PersonCard[] {
  const s = ctx.student;
  if (!s) return [];
  const sessions = getSessions(ctx.learnerId);
  const card = (id: string, role: PersonCard['role']): PersonCard | null => {
    const p = getPersonName(id);
    if (!p) return null;
    const mine = sessions.filter((x) => x.hostId === id);
    const subj = mine.find((x) => x.subjectId)?.subjectId;
    const subjName = subj ? getSubject(subj)?.subject.name : undefined;
    return {
      id, role, name: p.name,
      focus: role === 'counsellor' ? (id === s.counsellorIds[0] ? 'Main counsellor' : 'Counsellor') : role === 'mentor' ? 'Career mentor' : `${subjName ?? 'Subject'} tutor`,
      sinceUtc: mine[0]?.startUtc ?? s.joinedUtc,
      sessionCount: mine.filter((x) => x.status === 'completed').length,
    };
  };
  return [
    ...(s.counsellorIds ?? []).map((id) => card(id, 'counsellor')),
    ...(s.tutorIds ?? []).map((id) => card(id, 'tutor')),
    ...(s.mentorIds ?? []).map((id) => card(id, 'mentor')),
  ].filter((x): x is PersonCard => !!x);
}

export function mainCounsellor(ctx: StudentCtx) {
  const id = ctx.student?.counsellorIds?.[0];
  const p = id ? getPersonName(id) : undefined;
  return p ? { id: p.id, name: p.name } : undefined;
}

/** To-dos a person set for the student: the tasks they created (PDF 10b). */
export function todosFrom(ctx: StudentCtx, personId: string): TodoItem[] {
  return getTasks(ctx.learnerId, undefined, { createdBy: personId })
    .filter((t) => t.status !== 'skipped')
    .map((t) => ({ id: t.id, fromPersonId: personId, title: t.title, dueOn: t.dueDate, status: t.status === 'done' ? 'done' : 'pending' }));
}

// ------------------------------------------------------------------ applications (PDF 2c)

export function applicationCards(ctx: StudentCtx): ApplicationCard[] {
  return getApplications(ctx.learnerId).applications
    .filter((a) => a.status !== 'decision')
    .sort((a, b) => a.deadline.localeCompare(b.deadline))
    .slice(0, 3)
    .map((a) => {
      const u = getUniversity(a.universityId);
      const prog = u?.programmes.find((p) => p.id === a.programmeId);
      const done = a.checklist.filter((c) => c.done).length;
      const open = a.checklist.find((c) => !c.done);
      return {
        id: a.id, title: `${u?.shortName ?? a.universityId}${prog ? ` · ${prog.name}` : ''}`,
        progress: a.checklist.length ? done / a.checklist.length : 0,
        deadlineUtc: `${a.deadline}T12:00:00.000Z`,
        note: a.riskFlags?.[0] ?? (a.status === 'submitted' ? 'Submitted' : open ? `Next: ${open.title}` : 'Ready to submit'),
        status: a.status, atRisk: (a.riskFlags?.length ?? 0) > 0,
      };
    });
}

// ------------------------------------------------------------------ timetable change requests (PDF 3b, 3c)

export function pendingRequests(learnerId: string): TimetableRequest[] {
  return getTimetableRequests({ learnerId, status: 'pending' });
}
export function requestTitle(r: TimetableRequest, blockTitle?: (id: string) => string | undefined): string {
  const fromBlock = r.blockIds.map((id) => blockTitle?.(id)).find(Boolean);
  return fromBlock ?? (r.reason.split(' · ')[0] || 'Change');
}
/** Dates a pending request would occupy inside the given week. */
export function requestDates(r: TimetableRequest, weekStart: string): string[] {
  const p = r.proposed;
  if (!p || typeof p !== 'object') return [];
  return p.date >= weekStart && p.date < addDaysStr(weekStart, 7) ? [p.date] : [];
}
export function describeRequest(r: TimetableRequest, blockTitle?: (id: string) => string | undefined): string {
  const p = r.proposed;
  const t = requestTitle(r, blockTitle);
  const why = r.reason.includes(' · ') || t === r.reason ? '' : ` (${r.reason.replace(/\.$/, '')})`;
  if (p && typeof p === 'object') return `${t} → ${fmtDay(p.date)}, ${fmtTime(p.start)} to ${fmtTime(p.end)}${why}`;
  return `${t} → ${typeof p === 'string' ? p : 'a new time'}${why}`;
}

// ------------------------------------------------------------------ inventory (PDF 4a to 4c)

export type Shelf = DocumentRecord['folder'];
export const SHELF_LABEL: Record<Shelf, string> = {
  academics: 'Academics', activities: 'Activities', application_documents: 'Application documents', job_ready: 'Job-ready profile',
};
export interface InventoryFile {
  id: string; title: string; fileName?: string; kind: string; uploadedAt: string; source: 'uploaded' | 'auto'; href?: string;
}
export interface InventoryFolder { slug: string; name: string; shelf: Shelf; files: InventoryFile[]; locked: boolean; hint: string }

export const slugify = (s: string) => s.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

/** Class a document belongs to: Indian school year (April to March) of its date, relative to the current grade. */
function classOf(isoUtc: string, grade: number): number {
  const yearStart = (date: string) => Number(date.slice(0, 4)) - (Number(date.slice(5, 7)) < 4 ? 1 : 0);
  return grade - (yearStart(todayLocal()) - yearStart(toLocal(isoUtc).date));
}

const FOLDERS: [Shelf, string, string][] = [
  ['activities', 'Projects', 'School and personal projects, with a photo or a link.'],
  ['activities', 'Extracurricular', 'Sports, music, clubs and anything you do outside class.'],
  ['activities', 'Internships', 'Offer letters, completion letters and what you worked on.'],
  ['activities', 'Competitions', 'Olympiads, quizzes, debates and hackathons.'],
  ['activities', 'Hobbies & interests', 'What you love doing; it shapes career matches.'],
  ['application_documents', 'Essay drafts', 'Personal statements and supplements, with versions.'],
  ['application_documents', 'Resume', 'Your activities resume for applications.'],
  ['application_documents', 'Letters and records', 'Recommendations, transcripts and ID documents for applications.'],
  ['job_ready', 'Profile', 'Skills and evidence employers and colleges look for.'],
  ['job_ready', 'Portfolio projects', 'Work samples that show a skill: code, models, designs, writing.'],
];

/** The record carries only the shelf; the folder follows from kind, title and date. */
export function folderOf(d: Pick<DocumentRecord, 'folder' | 'title' | 'kind' | 'uploadedUtc' | 'refId'>, grade: number, names: string[] = []): string {
  const pinned = d.refId?.startsWith('folder:') ? names.find((n) => slugify(n) === d.refId!.slice(7)) : undefined;
  if (pinned) return pinned;
  const t = d.title.toLowerCase();
  if (d.folder === 'academics') return `Class ${classOf(d.uploadedUtc, grade)}`;
  if (d.folder === 'activities') {
    if (/intern/.test(t)) return 'Internships';
    if (/olympiad|quiz|competition|hackathon|debate|contest|mun\b/.test(t)) return 'Competitions';
    if (/project/.test(t)) return 'Projects';
    if (/hobb|music|art|paint|reading/.test(t)) return 'Hobbies & interests';
    return 'Extracurricular';
  }
  if (d.folder === 'application_documents') return d.kind === 'essay' ? 'Essay drafts' : /resume|\bcv\b/.test(t) ? 'Resume' : 'Letters and records';
  return d.kind === 'portfolio' ? 'Portfolio projects' : 'Profile';
}

export function inventory(ctx: StudentCtx): InventoryFolder[] {
  const g = ctx.grade ?? 9;
  const classes: [Shelf, string, string][] = [g - 1, g, g + 1].filter((c) => c >= 8 && c <= 12)
    .map((c) => ['academics', `Class ${c}`, 'Report cards, test papers, marksheets and certificates for the year.']);
  const docs = getDocuments(ctx.learnerId);
  const all = [...classes, ...FOLDERS];
  const names = all.map((f) => f[1]);
  return all.map(([shelf, name, hint]) => ({
    slug: slugify(name), name, shelf, hint, locked: shelf === 'application_documents' && !isSubscriber(ctx),
    files: docs.filter((d) => d.folder === shelf && folderOf(d, g, names) === name).map((d) => ({
      id: d.id, title: d.title, fileName: d.fileName, kind: d.kind, uploadedAt: d.uploadedUtc,
      source: d.source === 'auto' ? 'auto' : 'uploaded',
      href: d.source === 'auto' && d.refId && !d.refId.startsWith('folder:') ? `/student/assessments/results/${d.refId}/gaps` : undefined,
    })),
  }));
}

// ------------------------------------------------------------------ careers (PDF 9a to 9f)

export const careers = (): Career[] => listCareers();
export const skills = () => listSkills();
export const universities = () => listUniversities();
export const careerById = (id: string) => getCareer(id);
export const universityById = (id: string) => getUniversity(id);
export const resourceById = (id: string) => listResources().find((r) => r.id === id);

export function careerCtx(ctx: StudentCtx) {
  return { grade: ctx.grade as never, stream: ctx.stream as never, weeklyHours: 5, skills: listSkills(), resources: listResources(), exams: listExams() };
}
/** Stored matches when the persona has them, else computed live (the engine strips T3 values). */
export function careerMatches(ctx: StudentCtx, limit?: number): CareerFit[] {
  const stored = getCareerMatches(ctx.learnerId);
  const fits = stored?.fits.length ? stored.fits : mapCareers(getProfileValues(ctx.learnerId), careers(), careerCtx(ctx));
  return limit ? fits.slice(0, limit) : fits;
}
export function careerGapFor(ctx: StudentCtx, careerId: string): { career: Career; gap: CareerGapResult } | null {
  const career = getCareer(careerId);
  if (!career) return null;
  const stored = getCareerMatches(ctx.learnerId)?.gaps?.[careerId];
  return { career, gap: stored ?? careerGap(getProfileValues(ctx.learnerId), career, careerCtx(ctx)) };
}

export const lpa = (inr: number) => `₹${Math.round((inr / 100_000) * 10) / 10} LPA`;
export const lpaRange = (lo: number, hi: number) => `₹${Math.round(lo / 100_000)}–${Math.round(hi / 100_000)} LPA`;
export const DEMAND_LABEL: Record<string, string> = { very_high: 'Very high', high: 'High', medium: 'Medium', low: 'Low' };
export const skillName = (id: string) => listSkills().find((s) => s.id === id)?.name ?? id.replace(/^skill-/, '').replace(/-/g, ' ');

/** Platform tutors who teach a subject behind the career's gap skills ("trainers on platform", PDF 9d). */
export function trainersFor(career: Career, skillIds: string[], limit = 2) {
  const slugs = new Set([
    ...listSkills().filter((s) => skillIds.includes(s.id)).flatMap((s) => s.subjectSlugs),
    ...career.subjects.map((s) => s.subjectSlug),
  ]);
  return listTutors().filter((t) => t.subjects.some((s) => slugs.has(s.subjectSlug)))
    .sort((a, b) => a.pricing.oneToOnePerHourInr - b.pricing.oneToOnePerHourInr).slice(0, limit);
}
