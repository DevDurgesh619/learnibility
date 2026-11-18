'use server';
/**
 * Application-support writes (W2-A). Every write goes through the demo store as an overlay record, so
 * "Reset demo" undoes it. Student actions only touch the signed-in student's own records; counsellor
 * actions only touch applications where they are the counsellor; parents never write here.
 */
import { revalidatePath } from 'next/cache';
import { aiPrePass, extractActionItems } from '@/components/applications/ai';
import { fitAll, type FitProfile } from '@/components/applications/fit';
import { latestVersion, qaPassed, STATUS_ORDER } from '@/components/applications/logic';
import { DEMO_NOW, DEMO_NOW_ISO } from '@/lib/demo-clock';
import { listUniversities } from '@/lib/data/catalogue';
import type { Application, ApplicationStatus, Approval, Essay, EssayComment, MeetingNote, ShortlistEntry, Task } from '@/lib/data/types';
import { currentPersona } from '@/lib/session';
import { getApplication, getApplications, getMeetingNotes, getStudent } from '@/lib/data';
import { newId as coreId, nowStamp, putRecord, recomputeLearner, removeRecord } from '@/lib/actions/core';
import type { ProfileValue } from '@/lib/types';

const nowIso = () => nowStamp();
const today = () => DEMO_NOW_ISO.slice(0, 10);
const newId = coreId;

type Who = { id: string; role: 'student' | 'counsellor' };

async function me(): Promise<Who> {
  const p = await currentPersona();
  if (!p || (p.role !== 'student' && p.role !== 'counsellor')) throw new Error('Only students and counsellors can change applications.');
  return { id: p.id, role: p.role };
}

function loadApp(applicationId: string, who: Who): Application {
  const app = getApplication(applicationId);
  if (!app) throw new Error('Application not found.');
  if (who.role === 'student' && app.learnerId !== who.id) throw new Error('Not your application.');
  if (who.role === 'counsellor' && app.counsellorId !== who.id) throw new Error('Not in your caseload.');
  return app;
}

function saveApp(app: Application) {
  const clean = { ...app, updatedUtc: nowIso() };
  delete clean.riskFlags;
  putRecord('applications', clean);
}

function refresh() {
  for (const p of ['/student/universities', '/student/applications', '/counsellor/applications', '/counsellor/draft-reviews', '/parent/applications', '/student', '/student/timetable']) {
    revalidatePath(p, 'layout');
  }
}

function addTask(t: Omit<Task, 'id' | 'createdUtc' | 'status'>): Task {
  const task: Task = { ...t, id: newId('tsk'), status: 'todo', createdUtc: nowIso() };
  putRecord('tasks', task);
  return task;
}

// ------------------------------------------------------------------ shortlist and status

export async function toggleShortlist(universityId: string, programmeId?: string, fitGroup?: ShortlistEntry['fitGroup']) {
  const who = await me();
  if (who.role !== 'student') throw new Error('Students shortlist.');
  const existing = getApplications(who.id).shortlist.find((s) => s.universityId === universityId);
  if (existing) {
    removeRecord('shortlist', `${existing.learnerId}:${existing.universityId}:${existing.programmeId ?? ''}`, who.id);
  } else {
    putRecord('shortlist', { learnerId: who.id, universityId, programmeId, fitGroup, savedUtc: nowIso() } satisfies ShortlistEntry);
  }
  refresh();
}

/** Paid: add a university to the applications board (PDF 7b "Shortlist" adds to 7c). */
export async function addToBoard(universityId: string, programmeId: string) {
  const who = await me();
  if (who.role !== 'student') throw new Error('Students add applications.');
  const mine = getApplications(who.id).applications;
  if (mine.some((a) => a.universityId === universityId && a.programmeId === programmeId)) return;
  const uni = listUniversities().find((u) => u.id === universityId);
  if (!uni) throw new Error('Unknown university.');
  const profile = await fitProfileFor(who.id);
  const fit = fitAll([uni], profile);
  const band = (['reach', 'target', 'safe'] as const).find((b) => fit[b].length) ?? 'target';
  const { mainRoute } = await import('@/components/applications/fit');
  const route = mainRoute(uni);
  const student = getStudent(who.id);
  const counsellorId = mine[0]?.counsellorId ?? student?.counsellorIds?.[0] ?? 'csl_farah_siddiqui';
  const req = route?.requirements;
  const checklist: Application['checklist'] = [
    { id: newId('chk'), title: 'Transcript and predicted grades', kind: 'document', done: false },
    ...(req?.ielts ? [{ id: newId('chk'), title: `English test (IELTS ${req.ielts}+)`, kind: 'test_score' as const, done: false }] : []),
    ...(req?.testPolicy === 'required' ? [{ id: newId('chk'), title: 'SAT score report', kind: 'test_score' as const, done: false }] : []),
    ...(req?.essays ?? []).map((e) => ({ id: newId('chk'), title: e.prompt.split(':')[0]!.slice(0, 60), kind: 'essay' as const, done: false })),
    ...(req?.recommendations ? [{ id: newId('chk'), title: req.recommendations > 1 ? `${req.recommendations} recommendation letters` : 'School reference', kind: 'recommendation' as const, done: false }] : []),
    { id: newId('chk'), title: 'Application form completed', kind: 'form', done: false },
    { id: newId('chk'), title: req?.applicationFeeInr ? `Application fee (₹${new Intl.NumberFormat('en-IN').format(req.applicationFeeInr)})` : 'Application fee', kind: 'fee', done: false },
  ];
  const app: Application = {
    id: newId('app'), learnerId: who.id, universityId, programmeId, routeType: route?.type ?? 'regular', status: 'shortlisted', fitGroup: band,
    deadline: route?.deadline.value ?? today(), counsellorId, checklist, recommenders: [],
    essays: (req?.essays ?? []).map((e) => ({ id: newId('ess'), prompt: e.prompt, wordLimit: e.wordLimit, status: 'drafting', versions: [{ version: 1, text: '', createdAt: nowIso() }], comments: [] })),
    updatedUtc: nowIso(),
  };
  putRecord('applications', app);
  refresh();
}

export async function moveApplication(applicationId: string, status: ApplicationStatus) {
  const who = await me();
  const app = loadApp(applicationId, who);
  if (!STATUS_ORDER.includes(status)) throw new Error('Unknown status.');
  if (status === 'submitted' && !qaPassed(app, DEMO_NOW)) throw new Error('Finish the QA check before submitting.');
  if (status === 'decision' && who.role !== 'counsellor') throw new Error('Your counsellor records decisions.');
  saveApp({ ...app, status });
  refresh();
}

export async function markSubmitted(applicationId: string) {
  return moveApplication(applicationId, 'submitted');
}

export async function recordDecision(applicationId: string, decision: NonNullable<Application['decision']>) {
  const who = await me();
  if (who.role !== 'counsellor') throw new Error('Counsellors record decisions.');
  const app = loadApp(applicationId, who);
  saveApp({ ...app, status: 'decision', decision });
  refresh();
}

export async function toggleChecklistItem(applicationId: string, itemId: string) {
  const who = await me();
  const app = loadApp(applicationId, who);
  const checklist = app.checklist.map((c) => (c.id === itemId ? { ...c, done: !c.done } : c));
  // Ticking the first item moves a shortlisted application into document collection.
  const status: ApplicationStatus = app.status === 'shortlisted' && checklist.some((c) => c.done) ? 'collecting_documents' : app.status;
  saveApp({ ...app, checklist, status });
  refresh();
}

export async function updateRecommender(applicationId: string, recommenderId: string, status: Application['recommenders'][number]['status']) {
  const who = await me();
  const app = loadApp(applicationId, who);
  const recommenders = app.recommenders.map((r) => (r.id === recommenderId ? { ...r, status } : r));
  // A submitted reference ticks the matching checklist item.
  const allIn = recommenders.every((r) => r.status === 'submitted');
  const checklist = app.checklist.map((c) => (c.kind === 'recommendation' ? { ...c, done: allIn } : c));
  saveApp({ ...app, recommenders, checklist });
  refresh();
}

export async function requestRecommender(applicationId: string, name: string, role: string, dueOn: string) {
  const who = await me();
  const app = loadApp(applicationId, who);
  if (!name.trim()) return;
  saveApp({ ...app, recommenders: [...app.recommenders, { id: newId('rec'), name: name.trim(), role: role.trim() || 'Teacher', status: 'requested', requestedOn: today(), dueOn: dueOn || today() }] });
  refresh();
}

// ------------------------------------------------------------------ essays

async function loadEssay(essayId: string, who: Who): Promise<{ app: Application; essay: Essay }> {
  const pool = who.role === 'student' ? getApplications(who.id).applications : (await import('@/lib/data')).getApplicationsPipeline(who.id);
  for (const a of pool) {
    const essay = a.essays.find((e) => e.id === essayId);
    if (essay) return { app: loadApp(a.id, who), essay };
  }
  throw new Error('Essay not found.');
}

function saveEssay(app: Application, essay: Essay) {
  const essays = app.essays.map((e) => (e.id === essay.id ? essay : e));
  const checklist = app.checklist.map((c) => (c.kind === 'essay' && app.essays.length === 1 ? { ...c, done: essay.status === 'final' } : c));
  saveApp({ ...app, essays, checklist });
}

/** Saves a new version. Comments stay on the version they were written on. */
export async function saveEssayVersion(essayId: string, text: string) {
  const who = await me();
  if (who.role !== 'student') throw new Error('Only the student edits the essay.');
  const { app, essay } = await loadEssay(essayId, who);
  const last = latestVersion(essay);
  if (last.text === text) return { version: last.version };
  // An empty starter version is overwritten instead of kept.
  const versions = last.text.trim() === '' ? essay.versions.map((v) => (v.version === last.version ? { ...v, text, createdAt: nowIso() } : v)) : [...essay.versions, { version: last.version + 1, text, createdAt: nowIso() }];
  const next: Essay = { ...essay, versions, status: essay.status === 'final' ? 'drafting' : essay.status };
  saveEssay(app, next);
  refresh();
  return { version: latestVersion(next).version };
}

export async function addEssayComment(essayId: string, input: { text: string; anchor?: EssayComment['anchor']; parentId?: string }) {
  const who = await me();
  const { app, essay } = await loadEssay(essayId, who);
  if (!input.text.trim()) return;
  const parent = input.parentId ? essay.comments.find((c) => c.id === input.parentId) : undefined;
  const c: EssayComment = {
    id: newId('cmt'), version: parent?.version ?? latestVersion(essay).version, authorId: who.id, kind: 'human',
    anchor: parent ? undefined : input.anchor, text: input.text.trim(), resolved: false, createdAt: nowIso(), parentId: parent?.id,
  };
  saveEssay(app, { ...essay, comments: [...essay.comments, c] });
  refresh();
}

export async function setCommentResolved(essayId: string, commentId: string, resolved: boolean) {
  const who = await me();
  const { app, essay } = await loadEssay(essayId, who);
  saveEssay(app, { ...essay, comments: essay.comments.map((c) => (c.id === commentId || c.parentId === commentId ? { ...c, resolved } : c)) });
  refresh();
}

/** Simulated AI pre-pass on the latest version: replaces earlier open AI comments on that version. */
export async function runAiPrePass(essayId: string) {
  const who = await me();
  const { app, essay } = await loadEssay(essayId, who);
  const v = latestVersion(essay);
  const { comments, summary } = aiPrePass(v.text, essay.prompt, essay.wordLimit);
  const kept = essay.comments.filter((c) => !(c.kind === 'ai' && c.version === v.version && !c.resolved));
  const added: EssayComment[] = comments.map((c) => ({ id: newId('cmt'), version: v.version, authorId: null, kind: 'ai', anchor: c.anchor, text: c.text, resolved: false, createdAt: nowIso() }));
  saveEssay(app, { ...essay, comments: [...kept, ...added] });
  refresh();
  return { summary, count: added.length };
}

export async function sendEssayForReview(essayId: string) {
  const who = await me();
  const { app, essay } = await loadEssay(essayId, who);
  saveEssay(app, { ...essay, status: 'in_review' });
  refresh();
}

/** Counsellor: approve as final, or send back to the student with the comments. */
export async function reviewEssay(essayId: string, verdict: 'final' | 'return') {
  const who = await me();
  if (who.role !== 'counsellor') throw new Error('Counsellors review essays.');
  const { app, essay } = await loadEssay(essayId, who);
  saveEssay(app, { ...essay, status: verdict === 'final' ? 'final' : 'drafting' });
  refresh();
}

// ------------------------------------------------------------------ meetings

function findMeeting(meetingId: string, who: Who): MeetingNote | undefined {
  if (who.role === 'student') return getMeetingNotes(who.id).find((m) => m.id === meetingId);
  return getMeetingNotes(who.id).find((m) => m.id === meetingId);
}

/** Meeting intelligence: turn a meeting's open action items into the student's timetable tasks. */
export async function actionItemsToTasks(meetingId: string) {
  const who = await me();
  const m = findMeeting(meetingId, who);
  if (!m) throw new Error('Meeting not found.');
  if (who.role === 'student' && m.learnerId !== who.id) throw new Error('Not your meeting.');
  const actionItems = m.actionItems.map((a) => {
    if (a.taskId || a.done) return a;
    const t = addTask({ learnerId: m.learnerId, title: a.title, kind: 'action_item', dueDate: a.dueOn, source: 'meeting', createdBy: m.staffId, minutes: 30, refId: m.id, href: '/student/applications/meetings', detail: `From your ${m.kind} meeting on ${m.date}` });
    return { ...a, taskId: t.id };
  });
  putRecord('meetings', { ...m, actionItems });
  recomputeLearner(m.learnerId, { reason: 'task_assigned' });
  refresh();
}

/** Counsellor: save a meeting note; action items are extracted from the notes and become tasks. */
export async function saveMeetingNote(learnerId: string, input: { summary: string; notes: string; decisions: string; items?: { title: string; dueOn: string }[] }) {
  const who = await me();
  if (who.role !== 'counsellor') throw new Error('Counsellors write meeting notes.');
  const first = getStudent(learnerId)?.firstName ?? learnerId.split('_')[1] ?? '';
  const items = input.items?.length ? input.items : extractActionItems(input.notes, first, today());
  const m: MeetingNote = {
    id: newId('mtg'), learnerId, staffId: who.id, date: today(), kind: 'applications', tier: 'T1',
    summary: input.summary.trim() || input.notes.trim().split('\n')[0]!.slice(0, 240),
    decisions: input.decisions.split('\n').map((d) => d.replace(/^[-*•]\s*/, '').trim()).filter(Boolean),
    actionItems: items.map((i) => ({ id: newId('ai'), title: i.title, dueOn: i.dueOn })),
  };
  putRecord('meetings', m);
  await actionItemsToTasksFor(m);
  refresh();
  return m.id;
}

async function actionItemsToTasksFor(m: MeetingNote) {
  const actionItems = m.actionItems.map((a) => {
    const t = addTask({ learnerId: m.learnerId, title: a.title, kind: 'action_item', dueDate: a.dueOn, source: 'meeting', createdBy: m.staffId, minutes: 30, refId: m.id, href: '/student/applications/meetings', detail: `From your ${m.kind} meeting on ${m.date}` });
    return { ...a, taskId: t.id };
  });
  putRecord('meetings', { ...m, actionItems });
  recomputeLearner(m.learnerId, { reason: 'task_assigned' });
}

export async function toggleActionItem(meetingId: string, itemId: string) {
  const who = await me();
  const m = findMeeting(meetingId, who);
  if (!m || (who.role === 'student' && m.learnerId !== who.id)) throw new Error('Meeting not found.');
  putRecord('meetings', { ...m, actionItems: m.actionItems.map((a) => (a.id === itemId ? { ...a, done: !a.done } : a)) });
  refresh();
}

// ------------------------------------------------------------------ finance and visa

export async function toggleFinanceItem(universityId: string, block: 'aid' | 'visa' | 'visaDocs', index: number) {
  const who = await me();
  if (who.role !== 'student') throw new Error('Students update their checklist.');
  const f = getApplications(who.id).finance.find((x) => x.universityId === universityId);
  if (!f) return;
  putRecord('finance', { ...f, [block]: f[block].map((x, i) => (i === index ? { ...x, done: !x.done } : x)) });
  refresh();
}

// ------------------------------------------------------------------ fit profile and plan

async function fitProfileFor(learnerId: string): Promise<FitProfile> {
  const { fitInputs } = await import('@/components/applications/data');
  return fitInputs(learnerId).profile;
}

/** PDF 6e: save fit inputs as profile values (source M2, the student's own form). */
export async function saveFitProfile(form: FormData) {
  const who = await me();
  if (who.role !== 'student') throw new Error('Students edit their own profile.');
  const put = (paramId: string, value: unknown, tier: ProfileValue['tier'] = 'T1') => {
    if (value === undefined || value === null || value === '') return;
    putRecord('profile', { learnerId: who.id, paramId, value, source: 'M2', asOfUtc: nowIso(), confidence: 'medium', tier } satisfies ProfileValue);
  };
  const academic = String(form.get('academic') ?? '').trim();
  if (academic) put('p16', /^(A\*|[A-E]){2,4}$/i.test(academic) ? academic.toUpperCase() : /^ib/i.test(academic) ? academic.toUpperCase() : Number(academic.replace(/[^\d.]/g, '')) || academic);
  const sat = String(form.get('sat') ?? '').trim();
  if (sat) put('p25', [{ exam: 'SAT', score: Number(sat.replace(/\D/g, '')) || sat }]);
  const ielts = String(form.get('ielts') ?? '').trim();
  if (ielts) put('p212', Number(ielts) || ielts);
  const activities = String(form.get('activities') ?? '');
  if (activities) put('p268', activities);
  const essay = String(form.get('essay') ?? '').trim();
  if (essay) put('p267', essay.length > 1200 ? 'strong' : essay.length > 400 ? 'average' : 'weak');
  const countries = form.getAll('countries').map(String).filter(Boolean);
  if (countries.length) put('p231', countries);
  refresh();
}

/** Demo upgrade to Application Support (no payment). */
export async function upgradeToApplicationSupport() {
  const who = await me();
  if (who.role !== 'student') throw new Error('Students upgrade.');
  const s = getStudent(who.id);
  if (s) putRecord('student', { ...s, plan: 'application_support' });
  putRecord('approvals', { id: newId('apr'), learnerId: who.id, kind: 'plan_upgrade', targetId: 'application_support', byId: who.id, decision: 'approved', utc: nowIso(), note: 'Demo upgrade, no payment taken' } satisfies Approval);
  // Saved universities carry over to the board.
  for (const e of getApplications(who.id).shortlist) {
    if (e.programmeId) await addToBoard(e.universityId, e.programmeId);
  }
  refresh();
}
