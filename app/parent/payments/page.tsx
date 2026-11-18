import { CheckCircle2, CreditCard, Receipt, Video } from 'lucide-react';
import { payInvoice } from '@/lib/actions/parent';
import { ChildSwitcher } from '@/components/parent/child-switcher';
import { param, parentContext, type SearchParams } from '@/components/parent/context';
import { fmtDateTime, fmtDateYear } from '@/components/parent/format';
import { NoChild } from '@/components/parent/no-child';
import { Notice } from '@/components/parent/notice';
import { Avatar, Badge, Button, Card, CardBody, CardHeader, EmptyState, PageHeader, StatTile, Table, TBody, TD, TH, THead, TR } from '@/components/ui';
import { demoNow, getBookings, getInvoices, getPersonName, getSessions, getSubject, getTutor } from '@/lib/data';
import { formatInr } from '@/lib/format';

const SESSION_TONE = { scheduled: 'brand', completed: 'success', cancelled: 'neutral', no_show: 'danger' } as const;
const INVOICE_TONE = { paid: 'success', due: 'warning', overdue: 'danger' } as const;

export default async function ParentPayments({ searchParams }: { searchParams: SearchParams }) {
  const sp = await searchParams;
  const { parent, children, child } = await parentContext(searchParams);
  if (!child) return (<><PageHeader eyebrow="Parent" title="Sessions and payments" /><NoChild /></>);
  const s = child.student;
  const now = demoNow();
  const sessions = getSessions(s.id);
  const upcoming = sessions.filter((x) => x.status === 'scheduled' && x.startUtc >= now);
  const past = sessions.filter((x) => x.startUtc < now).reverse().slice(0, 12);
  const bookings = getBookings(s.id).filter((b) => b.status !== 'declined');
  const invoices = getInvoices(parent.id).filter((i) => i.learnerId === s.id);
  const paidId = param(sp, 'paid');
  const paid = paidId ? invoices.find((i) => i.id === paidId) : undefined;
  const ytd = invoices.filter((i) => i.status === 'paid' && (i.paidUtc ?? i.issuedUtc).slice(0, 4) === now.slice(0, 4)).reduce((a, i) => a + i.amountInr, 0);
  const due = invoices.filter((i) => i.status !== 'paid').reduce((a, i) => a + i.amountInr, 0);
  const month = invoices.filter((i) => i.issuedUtc.slice(0, 7) === now.slice(0, 7)).reduce((a, i) => a + i.amountInr, 0);

  return (
    <>
      <PageHeader eyebrow="Parent" title="Sessions and payments" description={`${s.firstName}'s tutor and counsellor sessions, bookings, invoices and receipts.`} />
      <ChildSwitcher children={children} selectedId={s.id} basePath="/parent/payments" />
      {paid && <Notice><p className="font-medium">Payment successful: {formatInr(paid.amountInr)}</p><p>Receipt {paid.id.toUpperCase()} is saved below. This is a demo, so no money moved.</p></Notice>}

      <section className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatTile label="Upcoming sessions" value={upcoming.length} icon={<Video />} />
        <StatTile label="Billed this month" value={formatInr(month)} icon={<Receipt />} />
        <StatTile label="To pay" value={formatInr(due)} icon={<CreditCard />} hint={due ? 'See invoices below' : 'Nothing due'} />
        <StatTile label="Paid this year" value={formatInr(ytd)} icon={<CheckCircle2 />} />
      </section>

      <div className="mb-6 grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader title="Upcoming sessions" />
          <CardBody className="pt-3">
            {upcoming.length ? (
              <ul className="divide-y divide-line">{upcoming.map((x) => (
                <li key={x.id} className="flex items-center gap-3 py-3 first:pt-0">
                  <Avatar name={getPersonName(x.hostId)?.name ?? x.hostId} size="sm" />
                  <div className="min-w-0 flex-1"><p className="truncate text-sm font-medium text-ink">{x.title}</p><p className="text-xs text-muted">{fmtDateTime(x.startUtc)} · {x.minutes} min · {getPersonName(x.hostId)?.name}</p></div>
                  {x.rateInr ? <span className="text-sm text-ink">{formatInr(Math.round((x.rateInr * x.minutes) / 60))}</span> : <Badge>Free</Badge>}
                </li>
              ))}</ul>
            ) : <EmptyState className="border-0 py-6" icon={<Video />} title="No upcoming sessions" description="Booked tutor demos, tutor sessions and counsellor meetings show here." />}
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Bookings" description="Tutor requests and their status" />
          <CardBody className="pt-3">
            {bookings.length ? (
              <ul className="divide-y divide-line">{bookings.map((b) => (
                <li key={b.id} className="flex items-center gap-3 py-3 first:pt-0">
                  <Avatar name={getTutor(b.tutorId)?.displayName ?? b.tutorId} size="sm" />
                  <div className="min-w-0 flex-1"><p className="truncate text-sm font-medium text-ink">{getTutor(b.tutorId)?.displayName} · {b.kind === 'demo' ? 'Free demo' : getSubject(b.subjectId ?? '')?.subject.name ?? 'Tutoring'}</p>
                    <p className="text-xs text-muted">Requested {fmtDateYear(b.requestedAt)}{b.priceInr ? ` · ${formatInr(b.priceInr)}/h` : ''}{b.parentApproval ? ` · you ${b.parentApproval.status === 'pending' ? 'have not decided yet' : b.parentApproval.status}` : ''}</p></div>
                  <Badge tone={b.status === 'active' || b.status === 'accepted' ? 'success' : b.status === 'requested' ? 'info' : 'neutral'}>{b.status}</Badge>
                </li>
              ))}</ul>
            ) : <EmptyState className="border-0 py-6" title="No bookings" description="When a tutor is booked, it appears here." />}
          </CardBody>
        </Card>
      </div>

      <Card className="mb-6">
        <CardHeader title="Invoices and receipts" />
        {invoices.length ? (
          <div className="overflow-x-auto">
            <Table className="mt-4 min-w-[640px]">
              <THead><TR><TH>Invoice</TH><TH>For</TH><TH>Issued</TH><TH>Due</TH><TH>Amount</TH><TH>Status</TH><TH /></TR></THead>
              <TBody>{invoices.map((i) => (
                <TR key={i.id} className={i.id === paidId ? 'bg-success-50' : undefined}>
                  <TD className="font-mono text-xs">{i.id.toUpperCase()}</TD>
                  <TD><p className="text-ink">{i.lines[0]?.title}</p>{i.lines.length > 1 && <p className="text-xs text-muted">+ {i.lines.length - 1} more</p>}</TD>
                  <TD>{fmtDateYear(i.issuedUtc)}</TD><TD>{fmtDateYear(i.dueDate)}</TD>
                  <TD className="font-medium text-ink">{formatInr(i.amountInr)}</TD>
                  <TD><Badge tone={INVOICE_TONE[i.status]}>{i.status === 'paid' && i.paidUtc ? `Paid ${fmtDateYear(i.paidUtc)}` : i.status}</Badge></TD>
                  <TD>{i.status !== 'paid' && (
                    <form action={payInvoice}><input type="hidden" name="learnerId" value={s.id} /><input type="hidden" name="invoiceId" value={i.id} /><Button size="sm" type="submit"><CreditCard />Pay {formatInr(i.amountInr)}</Button></form>
                  )}</TD>
                </TR>
              ))}</TBody>
            </Table>
          </div>
        ) : <CardBody><EmptyState className="border-0" icon={<Receipt />} title="No invoices yet" description="Invoices arrive after paid sessions or a plan upgrade." /></CardBody>}
      </Card>

      <Card>
        <CardHeader title="Past sessions" />
        <CardBody className="pt-3">
          {past.length ? (
            <ul className="divide-y divide-line">{past.map((x) => (
              <li key={x.id} className="flex flex-col gap-1 py-3 first:pt-0 sm:flex-row sm:items-center sm:justify-between">
                <div className="min-w-0"><p className="text-sm font-medium text-ink">{x.title}</p><p className="text-xs text-muted">{fmtDateTime(x.startUtc)} · {getPersonName(x.hostId)?.name}{x.report ? ` · ${x.report.nextFocus ? `Next: ${x.report.nextFocus}` : ''}` : ''}</p></div>
                <Badge tone={SESSION_TONE[x.status]}>{x.status.replace('_', ' ')}</Badge>
              </li>
            ))}</ul>
          ) : <p className="text-sm text-muted">No past sessions.</p>}
        </CardBody>
      </Card>
    </>
  );
}
