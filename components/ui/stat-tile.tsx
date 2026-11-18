import type { ReactNode } from 'react';
import { ArrowDownRight, ArrowUpRight } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Card } from './card';

export interface StatTileProps {
  label: string;
  value: ReactNode;
  /** e.g. "+6% this week". Positive or negative drives the colour unless `trendGood` overrides it. */
  delta?: { value: string; direction: 'up' | 'down'; good?: boolean };
  hint?: ReactNode;
  icon?: ReactNode;
  className?: string;
}

export function StatTile({ label, value, delta, hint, icon, className }: StatTileProps) {
  const good = delta ? (delta.good ?? delta.direction === 'up') : true;
  return (
    <Card className={cn('p-4', className)}>
      <div className="flex items-center justify-between text-sm text-muted">
        <span>{label}</span>
        {icon && <span className="text-subtle [&_svg]:size-4">{icon}</span>}
      </div>
      <div className="mt-2 flex items-baseline gap-2">
        <span className="text-2xl font-semibold tracking-tight text-ink">{value}</span>
        {delta && (
          <span className={cn('inline-flex items-center text-xs font-medium', good ? 'text-success-700' : 'text-danger-700')}>
            {delta.direction === 'up' ? <ArrowUpRight className="size-3.5" /> : <ArrowDownRight className="size-3.5" />}
            {delta.value}
          </span>
        )}
      </div>
      {hint && <p className="mt-1 text-xs text-subtle">{hint}</p>}
    </Card>
  );
}
