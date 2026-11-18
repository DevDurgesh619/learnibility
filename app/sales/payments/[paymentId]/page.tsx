import Link from 'next/link';
import { notFound } from 'next/navigation';
import { ArrowLeft } from 'lucide-react';
import { Card, CardBody, PageHeader } from '@/components/ui';
import { Logo } from '@/components/shell/logo';
import { fmtDateYear, PaymentBadge } from '@/components/crm/ui';
import { getLead, getPackage, getPayment } from '@/lib/data/crm';
import { formatInr } from '@/lib/format';

/** Invoice and receipt for one payment (dummy company details). */
export default async function InvoicePage({ params }: { params: Promise<{ paymentId: string }> }) {
  const { paymentId } = await params;
  const p = getPayment(paymentId);
  if (!p) notFound();
  const lead = getLead(p.leadId)!;
  const pkg = getPackage(p.packageId)!;
  const half = Math.round(p.gstInr / 2);
  return (
    <>
      <Link href={`/sales/leads/${lead.id}`} className="mb-3 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ArrowLeft className="size-4" /> {lead.parentName}</Link>
      <PageHeader eyebrow="Sales · Payments" title={p.invoiceNo ? `Tax invoice ${p.invoiceNo}` : 'Payment link'} actions={<PaymentBadge status={p.status} />} />
      <Card className="max-w-3xl">
        <CardBody className="space-y-6">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div><Logo /><p className="mt-2 text-xs text-muted">Learnibility Learning Pvt. Ltd. (demo)<br />GSTIN 29AAACL0000D1Z5 (sample) · Bengaluru, Karnataka</p></div>
            <div className="text-right text-sm"><p className="text-muted">Invoice date</p><p className="font-medium text-ink">{fmtDateYear(p.paidUtc ?? p.createdUtc)}</p>{p.receiptNo && <p className="mt-1 text-xs text-muted">Receipt {p.receiptNo}</p>}</div>
          </div>
          <div className="text-sm"><p className="text-muted">Billed to</p><p className="font-medium text-ink">{lead.parentName}</p><p className="text-muted">{lead.city} · {lead.phone} · {lead.email}</p><p className="text-muted">For: {lead.studentName}, Class {lead.grade} {lead.board.toUpperCase()}</p></div>
          <table className="w-full text-sm">
            <thead><tr className="border-b border-line text-left text-xs uppercase tracking-wide text-subtle"><th className="py-2">Item</th><th className="py-2 text-right">Amount</th></tr></thead>
            <tbody className="divide-y divide-line">
              <tr><td className="py-2">{pkg.name}<p className="text-xs text-muted">{pkg.blurb} SAC 999293.</p></td><td className="py-2 text-right tabular-nums">{formatInr(p.amountInr)}</td></tr>
              <tr><td className="py-2 text-muted">CGST 9%</td><td className="py-2 text-right tabular-nums">{formatInr(half)}</td></tr>
              <tr><td className="py-2 text-muted">SGST 9%</td><td className="py-2 text-right tabular-nums">{formatInr(p.gstInr - half)}</td></tr>
              <tr className="font-semibold"><td className="py-2">Total</td><td className="py-2 text-right tabular-nums">{formatInr(p.totalInr)}</td></tr>
            </tbody>
          </table>
          <p className="text-xs text-subtle">{p.status === 'paid' ? `Paid by ${p.method} on ${fmtDateYear(p.paidUtc)}.` : `Payment link: ${p.link}`} Sample prices for the demo.</p>
        </CardBody>
      </Card>
    </>
  );
}
