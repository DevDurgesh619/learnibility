import { describe, expect, it } from 'vitest';
import { buildTimetable, replanTimetable, toIcs, weekdayOf, type TimetableInput } from '../timetable';

const base: TimetableInput = {
  learnerId: 'lrn_kabir_singh',
  weekStart: '2026-11-23',
  now: '2026-11-22T12:00:00.000Z',
  availability: [
    ...(['mon', 'tue', 'wed', 'thu', 'fri'] as const).map((day) => ({ day, start: '17:00', end: '19:00' })),
    { day: 'sat', start: '10:00', end: '13:00' },
    { day: 'sun', start: '10:00', end: '12:00' },
  ],
  sessions: [{ id: 'ses_1', title: 'Maths with Rahul Verma', date: '2026-11-25', start: '17:00', end: '18:00' }],
  masteryStates: [
    { subtopicId: 'cbse-g8-maths-ch01-st1', lastTestedUtc: '2026-11-22T06:00:00.000Z', level: 4 }, // reviews due 23, 25, 29
    { subtopicId: 'cbse-g8-maths-ch01-st2', lastTestedUtc: '2026-11-01T06:00:00.000Z', level: 3 }, // r5 due Dec 1: outside
  ],
  gaps: [
    { id: 'gap_a', subtopicId: 'cbse-g8-maths-ch01-st2', code: 'G5', hoursToClose: 2.2, status: 'suspected', weeks: 0.7 },
    { id: 'gap_b', subtopicId: 'cbse-g8-maths-ch02-st1', code: 'G1', hoursToClose: 7.7, status: 'confirmed', weeks: 2.6 },
    { id: 'gap_c', subtopicId: 'x', code: 'G4', hoursToClose: 1, status: 'closed' },
  ],
  currentChapter: { chapterId: 'cbse-g8-maths-ch03', title: 'A Story of Numbers', hoursThisWeek: 2 },
  names: { 'cbse-g8-maths-ch01-st1': 'Perfect squares' },
};

describe('buildTimetable', () => {
  const t = buildTimetable(base);
  const kinds = (k: string) => t.blocks.filter((b) => b.kind === k);

  it('keeps fixed sessions and never overlaps blocks', () => {
    expect(kinds('session')).toHaveLength(1);
    const sorted = [...t.blocks].sort((a, b) => a.startUtc.localeCompare(b.startUtc));
    for (let i = 1; i < sorted.length; i++) expect(sorted[i].startUtc >= sorted[i - 1].endUtc).toBe(true);
  });
  it('holds back a 15% buffer every day', () => {
    expect(kinds('buffer')).toHaveLength(7);
    expect(t.bufferMinutes / t.capacityMinutes).toBeGreaterThan(0.13);
    expect(t.bufferMinutes / t.capacityMinutes).toBeLessThan(0.17);
  });
  it('puts the weekly test on Saturday', () => {
    expect(kinds('weekly_test')).toHaveLength(1);
    expect(weekdayOf(kinds('weekly_test')[0].date)).toBe('sat');
  });
  it('schedules reviews on their due days (1, 3, 7 days after the test)', () => {
    const r = kinds('review');
    expect(r.map((b) => b.date)).toEqual(['2026-11-23', '2026-11-25', '2026-11-29']);
    expect(r[0].title).toBe('Review 1/5: Perfect squares');
  });
  it('sizes gap blocks from hours to close, prerequisite gap first, closed gaps ignored', () => {
    const gb = kinds('gap');
    const a = gb.filter((b) => b.refId === 'gap_a').reduce((s, b) => s + b.minutes, 0);
    const bb = gb.filter((b) => b.refId === 'gap_b').reduce((s, b) => s + b.minutes, 0);
    expect(a).toBe(135); // 2.2 h in one week
    expect(bb).toBe(155); // 7.7 h over 3 weeks
    expect(gb.some((b) => b.refId === 'gap_c')).toBe(false);
    expect(gb[0].refId).toBe('gap_b');
  });
  it('reports what does not fit', () => {
    expect(t.plannedMinutes).toBeGreaterThan(0);
    expect(t.unscheduled.every((u) => u.minutes > 0)).toBe(true);
  });
});

describe('replanTimetable', () => {
  const t = buildTimetable(base);
  it('carries a missed block forward and keeps the past', () => {
    const missed = t.blocks.find((b) => b.kind === 'gap' && b.date === '2026-11-23')!;
    const now = '2026-11-23T14:00:00.000Z'; // 19:30 IST Monday
    const r = replanTimetable(t, { ...base, now }, { type: 'missed', blockIds: [missed.id] });
    const old = r.blocks.find((b) => b.id === missed.id)!;
    expect(old.status).toBe('missed');
    const carry = r.blocks.filter((b) => b.kind === 'carry_over');
    expect(carry).toHaveLength(1);
    expect(carry[0].date > '2026-11-23').toBe(true);
    expect(r.blocks.filter((b) => b.date === '2026-11-23' && b.kind !== 'buffer').every((b) => b.status !== 'planned' || b.kind === 'session')).toBe(true);
  });
  it('rebuilds gap blocks after a test result and respects locked blocks', () => {
    const lockMe = t.blocks.find((b) => b.kind === 'chapter')!;
    const locked = replanTimetable(t, base, { type: 'lock', blockIds: [lockMe.id] });
    expect(locked.blocks.find((b) => b.id === lockMe.id)?.locked).toBe(true);
    const r = replanTimetable(locked, base, { type: 'test_result', gaps: [{ id: 'gap_z', subtopicId: 's', code: 'G10', hoursToClose: 1, status: 'suspected' }] });
    const gb = r.blocks.filter((b) => b.kind === 'gap');
    expect(gb.every((b) => b.refId === 'gap_z' && b.minutes <= 20)).toBe(true);
    expect(r.blocks.find((b) => b.id === lockMe.id)).toBeTruthy();
  });
  it('reports an unplaceable weekly test and skips it when disabled', () => {
    const tiny = buildTimetable({ ...base, availability: [{ day: 'mon', start: '17:00', end: '17:30' }], gaps: [], currentChapter: undefined, masteryStates: [] });
    expect(tiny.unscheduled.some((u) => u.kind === 'weekly_test')).toBe(true);
    const none = buildTimetable({ ...base, weeklyTest: false });
    expect(none.blocks.some((b) => b.kind === 'weekly_test')).toBe(false);
  });
  it('flags full weeks', () => {
    const full = buildTimetable({ ...base, availability: [{ day: 'sat', start: '10:00', end: '11:30' }], carryOver: [{ ...t.blocks[0], minutes: 200, title: 'Big' }] });
    expect(full.unscheduled.map((u) => u.kind)).toEqual(expect.arrayContaining(['carry_over', 'review', 'gap', 'chapter']));
  });
});

describe('toIcs', () => {
  it('exports RFC 5545 events without buffers', () => {
    const t = buildTimetable(base);
    const ics = toIcs(t.blocks, { now: base.now, calendarName: 'Kabir, week 48' });
    expect(ics.startsWith('BEGIN:VCALENDAR\r\n')).toBe(true);
    expect(ics).toContain('DTSTART:20261125T113000Z'); // 17:00 IST
    expect(ics).toContain('SUMMARY:Maths with Rahul Verma');
    expect(ics).toContain('X-WR-CALNAME:Kabir\\, week 48');
    expect((ics.match(/BEGIN:VEVENT/g) ?? []).length).toBe(t.blocks.filter((b) => b.kind !== 'buffer').length);
  });
});
