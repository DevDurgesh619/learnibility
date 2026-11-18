import Link from 'next/link';
import { CircleAlert, CircleCheck, Clock3, IndianRupee } from 'lucide-react';
import { Card, PageHeader, StatTile, Table, TBody, TD, TH, THead, TR } from '@/components/ui';
import { fmtDateTime, PaymentBadge } from '@/components/crm/ui';
import { getLead, getPackage, listPayments, monthIst, revenueByMonth } from '@/lib/data/crm';
import { DEMO_NOW_ISO } from '@/lib/demo-clock';
import { formatInr } from '@/lib/format';
import { cn } from '@/lib/utils';

type SP = Promise<Record<string, string | string[] | undefined>>;

export default async function PaymentsPage({ searchParams }: { searchParams: SP }) {
  const sp = await searchParams;
  const status = typeof sp.status === 'string' ? sp.status : 'all';
  const all = listPayments().sort((a, b) => (b.paidUtc ?? b.failedUtc ?? b.createdUtc).localeCompare(a.paidUtc ?? a.failedUtc ?? a.createdUtc));
  const rows = all.filter((p) => status === 'all' || p.status === status);
  const rev = revenueByMonth(monthIst(DEMO_NOW_ISO));
  const pending = all.filter((p) => p.status === 'pending');
  const failed = all.filter((p) => p.status === 'failed');
  return (
    <>
      <PageHeader eyebrow="Sales" title="Payments" description="Payment links, invoices with GST, and receipts. Demo only: no money moves." />
      <section className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatTile label="Collected this month" value={formatInr(rev.totalInr)} hint="Incl. 18% GST" icon={<IndianRupee />} />
        <StatTile label="Paid this month" value={rev.count} icon={<CircleCheck />} />
        <StatTile label="Links pending" value={pending.length} hint={formatInr(pending.reduce((s, p) => s + p.totalInr, 0))} icon={<Clock3 />} />
        <StatTile label="Failed attempts" value={failed.length} icon={<CircleAlert />} />
      </section>
      <nav className="mb-4 flex gap-2">{['all', 'pending', 'paid', 'failed'].map((s) => (
        <Link key={s} href={`/sales/payments?status=${s}`} className={cn('rounded-full border px-3 py-1.5 text-sm capitalize', status === s ? 'border-brand-600 bg-brand-600 text-white' : 'border-line bg-surface text-muted')}>{s}</Link>
      ))}</nav>
      <Card>
        <Table>
          <THead><TR><TH>Family</TH><TH className="hidden md:table-cell">Package</TH><TH className="text-right">Total</TH><TH>Status</TH><TH className="hidden sm:table-cell">Date</TH><TH className="hidden lg:table-cell">Invoice</TH></TR></THead>
          <TBody>{rows.map((p) => {
            const l = getLead(p.leadId)!;
            return (
              <TR key={p.id} data-testid="payment-row">
                <TD><Link href={`/sales/leads/${l.id}`} className="font-medium text-ink hover:text-brand-700">{l.parentName}</Link><p className="text-xs text-muted">{l.studentName}</p></TD>
                <TD className="hidden md:table-cell text-sm">{getPackage(p.packageId)?.name}</TD>
                <TD className="text-right tabular-nums">{formatInr(p.totalInr)}<p className="text-xs text-muted">GST {formatInr(p.gstInr)}</p></TD>
                <TD><PaymentBadge status={p.status} /></TD>
                <TD className="hidden sm:table-cell text-sm tabular-nums">{fmtDateTime(p.paidUtc ?? p.failedUtc ?? p.createdUtc)}</TD>
                <TD className="hidden lg:table-cell text-sm">{p.invoiceNo ? <Link href={`/sales/payments/${p.id}`} className="text-brand-700 hover:underline">{p.invoiceNo}</Link> : <span className="truncate text-xs text-muted">{p.status === 'pending' ? 'Link sent' : '—'}</span>}</TD>
              </TR>
            );
          })}</TBody>
        </Table>
      </Card>
    </>
  );
}
