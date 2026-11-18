/**
 * Onboarding scoring: turns one finished onboarding form into a starting profile.
 *
 *  - Part A: percent per subject group from the ladder weights (D1 1, D2 2, D3 3; max 3 per slot),
 *    band by the workbook's LRS cut-offs used as score cut-offs (<45 below avg, 45-64 average,
 *    65-79 above avg, >=80 excellent), prerequisite-gap index, and one suspected gap per wrong item
 *    (primary code from the item, secondary flags G4 / G8 / G9 from the same paper).
 *  - Part B: percent per reasoning domain and processing speed.
 *  - Part C and parent form: each answer written to its parameter; RIASEC code from 12 items.
 *
 * Every value is written with its source method and low confidence (medium for parent-declared facts),
 * as the blueprint says, until chapter checks replace it. Pure: pass `nowUtc`.
 */
import type { Band, Difficulty, GapCode, Level, SourceMethod, Tier } from '../types/enums';
import type { ProfileValue } from '../types/learner';
import type {
  BandCutoff,
  OnboardingAcademicItem,
  OnboardingFormFile,
  OnboardingReasoningItem,
  OnboardingSurveyItem,
  ReasoningDomain,
} from '../types/onboarding';
import { DEFAULT_LADDER } from './ladder';

export interface AcademicResponse {
  questionId: string;
  correct: boolean;
  secondsTaken: number;
  confidence?: 1 | 2 | 3 | 4 | 5;
}
export interface ReasoningResponse {
  questionId: string;
  answer: string;
  secondsTaken: number;
}
export interface SurveyResponse {
  questionId: string;
  value: string | number | (string | number)[];
}
export interface OnboardingResponses {
  academic: AcademicResponse[];
  reasoning: ReasoningResponse[];
  survey: SurveyResponse[];
}

export interface GroupResult {
  group: string;
  label: string;
  itemsSeen: number;
  correct: number;
  percent: number;
  band: Band;
  prerequisiteGapIndex: number;
  meanConfidence: number | null;
  highestSustained: Difficulty | null;
}

export interface SuspectedGap {
  learnerId: string;
  subtopicId: string;
  subjectId: string;
  code: GapCode;
  secondaryFlags: GapCode[];
  level: Level;
  size: number;
  status: 'suspected';
  evidenceItemIds: string[];
  /** For the "why" panel. */
  reason: string;
}

export interface OnboardingResult {
  formId: string;
  groups: GroupResult[];
  suspectedGaps: SuspectedGap[];
  reasoning: Record<ReasoningDomain, number>;
  processingSpeed: number;
  riasec: { scores: Record<'R' | 'I' | 'A' | 'S' | 'E' | 'C', number>; code: string };
  profile: ProfileValue[];
}

export const DEFAULT_BANDS: BandCutoff[] = [
  { band: 'excellent', minPercent: 80 },
  { band: 'above_avg', minPercent: 65 },
  { band: 'average', minPercent: 45 },
  { band: 'below_avg', minPercent: 0 },
];

export function bandFor(percent: number, cutoffs: BandCutoff[] = DEFAULT_BANDS): Band {
  const sorted = [...cutoffs].sort((a, b) => b.minPercent - a.minPercent);
  return (sorted.find((c) => percent >= c.minPercent) ?? sorted[sorted.length - 1]).band;
}

/** Tiers of the parameters computed here (copied from data/profile/parameters.json). */
const COMPUTED_TIER: Record<string, Tier> = {
  p1: 'T1', p3: 'T1', p5: 'T1', p13: 'T1', p14: 'T1', p61: 'T1', p62: 'T1', p63: 'T2', p64: 'T1', p65: 'T1',
  p68: 'T1', p69: 'T2', p140: 'T1', p141: 'T2', p200: 'T2', p278: 'T1', p279: 'T1', p284: 'T1',
};

const LEVEL_ON_MISS: Record<string, Level> = { C1: 0, C2: 1, C3: 2 };
const round1 = (n: number) => Math.round(n * 10) / 10;

export function scoreOnboarding(
  file: OnboardingFormFile,
  responses: OnboardingResponses,
  ctx: { learnerId: string; nowUtc: string },
): OnboardingResult {
  const { form } = file;
  const rule = form.scoring.ladder ?? DEFAULT_LADDER;
  const cutoffs = form.scoring.bandCutoffs ?? DEFAULT_BANDS;
  const byId = new Map(file.items.map((it) => [it.id, it]));
  const profile: ProfileValue[] = [];
  const put = (paramId: string, value: unknown, source: SourceMethod, confidence: ProfileValue['confidence'], tier?: Tier) =>
    profile.push({ learnerId: ctx.learnerId, paramId, value, source, asOfUtc: ctx.nowUtc, confidence, tier: tier ?? COMPUTED_TIER[paramId] ?? 'T1' });

  put('p1', form.grade, 'M1', 'high');
  put('p3', form.board, 'M1', 'high');
  if (form.stream !== 'none') put('p5', form.stream, 'M1', 'high');

  // ---------- Part A ----------
  const max = rule.weights[rule.ceiling as 'D1' | 'D2' | 'D3'];
  const w = (d: Difficulty) => rule.weights[d as 'D1' | 'D2' | 'D3'] ?? 0;
  const groups: GroupResult[] = [];
  const gaps: SuspectedGap[] = [];
  const mastery: Record<string, { pMastery: number; level: Level }> = {};
  let calibSum = 0;
  let calibN = 0;

  for (const g of form.scoring.groups) {
    const seen = responses.academic
      .map((r) => ({ r, it: byId.get(r.questionId) as OnboardingAcademicItem | undefined }))
      .filter((x): x is { r: AcademicResponse; it: OnboardingAcademicItem } => !!x.it && x.it.part === 'A' && x.it.group === g.group)
      .sort((a, b) => a.it.slot - b.it.slot);
    const earned = seen.reduce((s, x) => s + (x.r.correct ? w(x.it.difficulty) : 0), 0);
    const percent = seen.length ? Math.round((100 * earned) / (seen.length * max)) : 0;
    const pre = seen.filter((x) => x.it.half === 'prerequisite');
    const preW = pre.reduce((s, x) => s + w(x.it.difficulty), 0);
    const preMiss = pre.reduce((s, x) => s + (x.r.correct ? 0 : w(x.it.difficulty)), 0);
    const confs = seen.map((x) => x.r.confidence).filter((c): c is 1 | 2 | 3 | 4 | 5 => c !== undefined);
    for (const x of seen) {
      if (x.r.confidence !== undefined) {
        calibSum += Math.abs(x.r.confidence / 5 - (x.r.correct ? 1 : 0));
        calibN++;
      }
    }
    // Highest difficulty answered right twice in a row.
    let highest: Difficulty | null = null;
    for (let i = 1; i < seen.length; i++) {
      const a = seen[i - 1];
      const b = seen[i];
      if (a.r.correct && b.r.correct) {
        const d = w(a.it.difficulty) <= w(b.it.difficulty) ? a.it.difficulty : b.it.difficulty;
        if (!highest || w(d) > w(highest)) highest = d;
      }
    }
    const d3Right = seen.some((x) => x.it.difficulty === 'D3' && x.r.correct);
    for (const x of seen) {
      const level: Level = x.r.correct ? (x.it.difficulty === 'D1' ? 1 : x.it.difficulty === 'D2' ? 2 : 3) : LEVEL_ON_MISS[x.it.conceptGroup] ?? 0;
      const p = x.r.correct ? (x.it.difficulty === 'D1' ? 0.55 : 0.7) : 0.25;
      const prev = mastery[x.it.subtopicId];
      if (!prev || p < prev.pMastery) mastery[x.it.subtopicId] = { pMastery: p, level };
      if (x.r.correct) continue;
      const flags: GapCode[] = [];
      if (x.it.difficulty === 'D2' && d3Right) flags.push('G4');
      if (x.r.secondsTaken > 2 * x.it.minutes * 60) flags.push('G8');
      if ((x.r.confidence ?? 0) >= 4) flags.push('G9');
      const code = (x.it.likelyGapOnWrong ?? 'G1') as GapCode;
      gaps.push({
        learnerId: ctx.learnerId,
        subtopicId: x.it.subtopicId,
        subjectId: x.it.subjectId,
        code,
        secondaryFlags: flags.filter((f) => f !== code),
        level,
        size: 5 - level,
        status: 'suspected',
        evidenceItemIds: [x.it.id],
        reason: `${x.it.half === 'prerequisite' ? 'Prerequisite' : 'This year'}: missed a ${x.it.difficulty} item on ${x.it.subtopicHint}`,
      });
    }
    groups.push({
      group: g.group,
      label: g.label,
      itemsSeen: seen.length,
      correct: seen.filter((x) => x.r.correct).length,
      percent,
      band: bandFor(percent, cutoffs),
      prerequisiteGapIndex: preW ? Math.round((100 * preMiss) / preW) : 0,
      meanConfidence: confs.length ? round1(confs.reduce((s, c) => s + c, 0) / confs.length) : null,
      highestSustained: highest,
    });
  }

  put('p278', mastery, 'M9', 'low');
  const answeredGroups = groups.filter((g) => g.itemsSeen > 0);
  if (answeredGroups.length) {
    put('p279', Math.round(answeredGroups.reduce((s, g) => s + g.prerequisiteGapIndex, 0) / answeredGroups.length), 'M9', 'low');
    const ranked = [...answeredGroups].sort((a, b) => b.percent - a.percent);
    put('p13', ranked.filter((g) => g.percent >= 65).slice(0, 2).map((g) => g.group), 'M9', 'low');
    put('p14', [...ranked].reverse().filter((g) => g.percent < 65).slice(0, 2).map((g) => g.group), 'M9', 'low');
    put('p140', Object.fromEntries(answeredGroups.map((g) => [g.group, g.meanConfidence])), 'M1', 'medium');
    const best = answeredGroups.map((g) => g.highestSustained).filter(Boolean) as Difficulty[];
    const top = best.sort((a, b) => w(b) - w(a))[0];
    put('p284', top === 'D3' ? 'high' : top === 'D2' ? 'medium' : 'low', 'M9', 'low');
  }
  if (calibN) put('p141', round1(1 - calibSum / calibN), 'M9', 'low');

  // ---------- Part B ----------
  const domains: ReasoningDomain[] = ['numerical', 'verbal', 'abstract', 'spatial'];
  const reasoning = { numerical: 0, verbal: 0, abstract: 0, spatial: 0 } as Record<ReasoningDomain, number>;
  const rItems = file.items.filter((it): it is OnboardingReasoningItem => it.part === 'B');
  const rResp = new Map(responses.reasoning.map((r) => [r.questionId, r]));
  let fastRight = 0;
  let deductionRight = 0;
  let deductionN = 0;
  let numericFluency = 0;
  for (const d of domains) {
    const list = rItems.filter((it) => it.domain === d);
    const right = list.filter((it) => rResp.get(it.id)?.answer === it.answer);
    reasoning[d] = list.length ? Math.round((100 * right.length) / list.length) : 0;
    for (const it of right) if ((rResp.get(it.id)?.secondsTaken ?? Infinity) <= it.seconds) fastRight++;
    if (d === 'numerical' && list.length) {
      const credit = right.reduce((s, it) => s + ((rResp.get(it.id)?.secondsTaken ?? Infinity) <= it.seconds ? 1.2 : 1), 0);
      numericFluency = Math.min(100, Math.round((100 * credit) / list.length));
    }
  }
  for (const it of rItems.filter((x) => x.paramIds.includes('p65'))) {
    deductionN++;
    if (rResp.get(it.id)?.answer === it.answer) deductionRight++;
  }
  const processingSpeed = rItems.length ? Math.round((100 * fastRight) / rItems.length) : 0;
  if (responses.reasoning.length) {
    put('p61', reasoning.verbal, 'M9', 'low');
    put('p62', reasoning.numerical, 'M9', 'low');
    put('p63', reasoning.abstract, 'M9', 'low');
    put('p64', reasoning.spatial, 'M9', 'low');
    if (deductionN) put('p65', Math.round((100 * deductionRight) / deductionN), 'M9', 'low');
    put('p68', numericFluency, 'M9', 'low');
    put('p69', processingSpeed, 'M9', 'low');
  }

  // ---------- Part C and parent form ----------
  const sResp = new Map(responses.survey.map((r) => [r.questionId, r]));
  const riasecSum = { R: 0, I: 0, A: 0, S: 0, E: 0, C: 0 };
  const riasecN = { R: 0, I: 0, A: 0, S: 0, E: 0, C: 0 };
  const surveyItems = file.items.filter((it): it is OnboardingSurveyItem => it.part === 'C' || it.part === 'P');
  const written = new Set<string>();
  for (const it of surveyItems) {
    const r = sResp.get(it.id);
    if (!r) continue;
    if (it.riasec) {
      riasecSum[it.riasec] += Number(r.value);
      riasecN[it.riasec] += 1;
      continue;
    }
    // A parameter asked of both (p21 tuition): the parent's answer replaces the student's.
    if (written.has(it.paramId)) {
      if (it.respondent !== 'parent') continue;
      const i = profile.findIndex((p) => p.paramId === it.paramId);
      if (i >= 0) profile.splice(i, 1);
    }
    written.add(it.paramId);
    const source: SourceMethod = it.respondent === 'parent' ? 'M2' : 'M1';
    put(it.paramId, r.value, source, it.respondent === 'parent' ? 'medium' : 'low', it.tier);
  }
  const scores = Object.fromEntries(
    (Object.keys(riasecSum) as (keyof typeof riasecSum)[]).map((k) => [k, riasecN[k] ? round1(riasecSum[k] / riasecN[k]) : 0]),
  ) as Record<'R' | 'I' | 'A' | 'S' | 'E' | 'C', number>;
  const code = (Object.keys(scores) as (keyof typeof scores)[])
    .sort((a, b) => scores[b] - scores[a] || 'RIASEC'.indexOf(a) - 'RIASEC'.indexOf(b))
    .slice(0, 3)
    .join('');
  if (Object.values(riasecN).some((n) => n > 0)) put('p200', { code, scores }, 'M1', 'low');

  return { formId: form.formId, groups, suspectedGaps: gaps, reasoning, processingSpeed, riasec: { scores, code }, profile };
}
