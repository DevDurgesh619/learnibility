/**
 * Engine 8: ranked "do this next" actions for the student home screen, each with a reason.
 * Source: blueprint "The engines behind the daily loop" (next best action) and W3 brief.
 *
 * Scoring (higher first; ties broken by kind order below):
 *   deadline within 14 days     100 − 3 × days left (overdue = 100)
 *   reviews due today/overdue   85 (+1 per extra review, max +5)
 *   weekly test not yet taken   82 on its day or later, 40 earlier in the week
 *   biggest weighted gap        55 + 3 × hours to close, G1 +5 (fix prerequisites first), max 80
 *   next gap(s)                 same formula − 10, up to 2 more
 *   profile completion < 80%    30 + (80 − completion) ÷ 4
 *   career exploration          20 (grades 9-12 with no career shortlisted; 10 for grade 8)
 */
import type { Grade, IsoUtc } from '../types';
import { daysBetween, localDate } from './util';

export type ActionKind = 'deadline' | 'review' | 'weekly_test' | 'gap' | 'profile' | 'career';

export interface NbaState {
  learnerId: string;
  now: IsoUtc;
  tzOffsetMinutes?: number;
  grade?: Grade;
  deadlines?: { id: string; title: string; dueUtc: IsoUtc; href?: string }[];
  /** Reviews due (from the timetable or mastery states). */
  reviewsDue?: { id: string; title: string; dueUtc: IsoUtc }[];
  weeklyTest?: { dueUtc: IsoUtc; taken: boolean; href?: string };
  gaps?: { id: string; subtopicId: string; code: string; hoursToClose: number; title?: string; status?: string }[];
  /** 0-100 */
  profileCompletionPct?: number;
  careersShortlisted?: number;
}

export interface NextAction {
  id: string;
  kind: ActionKind;
  title: string;
  reason: string;
  score: number;
  refId?: string;
  href?: string;
}

const KIND_ORDER: ActionKind[] = ['deadline', 'review', 'weekly_test', 'gap', 'profile', 'career'];

export function nextBestAction(state: NbaState, limit = 5): NextAction[] {
  const off = state.tzOffsetMinutes ?? 330;
  const today = localDate(state.now, off);
  const out: NextAction[] = [];

  for (const d of state.deadlines ?? []) {
    const days = daysBetween(today + 'T00:00:00.000Z', localDate(d.dueUtc, off) + 'T00:00:00.000Z');
    if (days > 14) continue;
    out.push({
      id: `nba_deadline_${d.id}`, kind: 'deadline', title: d.title, refId: d.id, href: d.href,
      score: days < 0 ? 100 : 100 - 3 * days,
      reason: days < 0 ? `Overdue by ${-days} day${days === -1 ? '' : 's'}.` : days === 0 ? 'Due today.' : `Due in ${days} day${days === 1 ? '' : 's'}.`,
    });
  }

  const due = (state.reviewsDue ?? []).filter((r) => localDate(r.dueUtc, off) <= today);
  if (due.length) {
    out.push({
      id: 'nba_reviews', kind: 'review', title: due.length === 1 ? due[0].title : `${due.length} quick reviews`, refId: due[0].id,
      score: 85 + Math.min(5, due.length - 1),
      reason: `${due.length} spaced review${due.length === 1 ? ' is' : 's are'} due; doing ${due.length === 1 ? 'it' : 'them'} on time keeps retention above 70%.`,
    });
  }

  if (state.weeklyTest && !state.weeklyTest.taken) {
    const onDay = localDate(state.weeklyTest.dueUtc, off) <= today;
    out.push({
      id: 'nba_weekly_test', kind: 'weekly_test', title: 'Take this week’s test', href: state.weeklyTest.href,
      score: onDay ? 82 : 40,
      reason: onDay ? 'The weekly test is due; it re-checks your gaps and re-plans next week.' : 'The weekly test is coming up on Saturday.',
    });
  }

  const gaps = (state.gaps ?? []).filter((g) => g.status !== 'closed' && g.hoursToClose > 0)
    .map((g) => ({ g, s: Math.min(80, 55 + 3 * g.hoursToClose + (g.code === 'G1' ? 5 : 0)) }))
    .sort((a, b) => b.s - a.s);
  gaps.slice(0, 3).forEach(({ g, s }, i) => {
    out.push({
      id: `nba_gap_${g.id}`, kind: 'gap', title: g.title ?? `Work on ${g.subtopicId}`, refId: g.id,
      score: i === 0 ? s : s - 10,
      reason: i === 0
        ? `Your biggest gap (${g.code}, about ${g.hoursToClose} h to close)${g.code === 'G1' ? '; fixing the prerequisite first makes everything after it faster' : ''}.`
        : `Next gap (${g.code}, about ${g.hoursToClose} h).`,
    });
  });

  if (state.profileCompletionPct !== undefined && state.profileCompletionPct < 80) {
    out.push({
      id: 'nba_profile', kind: 'profile', title: 'Complete your profile', href: '/student/profile',
      score: 30 + (80 - state.profileCompletionPct) / 4,
      reason: `Your profile is ${state.profileCompletionPct}% complete; more answers make the plan and matches more accurate.`,
    });
  }

  if (!state.careersShortlisted) {
    const g = state.grade ?? 9;
    out.push({
      id: 'nba_career', kind: 'career', title: 'Explore careers that fit you', href: '/student/careers',
      score: g >= 9 ? 20 : 10,
      reason: g >= 11 ? 'No careers shortlisted yet; entrance-exam choices depend on it.' : 'No careers shortlisted yet; a first look helps choose subjects and streams.',
    });
  }

  return out
    .sort((a, b) => b.score - a.score || KIND_ORDER.indexOf(a.kind) - KIND_ORDER.indexOf(b.kind) || a.id.localeCompare(b.id))
    .slice(0, limit)
    .map((a) => ({ ...a, score: Math.round(a.score * 10) / 10 }));
}
