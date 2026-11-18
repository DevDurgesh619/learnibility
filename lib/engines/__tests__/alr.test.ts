import { describe, expect, it } from 'vitest';
import fx from '../__fixtures__/maths8.json';
import { alrInputsFromResponses, alrYearToDate, bandFromLrs, computeAlr, meanConfidenceError, normaliseLrs, pctCorrect, weightedPct } from '../alr';
import { questions } from './helpers';

const row = fx.alrTracker;

describe('computeAlr: ALR Tracker row 1', () => {
  const r = computeAlr({ ...row, learnerId: 'lrn_example' });
  it('gives dK 0.75, R 0.89, TQ 0.80, CE 0.77, ECV 0.67, MCI 0.75, LRS 0.79', () => {
    expect(r.indices).toEqual({ dK: 0.75, R: 0.89, TQ: 0.8, CE: 0.77, ECV: 0.67, MCI: 0.75 });
    expect(r.LRS).toBe(0.79);
    expect(row.expected).toMatchObject({ ...r.indices, LRS: r.LRS });
  });
  it('bands it Above average', () => {
    expect(r.band).toBe('above_avg');
    expect(row.expectedBand).toBe('Above average');
    expect(r.snapshot).toMatchObject({ learnerId: 'lrn_example', chapterId: 'cbse-g8-maths-ch01', LRS: 0.79, band: 'above_avg' });
    expect(r.missing).toEqual([]);
    expect(r.decayPerDay).toBeCloseTo(0.0166, 3);
  });
  it('other weight sets change the composite', () => {
    expect(computeAlr(row, 'exam_oriented').LRS).not.toBe(0.79);
    expect(computeAlr(row, { dK: 1, R: 0, TQ: 0, CE: 0, ECV: 0, MCI: 0 }).LRS).toBe(0.75);
  });
});

describe('band cut-offs', () => {
  it.each([[0.8, 'excellent'], [0.79, 'above_avg'], [0.65, 'above_avg'], [0.64, 'average'], [0.45, 'average'], [0.44, 'below_avg']])('%s → %s', (v, b) => {
    expect(bandFromLrs(v as number)).toBe(b);
  });
});

describe('missing data', () => {
  it('rescales weights over present indices', () => {
    const r = computeAlr({ chapterId: 'c', preWeightedPct: 40, postWeightedPct: 85 });
    expect(r.indices.dK).toBe(0.75);
    expect(r.LRS).toBe(0.75);
    expect(r.missing).toEqual(['R', 'TQ', 'CE', 'ECV', 'MCI']);
  });
  it('no dK → no LRS', () => {
    const r = computeAlr({ chapterId: 'c', practisedPct: 50, transferPct: 25 });
    expect(r.LRS).toBeNull();
    expect(r.band).toBeNull();
    expect(r.snapshot).toBeNull();
    expect(r.decayPerDay).toBeNull();
  });
});

describe('inputs from raw responses', () => {
  const ch = questions.filter((q) => q.chapterId === 'cbse-g8-maths-ch01');
  const post = ch.map((q) => ({ questionId: q.id, correct: q.alrRole !== 'transfer_probe' || q.difficulty === 'D3', secondsTaken: q.minutes * 60, confidence: 4 as const }));
  const pre = ch.map((q) => ({ questionId: q.id, correct: q.conceptGroup === 'C1', secondsTaken: 60 }));
  const delayed = ch.filter((q) => q.alrRole === 'retention_probe').map((q, i) => ({ questionId: q.id, correct: i % 4 !== 0, secondsTaken: 60 }));
  it('builds a full set of inputs and a band', () => {
    const inp = alrInputsFromResponses({ learnerId: 'lrn_x', chapterId: 'cbse-g8-maths-ch01', questions, pre, post, delayed, meanAttemptsToMastery: 2, hintRate: 0.1 });
    expect(inp.minutesAllotted).toBe(68);
    expect(inp.preWeightedPct).toBe(33.3); // C1-D2 right, C3-D2 wrong, marks-weighted
    expect(inp.retentionPostPct).toBe(100);
    expect(inp.retention7dPct).toBe(75);
    const r = computeAlr(inp);
    expect(r.missing).toEqual([]);
    expect(r.band).not.toBeNull();
  });
  it('helpers', () => {
    expect(weightedPct([], [])).toBeUndefined();
    expect(pctCorrect([], [])).toBeUndefined();
    expect(meanConfidenceError([])).toBeUndefined();
    expect(meanConfidenceError([{ questionId: 'a', correct: true, secondsTaken: 1, confidence: 5 }, { questionId: 'b', correct: false, secondsTaken: 1, confidence: 1 }])).toBe(0.1);
    const inp = alrInputsFromResponses({ learnerId: 'l', chapterId: 'cbse-g8-maths-ch01', questions, post });
    expect(inp.preWeightedPct).toBeUndefined();
  });
});

describe('year to date and normalisation', () => {
  it('averages filled chapters', () => {
    const a = computeAlr(row);
    const b = computeAlr({ chapterId: 'c2', preWeightedPct: 50, postWeightedPct: 75 });
    const y = alrYearToDate([a, b]);
    expect(y.dK).toBe(0.63);
    expect(y.R).toBe(0.89);
  });
  it('min-max scales', () => {
    expect(normaliseLrs([0.4, 0.6, 0.8])).toEqual([0, 0.5, 1]);
    expect(normaliseLrs([0.5, 0.5])).toEqual([0.5, 0.5]);
    expect(normaliseLrs([])).toEqual([]);
  });
});
