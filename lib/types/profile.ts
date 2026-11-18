import type { SourceMethod, Tier } from './enums';

export const PROFILE_SECTIONS = [
  'Academic Profile',
  'Learning Behaviour',
  'Cognitive',
  'Biological Readiness',
  'Psychological & Emotional',
  'Social',
  'Communication & Language',
  'Economic',
  'Global Mobility',
  'Career & Future Skills',
  'Portfolio',
  'Real-Time Learning Dynamics & Model Quality',
] as const;
export type ProfileSection = (typeof PROFILE_SECTIONS)[number];

export const CADENCES = ['Once', 'Annual', 'Term', 'Monthly', 'Weekly', 'Continuous', 'As needed'] as const;
export type Cadence = (typeof CADENCES)[number];

/** One of the 430 parameters (data/profile/parameters.json). */
export interface ProfileParameter {
  id: string; // p{ID}
  number: number; // 1..430
  origin: 'existing_277' | 'proposed_v2';
  section: ProfileSection;
  category: string;
  name: string;
  description: string;
  /** As written in the source, e.g. "Scale 1-5", "Enum", "0-100 score". */
  dataType: string;
  /** Collection methods in preferential order. */
  methods: SourceMethod[];
  /** Method wording as written in the source, for display. */
  methodsText: string;
  phase1Default: SourceMethod | null;
  tier: Tier;
  handlingNote?: string;
  cadence: Cadence;
  refreshesPerYear: number | null;
  aiUse?: string;
  evidenceDensity?: string;
  humanValidation?: string;
  externalShareRule?: string;
}

export interface CollectionMethod {
  code: SourceMethod;
  name: string;
  intrusiveness: 'Low' | 'Medium' | 'High';
  tierGroup: string;
  guidance: string;
}

export interface SensitivityTier {
  tier: Tier;
  label: string;
  count: number;
  definition: string;
  modelUseRule: string;
}
