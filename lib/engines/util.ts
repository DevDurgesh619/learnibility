/** Small pure helpers shared by the engines. */

/** Round half away from zero to `dp` places, like Excel ROUND. */
export function round(x: number, dp = 1): number {
  const f = 10 ** dp;
  const v = Math.abs(x) * f;
  // nudge to absorb binary error such as 2.675 → 2.67499999
  const r = Math.round(v + 1e-9) / f;
  return x < 0 ? -r : r;
}

/** Round up to an integer, like Excel ROUNDUP(x, 0) for positive x. */
export function roundUp(x: number): number {
  return Math.ceil(x - 1e-9);
}

export function clamp(x: number, lo: number, hi: number): number {
  return Math.min(hi, Math.max(lo, x));
}

const DAY_MS = 86_400_000;

/** Add whole days to an ISO timestamp and return ISO. */
export function addDays(iso: string, days: number): string {
  return new Date(Date.parse(iso) + days * DAY_MS).toISOString();
}

/** Whole days from a to b (b − a), floored. */
export function daysBetween(aIso: string, bIso: string): number {
  return Math.floor((Date.parse(bIso) - Date.parse(aIso)) / DAY_MS);
}

/** YYYY-MM-DD of an ISO time shifted by an offset in minutes (e.g. 330 for IST). */
export function localDate(iso: string, offsetMinutes: number): string {
  return new Date(Date.parse(iso) + offsetMinutes * 60_000).toISOString().slice(0, 10);
}

/** Look up a profile parameter value from a ProfileValue list or a plain map. */
export function profileGet<T = unknown>(profile: ProfileLike | undefined, paramId: string): T | undefined {
  if (!profile) return undefined;
  if (Array.isArray(profile)) {
    const hit = profile.filter((p) => p.paramId === paramId).sort((a, b) => (a.asOfUtc < b.asOfUtc ? 1 : -1))[0];
    return hit?.value as T | undefined;
  }
  return profile[paramId] as T | undefined;
}

export type ProfileLike = { paramId: string; value: unknown; asOfUtc: string; tier?: string }[] | Record<string, unknown>;
