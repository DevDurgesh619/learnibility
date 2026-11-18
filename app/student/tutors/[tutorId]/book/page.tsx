import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound, redirect } from 'next/navigation';
import { ChevronLeft } from 'lucide-react';
import { DemoBookingForm } from '@/components/marketplace/demo-booking-form';
import { GAP_LABEL } from '@/components/ui/badge';
import { buildSnapshot, getTutor, loadMarketplaceLearner, mainSubjectFor, slotsFor } from '@/components/marketplace/queries';
import { Card, CardBody } from '@/components/ui/card';
import { requestDemo } from '@/lib/actions/booking';
import { currentPersona } from '@/lib/session';
import { formatHours } from '@/lib/format';

export const metadata: Metadata = { title: 'Book a free demo · Explore Tutors' };

export default async function BookDemoPage({ params }: { params: Promise<{ tutorId: string }> }) {
  const { tutorId } = await params;
  const tutor = getTutor(tutorId);
  if (!tutor) notFound();
  const persona = await currentPersona();
  const learner = persona ? await loadMarketplaceLearner(persona.id) : undefined;
  const open = learner?.bookings.find((b) => b.tutorId === tutor.id && (b.status === 'requested' || b.status === 'accepted'));
  if (open) redirect(`/student/tutors/booked/${open.id}`);

  const subjectId = learner ? mainSubjectFor(learner, tutor) : undefined;
  const snap = learner && subjectId ? buildSnapshot(learner, subjectId) : undefined;
  const preview = snap ? [learner!.names[subjectId!] ?? subjectId!, ...snap.gaps.slice(0, 4).map((g) => `${g.name} · ${g.code} ${GAP_LABEL[g.code]} · about ${formatHours(g.hoursToClose)} to close`)] : [];
  const topic = snap?.gaps[0] ? `${snap.gaps[0].name}${snap.gaps[1] ? ` and ${snap.gaps[1].name}` : ''} (from your gap analysis)` : '';
  const { days, bothCalendars } = await slotsFor(tutor, learner?.student);
  const minutes = tutor.pricing.demoMinutes || 30;

  return (
    <>
      <Link href={`/student/tutors/${tutor.id}`} className="mb-4 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" /> {tutor.displayName}</Link>
      <h1 className="text-2xl font-semibold tracking-tight text-ink">{tutor.pricing.demoInr === 0 ? 'Free demo' : 'Demo'} call with {tutor.firstName} · {minutes} min</h1>
      <p className="mt-1 text-sm text-muted">Meet {tutor.firstName}, talk through what you need, and decide after. Nothing is charged for a free demo.</p>
      <Card className="mt-6">
        <CardBody>
          <DemoBookingForm action={requestDemo} tutorId={tutor.id} tutorFirstName={tutor.firstName} days={days} defaultTopic={topic} subjectId={subjectId} snapshotPreview={preview} minutes={minutes} bothCalendars={bothCalendars} />
        </CardBody>
      </Card>
    </>
  );
}
