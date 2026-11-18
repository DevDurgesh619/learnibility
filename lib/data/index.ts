/**
 * W2-0 read API. The ONLY way screens read persona data. Server only.
 *
 * Source per learner: data/personas/students/{id}/ when present, else data/fixtures/students/{id}/,
 * plus data/fixtures/contrib/*.json, with demo writes (lib/store overlay) merged on top.
 * Writes go through lib/actions/core.ts (appendEvent, putRecord, recomputeLearner).
 *
 * Every function is synchronous and returns plain JSON-safe data (safe to pass to client components).
 */
import 'server-only';
import path from 'node:path';
import { DEMO_NOW_ISO } from '@/lib/demo-clock';
import { getPersona, listPersonas } from '@/lib/data/personas';
import { matchTutors, type NextAction, type TutorMatch } from '@/lib/engines';
import type { EvidenceEvent, ProfileParameter, ProfileValue, Role, Tutor } from '@/lib/types';
import { visibleProfile, type VisibilityOptions, type VisibleValue } from '@/lib/visibility';
import { learnerRecords, records } from '@/lib/store/collections';
import { getSubject, getTutor, namesFor } from './catalogue';
import { addDaysLocal, buildWeek, localDateOf, nbaFor, summariseAlr, weekStartOf } from './derive';
import { dataRoot, itemsOf, learnerSources } from './source';
import type {
  Adult,
  AlrSummary,
  Application,
  ApplicationsBundle,
  Approval,
  Assignment,
  Attempt,
  Booking,
  CareerMatches,
  CaseloadEntry,
  ChildSummary,
  Comment,
  Consent,
  DocumentRecord,
  FinanceVisa,
  GapRecord,
  Invoice,
  LocalDate,
  MasteryRecord,
  MeetingNote,
  Message,
  Payout,
  PlanRecord,
  RiskFlag,
  Section,
  SectionHeatmap,
  Session,
  ShortlistEntry,
  Student,
  Task,
  TimetableRequest,
  TimetableWeek,
  TutorNote,
  TutorWorkspace,
} from './types';

export * from './types';
export * from './catalogue';
export { weekStartOf, localDateOf, addDaysLocal } from './derive';

/** The demo's "now" (ISO). All reads that depend on time use it. */
export const demoNow = (): string => new Date(DEMO_NOW_ISO).toISOString();
export const demoToday = (): LocalDate => localDateOf(demoNow());

const byTime = <T>(k: keyof T) => (a: T, b: T) => String(a[k]).localeCompare(String(b[k]));

// ------------------------------------------------------------------ people

/** Every learner with data (fixtures or personas). */
export function listStudents(): Student[] {
  return records<Student>('student').sort((a, b) => a.name.localeCompare(b.name));
}

/** A student record. Falls back to the persona picker entry (e.g. a brand-new user) when no student.json exists. */
export function getStudent(id: string): Student | undefined {
  const s = records<Student>('student').find((x) => x.id === id);
  if (s) return s;
  const p = getPersona(id);
  if (!p || p.role !== 'student') return undefined;
  const [firstName, ...rest] = p.name.split(' ');
  return {
    id: p.id, role: 'student', firstName, lastName: rest.join(' '), name: p.name,
    board: p.board ?? 'cbse', grade: p.grade ?? 9, stream: p.stream ?? 'none', programme: p.programme ?? '',
    school: '', city: '', band: 'average', plan: 'free', subjects: [], availability: [], weeklyHours: 6, tzOffsetMinutes: 330,
    joinedUtc: demoNow(), parentIds: [], counsellorIds: [], mentorIds: [], tutorIds: [], sectionIds: [], profileCompletionPct: 0, story: p.story,
  };
}

export function listAdults(role?: Adult['role']): Adult[] {
  return records<Adult>('adults').filter((a) => !role || a.role === role);
}

export function getAdult(id: string): Adult | undefined {
  return records<Adult>('adults').find((a) => a.id === id);
}

/** Name and role of anyone (student, adult or tutor), for bylines and avatars. */
export function getPersonName(id: string): { id: string; name: string; role: Role } | undefined {
  const s = records<Student>('student').find((x) => x.id === id);
  if (s) return { id, name: s.name, role: 'student' };
  const a = getAdult(id);
  if (a) return { id, name: a.name, role: a.role };
  const t = getTutor(id);
  if (t) return { id, name: t.displayName, role: 'tutor' };
  const p = getPersona(id);
  return p ? { id, name: p.name, role: p.role } : undefined;
}

/** Where a learner's data comes from right now. */
export function dataSourceOf(learnerId: string): 'personas' | 'fixtures' | 'none' {
  return learnerSources().get(learnerId) ?? 'none';
}

// ------------------------------------------------------------------ profile

export function getProfileValues(id: string): ProfileValue[] {
  return learnerRecords<ProfileValue>('profile', id);
}

/** Profile values filtered for the viewer (lib/visibility). Tutors see only shared params. */
export function getProfile(id: string, viewerRole: Role, opts: VisibilityOptions & { viewerId?: string } = {}): VisibleValue[] {
  const values = getProfileValues(id);
  let shared = opts.sharedParamIds;
  if (viewerRole === 'tutor' && !shared && opts.viewerId) {
    shared = getBookings(id).filter((b) => b.tutorId === opts.viewerId).flatMap((b) => b.sharedParamIds ?? []);
  }
  return visibleProfile(values, viewerRole, { ...opts, sharedParamIds: shared, isSelf: opts.isSelf ?? (viewerRole === 'student' ? opts.viewerId === undefined || opts.viewerId === id : undefined) });
}

let paramsCache: ProfileParameter[] | undefined;
export function listParameters(): ProfileParameter[] {
  paramsCache ??= itemsOf<ProfileParameter>(path.join(dataRoot(), 'profile', 'parameters.json'));
  return paramsCache;
}

/** Filled parameters and evidence events per profile section (counsellor data-sparsity flags). */
export function getEvidenceDensity(id: string): { section: string; parameters: number; filled: number; events: number }[] {
  const params = listParameters();
  const filled = new Set(getProfileValues(id).map((v) => v.paramId));
  const events = getEvents(id);
  const evBySection = new Map<string, number>();
  const sectionOf = new Map(params.map((p) => [p.id, p.section]));
  for (const e of events) {
    for (const pid of ((e.payload?.parameterIds as string[] | undefined) ?? [])) {
      const s = sectionOf.get(pid);
      if (s) evBySection.set(s, (evBySection.get(s) ?? 0) + 1);
    }
  }
  const sections = [...new Set(params.map((p) => p.section))];
  return sections.map((section) => {
    const ps = params.filter((p) => p.section === section);
    return { section, parameters: ps.length, filled: ps.filter((p) => filled.has(p.id)).length, events: evBySection.get(section) ?? 0 };
  });
}

/** Evidence events, oldest first. Wellbeing check-ins are type 'wellbeing_checkin' (T3: counsellor and student only). */
export function getEvents(id: string, filter: { type?: string | string[]; since?: string } = {}): EvidenceEvent[] {
  const types = filter.type ? (Array.isArray(filter.type) ? filter.type : [filter.type]) : undefined;
  return learnerRecords<EvidenceEvent>('events', id)
    .filter((e) => (!types || types.includes(e.type)) && (!filter.since || e.timestampUtc >= filter.since))
    .sort(byTime('timestampUtc'));
}

// ------------------------------------------------------------------ learning record

export function getMastery(id: string, subjectId?: string): MasteryRecord[] {
  return learnerRecords<MasteryRecord>('mastery', id).filter((m) => !subjectId || m.subjectId === subjectId).sort(byTime('subtopicId'));
}

export function getAlr(id: string): AlrSummary {
  return summariseAlr(learnerRecords('alr', id));
}

/** Gaps, worst first. Default: every status. Teacher validation (#430) is on `validation`; a corrected code is applied. */
export function getGaps(id: string, opts: { status?: GapRecord['status'] | GapRecord['status'][] | 'open'; subjectId?: string } = {}): GapRecord[] {
  const st = opts.status === 'open' ? ['suspected', 'confirmed', 'in_progress'] : opts.status ? (Array.isArray(opts.status) ? opts.status : [opts.status]) : undefined;
  return learnerRecords<GapRecord>('gaps', id)
    .map((g) => (g.validation?.verdict === 'corrected' && g.validation.correctedCode ? { ...g, code: g.validation.correctedCode } : g))
    .filter((g) => (!st || st.includes(g.status)) && (!opts.subjectId || g.subjectId === opts.subjectId))
    .sort((a, b) => Number(a.status === 'closed') - Number(b.status === 'closed') || a.level - b.level || b.hoursToClose - a.hoursToClose || a.id.localeCompare(b.id));
}

/** Intervention plans, newest first. The first one with status 'active' is current. */
export function getPlans(id: string): PlanRecord[] {
  return learnerRecords<PlanRecord>('plans', id).sort((a, b) => b.createdUtc.localeCompare(a.createdUtc));
}

export function getCurrentPlan(id: string): PlanRecord | undefined {
  return getPlans(id).find((p) => p.status === 'active') ?? getPlans(id)[0];
}

/** Attempts, newest first. */
export function getAttempts(id: string, filter: { kind?: Attempt['kind']; subjectId?: string; chapterId?: string } = {}): Attempt[] {
  return learnerRecords<Attempt>('attempts', id)
    .filter((a) => (!filter.kind || a.kind === filter.kind) && (!filter.subjectId || a.subjectId === filter.subjectId) && (!filter.chapterId || a.chapterId === filter.chapterId))
    .sort((a, b) => b.submittedUtc.localeCompare(a.submittedUtc));
}

export function getAttempt(attemptId: string): Attempt | undefined {
  return records<Attempt>('attempts').find((a) => a.id === attemptId);
}

// ------------------------------------------------------------------ daily loop

/**
 * The week's timetable (weekStart is a local Monday; any date is snapped to its Monday).
 * Stored weeks (JSON or re-planned by a write) win; other weeks are built live with the timetable engine.
 */
export function getTimetable(id: string, weekStart: LocalDate = weekStartOf(demoToday())): TimetableWeek | undefined {
  const ws = weekStartOf(weekStart);
  const stored = learnerRecords<TimetableWeek>('timetable', id).filter((w) => w.weekStart === ws).sort(byTime('generatedUtc')).pop();
  if (stored) return stored;
  const student = getStudent(id);
  if (!student || !student.availability.length) return undefined;
  return buildWeek(student, ws, { gaps: getGaps(id), mastery: getMastery(id), sessions: getSessions(id), now: demoNow() });
}

/** Tasks. `date` = one local day; `range` = [from, to] inclusive; neither = all. Sorted by due date. */
export function getTasks(id: string, date?: LocalDate, opts: { range?: [LocalDate, LocalDate]; status?: Task['status']; source?: Task['source']; createdBy?: string } = {}): Task[] {
  return learnerRecords<Task>('tasks', id)
    .filter(
      (t) =>
        (!date || t.dueDate === date) &&
        (!opts.range || (t.dueDate >= opts.range[0] && t.dueDate <= opts.range[1])) &&
        (!opts.status || t.status === opts.status) &&
        (!opts.source || t.source === opts.source) &&
        (!opts.createdBy || t.createdBy === opts.createdBy),
    )
    .sort((a, b) => a.dueDate.localeCompare(b.dueDate) || a.id.localeCompare(b.id));
}

/** Timetable change requests. Filter by learner, counsellor (their caseload) or status. Newest first. */
export function getTimetableRequests(f: { learnerId?: string; counsellorId?: string; status?: TimetableRequest['status'] } = {}): TimetableRequest[] {
  const caseload = f.counsellorId ? new Set(getAdult(f.counsellorId)?.learnerIds ?? []) : undefined;
  return records<TimetableRequest>('requests')
    .filter((r) => (!f.learnerId || r.learnerId === f.learnerId) && (!caseload || caseload.has(r.learnerId) || r.counsellorId === f.counsellorId) && (!f.status || r.status === f.status))
    .sort((a, b) => b.createdUtc.localeCompare(a.createdUtc));
}

/** Ranked next best actions, computed live from current state (changes after every write). */
export function getNextBestActions(id: string, limit = 5): NextAction[] {
  const student = getStudent(id);
  if (!student) return [];
  return nbaFor(
    student,
    { now: demoNow(), gaps: getGaps(id), mastery: getMastery(id), attempts: getAttempts(id), tasks: getTasks(id), applications: getApplications(id).applications, careers: getCareerMatches(id) },
    limit,
  );
}

// ------------------------------------------------------------------ sessions and marketplace

/** Sessions for a learner (any host) or a host (tutor, counsellor, mentor, teacher). Oldest first. */
export function getSessions(personId: string, f: { from?: string; to?: string; status?: Session['status'] } = {}): Session[] {
  const isLearner = personId.startsWith('lrn_');
  return records<Session>('sessions')
    .filter((s) => (isLearner ? (s.learnerIds ?? [s.learnerId]).includes(personId) : s.hostId === personId))
    .filter((s) => (!f.from || s.startUtc >= f.from) && (!f.to || s.startUtc <= f.to) && (!f.status || s.status === f.status))
    .sort(byTime('startUtc'));
}

/** Bookings for a learner or a tutor. Newest first. */
export function getBookings(personId: string): Booking[] {
  const isLearner = personId.startsWith('lrn_');
  return records<Booking>('bookings')
    .filter((b) => (isLearner ? b.learnerId === personId : b.tutorId === personId))
    .sort((a, b) => b.requestedAt.localeCompare(a.requestedAt));
}

/** Tutors ranked for the learner's open gaps (engine 5). T3 is never used. */
export function getTutorMatches(id: string, opts: { subjectId?: string; limit?: number } = {}): TutorMatch[] {
  const student = getStudent(id);
  if (!student) return [];
  const gaps = getGaps(id, { status: 'open', subjectId: opts.subjectId });
  const profile = getProfileValues(id).filter((v) => v.tier !== 'T3' && v.tier !== 'C');
  const names = namesFor(student.subjects.map((s) => s.subjectId));
  return matchTutors(
    gaps.map((g) => ({ id: g.id, subtopicId: g.subtopicId, code: g.code, hoursToClose: g.hoursToClose, board: student.board, grade: student.grade })),
    profile,
    itemsOf<Tutor>(path.join(dataRoot(), 'catalogues', 'tutors.json')),
    { names, availability: student.availability, limit: opts.limit ?? 6 },
  );
}

// ------------------------------------------------------------------ careers, applications, documents

export function getCareerMatches(id: string): CareerMatches | undefined {
  return learnerRecords<CareerMatches>('careers', id)[0];
}

function riskFlagsFor(a: Application, today: LocalDate): string[] {
  const flags = [...(a.riskFlags ?? [])];
  if (a.status === 'submitted' || a.status === 'decision') return flags;
  const days = Math.round((Date.parse(a.deadline) - Date.parse(today)) / 86_400_000);
  const open = a.checklist.filter((c) => !c.done).length;
  if (days < 14 && open > 0) flags.push(`Deadline in ${days} day${days === 1 ? '' : 's'} with ${open} open item${open === 1 ? '' : 's'}`);
  const recs = a.recommenders.filter((r) => r.status !== 'submitted' && r.dueOn < today);
  if (recs.length) flags.push(`${recs.length} recommendation letter${recs.length === 1 ? '' : 's'} overdue`);
  return [...new Set(flags)];
}

export function getApplications(id: string): ApplicationsBundle {
  const today = demoToday();
  return {
    applications: learnerRecords<Application>('applications', id)
      .map((a) => ({ ...a, riskFlags: riskFlagsFor(a, today) }))
      .sort((a, b) => a.deadline.localeCompare(b.deadline)),
    shortlist: learnerRecords<ShortlistEntry>('shortlist', id),
    meetings: getMeetingNotes(id),
    finance: learnerRecords<FinanceVisa>('finance', id),
  };
}

/** Applications across a counsellor's students (pipeline view). */
export function getApplicationsPipeline(counsellorId: string): (Application & { studentName: string })[] {
  const today = demoToday();
  return records<Application>('applications')
    .filter((a) => a.counsellorId === counsellorId)
    .map((a) => ({ ...a, riskFlags: riskFlagsFor(a, today), studentName: getStudent(a.learnerId)?.name ?? a.learnerId }))
    .sort((a, b) => a.deadline.localeCompare(b.deadline));
}

export function getApplication(applicationId: string): Application | undefined {
  const a = records<Application>('applications').find((x) => x.id === applicationId);
  return a && { ...a, riskFlags: riskFlagsFor(a, demoToday()) };
}

export function getMeetingNotes(id: string, f: { staffId?: string; kind?: MeetingNote['kind'] } = {}): MeetingNote[] {
  const isLearner = id.startsWith('lrn_');
  return records<MeetingNote>('meetings')
    .filter((m) => (isLearner ? m.learnerId === id : m.staffId === id) && (!f.staffId || m.staffId === f.staffId) && (!f.kind || m.kind === f.kind))
    .sort((a, b) => b.date.localeCompare(a.date));
}

export function getDocuments(id: string, folder?: DocumentRecord['folder']): DocumentRecord[] {
  return learnerRecords<DocumentRecord>('documents', id)
    .filter((d) => !folder || d.folder === folder)
    .sort((a, b) => b.uploadedUtc.localeCompare(a.uploadedUtc));
}

export function getInvoices(personId: string): Invoice[] {
  return records<Invoice>('invoices')
    .filter((i) => i.learnerId === personId || i.payerId === personId)
    .sort((a, b) => b.issuedUtc.localeCompare(a.issuedUtc));
}

export function getConsents(id: string): Consent[] {
  return learnerRecords<Consent>('consents', id).sort(byTime('grantedUtc'));
}

/** Messages a person can see (learner: their threads; adult: threads they are in). Oldest first. */
export function getMessages(personId: string, f: { learnerId?: string; threadId?: string } = {}): Message[] {
  return records<Message>('messages')
    .filter((m) => m.learnerId === personId || m.from === personId || m.toIds.includes(personId))
    .filter((m) => (!f.learnerId || m.learnerId === f.learnerId) && (!f.threadId || m.threadId === f.threadId))
    .sort(byTime('sentUtc'));
}

export function getComments(targetType: Comment['targetType'], targetId: string): Comment[] {
  return records<Comment>('comments').filter((c) => c.targetType === targetType && c.targetId === targetId).sort(byTime('createdUtc'));
}

export function getApprovals(f: { learnerId?: string; targetId?: string; kind?: Approval['kind'] } = {}): Approval[] {
  return records<Approval>('approvals')
    .filter((a) => (!f.learnerId || a.learnerId === f.learnerId) && (!f.targetId || a.targetId === f.targetId) && (!f.kind || a.kind === f.kind))
    .sort(byTime('utc'));
}

// ------------------------------------------------------------------ parent

export function getChildren(parentId: string): ChildSummary[] {
  const adult = getAdult(parentId);
  const ids = adult?.learnerIds ?? getPersona(parentId)?.linkedLearnerIds ?? [];
  const today = demoToday();
  const ws = weekStartOf(today);
  return ids
    .map(getStudent)
    .filter((s): s is Student => !!s)
    .map((student) => {
      const gaps = getGaps(student.id, { status: 'open' });
      const tasks = getTasks(student.id, undefined, { range: [ws, addDaysLocal(ws, 6)] });
      const alr = getAlr(student.id);
      return {
        student,
        band: student.band,
        lrs: alr.overall.LRS,
        openGaps: gaps.length,
        hoursToClose: Math.round(gaps.reduce((a, g) => a + g.hoursToClose, 0) * 10) / 10,
        nextSession: getSessions(student.id, { from: demoNow(), status: 'scheduled' })[0],
        tasksThisWeek: { done: tasks.filter((t) => t.status === 'done').length, total: tasks.length },
      };
    });
}

// ------------------------------------------------------------------ teacher

export function getSections(teacherId: string): Section[] {
  return records<Section>('sections').filter((s) => s.teacherId === teacherId).sort((a, b) => a.name.localeCompare(b.name));
}

export function getSection(sectionId: string): Section | undefined {
  return records<Section>('sections').find((s) => s.id === sectionId);
}

/** Students × subtopics mastery for a section (persona learners live, background learners from the class file). */
export function getSectionHeatmap(sectionId: string, opts: { chapterId?: string } = {}): SectionHeatmap | undefined {
  const section = getSection(sectionId);
  if (!section) return undefined;
  const subj = getSubject(section.subjectId);
  const chapters = new Map((subj?.chapters ?? []).map((c) => [c.id, c]));
  const subtopics = (subj?.subtopics ?? [])
    .filter((s) => !opts.chapterId || s.chapterId === opts.chapterId)
    .map((s) => ({ id: s.id, name: s.name, chapterId: s.chapterId, chapterName: chapters.get(s.chapterId)?.name ?? '', order: (chapters.get(s.chapterId)?.order ?? 0) * 100 + s.order }))
    .sort((a, b) => a.order - b.order);
  const bg = new Map(section.background.map((b) => [b.id, b]));
  const clusters = new Map<string, Set<string>>();
  const addCluster = (sub: string, code: string, lid: string) => {
    const k = `${sub}|${code}`;
    if (!clusters.has(k)) clusters.set(k, new Set());
    clusters.get(k)!.add(lid);
  };
  const subIds = new Set(subtopics.map((s) => s.id));
  const rows = section.learnerIds.map((lid) => {
    const b = bg.get(lid);
    const cells: SectionHeatmap['rows'][number]['cells'] = {};
    if (b) {
      for (const s of subtopics) cells[s.id] = b.mastery[s.id] ?? null;
      for (const g of b.gaps) if (g.status !== 'closed' && subIds.has(g.subtopicId)) addCluster(g.subtopicId, g.code, lid);
      return { learnerId: lid, name: b.name, isPersona: false, cells };
    }
    const m = new Map(getMastery(lid, section.subjectId).map((x) => [x.subtopicId, x]));
    for (const s of subtopics) {
      const x = m.get(s.id);
      cells[s.id] = x ? { level: x.level, pMastery: x.pMastery, lastTestedUtc: x.lastTestedUtc } : null;
    }
    for (const g of getGaps(lid, { status: 'open', subjectId: section.subjectId })) if (subIds.has(g.subtopicId)) addCluster(g.subtopicId, g.code, lid);
    return { learnerId: lid, name: getStudent(lid)?.name ?? lid, isPersona: true, cells };
  });
  const { background: _bg, ...rest } = section;
  return {
    section: rest,
    subtopics,
    rows,
    clusters: [...clusters.entries()]
      .map(([k, set]) => ({ subtopicId: k.split('|')[0], code: k.split('|')[1] as GapRecord['code'], learnerIds: [...set] }))
      .sort((a, b) => b.learnerIds.length - a.learnerIds.length || a.subtopicId.localeCompare(b.subtopicId)),
  };
}

// ------------------------------------------------------------------ counsellor / mentor

export function getCaseload(staffId: string): CaseloadEntry[] {
  const staff = getAdult(staffId);
  const ids = staff?.learnerIds ?? getPersona(staffId)?.linkedLearnerIds ?? (getPersona(staffId)?.role === 'counsellor' ? listStudents().map((s) => s.id) : []);
  const today = demoToday();
  return ids
    .map(getStudent)
    .filter((s): s is Student => !!s)
    .map((student) => {
      const flags: RiskFlag[] = [];
      const requests = getTimetableRequests({ learnerId: student.id, status: 'pending' });
      if (requests.length) flags.push({ kind: 'request_pending', severity: 'medium', text: `${requests.length} timetable request${requests.length === 1 ? '' : 's'} waiting`, refId: requests[0].id });
      for (const a of getApplications(student.id).applications) for (const t of a.riskFlags ?? []) flags.push({ kind: 'deadline', severity: 'high', text: t, refId: a.id });
      const wellbeing = getEvents(student.id, { type: 'wellbeing_checkin' }).pop();
      if (wellbeing && (wellbeing.payload?.flag as boolean | undefined)) flags.push({ kind: 'wellbeing', severity: 'high', text: 'Wellbeing check-in flagged', refId: wellbeing.eventId });
      const plan = getCurrentPlan(student.id);
      if (plan?.plan.paidTuition.recommended) flags.push({ kind: 'paid_rule', severity: 'medium', text: plan.plan.paidTuition.reason });
      const density = getEvidenceDensity(student.id);
      const sparse = density.filter((d) => d.filled / Math.max(1, d.parameters) < 0.2).length;
      if (sparse >= 6) flags.push({ kind: 'data_sparsity', severity: 'low', text: `${sparse} of 12 profile sections have little evidence` });
      const blanks = getGaps(student.id, { status: 'open' }).filter((g) => g.code === 'G10').length;
      if (blanks) flags.push({ kind: 'engagement', severity: 'medium', text: `${blanks} engagement gap${blanks === 1 ? '' : 's'} (blanks, skipped work)` });
      const sessions = getSessions(student.id).filter((s) => s.hostId === staffId);
      const nextSession = sessions.find((s) => s.status === 'scheduled' && s.startUtc >= demoNow());
      return {
        student,
        focus: staff?.focus ?? 'academic_wellbeing',
        flags,
        needsYouToday: flags.some((f) => f.severity === 'high') || requests.length > 0 || (!!nextSession && localDateOf(nextSession.startUtc) === today),
        pendingRequests: requests.length,
        nextSession,
        lastMeeting: getMeetingNotes(student.id, { staffId })[0],
        openGaps: getGaps(student.id, { status: 'open' }).length,
      };
    })
    .sort((a, b) => Number(b.needsYouToday) - Number(a.needsYouToday) || b.flags.length - a.flags.length || a.student.name.localeCompare(b.student.name));
}

// ------------------------------------------------------------------ tutor

export function getTutorWorkspace(tutorId: string): TutorWorkspace | undefined {
  const tutor = getTutor(tutorId);
  if (!tutor) return undefined;
  const bookings = getBookings(tutorId);
  const sessions = getSessions(tutorId);
  const learnerIds = [...new Set([...bookings.filter((b) => b.status !== 'declined' && b.status !== 'cancelled').map((b) => b.learnerId), ...sessions.flatMap((s) => s.learnerIds ?? [s.learnerId])])];
  const students = learnerIds.map((lid) => {
    const st = getStudent(lid);
    const mine = bookings.filter((b) => b.learnerId === lid);
    const ss = sessions.filter((s) => (s.learnerIds ?? [s.learnerId]).includes(lid));
    const since = [...mine.map((b) => b.requestedAt), ...ss.map((s) => s.startUtc)].sort()[0] ?? demoNow();
    const last = [...ss.filter((s) => s.startUtc <= demoNow()).map((s) => s.startUtc)].sort().pop() ?? since;
    return {
      learnerId: lid,
      name: st?.name ?? getPersona(lid)?.name ?? lid,
      grade: st?.grade ?? 9,
      board: st?.board ?? 'cbse',
      goal: st?.goal ?? '',
      subjectIds: [...new Set([...mine.map((b) => b.subjectId), ...ss.map((s) => s.subjectId)].filter((x): x is string => !!x))],
      sinceUtc: since,
      lastActivityUtc: last,
      openGaps: getGaps(lid, { status: 'open' }).length,
      student: st,
    };
  });
  const rate = (tutor as Tutor & { platformFeeRate?: number }).platformFeeRate ?? 0.15;
  const byMonth = new Map<string, { sessions: number; gross: number }>();
  for (const s of sessions.filter((x) => x.status === 'completed' && (x.rateInr ?? 0) > 0)) {
    const m = s.startUtc.slice(0, 7);
    const cur = byMonth.get(m) ?? { sessions: 0, gross: 0 };
    cur.sessions += 1;
    cur.gross += Math.round(((s.rateInr ?? 0) * s.minutes) / 60);
    byMonth.set(m, cur);
  }
  return {
    tutor,
    students,
    bookings,
    sessions,
    assignments: records<Assignment>('assignments').filter((a) => a.tutorId === tutorId),
    messages: records<Message>('messages').filter((m) => m.tutorId === tutorId || m.from === tutorId || m.toIds.includes(tutorId)).sort(byTime('sentUtc')),
    notes: records<TutorNote>('tutorNotes').filter((n) => n.tutorId === tutorId).sort(byTime('createdUtc')),
    payouts: records<Payout>('payouts').filter((p) => p.tutorId === tutorId).sort(byTime('paidOn')),
    earnings: [...byMonth.entries()].sort().map(([month, v]) => ({ month, sessions: v.sessions, grossInr: v.gross, platformFeeInr: Math.round(v.gross * rate), netInr: v.gross - Math.round(v.gross * rate) })),
  };
}

/** Persona picker list (index.json plus fixture people). Re-exported for convenience. */
export { listPersonas, getPersona };
