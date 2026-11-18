/**
 * Onboarding test forms (QB-ONB). Proposed by the QB-ONB thread; see docs/onboarding.md.
 *
 * 15 form designs (grades 8, 9, 10 x 3 boards; grades 11 and 12 x 3 streams with
 * board-specific swaps) are delivered as one file per board/grade/stream a student can be in:
 * data/questions/onboarding/{formId}.json, formId = onb-{board}-g{grade}-{stream}.
 *
 * Part A items are ordinary `Question`s (set 'onboarding'). Parts B, C and the parent
 * form use the item types below. Every item ID follows onb-{board}-g{grade}-{stream}-q{NN}.
 */
import type { Board, Difficulty, Grade, Stream, Tier } from './enums';
import type { Question } from './assessment';

export const ONBOARDING_PARTS = ['A', 'B', 'C', 'P'] as const;
/** A academic diagnostic, B reasoning, C about me, P parent form. */
export type OnboardingPart = (typeof ONBOARDING_PARTS)[number];

/** Subject groups used for Part A banding. Grades 8-10 use the four core groups. */
export type SubjectGroup = string; // e.g. 'maths', 'science', 'english', 'social-science', 'physics', 'accountancy'

/** A Part A item: a Question plus its place on the adaptive ladder. */
export interface OnboardingAcademicItem extends Question {
  set: 'onboarding';
  part: 'A';
  group: SubjectGroup;
  /** 1-8. Slots 1-4 probe the previous grade's prerequisites, 5-8 this grade's first chapters. */
  slot: number;
  half: 'prerequisite' | 'current';
  /** Plain-words name of the subtopic, used to re-link subtopicId to the curriculum map. */
  subtopicHint: string;
  /** For grade 8 prerequisites (grade 7 is not in the map): the earlier skill in words. */
  prerequisiteNote?: string;
  /** False until scripts/onboarding/link-curriculum.ts has resolved subtopicId against data/curriculum. */
  subtopicLinked: boolean;
  /** Same content reused in another form (e.g. a shared prerequisite) carries the same key. */
  contentKey: string;
}

export const REASONING_DOMAINS = ['numerical', 'verbal', 'abstract', 'spatial'] as const;
export type ReasoningDomain = (typeof REASONING_DOMAINS)[number];

export interface OnboardingReasoningItem {
  id: string;
  part: 'B';
  domain: ReasoningDomain;
  difficulty: Difficulty;
  stem: string;
  /** Inline SVG for abstract and spatial figures (optional; the stem always describes it in words too). */
  svg?: string;
  options: string[];
  answer: string;
  explanation: string;
  /** Target time; answers faster than this with the right answer feed processing speed (p69). */
  seconds: number;
  /** Parameters this item contributes to, e.g. ['p62', 'p68']. */
  paramIds: string[];
  contentKey: string;
}

export type SurveyResponseType = 'single' | 'multi' | 'scale' | 'number' | 'consent';

export interface SurveyOption {
  label: string;
  /** Stored value; for scales 1-5. */
  value: string | number;
  /** Extra parameter writes this option causes, e.g. RIASEC letter or a derived band. */
  sets?: Record<string, string | number>;
}

export interface OnboardingSurveyItem {
  id: string;
  part: 'C' | 'P';
  respondent: 'student' | 'parent';
  prompt: string;
  helpText?: string;
  responseType: SurveyResponseType;
  options?: SurveyOption[];
  /** number inputs */
  min?: number;
  max?: number;
  unit?: string;
  /** Primary parameter the answer is written to. */
  paramId: string;
  /** Other parameters the answer also informs. */
  alsoInforms?: string[];
  /** Tier of the primary parameter (copied from parameters.json). T3 items are screened, support-only. */
  tier: Tier;
  /** True for T3 items: shown with a "you can skip this" note; never used for ranking or fit. */
  screened: boolean;
  optional: boolean;
  /** RIASEC letter for the 12 career-interest items. */
  riasec?: 'R' | 'I' | 'A' | 'S' | 'E' | 'C';
  contentKey: string;
}

export type OnboardingItem = OnboardingAcademicItem | OnboardingReasoningItem | OnboardingSurveyItem;

export interface BandCutoff {
  band: 'below_avg' | 'average' | 'above_avg' | 'excellent';
  /** Inclusive lower bound, percent. */
  minPercent: number;
}

export interface LadderRule {
  start: Difficulty; // 'D2'
  /** After a miss, step down one level (not below `floor`). */
  floor: Difficulty; // 'D1'
  /** After `hitsToStepUp` consecutive hits, step up one level (not above `ceiling`). */
  ceiling: Difficulty; // 'D3'
  hitsToStepUp: number; // 2
  /** Score weight per difficulty; percent = earned / (slots x weight[ceiling]). */
  weights: Record<'D1' | 'D2' | 'D3', number>;
}

export interface ParameterWrite {
  paramId: string;
  /** How the value is computed, in words, for the demo's "why" panel. */
  rule: string;
  source: 'M1' | 'M2' | 'M9' | 'M10' | 'M14' | 'M16';
  confidence: 'low' | 'medium' | 'high';
}

export interface OnboardingScoringMap {
  ladder: LadderRule;
  bandCutoffs: BandCutoff[];
  /** Part A subject groups in delivery order, with the subject IDs their items belong to. */
  groups: { group: SubjectGroup; label: string; subjectIds: string[] }[];
  /** Every parameter the form seeds and how. */
  writes: ParameterWrite[];
  reasoning: { domain: ReasoningDomain; paramId: string; itemIds: string[] }[];
  riasec: Record<'R' | 'I' | 'A' | 'S' | 'E' | 'C', string[]>;
}

export interface OnboardingForm {
  formId: string; // onb-{board}-g{grade}-{stream}
  /** The design this form is generated from (15 designs). */
  designId: string; // e.g. 'g8-cbse', 'g11-science'
  board: Board;
  grade: Grade;
  stream: Stream;
  title: string;
  minutes: { A: number; B: number; C: number; P: number };
  /** Part A pool size vs items a student actually sees (8 per group). */
  partA: { pool: number; delivered: number };
  scoring: OnboardingScoringMap;
}

/** Shape of data/questions/onboarding/{formId}.json */
export interface OnboardingFormFile {
  schemaVersion: 1;
  generatedBy: string;
  form: OnboardingForm;
  items: OnboardingItem[];
}
