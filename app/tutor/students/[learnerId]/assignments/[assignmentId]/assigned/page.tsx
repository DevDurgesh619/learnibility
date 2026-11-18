import Link from 'next/link';
import { notFound } from 'next/navigation';
import { CheckCircle2 } from 'lucide-react';
import { studentContext } from '@/components/tutor/model';
import { formatDay } from '@/components/marketplace/dates';
import { buttonVariants } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { currentPersona } from '@/lib/session';

/** 4l: assigned, and already in the student's Today and timetable. */
export default async function Assigned({ params }: { params: Promise<{ learnerId: string; assignmentId: string }> }) {
  const { learnerId, assignmentId } = await params;
  const { ws, row } = studentContext((await currentPersona())!.id, learnerId)!;
  const a = ws.assignments.find((x) => x.id === assignmentId);
  if (!a) notFound();
  const first = row.name.split(' ')[0];
  return (
    <Card className="mx-auto max-w-xl px-6 py-10 text-center">
      <CheckCircle2 className="mx-auto size-12 text-success-600" />
      <h2 className="mt-3 text-xl font-semibold text-ink">Assigned to {first}</h2>
      <p className="mt-2 text-sm text-muted">{a.title} · due {formatDay(a.dueOn)}. It&apos;s now in {first}&apos;s Today tasks and timetable. You&apos;ll see it in your review queue when {first} submits.</p>
      <div className="mt-6 flex flex-wrap justify-center gap-2">
        <Link href="/tutor/students?pick=assign" className={buttonVariants({ variant: 'secondary' })}>Assign to another student</Link>
        <Link href={`/tutor/students/${learnerId}/assignments`} className={buttonVariants()}>Done</Link>
      </div>
    </Card>
  );
}
