'use server';

/**
 * Student daily-loop writes (W2-S2): tick a timetable block or task, update a to-do, request a timetable change,
 * withdraw it, file an upload. All go through W2-0's core (putRecord / removeRecord / appendEvent).
 * Requests land in `requests` with status 'pending' and the student's counsellor; the counsellor's queue
 * (getTimetableRequests) picks them up and approval re-plans via recomputeLearner (W2-C).
 */
import { revalidatePath } from 'next/cache';
import { getStudent, getTasks, getTimetable, getTimetableRequests, weekStartOf, type DocumentRecord, type Task, type TimetableRequest } from '@/lib/data';
import { appendEvent, newId, nowStamp, putRecord } from '@/lib/actions/core';
import { currentPersona } from '@/lib/session';

async function learnerId(): Promise<string> {
  const p = await currentPersona();
  if (!p || p.role !== 'student') throw new Error('Only a signed-in student can do this.');
  return p.id;
}

function refresh() {
  revalidatePath('/student', 'layout');
}

/** Tick a timetable block (blk_…) or a task. Blocks are saved by re-storing their week with the new status. */
export async function setTaskDone(itemId: string, done: boolean): Promise<void> {
  const id = await learnerId();
  if (itemId.startsWith('blk_')) {
    const date = /_(\d{4}-\d{2}-\d{2})_/.exec(itemId)?.[1];
    const week = getTimetable(id, date ? weekStartOf(date) : undefined);
    const block = week?.blocks.find((b) => b.id === itemId);
    if (!week || !block) return;
    putRecord('timetable', { ...week, blocks: week.blocks.map((b) => (b.id === itemId ? { ...b, status: done ? 'done' : 'planned' } : b)) });
    appendEvent(id, { sourceMethod: 'M16', type: done ? 'block_done' : 'block_undone', payload: { blockId: itemId, kind: block.kind, refId: block.refId } });
  } else {
    const task = getTasks(id).find((t) => t.id === itemId);
    if (!task) return;
    putRecord<Task>('tasks', { ...task, status: done ? 'done' : 'todo', completedUtc: done ? nowStamp() : undefined });
    appendEvent(id, { sourceMethod: 'M16', type: done ? 'task_done' : 'task_reopened', payload: { taskId: itemId, source: task.source } });
  }
  refresh();
}

/** PDF 10b to-dos: Pending / Done / Remove (remove = skipped, kept for the record). */
export async function setTodoStatus(taskId: string, status: 'pending' | 'done' | 'removed'): Promise<void> {
  const id = await learnerId();
  const task = getTasks(id).find((t) => t.id === taskId);
  if (!task) return;
  putRecord<Task>('tasks', { ...task, status: status === 'done' ? 'done' : status === 'removed' ? 'skipped' : 'todo', completedUtc: status === 'done' ? nowStamp() : undefined });
  refresh();
}

export interface RequestChangeInput {
  task: string;
  blockIds: string[];
  fromDate: string;
  toDate: string;
  fromTime: string;
  toTime: string;
  repeat: 'none' | 'daily' | 'weekly' | 'custom';
  days: string[];
  reason?: string;
}
export type RequestChangeResult = { ok: true; id: string } | { ok: false; error: string };

const cap = (d: string) => d[0]!.toUpperCase() + d.slice(1);

/** PDF 3b. The reason line reads "task · repeat · why" so the counsellor sees everything in one place. */
export async function requestTimetableChange(input: RequestChangeInput): Promise<RequestChangeResult> {
  const id = await learnerId();
  const student = getStudent(id);
  const counsellorId = student?.counsellorIds?.[0];
  if (!counsellorId) return { ok: false, error: 'You need a counsellor to request a change.' };
  if (!input.task) return { ok: false, error: 'Pick the task you want to move.' };
  if (!input.fromDate || !input.fromTime || !input.toTime) return { ok: false, error: 'Add a date and a time.' };
  if (input.toTime <= input.fromTime) return { ok: false, error: 'The end time must be after the start time.' };
  const toDate = input.toDate || input.fromDate;
  if (toDate < input.fromDate) return { ok: false, error: 'The end date must be on or after the start date.' };
  const repeat = input.repeat === 'none' ? 'once'
    : input.repeat === 'daily' ? `daily until ${toDate}`
      : `${input.days.length ? input.days.map(cap).join('/') : 'weekly'} until ${toDate}`;
  const req: TimetableRequest = {
    id: newId('ttr'),
    learnerId: id,
    createdUtc: nowStamp(),
    weekStart: weekStartOf(input.fromDate),
    blockIds: input.blockIds,
    kind: 'move',
    reason: [input.task, repeat, input.reason?.trim()].filter(Boolean).join(' · '),
    proposed: { date: input.fromDate, start: input.fromTime, end: input.toTime },
    status: 'pending',
    counsellorId,
  };
  putRecord('requests', req);
  appendEvent(id, { sourceMethod: 'M16', type: 'timetable_change_requested', payload: { requestId: req.id, counsellorId } });
  refresh();
  return { ok: true, id: req.id };
}

/** Undo on the pending card (PDF 3c): the request is withdrawn as declined by the student. */
export async function withdrawTimetableRequest(requestId: string): Promise<void> {
  const id = await learnerId();
  const r = getTimetableRequests({ learnerId: id }).find((x) => x.id === requestId);
  if (!r || r.status !== 'pending') return;
  putRecord<TimetableRequest>('requests', { ...r, status: 'declined', decidedBy: id, decidedUtc: nowStamp(), decisionNote: 'Withdrawn by the student' });
  refresh();
}

/** PDF 4c upload. Demo: only names are stored; `refId` "folder:{slug}" pins the file to the folder it was dropped in. */
export async function uploadToInventory(shelf: DocumentRecord['folder'], folderSlug: string, files: { name: string; sizeKb: number }[], uploadedUtc?: string): Promise<void> {
  const id = await learnerId();
  for (const f of files.slice(0, 10)) {
    const kind: DocumentRecord['kind'] = shelf === 'application_documents' && folderSlug === 'essay-drafts' ? 'essay' : shelf === 'job_ready' && folderSlug === 'portfolio-projects' ? 'portfolio' : 'other';
    putRecord<DocumentRecord>('documents', {
      id: newId('doc'), learnerId: id, folder: shelf, title: f.name.replace(/\.[a-z0-9]+$/i, ''), fileName: f.name, kind,
      uploadedUtc: uploadedUtc ?? nowStamp(), source: 'M5', sizeKb: f.sizeKb, refId: `folder:${folderSlug}`,
    });
  }
  refresh();
}

/** Regenerate (PDF 3a): drop nothing, just re-read; the live week is rebuilt by the engine on read. */
export async function regenerateTimetable(): Promise<void> {
  await learnerId();
  refresh();
}
