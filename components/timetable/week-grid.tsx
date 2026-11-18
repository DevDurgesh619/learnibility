import type { TimetableBlock } from '@/lib/engines';
import { cn } from '@/lib/utils';

export const BLOCK_STYLE: Record<TimetableBlock['kind'] | 'pending', string> = {
  session: 'bg-success-50 text-success-700 ring-success-600/20',
  weekly_test: 'bg-brand-50 text-brand-700 ring-brand-200',
  carry_over: 'bg-danger-50 text-danger-700 ring-danger-600/20',
  review: 'bg-info-50 text-info-600 ring-info-600/20',
  gap: 'bg-warning-50 text-warning-700 ring-warning-600/20',
  chapter: 'bg-surface-muted text-ink ring-line',
  buffer: 'bg-surface text-subtle ring-line ring-dashed',
  locked: 'bg-surface-muted text-muted ring-line',
  pending: 'bg-surface text-muted ring-line border border-dashed border-subtle',
};

export const BLOCK_LABEL: Record<TimetableBlock['kind'], string> = {
  session: 'Session', weekly_test: 'Weekly test', carry_over: 'Carried over', review: 'Spaced review', gap: 'Gap practice',
  chapter: 'Chapter practice', buffer: 'Buffer', locked: 'Locked',
};

export interface GridDay {
  date: string;
  label: string;
  dayNum: string;
  isToday: boolean;
  blocks: (Pick<TimetableBlock, 'id' | 'kind' | 'title' | 'start' | 'minutes' | 'status'> & { pending?: boolean })[];
}

/** PDF 3a bottom strip: the week, one column per day, blocks as chips. Collapses to a list of days on phones. */
export function WeekGrid({ days }: { days: GridDay[] }) {
  return (
    <div className="grid gap-2 sm:grid-cols-7">
      {days.map((d) => (
        <section
          key={d.date}
          aria-label={d.label}
          className={cn('min-h-28 rounded-xl border bg-surface p-2', d.isToday ? 'border-brand-500 ring-2 ring-brand-100' : 'border-line')}
        >
          <header className="mb-2 flex items-baseline justify-between border-b border-line pb-1">
            <span className={cn('text-xs font-semibold', d.isToday ? 'text-brand-700' : 'text-ink')}>{d.label}</span>
            <span className="text-[11px] text-subtle">{d.dayNum}</span>
          </header>
          {d.blocks.length === 0 ? (
            <p className="text-[11px] text-subtle">Free</p>
          ) : (
            <ul className="flex flex-col gap-1">
              {d.blocks.map((b) => (
                <li
                  key={b.id}
                  title={`${b.start} · ${b.minutes} min · ${b.title}`}
                  className={cn('rounded-md px-1.5 py-1 text-[11px] leading-tight ring-1 ring-inset', BLOCK_STYLE[b.pending ? 'pending' : b.kind], b.status === 'done' && !b.pending && 'opacity-55')}
                >
                  <span className="font-medium tabular-nums">{b.start}</span>{' '}
                  <span className={cn(b.status === 'done' && !b.pending && 'line-through')}>{b.title}</span>
                  {b.pending && <span className="block italic">(pending)</span>}
                </li>
              ))}
            </ul>
          )}
        </section>
      ))}
    </div>
  );
}

export function BlockLegend() {
  const kinds: TimetableBlock['kind'][] = ['gap', 'review', 'chapter', 'weekly_test', 'session'];
  return (
    <div className="flex flex-wrap gap-2 text-[11px]">
      {kinds.map((k) => <span key={k} className={cn('rounded-md px-1.5 py-0.5 ring-1 ring-inset', BLOCK_STYLE[k])}>{BLOCK_LABEL[k]}</span>)}
    </div>
  );
}
