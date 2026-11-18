/**
 * Engine 6: rank tutors for a learner's diagnosed gaps.
 * Source: W3 brief (weights), blueprint "The engines behind the daily loop" (tutor matching),
 * Design Edu Tech PDF area 5 (Explore Tutors), catalogue type Tutor (lib/types/catalogue.ts).
 *
 * Score out of 100:
 *   topic 40      per gap, weighted by hours to close: teaches the subject, board and grade = 20;
 *                 plus a topic-strength tag found in the chapter or subtopic name = 40
 *   style fit 20  tutor's primary style is one the gap type calls for (or the learner's stated
 *                 preference) = 20; a secondary style = 12; otherwise 4
 *   price 15      hourly price within the learner's hourly budget = 15, falling linearly to 0 at 2× budget;
 *                 budget unknown = 8
 *   rating 10     Bayesian rating (prior 4.0 worth 10 reviews) ÷ 5 × 10
 *   slots 10      overlapping weekly minutes with the learner's study windows (tutor slots read in the
 *                 tutor's own time zone); 2 sessions' worth = 10
 *   language 5    shares a language with the learner = 5
 * Filters: mode (online, or offline in the learner's city) and format. Unverified tutors are kept but
 * ranked with a 5-point penalty. T3 data is never read; the budget (T2) is used only for price fit.
 */
import type { Board, Gap, Grade } from '../types';
import type { AvailabilitySlot, SessionFormat, SessionMode, TeachingStyle, Tutor, Weekday } from '../types/catalogue';
import { parseSubtopicId, slugify } from '../ids';
import { parseInr, ProfileLike, profileGet, round, tzOffsetMinutes } from './util';

/** Teaching styles each gap type calls for, best first. */
export const STYLE_FOR_GAP: Record<string, TeachingStyle[]> = {
  G1: ['concept_first', 'socratic'],
  G2: ['concept_first', 'socratic'],
  G3: ['practice_first', 'exam_focused'],
  G4: ['practice_first', 'exam_focused'],
  G5: ['socratic', 'project_based'],
  G6: ['practice_first', 'exam_focused'],
  G7: ['concept_first', 'socratic'],
  G8: ['exam_focused', 'practice_first'],
  G9: ['socratic', 'concept_first'],
  G10: ['project_based', 'socratic'],
};

export interface TutorMatchGap extends Pick<Gap, 'id' | 'subtopicId' | 'code' | 'hoursToClose'> {
  /** Override when the subtopic id does not carry them. */
  subjectSlug?: string;
  board?: Board;
  grade?: Grade;
}

export interface TutorMatchContext {
  /** Names of subtopics and chapters, keyed by id, for topic matching and reasons. */
  names?: Record<string, string>;
  /** Learner's weekly study windows (local time). */
  availability?: { day: Weekday; start: string; end: string }[];
  mode?: SessionMode | 'any';
  city?: string;
  format?: SessionFormat;
  /** Rupees a month for tutoring; falls back to profile p178. */
  monthlyBudgetInr?: number;
  /** Planned tutoring hours a month (default 8: 2 × 60 min a week). */
  hoursPerMonth?: number;
  languages?: string[];
  preferredStyle?: TeachingStyle;
  /** Learner's offset east of UTC in minutes (default 330, IST). */
  tzOffsetMinutes?: number;
  /** Instant used to resolve tutors' time-zone offsets (DST); pass `now`. */
  now?: string;
  limit?: number;
}

export interface TutorMatch {
  tutorId: string;
  name: string;
  score: number;
  parts: { topic: number; style: number; price: number; rating: number; slots: number; language: number };
  pricePerHourInr: number;
  matchedGaps: string[];
  sharedSlotMinutes: number;
  reason: string;
}

const toMin = (t: string) => Number(t.slice(0, 2)) * 60 + Number(t.slice(3, 5));
const WEEK = 7 * 1440;
const DAY_INDEX: Record<Weekday, number> = { mon: 0, tue: 1, wed: 2, thu: 3, fri: 4, sat: 5, sun: 6 };

/** Weekly windows as [start, end) minute-of-week intervals in UTC, split at the week boundary. */
function weekIntervals(slots: { day: Weekday; start: string; end: string }[], offsetMinutes: number): [number, number][] {
  const out: [number, number][] = [];
  for (const s of slots) {
    let a = DAY_INDEX[s.day] * 1440 + toMin(s.start) - offsetMinutes;
    const len = toMin(s.end) - toMin(s.start);
    if (len <= 0) continue;
    a = ((a % WEEK) + WEEK) % WEEK;
    const b = a + len;
    if (b <= WEEK) out.push([a, b]);
    else out.push([a, WEEK], [0, b - WEEK]);
  }
  return out;
}

/**
 * Weekly minutes when both are free. The learner's windows are in `learnerOffset` (default IST);
 * the tutor's in `tutorTimeZone` (IANA), converted at `atIso`.
 */
export function slotOverlapMinutes(a: { day: Weekday; start: string; end: string }[], b: AvailabilitySlot[], opts: { learnerOffset?: number; tutorTimeZone?: string; atIso?: string } = {}): number {
  const lo = opts.learnerOffset ?? 330;
  const to = opts.tutorTimeZone ? tzOffsetMinutes(opts.tutorTimeZone, opts.atIso ?? '2026-11-18T00:00:00Z') : lo;
  let total = 0;
  for (const [x1, x2] of weekIntervals(a, lo)) for (const [y1, y2] of weekIntervals(b, to)) total += Math.max(0, Math.min(x2, y2) - Math.max(x1, y1));
  return total;
}

function words(s: string): Set<string> {
  return new Set(slugify(s).split('-').filter((w) => w.length > 2));
}

function topicScore(t: Tutor, g: TutorMatchGap, names: Record<string, string>): { score: number; tag?: string } {
  const p = parseSubtopicId(g.subtopicId);
  const slug = g.subjectSlug ?? p?.slug;
  const board = g.board ?? p?.board;
  const grade = g.grade ?? p?.grade;
  const subj = t.subjects.find((s) => s.subjectSlug === slug && (!board || s.boards.includes(board)) && (!grade || s.grades.includes(grade)));
  if (!subj) return { score: 0 };
  const text = new Set([...words(names[g.subtopicId] ?? ''), ...words(p ? names[p.chapterId] ?? '' : '')]);
  const tag = subj.topicStrengths.find((tg) => {
    const w = tg.split('-').filter((x) => x.length > 2);
    return w.length > 0 && w.every((x) => text.has(x) || [...text].some((y) => y.startsWith(x) || x.startsWith(y)));
  });
  return { score: tag ? 40 : 20, tag };
}

/** Monthly rupees from p178 (annual education budget) ÷ 12. */
function budgetFrom(profile: ProfileLike | undefined): number | undefined {
  const annual = parseInr(profileGet(profile, 'p178'));
  return annual === undefined ? undefined : annual / 12;
}

const inr = (n: number) => '₹' + n.toLocaleString('en-IN');
const STYLE_LABEL: Record<TeachingStyle, string> = { concept_first: 'concept-first', practice_first: 'practice-first', socratic: 'Socratic', exam_focused: 'exam-focused', project_based: 'project-based' };

export function matchTutors(gaps: TutorMatchGap[], profile: ProfileLike | undefined, tutors: Tutor[], ctx: TutorMatchContext = {}): TutorMatch[] {
  const names = ctx.names ?? {};
  const open = gaps.filter((g) => g.hoursToClose > 0);
  const totalHours = open.reduce((s, g) => s + g.hoursToClose, 0) || 1;
  const budget = ctx.monthlyBudgetInr ?? budgetFrom(profile);
  const hourlyBudget = budget === undefined ? undefined : budget / (ctx.hoursPerMonth ?? 8);
  const langs = (ctx.languages ?? (profileGet<string[]>(profile, 'p157') ?? [])).map((l) => l.toLowerCase());
  const mode = ctx.mode ?? 'any';
  const format = ctx.format ?? 'one_to_one';
  // dominant gap type decides the style the learner needs
  const byCode = new Map<string, number>();
  for (const g of open) byCode.set(g.code, (byCode.get(g.code) ?? 0) + g.hoursToClose);
  const mainCode = [...byCode.entries()].sort((a, b) => b[1] - a[1])[0]?.[0];
  const wanted = ctx.preferredStyle ? [ctx.preferredStyle] : (mainCode ? STYLE_FOR_GAP[mainCode] : []);

  const out: TutorMatch[] = [];
  for (const t of tutors) {
    if (mode === 'online' && !t.modes.includes('online')) continue;
    if (mode === 'offline' && !(t.modes.includes('offline') && (!ctx.city || t.city.toLowerCase() === ctx.city.toLowerCase()))) continue;
    if (!t.formats.includes(format)) continue;
    const price = format === 'group' ? t.pricing.groupPerStudentPerHourInr ?? t.pricing.oneToOnePerHourInr : t.pricing.oneToOnePerHourInr;

    let topic = 0;
    const matched: string[] = [];
    const tags: string[] = [];
    for (const g of open) {
      const ts = topicScore(t, g, names);
      topic += (ts.score * g.hoursToClose) / totalHours;
      if (ts.score > 0) matched.push(g.id);
      if (ts.tag) tags.push(names[g.subtopicId] ?? ts.tag);
    }
    if (open.length && matched.length === 0) continue; // cannot help with any gap

    const style = wanted.length === 0 ? 10 : wanted.includes(t.teachingStyles[0]) ? 20 : t.teachingStyles.slice(1).some((s) => wanted.includes(s)) ? 12 : 4;
    const priceScore = hourlyBudget === undefined ? 8 : hourlyBudget <= 0 ? 0 : price <= hourlyBudget ? 15 : Math.max(0, 15 * (1 - (price - hourlyBudget) / hourlyBudget));
    const bayes = (t.rating * t.reviewsCount + 4.0 * 10) / (t.reviewsCount + 10);
    const rating = (bayes / 5) * 10;
    const shared = ctx.availability ? slotOverlapMinutes(ctx.availability, t.availability, { learnerOffset: ctx.tzOffsetMinutes, tutorTimeZone: t.timeZone, atIso: ctx.now }) : 0;
    const slots = ctx.availability ? Math.min(10, (shared / (2 * t.sessionMinutes)) * 10) : 5;
    const sharedLang = t.languages.find((l) => langs.includes(l.toLowerCase()));
    const language = langs.length === 0 ? 3 : sharedLang ? 5 : 0;
    const penalty = t.verified ? 0 : 5;
    const score = round(Math.max(0, topic + style + priceScore + rating + slots + language - penalty), 1);

    const subj = open.length ? parseSubtopicId(open[0].subtopicId) : null;
    const bits = [
      tags.length ? `Strong in ${tags.slice(0, 2).join(' and ')}` : matched.length ? `Teaches ${subj?.slug ?? 'this subject'}${subj ? ` for ${subj.board.toUpperCase()} class ${subj.grade}` : ''}` : 'General support',
      wanted.length ? `${STYLE_LABEL[t.teachingStyles[0]]} teaching${wanted.includes(t.teachingStyles[0]) ? ` suits ${ctx.preferredStyle ? 'your preference' : `a ${mainCode} gap`}` : ''}` : null,
      `${inr(price)}/hr${hourlyBudget !== undefined ? (price <= hourlyBudget ? ' within budget' : ` (budget ${inr(Math.round(hourlyBudget))}/hr)`) : ''}`,
      `${t.rating.toFixed(1)}★ from ${t.reviewsCount} reviews`,
      ctx.availability ? (shared >= 2 * t.sessionMinutes ? `${Math.floor(shared / t.sessionMinutes)} shared slots a week` : shared >= t.sessionMinutes ? '1 shared slot a week' : 'few shared slots') : null,
      sharedLang && sharedLang.toLowerCase() !== 'english' ? `teaches in ${sharedLang}` : null,
      t.pricing.demoInr === 0 ? 'free demo' : null,
      t.verified ? null : 'not yet verified',
    ].filter(Boolean);

    out.push({
      tutorId: t.id, name: t.displayName, score,
      parts: { topic: round(topic, 1), style, price: round(priceScore, 1), rating: round(rating, 1), slots: round(slots, 1), language },
      pricePerHourInr: price, matchedGaps: matched, sharedSlotMinutes: shared, reason: bits.join('; ') + '.',
    });
  }
  return out.sort((a, b) => b.score - a.score || a.pricePerHourInr - b.pricePerHourInr || a.tutorId.localeCompare(b.tutorId)).slice(0, ctx.limit ?? 10);
}
