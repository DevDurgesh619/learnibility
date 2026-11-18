import type { AlrRole, ConceptGroup, Difficulty, GapCode } from './enums';

export const QUESTION_TYPES = ['mcq', 'short', 'explain', 'numerical', 'multi_step', 'case', 'long'] as const;
export type QuestionType = (typeof QUESTION_TYPES)[number];

export const QUESTION_SETS = ['mastery_bank', 'practice_form_a', 'practice_form_b', 'mock', 'onboarding'] as const;
export type QuestionSet = (typeof QUESTION_SETS)[number];

export interface Question {
  id: string;
  /** e.g. the class 8 maths workbook's M8-001. */
  legacyId?: string;
  subtopicId: string;
  chapterId: string;
  subjectId: string;
  conceptGroup: ConceptGroup;
  difficulty: Difficulty;
  type: QuestionType;
  stem: string;
  options?: string[];
  answer: string;
  markingKey: string;
  marks: number;
  minutes: number;
  alrRole: AlrRole;
  likelyGapOnWrong?: GapCode;
  set: QuestionSet;
}

export interface ItemResponse {
  questionId: string;
  correct: boolean;
  secondsTaken: number;
  confidence?: 1 | 2 | 3 | 4 | 5;
  answer?: string;
}
