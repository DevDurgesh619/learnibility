import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { CalendarClock, Lock, Sparkles } from 'lucide-react';
import { BackLink } from '@/components/tutor/bits';
import { loadWorkspace, nameOf } from '@/components/tutor/model';
import { BookingStatusBadge } from '@/components/marketplace/booking-status';
import { formatDateTime } from '@/components/marketplace/dates';
import { BOARD_LABEL } from '@/components/marketplace/labels';
import { Avatar } from '@/components/ui/avatar';
import { GapBadge, LEVEL_LABEL } from '@/components/ui/badge';
import { Button, buttonVariants } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { acceptBooking, declineBooking } from '@/lib/actions/booking';
import { getSubject } from '@/lib/data';
import { formatHours } from '@/lib/format';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Student request · Tutor' };

/** Tutor HTML 2c: a demo request with the student's shared gap snapshot. */
export default async function RequestPage({ params }: { params: Promise<{ bookingId: string }> }) {
  const { bookingId } = await params;
  const persona = (await currentPersona())!;
  const ws = loadWorkspace(persona.id);
  const b = ws?.bookings.find((x) => x.id === bookingId);
  if (!ws || !b) notFound();
  const st = ws.students.find((s) => s.learnerId === b.learnerId);
  const name = nameOf(ws, b.learnerId);
  const first = name.split(' ')[0];
  const snap = b.sharedGapSnapshot;
  const subject = (snap?.subjectId ?? b.subjectId) ? getSubject(snap?.subjectId ?? b.subjectId!)?.subject.name : undefined;

  return (
    <div className="mx-auto max-w-3xl">
      <BackLink href="/tutor">Home</BackLink>
      <Card>
        <CardBody className="space-y-6">
          <div className="flex items-start gap-4">
            <Avatar name={name} size="lg" />
            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-2"><h1 className="text-xl font-semibold text-ink">{b.kind === 'demo' ? 'Demo request' : 'Request'} · {name}</h1><BookingStatusBadge status={b.status} /></div>
              <p className="text-sm text-muted">Class {st?.grade} · {st ? BOARD_LABEL[st.board] : ''}{subject ? ` · ${subject}` : ''}{st?.goal ? ` · ${st.goal}` : ''}</p>
            </div>
          </div>

          {b.topic && (
            <section>
              <h2 className="text-sm font-semibold text-ink">What {first} wants to cover</h2>
              <p className="mt-1 rounded-lg bg-surface-muted p-3 text-sm text-ink">“{b.topic}”</p>
            </section>
          )}

          <section>
            <h2 className="text-sm font-semibold text-ink">Gap snapshot {snap && <span className="font-normal text-muted">· shared by {first}</span>}</h2>
            {snap ? (
              <div className="mt-2 overflow-hidden rounded-lg border border-line">
                {snap.score !== undefined && <p className="border-b border-line bg-surface-muted px-3 py-2 text-sm text-ink">{subject}: latest score {snap.score}/100</p>}
                <ul className="divide-y divide-line">
                  {snap.gaps.map((g) => (
                    <li key={g.subtopicId} className="flex flex-wrap items-center gap-2 px-3 py-2 text-sm">
                      <span className="min-w-0 flex-1 font-medium text-ink">{g.name}</span>
                      <GapBadge code={g.code} />
                      <span className="text-xs text-muted">{LEVEL_LABEL[g.level]} · ~{formatHours(g.hoursToClose)} to close</span>
                    </li>
                  ))}
                  {snap.gaps.length === 0 && <li className="px-3 py-2 text-sm text-muted">No open gaps in this subject.</li>}
                </ul>
              </div>
            ) : (
              <p className="mt-2 flex items-center gap-1.5 rounded-lg border border-dashed border-line p-3 text-sm text-muted"><Lock className="size-4" /> {first} chose not to share test results. Ask in the demo.</p>
            )}
            {b.matchReason && <p className="mt-2 flex gap-1.5 text-xs text-muted"><Sparkles className="mt-0.5 size-3.5 shrink-0 text-brand-600" />Matched because: {b.matchReason}</p>}
          </section>

          <section className="grid gap-3 sm:grid-cols-2">
            <div className="rounded-lg border border-line p-3">
              <p className="text-xs font-medium uppercase tracking-wide text-muted">When</p>
              <p className="mt-1 flex items-center gap-1.5 text-sm text-ink"><CalendarClock className="size-4 text-brand-600" />{b.slotStartUtc ? formatDateTime(b.slotStartUtc) : 'To be agreed'} · {b.minutes} min · online</p>
            </div>
            <div className="rounded-lg border border-line p-3">
              <p className="text-xs font-medium uppercase tracking-wide text-muted">After the demo</p>
              <p className="mt-1 text-sm text-ink">{b.sessionsPerWeek ? `Wants ${b.sessionsPerWeek} sessions a week` : 'Decides after the demo'}{b.priceInr ? ` · ${b.priceInr}/hr` : ''}</p>
            </div>
          </section>

          {b.status === 'requested' ? (
            <div className="flex flex-col-reverse gap-2 border-t border-line pt-4 sm:flex-row sm:items-center">
              {(() => { const sid = ws.sessions.find((s) => s.bookingId === b.id)?.id; return sid ? <Link href={`/tutor/sessions/${sid}/reschedule`} className="text-sm text-brand-700 hover:underline sm:mr-auto">Suggest another time</Link> : <span className="sm:mr-auto" />; })()}
              <form action={declineBooking} className="flex gap-2">
                <input type="hidden" name="bookingId" value={b.id} />
                <input name="reason" placeholder="Reason (optional)" className="h-10 min-w-0 flex-1 rounded-lg border border-line px-3 text-sm sm:w-44" />
                <Button variant="secondary">Decline</Button>
              </form>
              <form action={acceptBooking}><input type="hidden" name="bookingId" value={b.id} /><Button className="w-full">Accept demo</Button></form>
            </div>
          ) : (
            <div className="flex gap-2 border-t border-line pt-4">
              <Link href={`/tutor/students/${b.learnerId}`} className={buttonVariants()}>Open student</Link>
              <Link href="/tutor/sessions" className={buttonVariants({ variant: 'secondary' })}>Sessions</Link>
            </div>
          )}
        </CardBody>
      </Card>
    </div>
  );
}
