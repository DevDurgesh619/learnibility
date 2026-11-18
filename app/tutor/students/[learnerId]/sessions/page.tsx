import Link from 'next/link';
import { Plus } from 'lucide-react';
import { SectionKindRow } from '@/components/tutor/session-row';
import { SectionTitle } from '@/components/tutor/bits';
import { isUpcoming, sessionsFor, studentContext } from '@/components/tutor/model';
import { buttonVariants } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import { currentPersona } from '@/lib/session';

/** 4f sessions with one student. */
export default async function StudentSessions({ params, searchParams }: { params: Promise<{ learnerId: string }>; searchParams: Promise<{ all?: string }> }) {
  const { learnerId } = await params;
  const sp = await searchParams;
  const { ws, row } = studentContext((await currentPersona())!.id, learnerId)!;
  const all = sessionsFor(ws, learnerId).filter((s) => s.status !== 'cancelled');
  const upcoming = all.filter((s) => isUpcoming(s));
  const past = all.filter((s) => !isUpcoming(s)).reverse();
  const shown = sp.all ? past : past.slice(0, 4);
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-3 gap-3">
        <Card className="p-4"><p className="text-sm text-muted">Total sessions</p><p className="mt-1 text-2xl font-semibold">{row.sessionsDone}</p></Card>
        <Card className="p-4"><p className="text-sm text-muted">Attendance</p><p className="mt-1 text-2xl font-semibold">{row.attendancePct ?? 100}%</p></Card>
        <Card className="p-4"><p className="text-sm text-muted">Reports filed</p><p className="mt-1 text-2xl font-semibold">{past.filter((s) => s.report).length}</p></Card>
      </div>
      <section>
        <SectionTitle action={<Link href={`/tutor/sessions?view=calendar&student=${learnerId}`} className={buttonVariants({ size: 'sm', variant: 'secondary' })}><Plus /> Create session</Link>}>Upcoming</SectionTitle>
        {upcoming.length === 0 ? <EmptyState title="Nothing scheduled" description="Create a session from an open slot in your calendar." /> : <Card><ul className="divide-y divide-line">{upcoming.map((s) => <SectionKindRow key={s.id} ws={ws} s={s} />)}</ul></Card>}
      </section>
      <section>
        <SectionTitle>Completed</SectionTitle>
        {past.length === 0 ? <p className="text-sm text-muted">No past sessions yet.</p> : (
          <Card><ul className="divide-y divide-line">{shown.map((s) => <SectionKindRow key={s.id} ws={ws} s={s} />)}</ul></Card>
        )}
        {past.length > shown.length && <Link href="?all=1" className="mt-2 inline-block text-sm text-brand-700 hover:underline">Show {past.length - shown.length} more</Link>}
      </section>
    </div>
  );
}
