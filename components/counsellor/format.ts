import { DEMO_TIMEZONE } from '@/lib/demo-clock';

const date = new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric', timeZone: DEMO_TIMEZONE });
const dateShort = new Intl.DateTimeFormat('en-IN', { weekday: 'short', day: 'numeric', month: 'short', timeZone: DEMO_TIMEZONE });
const time = new Intl.DateTimeFormat('en-IN', { hour: 'numeric', minute: '2-digit', hour12: true, timeZone: DEMO_TIMEZONE });

export const formatDate = (iso: string) => date.format(new Date(iso.length === 10 ? iso + 'T12:00:00+05:30' : iso));
export const formatDay = (iso: string) => dateShort.format(new Date(iso.length === 10 ? iso + 'T12:00:00+05:30' : iso));
export const formatTime = (iso: string) => time.format(new Date(iso));

/** "09:30" → "9:30 am" */
export function formatHHMM(hhmm: string) {
  const [h, m] = hhmm.split(':').map(Number) as [number, number];
  return `${((h + 11) % 12) + 1}:${String(m).padStart(2, '0')} ${h < 12 ? 'am' : 'pm'}`;
}

export function relativeDays(iso: string, now: Date) {
  const d = Math.round((Date.parse(iso) - now.getTime()) / 86_400_000);
  if (d === 0) return 'today';
  if (d === 1) return 'tomorrow';
  if (d === -1) return 'yesterday';
  return d > 0 ? `in ${d} days` : `${-d} days ago`;
}
