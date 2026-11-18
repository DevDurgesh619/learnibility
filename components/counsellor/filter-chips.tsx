import Link from 'next/link';
import { cn } from '@/lib/utils';

/** Link chips that set one query param (server-rendered filters, no client state). */
export function FilterChips({ base, param, options, value, keep = {} }: {
  base: string; param: string; value?: string;
  options: { value: string; label: string; count?: number }[];
  keep?: Record<string, string | undefined>;
}) {
  const href = (v: string) => {
    const q = new URLSearchParams();
    for (const [k, x] of Object.entries(keep)) if (x) q.set(k, x);
    if (v) q.set(param, v);
    const s = q.toString();
    return s ? `${base}?${s}` : base;
  };
  return (
    <div className="flex flex-wrap gap-2">
      {options.map((o) => {
        const active = (value ?? '') === o.value;
        return (
          <Link key={o.value || 'all'} href={href(o.value)} scroll={false}
            className={cn('inline-flex h-8 items-center gap-1.5 rounded-full border px-3 text-sm transition-colors',
              active ? 'border-brand-600 bg-brand-600 text-white' : 'border-line bg-surface text-muted hover:text-ink')}>
            {o.label}
            {o.count != null && <span className={cn('rounded-full px-1.5 text-xs', active ? 'bg-white/20' : 'bg-surface-muted')}>{o.count}</span>}
          </Link>
        );
      })}
    </div>
  );
}
