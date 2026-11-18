/**
 * Engine 1: time to LEARN and time to MASTER a subtopic, per learner band.
 * Source: workbook sheets "Mastery Inputs" (formulas B4, rows 10-24), "Mastery Time", "Mastery Summary".
 *
 *   instruction   = teaching periods × 40 min
 *   learn         = instruction × absorption + instruction × guided-practice fraction
 *   opportunities = ROUNDUP((target − start accuracy) ÷ gain per opportunity)
 *   master        = learn + opportunities × minutes per opportunity × error-correction factor
 *                   + retrieval sessions × minutes per retrieval
 */
import type { Band, Subtopic, Weight } from '../types';
import { BANDS, BAND_PARAMS, BandParams, CHAPTER_TEST_WEEKS, PERIODS_PER_WEEK, PERIOD_MINUTES, WEIGHT_PARAMS } from './config';
import { round, roundUp } from './util';

export type SubtopicTimingInput = Pick<Subtopic, 'weight'> & { teachingPeriods?: number };

export interface MasteryTimeResult {
  band: Band;
  instructionHours: number;
  learnHours: number;
  masterHours: number;
  /** MASTER − instruction: homework / remediation time outside class. */
  practiceBeyondClassHours: number;
  practiceOpportunities: number;
}

/** Practice opportunities to go from starting to target accuracy (Mastery Inputs row 18). */
export function practiceOpportunities(params: BandParams): number {
  return roundUp((params.targetAccuracyPct - params.startAccuracyPct) / params.gainPerOpportunityPct);
}

function instructionMinutes(sub: SubtopicTimingInput): number {
  const periods = sub.teachingPeriods && sub.teachingPeriods > 0 ? sub.teachingPeriods : WEIGHT_PARAMS[sub.weight].teachingPeriods;
  return periods * PERIOD_MINUTES;
}

/**
 * Learn and master hours for one subtopic and band.
 * `overrides` lets a learner's measured parameters (from the ALR tracker) replace the band defaults.
 */
export function masteryTime(sub: SubtopicTimingInput, band: Band, overrides: Partial<BandParams> = {}): MasteryTimeResult {
  const p: BandParams = { ...BAND_PARAMS[band], ...overrides };
  const w = WEIGHT_PARAMS[sub.weight as Weight];
  const instrMin = instructionMinutes(sub);
  const learnMin = instrMin * p.absorptionFactor + instrMin * p.guidedPracticeFraction;
  const opps = practiceOpportunities(p);
  const masterMin = learnMin + opps * w.minutesPerOpportunity * p.errorCorrectionFactor + p.retrievalSessions * p.minutesPerRetrieval;
  const instructionHours = round(instrMin / 60);
  const masterHours = round(masterMin / 60);
  return {
    band,
    instructionHours,
    learnHours: round(learnMin / 60),
    masterHours,
    practiceBeyondClassHours: round(masterHours - instructionHours),
    practiceOpportunities: opps,
  };
}

/** All four bands at once, shaped for Subtopic.learnHours / masterHours. */
export function masteryTimeAllBands(sub: SubtopicTimingInput): { learnHours: Record<Band, number>; masterHours: Record<Band, number>; instructionHours: number } {
  const learnHours = {} as Record<Band, number>;
  const masterHours = {} as Record<Band, number>;
  let instructionHours = 0;
  for (const b of BANDS) {
    const r = masteryTime(sub, b);
    learnHours[b] = r.learnHours;
    masterHours[b] = r.masterHours;
    instructionHours = r.instructionHours;
  }
  return { learnHours, masterHours, instructionHours };
}

/** Return a copy of the subtopic with learnHours / masterHours filled (used by the Wave 2 curriculum fill script). */
export function withMasteryHours<T extends SubtopicTimingInput>(sub: T): T & { learnHours: Record<Band, number>; masterHours: Record<Band, number> } {
  const { learnHours, masterHours } = masteryTimeAllBands(sub);
  return { ...sub, learnHours, masterHours };
}

export interface ChapterTimeSummary {
  subtopics: number;
  instructionHours: number;
  learnHours: Record<Band, number>;
  masterHours: Record<Band, number>;
  practiceBeyondClassHours: Record<Band, number>;
  /** Instruction periods ÷ 6 per week + a quarter week for the chapter test. */
  suggestedWeeks: number;
}

/** Chapter totals as on "Mastery Summary": sums of the rounded subtopic rows, rounded again. */
export function chapterTimeSummary(subs: SubtopicTimingInput[]): ChapterTimeSummary {
  const learnHours = {} as Record<Band, number>;
  const masterHours = {} as Record<Band, number>;
  const beyond = {} as Record<Band, number>;
  let instr = 0;
  for (const b of BANDS) {
    let l = 0, m = 0, p = 0, i = 0;
    for (const s of subs) {
      const r = masteryTime(s, b);
      l += r.learnHours; m += r.masterHours; p += r.practiceBeyondClassHours; i += r.instructionHours;
    }
    learnHours[b] = round(l); masterHours[b] = round(m); beyond[b] = round(p); instr = round(i);
  }
  return {
    subtopics: subs.length,
    instructionHours: instr,
    learnHours,
    masterHours,
    practiceBeyondClassHours: beyond,
    suggestedWeeks: round((instr * 60) / PERIOD_MINUTES / PERIODS_PER_WEEK + CHAPTER_TEST_WEEKS),
  };
}
