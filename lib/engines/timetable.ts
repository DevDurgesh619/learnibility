/**
 * Engine 5: the learner's week, as calendar blocks in priority order.
 * Source: blueprint "The engines behind the daily loop" (timetable), workbook "Mastery Inputs" row 16-17
 * (retrieval sessions) and "Interventions" G6-1 (spaced retrieval), "Gap Calculator" C57 (weeks to close).
 *
 * Priority (highest first), each placed into the learner's free study windows:
 *   1. fixed sessions (tutor sessions, classes) and locked blocks: never moved
 *   2. Saturday weekly test
 *   3. carried-over missed tasks
 *   4. spaced reviews due 1, 3, 7, 14 and 30 days after a subtopic was last tested, on the due day
 *   5. gap blocks, sized from hours to close spread over the planned weeks, worst gap first
 *   6. current-chapter practice
 * 15% of each day's free time is held back as a buffer block at the end of the day.
 * Re-plan (missed task or new test result) keeps the past and locked blocks and rebuilds the rest.
 * Pure: pass `now` and the time-zone offset; nothing reads the clock.
 */
import type { Gap, IsoUtc, MasteryState } from '../types';
import type { Weekday } from '../types/catalogue';
import { REVIEW_INTERVALS_DAYS } from './config';

export type BlockKind = 'session' | 'weekly_test' | 'carry_over' | 'review' | 'gap' | 'chapter' | 'buffer' | 'locked';

export interface TimetableBlock {
  id: string;
  /** Local date YYYY-MM-DD. */
  date: string;
  /** Local HH:MM. */
  start: string;
  end: string;
  minutes: number;
  kind: BlockKind;
  title: string;
  /** Subtopic, gap, chapter or session id the block works on. */
  refId?: string;
  priority: number;
  locked: boolean;
  status: 'planned' | 'done' | 'missed';
  startUtc: IsoUtc;
  endUtc: IsoUtc;
}

export interface StudyWindow { day: Weekday; start: string; end: string }
export interface FixedSession { id: string; title: string; date: string; start: string; end: string }

export type TimetableGap = Pick<Gap, 'id' | 'subtopicId' | 'code' | 'hoursToClose' | 'status'> & { title?: string; weeks?: number | null };

export interface TimetableInput {
  learnerId: string;
  /** Local Monday, YYYY-MM-DD. */
  weekStart: string;
  now: IsoUtc;
  /** Minutes east of UTC; 330 for India. */
  tzOffsetMinutes?: number;
  availability: StudyWindow[];
  sessions?: FixedSession[];
  locked?: TimetableBlock[];
  masteryStates?: Pick<MasteryState, 'subtopicId' | 'lastTestedUtc' | 'level'>[];
  gaps?: TimetableGap[];
  currentChapter?: { chapterId: string; title: string; hoursThisWeek: number };
  weeklyTest?: { minutes: number; title?: string; day?: Weekday } | false;
  carryOver?: TimetableBlock[];
  /** Display names, keyed by subtopic id. */
  names?: Record<string, string>;
  bufferFraction?: number;
  reviewMinutes?: number;
  blockMinutes?: number;
}

export interface Timetable {
  learnerId: string;
  weekStart: string;
  blocks: TimetableBlock[];
  unscheduled: { kind: BlockKind; refId?: string; title: string; minutes: number; reason: string }[];
  capacityMinutes: number;
  plannedMinutes: number;
  bufferMinutes: number;
}

const DAYS: Weekday[] = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'];
const PRIORITY: Record<BlockKind, number> = { session: 1, locked: 1, weekly_test: 2, carry_over: 3, review: 4, gap: 5, chapter: 6, buffer: 9 };
const DAY_MS = 86_400_000;

const toMin = (hhmm: string) => Number(hhmm.slice(0, 2)) * 60 + Number(hhmm.slice(3, 5));
const toHHMM = (m: number) => `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;
const dateAdd = (date: string, days: number) => new Date(Date.parse(date + 'T00:00:00Z') + days * DAY_MS).toISOString().slice(0, 10);
export const weekdayOf = (date: string): Weekday => DAYS[(new Date(date + 'T00:00:00Z').getUTCDay() + 6) % 7];

function utc(date: string, minute: number, off: number): IsoUtc {
  return new Date(Date.parse(date + 'T00:00:00Z') + (minute - off) * 60_000).toISOString();
}

type Interval = [number, number];

function subtract(free: Interval[], busy: Interval): Interval[] {
  const out: Interval[] = [];
  for (const [a, b] of free) {
    if (busy[1] <= a || busy[0] >= b) out.push([a, b]);
    else {
      if (busy[0] > a) out.push([a, busy[0]]);
      if (busy[1] < b) out.push([busy[1], b]);
    }
  }
  return out;
}

export function buildTimetable(input: TimetableInput): Timetable {
  const off = input.tzOffsetMinutes ?? 330;
  const bufferFraction = input.bufferFraction ?? 0.15;
  const reviewMin = input.reviewMinutes ?? 10;
  const chunk = input.blockMinutes ?? 30;
  const dates = DAYS.map((_, i) => dateAdd(input.weekStart, i));
  const weekEnd = dateAdd(input.weekStart, 7);
  const nowLocal = Date.parse(input.now) + off * 60_000;
  const blocks: TimetableBlock[] = [];
  const unscheduled: Timetable['unscheduled'] = [];

  const make = (date: string, s: number, e: number, kind: BlockKind, title: string, refId?: string, extra: Partial<TimetableBlock> = {}): TimetableBlock => ({
    id: `blk_${input.learnerId}_${date}_${toHHMM(s).replace(':', '')}_${kind}`,
    date, start: toHHMM(s), end: toHHMM(e), minutes: e - s, kind, title, ...(refId ? { refId } : {}),
    priority: PRIORITY[kind], locked: kind === 'session' || kind === 'locked', status: 'planned',
    startUtc: utc(date, s, off), endUtc: utc(date, e, off), ...extra,
  });

  // free time per day, clipped to after `now`
  const free: Record<string, Interval[]> = {};
  for (const d of dates) {
    const dayStart = Date.parse(d + 'T00:00:00Z');
    const nowMin = Math.ceil((nowLocal - dayStart) / 60_000 / 5) * 5;
    const iv: Interval[] = input.availability
      .filter((w) => w.day === weekdayOf(d))
      .map((w) => [Math.max(toMin(w.start), nowMin), toMin(w.end)] as Interval)
      .filter(([a, b]) => b - a >= 5);
    free[d] = iv.sort((a, b) => a[0] - b[0]);
  }
  const occupy = (date: string, s: number, e: number) => { if (free[date]) free[date] = subtract(free[date], [s, e]); };

  // 1. fixed sessions and locked blocks (also past blocks kept by replan)
  for (const s of input.sessions ?? []) {
    if (s.date < input.weekStart || s.date >= weekEnd) continue;
    blocks.push(make(s.date, toMin(s.start), toMin(s.end), 'session', s.title, s.id, { id: `blk_${s.id}` }));
    occupy(s.date, toMin(s.start), toMin(s.end));
  }
  for (const b of input.locked ?? []) {
    blocks.push({ ...b });
    occupy(b.date, toMin(b.start), toMin(b.end));
  }

  // buffer: 15% of each day's free time, at the end of the day's last window
  let capacity = 0, bufferMinutes = 0;
  for (const d of dates) {
    const total = free[d].reduce((s, [a, b]) => s + b - a, 0);
    capacity += total;
    const buf = Math.round((total * bufferFraction) / 5) * 5;
    if (buf >= 5) {
      const last = free[d][free[d].length - 1];
      const s = Math.max(last[0], last[1] - buf);
      blocks.push(make(d, s, last[1], 'buffer', 'Buffer: catch-up or rest'));
      bufferMinutes += last[1] - s;
      occupy(d, s, last[1]);
    }
  }

  /** Place `minutes` on the first preferred date with room; returns the block or null. */
  const place = (minutes: number, prefer: string[], kind: BlockKind, title: string, refId?: string): TimetableBlock | null => {
    for (const d of prefer) {
      const slot = (free[d] ?? []).find(([a, b]) => b - a >= minutes);
      if (slot) {
        const blk = make(d, slot[0], slot[0] + minutes, kind, title, refId);
        blocks.push(blk);
        occupy(d, slot[0], slot[0] + minutes);
        return blk;
      }
    }
    return null;
  };
  const from = (d: string) => dates.filter((x) => x >= d);
  const done = new Map<string, number>();
  for (const b of input.locked ?? []) if (b.refId && b.status !== 'missed') done.set(`${b.kind}:${b.refId}`, (done.get(`${b.kind}:${b.refId}`) ?? 0) + b.minutes);

  // 2. weekly test
  if (input.weeklyTest !== false) {
    const wt = input.weeklyTest ?? { minutes: 45 };
    const day = dates[DAYS.indexOf(wt.day ?? 'sat')];
    if (!done.has(`weekly_test:week-${input.weekStart}`)) {
      if (!place(wt.minutes, [...from(day), ...dates.filter((x) => x < day).reverse()], 'weekly_test', wt.title ?? 'Weekly test', `week-${input.weekStart}`))
        unscheduled.push({ kind: 'weekly_test', title: wt.title ?? 'Weekly test', minutes: wt.minutes, reason: 'No free window long enough this week' });
    }
  }

  // 3. carried-over missed tasks
  for (const c of input.carryOver ?? []) {
    if (!place(c.minutes, dates, 'carry_over', `Catch up: ${c.title.replace(/^Catch up: /, '')}`, c.refId))
      unscheduled.push({ kind: 'carry_over', refId: c.refId, title: c.title, minutes: c.minutes, reason: 'No room left this week' });
  }

  // 4. spaced reviews due this week
  const reviews: { due: string; subtopicId: string; n: number }[] = [];
  for (const m of input.masteryStates ?? []) {
    REVIEW_INTERVALS_DAYS.forEach((days, idx) => {
      const due = new Date(Date.parse(m.lastTestedUtc) + off * 60_000 + days * DAY_MS).toISOString().slice(0, 10);
      if (due >= input.weekStart && due < weekEnd) reviews.push({ due, subtopicId: m.subtopicId, n: idx + 1 });
    });
  }
  reviews.sort((a, b) => a.due.localeCompare(b.due) || a.subtopicId.localeCompare(b.subtopicId));
  for (const r of reviews) {
    const ref = `${r.subtopicId}#r${r.n}`;
    if (done.has(`review:${ref}`)) continue;
    const name = input.names?.[r.subtopicId] ?? r.subtopicId;
    const title = `Review ${r.n}/${REVIEW_INTERVALS_DAYS.length}: ${name}`;
    const prefer = from(r.due);
    if (!place(reviewMin, prefer.length ? prefer : dates, 'review', title, ref))
      unscheduled.push({ kind: 'review', refId: ref, title, minutes: reviewMin, reason: 'No room on or after the due day' });
  }

  // 5. gap blocks: worst first, spread one block per gap per day before doubling up
  const gaps = (input.gaps ?? []).filter((g) => g.status !== 'closed' && g.hoursToClose > 0)
    .sort((a, b) => Number(b.code === 'G1') - Number(a.code === 'G1') || b.hoursToClose - a.hoursToClose);
  const need = new Map<string, number>();
  for (const g of gaps) {
    const weeks = Math.max(1, Math.ceil(g.weeks ?? 1));
    const perWeek = Math.ceil((g.hoursToClose * 60) / weeks / 5) * 5;
    need.set(g.id, Math.max(0, perWeek - (done.get(`gap:${g.id}`) ?? 0)));
  }
  const gapChunk = (g: TimetableGap) => (g.code === 'G10' ? 20 : chunk);
  for (let pass = 0; pass < 3; pass++) {
    for (const d of dates) {
      for (const g of gaps) {
        const left = need.get(g.id)!;
        if (left <= 0) continue;
        const m = Math.min(gapChunk(g), left);
        const title = g.title ?? `Close gap ${g.code}: ${input.names?.[g.subtopicId] ?? g.subtopicId}`;
        if (place(m, [d], 'gap', title, g.id)) need.set(g.id, left - m);
      }
    }
  }
  for (const g of gaps) if (need.get(g.id)! > 0) unscheduled.push({ kind: 'gap', refId: g.id, title: g.title ?? g.subtopicId, minutes: need.get(g.id)!, reason: 'Week is full; continues next week' });

  // 6. current chapter
  if (input.currentChapter) {
    const c = input.currentChapter;
    let left = Math.max(0, Math.ceil((c.hoursThisWeek * 60) / 5) * 5 - (done.get(`chapter:${c.chapterId}`) ?? 0));
    for (let pass = 0; pass < 3 && left > 0; pass++) {
      for (const d of dates) {
        if (left <= 0) break;
        const m = Math.min(chunk, left);
        if (place(m, [d], 'chapter', `Practice: ${c.title}`, c.chapterId)) left -= m;
      }
    }
    if (left > 0) unscheduled.push({ kind: 'chapter', refId: c.chapterId, title: c.title, minutes: left, reason: 'Week is full' });
  }

  blocks.sort((a, b) => a.startUtc.localeCompare(b.startUtc) || a.priority - b.priority);
  const planned = blocks.filter((b) => b.kind !== 'buffer' && b.kind !== 'session' && b.kind !== 'locked').reduce((s, b) => s + b.minutes, 0);
  return { learnerId: input.learnerId, weekStart: input.weekStart, blocks, unscheduled, capacityMinutes: capacity, plannedMinutes: planned, bufferMinutes };
}

export type ReplanChange =
  | { type: 'missed'; blockIds: string[] }
  | { type: 'test_result'; gaps: TimetableGap[]; masteryStates?: TimetableInput['masteryStates'] }
  | { type: 'lock'; blockIds: string[] };

/**
 * Re-plan the rest of the week after a missed task, a new test result or a lock.
 * Blocks that ended before `input.now` are kept (as done unless missed); locked blocks are kept;
 * missed blocks are carried over; everything else is rebuilt from `input`.
 */
export function replanTimetable(prev: Timetable, input: TimetableInput, change: ReplanChange): Timetable {
  const now = input.now;
  const missed = new Set(change.type === 'missed' ? change.blockIds : []);
  const lockIds = new Set(change.type === 'lock' ? change.blockIds : []);
  const keep: TimetableBlock[] = [];
  const carry: TimetableBlock[] = [...(input.carryOver ?? [])];
  for (const b of prev.blocks) {
    if (b.kind === 'session' || b.kind === 'buffer') continue; // sessions come from input; buffer is recomputed
    if (missed.has(b.id)) {
      keep.push({ ...b, status: 'missed', locked: true });
      if (b.kind !== 'weekly_test') carry.push({ ...b });
      continue;
    }
    if (b.endUtc <= now) keep.push({ ...b, status: b.status === 'missed' ? 'missed' : 'done', locked: true });
    else if (b.locked || lockIds.has(b.id)) keep.push({ ...b, locked: true });
  }
  const next: TimetableInput = {
    ...input,
    locked: [...(input.locked ?? []), ...keep],
    carryOver: carry,
    ...(change.type === 'test_result' ? { gaps: change.gaps, masteryStates: change.masteryStates ?? input.masteryStates } : {}),
  };
  return buildTimetable(next);
}

// ---------------------------------------------------------------- .ics export

const icsTime = (iso: string) => iso.replace(/[-:]/g, '').replace(/\.\d{3}/, '');
const icsEscape = (s: string) => s.replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\n/g, '\\n');

/** RFC 5545 calendar for the blocks (buffer blocks left out). */
export function toIcs(blocks: TimetableBlock[], opts: { now: IsoUtc; calendarName?: string }): string {
  const lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Learnibility//Timetable//EN', 'CALSCALE:GREGORIAN', `X-WR-CALNAME:${icsEscape(opts.calendarName ?? 'Learnibility study plan')}`];
  for (const b of blocks) {
    if (b.kind === 'buffer') continue;
    lines.push('BEGIN:VEVENT', `UID:${b.id}@learnibility`, `DTSTAMP:${icsTime(opts.now)}`, `DTSTART:${icsTime(b.startUtc)}`, `DTEND:${icsTime(b.endUtc)}`,
      `SUMMARY:${icsEscape(b.title)}`, `CATEGORIES:${b.kind.toUpperCase()}`, `DESCRIPTION:${icsEscape(`${b.minutes} min · ${b.kind.replace('_', ' ')}${b.refId ? ' · ' + b.refId : ''}`)}`, 'END:VEVENT');
  }
  lines.push('END:VCALENDAR');
  return lines.join('\r\n') + '\r\n';
}
