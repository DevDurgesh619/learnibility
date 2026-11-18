import { Badge } from '@/components/ui';
import type { TimetableWeek } from '@/lib/data/types';
import { cn } from '@/lib/utils';
import { formatDay, formatHHMM } from './format';

const KIND_LABEL: Record<string, string> = { session: 'Session', weekly_test: 'Weekly test', carry_over: 'Carried over', review: 'Review', gap: 'Gap work', chapter: 'Chapter', buffer: 'Buffer', locked: 'Locked' };

/** The days a change touched (or the whole week), as compact block lists. */
export function DayPlan({ week, highlight = [] }: { week: TimetableWeek; highlight?: string[] }) {
  const hl = new Set(highlight);
  const dates = [...new Set(week.blocks.filter((b) => !hl.size || hl.has(b.id)).map((b) => b.date))].sort();
  return (
    <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
      {dates.map((d) => (
        <div key={d} className="rounded-lg border border-line bg-surface p-3">
          <p className="mb-2 text-sm font-medium text-ink">{formatDay(d)}</p>
          <ul className="space-y-1">
            {week.blocks.filter((b) => b.date === d && b.kind !== 'buffer').map((b) => (
              <li key={b.id} className={cn('flex items-center gap-2 rounded px-2 py-1 text-xs', hl.has(b.id) ? 'bg-brand-50 ring-1 ring-brand-200' : '')}>
                <span className="w-24 shrink-0 text-muted">{formatHHMM(b.start)}–{formatHHMM(b.end)}</span>
                <span className="min-w-0 flex-1 truncate text-ink">{b.title}</span>
                {hl.has(b.id) ? <Badge tone="brand">Changed</Badge> : <span className="text-subtle">{KIND_LABEL[b.kind]}</span>}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
