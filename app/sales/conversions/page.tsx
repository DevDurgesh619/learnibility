import Link from 'next/link';
import { Rocket } from 'lucide-react';
import { Badge, Card, CardHeader, EmptyState, PageHeader, StatTile, Table, TBody, TD, TH, THead, TR } from '@/components/ui';
import { Submit } from '@/components/crm/submit';
import { fmtDateTime } from '@/components/crm/ui';
import { convertToPlatform, openInPlatform } from '@/lib/actions/crm';
import { getLead, getPackage, getPayment, listConversions, listPayments, repName } from '@/lib/data/crm';
import { getAdult } from '@/lib/data';
import { getPersona } from '@/lib/data/personas';

export default async function ConversionsPage() {
  const convs = listConversions().map((c) => ({ c, lead: getLead(c.leadId)!, pay: listPayments().find((p) => p.leadId === c.leadId && p.status === 'paid') }));
  const waiting = convs.filter((x) => x.c.status === 'waiting').sort((a, b) => b.c.wonUtc.localeCompare(a.c.wonUtc));
  const done = convs.filter((x) => x.c.status === 'handed_over').sort((a, b) => (b.c.handedOverUtc ?? '').localeCompare(a.c.handedOverUtc ?? ''));
  return (
    <>
      <PageHeader eyebrow="Sales" title="Conversions" description="Paid families move to the platform: learner and parent accounts, counsellor, subscription and invoice." />
      <section className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-3">
        <StatTile label="Waiting for hand-over" value={waiting.length} />
        <StatTile label="Handed over" value={done.length} />
        <StatTile label="Demo families on the platform" value={done.filter((x) => x.lead.personaFamily).length} className="col-span-2 lg:col-span-1" />
      </section>
      <Card className="mb-6">
        <CardHeader title="Waiting for hand-over" description="Payment recorded; convert to create the platform accounts." />
        {waiting.length ? (
          <ul className="divide-y divide-line">{waiting.map(({ c, lead, pay }) => (
            <li key={c.id} className="flex flex-wrap items-center gap-3 px-5 py-4" data-testid="conversion-waiting">
              <div className="min-w-0 flex-1">
                <Link href={`/sales/leads/${lead.id}`} className="font-medium text-ink hover:text-brand-700">{lead.parentName} for {lead.studentName}</Link>
                <p className="text-xs text-muted">Won {fmtDateTime(c.wonUtc)} by {repName(lead.ownerId)} · {getPackage(pay?.packageId)?.name} · counsellor {getAdult(c.counsellorId)?.name}</p>
              </div>
              <form action={convertToPlatform}><input type="hidden" name="leadId" value={lead.id} /><Submit size="sm" pendingText="Converting…"><Rocket /> Convert to platform</Submit></form>
            </li>
          ))}</ul>
        ) : <div className="p-5"><EmptyState className="border-0 py-4" title="All caught up" description="Every paid family is on the platform." /></div>}
      </Card>
      <Card>
        <CardHeader title="Handed over" />
        <Table>
          <THead><TR><TH>Family</TH><TH className="hidden md:table-cell">Plan</TH><TH className="hidden sm:table-cell">Handed over</TH><TH className="hidden lg:table-cell">Counsellor</TH><TH><span className="sr-only">Open</span></TH></TR></THead>
          <TBody>{done.map(({ c, lead, pay }) => (
            <TR key={c.id}>
              <TD><Link href={`/sales/leads/${lead.id}`} className="font-medium text-ink hover:text-brand-700">{lead.parentName}</Link><p className="text-xs text-muted">{lead.studentName}{lead.personaFamily && <Badge tone="brand" className="ml-2">Demo family</Badge>}</p></TD>
              <TD className="hidden md:table-cell text-sm">{getPackage(pay?.packageId ?? getPayment(c.leadId)?.packageId)?.name}</TD>
              <TD className="hidden sm:table-cell text-sm tabular-nums">{fmtDateTime(c.handedOverUtc)}</TD>
              <TD className="hidden lg:table-cell text-sm">{getAdult(c.counsellorId)?.name}</TD>
              <TD className="text-right">{c.learnerIds.filter((id) => getPersona(id)).slice(0, 2).map((id) => (
                <form key={id} action={openInPlatform} className="inline-block"><input type="hidden" name="learnerId" value={id} /><Submit size="sm" variant="secondary">Open {getPersona(id)!.name.split(' ')[0]}</Submit></form>
              ))}</TD>
            </TR>
          ))}</TBody>
        </Table>
      </Card>
    </>
  );
}
