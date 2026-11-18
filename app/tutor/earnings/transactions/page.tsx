import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { Search } from 'lucide-react';
import { Pill } from '@/components/tutor/bits';
import { earningRows, loadWorkspace, money, type EarningRow } from '@/components/tutor/model';
import { formatDate, formatDay } from '@/components/marketplace/dates';
import { buttonVariants } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import { Table, TBody, TD, TH, THead, TR } from '@/components/ui/table';
import { demoToday, localDateOf } from '@/lib/data';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Transactions · Tutor' };

const STATUS: Record<EarningRow['status'], { label: string; tone: 'success' | 'neutral' | 'danger' | 'warning' }> = {
  paid: { label: 'Paid', tone: 'success' }, pending: { label: 'Pending', tone: 'neutral' }, report_missing: { label: 'Report missing', tone: 'danger' }, free: { label: '—', tone: 'neutral' },
};

/** Tutor HTML 7b: per-session transactions (filters: student search, this month, pending only) and the payouts list. */
export default async function TransactionsPage({ searchParams }: { searchParams: Promise<{ tab?: string; q?: string; month?: string; pending?: string }> }) {
  const sp = await searchParams;
  const persona = (await currentPersona())!;
  const ws = loadWorkspace(persona.id);
  if (!ws) notFound();
  const tab = sp.tab === 'payouts' ? 'payouts' : 'sessions';
  const q = (sp.q ?? '').trim().toLowerCase();
  const month = demoToday().slice(0, 7);
  const rows = earningRows(ws).filter((r) => (!q || r.who.toLowerCase().includes(q) || (r.session.code ?? '').toLowerCase().includes(q))
    && (!sp.month || localDateOf(r.session.startUtc).startsWith(month)) && (!sp.pending || r.status === 'pending' || r.status === 'report_missing'));
  const payouts = [...ws.payouts].sort((a, b) => b.paidOn.localeCompare(a.paidOn));
  const fee = Math.round((ws.tutor.platformFeeRate ?? 0.15) * 100);
  const link = (p: Record<string, string | undefined>) => {
    const u = new URLSearchParams(Object.entries({ q: sp.q, month: sp.month, pending: sp.pending, ...p }).filter(([, v]) => v) as [string, string][]);
    const str = u.toString();
    return `/tutor/earnings/transactions${str ? `?${str}` : ''}`;
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-2">
        <Link href={link({ tab: undefined })} className={buttonVariants({ size: 'sm', variant: tab === 'sessions' ? 'primary' : 'secondary' })}>Sessions</Link>
        <Link href={link({ tab: 'payouts' })} className={buttonVariants({ size: 'sm', variant: tab === 'payouts' ? 'primary' : 'secondary' })}>Payouts · {payouts.length}</Link>
      </div>

      {tab === 'sessions' ? (
        <>
          <form className="flex flex-wrap items-center gap-2" action="/tutor/earnings/transactions">
            <label className="relative flex-1 sm:max-w-xs"><Search className="absolute left-3 top-2.5 size-4 text-subtle" /><input name="q" defaultValue={sp.q} placeholder="Student or session…" aria-label="Search transactions" className="h-9 w-full rounded-lg border border-line bg-surface pl-9 pr-3 text-sm text-ink" /></label>
            {sp.month && <input type="hidden" name="month" value="1" />}{sp.pending && <input type="hidden" name="pending" value="1" />}
            <Link href={link({ month: sp.month ? undefined : '1' })} className={buttonVariants({ size: 'sm', variant: sp.month ? 'primary' : 'secondary' })}>This month</Link>
            <Link href={link({ pending: sp.pending ? undefined : '1' })} className={buttonVariants({ size: 'sm', variant: sp.pending ? 'primary' : 'secondary' })}>Pending only</Link>
          </form>
          {rows.length ? (
            <Card className="overflow-x-auto">
              <Table>
                <THead><TR><TH>Date</TH><TH>Session</TH><TH>Student</TH><TH>Duration</TH><TH>Rate</TH><TH className="text-right">You get</TH><TH>Status</TH></TR></THead>
                <TBody>
                  {rows.map((r) => {
                    const n = r.session.learnerIds?.length || 1;
                    return (
                      <TR key={r.session.id}>
                        <TD className="whitespace-nowrap">{formatDay(r.session.startUtc)}</TD>
                        <TD><Link href={`/tutor/sessions/${r.session.id}`} className="font-medium text-brand-700 hover:underline">{r.session.kind === 'demo' ? 'Demo' : r.session.code}</Link></TD>
                        <TD className="whitespace-nowrap">{r.who}{r.session.kind === 'group' ? ' (group)' : ''}</TD>
                        <TD>{r.session.minutes} min</TD>
                        <TD className="whitespace-nowrap">{r.grossInr === 0 ? 'Free' : `${money(r.session.rateInr ?? 0)}${r.session.kind === 'group' ? ` ×${n}` : ''}`}</TD>
                        <TD className="text-right font-medium">{money(r.netInr)}</TD>
                        <TD><Pill tone={STATUS[r.status].tone}>{STATUS[r.status].label}{r.paidOn ? ` ${formatDay(r.paidOn).split(', ')[1]}` : ''}</Pill></TD>
                      </TR>
                    );
                  })}
                </TBody>
              </Table>
            </Card>
          ) : <EmptyState title="No transactions match" description="Clear the filters to see every session." action={<Link href="/tutor/earnings/transactions" className={buttonVariants({ variant: 'secondary' })}>Clear filters</Link>} />}
          <p className="text-xs text-subtle">Platform fee {fee}% is deducted per session. Payouts every Monday for sessions with a submitted report.</p>
        </>
      ) : payouts.length ? (
        <Card className="overflow-x-auto">
          <Table>
            <THead><TR><TH>Paid on</TH><TH>Sessions</TH><TH className="text-right">Amount</TH><TH>To</TH></TR></THead>
            <TBody>{payouts.map((p) => <TR key={p.id}><TD>{formatDate(p.paidOn)}</TD><TD>{p.sessionIds.length}</TD><TD className="text-right font-medium">{money(p.amountInr)}</TD><TD className="text-muted">Bank account ••••4821</TD></TR>)}</TBody>
          </Table>
        </Card>
      ) : <EmptyState title="No payouts yet" description="Your first payout arrives the Monday after your first paid session report." />}
    </div>
  );
}
