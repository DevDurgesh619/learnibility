import 'server-only';
import type { TutorMatch } from '@/lib/engines';
import { getBookings, getGaps, getSessions, getStudent, getTutor, getTutorMatches, listTutors, namesFor } from '@/lib/data';
import type { Booking, GapRecord, GapSnapshot, Student } from '@/lib/data/types';
import { DEMO_NOW } from '@/lib/demo-clock';
import type { Tutor } from '@/lib/types/catalogue';
import { parseSubtopicId } from '@/lib/ids';
import { listPersonas } from '@/lib/data/personas';
import { demoSlots, type BusyInterval, type DemoDay } from './slots';

/** Everything Explore Tutors needs about the signed-in student, in one read. */
export interface MarketplaceLearner {
  student: Student;
  openGaps: GapRecord[];
  names: Record<string, string>;
  bookings: Booking[];
  matches: TutorMatch[];
}

export async function loadMarketplaceLearner(learnerId: string): Promise<MarketplaceLearner | undefined> {
  const student = await getStudent(learnerId);
  if (!student) return undefined;
  const gaps = getGaps(learnerId, { status: 'open' });
  const names = namesFor([...new Set([...student.subjects.map((s) => s.subjectId), ...gaps.map((g) => g.subjectId)])]);
  const bookings = getBookings(learnerId);
  // Engine 5 via the data layer: budget and languages from the profile, never T3.
  const matches = gaps.length ? withLoginTutors(getTutorMatches(learnerId, { limit: 40 })).slice(0, 12) : [];
  return { student, openGaps: gaps, names, bookings, matches };
}

const SHOWN = 6;

/**
 * Demo rule: a tutor who has a login on the persona picker and genuinely fits (the engine matched at least one of
 * the learner's gaps, score at least 70% of the best) is moved into the 6 recommendations shown, so a booking can
 * be followed to the tutor side. Order otherwise stays the engine's.
 */
function withLoginTutors(matches: TutorMatch[]): TutorMatch[] {
  const logins = new Set(listPersonas().filter((p) => p.role === 'tutor').map((p) => p.id));
  const top = matches[0]?.score ?? 0;
  const lift = matches.slice(SHOWN).filter((m) => logins.has(m.tutorId) && m.matchedGaps.length > 0 && m.score >= top * 0.7);
  if (!lift.length) return matches;
  const shown = matches.slice(0, SHOWN);
  const keep = shown.slice(0, Math.max(0, SHOWN - lift.length));
  const out = [...keep, ...lift];
  return [...out, ...matches.filter((m) => !out.includes(m))];
}

/** Subject of the learner's biggest open gaps, used to default the demo topic and the shared snapshot. */
export function mainSubjectFor(l: MarketplaceLearner, tutor?: Tutor): string | undefined {
  const taught = (subjectId: string) => {
    if (!tutor) return true;
    const p = parseSubtopicId(`${subjectId}-ch01-st1`);
    return !p || tutor.subjects.some((s) => s.subjectSlug === p.slug && s.boards.includes(p.board) && s.grades.includes(p.grade));
  };
  const hours = new Map<string, number>();
  for (const g of l.openGaps) if (taught(g.subjectId)) hours.set(g.subjectId, (hours.get(g.subjectId) ?? 0) + g.hoursToClose);
  return [...hours.entries()].sort((a, b) => b[1] - a[1])[0]?.[0];
}

/** The gap snapshot a student shares with a tutor: one subject, open gaps biggest first, latest score. */
export function buildSnapshot(l: MarketplaceLearner, subjectId: string, scorePct?: number): GapSnapshot {
  const gaps = l.openGaps
    .filter((g) => g.subjectId === subjectId)
    .sort((a, b) => b.hoursToClose - a.hoursToClose)
    .slice(0, 6)
    .map((g) => ({ gapId: g.id, subtopicId: g.subtopicId, name: l.names[g.subtopicId] ?? g.subtopicId, code: g.code, level: g.level, hoursToClose: g.hoursToClose }));
  return { sharedUtc: DEMO_NOW.toISOString(), subjectId, score: scorePct, gaps };
}

/** Demo slots for a tutor and student: both calendars, minus both people's booked sessions. */
export async function slotsFor(tutor: Tutor, student: Student | undefined): Promise<{ days: DemoDay[]; bothCalendars: boolean }> {
  const busy: BusyInterval[] = [];
  const add = (xs: { startUtc: string; minutes: number; status: string }[]) => {
    for (const s of xs) if (s.status === 'scheduled') busy.push({ startUtc: s.startUtc, minutes: s.minutes });
  };
  add(await getSessions(tutor.id));
  if (student) add(await getSessions(student.id));
  const bothCalendars = !!student?.availability?.length;
  const days = demoSlots({
    now: DEMO_NOW, tutorAvailability: tutor.availability, studentWindows: student?.availability, busy,
    minutes: tutor.pricing.demoMinutes || 30, maxPerDay: tutor.maxSessionsPerDay,
  });
  return { days, bothCalendars };
}

export { getTutor, listTutors };
