import type { ReactNode } from 'react';
import { Badge, type BadgeProps } from '@/components/ui';
import { cn } from '@/lib/utils';
import { STATUS_LABEL, SOURCE_LABEL, type LeadSource, type LeadStatus, type Payment } from './types';

const STATUS_TONE: Record<LeadStatus, BadgeProps['tone']> = {
  new: 'info', contacted: 'neutral', qualified: 'brand', demo_booked: 'brand', demo_done: 'brand', proposal_sent: 'warning',
  negotiation: 'warning', closed_won: 'success', converted: 'success', closed_lost: 'danger', nurture: 'neutral',
};
export function StatusBadge({ status }: { status: LeadStatus }) {
  return <Badge tone={STATUS_TONE[status]}>{STATUS_LABEL[status]}</Badge>;
}
export const SourceLabel = ({ source }: { source: LeadSource }) => <>{SOURCE_LABEL[source]}</>;

const PAY_TONE: Record<Payment['status'], BadgeProps['tone']> = { pending: 'warning', paid: 'success', failed: 'danger' };
export function PaymentBadge({ status }: { status: Payment['status'] }) {
  return <Badge tone={PAY_TONE[status]}>{status === 'pending' ? 'Pending' : status === 'paid' ? 'Paid' : 'Failed'}</Badge>;
}

export function ScorePill({ score }: { score: number }) {
  const tone = score >= 70 ? 'bg-success-50 text-success-700' : score >= 45 ? 'bg-warning-50 text-warning-700' : 'bg-surface-muted text-muted';
  return <span className={cn('inline-flex min-w-9 justify-center rounded-md px-1.5 py-0.5 text-xs font-semibold tabular-nums', tone)}>{score}</span>;
}

const TZ = 'Asia/Kolkata';
export const fmtDate = (iso?: string) => (iso ? new Date(iso).toLocaleDateString('en-IN', { timeZone: TZ, day: 'numeric', month: 'short' }) : '—');
export const fmtDateYear = (iso?: string) => (iso ? new Date(iso).toLocaleDateString('en-IN', { timeZone: TZ, day: 'numeric', month: 'short', year: 'numeric' }) : '—');
export const fmtDateTime = (iso?: string) =>
  iso ? new Date(iso).toLocaleString('en-IN', { timeZone: TZ, day: 'numeric', month: 'short', hour: 'numeric', minute: '2-digit' }) : '—';
export const fmtTime = (iso: string) => new Date(iso).toLocaleTimeString('en-IN', { timeZone: TZ, hour: 'numeric', minute: '2-digit' });
/** For <input type="datetime-local"> in IST. */
export const toLocalInput = (iso: string) => new Date(Date.parse(iso) + 5.5 * 3_600_000).toISOString().slice(0, 16);

export function relDays(iso: string, nowIso: string): string {
  const days = Math.round((Date.parse(nowIso) - Date.parse(iso)) / 86_400_000);
  if (days <= 0) return 'today';
  if (days === 1) return 'yesterday';
  if (days < 30) return `${days} days ago`;
  return `${Math.round(days / 30)} mo ago`;
}

export function Field({ label, children, className }: { label: string; children: ReactNode; className?: string }) {
  return (
    <label className={cn('flex flex-col gap-1 text-sm', className)}>
      <span className="text-xs font-medium text-muted">{label}</span>
      {children}
    </label>
  );
}
export const inputCls = 'h-9 w-full rounded-lg border border-line bg-surface px-3 text-sm text-ink focus:outline-none focus:ring-2 focus:ring-brand-200';
export const textareaCls = 'min-h-[72px] w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm text-ink focus:outline-none focus:ring-2 focus:ring-brand-200';

export function DefRow({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="flex items-start justify-between gap-3 py-1.5 text-sm">
      <dt className="text-muted">{label}</dt>
      <dd className="text-right text-ink">{children}</dd>
    </div>
  );
}
