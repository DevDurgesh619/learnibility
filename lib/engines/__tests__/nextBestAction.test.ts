import { describe, expect, it } from 'vitest';
import { nextBestAction } from '../nextBestAction';

const now = '2026-11-21T04:30:00.000Z'; // Saturday 10:00 IST

describe('nextBestAction', () => {
  it('ranks a near deadline, due reviews, the weekly test, then gaps', () => {
    const a = nextBestAction({
      learnerId: 'lrn_ananya_kapoor', now, grade: 12,
      deadlines: [{ id: 'd1', title: 'Common App essay draft', dueUtc: '2026-11-24T18:00:00.000Z' }, { id: 'd2', title: 'Far', dueUtc: '2027-01-01T00:00:00.000Z' }],
      reviewsDue: [{ id: 'r1', title: 'Review: Perfect squares', dueUtc: '2026-11-21T00:00:00.000Z' }, { id: 'r2', title: 'Later', dueUtc: '2026-11-25T00:00:00.000Z' }],
      weeklyTest: { dueUtc: '2026-11-21T04:00:00.000Z', taken: false },
      gaps: [{ id: 'g1', subtopicId: 's1', code: 'G5', hoursToClose: 2.2 }, { id: 'g2', subtopicId: 's2', code: 'G1', hoursToClose: 7.7 }, { id: 'g3', subtopicId: 's3', code: 'G4', hoursToClose: 1, status: 'closed' }],
      profileCompletionPct: 60,
    }, 10);
    expect(a.map((x) => x.kind)).toEqual(['deadline', 'review', 'weekly_test', 'gap', 'gap', 'profile', 'career']);
    expect(a[0].reason).toBe('Due in 3 days.');
    expect(a[1].title).toBe('Review: Perfect squares');
    expect(a[3].refId).toBe('g2');
    expect(a[3].reason).toContain('prerequisite');
    expect(a.some((x) => x.refId === 'd2' || x.refId === 'g3')).toBe(false);
  });
  it('handles overdue and same-day deadlines, multiple reviews, early-week test and grade 8', () => {
    const a = nextBestAction({
      learnerId: 'l', now: '2026-11-17T04:30:00.000Z', grade: 8,
      deadlines: [{ id: 'o', title: 'Overdue', dueUtc: '2026-11-15T00:00:00.000Z' }, { id: 't', title: 'Today', dueUtc: '2026-11-17T10:00:00.000Z' }],
      reviewsDue: [{ id: 'r1', title: 'a', dueUtc: '2026-11-16T00:00:00.000Z' }, { id: 'r2', title: 'b', dueUtc: '2026-11-17T00:00:00.000Z' }],
      weeklyTest: { dueUtc: '2026-11-21T04:00:00.000Z', taken: false },
    }, 10);
    expect(a[0].reason).toBe('Overdue by 2 days.');
    expect(a[1].reason).toBe('Due today.');
    expect(a.find((x) => x.kind === 'review')!.title).toBe('2 quick reviews');
    expect(a.find((x) => x.kind === 'weekly_test')!.score).toBe(40);
    expect(a.find((x) => x.kind === 'career')!.score).toBe(10);
  });
  it('drops completed items and respects the limit', () => {
    const a = nextBestAction({ learnerId: 'l', now, weeklyTest: { dueUtc: now, taken: true }, careersShortlisted: 2, profileCompletionPct: 95 });
    expect(a).toEqual([]);
    expect(nextBestAction({ learnerId: 'l', now, grade: 10 }, 1)[0].reason).toContain('subjects and streams');
  });
});
