/**
 * Shared enums. Source of truth: docs/contracts.md (Wave 1 shared contract).
 * Gap codes, level ladder and band parameters follow the CBSE class 8 maths workbook
 * (sheets Gap Diagnosis, Mastery Inputs, ALR Method).
 */

export const BOARDS = ['cbse', 'cambridge', 'ib'] as const;
export type Board = (typeof BOARDS)[number];

export const GRADES = [8, 9, 10, 11, 12] as const;
export type Grade = (typeof GRADES)[number];

/** 'none' for grades 8 to 10. */
export const STREAMS = ['none', 'science', 'commerce', 'humanities'] as const;
export type Stream = (typeof STREAMS)[number];

/** Subtopic weight: Light, Standard, Heavy. */
export const WEIGHTS = ['L', 'S', 'H'] as const;
export type Weight = (typeof WEIGHTS)[number];

export const CONCEPT_GROUPS = ['C1', 'C2', 'C3', 'C4'] as const;
export type ConceptGroup = (typeof CONCEPT_GROUPS)[number];

export const DIFFICULTIES = ['D1', 'D2', 'D3', 'D4', 'D5'] as const;
export type Difficulty = (typeof DIFFICULTIES)[number];

export const ALR_ROLES = ['practised', 'retention_probe', 'transfer_probe'] as const;
export type AlrRole = (typeof ALR_ROLES)[number];

/** L0 to L5 mastery ladder. */
export const LEVELS = [0, 1, 2, 3, 4, 5] as const;
export type Level = (typeof LEVELS)[number];

export const GAP_CODES = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10'] as const;
export type GapCode = (typeof GAP_CODES)[number];

export const BANDS = ['below_avg', 'average', 'above_avg', 'excellent'] as const;
export type Band = (typeof BANDS)[number];

export const ROLES = ['student', 'parent', 'teacher', 'counsellor', 'tutor', 'mentor'] as const;
export type Role = (typeof ROLES)[number];

/** Collection methods M1 to M20 from the 430-parameter file's Collection Method Legend. */
export type SourceMethod = `M${1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20}`;
export const SOURCE_METHODS = Array.from({ length: 20 }, (_, i) => `M${i + 1}`) as SourceMethod[];

/** Sensitivity tiers: T1 Standard, T2 Elevated, T3 Sensitive Health, C Consent Artefact. */
export const TIERS = ['T1', 'T2', 'T3', 'C'] as const;
export type Tier = (typeof TIERS)[number];

/** Timestamps are ISO 8601 UTC strings, e.g. "2026-08-19T06:00:00Z". */
export type IsoUtc = string;

/** Money is integer Indian rupees. */
export type Inr = number;

/** Hours are decimals rounded to 0.1. */
export type Hours = number;
