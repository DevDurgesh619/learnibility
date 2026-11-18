/** Date helpers for parent and mentor screens. Everything shows in the family's time zone (IST). */
const TZ = 'Asia/Kolkata';

export function fmtDate(isoOrLocal: string, opts: Intl.DateTimeFormatOptions = { day: 'numeric', month: 'short' }): string {
  const d = isoOrLocal.length === 10 ? new Date(`${isoOrLocal}T12:00:00+05:30`) : new Date(isoOrLocal);
  return new Intl.DateTimeFormat('en-IN', { timeZone: TZ, ...opts }).format(d);
}

export const fmtDay = (s: string) => fmtDate(s, { weekday: 'short', day: 'numeric', month: 'short' });
export const fmtDateYear = (s: string) => fmtDate(s, { day: 'numeric', month: 'short', year: 'numeric' });
export const fmtTime = (iso: string) => fmtDate(iso, { hour: 'numeric', minute: '2-digit', hour12: true });
export const fmtDateTime = (iso: string) => `${fmtDay(iso)}, ${fmtTime(iso)}`;

/** Whole days from `from` to `to` (local dates or ISO). */
export function daysBetween(from: string, to: string): number {
  const a = Date.parse(from.length === 10 ? `${from}T00:00:00+05:30` : from);
  const b = Date.parse(to.length === 10 ? `${to}T00:00:00+05:30` : to);
  return Math.round((b - a) / 86_400_000);
}

export function plural(n: number, one: string, many = `${one}s`): string {
  return `${n} ${n === 1 ? one : many}`;
}

export const firstName = (name: string) => name.split(' ')[0] ?? name;
