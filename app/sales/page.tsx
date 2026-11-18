import Link from 'next/link';
import { AlarmClock, IndianRupee, Trophy, UserPlus, Wallet } from 'lucide-react';
import { BarChart } from '@/components/charts';
import { Avatar, Badge, Card, CardBody, CardHeader, PageHeader, StatTile, Table, TBody, TD, TH, THead, TR, buttonVariants } from '@/components/ui';
import { fmtDateTime, fmtTime, StatusBadge } from '@/components/crm/ui';
import {
  SOURCE_LABEL, STATUS_LABEL, followUpState, funnel, getLead, getPackage, isOpen, leaderboard, listFollowUps, listLeadsRaw, listPayments,
  monthIst, prevMonth, repName, revenueByMonth, sourceStats, todayIst,
} from '@/lib/data/crm';
import { DEMO_NOW_ISO } from '@/lib/demo-clock';
import { formatInr, formatPercent } from '@/lib/format';
import { currentPersona } from '@/lib/session';

export default async function SalesDashboard() {
  const me = await currentPersona();
  const leads = listLeadsRaw();
  const now = Date.parse(DEMO_NOW_ISO);
  const month = monthIst(DEMO_NOW_ISO);
  const rev = revenueByMonth(month);
  const revPrev = revenueByMonth(prevMonth(month));
  const new30 = leads.filter((l) => now - Date.parse(l.createdUtc) <= 30 * 86_400_000).length;
  const prev30 = leads.filter((l) => {
    const age = now - Date.parse(l.createdUtc);
    return age > 30 * 86_400_000 && age <= 60 * 86_400_000;
  }).length;
  const open = leads.filter((l) => isOpen(l.status));
  const pipeline = open.reduce((s, l) => s + l.valueInr, 0);
  const steps = funnel(leads);
  const maxReached = steps[0]!.reached;
  const sources = sourceStats(leads);
  const board = leaderboard(month);

  const fus = listFollowUps().filter((f) => f.status === 'open');
  const today = fus.filter((f) => followUpState(f) === 'today').sort((a, b) => a.dueUtc.localeCompare(b.dueUtc));
  const overdue = fus.filter((f) => followUpState(f) === 'overdue');

  const months = [prevMonth(prevMonth(prevMonth(month))), prevMonth(prevMonth(month)), prevMonth(month), month];
  const monthLabel = (m: string) => new Date(`${m}-01T00:00:00Z`).toLocaleDateString('en-IN', { month: 'short' });
  const revenueSeries = months.map((m) => ({ x: monthLabel(m) + (m === month ? ' (MTD)' : ''), revenue: Math.round(revenueByMonth(m).amountInr / 1000) }));

  const awaiting = listPayments()
    .filter((p) => p.status === 'pending')
    .map((p) => ({ p, lead: getLead(p.leadId)! }))
    .filter((x) => x.lead && (x.lead.status === 'proposal_sent' || x.lead.status === 'negotiation'))
    .sort((a, b) => b.p.createdUtc.localeCompare(a.p.createdUtc))
    .slice(0, 6);

  return (
    <>
      <PageHeader
        eyebrow="Sales"
        title={`Good morning, ${me?.name.split(' ')[0] ?? 'team'}`}
        description={`Admissions funnel as of ${fmtDateTime(DEMO_NOW_ISO)} IST · last 90 days plus earlier won families`}
        actions={<>
          <Link href="/sales/leads" className={buttonVariants({ variant: 'secondary', size: 'sm' })}>All leads</Link>
          <Link href="/sales/follow-ups" className={buttonVariants({ size: 'sm' })}>Today’s follow-ups</Link>
        </>}
      />

      <section className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-5">
        <StatTile label="New leads, 30 days" value={new30} icon={<UserPlus />} delta={prev30 ? { value: `${Math.round(((new30 - prev30) / prev30) * 100)}% vs prior 30`, direction: new30 >= prev30 ? 'up' : 'down' } : undefined} />
        <StatTile label="Revenue this month" value={formatInr(rev.amountInr)} icon={<IndianRupee />} hint={`${formatInr(rev.totalInr)} incl. GST · last month ${formatInr(revPrev.amountInr)}`} />
        <StatTile label="Deals won this month" value={rev.count} icon={<Trophy />} hint={`${revPrev.count} last month`} />
        <StatTile label="Open pipeline" value={formatInr(pipeline)} icon={<Wallet />} hint={`${open.length} open deals`} />
        <StatTile label="Follow-ups due today" value={today.length} icon={<AlarmClock />} hint={overdue.length ? `${overdue.length} overdue` : 'Nothing overdue'} className="col-span-2 lg:col-span-1" />
      </section>

      <div className="mb-6 grid gap-6 lg:grid-cols-5">
        <Card className="min-w-0 lg:col-span-3">
          <CardHeader title="Funnel by stage" description="Leads that reached each stage, with the conversion rate from the stage before." />
          <CardBody>
            <ol className="space-y-2.5" data-testid="funnel">
              {steps.map((s) => (
                <li key={s.status} className="grid grid-cols-[7.5rem_1fr_4.5rem] items-center gap-3 text-sm sm:grid-cols-[9rem_1fr_5rem]">
                  <span className="truncate text-muted">{STATUS_LABEL[s.status]}</span>
                  <div className="relative h-7 rounded-md bg-surface-muted">
                    <div className="absolute inset-y-0 left-0 flex items-center rounded-md bg-brand-500/85 px-2 text-xs font-semibold text-white" style={{ width: `${Math.max(8, (s.reached / maxReached) * 100)}%` }}>
                      {s.reached}
                    </div>
                  </div>
                  <span className="text-right text-xs tabular-nums text-muted">{s.rateFromPrev !== undefined ? formatPercent(s.rateFromPrev) : '—'}</span>
                </li>
              ))}
            </ol>
            <p className="mt-4 text-xs text-subtle">
              Lead to won: <span className="font-medium text-ink" data-testid="win-rate">{formatPercent(steps.at(-1)!.reached / maxReached)}</span> ·
              Negotiation is optional, so Closed won is measured against Proposal sent.
            </p>
          </CardBody>
        </Card>
        <Card className="min-w-0 lg:col-span-2">
          <CardHeader title="Revenue by month" description="Paid, before GST, in ₹ thousands." />
          <CardBody><BarChart data={revenueSeries} series={[{ key: 'revenue', label: 'Revenue (₹ k)' }]} height={240} /></CardBody>
        </Card>
      </div>

      <div className="mb-6 grid gap-6 lg:grid-cols-2">
        <Card className="min-w-0">
          <CardHeader title="Leads by source" description="All leads and how many became paying families." />
          <CardBody>
            <BarChart data={sources.map((s) => ({ x: SOURCE_LABEL[s.source].replace('School partnership', 'Schools'), leads: s.leads, won: s.won }))} series={[{ key: 'leads', label: 'Leads' }, { key: 'won', label: 'Won' }]} height={240} />
          </CardBody>
        </Card>
        <Card className="min-w-0">
          <CardHeader title="Rep leaderboard" description="This month, revenue before GST." />
          <Table>
            <THead><TR><TH>Rep</TH><TH className="text-right">Won</TH><TH className="text-right">Revenue</TH><TH className="hidden text-right sm:table-cell">Target</TH><TH className="hidden text-right md:table-cell">Open</TH></TR></THead>
            <TBody>{board.map((b, i) => (
              <TR key={b.member.id}>
                <TD><div className="flex items-center gap-2"><span className="w-4 text-xs text-subtle">{i + 1}</span><Avatar name={b.member.name} size="sm" /><div className="min-w-0"><p className="truncate font-medium text-ink">{b.member.name}</p><p className="truncate text-xs text-muted">{b.member.title}</p></div></div></TD>
                <TD className="text-right tabular-nums">{b.won}</TD>
                <TD className="text-right tabular-nums">{formatInr(b.revenueInr)}</TD>
                <TD className="hidden text-right sm:table-cell"><Badge tone={b.targetPct >= 1 ? 'success' : b.targetPct >= 0.5 ? 'warning' : 'neutral'}>{formatPercent(b.targetPct)}</Badge></TD>
                <TD className="hidden text-right tabular-nums md:table-cell">{b.open}</TD>
              </TR>
            ))}</TBody>
          </Table>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card className="min-w-0">
          <CardHeader title="Follow-ups due today" description={overdue.length ? `${overdue.length} more are overdue.` : undefined} action={<Link className={buttonVariants({ variant: 'link', size: 'sm' })} href="/sales/follow-ups">Open list</Link>} />
          <CardBody className="pt-3">
            <ul className="divide-y divide-line">{today.slice(0, 8).map((f) => {
              const l = getLead(f.leadId)!;
              return (
                <li key={f.id} className="flex items-center gap-3 py-2.5">
                  <span className="w-16 shrink-0 text-xs tabular-nums text-muted">{fmtTime(f.dueUtc)}</span>
                  <div className="min-w-0 flex-1">
                    <Link href={`/sales/leads/${l.id}`} className="block truncate text-sm font-medium text-ink hover:text-brand-700">{f.title}: {l.parentName}</Link>
                    <p className="truncate text-xs text-muted">{l.studentName} · {repName(f.ownerId)}</p>
                  </div>
                  <StatusBadge status={l.status} />
                </li>
              );
            })}</ul>
            {!today.length && <p className="text-sm text-muted">Nothing due today.</p>}
          </CardBody>
        </Card>
        <Card className="min-w-0">
          <CardHeader title="Proposals awaiting payment" description="Payment links sent, not paid yet." />
          <CardBody className="pt-3">
            <ul className="divide-y divide-line">{awaiting.map(({ p, lead }) => (
              <li key={p.id} className="flex items-center gap-3 py-2.5">
                <Avatar name={lead.parentName} size="sm" />
                <div className="min-w-0 flex-1">
                  <Link href={`/sales/leads/${lead.id}`} className="block truncate text-sm font-medium text-ink hover:text-brand-700">{lead.parentName} for {lead.studentName}</Link>
                  <p className="truncate text-xs text-muted">{getPackage(p.packageId)?.name} · sent {fmtDateTime(p.createdUtc)}</p>
                </div>
                <span className="text-sm font-medium tabular-nums text-ink">{formatInr(p.totalInr)}</span>
              </li>
            ))}</ul>
            {!awaiting.length && <p className="text-sm text-muted">No proposals waiting.</p>}
          </CardBody>
        </Card>
      </div>
      <p className="mt-6 text-xs text-subtle">Demo data. Dates in IST, today {todayIst()}. Prices are sample values.</p>
    </>
  );
}
