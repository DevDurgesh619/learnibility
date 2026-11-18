import Link from 'next/link';
import { Plus } from 'lucide-react';
import { AssignmentStatus } from '@/components/tutor/bits';
import { questionsOf, studentContext, type TutorAssignment } from '@/components/tutor/model';
import { formatDay } from '@/components/marketplace/dates';
import { Button, buttonVariants } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import { Table, TBody, TD, TH, THead, TR } from '@/components/ui/table';
import { remindTask } from '@/lib/actions/tutor';
import { getSubtopic } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import { cn } from '@/lib/utils';

const GROUPS = { all: 'All', review: 'Pending review', progress: 'In progress', done: 'Completed' } as const;

/** 4g assignments for one student, following the lifecycle Draft → Assigned → In progress → Submitted → AI evaluated → Reviewed → Completed. */
export default async function Assignments({ params, searchParams }: { params: Promise<{ learnerId: string }>; searchParams: Promise<{ g?: string }> }) {
  const { learnerId } = await params;
  const g = ((await searchParams).g ?? 'all') as keyof typeof GROUPS;
  const { ws } = studentContext((await currentPersona())!.id, learnerId)!;
  const all = (ws.assignments.filter((a) => a.learnerId === learnerId) as TutorAssignment[]).sort((a, b) => b.dueOn.localeCompare(a.dueOn));
  const grp = (a: TutorAssignment) => (a.status === 'submitted' || a.status === 'ai_evaluated' ? 'review' : a.status === 'completed' || a.status === 'reviewed' ? 'done' : 'progress');
  const list = all.filter((a) => g === 'all' || grp(a) === g);
  const base = `/tutor/students/${learnerId}/assignments`;
  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-2">
        {(Object.keys(GROUPS) as (keyof typeof GROUPS)[]).map((k) => (
          <Link key={k} href={`?g=${k}`} className={cn('rounded-full border px-3 py-1 text-sm', g === k ? 'border-brand-600 bg-brand-600 text-white' : 'border-line bg-surface hover:bg-surface-muted')}>
            {GROUPS[k]} · {k === 'all' ? all.length : all.filter((a) => grp(a) === k).length}
          </Link>
        ))}
        <Link href={`${base}/new`} className={buttonVariants({ size: 'sm', className: 'ml-auto' })}><Plus /> Add test</Link>
      </div>
      {list.length === 0 ? <EmptyState title="No assignments here" description="Add a test made with AI, from the question bank, or your own." action={<Link href={`${base}/new`} className={buttonVariants()}>Add test</Link>} /> : (
        <Card>
          <Table>
            <THead><TR><TH>Assignment</TH><TH className="hidden md:table-cell">Topic</TH><TH className="text-right">Qs</TH><TH>Status</TH><TH className="text-right">Score</TH><TH className="text-right">Action</TH></TR></THead>
            <TBody>
              {list.map((a) => (
                <TR key={a.id}>
                  <TD><p className="font-medium text-ink">{a.title}</p><p className="text-xs text-muted">due {formatDay(a.dueOn)}</p></TD>
                  <TD className="hidden max-w-56 truncate text-muted md:table-cell">{getSubtopic(a.subtopicIds[0] ?? '')?.name.split(/[;:]/)[0] ?? '—'}</TD>
                  <TD className="text-right">{questionsOf(a).length}</TD>
                  <TD><AssignmentStatus status={a.status} /></TD>
                  <TD className="text-right">{a.score !== undefined && a.maxScore ? `${a.score}/${a.maxScore}` : '—'}</TD>
                  <TD className="text-right">
                    {grp(a) === 'review' ? <Link href={`${base}/${a.id}`} className={buttonVariants({ size: 'sm' })}>Evaluate</Link>
                      : a.status === 'overdue' && a.taskId ? <form action={remindTask}><input type="hidden" name="learnerId" value={learnerId} /><input type="hidden" name="taskId" value={a.taskId} /><Button size="sm" variant="secondary">Remind</Button></form>
                        : grp(a) === 'done' ? <Link href={`/tutor/students/${learnerId}/learning/${a.id}`} className={buttonVariants({ size: 'sm', variant: 'secondary' })}>View</Link>
                          : <Link href={`${base}/${a.id}`} className={buttonVariants({ size: 'sm', variant: 'secondary' })}>View</Link>}
                  </TD>
                </TR>
              ))}
            </TBody>
          </Table>
        </Card>
      )}
      <p className="text-xs text-muted">Lifecycle: Draft → Assigned → In progress → Submitted → AI evaluated → Reviewed → Completed. Exceptions: Overdue, Needs revision.</p>
    </div>
  );
}
