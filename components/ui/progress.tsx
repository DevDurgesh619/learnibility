import { cn } from '@/lib/utils';

/** value 0..1 */
export function Progress({ value, className, tone = 'brand' }: { value: number; className?: string; tone?: 'brand' | 'success' | 'warning' | 'danger' }) {
  const pct = Math.max(0, Math.min(1, value)) * 100;
  const bar = { brand: 'bg-brand-600', success: 'bg-success-600', warning: 'bg-warning-600', danger: 'bg-danger-600' }[tone];
  return (
    <div className={cn('h-2 w-full overflow-hidden rounded-full bg-surface-muted', className)} role="progressbar" aria-valuenow={Math.round(pct)} aria-valuemin={0} aria-valuemax={100}>
      <div className={cn('h-full rounded-full transition-all', bar)} style={{ width: `${pct}%` }} />
    </div>
  );
}
