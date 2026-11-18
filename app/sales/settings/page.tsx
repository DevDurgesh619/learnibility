import { Avatar, Badge, Card, CardBody, CardHeader, PageHeader, Table, TBody, TD, TH, THead, TR } from '@/components/ui';
import { INTEREST_LABEL, gstFor, listPackages, listRules, listTeam, listTemplates } from '@/lib/data/crm';
import { formatInr } from '@/lib/format';

export default async function SettingsPage() {
  return (
    <>
      <PageHeader eyebrow="Sales" title="Settings" description="Plans and prices, message templates, follow-up rules and the team. Read only in the demo." />
      <Card className="mb-6">
        <CardHeader title="Plans and prices" description="Sample prices from data/crm/packages.json. GST 18% is added at checkout." />
        <Table>
          <THead><TR><TH>Package</TH><TH className="hidden md:table-cell">For</TH><TH className="hidden sm:table-cell">Term</TH><TH className="text-right">Price</TH><TH className="hidden sm:table-cell text-right">With GST</TH></TR></THead>
          <TBody>{listPackages().map((p) => (
            <TR key={p.id}>
              <TD><p className="font-medium text-ink">{p.name}</p><p className="text-xs text-muted">{p.blurb}</p></TD>
              <TD className="hidden md:table-cell"><div className="flex flex-wrap gap-1">{p.interests.map((i) => <Badge key={i}>{INTEREST_LABEL[i]}</Badge>)}</div></TD>
              <TD className="hidden sm:table-cell text-sm">{p.months ? `${p.months} month${p.months > 1 ? 's' : ''}` : 'One-off'}</TD>
              <TD className="text-right tabular-nums">{formatInr(p.priceInr)}</TD>
              <TD className="hidden sm:table-cell text-right tabular-nums">{formatInr(p.priceInr + gstFor(p.priceInr))}</TD>
            </TR>
          ))}</TBody>
        </Table>
      </Card>
      <div className="mb-6 grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader title="Follow-up rules" description="Shown and simulated; nothing is really sent." />
          <CardBody className="pt-3"><ul className="divide-y divide-line">{listRules().map((r) => (
            <li key={r.id} className="py-3 text-sm"><div className="flex items-center justify-between gap-2"><p className="font-medium text-ink">{r.name}</p><Badge tone={r.channel === 'whatsapp' ? 'success' : 'info'}>{r.channel === 'whatsapp' ? 'WhatsApp' : r.channel === 'call' ? 'Call task' : 'Email'}</Badge></div><p className="text-muted">When: {r.trigger}. Then: {r.action}.</p></li>
          ))}</ul></CardBody>
        </Card>
        <Card>
          <CardHeader title="Team" />
          <CardBody className="pt-3"><ul className="divide-y divide-line">{listTeam().map((m) => (
            <li key={m.id} className="flex items-center gap-3 py-3"><Avatar name={m.name} size="sm" /><div className="min-w-0 flex-1"><p className="text-sm font-medium text-ink">{m.name}</p><p className="text-xs text-muted">{m.title}</p></div><span className="text-xs text-muted">Target {formatInr(m.monthlyTargetInr)}/mo</span></li>
          ))}</ul></CardBody>
        </Card>
      </div>
      <Card>
        <CardHeader title="Message templates" description="Placeholders in braces are filled from the lead." />
        <CardBody className="pt-3"><ul className="grid gap-3 md:grid-cols-2">{listTemplates().map((t) => (
          <li key={t.id} className="rounded-lg border border-line p-3 text-sm"><div className="mb-1 flex items-center justify-between"><p className="font-medium text-ink">{t.name}</p><Badge tone={t.channel === 'whatsapp' ? 'success' : 'info'}>{t.channel === 'whatsapp' ? 'WhatsApp' : 'Email'}</Badge></div><p className="text-muted">{t.body}</p></li>
        ))}</ul></CardBody>
      </Card>
    </>
  );
}
