'use server';
/**
 * W2-C counsellor writes. All go through lib/actions/core.ts so every screen sees them.
 *  - decideTimetableRequest: approve, approve with an edited slot, or decline a student's timetable request (PDF 3b).
 *    Approval moves or drops the blocks, locks the new slot, and re-plans the rest of the week (recomputeLearner).
 *  - saveCareerSession: a career session with notes, decisions and action items; each action item becomes a task.
 */
import { redirect } from 'next/navigation';
import { revalidatePath } from 'next/cache';
import { appendEvent, newId, nowStamp, putRecord, recomputeLearner } from '@/lib/actions/core';
import { addDaysLocal, demoToday, getStudent, getTimetable, getTimetableRequests, localDateOf } from '@/lib/data';
import type { Approval, MeetingNote, Message, Session, Task, TimetableRequest, TimetableWeek } from '@/lib/data/types';
import type { TimetableBlock } from '@/lib/engines';
import { currentPersona } from '@/lib/session';

async function counsellor() {
  const p = await currentPersona();
  if (!p || p.role !== 'counsellor') throw new Error('Only a counsellor can do this');
  return p;
}

const HHMM = /^\d{2}:\d{2}$/;
const DATE = /^\d{4}-\d{2}-\d{2}$/;
const toMin = (t: string) => Number(t.slice(0, 2)) * 60 + Number(t.slice(3, 5));
const toHHMM = (m: number) => `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;

/** Local date + HH:MM (IST unless the student says otherwise) to ISO UTC. */
function utcOf(date: string, hhmm: string, offsetMinutes: number) {
  return new Date(Date.parse(`${date}T00:00:00Z`) + (toMin(hhmm) - offsetMinutes) * 60_000).toISOString();
}

/** Apply an approved change to the week: move (or swap) blocks to the slot, drop them, or resize them. Returns the new week. */
async function applyRequestToWeek(week: TimetableWeek, req: TimetableRequest, slot: { date: string; start: string; end: string } | undefined, offset: number): Promise<TimetableWeek> {
  const ids = new Set(req.blockIds);
  let blocks: TimetableBlock[] = week.blocks.map((b) => ({ ...b }));
  if (req.kind === 'drop') {
    blocks = blocks.filter((b) => !ids.has(b.id));
  } else if (slot && (req.kind === 'move' || req.kind === 'swap' || req.kind === 'other' || req.kind === 'more_time' || req.kind === 'less_time')) {
    // Lay the requested blocks back to back from the slot start, up to the slot end.
    let cursor = toMin(slot.start);
    const end = toMin(slot.end);
    const moving = blocks.filter((b) => ids.has(b.id));
    const resize = req.kind === 'more_time' || req.kind === 'less_time' || moving.length === 1;
    for (const b of moving) {
      const minutes = resize && moving.length === 1 ? Math.max(10, end - cursor) : Math.min(b.minutes, Math.max(10, end - cursor));
      b.date = slot.date;
      b.start = toHHMM(cursor);
      b.end = toHHMM(cursor + minutes);
      b.minutes = minutes;
      b.startUtc = utcOf(slot.date, b.start, offset);
      b.endUtc = utcOf(slot.date, b.end, offset);
      cursor += minutes;
    }
    // Anything else (not requested) that overlaps the new slot is freed for the re-plan to place elsewhere.
    blocks = blocks.filter((b) => ids.has(b.id) || b.locked || b.date !== slot.date || toMin(b.end) <= toMin(slot.start) || toMin(b.start) >= end);
  }
  // Requested blocks are locked so the re-plan builds around them.
  blocks = blocks.map((b) => (ids.has(b.id) ? { ...b, locked: true } : b)).sort((a, b) => a.startUtc.localeCompare(b.startUtc));
  return { ...week, blocks, generatedUtc: nowStamp(), reason: 'request_approved' };
}

export async function decideTimetableRequest(form: FormData) {
  const me = await counsellor();
  const requestId = String(form.get('requestId') ?? '');
  const decision = String(form.get('decision') ?? '') as 'approved' | 'edited' | 'declined';
  const note = String(form.get('note') ?? '').trim().slice(0, 500);
  const req = getTimetableRequests({}).find((r) => r.id === requestId);
  if (!req || req.status !== 'pending' || !['approved', 'edited', 'declined'].includes(decision)) redirect('/counsellor/timetable-requests');
  const student = getStudent(req.learnerId);
  const offset = student?.tzOffsetMinutes ?? 330;
  const utc = nowStamp();

  let slot = typeof req.proposed === 'object' && req.proposed ? req.proposed : undefined;
  if (decision === 'edited') {
    const date = String(form.get('date') ?? ''), start = String(form.get('start') ?? ''), end = String(form.get('end') ?? '');
    if (DATE.test(date) && HHMM.test(start) && HHMM.test(end) && toMin(end) > toMin(start)) slot = { date, start, end };
  }

  const decided: TimetableRequest = {
    ...req, status: decision, counsellorId: req.counsellorId ?? me.id, decidedBy: me.id, decidedUtc: utc,
    decisionNote: note || (decision === 'declined' ? 'Declined' : decision === 'edited' && slot ? `Approved for ${slot.date} ${slot.start} to ${slot.end}` : 'Approved'),
    ...(decision === 'edited' && slot ? { proposed: slot } : {}),
  };
  putRecord('requests', decided);
  putRecord<Approval>('approvals', { id: newId('apr'), learnerId: req.learnerId, kind: 'timetable_request', targetId: req.id, byId: me.id, decision: decision === 'declined' ? 'declined' : 'approved', utc, note: decided.decisionNote });
  appendEvent(req.learnerId, { sourceMethod: 'M17', type: 'timetable_request_decided', payload: { requestId: req.id, decision, by: me.id } });

  if (decision !== 'declined') {
    const week = getTimetable(req.learnerId, req.weekStart);
    if (week) putRecord('timetable', await applyRequestToWeek(week, req, slot, offset));
    recomputeLearner(req.learnerId, { reason: 'request_approved' });
  }

  const first = me.name.split(' ')[0];
  putRecord<Message>('messages', {
    id: newId('msg'), threadId: `${req.learnerId}:${me.id}`, learnerId: req.learnerId, from: me.id, toIds: [req.learnerId], sentUtc: utc,
    text: decision === 'declined'
      ? `${first} declined your timetable request${note ? `: ${note}` : '.'}`
      : `${first} approved your timetable request${slot ? ` (${slot.date}, ${slot.start} to ${slot.end})` : ''}. Your week has been re-planned.${note ? ` ${note}` : ''}`,
  });
  revalidatePath('/', 'layout');
  redirect(`/counsellor/timetable-requests?done=${encodeURIComponent(req.id)}&status=decided`);
}

export async function saveCareerSession(form: FormData) {
  const me = await counsellor();
  const learnerId = String(form.get('learnerId') ?? '');
  const student = getStudent(learnerId);
  if (!student) redirect('/counsellor/career-sessions');
  const summary = String(form.get('summary') ?? '').trim().slice(0, 2000);
  const decisions = String(form.get('decisions') ?? '').split('\n').map((s) => s.trim()).filter(Boolean).slice(0, 10);
  const careerIds = form.getAll('careerId').map(String).slice(0, 2);
  const titles = form.getAll('itemTitle').map((s) => String(s).trim());
  const dues = form.getAll('itemDue').map(String);
  const today = demoToday();
  const utc = nowStamp();
  const noteId = newId('mtg');
  const sessionId = newId('ses');

  const actionItems: MeetingNote['actionItems'] = [];
  titles.forEach((title, i) => {
    if (!title) return;
    const dueOn = DATE.test(dues[i] ?? '') ? dues[i]! : addDaysLocal(today, 14);
    const taskId = newId('task');
    putRecord<Task>('tasks', {
      id: taskId, learnerId, title: title.slice(0, 200), kind: 'action_item', dueDate: dueOn, status: 'todo', source: 'counsellor',
      createdBy: me.id, createdUtc: utc, minutes: 30, refId: noteId, href: '/student/career', detail: `From your career session with ${me.name}`,
    });
    actionItems.push({ id: newId('ai'), title: title.slice(0, 200), dueOn, taskId, done: false });
  });

  putRecord<MeetingNote>('meetings', { id: noteId, learnerId, staffId: me.id, date: today, kind: 'career', summary: summary || 'Career session', decisions, actionItems, tier: 'T1' });
  putRecord<Session>('sessions', {
    id: sessionId, learnerId, learnerIds: [learnerId], hostId: me.id, hostRole: 'counsellor', kind: 'career', title: 'Career session',
    focus: careerIds.join(', '), startUtc: new Date(Date.parse(utc) - 45 * 60_000).toISOString(), minutes: 45, status: 'completed', mode: 'online', meetingNoteId: noteId,
  });
  appendEvent(learnerId, { sourceMethod: 'M3', type: 'career_session', payload: { meetingNoteId: noteId, careerIds, actionItems: actionItems.length, parameterIds: ['p200'] } });
  recomputeLearner(learnerId, { reason: 'task_assigned' });
  revalidatePath('/', 'layout');
  void localDateOf;
  redirect(`/counsellor/career-sessions?student=${learnerId}${careerIds[0] ? `&a=${careerIds[0]}` : ''}${careerIds[1] ? `&b=${careerIds[1]}` : ''}&saved=1`);
}
