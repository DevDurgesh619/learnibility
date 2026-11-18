/** Type-only re-exports so lib/data/types.ts has one import site. */
export type {
  AlrSnapshot,
  ApplicationType,
  Band,
  Board,
  Gap,
  GapCode,
  Grade,
  Inr,
  IsoUtc,
  ItemResponse,
  Level,
  MasteryState,
  Role,
  SessionFormat,
  SessionMode,
  Stream,
} from '@/lib/types';
export type { CareerFit, CareerGapResult, InterventionPlan, NextAction, StudyWindow, Timetable, TimetableBlock } from '@/lib/engines';
