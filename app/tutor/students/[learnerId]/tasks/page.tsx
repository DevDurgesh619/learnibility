import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import { Table, TBody, TD, TH, THead, TR } from '@/components/ui/table';
import { formatDay } from '@/components/marketplace/dates';
import { studentContext } from '@/components/tutor/model';
import { addTask, remindTask } from '@/lib/actions/tutor';
import { addDaysLocal, demoToday, getTasks } from '@/lib/data';
import type { Task } from '@/lib/data/types';
import { currentPersona } from '@/lib/session';
import { cn } from '@/lib/utils';

const FILTERS = ['pending', 'completed', 'urgent', 'critical', 'forgot'] as const;

/** 4m tasks set for one student (the student sees them in Today and the timetable). */
export default async function Tasks({ params, searchParams }: { params: Promise<{ learnerId: string }>; searchParams: Promise<{ f?: string }> }) {
  const { learnerId } = await params;
  const f = (await searchParams).f ?? 'pending';
  const { ws, row } = studentContext((await currentPersona())!.id, learnerId)!;
  const today = demoToday();
  const all = getTasks(learnerId).filter((t) => t.createdBy === ws.tutor.id || t.source === 'tutor');
  const nextSessionDay = row.nextSession?.startUtc.slice(0, 10);
  const tag = (t: Task) => {
    if (t.status === 'done') return 'completed';
    if (t.status === 'skipped' || (t.dueDate < today && t.detail?.startsWith('Forgot'))) return 'forgot';
    if (t.dueDate <= today) return 'urgent';
    if (nextSessionDay && t.dueDate <= nextSessionDay) return 'critical';
    return 'pending';
  };
  const list = all.filter((t) => (f === 'pending' ? t.status === 'todo' : tag(t) === f)).sort((a, b) => (f === 'completed' ? b.dueDate.localeCompare(a.dueDate) : a.dueDate.localeCompare(b.dueDate)));
  const source = (t: Task) => (t.kind === 'test' ? 'Assignment' : t.refId?.startsWith('ses') ? `Session ${ws.sessions.find((s) => s.id === t.refId)?.code ?? ''}` : 'Added by you');
  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2">
        {FILTERS.map((k) => (
          <Link key={k} href={`?f=${k}`} className={cn('rounded-full border px-3 py-1 text-sm capitalize', f === k ? 'border-brand-600 bg-brand-600 text-white' : 'border-line bg-surface hover:bg-surface-muted')}>
            {k}{k === 'pending' ? ` · ${all.filter((t) => t.status === 'todo').length}` : ''}
          </Link>
        ))}
      </div>
      <form action={addTask} className="flex flex-col gap-2 rounded-[var(--radius-card)] border border-line bg-surface p-3 sm:flex-row">
        <input type="hidden" name="learnerId" value={learnerId} />
        <input name="title" required placeholder="Add a task, e.g. Read 4 pages on constraint equations" className="h-9 flex-1 rounded-lg border border-line px-3 text-sm" />
        <input name="dueDate" type="date" defaultValue={addDaysLocal(today, 2)} className="h-9 rounded-lg border border-line px-2 text-sm" />
        <select name="priority" className="h-9 rounded-lg border border-line px-2 text-sm"><option value="normal">Normal</option><option value="urgent">Urgent</option></select>
        <Button size="sm" className="h-9">Add task</Button>
      </form>
      {list.length === 0 ? <EmptyState title={`No ${f} tasks`} description="Homework from session reports and assignments shows here." /> : (
        <Card>
          <Table>
            <THead><TR><TH>Task</TH><TH>Due</TH><TH>Priority</TH><TH className="hidden sm:table-cell">Source</TH><TH /></TR></THead>
            <TBody>
              {list.map((t) => {
                const tg = tag(t);
                return (
                  <TR key={t.id}>
                    <TD className={cn('text-ink', t.status === 'done' && 'text-muted line-through')}>{t.title}</TD>
                    <TD className={cn(t.status === 'todo' && t.dueDate < today && 'text-danger-700')}>{formatDay(t.dueDate)}{t.status === 'todo' && t.dueDate < today ? ' · overdue' : ''}</TD>
                    <TD><Badge tone={tg === 'urgent' ? 'danger' : tg === 'critical' ? 'warning' : tg === 'completed' ? 'success' : tg === 'forgot' ? 'neutral' : 'info'}>{tg === 'critical' ? 'Critical' : tg === 'urgent' ? 'Urgent' : tg === 'completed' ? 'Done' : tg === 'forgot' ? 'Forgot' : 'Normal'}</Badge></TD>
                    <TD className="hidden text-muted sm:table-cell">{source(t)}</TD>
                    <TD className="text-right">{t.status === 'todo' && t.dueDate < today && (
                      <form action={remindTask}><input type="hidden" name="learnerId" value={learnerId} /><input type="hidden" name="taskId" value={t.id} /><Button size="sm" variant="secondary">Remind</Button></form>
                    )}</TD>
                  </TR>
                );
              })}
            </TBody>
          </Table>
        </Card>
      )}
      <p className="text-xs text-muted">Tasks appear in {row.name.split(' ')[0]}&apos;s Today and timetable. Critical = due before the next session; Forgot = marked missed.</p>
    </div>
  );
}
