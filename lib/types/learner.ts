import type { Band, GapCode, Hours, IsoUtc, Level, SourceMethod, Tier } from './enums';

/** Append-only evidence event (430 file, sheet "AI Event Schema"). */
export interface EvidenceEvent {
  eventId: string;
  learnerId: string;
  timestampUtc: IsoUtc;
  sourceMethod: SourceMethod;
  type: string;
  payload: Record<string, unknown>;
}

export interface MasteryState {
  learnerId: string;
  subtopicId: string;
  level: Level;
  /** 0 to 1. */
  pMastery: number;
  lastTestedUtc: IsoUtc;
  retention?: number;
}

/** ALR indices per chapter (class 8 maths workbook, sheet "ALR Method"). */
export interface AlrSnapshot {
  learnerId: string;
  chapterId: string;
  dK: number;
  R: number;
  TQ: number;
  CE: number;
  ECV: number;
  MCI: number;
  LRS: number;
  band: Band;
}

export const GAP_STATUSES = ['suspected', 'confirmed', 'in_progress', 'closed'] as const;
export type GapStatus = (typeof GAP_STATUSES)[number];

export interface Gap {
  id: string;
  learnerId: string;
  subtopicId: string;
  code: GapCode;
  secondaryFlags: GapCode[];
  level: Level;
  size: number;
  hoursToClose: Hours;
  status: GapStatus;
}

export type Confidence = 'low' | 'medium' | 'high';

/** One value of one of the 430 profile parameters for one learner. */
export interface ProfileValue {
  learnerId: string;
  paramId: string; // p{ID}
  value: unknown;
  source: SourceMethod;
  asOfUtc: IsoUtc;
  confidence: Confidence;
  tier: Tier;
}
