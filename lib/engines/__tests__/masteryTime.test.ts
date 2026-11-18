import { describe, expect, it } from 'vitest';
import fx from '../__fixtures__/maths8.json';
import { BANDS } from '../config';
import { chapterTimeSummary, masteryTime, masteryTimeAllBands, practiceOpportunities, withMasteryHours } from '../masteryTime';
import { BAND_PARAMS } from '../config';
import type { Weight } from '../../types';

describe('masteryTime (sheet Mastery Time)', () => {
  it('practice opportunities match Mastery Inputs row 18', () => {
    expect(BANDS.map((b) => practiceOpportunities(BAND_PARAMS[b]))).toEqual([20, 14, 10, 6]);
  });

  it.each(fx.masteryTime.map((r) => [r.subtopicId, r] as const))('reproduces %s within 0.1 h', (_id, row) => {
    for (const b of BANDS) {
      const r = masteryTime({ weight: row.weight as Weight, teachingPeriods: row.teachingPeriods }, b);
      expect(r.instructionHours).toBeCloseTo(row.instructionHours, 5);
      expect(Math.abs(r.learnHours - (row.learnHours as Record<string, number>)[b])).toBeLessThanOrEqual(0.1 + 1e-9);
      expect(Math.abs(r.masterHours - (row.masterHours as Record<string, number>)[b])).toBeLessThanOrEqual(0.1 + 1e-9);
      expect(Math.abs(r.practiceBeyondClassHours - (row.practiceBeyondClassHours as Record<string, number>)[b])).toBeLessThanOrEqual(0.1 + 1e-9);
    }
  });

  it('reproduces every row exactly (not just within 0.1)', () => {
    let mismatches = 0;
    for (const row of fx.masteryTime) for (const b of BANDS) {
      const r = masteryTime({ weight: row.weight as Weight, teachingPeriods: row.teachingPeriods }, b);
      if (r.masterHours !== (row.masterHours as Record<string, number>)[b] || r.learnHours !== (row.learnHours as Record<string, number>)[b]) mismatches++;
    }
    expect(mismatches).toBe(0);
  });

  it('falls back to weight default periods and accepts overrides', () => {
    expect(masteryTime({ weight: 'H' }, 'average').masterHours).toBe(5.5);
    const faster = masteryTime({ weight: 'H' }, 'average', { startAccuracyPct: 65 });
    expect(faster.practiceOpportunities).toBe(6);
    expect(faster.masterHours).toBeLessThan(5.5);
  });

  it('fills Subtopic.learnHours / masterHours', () => {
    const s = withMasteryHours({ id: 'x', weight: 'S' as Weight, teachingPeriods: 3 });
    expect(s.masterHours).toEqual({ below_avg: 5.7, average: 4.2, above_avg: 3.4, excellent: 2.8 });
    expect(masteryTimeAllBands({ weight: 'L', teachingPeriods: 2 }).instructionHours).toBe(1.3);
  });
});

describe('chapterTimeSummary (sheet Mastery Summary)', () => {
  it.each(fx.masterySummary.map((c) => [c.chapterId, c] as const))('reproduces %s', (id, ch) => {
    const subs = fx.masteryTime.filter((r) => r.subtopicId.startsWith(id + '-')).map((r) => ({ weight: r.weight as Weight, teachingPeriods: r.teachingPeriods }));
    const s = chapterTimeSummary(subs);
    expect(s.instructionHours).toBe(ch.instructionHours);
    expect(s.masterHours).toEqual(ch.masterHours);
    expect(s.learnHours).toEqual(ch.learnHours);
    expect(s.suggestedWeeks).toBe(ch.suggestedWeeks);
  });
});
