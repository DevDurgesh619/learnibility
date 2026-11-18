import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { AlertTriangle } from 'lucide-react';
import { SessionHeader } from '@/components/tutor/session-header';
import { SectionTitle } from '@/components/tutor/bits';
import { firstName, isUpcoming, nameOf, sessionContext } from '@/components/tutor/model';
import { demoSlots, type BusyInterval } from '@/components/marketplace/slots';
import { formatDay, formatTime } from '@/components/marketplace/dates';
import { Button } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import { rescheduleSession } from '@/lib/actions/booking';
import { demoNow, getSessions, getStudent } from '@/lib/data';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Reschedule · Tutor' };

/** Tutor HTML 5g: move a session to a free slot in the tutor's hours (and the student's, when known), or cancel it. */
export default async function ReschedulePage({ params }: { params: Promise<{ sessionId: string }> }) {
  const { sessionId } = await params;
  const persona = (await currentPersona())!;
  const ctx = sessionContext(persona.id, sessionId);
  if (!ctx) notFound();
  const { ws, s, learners } = ctx;
  const who = learners.length > 1 ? 'the group' : firstName(nameOf(ws, s.learnerId));
  const busy: BusyInterval[] = [];
  for (const x of [...getSessions(persona.id), ...learners.flatMap((l) => getSessions(l))]) if (x.status === 'scheduled' && x.id !== s.id) busy.push({ startUtc: x.startUtc, minutes: x.minutes });
  const student = learners.length === 1 ? getStudent(s.learnerId) : undefined;
  const days = demoSlots({ now: new Date(demoNow()), tutorAvailability: ws.tutor.availability, studentWindows: student?.availability, busy, minutes: s.minutes, maxPerDay: ws.tutor.maxSessionsPerDay, days: 7 })
    .map((d) => ({ ...d, slots: d.slots.filter((x) => Number(x.start.slice(3)) === 0) })).filter((d) => d.slots.length);
  const hoursLeft = (Date.parse(s.startUtc) - Date.parse(demoNow())) / 3_600_000;

  if (!isUpcoming(s)) {
    return (
      <div className="mx-auto max-w-3xl">
        <SessionHeader ws={ws} s={s} title="Reschedule" back={`/tutor/sessions/${s.id}`} backLabel="Session" />
        <EmptyState title="This session can't be moved" description="Only upcoming sessions can be rescheduled or cancelled." />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl">
      <SessionHeader ws={ws} s={s} title="Reschedule" back={`/tutor/sessions/${s.id}`} backLabel="Session" />
      <form action={rescheduleSession}>
        <input type="hidden" name="sessionId" value={s.id} />
        <Card><CardBody className="space-y-5">
          <p className="text-sm text-muted">Pick a new slot from your availability{student?.availability?.length ? ` that also fits ${who}'s study windows` : ''}. {who === 'the group' ? 'Everyone in the group' : who} gets a message with the new time.</p>
          <section>
            <SectionTitle>Free slots · next 7 days</SectionTitle>
            {days.length ? (
              <div className="space-y-3">
                {days.map((d) => (
                  <div key={d.date}>
                    <p className="mb-1 text-sm font-medium text-ink">{formatDay(d.date)}</p>
                    <div className="flex flex-wrap gap-2">
                      {d.slots.map((x) => (
                        <label key={x.startUtc} className="cursor-pointer">
                          <input type="radio" name="slotStartUtc" value={x.startUtc} className="peer sr-only" required />
                          <span className="block rounded-lg border border-line px-3 py-1.5 text-sm text-ink peer-checked:border-brand-500 peer-checked:bg-brand-50 peer-checked:font-medium peer-checked:text-brand-700 peer-focus-visible:ring-2 peer-focus-visible:ring-brand-400">{formatTime(x.startUtc)}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : <EmptyState title="No free slots this week" description="Every hour in your availability is booked. Add hours in Profile, or cancel instead." />}
          </section>
          <section>
            <label htmlFor="message" className="mb-1 block text-sm font-semibold text-ink">Message to {who} (optional)</label>
            <textarea id="message" name="message" rows={2} placeholder="Sorry, something came up…" className="w-full rounded-lg border border-line bg-surface p-3 text-sm text-ink focus:border-brand-400 focus:outline-none" />
          </section>
          {hoursLeft < 12 && <p className="flex items-start gap-2 rounded-lg bg-warning-50 p-3 text-sm text-warning-700"><AlertTriangle className="mt-0.5 size-4 shrink-0" />This session starts in under 12 hours. Cancelling now counts against your reliability score.</p>}
          <div className="flex flex-col-reverse gap-2 sm:flex-row sm:justify-between">
            <Button type="submit" name="intent" value="cancel" variant="ghost" formNoValidate className="text-danger-700">Cancel session instead</Button>
            <Button type="submit" name="intent" value="move" disabled={!days.length}>Move session</Button>
          </div>
        </CardBody></Card>
      </form>
    </div>
  );
}
