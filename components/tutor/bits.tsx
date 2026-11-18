import type { ReactNode } from 'react';
import Link from 'next/link';
import { ArrowDownRight, ArrowUpRight, ChevronLeft, Minus } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import type { Assignment, Session } from '@/lib/data/types';

export function BackLink({ href, children }: { href: string; children: ReactNode }) {
  return <Link href={href} className="mb-4 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" />{children}</Link>;
}

export function Delta({ value, suffix = '%', className }: { value: number | null | undefined; suffix?: string; className?: string }) {
  if (value === null || value === undefined) return <span className={cn('text-xs text-subtle', className)}>—</span>;
  const Icon = value > 0 ? ArrowUpRight : value < 0 ? ArrowDownRight : Minus;
  return (
    <span className={cn('inline-flex items-center gap-0.5 text-xs font-medium', value > 0 ? 'text-success-700' : value < 0 ? 'text-danger-700' : 'text-muted', className)}>
      <Icon className="size-3.5" />{Math.abs(value)}{suffix}
    </span>
  );
}

export function SectionTitle({ children, action, className }: { children: ReactNode; action?: ReactNode; className?: string }) {
  return (
    <div className={cn('mb-3 flex items-center justify-between gap-3', className)}>
      <h2 className="text-base font-semibold text-ink">{children}</h2>
      {action}
    </div>
  );
}

const ASG: Record<Assignment['status'], { label: string; tone: 'neutral' | 'brand' | 'success' | 'warning' | 'danger' | 'info' }> = {
  draft: { label: 'Draft', tone: 'neutral' }, assigned: { label: 'Assigned', tone: 'info' }, in_progress: { label: 'In progress', tone: 'info' },
  submitted: { label: 'Needs review', tone: 'warning' }, ai_evaluated: { label: 'Needs review', tone: 'warning' }, reviewed: { label: 'Reviewed', tone: 'brand' },
  completed: { label: 'Completed', tone: 'success' }, overdue: { label: 'Overdue', tone: 'danger' },
};
export function AssignmentStatus({ status }: { status: Assignment['status'] }) {
  return <Badge tone={ASG[status].tone}>{ASG[status].label}</Badge>;
}

export function SessionKind({ s }: { s: Session }) {
  return <Badge tone={s.kind === 'demo' ? 'info' : s.kind === 'group' ? 'brand' : 'neutral'}>{s.kind === 'demo' ? 'Demo' : s.kind === 'group' ? 'Group' : '1:1'}</Badge>;
}

export function Stat({ label, value, hint, href }: { label: string; value: ReactNode; hint?: ReactNode; href?: string }) {
  const body = (
    <div className={cn('rounded-[var(--radius-card)] border border-line bg-surface p-4 shadow-[var(--shadow-card)]', href && 'hover:border-brand-300')}>
      <p className="text-sm text-muted">{label}</p>
      <p className="mt-1 text-2xl font-semibold tracking-tight text-ink">{value}</p>
      {hint && <p className="mt-0.5 text-xs text-subtle">{hint}</p>}
    </div>
  );
  return href ? <Link href={href}>{body}</Link> : body;
}

export function Pill({ children, tone = 'neutral' }: { children: ReactNode; tone?: 'neutral' | 'success' | 'warning' | 'danger' | 'brand' }) {
  const t = { neutral: 'bg-surface-muted text-muted', success: 'bg-success-50 text-success-700', warning: 'bg-warning-50 text-warning-700', danger: 'bg-danger-50 text-danger-700', brand: 'bg-brand-50 text-brand-700' }[tone];
  return <span className={cn('inline-flex items-center rounded-md px-1.5 py-0.5 text-xs font-medium', t)}>{children}</span>;
}
