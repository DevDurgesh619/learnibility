import type { AvailabilitySlot, Weekday } from '@/lib/types/catalogue';

/** One bookable demo slot. Times are local (IST by default); startUtc is the instant. */
export interface DemoSlot { startUtc: string; start: string; end: string }
export interface DemoDay { date: string; day: Weekday; slots: DemoSlot[]; full?: boolean }
export interface BusyInterval { startUtc: string; minutes: number }

const DAYS: Weekday[] = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
const toMin = (t: string) => Number(t.slice(0, 2)) * 60 + Number(t.slice(3, 5));
const hhmm = (m: number) => `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;

/** Local date (YYYY-MM-DD) and minutes-of-day for an instant at a fixed offset. */
export function localParts(iso: string | Date, tzOffsetMin = 330): { date: string; minutes: number; day: Weekday } {
  const d = new Date((typeof iso === 'string' ? Date.parse(iso) : iso.getTime()) + tzOffsetMin * 60_000);
  return { date: d.toISOString().slice(0, 10), minutes: d.getUTCHours() * 60 + d.getUTCMinutes(), day: DAYS[d.getUTCDay()]! };
}

export function localToUtc(date: string, time: string, tzOffsetMin = 330): string {
  const [y, m, d] = date.split('-').map(Number);
  return new Date(Date.UTC(y!, m! - 1, d!, 0, toMin(time) - tzOffsetMin)).toISOString();
}

function addDays(date: string, n: number): string {
  const d = new Date(`${date}T00:00:00Z`);
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}

function intersect(a: [number, number][], b: [number, number][]): [number, number][] {
  const out: [number, number][] = [];
  for (const x of a) for (const y of b) {
    const s = Math.max(x[0], y[0]), e = Math.min(x[1], y[1]);
    if (e > s) out.push([s, e]);
  }
  return out;
}

/**
 * Demo slots for the next `days` days (starting tomorrow): the tutor's weekly hours, intersected with the
 * student's study windows when known ("only times you're both free", PDF 5e), minus anything either of them
 * already has booked, on a 30-minute grid, capped by the tutor's max sessions a day.
 */
export function demoSlots(opts: {
  now: Date;
  tutorAvailability: AvailabilitySlot[];
  studentWindows?: { day: Weekday; start: string; end: string }[];
  busy?: BusyInterval[];
  minutes: number;
  maxPerDay?: number;
  days?: number;
  tzOffsetMin?: number;
}): DemoDay[] {
  const tz = opts.tzOffsetMin ?? 330;
  const today = localParts(opts.now, tz).date;
  const out: DemoDay[] = [];
  for (let i = 1; i <= (opts.days ?? 7); i++) {
    const date = addDays(today, i);
    const day = localParts(localToUtc(date, '12:00', tz), tz).day;
    let free: [number, number][] = opts.tutorAvailability.filter((s) => s.day === day).map((s) => [toMin(s.start), toMin(s.end)]);
    if (opts.studentWindows?.length) free = intersect(free, opts.studentWindows.filter((s) => s.day === day).map((s) => [toMin(s.start), toMin(s.end)]));
    const busyToday = (opts.busy ?? []).map((b) => ({ ...localParts(b.startUtc, tz), len: b.minutes })).filter((b) => b.date === date);
    const slots: DemoSlot[] = [];
    for (const [s, e] of free) {
      for (let t = Math.ceil(s / 30) * 30; t + opts.minutes <= e; t += 30) {
        const clash = busyToday.some((b) => t < b.minutes + b.len && b.minutes < t + opts.minutes);
        if (!clash) slots.push({ startUtc: localToUtc(date, hhmm(t), tz), start: hhmm(t), end: hhmm(t + opts.minutes) });
      }
    }
    // one demo per tutor-hour keeps the grid readable: keep slots on the hour where possible
    const onHour = slots.filter((s) => s.start.endsWith(':00'));
    const pick = (onHour.length ? onHour : slots).sort((a, b) => a.start.localeCompare(b.start));
    const full = opts.maxPerDay !== undefined && busyToday.length >= opts.maxPerDay;
    out.push({ date, day, slots: full ? [] : pick, full: full || undefined });
  }
  return out;
}
