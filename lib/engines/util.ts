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

/** Named budget bands (annual rupees) used when a profile stores a band label instead of a number. */
export const ANNUAL_BUDGET_BANDS: Record<string, number> = { none: 0, low: 25_000, medium: 75_000, high: 150_000, very_high: 300_000 };

/**
 * Rupees from a profile value: a number, "₹4,000", "₹1.5 lakh", "50k", a range "₹50,000–1,00,000" (midpoint)
 * or a named band from `bands`. Undefined when it cannot be read.
 */
export function parseInr(v: unknown, bands: Record<string, number> = ANNUAL_BUDGET_BANDS): number | undefined {
  if (typeof v === 'number') return v;
  if (typeof v !== 'string') return undefined;
  const key = v.trim().toLowerCase().replace(/[\s-]+/g, '_');
  if (key in bands) return bands[key];
  const nums = [...v.toLowerCase().matchAll(/(\d[\d,]*(?:\.\d+)?)\s*(lakh|lac|l\b|k\b|cr|crore)?/g)].map((m) => {
    const n = Number(m[1].replace(/,/g, ''));
    const u = m[2];
    return u === 'k' ? n * 1_000 : u && u.startsWith('l') ? n * 100_000 : u && u.startsWith('cr') ? n * 10_000_000 : n;
  });
  if (!nums.length) return undefined;
  return Math.round(nums.length > 1 ? (nums[0] + nums[1]) / 2 : nums[0]);
}

/** Minutes east of UTC for an IANA time zone at a given instant (e.g. Asia/Kolkata → 330). */
export function tzOffsetMinutes(timeZone: string, atIso: string): number {
  const name = new Intl.DateTimeFormat('en-US', { timeZone, timeZoneName: 'longOffset' }).formatToParts(new Date(atIso)).find((p) => p.type === 'timeZoneName')?.value ?? 'GMT';
  const m = /GMT([+-])(\d{2}):?(\d{2})?/.exec(name);
  if (!m) return 0;
  return (m[1] === '-' ? -1 : 1) * (Number(m[2]) * 60 + Number(m[3] ?? 0));
}
