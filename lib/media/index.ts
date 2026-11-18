import { PERSON_PHOTOS, type PersonPhoto } from './people-data';

export type { PersonPhoto };
export { PERSON_PHOTOS };

const BY_NAME = new Map<string, PersonPhoto>();
for (const p of Object.values(PERSON_PHOTOS)) BY_NAME.set(normal(p.name), p);

function normal(s: string) {
  return s.normalize('NFKD').replace(/[’']/g, '').replace(/\s+/g, ' ').trim().toLowerCase();
}

/**
 * Profile photo for a persona or tutor, looked up by ID (lrn_, tut_, csl_ ...) or by display name.
 * Returns undefined for anyone without a photo, so callers fall back to initials.
 */
export function photoFor(idOrName: string | undefined | null): string | undefined {
  if (!idOrName) return undefined;
  return (PERSON_PHOTOS[idOrName] ?? BY_NAME.get(normal(idOrName)))?.src;
}

import { UNI_PHOTOS, type UniPhoto } from './universities-data';

export type { UniPhoto };
export { UNI_PHOTOS };

/** Campus photo for a university in the catalogue (bundled under /public/media/universities). */
export function uniPhoto(universityId: string | undefined | null): UniPhoto | undefined {
  return universityId ? UNI_PHOTOS[universityId] : undefined;
}
