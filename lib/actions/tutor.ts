'use server';

/**
 * W2-T tutor actions (tutor HTML 2a to 8e): home layout, session reports with homework, assignments,
 * evaluation, messages, private notes and profile edits. Learner-facing writes call recomputeLearner.
 */
import { cookies } from 'next/headers';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { TUTOR_HOME_COOKIE } from '@/components/tutor/constants';
import { appendEvent, newId, nowStamp, putRecord, recomputeLearner } from '@/lib/actions/core';
import { addDaysLocal, demoToday, getTasks, getTutorWorkspace } from '@/lib/data';
import type { Message, Session, Task, TutorNote } from '@/lib/data/types';
import { currentPersona } from '@/lib/session';
import type { TutorAssignment, TutorQuestion } from '@/components/tutor/model';

/** Tutor Home ships both wireframe options (2a teaching-first, 2b marketplace-first) until one is picked. */
export async function setHomeLayout(data: FormData) {
  const v = data.get('layout') === 'b' ? 'b' : 'a';
  const persona = await currentPersona();
  if (persona?.role === 'tutor') await saveSettings(persona.id, { homeLayout: v });
  (await cookies()).set(TUTOR_HOME_COOKIE, v, { path: '/', maxAge: 60 * 60 * 24 * 365, sameSite: 'lax' });
  revalidatePath('/tutor');
  redirect('/tutor');
}

// ------------------------------------------------------------------ helpers

/** Writes the tutor's settings record to the demo store when the `tutorSettings` collection exists (else cookie only). */
async function saveSettings(tutorId: string, patch: { homeLayout?: 'a' | 'b'; prefs?: object }) {
  const { hasSettingsStore, storedSettings, SETTINGS } = await import('@/components/tutor/settings');
  if (!hasSettingsStore()) return;
  putRecord(SETTINGS as Parameters<typeof putRecord>[0], { ...(storedSettings(tutorId) ?? { id: tutorId }), ...patch });
}


async function tutorFor(learnerId?: string) {
  const persona = await currentPersona();
  if (!persona || persona.role !== 'tutor') throw new Error('Tutors only');
  const ws = getTutorWorkspace(persona.id);
  if (!ws) throw new Error('No tutor workspace');
  if (learnerId && !ws.students.some((s) => s.learnerId === learnerId)) throw new Error('Not your student');
  return { tutorId: persona.id, ws, tutorName: ws.tutor.firstName };
}

function touch(learnerId?: string) {
  revalidatePath('/tutor', 'layout');
  revalidatePath('/student', 'layout');
  if (learnerId) revalidatePath(`/tutor/students/${learnerId}`, 'layout');
}

function message(learnerId: string, tutorId: string, from: string, text: string): Message {
  return { id: newId('msg'), threadId: `${learnerId}:${tutorId}`, learnerId, from, toIds: from === 'system' ? [learnerId, tutorId] : [learnerId], text, sentUtc: nowStamp(), tutorId, readBy: [tutorId] };
}

const s = (d: FormData, k: string) => String(d.get(k) ?? '').trim();

// ------------------------------------------------------------------ messages and notes (4n, 4o)

export async function sendMessage(data: FormData) {
  const learnerId = s(data, 'learnerId');
  const { tutorId } = await tutorFor(learnerId);
  const text = s(data, 'text').slice(0, 1000);
  if (text) putRecord('messages', message(learnerId, tutorId, tutorId, text));
  touch(learnerId);
}

export async function addNote(data: FormData) {
  const learnerId = s(data, 'learnerId');
  const { tutorId } = await tutorFor(learnerId);
  const text = s(data, 'text').slice(0, 2000);
  if (text) putRecord('tutorNotes', { id: newId('note'), learnerId, tutorId, text, createdUtc: nowStamp(), source: 'manual' } satisfies TutorNote);
  touch(learnerId);
}

// ------------------------------------------------------------------ tasks (4m)

function homeworkTask(learnerId: string, tutorId: string, title: string, dueDate: string, extra: Partial<Task> = {}): Task {
  return { id: newId('task'), learnerId, title, kind: 'homework', dueDate, status: 'todo', source: 'tutor', createdBy: tutorId, createdUtc: nowStamp(), minutes: 30, detail: 'From your tutor', ...extra };
}

export async function addTask(data: FormData) {
  const learnerId = s(data, 'learnerId');
  const { tutorId, tutorName } = await tutorFor(learnerId);
  const title = s(data, 'title');
  if (!title) return;
  const due = s(data, 'dueDate') || addDaysLocal(demoToday(), 2);
  const t = homeworkTask(learnerId, tutorId, title, due, { detail: s(data, 'priority') === 'urgent' ? 'Urgent · from your tutor' : 'From your tutor' });
  putRecord('tasks', t);
  putRecord('messages', message(learnerId, tutorId, 'system', `${tutorName} added a task: ${title}`));
  appendEvent(learnerId, { sourceMethod: 'M15', type: 'task_assigned', payload: { taskId: t.id, by: tutorId } });
  recomputeLearner(learnerId, { reason: 'task_assigned' });
  touch(learnerId);
}

export async function remindTask(data: FormData) {
  const learnerId = s(data, 'learnerId');
  const { tutorId } = await tutorFor(learnerId);
  const task = getTasks(learnerId).find((t) => t.id === s(data, 'taskId'));
  if (task) putRecord('messages', message(learnerId, tutorId, tutorId, `Reminder: “${task.title}” was due ${task.dueDate}. Can you finish it today?`));
  touch(learnerId);
}

// ------------------------------------------------------------------ assignments (4h-4l)

/** 4k "Assign to …": the verified draft becomes an assignment and a test task on the student's Today and timetable. */
export async function assignTest(data: FormData) {
  const learnerId = s(data, 'learnerId');
  const { tutorId, tutorName } = await tutorFor(learnerId);
  const questions = JSON.parse(s(data, 'questions') || '[]') as TutorQuestion[];
  const title = s(data, 'title') || 'Practice test';
  const due = s(data, 'dueOn') || addDaysLocal(demoToday(), 2);
  if (!questions.length) throw new Error('No questions');
  const id = newId('asg');
  const bankIds = questions.filter((q) => !q.id.startsWith('tq_')).map((q) => q.id);
  const task: Task = {
    id: newId('task'), learnerId, title: `Complete ${title}`, kind: 'test', dueDate: due, status: 'todo', source: 'tutor', createdBy: tutorId, createdUtc: nowStamp(),
    minutes: Number(s(data, 'timeLimitMin')) || 30, subjectId: questions[0]!.subtopicId.replace(/-ch\d+-st\d+$/, ''), refId: id,
    questionIds: bankIds.length === questions.length ? bankIds : undefined, detail: `Assigned by ${tutorName}`,
  };
  const a: TutorAssignment = {
    id, learnerId, tutorId, title, subtopicIds: [...new Set(questions.map((q) => q.subtopicId))], questionIds: questions.map((q) => q.id), status: 'assigned', dueOn: due, taskId: task.id,
    questions, source: (s(data, 'source') as TutorAssignment['source']) || 'ai', evaluation: s(data, 'evaluation') === 'manual' ? 'manual' : 'ai_review', timeLimitMin: Number(s(data, 'timeLimitMin')) || 30,
  };
  putRecord('assignments', a);
  putRecord('tasks', task);
  putRecord('messages', message(learnerId, tutorId, 'system', `${tutorName} assigned ${title} · due ${due}`));
  appendEvent(learnerId, { sourceMethod: 'M15', type: 'task_assigned', payload: { taskId: task.id, assignmentId: id, by: tutorId } });
  recomputeLearner(learnerId, { reason: 'task_assigned' });
  touch(learnerId);
  redirect(`/tutor/students/${learnerId}/assignments/${id}/assigned`);
}

/** 4h: save tutor scores/feedback; publish when nothing is left to review. */
export async function saveEvaluation(data: FormData) {
  const learnerId = s(data, 'learnerId');
  const { ws, tutorId, tutorName } = await tutorFor(learnerId);
  const a = ws.assignments.find((x) => x.id === s(data, 'assignmentId') && x.learnerId === learnerId) as TutorAssignment | undefined;
  if (!a) throw new Error('Assignment not found');
  const per = (a.perQuestion ?? []).map((p) => {
    const sc = data.get(`score_${p.questionId}`);
    const fb = data.get(`fb_${p.questionId}`);
    if (sc === null && fb === null) return p;
    return { ...p, tutorScore: sc === null || sc === '' ? p.tutorScore : Number(sc), tutorFeedback: fb === null ? p.tutorFeedback : String(fb), needsReview: false };
  });
  const qs = new Map((a.questions ?? []).map((q) => [q.id, q]));
  const max = (a.questions ?? []).reduce((t, q) => t + q.marks, 0) || a.maxScore || per.length;
  const score = per.reduce((t, p) => t + (p.tutorScore ?? p.aiScore ?? (p.correct ? qs.get(p.questionId)?.marks ?? 1 : 0)), 0);
  const publish = data.get('intent') === 'publish';
  const feedback = a.feedback ? { ...a.feedback, weakness: s(data, 'weakness') || a.feedback.weakness, strength: s(data, 'strength') || a.feedback.strength } : a.feedback;
  const next: TutorAssignment = { ...a, perQuestion: per, score, maxScore: max, feedback, status: publish ? 'completed' : 'reviewed', ...(publish ? { publishedUtc: nowStamp() } : {}) };
  putRecord('assignments', next);
  if (publish) {
    putRecord('messages', message(learnerId, tutorId, 'system', `${tutorName} published your result for ${a.title}: ${score}/${max}`));
    appendEvent(learnerId, { sourceMethod: 'M11', type: 'assignment_evaluated', payload: { assignmentId: a.id, score, maxScore: max, by: tutorId } });
  }
  touch(learnerId);
  redirect(publish ? `/tutor/students/${learnerId}/learning/${a.id}` : `/tutor/students/${learnerId}/assignments/${a.id}`);
}

// ------------------------------------------------------------------ session report (5e)

/**
 * 5e "Submit report": the session is completed with a report; each homework line becomes a task in every
 * attending student's Today and timetable; private notes go to Notes; next focus moves to the next session.
 */
export async function submitSessionReport(data: FormData) {
  const { ws, tutorId, tutorName } = await tutorFor();
  const sess = ws.sessions.find((x) => x.id === s(data, 'sessionId'));
  if (!sess) throw new Error('Session not found');
  const learners = sess.learnerIds?.length ? sess.learnerIds : [sess.learnerId];
  const topics = data.getAll('topic').map(String).map((x) => x.trim()).filter(Boolean);
  const homework = data.getAll('homework').map(String).map((x) => x.trim()).filter(Boolean);
  const due = s(data, 'dueDate') || addDaysLocal(demoToday(), 2);
  const taskIds: string[] = [];
  for (const lid of learners) {
    // Editing a filed report keeps tasks that are still listed and skips the ones removed, so nothing is duplicated.
    const existing = getTasks(lid).filter((t) => t.refId === sess.id && t.createdBy === tutorId);
    for (const t of existing) if (!homework.includes(t.title) && t.status === 'todo') putRecord('tasks', { ...t, status: 'skipped' });
    for (const h of homework) {
      const same = existing.find((t) => t.title === h);
      if (same) { putRecord('tasks', { ...same, dueDate: due, status: same.status === 'skipped' ? 'todo' : same.status }); taskIds.push(same.id); continue; }
      const t = homeworkTask(lid, tutorId, h, due, { refId: sess.id, subjectId: sess.subjectId, detail: `Homework from ${sess.code ?? 'your session'} with ${tutorName}` });
      putRecord('tasks', t);
      taskIds.push(t.id);
    }
  }
  const notes = s(data, 'notes');
  const nextFocus = s(data, 'nextFocus');
  const report = {
    topics, performance: (s(data, 'performance') || 'getting_there') as 'struggled' | 'getting_there' | 'confident', engagement: (s(data, 'engagement') || 'medium') as 'high' | 'medium' | 'low',
    notes, homeworkTaskIds: taskIds, nextFocus, submittedUtc: nowStamp(),
  };
  putRecord('sessions', { ...sess, status: 'completed', report } satisfies Session);
  const nextSess = ws.sessions.filter((x) => x.status === 'scheduled' && x.startUtc > sess.startUtc && (x.learnerIds ?? [x.learnerId]).some((l) => learners.includes(l))).sort((a, b) => a.startUtc.localeCompare(b.startUtc))[0];
  if (nextSess && nextFocus) putRecord('sessions', { ...nextSess, focus: nextFocus });
  for (const lid of learners) {
    if (notes) putRecord('tutorNotes', { id: newId('note'), learnerId: lid, tutorId, text: notes, createdUtc: nowStamp(), source: 'session_report' } satisfies TutorNote);
    putRecord('messages', message(lid, tutorId, 'system', `${tutorName} ${sess.report ? 'updated' : 'filed'} the report for ${sess.code ?? 'your session'}: ${topics.join(', ') || sess.title}.${homework.length ? ` Homework: ${homework.join('; ')} (due ${due}).` : ''}${nextFocus ? ` Next: ${nextFocus}.` : ''}`));
    appendEvent(lid, { sourceMethod: 'M18', type: 'tutor_session_report', payload: { sessionId: sess.id, tutorId, performance: report.performance, engagement: report.engagement, topics, homeworkTaskIds: taskIds } });
    recomputeLearner(lid, { reason: 'task_assigned' });
  }
  touch(learners[0]);
  redirect(`/tutor/sessions/${sess.id}?filed=1`);
}

/** 5c: save the edited session plan as prep notes. */
export async function savePrep(data: FormData) {
  const { ws } = await tutorFor();
  const sess = ws.sessions.find((x) => x.id === s(data, 'sessionId'));
  if (!sess) throw new Error('Session not found');
  putRecord('sessions', { ...sess, prepNotes: s(data, 'plan') || sess.prepNotes || 'Prepared' });
  touch();
  redirect(`/tutor/sessions/${sess.id}/prep?saved=1`);
}

// ------------------------------------------------------------------ AI test drafts (4j, 4k). Pre-written logic, no live model.

export interface DraftParams { subtopicIds: string[]; count: number; difficulty: 'easy' | 'medium' | 'hard'; type: 'mixed' | 'mcq' | 'numerical' | 'short'; retentionFrom?: string[]; seed?: number }

const DIFF: Record<DraftParams['difficulty'], string[]> = { easy: ['D1', 'D2'], medium: ['D2', 'D3', 'D4'], hard: ['D4', 'D5'] };

/**
 * Builds a draft from the real question bank for the chosen subtopics (difficulty and type filtered), topped up
 * with templated items when the bank for that subject is not generated yet. Flags items worth a second look.
 */
export async function draftTest(p: DraftParams): Promise<(TutorQuestion & { flag?: string })[]> {
  await tutorFor();
  const { getQuestions, getSubtopic } = await import('@/lib/data');
  const want = Math.max(1, Math.min(25, p.count));
  const pool = getQuestions({ subtopicIds: p.subtopicIds, set: 'mastery_bank' })
    .filter((q) => DIFF[p.difficulty].includes(q.difficulty))
    .filter((q) => p.type === 'mixed' || (p.type === 'short' ? ['short', 'explain'].includes(q.type) : q.type === p.type));
  const seed = p.seed ?? 0;
  const rot = pool.length ? seed % pool.length : 0;
  const picked = [...pool.slice(rot), ...pool.slice(0, rot)].slice(0, want).map((q) => ({ id: q.id, type: q.type, subtopicId: q.subtopicId, stem: q.stem, options: q.options ?? null, answer: String(q.answer), markingKey: q.markingKey, marks: q.marks }));
  const retention = (p.retentionFrom ?? []).flatMap((sid) => getQuestions({ subtopicIds: [sid], set: 'mastery_bank' }).slice(seed % 3, (seed % 3) + 1))
    .map((q) => ({ id: q.id, type: q.type, subtopicId: q.subtopicId, stem: q.stem, options: q.options ?? null, answer: String(q.answer), markingKey: q.markingKey, marks: q.marks, flag: 'Retention check' }));
  const out: (TutorQuestion & { flag?: string })[] = [...picked, ...retention].slice(0, want);
  const kinds = p.type === 'mixed' ? ['numerical', 'short', 'mcq'] : [p.type];
  let i = 0;
  while (out.length < want) {
    const sid = p.subtopicIds[i % p.subtopicIds.length]!;
    const name = (getSubtopic(sid)?.name ?? 'this topic').split(/[;:]/)[0]!;
    const kind = kinds[i % kinds.length]!;
    const n = out.length + 1;
    const lvl = p.difficulty === 'hard' ? 'a multi-step' : p.difficulty === 'easy' ? 'a direct' : 'a standard';
    out.push(kind === 'mcq'
      ? { id: `tq_${sid}_${seed}${n}`, type: 'mcq', subtopicId: sid, stem: `Which of these is the correct first step for ${lvl} problem on ${name.toLowerCase()}?`, options: ['Write what is given and what is asked', 'Substitute numbers immediately', 'Guess and check', 'Skip to the formula sheet'], answer: 'Write what is given and what is asked', markingKey: 'Option A', marks: 1, flag: 'Check: possible ambiguity' }
      : kind === 'short'
        ? { id: `tq_${sid}_${seed}${n}`, type: 'short', subtopicId: sid, stem: `In two or three sentences, explain the key idea behind ${name.toLowerCase()} and where students usually go wrong.`, answer: 'Rubric', markingKey: 'Key idea stated (1) · common error named (1) · example (1)', marks: 3 }
        : { id: `tq_${sid}_${seed}${n}`, type: 'numerical', subtopicId: sid, stem: `Solve ${lvl} problem on ${name.toLowerCase()} (question ${n}); show each step.`, answer: 'Tutor to set', markingKey: 'Method (2) · answer (1)', marks: 3, flag: 'Add numbers before assigning' });
    i += 1;
  }
  return out;
}

// ------------------------------------------------------------------ profile, availability, pricing, payout settings (7c, 8a-8e)

/**
 * Merges one settings section into the tutor's prefs cookie (see components/tutor/prefs.ts) and returns to the
 * page with ?saved=1. Fields arrive as JSON in `patch` so each page can post its own shape.
 */
export async function saveTutorPrefs(data: FormData) {
  const { tutorId } = await tutorFor();
  const { prefsCookie } = await import('@/components/tutor/prefs');
  const jar = await cookies();
  const { readPrefs } = await import('@/components/tutor/prefs');
  const current = (await readPrefs(tutorId)) as Record<string, unknown>;
  let patch: Record<string, unknown> = {};
  try { patch = JSON.parse(s(data, 'patch') || '{}'); } catch { patch = {}; }
  for (const [k, v] of data.entries()) if (k.startsWith('f.')) patch[k.slice(2)] = String(v);
  for (const k of data.getAll('list').map(String)) patch[k] = data.getAll(`l.${k}`).map(String);
  if (s(data, 'section') === 'availability') {
    const { BANDS } = await import('@/components/tutor/form-bits');
    const cells = data.getAll('cell').map(String); // "mon:a"
    const days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'];
    const slots: { day: string; start: string; end: string }[] = [];
    for (const d of days) {
      for (const b of BANDS.filter((x) => cells.includes(`${d}:${x.key}`))) {
        const last = slots.at(-1);
        if (last && last.day === d && last.end === b.start) last.end = b.end; else slots.push({ day: d, start: b.start, end: b.end });
      }
    }
    patch.availability = slots;
    patch.maxSessionsPerDay = Number(s(data, 'maxSessionsPerDay')) || 4;
    const from = s(data, 'blockFrom');
    const prev = (current.blocked as { from: string; to: string; label: string }[] | undefined) ?? [];
    const keep = prev.filter((b) => !data.getAll('unblock').map(String).includes(b.from));
    patch.blocked = from ? [...keep, { from, to: s(data, 'blockTo') || from, label: s(data, 'blockLabel') || 'Unavailable' }] : keep;
  }
  if (s(data, 'section') === 'pricing') {
    const n = (k: string) => Math.max(0, Number(s(data, k)) || 0);
    patch.pricing = { oneToOnePerHourInr: n('oneToOne'), groupPerStudentPerHourInr: s(data, 'group') ? n('group') : null, demoInr: n('demo'),
      packages: s(data, 'pkgSessions') ? [{ label: `${n('pkgSessions')} sessions / month`, sessions: n('pkgSessions'), priceInr: n('pkgPrice') }] : [] };
  }
  if (s(data, 'section') === 'payout') {
    patch.payout = { schedule: s(data, 'schedule') === 'monthly' ? 'monthly' : 'weekly', minimumInr: Number(s(data, 'minimumInr')) || 0, upi: s(data, 'upi') || undefined, gstin: s(data, 'gstin') || undefined };
  }
  if (patch.pricing && current.pricing) patch.pricing = { ...(current.pricing as object), ...(patch.pricing as object) };
  await saveSettings(tutorId, { prefs: { ...current, ...patch } });
  jar.set(prefsCookie(tutorId), JSON.stringify({ ...current, ...patch }), { path: '/', maxAge: 60 * 60 * 24 * 365, sameSite: 'lax' });
  touch();
  const back = s(data, 'back') || '/tutor/profile';
  redirect(`${back}${back.includes('?') ? '&' : '?'}saved=1`);
}
