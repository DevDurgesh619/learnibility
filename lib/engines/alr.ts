/**
 * Engine 4: Academic Learning Rate indices, composite LRS and band, per learner per chapter.
 * Source: workbook sheets "ALR Method" (index definitions D7-D12, LRS weights rows 16-21,
 * difficulty proxy weights rows 26-30, band cut-offs rows 34-37) and "ALR Tracker" (formulas N4-U4).
 *
 *   dK  = max(0, (post − pre) ÷ (100 − pre))                 weighted % uses D1..D5 = 0.8..1.6
 *   R   = min(1, retention 7-day % ÷ retention post-test %)
 *   TQ  = transfer-probe % ÷ practised-item %
 *   CE  = dK ÷ (minutes taken ÷ minutes allotted) × (1 − hint/re-attempt rate)
 *   ECV = 1 ÷ mean attempts to mastery on errored subtopics
 *   MCI = 1 − mean |confidence − correct|
 *   LRS = Σ weight × index, with dK, TQ and CE capped at 1 (indices rounded to 0.01 first, as the sheet does)
 *   band: ≥ 0.80 excellent, ≥ 0.65 above average, ≥ 0.45 average, else below average
 *
 * Deviation, documented: the sheet treats a blank index as 0 in the LRS. Here a missing index is left out
 * and the remaining weights are rescaled to sum to 1, so a learner without a 7-day probe yet is not
 * pushed down a band. With all six present the result is identical to the sheet.
 */
import type { AlrSnapshot, Band, Difficulty, ItemResponse, Question } from '../types';
import { ALR_WEIGHTS, AlrIndex, AlrWeightSet, CONFIDENCE_PROB, DIFFICULTY_WEIGHT, LRS_BAND_CUTOFFS } from './config';
import { round } from './util';

export interface AlrChapterInputs {
  learnerId?: string;
  chapterId: string;
  preWeightedPct?: number;
  postWeightedPct?: number;
  retentionPostPct?: number;
  retention7dPct?: number;
  practisedPct?: number;
  transferPct?: number;
  minutesTaken?: number;
  minutesAllotted?: number;
  /** 0-1 */
  hintRate?: number;
  meanAttemptsToMastery?: number;
  /** Mean |confidence − correct|, 0-1. */
  meanConfidenceError?: number;
}

export type AlrIndices = Record<AlrIndex, number | null>;

export interface AlrResult {
  indices: AlrIndices;
  LRS: number | null;
  band: Band | null;
  action: string | null;
  /** Indices that were missing and left out of the LRS. */
  missing: AlrIndex[];
  /** λ per day from R (ALR Method D8). */
  decayPerDay: number | null;
  /** Contract snapshot (missing indices as 0); null when LRS cannot be computed. */
  snapshot: AlrSnapshot | null;
}

const has = (...xs: (number | undefined)[]) => xs.every((x) => x !== undefined && x !== null && !Number.isNaN(x));

export function bandFromLrs(lrs: number): Band {
  return LRS_BAND_CUTOFFS.find((c) => lrs >= c.min)!.band;
}

export function computeAlr(input: AlrChapterInputs, weights: AlrWeightSet | Record<AlrIndex, number> = 'deep_mastery'): AlrResult {
  const w = typeof weights === 'string' ? ALR_WEIGHTS[weights] : weights;
  const i = input;
  const dK = has(i.preWeightedPct, i.postWeightedPct) ? round(Math.max(0, (i.postWeightedPct! - i.preWeightedPct!) / (100 - i.preWeightedPct!)), 2) : null;
  const R = has(i.retentionPostPct, i.retention7dPct) && i.retentionPostPct! > 0 ? round(Math.min(1, i.retention7dPct! / i.retentionPostPct!), 2) : null;
  const TQ = has(i.practisedPct, i.transferPct) && i.practisedPct! > 0 ? round(i.transferPct! / i.practisedPct!, 2) : null;
  const CE = dK !== null && has(i.minutesTaken, i.minutesAllotted) && i.minutesTaken! > 0 ? round((dK / (i.minutesTaken! / i.minutesAllotted!)) * (1 - (i.hintRate ?? 0)), 2) : null;
  const ECV = has(i.meanAttemptsToMastery) && i.meanAttemptsToMastery! > 0 ? round(1 / i.meanAttemptsToMastery!, 2) : null;
  const MCI = has(i.meanConfidenceError) ? round(1 - i.meanConfidenceError!, 2) : null;
  const indices: AlrIndices = { dK, R, TQ, CE, ECV, MCI };
  const capped: Record<AlrIndex, (v: number) => number> = { dK: (v) => Math.min(1, v), R: (v) => v, TQ: (v) => Math.min(1, v), CE: (v) => Math.min(1, v), ECV: (v) => v, MCI: (v) => v };

  const present = (Object.keys(indices) as AlrIndex[]).filter((k) => indices[k] !== null);
  const missing = (Object.keys(indices) as AlrIndex[]).filter((k) => indices[k] === null);
  let LRS: number | null = null;
  if (dK !== null) {
    const wsum = present.reduce((s, k) => s + w[k], 0);
    LRS = wsum > 0 ? round(present.reduce((s, k) => s + w[k] * capped[k](indices[k]!), 0) / wsum, 2) : null;
  }
  const band = LRS === null ? null : bandFromLrs(LRS);
  return {
    indices,
    LRS,
    band,
    action: band ? LRS_BAND_CUTOFFS.find((c) => c.band === band)!.action : null,
    missing,
    decayPerDay: R !== null && R > 0 ? round(-Math.log(R) / 7, 4) : null,
    snapshot:
      LRS !== null && band
        ? { learnerId: i.learnerId ?? '', chapterId: i.chapterId, dK: dK ?? 0, R: R ?? 0, TQ: TQ ?? 0, CE: CE ?? 0, ECV: ECV ?? 0, MCI: MCI ?? 0, LRS, band }
        : null,
  };
}

/** Marks-weighted % using the difficulty proxy weights (ALR Tracker note B20). */
export function weightedPct(responses: ItemResponse[], questions: Question[]): number | undefined {
  const byQ = new Map(responses.map((r) => [r.questionId, r]));
  let num = 0, den = 0;
  for (const q of questions) {
    const wt = q.marks * DIFFICULTY_WEIGHT[q.difficulty as Difficulty];
    den += wt;
    if (byQ.get(q.id)?.correct) num += wt;
  }
  return den ? round((num / den) * 100, 1) : undefined;
}

/** Plain % correct on a set of questions (undefined if empty). */
export function pctCorrect(responses: ItemResponse[], questions: Question[]): number | undefined {
  if (!questions.length) return undefined;
  const ok = new Set(responses.filter((r) => r.correct).map((r) => r.questionId));
  return round((questions.filter((q) => ok.has(q.id)).length / questions.length) * 100, 1);
}

/** Mean |confidence − correct| with confidence 1..5 → 0.1..0.9 (ALR Method D12). */
export function meanConfidenceError(responses: ItemResponse[]): number | undefined {
  const rated = responses.filter((r) => r.confidence !== undefined);
  if (!rated.length) return undefined;
  return round(rated.reduce((s, r) => s + Math.abs(CONFIDENCE_PROB[r.confidence!] - (r.correct ? 1 : 0)), 0) / rated.length, 2);
}

export interface ChapterEvidence {
  learnerId: string;
  chapterId: string;
  questions: Question[];
  pre?: ItemResponse[];
  post: ItemResponse[];
  /** 7-day delayed re-test of the retention probes. */
  delayed?: ItemResponse[];
  minutesAllotted?: number;
  hintRate?: number;
  meanAttemptsToMastery?: number;
}

/** Build ALR inputs from raw item responses for one chapter. Pre-test uses the C1-D2 and C3-D2 items. */
export function alrInputsFromResponses(e: ChapterEvidence): AlrChapterInputs {
  const qs = e.questions.filter((q) => q.chapterId === e.chapterId);
  const preItems = qs.filter((q) => (q.conceptGroup === 'C1' || q.conceptGroup === 'C3') && q.difficulty === 'D2');
  const retention = qs.filter((q) => q.alrRole === 'retention_probe');
  const practised = qs.filter((q) => q.alrRole !== 'transfer_probe' && q.conceptGroup !== 'C4' && Number(q.difficulty.slice(1)) <= 3);
  const transfer = qs.filter((q) => q.alrRole === 'transfer_probe');
  const postIds = new Set(e.post.map((r) => r.questionId));
  return {
    learnerId: e.learnerId,
    chapterId: e.chapterId,
    preWeightedPct: e.pre ? weightedPct(e.pre, preItems) : undefined,
    postWeightedPct: weightedPct(e.post, qs),
    retentionPostPct: pctCorrect(e.post, retention),
    retention7dPct: e.delayed ? pctCorrect(e.delayed, retention) : undefined,
    practisedPct: pctCorrect(e.post, practised),
    transferPct: pctCorrect(e.post, transfer),
    minutesTaken: round(e.post.reduce((s, r) => s + r.secondsTaken, 0) / 60, 1),
    minutesAllotted: e.minutesAllotted ?? qs.filter((q) => postIds.has(q.id)).reduce((s, q) => s + q.minutes, 0),
    hintRate: e.hintRate,
    meanAttemptsToMastery: e.meanAttemptsToMastery,
    meanConfidenceError: meanConfidenceError(e.post),
  };
}

/** Year-to-date means of filled chapters (ALR Tracker row 18). */
export function alrYearToDate(results: AlrResult[]): AlrIndices & { LRS: number | null } {
  const mean = (xs: (number | null)[]) => {
    const v = xs.filter((x): x is number => x !== null);
    return v.length ? round(v.reduce((a, b) => a + b, 0) / v.length, 2) : null;
  };
  const k: AlrIndex[] = ['dK', 'R', 'TQ', 'CE', 'ECV', 'MCI'];
  const out = Object.fromEntries(k.map((x) => [x, mean(results.map((r) => r.indices[x]))])) as AlrIndices;
  return { ...out, LRS: mean(results.map((r) => r.LRS)) };
}

/** Min-max scale LRS across a cohort before banding (ALR Tracker note B21). */
export function normaliseLrs(values: number[]): number[] {
  if (!values.length) return [];
  const lo = Math.min(...values), hi = Math.max(...values);
  return values.map((v) => (hi === lo ? 0.5 : round((v - lo) / (hi - lo), 2)));
}
