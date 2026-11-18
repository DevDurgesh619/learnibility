/**
 * Engine 2: from a marked student-check path to a named gap.
 * Source: workbook sheets "Gap Diagnosis" (level ladder B4, taxonomy section A, decision rule section B,
 * time fractions section C) and "Gap Calculator" (formulas C29-C58).
 *
 * The workbook's path is fixed per weight (L 5 items, S 6, H 8). The rules below are written in terms of
 * concept group and difficulty so they give the workbook's answer on its paths and still work on any
 * other board or subject whose questions carry the same C1-C4 × D1-D5 tags.
 *
 *   C1 passed = any C1 item correct
 *   C2 passed = the easiest C2 item correct
 *   C3 passed = the easiest C3 item correct (the routine C3-D2 item)
 *   C4 passed = the easiest C4 item correct, or every other transfer item (C3-D4+, harder C4) correct
 *               when there are at least two of them (workbook H rule: Q7 OR (Q6 AND Q8))
 *   level     = !C1 → 0, !C2 → 1, !C3 → 2, !C4 → 3, mastery rule met and retention ≥ 70% → 5, else 4
 *   primary   = ≥2 blanks → G10; L0 → G1 (G2 if the prerequisite probe passed); L1 → G2; L2 → G3;
 *               L3 → G5; L4 → G6 if retention < 70% else G4; L5 → none
 */
import type { Band, Gap, GapCode, ItemResponse, Level, Question, Subtopic } from '../types';
import {
  BAND_PARAMS,
  BANDS,
  ENGAGEMENT_BLANKS,
  GAP_TAXONOMY,
  LEVEL_LABEL,
  LEVEL_TIME_FRACTION,
  MASTERY_SCORE_PCT,
  MIN_ATTEMPTED,
  OVERCONFIDENT_MEAN,
  RETENTION_PASS_PCT,
  SPEED_FACTOR,
  TEACHER_SHARE,
} from './config';
import { masteryTime, practiceOpportunities } from './masteryTime';
import { round, roundUp } from './util';

export type SubtopicLike = Pick<Subtopic, 'id' | 'chapterId' | 'weight'> & Partial<Pick<Subtopic, 'teachingPeriods' | 'masterHours' | 'name' | 'prerequisiteIds' | 'prerequisiteNote'>>;

export interface SubtopicSignals {
  /** 7-day retention probe score, percent. Leave undefined when not yet given. */
  retentionPct?: number;
  /** Result of the confirming prerequisite probe: true passed, false failed, undefined not given. */
  prerequisiteProbePassed?: boolean;
  /** Word problems wrong but numerical items of the same level right. Computed from item types when undefined. */
  wordProblemPattern?: boolean;
  /** Minutes the learner took on this subtopic's items; summed from secondsTaken when undefined. */
  minutesTaken?: number;
  /** Mean 1-5 confidence on wrong items; computed from responses when undefined. */
  meanConfidenceWrong?: number;
}

export interface DiagnosisContext {
  learnerId: string;
  /** Planning band (measured ALR band once available). */
  band: Band;
  subtopics: SubtopicLike[] | Record<string, SubtopicLike>;
  /** Hours a week available for this subject outside class (#31, #163, #162). */
  weeklyHours?: number;
  signals?: Record<string, SubtopicSignals>;
}

export interface Diagnosis {
  subtopicId: string;
  chapterId: string;
  level: Level;
  levelLabel: string;
  passed: { C1: boolean; C2: boolean; C3: boolean; C4: boolean };
  correct: number;
  attempted: number;
  blank: number;
  itemsOnPath: number;
  scorePct: number;
  masteryRuleMet: boolean;
  /** Primary gap, or null at L5 or when evidence is insufficient. */
  primary: GapCode | null;
  secondaryFlags: GapCode[];
  flags: { careless: boolean; language: boolean; speed: boolean; overConfident: boolean; underConfident: boolean; engagement: boolean; insufficientEvidence: boolean };
  size: number;
  confirmingProbe: string | null;
  likelyCauses: string | null;
  causeParams: string[];
  prerequisiteToProbe: string | null;
  hoursToMaster: Record<Band, number>;
  /** For the selected band. */
  hours: number;
  teacherHours: number;
  selfHours: number;
  weeksToClose: number | null;
  practiceOpportunitiesNeeded: number;
  /** Set when one subtopic needs more than two weeks. */
  splitAdvice: string | null;
  gap: Gap | null;
}

const CG_ORDER = ['C1', 'C2', 'C3', 'C4'] as const;
const DIFF_N = (d: string) => Number(d.slice(1));
const WORD_TYPES = new Set(['multi_step', 'case', 'long']);
const NUMERIC_TYPES = new Set(['numerical', 'short', 'mcq']);

function easiest(items: Question[], cg: string): Question | undefined {
  return items.filter((q) => q.conceptGroup === cg).sort((a, b) => DIFF_N(a.difficulty) - DIFF_N(b.difficulty) || a.id.localeCompare(b.id))[0];
}

function toMap(subs: DiagnosisContext['subtopics']): Record<string, SubtopicLike> {
  if (!Array.isArray(subs)) return subs;
  return Object.fromEntries(subs.map((s) => [s.id, s]));
}

/** Diagnose one subtopic from its path questions and the learner's responses. */
export function diagnoseSubtopic(path: Question[], responses: ItemResponse[], sub: SubtopicLike, ctx: Omit<DiagnosisContext, 'subtopics'>): Diagnosis {
  const items = [...path].sort((a, b) => a.id.localeCompare(b.id));
  const byQ = new Map(responses.map((r) => [r.questionId, r]));
  const sig = ctx.signals?.[sub.id] ?? {};
  const res = (q: Question | undefined) => (q ? byQ.get(q.id) : undefined);
  const ok = (q: Question | undefined) => !!res(q)?.correct;

  const attemptedItems = items.filter((q) => byQ.has(q.id));
  const attempted = attemptedItems.length;
  const blank = items.length - attempted;
  const correct = items.filter(ok).length;
  const scorePct = items.length ? Math.round((correct / items.length) * 100) : 0;

  const c1 = items.some((q) => q.conceptGroup === 'C1' && ok(q));
  const c2 = ok(easiest(items, 'C2'));
  const c3 = ok(easiest(items, 'C3'));
  const c4First = easiest(items, 'C4');
  const others = items.filter((q) => q !== c4First && q.alrRole === 'transfer_probe');
  const c4 = ok(c4First) || (others.length >= 2 && others.every(ok));
  const masteryRuleMet = scorePct >= MASTERY_SCORE_PCT && c3 && c4;
  const retention = sig.retentionPct;

  let level: Level;
  if (!c1) level = 0;
  else if (!c2) level = 1;
  else if (!c3) level = 2;
  else if (!c4) level = 3;
  else level = masteryRuleMet && retention !== undefined && retention >= RETENTION_PASS_PCT ? 5 : 4;

  // secondary flags
  let careless = false;
  for (const cg of CG_ORDER) {
    const g = items.filter((q) => q.conceptGroup === cg);
    const d2wrong = g.some((q) => q.difficulty === 'D2' && byQ.has(q.id) && !ok(q));
    const d3right = g.some((q) => q.difficulty === 'D3' && ok(q));
    if (d2wrong && d3right) careless = true;
  }
  let language = sig.wordProblemPattern;
  if (language === undefined) {
    language = false;
    for (const d of ['D1', 'D2', 'D3', 'D4', 'D5']) {
      const word = attemptedItems.filter((q) => q.difficulty === d && WORD_TYPES.has(q.type));
      const num = attemptedItems.filter((q) => q.difficulty === d && NUMERIC_TYPES.has(q.type));
      if (word.length && num.length && word.every((q) => !ok(q)) && num.some(ok)) language = true;
    }
  }
  const allotted = items.reduce((s, q) => s + q.minutes, 0);
  const taken = sig.minutesTaken ?? attemptedItems.reduce((s, q) => s + (byQ.get(q.id)?.secondsTaken ?? 0), 0) / 60;
  const last = items[items.length - 1];
  const speed = allotted > 0 && taken > SPEED_FACTOR * allotted && !!last && !ok(last);
  const wrongConf = attemptedItems.filter((q) => !ok(q)).map((q) => byQ.get(q.id)?.confidence).filter((c): c is 1 | 2 | 3 | 4 | 5 => c !== undefined);
  const rightConf = attemptedItems.filter(ok).map((q) => byQ.get(q.id)?.confidence).filter((c): c is 1 | 2 | 3 | 4 | 5 => c !== undefined);
  const meanWrong = sig.meanConfidenceWrong ?? (wrongConf.length ? wrongConf.reduce((a, b) => a + b, 0) / wrongConf.length : undefined);
  const overConfident = meanWrong !== undefined && meanWrong >= OVERCONFIDENT_MEAN;
  const underConfident = rightConf.length >= 2 && rightConf.reduce((a, b) => a + b, 0) / rightConf.length <= 2;
  const engagement = blank >= ENGAGEMENT_BLANKS;
  const insufficientEvidence = attempted < MIN_ATTEMPTED;

  let primary: GapCode | null;
  if (engagement) primary = 'G10';
  else if (level === 0) primary = sig.prerequisiteProbePassed === true ? 'G2' : 'G1';
  else if (level === 1) primary = 'G2';
  else if (level === 2) primary = 'G3';
  else if (level === 3) primary = 'G5';
  else if (level === 4) primary = retention !== undefined && retention < RETENTION_PASS_PCT ? 'G6' : 'G4';
  else primary = null;
  if (insufficientEvidence && primary !== 'G10') primary = null;

  const secondary: GapCode[] = [];
  const add = (c: GapCode, on: boolean) => on && c !== primary && !secondary.includes(c) && secondary.push(c);
  add('G4', careless);
  add('G7', language);
  add('G8', speed);
  add('G9', overConfident || underConfident);
  add('G10', engagement);

  // time to close
  const lt = LEVEL_TIME_FRACTION[level];
  const fraction = lt.fraction + (primary === 'G1' ? lt.prerequisiteExtra : 0);
  const hoursToMaster = {} as Record<Band, number>;
  for (const b of BANDS) {
    const full = sub.masterHours?.[b] || masteryTime({ weight: sub.weight, teachingPeriods: sub.teachingPeriods }, b).masterHours;
    hoursToMaster[b] = round(full * fraction);
  }
  const hours = hoursToMaster[ctx.band];
  const weeksToClose = ctx.weeklyHours && ctx.weeklyHours > 0 ? round(hours / ctx.weeklyHours) : null;
  const size = 5 - level;
  const info = primary ? GAP_TAXONOMY[primary] : null;
  const prereq = sub.prerequisiteNote ?? (sub.prerequisiteIds?.length ? sub.prerequisiteIds.join('; ') : null);

  const gap: Gap | null = primary
    ? {
        id: `gap_${ctx.learnerId}_${sub.id}`,
        learnerId: ctx.learnerId,
        subtopicId: sub.id,
        code: primary,
        secondaryFlags: secondary,
        level,
        size,
        hoursToClose: hours,
        status: primary === 'G1' && sig.prerequisiteProbePassed === false ? 'confirmed' : 'suspected',
      }
    : null;

  return {
    subtopicId: sub.id,
    chapterId: sub.chapterId,
    level,
    levelLabel: LEVEL_LABEL[level],
    passed: { C1: c1, C2: c2, C3: c3, C4: c4 },
    correct,
    attempted,
    blank,
    itemsOnPath: items.length,
    scorePct,
    masteryRuleMet,
    primary,
    secondaryFlags: secondary,
    flags: { careless, language, speed, overConfident, underConfident, engagement, insufficientEvidence },
    size,
    confirmingProbe: info?.probe ?? null,
    likelyCauses: info ? `${info.causes}: ${info.causeParams.map((p) => '#' + p.slice(1)).join(', ')}` : null,
    causeParams: info?.causeParams ?? [],
    prerequisiteToProbe: prereq,
    hoursToMaster,
    hours,
    teacherHours: round(hours * TEACHER_SHARE),
    selfHours: round(hours * (1 - TEACHER_SHARE)),
    weeksToClose,
    practiceOpportunitiesNeeded: roundUp(practiceOpportunities(BAND_PARAMS[ctx.band]) * fraction),
    splitAdvice: weeksToClose !== null && weeksToClose > 2 ? 'This exceeds 2 weeks for one subtopic: split it, prerequisite first, then the subtopic.' : null,
    gap,
  };
}

/**
 * Diagnose every subtopic touched by `responses` (or by `questions` when a whole paper is passed).
 * Returns one Diagnosis per subtopic, worst level first; use `.gap` for the Gap records.
 */
export function diagnoseGaps(responses: ItemResponse[], questions: Question[], context: DiagnosisContext): Diagnosis[] {
  const subs = toMap(context.subtopics);
  const bySub = new Map<string, Question[]>();
  for (const q of questions) {
    if (!bySub.has(q.subtopicId)) bySub.set(q.subtopicId, []);
    bySub.get(q.subtopicId)!.push(q);
  }
  const out: Diagnosis[] = [];
  for (const [sid, path] of bySub) {
    const sub = subs[sid];
    if (!sub) throw new Error(`diagnoseGaps: subtopic ${sid} missing from context.subtopics`);
    out.push(diagnoseSubtopic(path, responses, sub, context));
  }
  return out.sort((a, b) => a.level - b.level || b.hours - a.hours || a.subtopicId.localeCompare(b.subtopicId));
}

/** Just the Gap records (contract type) from diagnoseGaps. */
export function gapsFrom(diagnoses: Diagnosis[]): Gap[] {
  return diagnoses.map((d) => d.gap).filter((g): g is Gap => g !== null);
}
