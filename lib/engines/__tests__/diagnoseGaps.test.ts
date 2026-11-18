import { describe, expect, it } from 'vitest';
import fx from '../__fixtures__/maths8.json';
import { diagnoseGaps, diagnoseSubtopic, gapsFrom } from '../diagnoseGaps';
import { pathFor, questions, responsesFrom, subtopics } from './helpers';

const gc = fx.gapCalculator;
const sub = subtopics.find((s) => s.id === gc.subtopicId)!;
const base = { learnerId: gc.learnerId, band: 'average' as const, weeklyHours: gc.weeklyHours };

describe('diagnoseGaps: Gap Calculator worked example (lrn_example, square roots, Average)', () => {
  const responses = responsesFrom(gc.subtopicId, gc.results as number[], { confidenceWrong: 4 });
  const [d] = diagnoseGaps(responses, pathFor(gc.subtopicId), {
    ...base,
    subtopics,
    signals: { [gc.subtopicId]: { minutesTaken: gc.minutesTaken, wordProblemPattern: gc.wordProblemPattern } },
  });

  it('gives the same level, gap and size', () => {
    expect(d.itemsOnPath).toBe(8);
    expect(d.level).toBe(gc.expected.level);
    expect(d.size).toBe(gc.expected.size);
    expect(d.primary).toBe(gc.expected.primary);
    expect(d.scorePct).toBe(gc.expected.scorePct);
    expect(d.passed).toEqual({ C1: true, C2: true, C3: true, C4: false });
    expect(d.masteryRuleMet).toBe(false);
  });
  it('raises the same secondary flags', () => {
    expect(d.flags.overConfident).toBe(true);
    expect(d.flags.careless).toBe(false);
    expect(d.flags.speed).toBe(false);
    expect(d.flags.engagement).toBe(false);
    expect(d.flags.insufficientEvidence).toBe(false);
    expect(d.secondaryFlags).toEqual(['G9']);
  });
  it('gives the same hours, weeks and practice opportunities', () => {
    expect(d.hoursToMaster).toEqual(gc.expected.hoursByBand);
    expect(d.hours).toBe(2.2);
    expect(d.teacherHours).toBe(0.8);
    expect(d.selfHours).toBe(1.4);
    expect(d.weeksToClose).toBe(gc.expected.weeks);
    expect(d.practiceOpportunitiesNeeded).toBe(gc.expected.practiceOpportunities);
    expect(d.confirmingProbe).toContain('C4-D3 item with a hint');
    expect(d.gap).toMatchObject({ code: 'G5', level: 3, size: 2, hoursToClose: 2.2, status: 'suspected', learnerId: 'lrn_example' });
  });
});

describe('diagnoseGaps: Gap Log row (L2, G3, 3.6 h, 1.2 weeks)', () => {
  it('reproduces it', () => {
    const r = responsesFrom(fx.gapLog.subtopicId, [1, 1, 0, 0, 0, 0, 0, 0]);
    const d = diagnoseSubtopic(pathFor(fx.gapLog.subtopicId), r, sub, { ...base, signals: { [sub.id]: { wordProblemPattern: false } } });
    expect(d.level).toBe(fx.gapLog.level);
    expect(d.primary).toBe(fx.gapLog.primary);
    expect(d.hours).toBe(fx.gapLog.hours);
    expect(d.weeksToClose).toBe(fx.gapLog.weeks);
  });
});

describe('decision rule branches', () => {
  const H = sub.id;
  const S = 'cbse-g8-maths-ch01-st1';
  const L = subtopics.find((s) => s.weight === 'L')!.id;
  const run = (id: string, res: (number | null)[], signals = {}, band: 'average' | 'below_avg' = 'average') =>
    diagnoseSubtopic(pathFor(id), responsesFrom(id, res), subtopics.find((s) => s.id === id)!, { ...base, band, signals: { [id]: { wordProblemPattern: false, ...signals } } });

  it('L0 → G1 with prerequisite extra time; confirmed when the probe fails; G2 when it passes', () => {
    const d = run(H, [0, 1, 1, 1, 1, 0, 0, 0], { prerequisiteProbePassed: false });
    expect(d.level).toBe(0);
    expect(d.primary).toBe('G1');
    expect(d.hours).toBe(7.7); // 5.5 × 1.4
    expect(d.gap?.status).toBe('confirmed');
    expect(run(H, [0, 1, 1, 1, 1, 0, 0, 0], { prerequisiteProbePassed: true }).primary).toBe('G2');
  });
  it('L1 → G2, L2 → G3', () => {
    expect(run(S, [1, 0, 1, 1, 1, 1]).primary).toBe('G2');
    expect(run(S, [1, 1, 1, 0, 1, 1]).primary).toBe('G3');
  });
  it('careless flag: D2 wrong, D3 right in the same group', () => {
    const d = run(S, [1, 1, 1, 0, 1, 1]);
    expect(d.flags.careless).toBe(true);
    expect(d.secondaryFlags).toContain('G4');
  });
  it('L4 → G4 without retention data, G6 when retention < 70, L5 when retained', () => {
    expect(run(S, [1, 1, 1, 1, 1, 1]).level).toBe(4);
    expect(run(S, [1, 1, 1, 1, 1, 1]).primary).toBe('G4');
    expect(run(S, [1, 1, 1, 1, 1, 1], { retentionPct: 60 }).primary).toBe('G6');
    const m = run(S, [1, 1, 1, 1, 1, 1], { retentionPct: 85 });
    expect(m.level).toBe(5);
    expect(m.primary).toBeNull();
    expect(m.gap).toBeNull();
    expect(m.hours).toBe(0);
  });
  it('H C4 alternative rule: Q6 and Q8 right passes C4 even with Q7 wrong', () => {
    expect(run(H, [1, 1, 1, 1, 1, 1, 0, 1]).passed.C4).toBe(true);
  });
  it('L path uses its own items', () => {
    const d = run(L, [0, 1, 1, 1, 1]);
    expect(d.passed.C1).toBe(true);
    expect(d.level).toBe(4);
  });
  it('two blanks → G10 engagement', () => {
    const d = run(S, [1, 1, null, 1, null, 0]);
    expect(d.primary).toBe('G10');
    expect(d.blank).toBe(2);
  });
  it('fewer than 4 attempted → insufficient evidence, no primary unless engagement', () => {
    const d = run(L, [1, 0, null, null, null]);
    expect(d.flags.insufficientEvidence).toBe(true);
    expect(d.primary).toBe('G10');
    const e = diagnoseSubtopic(pathFor(S), responsesFrom(S, [1, 0, 1]), subtopics.find((s) => s.id === S)!, base);
    expect(e.flags.insufficientEvidence).toBe(true);
  });
  it('speed flag: slow and last item wrong', () => {
    const d = run(S, [1, 1, 1, 1, 1, 0], { minutesTaken: 40 });
    expect(d.flags.speed).toBe(true);
    expect(d.secondaryFlags).toContain('G8');
  });
  it('language auto-detection when no signal is given', () => {
    const path = pathFor(S);
    const res = path.map((q) => ({ questionId: q.id, correct: q.type !== 'multi_step', secondsTaken: 60 }));
    const d = diagnoseSubtopic(path, res, subtopics.find((s) => s.id === S)!, base);
    expect(typeof d.flags.language).toBe('boolean');
  });
  it('under-confidence on right items flags G9', () => {
    const path = pathFor(S);
    const res = path.map((q) => ({ questionId: q.id, correct: true, secondsTaken: 60, confidence: 1 as const }));
    expect(diagnoseSubtopic(path, res, subtopics.find((s) => s.id === S)!, base).flags.underConfident).toBe(true);
  });
  it('split advice when over 2 weeks', () => {
    const d = diagnoseSubtopic(pathFor(H), responsesFrom(H, [0, 0, 0, 0, 1, 1, 1, 1]), sub, { ...base, weeklyHours: 1 });
    expect(d.splitAdvice).not.toBeNull();
  });
});

describe('diagnoseGaps over a whole chapter', () => {
  it('returns one diagnosis per subtopic, worst first, and gapsFrom extracts Gaps', () => {
    const ch = questions.filter((q) => q.chapterId === 'cbse-g8-maths-ch01');
    const responses = ch.map((q, i) => ({ questionId: q.id, correct: i % 3 !== 0, secondsTaken: 60 }));
    const ds = diagnoseGaps(responses, ch, { ...base, subtopics: Object.fromEntries(subtopics.map((s) => [s.id, s])) });
    expect(ds).toHaveLength(4);
    for (let i = 1; i < ds.length; i++) expect(ds[i].level).toBeGreaterThanOrEqual(ds[i - 1].level);
    expect(gapsFrom(ds).length).toBeGreaterThan(0);
    expect(() => diagnoseGaps(responses, ch, { ...base, subtopics: [] })).toThrow();
  });
});
