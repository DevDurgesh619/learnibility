import 'server-only';
import { cookies } from 'next/headers';
import type { Tutor } from '@/lib/types/catalogue';

/**
 * Profile, availability, pricing and payout edits (7c, 8a-8e) have no shared collection yet, so they are kept per
 * browser in a cookie and laid over the catalogue record on the tutor's own screens.
 */
export interface TutorPrefs {
  headline?: string; bio?: string; idealStudent?: string;
  teachingStyles?: Tutor['teachingStyles']; formats?: Tutor['formats']; modes?: Tutor['modes']; homework?: Tutor['homework'];
  audiences?: Tutor['audiences']; helpTypes?: Tutor['helpTypes'];
  availability?: Tutor['availability']; maxSessionsPerDay?: number; blocked?: { from: string; to: string; label: string }[];
  pricing?: Partial<Tutor['pricing']>;
  payout?: { schedule: 'weekly' | 'monthly'; minimumInr: number; upi?: string; gstin?: string };
  onboarded?: boolean;
}

export const prefsCookie = (tutorId: string) => `lb_tutor_prefs_${tutorId}`;

export async function readPrefs(tutorId: string): Promise<TutorPrefs> {
  const raw = (await cookies()).get(prefsCookie(tutorId))?.value;
  if (!raw) return {};
  try { return JSON.parse(raw) as TutorPrefs; } catch { return {}; }
}

export function withPrefs(t: Tutor, p: TutorPrefs): Tutor {
  return {
    ...t,
    headline: p.headline ?? t.headline, bio: p.bio ?? t.bio, idealStudent: p.idealStudent ?? t.idealStudent,
    teachingStyles: p.teachingStyles ?? t.teachingStyles, formats: p.formats ?? t.formats, modes: p.modes ?? t.modes, homework: p.homework ?? t.homework,
    audiences: p.audiences ?? t.audiences, helpTypes: p.helpTypes ?? t.helpTypes,
    availability: p.availability ?? t.availability, maxSessionsPerDay: p.maxSessionsPerDay ?? t.maxSessionsPerDay,
    pricing: { ...t.pricing, ...(p.pricing ?? {}) },
  };
}

/** Catalogue strength plus 10 points once the tutor writes their own intro (8a nudge). */
export function profileStrength(base: number, prefs: TutorPrefs) {
  return Math.min(100, base + (prefs.bio ? 10 : 0));
}
