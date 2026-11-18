'use server';
/**
 * W2-TE teacher write actions. Everything goes through lib/actions/core (putRecord, appendEvent, recomputeLearner).
 *  - assignWork: a chapter check or a re-teach set to a section or a group; one task per learner, so it lands in
 *    each student's tasks and (for persona learners) re-plans their week.
 *  - validateGap: the workbook Gap Log's "Notes (teacher validation #430)": confirm, correct or reject a diagnosis.
 *    Writes the gap's `validation`, a gap_validated event and profile parameter p430 (last human-validation status).
 */
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { appendEvent, newId, nowStamp, putRecord, recomputeLearner } from '@/lib/actions/core';
import { getChapter, getGaps, getQuestions, getSection, getStudent, getSubtopic, type GapRecord, type Task } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import { GAP_CODES, type GapCode, type Question } from '@/lib/types';
import { GAP_TAXONOMY } from '@/lib/engines';

async function requireTeacher() {
  const p = await currentPersona();
  if (!p || p.role !== 'teacher') throw new Error('Only a signed-in teacher can do this.');
  return p;
}

const byCD = (a: Question, b: Question) => a.conceptGroup.localeCompare(b.conceptGroup) || a.difficulty.localeCompare(b.difficulty) || a.id.localeCompare(b.id);

/** Chapter check: per subtopic the easiest C1, C2 and C3 items plus one C4, like the workbook's check path. */
function chapterCheckQuestions(chapterId: string): Question[] {
  const qs = getQuestions({ chapterId, set: 'mastery_bank' }).sort(byCD);
  const out: Question[] = [];
  const seen = new Set<string>();
  for (const q of qs) {
    const k = `${q.subtopicId}|${q.conceptGroup}`;
    if (seen.has(k)) continue;
    seen.add(k);
    out.push(q);
  }
  return out.slice(0, 20);
}

/** Re-teach set: the subtopic's C1 to C3 items at D1 to D3, easiest first (worked-example then practice). */
function reteachQuestions(subtopicId: string, code?: GapCode): Question[] {
  const qs = getQuestions({ subtopicIds: [subtopicId], set: 'mastery_bank' }).sort(byCD);
  const low = qs.filter((q) => q.conceptGroup !== 'C4' && ['D1', 'D2', 'D3'].includes(q.difficulty));
  // A transfer gap needs a couple of application items too.
  const extra = code === 'G5' ? qs.filter((q) => q.conceptGroup === 'C4').slice(0, 2) : [];
  return [...low.slice(0, 8), ...extra];
}

export interface AssignResult {
  groupId: string;
  title: string;
  learnerIds: string[];
  questionCount: number;
}

/** Form action for the Assign screen. Redirects back with `?done=` so the page shows the confirmation. */
export async function assignWork(formData: FormData): Promise<void> {
  const teacher = await requireTeacher();
  const sectionId = String(formData.get('sectionId') ?? '');
  const section = getSection(sectionId);
  if (!section || section.teacherId !== teacher.id) throw new Error('Unknown section.');

  const kind = String(formData.get('kind') ?? 'chapter_check') as 'chapter_check' | 'reteach';
  const dueDate = String(formData.get('dueDate') ?? '');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(dueDate)) throw new Error('Pick a due date.');
  const chosen = formData.getAll('learnerIds').map(String).filter((id) => section.learnerIds.includes(id));
  const learnerIds = chosen.length ? chosen : section.learnerIds;
  const note = String(formData.get('note') ?? '').trim();

  let title: string;
  let questions: Question[];
  let refId: string;
  let taskKind: Task['kind'];
  let minutes: number;
  let code: GapCode | undefined;
  if (kind === 'reteach') {
    const subtopicId = String(formData.get('subtopicId') ?? '');
    const sub = getSubtopic(subtopicId);
    if (!sub || sub.subjectId !== section.subjectId) throw new Error('Pick a subtopic.');
    const c = String(formData.get('gapCode') ?? '');
    code = (GAP_CODES as readonly string[]).includes(c) ? (c as GapCode) : undefined;
    questions = reteachQuestions(subtopicId, code);
    title = `Re-teach set: ${sub.name}`;
    refId = subtopicId;
    taskKind = 'test'; // opens in the test player (W2-S1: /student/assessments/task.{taskId})
    minutes = Math.max(20, Math.round(questions.reduce((a, q) => a + q.minutes, 0)) + 10);
  } else {
    const chapterId = String(formData.get('chapterId') ?? '');
    const ch = getChapter(chapterId);
    if (!ch || ch.subject.id !== section.subjectId) throw new Error('Pick a chapter.');
    questions = chapterCheckQuestions(chapterId);
    title = `Chapter check: ${ch.chapter.name}`;
    refId = chapterId;
    taskKind = 'test';
    minutes = Math.max(15, Math.round(questions.reduce((a, q) => a + q.minutes, 0)));
  }

  const groupId = newId('tasg');
  const createdUtc = nowStamp();
  const detail = [
    `Set by ${teacher.name} for ${section.name}`,
    code ? `${code} ${GAP_TAXONOMY[code].name.toLowerCase()} gap` : undefined,
    `${questions.length} questions, about ${minutes} min`,
    note || undefined,
  ].filter(Boolean).join(' · ');

  for (const lid of learnerIds) {
    const task: Task = {
      id: `${groupId}__${lid}`, learnerId: lid, title, kind: taskKind, dueDate, status: 'todo', source: 'teacher',
      createdBy: teacher.id, createdUtc, minutes, subjectId: section.subjectId, refId,
      questionIds: questions.map((q) => q.id), href: `/student/assessments/task.${groupId}__${lid}`, detail,
    };
    putRecord('tasks', task);
    if (getStudent(lid)) {
      appendEvent(lid, {
        sourceMethod: 'M15',
        type: 'task_assigned',
        payload: { taskId: task.id, groupId, by: teacher.id, sectionId, kind, refId, gapCode: code ?? null, dueDate, questionIds: task.questionIds },
      });
      recomputeLearner(lid, { reason: 'task_assigned' });
    }
  }

  revalidatePath('/teacher', 'layout');
  revalidatePath('/student', 'layout');
  redirect(`/teacher/assign?section=${encodeURIComponent(sectionId)}&done=${encodeURIComponent(groupId)}`);
}

/** Form action for the Gap log: confirm, correct (with a new code) or reject a diagnosis. */
export async function validateGap(formData: FormData): Promise<void> {
  const teacher = await requireTeacher();
  const sectionId = String(formData.get('sectionId') ?? '');
  const section = getSection(sectionId);
  if (!section || section.teacherId !== teacher.id) throw new Error('Unknown section.');
  const learnerId = String(formData.get('learnerId') ?? '');
  if (!section.learnerIds.includes(learnerId)) throw new Error('Student is not in this section.');
  const verdict = String(formData.get('verdict') ?? '') as 'confirmed' | 'corrected' | 'rejected';
  if (!['confirmed', 'corrected', 'rejected'].includes(verdict)) throw new Error('Pick confirm, correct or reject.');
  const cc = String(formData.get('correctedCode') ?? '');
  const correctedCode = verdict === 'corrected' && (GAP_CODES as readonly string[]).includes(cc) ? (cc as GapCode) : undefined;
  if (verdict === 'corrected' && !correctedCode) throw new Error('Pick the corrected gap code.');
  const note = String(formData.get('note') ?? '').trim() || undefined;

  // The gap as stored (persona) or as sent by the form (background learner, first validation).
  const gapId = String(formData.get('gapId') ?? '');
  const raw = getGaps(learnerId).find((g) => g.id === gapId);
  let gap: GapRecord;
  if (raw) {
    // getGaps applies a corrected code; keep the engine's original code on the record.
    const original = (raw.validation as { originalCode?: GapCode } | undefined)?.originalCode;
    gap = { ...raw, code: raw.validation?.verdict === 'corrected' && original ? original : raw.code };
  } else {
    const fromForm = JSON.parse(String(formData.get('gap') ?? 'null')) as GapRecord | null;
    if (!fromForm || fromForm.id !== gapId || fromForm.learnerId !== learnerId) throw new Error('Unknown gap.');
    gap = fromForm;
  }
  const utc = nowStamp();
  const validation = { byId: teacher.id, utc, verdict, correctedCode, note, originalCode: gap.code };
  putRecord('gaps', { ...gap, validation, updatedUtc: utc, ...(verdict === 'rejected' ? { status: 'closed' as const, closedUtc: utc } : {}) });

  // Parameter #430: last human-validation status (T1, M15 teacher observation).
  putRecord('profile', {
    learnerId, paramId: 'p430', source: 'M15', asOfUtc: utc, confidence: 'high', tier: 'T1',
    value: { status: verdict, by: teacher.id, byName: teacher.name, utc, gapId, subtopicId: gap.subtopicId, code: gap.code, correctedCode: correctedCode ?? null, note: note ?? null },
  });
  appendEvent(learnerId, {
    sourceMethod: 'M15',
    type: 'gap_validated',
    payload: { gapId, parameterIds: ['p430'], verdict, originalCode: gap.code, correctedCode: correctedCode ?? null, by: teacher.id, note: note ?? null },
  });
  if (getStudent(learnerId)) recomputeLearner(learnerId, { reason: 'gap_validated' });

  revalidatePath('/teacher', 'layout');
  redirect(`/teacher/gap-log?section=${encodeURIComponent(sectionId)}&saved=${encodeURIComponent(gapId)}`);
}
