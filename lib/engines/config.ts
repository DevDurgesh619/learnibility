/**
 * Every number the engines use, copied from the CBSE Class 8 Maths Assessment v4 workbook
 * (reference/cbse-class8-maths-assessment-v4.xlsx). Sheet and cell are given next to each value so a
 * reviewer can check them. Change a value here, not inside an engine.
 */
import type { Band, Difficulty, GapCode, Level, Weight } from '../types';

export const BANDS: Band[] = ['below_avg', 'average', 'above_avg', 'excellent'];

export const BAND_LABEL: Record<Band, string> = {
  below_avg: 'Below average',
  average: 'Average',
  above_avg: 'Above average',
  excellent: 'Excellent',
};

/** Mastery Inputs, section A (rows 10-17). */
export interface BandParams {
  startAccuracyPct: number; // row 10
  targetAccuracyPct: number; // row 11
  gainPerOpportunityPct: number; // row 12
  absorptionFactor: number; // row 13
  guidedPracticeFraction: number; // row 14
  errorCorrectionFactor: number; // row 15 (ECV proxy)
  retrievalSessions: number; // row 16 (R proxy)
  minutesPerRetrieval: number; // row 17
}

export const BAND_PARAMS: Record<Band, BandParams> = {
  below_avg: { startAccuracyPct: 30, targetAccuracyPct: 80, gainPerOpportunityPct: 2.5, absorptionFactor: 1.25, guidedPracticeFraction: 0.5, errorCorrectionFactor: 1.4, retrievalSessions: 4, minutesPerRetrieval: 8 },
  average: { startAccuracyPct: 45, targetAccuracyPct: 80, gainPerOpportunityPct: 2.5, absorptionFactor: 1.0, guidedPracticeFraction: 0.4, errorCorrectionFactor: 1.2, retrievalSessions: 3, minutesPerRetrieval: 8 },
  above_avg: { startAccuracyPct: 55, targetAccuracyPct: 80, gainPerOpportunityPct: 2.5, absorptionFactor: 0.9, guidedPracticeFraction: 0.35, errorCorrectionFactor: 1.1, retrievalSessions: 2, minutesPerRetrieval: 8 },
  excellent: { startAccuracyPct: 65, targetAccuracyPct: 80, gainPerOpportunityPct: 2.5, absorptionFactor: 0.8, guidedPracticeFraction: 0.3, errorCorrectionFactor: 1.0, retrievalSessions: 2, minutesPerRetrieval: 8 },
};

/** Mastery Inputs, section B (rows 22-24). Instruction minutes are the default when a subtopic has no teaching periods. */
export interface WeightParams { instructionMinutes: number; minutesPerOpportunity: number; testItems: number; teachingPeriods: number }
export const WEIGHT_PARAMS: Record<Weight, WeightParams> = {
  L: { instructionMinutes: 80, minutesPerOpportunity: 2.5, testItems: 5, teachingPeriods: 2 },
  S: { instructionMinutes: 120, minutesPerOpportunity: 3.5, testItems: 6, teachingPeriods: 3 },
  H: { instructionMinutes: 160, minutesPerOpportunity: 5.0, testItems: 8, teachingPeriods: 4 },
};

/** One teaching period, in minutes (Teaching Plan, column F header). */
export const PERIOD_MINUTES = 40;
/** Periods per week used for "suggested weeks" (Mastery Summary, column P). */
export const PERIODS_PER_WEEK = 6;
/** Quarter-week added per chapter for the chapter test (Mastery Summary note B18). */
export const CHAPTER_TEST_WEEKS = 0.25;

/** Gap Diagnosis, section C (rows 28-33): fraction of MASTER time still needed from each level. */
export const LEVEL_TIME_FRACTION: Record<Level, { fraction: number; prerequisiteExtra: number; spentOn: string }> = {
  0: { fraction: 1.0, prerequisiteExtra: 0.4, spentOn: 'Prerequisite mini-lesson + full re-teach + practice + retrieval' },
  1: { fraction: 0.85, prerequisiteExtra: 0, spentOn: 'Re-teach with worked examples + self-explanation + practice + retrieval' },
  2: { fraction: 0.65, prerequisiteExtra: 0, spentOn: 'Faded worked examples + deliberate practice + retrieval' },
  3: { fraction: 0.4, prerequisiteExtra: 0, spentOn: 'Varied-context / interleaved practice + retrieval' },
  4: { fraction: 0.15, prerequisiteExtra: 0, spentOn: 'Two spaced retrieval sessions + error re-do' },
  5: { fraction: 0, prerequisiteExtra: 0, spentOn: 'Maintenance retrieval only' },
};

export const LEVEL_LABEL: Record<Level, string> = {
  0: 'L0 – no recall / prerequisite missing',
  1: 'L1 – recalls, cannot explain',
  2: 'L2 – explains, cannot execute',
  3: 'L3 – routine only',
  4: 'L4 – passes C4, not yet 80% or not retained',
  5: 'L5 – mastered and retained',
};

/** Gap Calculator row 56: share of remediation hours with a teacher or tutor. */
export const TEACHER_SHARE = 0.35;

/** Mastery rule (Mastery Inputs B3 and Gap Calculator C36). */
export const MASTERY_SCORE_PCT = 80;
export const RETENTION_PASS_PCT = 70;

/** Secondary-flag thresholds (Gap Diagnosis B23). */
export const SPEED_FACTOR = 1.2;
export const OVERCONFIDENT_MEAN = 4;
export const ENGAGEMENT_BLANKS = 2;
export const MIN_ATTEMPTED = 4;

/** Gap Diagnosis, section A: the taxonomy. */
export interface GapInfo { code: GapCode; key: string; name: string; signature: string; probe: string; causes: string; causeParams: string[]; alrSignal: string; typicalSize: string }
export const GAP_TAXONOMY: Record<GapCode, GapInfo> = {
  G1: { code: 'G1', key: 'PREREQUISITE', name: 'Prerequisite gap', signature: 'C1-D1/D2 wrong, or C3-D2 wrong with the error located in an earlier skill.', probe: 'Give the prerequisite item from the prerequisite map. If that also fails, G1 is confirmed; if it passes, treat as G2.', causes: 'Missing earlier-class concept', causeParams: ['p279', 'p20', 'p22', 'p28', 'p14', 'p68'], alrSignal: 'dK stays low even after re-teaching the current subtopic', typicalSize: '4–5 (plus repair of the prerequisite)' },
  G2: { code: 'G2', key: 'CONCEPTUAL', name: 'Conceptual gap', signature: "C1 correct, C2-D2/D3 wrong: can state the rule but cannot explain why, compare, or spot the counter-example.", probe: "'Explain in one line why …' or 'Give an example where this is NOT true'.", causes: 'Learned by rote', causeParams: ['p288', 'p289', 'p80', 'p37'], alrSignal: 'TQ low; dK moderate', typicalSize: '3–4' },
  G3: { code: 'G3', key: 'PROCEDURAL', name: 'Procedural gap', signature: 'C2 correct, C3-D2 wrong: understands the idea but cannot carry out the method.', probe: 'Same method, new values (C3-D2 parallel item) with steps written out.', causes: 'Too little deliberate practice', causeParams: ['p41', 'p44', 'p68', 'p287'], alrSignal: 'dK moderate; ECV low if the same step keeps failing', typicalSize: '2–3' },
  G4: { code: 'G4', key: 'CARELESS', name: 'Fluency / careless gap', signature: 'D2 wrong but D3 of the same group right; fast answers; right method, wrong final line.', probe: "Re-do the failed item slowly with an estimate first.", causes: 'Speed over checking', causeParams: ['p75', 'p76', 'p105', 'p319', 'p324', 'p83'], alrSignal: 'MCI low (confident but wrong); CE low', typicalSize: '1' },
  G5: { code: 'G5', key: 'TRANSFER', name: 'Transfer / complex-application gap', signature: 'C3-D2/D3 correct, C3-D4 / C4 wrong: cannot choose the method in a messy or unfamiliar setting or combine two ideas.', probe: 'C4-D3 item with a hint that names the two ideas to combine; if it passes with the hint → G5 (strategy), if not → G3.', causes: 'Only blocked practice, one context', causeParams: ['p283', 'p291', 'p303', 'p321', 'p292'], alrSignal: 'TQ < 0.5', typicalSize: '1–2' },
  G6: { code: 'G6', key: 'RETENTION', name: 'Retention gap', signature: 'Post-test passed, 7-day retention probe < 70%.', probe: 'Re-give the two retention probes after a 10-minute self-review; if they now pass → G6 (forgetting), not G2.', causes: 'No spaced revision', causeParams: ['p39', 'p40', 'p301', 'p282', 'p71', 'p72', 'p83', 'p84', 'p85'], alrSignal: 'R < 0.7', typicalSize: '1 (recoverable quickly)' },
  G7: { code: 'G7', key: 'LANGUAGE', name: 'Language / reading gap', signature: 'Word problems wrong, numerical items of the same difficulty right; misreads; blanks on long stems.', probe: 'Read the item aloud and ask the learner to restate it in own words or home language before solving.', causes: 'Medium-of-instruction mismatch', causeParams: ['p4', 'p157', 'p66', 'p67'], alrSignal: 'dK fine on numerical C3, low on C4 word problems', typicalSize: '1–2 (subject-independent)' },
  G8: { code: 'G8', key: 'TIME_PRESSURE', name: 'Speed / pressure gap', signature: 'Correct when untimed, wrong under time; last items blank; time taken > 1.2× allotted.', probe: 'Give the failed items again untimed the next day.', causes: 'Test anxiety or slow fluency', causeParams: ['p286', 'p111', 'p69', 'p42'], alrSignal: 'CE low; dK fine untimed', typicalSize: '0–1' },
  G9: { code: 'G9', key: 'CALIBRATION', name: 'Metacognitive gap', signature: 'Confidence 4–5 on wrong items (over-confident) or 1–2 on right items (under-confident); does not check answers.', probe: 'Ask the learner to predict the score before marking; compare.', causes: 'Poor confidence–competence calibration', causeParams: ['p79', 'p141', 'p325', 'p124', 'p143'], alrSignal: 'MCI < 0.6', typicalSize: 'Amplifies other gaps' },
  G10: { code: 'G10', key: 'ENGAGEMENT', name: 'Engagement / effort gap', signature: 'Two or more items blank; unattempted homework; no retry after error.', probe: "Short conversation, not a probe: 'Which of these would you try first if you had to?'", causes: 'Low engagement or effort', causeParams: ['p295', 'p298', 'p46', 'p123', 'p151', 'p163', 'p162', 'p114'], alrSignal: 'All indices sparse (data-sparsity flag #424)', typicalSize: 'Cannot be sized until attempted' },
};

/** Gap Calculator C65: the add-on line for each secondary flag. */
export const FLAG_ADD_ON: Partial<Record<GapCode, string>> = {
  G4: 'G4 estimate-first + slow-down.',
  G7: 'G7 restate-then-solve + glossary.',
  G8: 'G8 untimed re-test first.',
  G9: 'G9 predict-then-check; review confident-and-wrong items.',
  G10: 'G10 20-minute blocks + trusted-adult check-in.',
};

/** ALR Method rows 16-21: LRS weight sets. */
export type AlrIndex = 'dK' | 'R' | 'TQ' | 'CE' | 'ECV' | 'MCI';
export type AlrWeightSet = 'default' | 'exam_oriented' | 'deep_mastery';
export const ALR_WEIGHTS: Record<AlrWeightSet, Record<AlrIndex, number>> = {
  default: { dK: 0.25, R: 0.2, TQ: 0.15, CE: 0.15, ECV: 0.1, MCI: 0.15 },
  exam_oriented: { dK: 0.35, R: 0.15, TQ: 0.1, CE: 0.15, ECV: 0.15, MCI: 0.1 },
  deep_mastery: { dK: 0.2, R: 0.25, TQ: 0.2, CE: 0.1, ECV: 0.1, MCI: 0.15 },
};

/** ALR Method rows 26-30: difficulty proxy weights for dK. */
export const DIFFICULTY_WEIGHT: Record<Difficulty, number> = { D1: 0.8, D2: 1.0, D3: 1.2, D4: 1.4, D5: 1.6 };

/** ALR Method rows 34-37: band cut-offs on LRS. */
export const LRS_BAND_CUTOFFS: { band: Band; min: number; action: string }[] = [
  { band: 'excellent', min: 0.8, action: 'Compress instruction; skip to C3-D3 / C4 items; extend with wider-bank D4–D5.' },
  { band: 'above_avg', min: 0.65, action: 'Standard pace; add transfer contexts.' },
  { band: 'average', min: 0.45, action: 'Standard pace; one extra retrieval session per chapter.' },
  { band: 'below_avg', min: -Infinity, action: 'Extra guided practice; pre-teach prerequisites; two retrieval sessions; error-analysis routine.' },
];

/** Confidence 1-5 to probability (ALR Method row 12: 1→0.1 … 5→0.9). */
export const CONFIDENCE_PROB: Record<1 | 2 | 3 | 4 | 5, number> = { 1: 0.1, 2: 0.3, 3: 0.5, 4: 0.7, 5: 0.9 };

/** Spaced review intervals in days after a subtopic is tested (blueprint, timetable engine). */
export const REVIEW_INTERVALS_DAYS = [1, 3, 7, 14, 30];

/** Paid-tuition rule (Interventions row ANY-1). */
export const PAID_TUITION_MIN_CHAPTERS = 2;
export const PAID_TUITION_FREE_PLAN_WEEKS = 3;
export const PAID_TUITION_INR = { min: 2000, max: 6000 };
/** Gap size from which a paid option is worth considering when money is available (Gap Calculator C66). */
export const DEEP_GAP_SIZE = 4;
