import 'server-only';
import { cookies } from 'next/headers';
import { COLLECTIONS, records, type CollectionName } from '@/lib/store/collections';
import { TUTOR_HOME_COOKIE } from './constants';
import type { TutorPrefs } from './prefs';

/**
 * Tutor settings (Home layout, profile edits) live in the demo store's `tutorSettings` collection when the data
 * layer provides it, so they survive across browsers and reset with the demo. Until then the cookie is used.
 */
export interface TutorSettings { id: string; homeLayout?: 'a' | 'b'; prefs?: TutorPrefs }

export const SETTINGS = 'tutorSettings';
export const hasSettingsStore = () => SETTINGS in COLLECTIONS;

export function storedSettings(tutorId: string): TutorSettings | undefined {
  if (!hasSettingsStore()) return undefined;
  return records<TutorSettings>(SETTINGS as CollectionName).find((r) => r.id === tutorId);
}

export async function homeLayout(tutorId: string): Promise<'a' | 'b'> {
  const stored = storedSettings(tutorId)?.homeLayout;
  if (stored) return stored;
  return (await cookies()).get(TUTOR_HOME_COOKIE)?.value === 'b' ? 'b' : 'a';
}
