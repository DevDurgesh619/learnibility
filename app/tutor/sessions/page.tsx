import type { Metadata } from 'next';
import Link from 'next/link';
import { CalendarDays, List, Search } from 'lucide-react';
import { RequestRow } from '@/components/tutor/home/parts';
import { SectionKindRow } from '@/components/tutor/session-row';
import { SectionTitle } from '@/components/tutor/bits';
import { earningRows, isUpcoming, loadWorkspace, money, reportMissing, requests, sessionWho } from '@/components/tutor/model';
import { DAY_LABEL, WEEKDAYS } from '@/components/marketplace/labels';
import { localParts } from '@/components/marketplace/slots';
import { formatDay, formatTime } from '@/components/marketplace/dates';
import { Card } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import { addDaysLocal, demoToday, localDateOf, weekStartOf } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import { cn } from '@/lib/utils';

export const metadata: Metadata = { title: 'Sessions · Tutor' };

type SP = { view?: string; tab?: string; week?: string; q?: string; f?: string; student?: string };

export default async function SessionsPage({ searchParams }: { searchParams: Promise<SP> }) {
  const sp = await searchParams;
  const ws = loadWorkspace((await currentPersona())!.id);
  if (!ws) return <EmptyState title="No sessions yet" />;
  const view = sp.view === 'calendar' ? 'calendar' : 'list';
  const tab = sp.tab === 'requests' || sp.tab === 'past' ? sp.tab : 'upcoming';
  const live = ws.sessions.filter((s) => s.status !== 'cancelled');
  const upcoming = live.filter((s) => isUpcoming(s) && !(s.bookingId && ws.bookings.find((b) => b.id === s.bookingId)?.status === 'requested'));
  const past = live.filter((s) => !isUpcoming(s)).reverse();
  const reqs = requests(ws);
  const missing = past.filter((s) => reportMissing(s) && s.kind !== 'demo');

  return (
    <>
      <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
        <h1 className="text-2xl font-semibold tracking-tight text-ink">Sessions</h1>
        <div className="inline-flex rounded-lg border border-line bg-surface p-0.5">
          <Link href="/tutor/sessions" className={cn('inline-flex items-center gap-1 rounded-md px-3 py-1 text-sm', view === 'list' ? 'bg-brand-600 text-white' : 'text-muted')}><List className="size-4" />List</Link>
          <Link href="/tutor/sessions?view=calendar" className={cn('inline-flex items-center gap-1 rounded-md px-3 py-1 text-sm', view === 'calendar' ? 'bg-brand-600 text-white' : 'text-muted')}><CalendarDays className="size-4" />Calendar</Link>
        </div>
      </div>
      {view === 'calendar' ? <Calendar ws={ws} sp={sp} /> : (
        <>
          <div className="mb-4 flex gap-1 border-b border-line">
            {([['upcoming', `Upcoming · ${upcoming.length}`], ['requests', `Requests · ${reqs.length}`], ['past', 'Past']] as const).map(([k, l]) => (
              <Link key={k} href={`/tutor/sessions?tab=${k}`} className={cn('-mb-px border-b-2 px-3 py-2 text-sm font-medium', tab === k ? 'border-brand-600 text-brand-700' : 'border-transparent text-muted hover:text-ink')}>{l}</Link>
            ))}
          </div>
          {tab === 'upcoming' && (upcoming.length === 0 ? <EmptyState title="No upcoming sessions" description="Accepted demos and recurring sessions show here." /> : (
            <div className="space-y-6">
              {[...new Set(upcoming.map((s) => localDateOf(s.startUtc)))].slice(0, 7).map((d) => (
                <section key={d}>
                  <SectionTitle>{d === demoToday() ? 'Today' : formatDay(d)}</SectionTitle>
                  <Card><ul className="divide-y divide-line">{upcoming.filter((s) => localDateOf(s.startUtc) === d).map((s) => <SectionKindRow key={s.id} ws={ws} s={s} showWho />)}</ul></Card>
                </section>
              ))}
              <p className="text-xs text-muted">Join opens 10 minutes before the start. Use ⋯ Reschedule on a session to move or cancel it.</p>
            </div>
          ))}
          {tab === 'requests' && (reqs.length === 0 ? <EmptyState title="No open requests" /> : <Card className="px-4"><ul className="divide-y divide-line">{reqs.map((b) => <RequestRow key={b.id} ws={ws} b={b} />)}</ul></Card>)}
          {tab === 'past' && <Past ws={ws} past={past} missing={missing} sp={sp} />}
        </>
      )}
    </>
  );
}

function Past({ ws, past, missing, sp }: { ws: NonNullable<ReturnType<typeof loadWorkspace>>; past: ReturnType<typeof loadWorkspace> extends infer W ? W extends { sessions: infer S } ? S : never : never; missing: typeof past; sp: SP }) {
  const q = sp.q?.toLowerCase();
  const month = demoToday().slice(0, 7);
  let list = sp.f === 'missing' ? missing : sp.f === 'month' ? past.filter((s) => s.startUtc.startsWith(month)) : past;
  if (q) list = list.filter((s) => `${sessionWho(ws, s)} ${s.title} ${s.report?.topics.join(' ') ?? ''}`.toLowerCase().includes(q));
  return (
    <div className="space-y-4">
      <form className="flex flex-col gap-2 sm:flex-row" action="/tutor/sessions">
        <input type="hidden" name="tab" value="past" />
        <label className="relative flex-1"><Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-subtle" /><input name="q" defaultValue={sp.q} placeholder="Student, topic…" className="h-10 w-full rounded-lg border border-line pl-9 pr-3 text-sm" /></label>
        <div className="flex gap-2">
          {([['', 'All'], ['missing', `Report missing · ${missing.length}`], ['month', 'This month']] as const).map(([k, l]) => (
            <Link key={k} href={`/tutor/sessions?tab=past${k ? `&f=${k}` : ''}`} className={cn('rounded-full border px-3 py-2 text-sm', (sp.f ?? '') === k ? 'border-brand-600 bg-brand-600 text-white' : 'border-line bg-surface')}>{l}</Link>
          ))}
        </div>
      </form>
      {missing.length > 0 && sp.f !== 'missing' && <p className="rounded-lg border border-warning-600/30 bg-warning-50 px-3 py-2 text-sm text-warning-700">{missing.length} {missing.length === 1 ? 'report is' : 'reports are'} missing. Earnings for {missing.length === 1 ? 'it are' : 'them are'} held, and students don&apos;t get their next steps until you file.</p>}
      {list.length === 0 ? <EmptyState title="Nothing here" /> : <Card><ul className="divide-y divide-line">{list.slice(0, 30).map((s) => <SectionKindRow key={s.id} ws={ws} s={s} showWho />)}</ul></Card>}
    </div>
  );
}

function Calendar({ ws, sp }: { ws: NonNullable<ReturnType<typeof loadWorkspace>>; sp: SP }) {
  const ws0 = sp.week && /^\d{4}-\d{2}-\d{2}$/.test(sp.week) ? weekStartOf(sp.week) : weekStartOf(demoToday());
  const days = WEEKDAYS.slice(0, 6).map((d, i) => ({ d, date: addDaysLocal(ws0, i) }));
  const bands = [['07:00', '10:00'], ['10:00', '13:00'], ['16:00', '19:00'], ['19:00', '22:00']] as const;
  const inWeek = ws.sessions.filter((s) => s.status !== 'cancelled' && localDateOf(s.startUtc) >= ws0 && localDateOf(s.startUtc) < addDaysLocal(ws0, 7));
  const rows = earningRows(ws);
  const value = inWeek.reduce((t, s) => t + (rows.find((r) => r.session.id === s.id)?.netInr ?? Math.round(((s.rateInr ?? 0) * s.minutes) / 60 * (s.kind === 'group' ? s.learnerIds.length : 1) * (1 - (ws.tutor.platformFeeRate ?? 0.15)))), 0);
  const toMin = (t: string) => Number(t.slice(0, 2)) * 60 + Number(t.slice(3, 5));
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <Link href={`/tutor/sessions?view=calendar&week=${addDaysLocal(ws0, -7)}`} className="rounded-lg border border-line px-3 py-1 text-sm">‹</Link>
        <p className="text-sm font-medium text-ink">{formatDay(ws0)} – {formatDay(addDaysLocal(ws0, 5))}</p>
        <Link href={`/tutor/sessions?view=calendar&week=${addDaysLocal(ws0, 7)}`} className="rounded-lg border border-line px-3 py-1 text-sm">›</Link>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[720px] table-fixed border-separate border-spacing-1 text-xs">
          <thead><tr><th className="w-16" />{days.map(({ d, date }) => <th key={d} className={cn('rounded-md py-1 font-medium', date === demoToday() ? 'bg-brand-50 text-brand-700' : 'text-muted')}>{DAY_LABEL[d]} {Number(date.slice(8))}</th>)}</tr></thead>
          <tbody>
            {bands.map(([a, b]) => (
              <tr key={a}>
                <td className="align-top text-muted">{Number(a.slice(0, 2)) % 12 || 12}–{Number(b.slice(0, 2)) % 12 || 12}</td>
                {days.map(({ d, date }) => {
                  const avail = ws.tutor.availability.some((x) => x.day === d && toMin(x.start) < toMin(b) && toMin(x.end) > toMin(a));
                  const here = inWeek.filter((s) => { const p = localParts(s.startUtc); return p.date === date && p.minutes >= toMin(a) && p.minutes < toMin(b); });
                  return (
                    <td key={d} className={cn('h-20 rounded-md p-1 align-top', avail ? 'border border-dashed border-line bg-surface' : 'bg-surface-muted')}>
                      {here.map((s) => (
                        <Link key={s.id} href={isUpcoming(s) ? `/tutor/sessions/${s.id}/prep` : `/tutor/sessions/${s.id}`} className={cn('mb-1 block truncate rounded px-1.5 py-1', s.kind === 'demo' ? 'bg-info-50 text-info-600' : s.kind === 'group' ? 'bg-brand-100 text-brand-800' : 'bg-brand-600 text-white')}>
                          {formatTime(s.startUtc)} {sessionWho(ws, s)}{s.kind === 'demo' ? ' demo' : ''}
                        </Link>
                      ))}
                      {avail && here.length === 0 && <span className="text-subtle">open</span>}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="text-xs text-muted">Solid = booked · dashed = open hours students can book · grey = outside your availability (change it in Profile). {inWeek.length} sessions this week · {inWeek.reduce((t, s) => t + s.minutes, 0) / 60} h · ~{money(value)} after fees.</p>
    </div>
  );
}
