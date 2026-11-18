import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { CheckCircle2, ChevronLeft, ChevronRight, Circle, PartyPopper, Sparkles } from 'lucide-react';
import { earningRows, loadWorkspace, money, reviewQueue, sessionsOn, studentRows, todayItems, type TodayItem } from '@/components/tutor/model';
import { formatDay, formatTime } from '@/components/marketplace/dates';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { addDaysLocal, demoToday, localDateOf } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import { cn } from '@/lib/utils';

export const metadata: Metadata = { title: 'Today · Tutor' };

const KIND: Record<TodayItem['kind'], string> = { prep: 'Prepare', session: 'Session', report: 'Report', review: 'Review', request: 'Request', nudge: 'Nudge' };

function Row({ it, now }: { it: TodayItem; now?: boolean }) {
  return (
    <li className={cn('flex items-start gap-3 px-4 py-3', now && 'bg-brand-50/60')}>
      <span className="w-16 shrink-0 pt-0.5 text-xs font-medium text-muted">{now ? 'now' : it.at ? formatTime(it.at) : ''}</span>
      {it.done ? <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-success-600" /> : <Circle className="mt-0.5 size-4 shrink-0 text-subtle" />}
      <div className="min-w-0 flex-1">
        <p className={cn('text-sm font-medium', it.done ? 'text-muted line-through' : 'text-ink')}>{it.kind === 'session' && <span className="text-muted">{KIND[it.kind]} · </span>}{it.title}</p>
        <p className="truncate text-xs text-muted">{it.detail}</p>
      </div>
      {!it.done && <Link href={it.href} className={buttonVariants({ size: 'sm', variant: now ? 'primary' : 'secondary' })}>{it.cta}</Link>}
    </li>
  );
}

/** Tutor HTML 6a/6b: one time-ordered checklist for the day (prep, session, report), then untimed to-dos; an end state when all is done. */
export default async function TodayPage({ searchParams }: { searchParams: Promise<{ day?: string }> }) {
  const sp = await searchParams;
  const persona = (await currentPersona())!;
  const ws = loadWorkspace(persona.id);
  if (!ws) notFound();
  const today = demoToday();
  const day = sp.day && /^\d{4}-\d{2}-\d{2}$/.test(sp.day) ? sp.day : today;
  const items = todayItems(ws, day);
  const timed = items.filter((x) => x.at);
  const untimed = items.filter((x) => !x.at);
  const done = items.filter((x) => x.done).length;
  const nowItem = day === today ? items.find((x) => !x.done) : undefined;
  const sessions = sessionsOn(ws, day).filter((s) => s.status !== 'cancelled');
  const attention = studentRows(ws).filter((r) => r.issue).length;
  const reviews = day === today ? reviewQueue(ws).length : 0;
  const allDone = items.length > 0 && done === items.length;
  const earned = earningRows(ws).filter((r) => localDateOf(r.session.startUtc) === day).reduce((a, r) => a + r.netInr, 0);
  const reports = sessions.filter((s) => s.report).length;
  const nav = (d: string, label: string, Icon: typeof ChevronLeft) => <Link href={d === today ? '/tutor/today' : `/tutor/today?day=${d}`} className={buttonVariants({ variant: 'ghost', size: 'sm' })} aria-label={label}><Icon /></Link>;

  return (
    <div className="mx-auto max-w-3xl space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="flex items-center gap-1 text-2xl font-semibold text-ink">{nav(addDaysLocal(day, -1), 'Previous day', ChevronLeft)}{day === today ? 'Today' : day < today ? 'Past day' : 'Upcoming day'} · {formatDay(day)}{nav(addDaysLocal(day, 1), 'Next day', ChevronRight)}</h1>
          <p className="mt-1 text-sm text-muted">{sessions.length} {sessions.length === 1 ? 'session' : 'sessions'}{day === today ? ` · ${reviews} ${reviews === 1 ? 'review' : 'reviews'} · ${attention} ${attention === 1 ? 'student needs' : 'students need'} attention · ${untimed.filter((x) => !x.done).length} to-dos` : ''}</p>
        </div>
        {items.length > 0 && <div className="w-48"><p className="mb-1 text-right text-sm text-muted">{done} / {items.length} done</p><Progress value={(done / items.length) * 100} /></div>}
      </div>

      {allDone ? (
        <Card><CardBody className="flex flex-col items-center py-10 text-center">
          <div className="mb-3 flex size-12 items-center justify-center rounded-full bg-success-50 text-success-600"><PartyPopper className="size-6" /></div>
          <h2 className="text-lg font-semibold text-ink">That&apos;s everything for {day === today ? 'today' : 'this day'}</h2>
          <p className="mt-1 max-w-md text-sm text-muted">{sessions.length} {sessions.length === 1 ? 'session' : 'sessions'} taught · {reports} {reports === 1 ? 'report' : 'reports'} filed · {money(earned)} earned. Homework and next focus are already on your students&apos; timetables.</p>
          <div className="mt-4 flex gap-2">
            <Link href={`/tutor/today?day=${addDaysLocal(day, 1)}`} className={buttonVariants({ variant: 'secondary' })}>See {day === today ? 'tomorrow' : 'next day'}</Link>
            <Link href="/tutor/earnings" className={buttonVariants()}>Open Earnings</Link>
          </div>
        </CardBody></Card>
      ) : items.length === 0 ? (
        <Card><CardBody className="py-10 text-center"><p className="font-medium text-ink">Nothing scheduled</p><p className="mt-1 text-sm text-muted">No sessions or to-dos on this day.</p><Link href="/tutor/sessions?view=calendar" className={cn(buttonVariants({ variant: 'secondary' }), 'mt-4')}>Open calendar</Link></CardBody></Card>
      ) : (
        <>
          {nowItem && (
            <Card className="border-brand-200"><CardBody className="flex items-start gap-3">
              <Sparkles className="mt-0.5 size-5 shrink-0 text-brand-600" />
              <div className="min-w-0 flex-1"><p className="text-xs font-medium uppercase tracking-wide text-brand-700">Do this next</p><p className="font-medium text-ink">{nowItem.title}</p><p className="text-sm text-muted">{nowItem.detail}</p></div>
              <Link href={nowItem.href} className={buttonVariants()}>{nowItem.cta}</Link>
            </CardBody></Card>
          )}
          {timed.length > 0 && <Card><ul className="divide-y divide-line">{timed.map((it) => <Row key={it.id} it={it} />)}</ul></Card>}
          {untimed.length > 0 && (
            <section>
              <h2 className="mb-2 text-sm font-semibold text-ink">Anytime today</h2>
              <Card><ul className="divide-y divide-line">{untimed.map((it) => <Row key={it.id} it={it} />)}</ul></Card>
            </section>
          )}
        </>
      )}
    </div>
  );
}
