import { describe, expect, it } from 'vitest';
import paramsFile from '@/data/profile/parameters.json';
import type { ProfileParameter } from '@/lib/types';
import { buildStudent360, displayValue, isStale, overallCompleteness } from './profile360';
import { riskFlags } from './risk';

const params = (paramsFile as { items: ProfileParameter[] }).items;
const now = new Date('2026-11-18T03:30:00Z');

describe('buildStudent360', () => {
  it('groups all 430 parameters into the 12 sections', () => {
    const s = buildStudent360(params, [], now);
    expect(s).toHaveLength(12);
    expect(s.reduce((a, x) => a + x.total, 0)).toBe(430);
    expect(overallCompleteness(s)).toBe(0);
    expect(s[0]!.densityLabel).toBe('Sparse');
  });
  it('uses the latest value and counts density, confidence and staleness', () => {
    const s = buildStudent360(params, [
      { paramId: 'p1', value: 9, source: 'M1', asOfUtc: '2026-04-01T00:00:00Z', confidence: 'high', tier: 'T1' },
      { paramId: 'p1', value: 8, source: 'M1', asOfUtc: '2025-04-01T00:00:00Z', confidence: 'low', tier: 'T1' },
      { paramId: 'p149', value: 2, source: 'M1', asOfUtc: '2026-08-01T00:00:00Z', confidence: 'medium', tier: 'T3' },
    ], now);
    const acad = s.find((x) => x.section === 'Academic Profile')!;
    expect(acad.filled).toBe(1);
    expect(acad.rows.find((r) => r.param.id === 'p1')!.value!.value).toBe(9);
    expect(acad.highConfidence).toBe(1);
    const all = s.flatMap((x) => x.rows);
    expect(all.find((r) => r.param.id === 'p149')!.stale).toBe(true);
  });
  it('formats values', () => {
    expect(displayValue(['a', 'b'])).toBe('a, b');
    expect(displayValue({ R: 60, I: 80 })).toBe('R: 60 · I: 80');
    expect(displayValue(0.456)).toBe('0.46');
    expect(displayValue('above_avg')).toBe('above avg');
    expect(isStale('Once', '2000-01-01T00:00:00Z', now)).toBe(false);
  });
});

describe('riskFlags', () => {
  it('raises deadline, wellbeing, data, learning and request flags in severity order', () => {
    const f = riskFlags({
      learnerId: 'lrn_x', now,
      applications: [{ id: 'a1', title: 'UCL Economics', deadlineUtc: '2026-11-23T00:00:00Z', openItems: 2 }, { id: 'a2', title: 'Far', deadlineUtc: '2027-01-15T00:00:00Z', openItems: 3 }],
      wellbeing: { p149: { value: 2, asOfUtc: '2026-11-10T00:00:00Z' }, p109: { value: 'high', asOfUtc: '2026-11-10T00:00:00Z' } },
      completeness: 0.05, lastAssessmentUtc: '2026-10-01T00:00:00Z', lrsBand: 'below_avg', gapCodes: ['G10'], missedTasks7d: 4,
      pendingRequests: [{ id: 'r1', createdUtc: '2026-11-14T00:00:00Z', summary: 'Move Thursday maths' }],
    });
    const kinds = f.map((x) => x.kind);
    expect(kinds).toContain('deadline');
    expect(f.filter((x) => x.kind === 'deadline')).toHaveLength(1);
    expect(f[0]!.severity).toBe('high');
    expect(kinds).toContain('request');
    expect(f.some((x) => x.id.endsWith('wb-due'))).toBe(false);
    expect(f.some((x) => x.id.endsWith('data-assessment'))).toBe(true);
  });
  it('asks for a check-in when none is on record', () => {
    const f = riskFlags({ learnerId: 'lrn_y', now, lastAssessmentUtc: '2026-11-15T00:00:00Z' });
    expect(f.map((x) => x.title)).toEqual(['Monthly wellbeing check-in due']);
  });
});
