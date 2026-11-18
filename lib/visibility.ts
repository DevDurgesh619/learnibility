/**
 * Role visibility for the 430-parameter profile, following the 430 file's "Sensitivity Tiers" sheet
 * and the blueprint's tier rule:
 *  - T1 Standard: standard product access.
 *  - T2 Elevated (family, financial, psychological, identity-adjacent): role-restricted and
 *    "not shown to the other party verbatim". Parents see a summary, never the student's screened answers.
 *  - T3 Sensitive Health: support adaptation only. Counsellor and the student; parents get a summary
 *    of support in place; nobody else.
 *  - C Consent Artefact: governs processing; visible to the student, the consent-giving parent and the counsellor.
 *  - Tutors see only the gap snapshot a student chose to share when booking.
 *
 * Model-use rule: T3 is never an input to ranking, admissions fit, career fit or work allocation,
 * and consent artefacts are never treated as a learner characteristic.
 */
import type { ProfileParameter, ProfileValue, Role, Tier } from './types';

export type VisibilityMode =
  /** Show the value verbatim. */
  | 'full'
  /** Show that the parameter exists and a non-verbatim summary (e.g. "Wellbeing check done, support in place"). */
  | 'summary'
  /** Show only parameters the student explicitly shared with this person. */
  | 'shared_only'
  /** Do not show at all. */
  | 'hidden';

export const VISIBILITY: Record<Role, Record<Tier, VisibilityMode>> = {
  student: { T1: 'full', T2: 'full', T3: 'full', C: 'full' },
  parent: { T1: 'full', T2: 'summary', T3: 'summary', C: 'full' },
  teacher: { T1: 'full', T2: 'hidden', T3: 'hidden', C: 'hidden' },
  counsellor: { T1: 'full', T2: 'full', T3: 'full', C: 'full' },
  tutor: { T1: 'shared_only', T2: 'hidden', T3: 'hidden', C: 'hidden' },
  mentor: { T1: 'full', T2: 'hidden', T3: 'hidden', C: 'hidden' },
  /** CRM team: no learner profile parameters at all (lead fields live in the CRM, not the 430 profile). */
  sales: { T1: 'hidden', T2: 'hidden', T3: 'hidden', C: 'hidden' },
};

export function visibilityFor(role: Role, tier: Tier): VisibilityMode {
  return VISIBILITY[role][tier];
}

export interface VisibleValue<V = unknown> {
  paramId: string;
  tier: Tier;
  mode: 'full' | 'summary';
  /** Present only when mode is 'full'. */
  value?: V;
  source?: ProfileValue['source'];
  asOfUtc?: string;
  confidence?: ProfileValue['confidence'];
}

export interface VisibilityOptions {
  /** Parameter IDs the student shared with this viewer (used for tutors). */
  sharedParamIds?: Iterable<string>;
  /** Viewer is looking at their own record (a student viewing themself). */
  isSelf?: boolean;
}

/**
 * Filter one learner's profile values for a viewer role. Hidden values are dropped; summary values
 * keep the parameter and metadata but not the value itself.
 */
export function visibleProfile(
  values: ProfileValue[],
  role: Role,
  opts: VisibilityOptions = {},
): VisibleValue[] {
  const shared = new Set(opts.sharedParamIds ?? []);
  const out: VisibleValue[] = [];
  for (const v of values) {
    let mode = visibilityFor(role, v.tier);
    if (role === 'student' && opts.isSelf === false) mode = v.tier === 'T1' ? 'summary' : 'hidden';
    if (mode === 'shared_only') mode = shared.has(v.paramId) ? 'full' : 'hidden';
    if (mode === 'hidden') continue;
    if (mode === 'full') {
      out.push({ paramId: v.paramId, tier: v.tier, mode, value: v.value, source: v.source, asOfUtc: v.asOfUtc, confidence: v.confidence });
    } else {
      out.push({ paramId: v.paramId, tier: v.tier, mode, asOfUtc: v.asOfUtc });
    }
  }
  return out;
}

/** Parameters (definitions) a role may see at all, e.g. to build a profile screen. */
export function visibleParameters(params: ProfileParameter[], role: Role, opts: VisibilityOptions = {}): ProfileParameter[] {
  const shared = new Set(opts.sharedParamIds ?? []);
  return params.filter((p) => {
    const mode = visibilityFor(role, p.tier);
    if (mode === 'hidden') return false;
    if (mode === 'shared_only') return shared.has(p.id);
    return true;
  });
}

export const MODEL_PURPOSES = [
  'support_adaptation',
  'learning_plan',
  'ranking',
  'admissions_fit',
  'career_fit',
  'work_allocation',
  'tutor_matching',
] as const;
export type ModelPurpose = (typeof MODEL_PURPOSES)[number];

const T3_FORBIDDEN: ModelPurpose[] = ['ranking', 'admissions_fit', 'career_fit', 'work_allocation', 'tutor_matching'];

/** May a parameter of this tier feed an engine used for this purpose? */
export function canUseForPurpose(tier: Tier, purpose: ModelPurpose): boolean {
  if (tier === 'C') return false;
  if (tier === 'T3') return !T3_FORBIDDEN.includes(purpose);
  return true;
}

/** Drop values an engine may not use for the given purpose (engines call this before scoring). */
export function valuesForPurpose<T extends { tier: Tier }>(values: T[], purpose: ModelPurpose): T[] {
  return values.filter((v) => canUseForPurpose(v.tier, purpose));
}
