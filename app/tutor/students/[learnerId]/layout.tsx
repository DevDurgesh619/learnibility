import type { ReactNode } from 'react';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { MessageSquare, CalendarPlus } from 'lucide-react';
import { BackLink } from '@/components/tutor/bits';
import { LinkTabs } from '@/components/tutor/tabs';
import { studentContext } from '@/components/tutor/model';
import { formatDate } from '@/components/marketplace/dates';
import { BOARD_LABEL } from '@/components/marketplace/labels';
import { Avatar } from '@/components/ui/avatar';
import { buttonVariants } from '@/components/ui/button';
import { currentPersona } from '@/lib/session';

/** Tutor HTML 4a-4o: one student's workspace with seven tabs. */
export default async function StudentLayout({ children, params }: { children: ReactNode; params: Promise<{ learnerId: string }> }) {
  const { learnerId } = await params;
  const persona = (await currentPersona())!;
  const ctx = studentContext(persona.id, learnerId);
  if (!ctx) notFound();
  const { row, ws } = ctx;
  const base = `/tutor/students/${learnerId}`;
  const reviews = row.pendingReview.length;
  const subj = row.subjectIds[0];
  return (
    <>
      <BackLink href="/tutor/students">Students</BackLink>
      <div className="mb-5 flex flex-col gap-4 sm:flex-row sm:items-center">
        <Avatar name={row.name} size="lg" />
        <div className="min-w-0 flex-1">
          <h1 className="text-2xl font-semibold tracking-tight text-ink">{row.name}</h1>
          <p className="text-sm text-muted">Class {row.grade} · {BOARD_LABEL[row.board]}{subj ? ` · ${subj.split('-').slice(2).join(' ').replace(/^\w/, (c) => c.toUpperCase())}` : ''}{row.goal ? ` · target ${row.goal}` : ''} · since {formatDate(row.sinceUtc)}</p>
        </div>
        <div className="flex gap-2">
          <Link href={`${base}/messages`} className={buttonVariants({ variant: 'secondary', size: 'sm' })}><MessageSquare /> Message</Link>
          <Link href={`/tutor/sessions?view=calendar&student=${learnerId}`} className={buttonVariants({ size: 'sm' })}><CalendarPlus /> Schedule session</Link>
        </div>
      </div>
      <LinkTabs className="mb-6" tabs={[
        { href: base, label: 'Overview' }, { href: `${base}/learning`, label: 'Learning' }, { href: `${base}/sessions`, label: 'Sessions' },
        { href: `${base}/tasks`, label: 'Tasks', count: row.overdueTasks.length }, { href: `${base}/assignments`, label: 'Assignments', count: reviews },
        { href: `${base}/messages`, label: 'Messages' }, { href: `${base}/notes`, label: 'Notes', count: ws.notes.filter((n) => n.learnerId === learnerId).length },
      ]} />
      {children}
    </>
  );
}
