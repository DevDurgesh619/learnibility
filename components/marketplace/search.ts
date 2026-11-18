import type { Board } from '@/lib/types';
import type { SessionFormat, SessionMode, Tutor } from '@/lib/types/catalogue';
import { subjectLabel, tagLabel } from './labels';

/** Filters from the Explore Tutors panel (PDF 5b). All optional; values come from the URL. */
export interface TutorFilters {
  q?: string;
  subject?: string;
  board?: Board;
  minRating?: number;
  maxPrice?: number;
  format?: SessionFormat;
  mode?: SessionMode;
  language?: string;
  verified?: boolean;
}

export const RATING_OPTIONS = [3, 4, 4.5] as const;
export const PRICE_OPTIONS = [500, 800, 1000, 1500, 3000] as const;

/** Parse URL search params into filters, ignoring anything unknown. */
export function parseFilters(sp: Record<string, string | string[] | undefined>): TutorFilters {
  const one = (k: string) => (Array.isArray(sp[k]) ? sp[k]![0] : sp[k]) as string | undefined;
  const num = (k: string) => { const v = Number(one(k)); return Number.isFinite(v) && v > 0 ? v : undefined; };
  const f: TutorFilters = {};
  const q = one('q')?.trim(); if (q) f.q = q;
  const subject = one('subject'); if (subject) f.subject = subject;
  const board = one('board'); if (board === 'cbse' || board === 'cambridge' || board === 'ib') f.board = board;
  f.minRating = num('rating'); f.maxPrice = num('price');
  const format = one('format'); if (format === 'one_to_one' || format === 'group') f.format = format;
  const mode = one('mode'); if (mode === 'online' || mode === 'offline') f.mode = mode;
  const language = one('lang'); if (language) f.language = language;
  if (one('verified') === '1') f.verified = true;
  for (const k of Object.keys(f) as (keyof TutorFilters)[]) if (f[k] === undefined) delete f[k];
  return f;
}

export function filtersToParams(f: TutorFilters): URLSearchParams {
  const p = new URLSearchParams();
  if (f.q) p.set('q', f.q);
  if (f.subject) p.set('subject', f.subject);
  if (f.board) p.set('board', f.board);
  if (f.minRating) p.set('rating', String(f.minRating));
  if (f.maxPrice) p.set('price', String(f.maxPrice));
  if (f.format) p.set('format', f.format);
  if (f.mode) p.set('mode', f.mode);
  if (f.language) p.set('lang', f.language);
  if (f.verified) p.set('verified', '1');
  return p;
}

/** Number of filters set, not counting the text query (the "Filters · 2" badge). */
export const activeFilterCount = (f: TutorFilters) => Object.keys(f).filter((k) => k !== 'q').length;

/** Text a tutor can be found by: name, headline, subjects, topic strengths, exams, languages, city. */
export function searchText(t: Tutor): string {
  return [
    t.displayName, t.headline, t.city, t.idealStudent,
    ...t.subjects.flatMap((s) => [s.subjectSlug, subjectLabel(s.subjectSlug), ...s.topicStrengths.map(tagLabel)]),
    ...t.examPrep, ...t.examPrep.map((e) => e.replace(/-/g, ' ')), ...t.languages,
  ].join(' ').toLowerCase();
}

/** Hourly price for the chosen format; group falls back to 1-on-1 when the tutor has no group rate. */
export function priceFor(t: Tutor, format: SessionFormat = 'one_to_one'): number {
  return format === 'group' ? t.pricing.groupPerStudentPerHourInr ?? t.pricing.oneToOnePerHourInr : t.pricing.oneToOnePerHourInr;
}

/** Every word of the query must appear somewhere in the tutor's search text ("SAT math" finds SAT maths tutors). */
export function matchesQuery(t: Tutor, q: string): boolean {
  const hay = searchText(t);
  return q.toLowerCase().split(/\s+/).filter(Boolean).every((w) => hay.includes(w.replace(/s$/, '')));
}

export function filterTutors(tutors: Tutor[], f: TutorFilters): Tutor[] {
  return tutors.filter((t) => {
    if (f.q && !matchesQuery(t, f.q)) return false;
    if (f.subject && !t.subjects.some((s) => s.subjectSlug === f.subject && (!f.board || s.boards.includes(f.board)))) return false;
    if (!f.subject && f.board && !t.subjects.some((s) => s.boards.includes(f.board!))) return false;
    if (f.minRating && t.rating < f.minRating) return false;
    if (f.format && !t.formats.includes(f.format)) return false;
    if (f.maxPrice && priceFor(t, f.format) > f.maxPrice) return false;
    if (f.mode && !t.modes.includes(f.mode)) return false;
    if (f.language && !t.languages.some((l) => l.toLowerCase() === f.language!.toLowerCase())) return false;
    if (f.verified && !t.verified) return false;
    return true;
  });
}

/** Tutors similar to a set of results: same subjects, not already shown ("More like these", PDF 5c). */
export function moreLikeThese(all: Tutor[], shown: Tutor[], limit = 3): Tutor[] {
  const ids = new Set(shown.map((t) => t.id));
  const subjects = new Set(shown.flatMap((t) => t.subjects.map((s) => s.subjectSlug)));
  return all
    .filter((t) => !ids.has(t.id) && t.subjects.some((s) => subjects.has(s.subjectSlug)))
    .sort((a, b) => b.rating - a.rating || b.reviewsCount - a.reviewsCount)
    .slice(0, limit);
}
