/**
 * W2-0 core write actions. Every demo write goes through here (directly or via a thread's lib/actions/*.ts):
 *   appendEvent(learnerId, event)      append an EvidenceEvent
 *   putRecord(collection, record)      upsert any record (task, booking, session, request, comment, approval...)
 *   removeRecord(collection, key)      delete (hide) a record
 *   recomputeLearner(learnerId)        re-run gaps, mastery, ALR, plan and this week's timetable after a write
 * Next best actions are computed live on every read, so they need no recompute.
 *
 * These are plain server functions; call them from your own 'use server' actions.
 */
import 'server-only';
import { replanTimetable } from '@/lib/engines';
import type { EvidenceEvent } from '@/lib/types';
import { baseRecords, deleteRecord, learnerRecords, overlayKeys, writeRecord, type CollectionName } from '@/lib/store/collections';
import { overlay } from '@/lib/store/overlay';
import { DEMO_NOW_ISO } from '@/lib/demo-clock';
import { applyAttempt, planFor, stateFrom, timetableInput, weekStartOf, localDateOf } from '@/lib/data/derive';
import { getAttempts, getCurrentPlan, getGaps, getMastery, getProfileValues, getSessions, getStudent, getTimetable } from '@/lib/data';
import type { AlrRecord, Attempt, GapRecord, PlanRecord, TimetableWeek } from '@/lib/data/types';

export type { CollectionName };

/**
 * Timestamp for a demo write: the demo clock plus one second per overlay write, so new records sort
 * after all history and after each other, and a reset brings time back to DEMO_NOW.
 */
export function nowStamp(): string {
  return new Date(Date.parse(DEMO_NOW_ISO) + (overlay().count() + 1) * 1000).toISOString();
}

let idSeq = 0;
/** Unique id for a new record, e.g. newId('task') → task_m3k9x_1. */
export function newId(prefix: string): string {
  idSeq += 1;
  return `${prefix}_${Date.now().toString(36)}${idSeq}`;
}

export function appendEvent(learnerId: string, e: Omit<EvidenceEvent, 'eventId' | 'learnerId' | 'timestampUtc'> & Partial<Pick<EvidenceEvent, 'eventId' | 'timestampUtc'>>): EvidenceEvent {
  const ev: EvidenceEvent = { eventId: e.eventId ?? newId('evt'), learnerId, timestampUtc: e.timestampUtc ?? nowStamp(), sourceMethod: e.sourceMethod, type: e.type, payload: e.payload };
  writeRecord('events', ev);
  return ev;
}

/** Upsert a record. The record must carry its key fields (usually `id`, and `learnerId` for learner data). */
export function putRecord<T extends object>(collection: CollectionName, record: T): T {
  writeRecord(collection, record);
  return record;
}

export function removeRecord(collection: CollectionName, key: string, learnerId?: string): void {
  deleteRecord(collection, key, learnerId);
}

export interface RecomputeResult {
  appliedAttemptIds: string[];
  changedGaps: GapRecord[];
  plan?: PlanRecord;
  timetable?: TimetableWeek;
}

/**
 * Re-run the engines for one learner after a write.
 * New attempts (written since the last recompute) are diagnosed in time order; changed gaps get a new
 * intervention plan; this week's timetable is re-planned (past blocks kept) whenever anything changed
 * or `reason` is given (e.g. 'request_approved', 'session_booked', 'task_assigned').
 */
export function recomputeLearner(learnerId: string, opts: { reason?: string } = {}): RecomputeResult {
  const student = getStudent(learnerId);
  const out: RecomputeResult = { appliedAttemptIds: [], changedGaps: [] };
  if (!student) return out;
  const now = nowStamp();

  // 1. attempts not yet applied
  const applied = new Set(
    learnerRecords<EvidenceEvent>('events', learnerId)
      .filter((e) => e.type === 'attempt_applied')
      .map((e) => String(e.payload.attemptId)),
  );
  const baseIds = new Set(baseRecords<Attempt>('attempts').filter((a) => a.learnerId === learnerId).map((a) => a.id));
  const writtenIds = overlayKeys('attempts');
  const all = getAttempts(learnerId).sort((a, b) => a.submittedUtc.localeCompare(b.submittedUtc));
  const pending = all.filter((a) => writtenIds.has(a.id) && !baseIds.has(a.id) && !applied.has(a.id));

  if (pending.length) {
    const state = stateFrom(getGaps(learnerId), getMastery(learnerId), learnerRecords<AlrRecord>('alr', learnerId));
    const changed = new Map<string, GapRecord>();
    for (const a of pending) {
      const eff = applyAttempt(student, a, state, all);
      for (const g of eff.gaps) changed.set(g.id, g);
      for (const m of eff.mastery) writeRecord('mastery', m);
      for (const r of eff.alr) writeRecord('alr', r);
      appendEvent(learnerId, {
        sourceMethod: 'M14',
        type: 'attempt_applied',
        payload: { attemptId: a.id, diagnosed: eff.diagnoses.length, gaps: eff.gaps.map((g) => ({ id: g.id, code: g.code, status: g.status })) },
      });
      out.appliedAttemptIds.push(a.id);
    }
    for (const g of changed.values()) writeRecord('gaps', g);
    out.changedGaps = [...changed.values()];
  }

  // 2. new plan when gaps changed
  if (out.changedGaps.length) {
    const prev = getCurrentPlan(learnerId);
    const weeks = prev ? prev.freePlanWeeks + Math.floor((Date.parse(now) - Date.parse(prev.createdUtc)) / (7 * 86_400_000)) : 0;
    if (prev && prev.status === 'active') writeRecord('plans', { ...prev, status: 'replaced' });
    const profile = getProfileValues(learnerId).filter((v) => v.tier !== 'T3' && v.tier !== 'C');
    out.plan = planFor(student, getGaps(learnerId), now, weeks, profile);
    writeRecord('plans', out.plan);
  }

  // 3. re-plan this week
  if (out.changedGaps.length || opts.reason) {
    const ws = weekStartOf(localDateOf(now));
    const prev = getTimetable(learnerId, ws);
    if (student.availability.length) {
      const input = timetableInput(student, ws, { gaps: getGaps(learnerId), mastery: getMastery(learnerId), sessions: getSessions(learnerId), now });
      const next = prev
        ? replanTimetable(prev, input, out.changedGaps.length ? { type: 'test_result', gaps: input.gaps ?? [], masteryStates: input.masteryStates } : { type: 'lock', blockIds: [] })
        : replanTimetable({ ...input, blocks: [], unscheduled: [], capacityMinutes: 0, plannedMinutes: 0, bufferMinutes: 0 } as never, input, { type: 'lock', blockIds: [] });
      out.timetable = { ...next, generatedUtc: now, reason: opts.reason ?? 'test_result' };
      writeRecord('timetable', out.timetable);
    }
  }
  return out;
}

/** Clear every demo write ("Reset demo"). */
export function resetDemo(): { cleared: number } {
  const ov = overlay();
  const n = ov.count();
  ov.clear();
  return { cleared: n };
}
