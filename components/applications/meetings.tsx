import { CheckCircle2, Circle, Sparkles } from 'lucide-react';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import { actionItemsToTasks, toggleActionItem } from '@/lib/actions/applications';
import type { MeetingNote } from '@/lib/data/types';
import { cn } from '@/lib/utils';
import { ActionButton } from './action-button';
import { nameOf } from './data';
import { fmtDate } from './logic';

/** Meeting notes with decisions and action items; action items become timetable tasks. */
export function MeetingList({ meetings, viewer, studentNames }: { meetings: MeetingNote[]; viewer: 'student' | 'counsellor' | 'parent'; studentNames?: Record<string, string> }) {
  if (!meetings.length) return <EmptyState title="No meetings yet" description="Notes, decisions and action items from each application meeting appear here." />;
  return (
    <div className="space-y-4">
      {meetings.map((m) => {
        const untasked = m.actionItems.filter((a) => !a.taskId && !a.done).length;
        return (
          <Card key={m.id}>
            <CardHeader
              title={<>{studentNames ? `${studentNames[m.learnerId] ?? m.learnerId} · ` : ''}Applications meeting with {nameOf(m.staffId)}</>}
              description={fmtDate(m.date)}
              action={<span className="inline-flex items-center gap-1 rounded-full bg-violet-50 px-2 py-0.5 text-xs font-medium text-violet-700"><Sparkles className="size-3" />AI summary</span>}
            />
            <CardBody className="grid gap-5 pt-3 lg:grid-cols-2">
              <div className="space-y-3 text-sm">
                <p className="text-ink">{m.summary}</p>
                {m.decisions.length > 0 && (
                  <div>
                    <p className="font-medium text-ink">Decisions</p>
                    <ul className="mt-1 list-disc space-y-0.5 pl-5 text-muted">{m.decisions.map((d) => <li key={d}>{d}</li>)}</ul>
                  </div>
                )}
              </div>
              <div>
                <p className="text-sm font-medium text-ink">Action items</p>
                <ul className="mt-1 divide-y divide-line">
                  {m.actionItems.map((a) => (
                    <li key={a.id} className="flex items-start gap-3 py-2 text-sm">
                      {viewer === 'student' ? (
                        <form action={toggleActionItem.bind(null, m.id, a.id)}><button aria-label={a.done ? 'Mark not done' : 'Mark done'} className={cn('mt-0.5 flex size-4 items-center justify-center rounded border text-[10px]', a.done ? 'border-brand-600 bg-brand-600 text-white' : 'border-line')}>{a.done ? '✓' : ''}</button></form>
                      ) : a.done ? <CheckCircle2 className="mt-0.5 size-4 text-success-600" /> : <Circle className="mt-0.5 size-4 text-subtle" />}
                      <div className="min-w-0 flex-1">
                        <p className={a.done ? 'text-subtle line-through' : 'text-ink'}>{a.title}</p>
                        <p className="text-xs text-subtle">Due {fmtDate(a.dueOn)}{a.taskId ? ' · in the timetable' : ''}</p>
                      </div>
                    </li>
                  ))}
                </ul>
                {viewer === 'student' && untasked > 0 && (
                  <div className="mt-2"><ActionButton size="sm" variant="secondary" action={actionItemsToTasks.bind(null, m.id)} done="Added ✓">Add {untasked} to my timetable</ActionButton></div>
                )}
              </div>
            </CardBody>
          </Card>
        );
      })}
    </div>
  );
}
