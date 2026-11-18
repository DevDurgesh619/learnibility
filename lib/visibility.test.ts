import { describe, expect, it } from 'vitest';
import type { ProfileValue, Tier } from './types';
import { canUseForPurpose, valuesForPurpose, visibilityFor, visibleProfile } from './visibility';

const v = (paramId: string, tier: Tier, value: unknown): ProfileValue => ({
  learnerId: 'lrn_meera_iyer', paramId, value, source: 'M1', asOfUtc: '2026-11-01T00:00:00Z', confidence: 'medium', tier,
});
const meera = [v('p1', 'T1', 9), v('p150', 'T2', 'screened stress: high'), v('p120', 'T3', 'sleep 5.5h'), v('p29', 'C', 'assent v2')];

describe('role visibility', () => {
  it('student and counsellor see everything verbatim', () => {
    for (const role of ['student', 'counsellor'] as const) {
      const out = visibleProfile(meera, role, { isSelf: true });
      expect(out).toHaveLength(4);
      expect(out.every((x) => x.mode === 'full')).toBe(true);
    }
  });

  it('parent sees T2 and T3 only as summaries, never the screened answer', () => {
    const out = visibleProfile(meera, 'parent');
    expect(out.find((x) => x.paramId === 'p150')).toEqual({ paramId: 'p150', tier: 'T2', mode: 'summary', asOfUtc: '2026-11-01T00:00:00Z' });
    expect(JSON.stringify(out)).not.toContain('screened stress');
    expect(JSON.stringify(out)).not.toContain('sleep');
    expect(out.find((x) => x.paramId === 'p1')?.value).toBe(9);
  });

  it('teacher and mentor see T1 only', () => {
    for (const role of ['teacher', 'mentor'] as const) {
      expect(visibleProfile(meera, role).map((x) => x.paramId)).toEqual(['p1']);
    }
  });

  it('tutor sees only what the student shared', () => {
    expect(visibleProfile(meera, 'tutor')).toEqual([]);
    expect(visibleProfile(meera, 'tutor', { sharedParamIds: ['p1', 'p120'] }).map((x) => x.paramId)).toEqual(['p1']);
  });

  it('matrix spot checks', () => {
    expect(visibilityFor('parent', 'C')).toBe('full');
    expect(visibilityFor('tutor', 'T1')).toBe('shared_only');
  });
});

describe('model-use rules', () => {
  it('T3 never feeds ranking, admissions, career fit or work allocation', () => {
    for (const p of ['ranking', 'admissions_fit', 'career_fit', 'work_allocation', 'tutor_matching'] as const) {
      expect(canUseForPurpose('T3', p)).toBe(false);
    }
    expect(canUseForPurpose('T3', 'support_adaptation')).toBe(true);
    expect(canUseForPurpose('T2', 'career_fit')).toBe(true);
    expect(canUseForPurpose('C', 'support_adaptation')).toBe(false);
    expect(valuesForPurpose(meera, 'career_fit').map((x) => x.paramId)).toEqual(['p1', 'p150']);
  });
});
