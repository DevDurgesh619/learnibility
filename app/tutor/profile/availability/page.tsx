import type { Metadata } from 'next';
import Link from 'next/link';
import { AlertTriangle } from 'lucide-react';
import { DAY_LABEL, WEEKDAYS } from '@/components/marketplace/labels';
import { getTutor } from '@/components/marketplace/queries';
import { formatDate, formatDateTime } from '@/components/marketplace/dates';
import { localParts } from '@/components/marketplace/slots';
import { BANDS, Saved } from '@/components/tutor/form-bits';
import { readPrefs, withPrefs } from '@/components/tutor/prefs';
import { SectionTitle } from '@/components/tutor/bits';
import { isUpcoming, loadWorkspace, sessionWho } from '@/components/tutor/model';
import { Button } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { saveTutorPrefs } from '@/lib/actions/tutor';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Availability · Tutor' };

const toMin = (hhmm: string) => Number(hhmm.slice(0, 2)) * 60 + Number(hhmm.slice(3, 5));

/** Tutor HTML 8c: weekly hours grid, blocked dates, and a notice for booked sessions outside new hours. */
export default async function AvailabilityPage({ searchParams }: { searchParams: Promise<{ saved?: string }> }) {
  const sp = await searchParams;
  const persona = (await currentPersona())!;
  const prefs = await readPrefs(persona.id);
  const t = withPrefs(getTutor(persona.id)!, prefs);
  const ws = loadWorkspace(persona.id)!;
  const covers = (d: string, b: (typeof BANDS)[number]) => t.availability.some((a) => a.day === d && toMin(a.start) <= toMin(b.start) && toMin(a.end) >= toMin(b.end));
  const outside = ws.sessions.filter((s) => isUpcoming(s)).filter((s) => {
    const lp = localParts(s.startUtc);
    return !t.availability.some((a) => a.day === lp.day && toMin(a.start) <= lp.minutes && toMin(a.end) >= lp.minutes + s.minutes);
  });
  const blocked = prefs.blocked ?? [];
  const days = WEEKDAYS;
  return (
    <form action={saveTutorPrefs}>
      <input type="hidden" name="back" value="/tutor/profile/availability" />
      <input type="hidden" name="section" value="availability" />
      <Saved show={sp.saved}>Availability saved.</Saved>
      {outside.length > 0 && (
        <div className="mb-4 flex items-start gap-3 rounded-lg border border-warning-600/20 bg-warning-50 p-4 text-sm text-warning-700">
          <AlertTriangle className="mt-0.5 size-4 shrink-0" />
          <div><p>Changing hours doesn&apos;t move booked sessions. {outside.length} upcoming {outside.length === 1 ? 'session falls' : 'sessions fall'} outside your hours:</p>
            <ul className="mt-1">{outside.slice(0, 4).map((s) => <li key={s.id}><Link href={`/tutor/sessions/${s.id}/reschedule`} className="underline">{sessionWho(ws, s)} · {formatDateTime(s.startUtc)}</Link></li>)}</ul></div>
        </div>
      )}
      <Card><CardBody className="space-y-6">
        <section>
          <SectionTitle>Weekly hours <span className="text-sm font-normal text-muted">· IST · {t.sessionMinutes}-min slots</span></SectionTitle>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[520px] text-sm">
              <thead><tr><th className="w-20" />{days.map((d) => <th key={d} className="pb-2 text-center font-medium text-muted">{DAY_LABEL[d]}</th>)}</tr></thead>
              <tbody>
                {BANDS.map((b) => (
                  <tr key={b.key}>
                    <th className="py-1 pr-2 text-left font-normal text-muted">{b.label}</th>
                    {days.map((d) => (
                      <td key={d} className="p-1 text-center">
                        <label className="relative block cursor-pointer">
                          <input type="checkbox" name="cell" value={`${d}:${b.key}`} defaultChecked={covers(d, b)} className="peer sr-only" aria-label={`${DAY_LABEL[d]} ${b.label}`} />
                          <span className="flex h-9 items-center justify-center rounded-md border border-line bg-surface text-transparent peer-checked:border-brand-400 peer-checked:bg-brand-50 peer-checked:text-brand-700 peer-focus-visible:ring-2 peer-focus-visible:ring-brand-400">✓</span>
                        </label>
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <label className="mt-3 flex items-center gap-2 text-sm text-muted">Max sessions a day <input type="number" name="maxSessionsPerDay" min={1} max={10} defaultValue={t.maxSessionsPerDay} className="h-9 w-20 rounded-lg border border-line bg-surface px-2 text-ink" /></label>
        </section>
        <section>
          <SectionTitle>Blocked dates</SectionTitle>
          {blocked.length ? (
            <ul className="mb-3 space-y-1 text-sm">{blocked.map((b) => <li key={b.from} className="flex items-center gap-3"><span className="text-ink">{formatDate(b.from)}{b.to !== b.from ? ` – ${formatDate(b.to)}` : ''} · {b.label}</span><label className="flex items-center gap-1 text-xs text-muted"><input type="checkbox" name="unblock" value={b.from} />remove</label></li>)}</ul>
          ) : <p className="mb-3 text-sm text-muted">No blocked dates. Add holidays or exam weeks so students can&apos;t book them.</p>}
          <div className="flex flex-wrap items-end gap-2 text-sm">
            <label className="text-muted">From<input type="date" name="blockFrom" className="mt-1 block h-9 rounded-lg border border-line bg-surface px-2 text-ink" /></label>
            <label className="text-muted">To<input type="date" name="blockTo" className="mt-1 block h-9 rounded-lg border border-line bg-surface px-2 text-ink" /></label>
            <label className="text-muted">Reason<input name="blockLabel" placeholder="Diwali travel" className="mt-1 block h-9 rounded-lg border border-line bg-surface px-2 text-ink" /></label>
          </div>
        </section>
        <div className="flex justify-end"><Button type="submit">Save</Button></div>
      </CardBody></Card>
    </form>
  );
}
