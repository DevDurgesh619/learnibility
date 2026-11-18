'use server';
/** W2-P mentor writes: career session notes whose action items become the mentee's tasks, skill-plan tasks, messages. */
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { demoToday, getCaseload, getMessages, getSessions, type MeetingNote, type Message, type Session, type Task } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import { appendEvent, newId, nowStamp, putRecord, recomputeLearner } from './core';

const str = (f: FormData, k: string) => {
  const v = f.get(k);
  return typeof v === 'string' && v.trim() ? v.trim() : undefined;
};

async function mentorFor(learnerId: string | undefined) {
  const me = await currentPersona();
  if (!me || me.role !== 'mentor') throw new Error('Only a mentor can do this.');
  if (!learnerId || !getCaseload(me.id).some((c) => c.student.id === learnerId)) throw new Error('Not your mentee.');
  return me;
}

function done(path: string, q: Record<string, string>): never {
  revalidatePath('/', 'layout');
  redirect(`${path}?${new URLSearchParams(q)}`);
}

function task(learnerId: string, mentorId: string, title: string, dueDate: string, refId?: string, detail?: string): Task {
  return { id: newId(`task_${learnerId}`), learnerId, title, kind: 'action_item', dueDate, status: 'todo', source: 'mentor', createdBy: mentorId, createdUtc: nowStamp(), refId, detail, minutes: 30 };
}

/** Save a career session: a MeetingNote (T1, kind career) and one task per action item for the mentee. */
export async function saveCareerSession(form: FormData) {
  const learnerId = str(form, 'learnerId');
  const me = await mentorFor(learnerId);
  const summary = str(form, 'summary');
  if (!summary) throw new Error('Add a short summary.');
  const date = str(form, 'date') ?? demoToday();
  const noteId = newId(`mtg_${learnerId}`);
  const items: MeetingNote['actionItems'] = [];
  for (let i = 0; i < 4; i++) {
    const title = str(form, `item${i}`);
    if (!title) continue;
    const t = task(learnerId!, me.id, title, str(form, `due${i}`) ?? date, noteId, 'From your career session');
    putRecord('tasks', t);
    items.push({ id: `${noteId}-a${i + 1}`, title, dueOn: t.dueDate, taskId: t.id, done: false });
  }
  const note: MeetingNote = {
    id: noteId, learnerId: learnerId!, staffId: me.id, date, kind: 'career', summary,
    decisions: (str(form, 'decisions') ?? '').split('\n').map((x) => x.trim()).filter(Boolean), actionItems: items, tier: 'T1',
  };
  putRecord('meetings', note);
  // Link the session it belongs to, if one was picked.
  const sessionId = str(form, 'sessionId');
  const sess = sessionId ? getSessions(me.id).find((s) => s.id === sessionId) : undefined;
  if (sess) putRecord('sessions', { ...sess, status: 'completed', meetingNoteId: noteId } satisfies Session);
  appendEvent(learnerId!, { sourceMethod: 'M18', type: 'career_session_logged', payload: { meetingNoteId: noteId, actionItems: items.length } });
  recomputeLearner(learnerId!, { reason: 'task_assigned' });
  done('/mentor/career-sessions', { mentee: learnerId!, saved: noteId });
}

/** Turn one skill line of a skill plan into a task for the mentee. */
export async function assignSkillTask(form: FormData) {
  const learnerId = str(form, 'learnerId');
  const me = await mentorFor(learnerId);
  const title = str(form, 'title');
  if (!title) throw new Error('Missing task.');
  const t = task(learnerId!, me.id, title, str(form, 'due') ?? demoToday(), str(form, 'skillId'), str(form, 'detail'));
  putRecord('tasks', t);
  appendEvent(learnerId!, { sourceMethod: 'M15', type: 'skill_task_assigned', payload: { taskId: t.id, skillId: t.refId, careerId: str(form, 'careerId') } });
  recomputeLearner(learnerId!, { reason: 'task_assigned' });
  done('/mentor/skill-plans', { mentee: learnerId!, career: str(form, 'careerId') ?? '', assigned: t.refId ?? '' });
}

export async function sendMentorMessage(form: FormData) {
  const learnerId = str(form, 'learnerId');
  const me = await mentorFor(learnerId);
  const text = str(form, 'text');
  if (!text) throw new Error('Write a message first.');
  const to = str(form, 'to') ?? learnerId!;
  const threadId = str(form, 'threadId') ?? `${learnerId}:${me.id}`;
  const m: Message = { id: newId('msg'), threadId, learnerId: learnerId!, from: me.id, toIds: [to], text, sentUtc: nowStamp(), readBy: [me.id] };
  putRecord('messages', m);
  done('/mentor/messages', { thread: getMessages(me.id, { threadId })[0]?.threadId ?? threadId });
}
