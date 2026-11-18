import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { CheckCircle2, Clock, Video } from 'lucide-react';
import { SessionHeader } from '@/components/tutor/session-header';
import { SectionTitle, Pill } from '@/components/tutor/bits';
import { aiFocus, isUpcoming, money, nameOf, reportMissing, sessionContext } from '@/components/tutor/model';
import { formatDay } from '@/components/marketplace/dates';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { demoNow } from '@/lib/data';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Session · Tutor' };

const PERF = { struggled: 'Struggled', getting_there: 'Getting there', confident: 'Confident' } as const;

/** Tutor HTML 5f: one session. Upcoming shows the focus and actions; past shows the filed report. */
export default async function SessionPage({ params, searchParams }: { params: Promise<{ sessionId: string }>; searchParams: Promise<{ filed?: string }> }) {
  const [{ sessionId }, sp] = await Promise.all([params, searchParams]);
  const persona = (await currentPersona())!;
  const ctx = sessionContext(persona.id, sessionId);
  if (!ctx) notFound();
  const { ws, s, learners, ownHomework, earning, next } = ctx;
  const up = isUpcoming(s);
  const missing = reportMissing(s);
  const joinable = up && Date.parse(s.startUtc) - Date.parse(demoNow()) <= 10 * 60_000;
  const r = s.report;

  return (
    <div className="mx-auto max-w-3xl">
      <SessionHeader ws={ws} s={s} title={r ? 'Summary' : up ? 'Upcoming session' : 'Session'} actions={
        <>
          {up && <Link href={`/tutor/sessions/${s.id}/prep`} className={buttonVariants({ variant: 'secondary' })}>{s.prepNotes ? 'Prep ✓' : 'Prepare'}</Link>}
          {up && <Link href={`/tutor/sessions/${s.id}/reschedule`} className={buttonVariants({ variant: 'secondary' })}>Reschedule</Link>}
          {up && <Link href={`/tutor/sessions/${s.id}/live`} aria-disabled={!joinable} className={buttonVariants({ className: joinable ? '' : 'pointer-events-none opacity-50' })}><Video />Join</Link>}
          {missing && <Link href={`/tutor/sessions/${s.id}/report`} className={buttonVariants()}>Write report</Link>}
          {r && <Link href={`/tutor/sessions/${s.id}/report`} className={buttonVariants({ variant: 'secondary' })}>Edit report</Link>}
        </>
      } />

      {sp.filed && r && (
        <div className="mb-4 flex items-start gap-3 rounded-lg border border-success-600/20 bg-success-50 p-4 text-sm text-success-700">
          <CheckCircle2 className="mt-0.5 size-5 shrink-0" />
          <p>Report filed. {ownHomework.length ? `${ownHomework.length} homework ${ownHomework.length === 1 ? 'task is' : 'tasks are'} now on ${learners.map((l) => nameOf(ws, l).split(' ')[0]).join(', ')}'s Today and timetable.` : 'No homework was set.'}{r.nextFocus && next ? ` Next focus is set for ${formatDay(next.startUtc)}.` : ''}</p>
        </div>
      )}

      {up && (
        <Card><CardBody className="space-y-2">
          <p className="text-sm text-muted">AI focus for this session</p>
          <p className="text-lg font-medium text-ink">{aiFocus(ws, s).line}</p>
          <p className="text-xs text-subtle">{aiFocus(ws, s).source}. Join opens 10 minutes before the start.</p>
        </CardBody></Card>
      )}

      {s.status === 'no_show' && <Card><CardBody><p className="text-sm text-ink">{nameOf(ws, s.learnerId)} did not join this session. No earnings accrue for a no-show.</p></CardBody></Card>}
      {s.status === 'cancelled' && <Card><CardBody><p className="text-sm text-ink">This session was cancelled.</p></CardBody></Card>}

      {missing && (
        <Card><CardBody className="flex items-start gap-3">
          <Clock className="mt-0.5 size-5 shrink-0 text-warning-600" />
          <div className="text-sm"><p className="font-medium text-ink">Report missing</p><p className="text-muted">The session is over. Filing the report releases {earning ? money(earning.netInr) : 'the earnings'} and puts homework on {nameOf(ws, s.learnerId).split(' ')[0]}'s timetable. It takes about 2 minutes.</p></div>
        </CardBody></Card>
      )}

      {r && (
        <Card><CardBody className="space-y-5">
          <div className="flex flex-wrap gap-2 text-sm">
            <Pill tone="success">Attended</Pill>
            <Pill>{s.minutes} min</Pill>
            {earning && <Pill tone={earning.status === 'paid' ? 'success' : 'neutral'}>{earning.status === 'free' ? 'Free demo' : `${money(earning.netInr)} · ${earning.status === 'paid' ? `paid ${earning.paidOn ? formatDay(earning.paidOn) : ''}` : 'pending payout'}`}</Pill>}
          </div>
          <section><SectionTitle>Covered</SectionTitle><p className="text-sm text-ink">{r.topics.join(', ') || '—'}</p></section>
          <section><SectionTitle>Performance</SectionTitle><p className="text-sm text-ink">{PERF[r.performance]} · engagement {r.engagement}</p><p className="mt-1 text-xs text-subtle">Only you see the rating and notes. Students see topics, homework and next focus.</p></section>
          <section>
            <SectionTitle>Homework</SectionTitle>
            {ownHomework.length ? (
              <ul className="divide-y divide-line rounded-lg border border-line">
                {ownHomework.map((t) => (
                  <li key={t.id} className="flex items-center justify-between gap-3 px-3 py-2 text-sm">
                    <span className="min-w-0 truncate text-ink">{t.title}{learners.length > 1 ? ` · ${nameOf(ws, t.learnerId).split(' ')[0]}` : ''}</span>
                    <span className="shrink-0 text-xs text-muted">due {formatDay(t.dueDate)} · {t.status === 'done' ? 'done' : t.status === 'skipped' ? 'skipped' : 'open'}</span>
                  </li>
                ))}
              </ul>
            ) : <p className="text-sm text-muted">No homework set in this session.</p>}
          </section>
          {r.notes && <section><SectionTitle>Your note</SectionTitle><p className="rounded-lg bg-surface-muted p-3 text-sm text-ink">{r.notes}</p></section>}
          {r.nextFocus && <section><SectionTitle>Next focus</SectionTitle><p className="text-sm text-ink">{r.nextFocus}{next ? <span className="text-muted"> · used in {next.code ?? 'the next session'} prep ({formatDay(next.startUtc)}) ✓</span> : ''}</p></section>}
          <div className="flex flex-wrap gap-2 border-t border-line pt-4">
            <Link href={`/tutor/students/${s.learnerId}`} className={buttonVariants({ variant: 'secondary', size: 'sm' })}>Open student</Link>
            <Link href={`/tutor/students/${s.learnerId}/tasks`} className={buttonVariants({ variant: 'secondary', size: 'sm' })}>Student tasks</Link>
          </div>
        </CardBody></Card>
      )}
    </div>
  );
}
