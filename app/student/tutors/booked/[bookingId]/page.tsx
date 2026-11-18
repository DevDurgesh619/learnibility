import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { CheckCircle2, Clock3, XCircle } from 'lucide-react';
import { formatDateTime, formatRange } from '@/components/marketplace/dates';
import { getTutor, loadMarketplaceLearner } from '@/components/marketplace/queries';
import { buttonVariants } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Booking · Explore Tutors' };

/** PDF 5f: confirmation and hand-off to Sessions (10a) and Timetable (3a). */
export default async function BookedPage({ params }: { params: Promise<{ bookingId: string }> }) {
  const { bookingId } = await params;
  const persona = await currentPersona();
  const learner = persona ? await loadMarketplaceLearner(persona.id) : undefined;
  const b = learner?.bookings.find((x) => x.id === bookingId);
  if (!b) notFound();
  const tutor = getTutor(b.tutorId);
  const name = tutor?.firstName ?? 'your tutor';
  const when = b.slotStartUtc ? `${formatDateTime(b.slotStartUtc).replace(/, \d.*$/, '')} · ${formatRange(b.slotStartUtc, b.minutes)}` : 'Time to be agreed';
  const declined = b.status === 'declined' || b.status === 'cancelled';
  const confirmed = b.status === 'accepted' || b.status === 'active' || b.status === 'completed';

  return (
    <Card className="mx-auto mt-6 max-w-xl px-6 py-12 text-center">
      <div className={`mx-auto flex size-14 items-center justify-center rounded-full ${declined ? 'bg-danger-50 text-danger-600' : confirmed ? 'bg-success-50 text-success-600' : 'bg-brand-50 text-brand-600'}`}>
        {declined ? <XCircle className="size-7" /> : confirmed ? <CheckCircle2 className="size-7" /> : <Clock3 className="size-7" />}
      </div>
      <h1 className="mt-4 text-xl font-semibold text-ink">
        {declined ? `${name} can't make this one` : confirmed ? `You're booked with ${name}` : `Demo requested with ${name}`}
      </h1>
      <p className="mt-1 text-sm text-ink">{when} · Online video call</p>
      <p className="mx-auto mt-3 max-w-md text-sm text-muted">
        {declined
          ? `Pick another time or another tutor. Your gap snapshot was not kept.`
          : `Added to your Sessions and Timetable${confirmed ? '' : `; ${name} usually confirms within ${tutor?.responseTimeHours ?? 24} hours`}. ${b.sharedGapSnapshot ? `${name} gets your ${b.topic ? 'topic and ' : ''}gap snapshot.` : `${name} only sees your name, class and topic.`}`}
      </p>
      {b.topic && <p className="mx-auto mt-2 max-w-md text-xs text-subtle">Topic: {b.topic}</p>}
      <div className="mt-6 flex flex-wrap justify-center gap-2">
        {declined ? (
          <Link href={`/student/tutors/${b.tutorId}/book`} className={buttonVariants()}>Pick another time</Link>
        ) : (
          <Link href="/student/sessions" className={buttonVariants()}>Go to Sessions</Link>
        )}
        <Link href="/student/tutors" className={buttonVariants({ variant: 'secondary' })}>Back to Explore</Link>
      </div>
    </Card>
  );
}
