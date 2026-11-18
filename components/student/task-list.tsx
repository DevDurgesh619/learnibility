'use client';

import Link from 'next/link';
import { useOptimistic, useTransition } from 'react';
import { Check } from 'lucide-react';
import { setTaskDone } from '@/lib/actions/timetable';
import { cn } from '@/lib/utils';
import type { TaskItem } from './model';

const KIND_DOT: Record<string, string> = {
  gap: 'bg-warning-600', review: 'bg-info-600', weekly_test: 'bg-brand-600', session: 'bg-success-600',
  chapter: 'bg-chart-2', carry_over: 'bg-danger-600', homework: 'bg-chart-5', todo: 'bg-subtle', application: 'bg-success-600',
};

/** Checkable task rows (PDF 2b "Today's tasks", 3a). Ticking writes through lib/actions/timetable.ts. */
export function TaskList({ tasks, columns = 1, readOnly = false }: { tasks: TaskItem[]; columns?: 1 | 2; readOnly?: boolean }) {
  const [optimistic, setOptimistic] = useOptimistic(tasks, (state, { id, done }: { id: string; done: boolean }) =>
    state.map((t) => (t.id === id ? { ...t, done } : t)));
  const [, start] = useTransition();
  const toggle = (t: TaskItem) => start(async () => {
    setOptimistic({ id: t.id, done: !t.done });
    await setTaskDone(t.id, !t.done);
  });

  return (
    <ul className={cn('grid gap-x-6', columns === 2 && 'sm:grid-cols-2')}>
      {optimistic.map((t, i) => (
        <li key={t.id} className="flex items-center gap-3 border-b border-line py-2.5 last:border-b-0 sm:[&:nth-last-child(2)]:border-b-0">
          <button
            type="button"
            disabled={readOnly || t.id.startsWith('starter_')}
            onClick={() => toggle(t)}
            aria-pressed={t.done}
            aria-label={t.done ? `Mark "${t.title}" not done` : `Mark "${t.title}" done`}
            className={cn('flex size-5 shrink-0 items-center justify-center rounded-md border transition-colors',
              t.done ? 'border-brand-600 bg-brand-600 text-white' : 'border-line bg-surface hover:border-brand-400', 'disabled:cursor-default')}
          >
            {t.done && <Check className="size-3.5" strokeWidth={3} />}
          </button>
          <span className={cn('size-1.5 shrink-0 rounded-full', KIND_DOT[t.kind] ?? 'bg-subtle')} aria-hidden />
          <div className="min-w-0 flex-1">
            {t.href && !t.done ? (
              <Link href={t.href} className="block truncate text-sm text-ink hover:text-brand-700">{columns === 2 ? `${i + 1}. ` : ''}{t.title}</Link>
            ) : (
              <p className={cn('truncate text-sm', t.done ? 'text-subtle line-through' : 'text-ink')}>{columns === 2 ? `${i + 1}. ` : ''}{t.title}</p>
            )}
          </div>
          {t.meta && <span className="hidden shrink-0 text-xs text-muted sm:inline">{t.meta}</span>}
          {t.tag && <span className="shrink-0 rounded-full bg-success-50 px-2 py-0.5 text-[11px] font-medium text-success-700 ring-1 ring-inset ring-success-600/20">{t.tag}</span>}
        </li>
      ))}
    </ul>
  );
}
