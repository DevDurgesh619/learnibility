import { DEMO_TIMEZONE } from '@/lib/demo-clock';

const dt = new Intl.DateTimeFormat('en-IN', { weekday: 'short', day: 'numeric', month: 'short', hour: 'numeric', minute: '2-digit', timeZone: DEMO_TIMEZONE });
const d = new Intl.DateTimeFormat('en-IN', { weekday: 'short', day: 'numeric', month: 'short', timeZone: DEMO_TIMEZONE });
const dLong = new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric', timeZone: DEMO_TIMEZONE });
const t = new Intl.DateTimeFormat('en-IN', { hour: 'numeric', minute: '2-digit', timeZone: DEMO_TIMEZONE });

/** "Thu, 19 Nov, 5:00 pm" */
export const formatDateTime = (iso: string) => dt.format(new Date(iso));
/** "Thu, 19 Nov" */
export const formatDay = (iso: string) => d.format(new Date(iso.length === 10 ? `${iso}T12:00:00+05:30` : iso));
/** "19 Nov 2026" */
export const formatDate = (iso: string) => dLong.format(new Date(iso.length === 10 ? `${iso}T12:00:00+05:30` : iso));
/** "5:00 pm" */
export const formatTime = (iso: string) => t.format(new Date(iso));
/** "5:00–5:30 pm" */
export function formatRange(iso: string, minutes: number) {
  const end = new Date(Date.parse(iso) + minutes * 60_000).toISOString();
  return `${formatTime(iso)}–${formatTime(end)}`;
}

/** "in 2 h 10 m", "in 3 days", "2 days ago". */
export function relative(iso: string, now: Date): string {
  const diff = Date.parse(iso) - now.getTime();
  const abs = Math.abs(diff);
  const mins = Math.round(abs / 60_000);
  let s: string;
  if (mins < 60) s = `${mins} m`;
  else if (mins < 24 * 60) s = `${Math.floor(mins / 60)} h${mins % 60 ? ` ${mins % 60} m` : ''}`;
  else { const days = Math.round(mins / 1440); s = `${days} ${days === 1 ? 'day' : 'days'}`; }
  return diff >= 0 ? `in ${s}` : `${s} ago`;
}
