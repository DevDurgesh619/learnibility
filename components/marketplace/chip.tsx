import type { ButtonHTMLAttributes, ReactNode } from 'react';
import Link from 'next/link';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';

const base = 'inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-sm transition-colors';
const on = 'border-brand-600 bg-brand-600 text-white';
const off = 'border-line bg-surface text-ink hover:border-brand-300 hover:bg-brand-50';

/** Toggle chip for filter panels and pickers. */
export function Chip({ selected, className, children, ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { selected?: boolean; children: ReactNode }) {
  return (
    <button type="button" aria-pressed={!!selected} className={cn(base, selected ? on : off, className)} {...props}>
      {children}
    </button>
  );
}

/** Static tag chip (expertise, topics). */
export function Tag({ children, tone = 'neutral', className }: { children: ReactNode; tone?: 'neutral' | 'brand'; className?: string }) {
  return (
    <span className={cn('inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium', tone === 'brand' ? 'border-brand-200 bg-brand-50 text-brand-700' : 'border-line bg-surface-muted text-muted', className)}>
      {children}
    </span>
  );
}

/** Applied-filter chip with a remove link (PDF 5c "★ 3+ ×"). */
export function RemovableChip({ href, children }: { href: string; children: ReactNode }) {
  return (
    <Link href={href} className={cn(base, 'border-line bg-surface text-ink hover:bg-surface-muted')}>
      {children}
      <X className="size-3.5 text-muted" aria-label="Remove filter" />
    </Link>
  );
}
