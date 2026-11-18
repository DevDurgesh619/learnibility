import type { Band, Board, Grade, Hours, Stream, Weight } from './enums';

export interface Subject {
  id: string; // {board}-g{grade}-{subjectSlug}
  board: Board;
  grade: Grade;
  stream: Stream;
  slug: string;
  name: string;
  /** e.g. "IGCSE Physics 0625" */
  programme: string;
  textbook?: string;
  examPattern?: string;
  chapterCount: number;
  /** From the assessment cost sheet. */
  questionTarget: number;
}

export interface Chapter {
  id: string; // {subjectId}-ch{NN}
  subjectId: string;
  order: number;
  name: string;
  /** 40-minute periods. */
  teachingPeriods: number;
  subtopicIds: string[];
}

export interface Subtopic {
  id: string; // {chapterId}-st{N}
  chapterId: string;
  order: number;
  name: string;
  weight: Weight;
  teachingPeriods: number;
  prerequisiteIds: string[];
  /** Earlier-grade skill in words when it is not in the map. */
  prerequisiteNote?: string;
  /** Computed by the mastery-time engine (W3). */
  learnHours: Record<Band, Hours>;
  masterHours: Record<Band, Hours>;
}
