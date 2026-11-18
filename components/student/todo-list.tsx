'use client';

import { useOptimistic, useTransition } from 'react';
import { Check } from 'lucide-react';
import { setTodoStatus } from '@/lib/actions/timetable';
import { cn } from '@/lib/utils';
import type { TodoItem } from './model';

/** PDF 10b: to-dos from a counsellor, tutor or mentor with Pending / Done and Remove. */
export function TodoList({ todos, personFirstName }: { todos: (TodoItem & { dueLabel?: string })[]; personFirstName: string }) {
  const [items, apply] = useOptimistic(todos, (s, { id, status }: { id: string; status: TodoItem['status'] }) =>
    s.map((t) => (t.id === id ? { ...t, status } : t)).filter((t) => t.status !== 'removed'));
  const [, start] = useTransition();
  const set = (id: string, status: TodoItem['status']) => start(async () => { apply({ id, status }); await setTodoStatus(id, status); });

  if (!items.length) return <p className="py-6 text-center text-sm text-muted">No to-dos from {personFirstName}.</p>;
  return (
    <>
      <ul className="divide-y divide-line">
        {items.map((t) => {
          const done = t.status === 'done';
          return (
            <li key={t.id} className="flex items-center gap-3 py-2.5">
              <button type="button" onClick={() => set(t.id, done ? 'pending' : 'done')} aria-pressed={done} aria-label={done ? 'Mark pending' : 'Mark done'}
                className={cn('flex size-5 shrink-0 items-center justify-center rounded-md border', done ? 'border-brand-600 bg-brand-600 text-white' : 'border-line hover:border-brand-400')}>
                {done && <Check className="size-3.5" strokeWidth={3} />}
              </button>
              <p className={cn('min-w-0 flex-1 text-sm', done ? 'text-subtle line-through' : 'text-ink')}>{t.title}{t.dueLabel && <span className="text-muted"> · due {t.dueLabel}</span>}</p>
              <span className={cn('rounded-full px-2 py-0.5 text-[11px] font-medium ring-1 ring-inset', done ? 'bg-surface-muted text-muted ring-line' : 'bg-success-50 text-success-700 ring-success-600/20')}>{done ? 'Done' : 'Pending'}</span>
              <button type="button" onClick={() => set(t.id, 'removed')} className="text-xs text-subtle hover:text-danger-700">Remove</button>
            </li>
          );
        })}
      </ul>
      <p className="mt-2 text-xs text-subtle">Mark done, or remove a to-do if you agreed that with {personFirstName}.</p>
    </>
  );
}
