/**
 * The sign-up answers from screens 1e-1g, kept in a small cookie until onboarding finishes
 * (then written to the learner's profile through lib/actions/onboarding.ts).
 */
import type { Board, Grade, Stream } from '@/lib/types';

export const DRAFT_COOKIE = 'learnibility_onboarding';

export const TARGETS = [
  { value: 'board_exams', label: 'Board exams' },
  { value: 'entrance_exams', label: 'Entrance exams (JEE, NEET, CUET, CLAT)' },
  { value: 'sat_act', label: 'SAT / ACT' },
  { value: 'study_abroad', label: 'Study abroad' },
  { value: 'not_sure', label: 'Not sure yet' },
] as const;
export type Target = (typeof TARGETS)[number]['value'];

export const NEEDS = [
  { value: 'tutors', label: 'Tutors and classes', hint: 'Find and book tutors matched to where you are stuck' },
  { value: 'progress', label: 'Progress monitoring', hint: 'Timetable, tests and gap analysis' },
  { value: 'applications', label: 'University applications', hint: 'Shortlist, essays, documents and visa' },
  { value: 'career', label: 'Career mapping', hint: 'Skills to jobs to universities' },
] as const;
export type Need = (typeof NEEDS)[number]['value'];

export interface OnboardingDraft {
  /** Mobile number the student signed up with (demo only). */
  phone?: string;
  name?: string;
  grade?: Grade;
  board?: Board;
  stream?: Stream;
  age?: number;
  target?: Target;
  targetYear?: number;
  needs?: Need[];
  /** 1g, all optional. */
  school?: string;
  lastExamPercent?: number;
  hardSubjects?: string[];
  satStatus?: 'taken' | 'planned' | 'no';
  satScore?: number;
  activities?: string;
  profileSkipped?: boolean;
  /** Onboarding test: true once started from the flow, 'later' when deferred. */
  test?: 'done' | 'later';
}

export function parseDraft(raw: string | undefined): OnboardingDraft {
  if (!raw) return {};
  try {
    const v = JSON.parse(raw);
    return v && typeof v === 'object' ? (v as OnboardingDraft) : {};
  } catch {
    return {};
  }
}

export const BOARD_LABEL: Record<Board, string> = { cbse: 'CBSE', cambridge: 'Cambridge', ib: 'IB' };

export const STEPS = [
  { href: '/onboarding/about', label: 'About you' },
  { href: '/onboarding/needs', label: 'What you need' },
  { href: '/onboarding/profile', label: 'Your profile' },
  { href: '/onboarding/test', label: 'Starting test' },
] as const;
