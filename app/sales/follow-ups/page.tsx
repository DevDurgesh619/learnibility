import Link from 'next/link';
import { MessageCircle, Phone, Mail } from 'lucide-react';
import { Badge, Card, EmptyState, PageHeader, Table, TBody, TD, TH, THead, TR } from '@/components/ui';
import { Submit } from '@/components/crm/submit';
import { fmtDateTime, StatusBadge } from '@/components/crm/ui';
import { completeFollowUp } from '@/lib/actions/crm';
import { followUpState, getLead, getRule, listFollowUps, listRules, repName, type FollowUpState } from '@/lib/data/crm';
import { cn } from '@/lib/utils';

type SP = Promise<Record<string, string | string[] | undefined>>;
const TABS: { key: FollowUpState | 'due'; label: string }[] = [
  { key: 'due', label: 'Due today' }, { key: 'overdue', label: 'Overdue' }, { key: 'upcoming', label: 'Upcoming' }, { key: 'done', label: 'Done' },
];
const CH = { whatsapp: MessageCircle, call: Phone, email: Mail } as const;

export default async function FollowUpsPage({ searchParams }: { searchParams: SP }) {
  const sp = await searchParams;
  const tab = (typeof sp.tab === 'string' ? sp.tab : 'due') as FollowUpState | 'due';
  const rule = typeof sp.rule === 'string' ? sp.rule : '';
  const all = listFollowUps().map((f) => ({ f, st: followUpState(f) }));
  const count = (k: string) => all.filter((x) => (k === 'due' ? x.st === 'today' : x.st === k)).length;
  const rows = all
    .filter((x) => (tab === 'due' ? x.st === 'today' : x.st === tab) && (!rule || x.f.ruleId === rule))
    .sort((a, b) => (tab === 'done' ? (b.f.doneUtc ?? '').localeCompare(a.f.doneUtc ?? '') : tab === 'upcoming' ? a.f.dueUtc.localeCompare(b.f.dueUtc) : a.f.dueUtc.localeCompare(b.f.dueUtc)))
    .slice(0, 60);

  return (
    <>
      <PageHeader eyebrow="Sales" title="Follow-ups" description="Created by the follow-up rules or by reps. Automated WhatsApp steps are simulated, not sent." />
      <nav className="mb-4 flex flex-wrap gap-2" aria-label="Follow-up views">
        {TABS.map((t) => (
          <Link key={t.key} href={`/sales/follow-ups?tab=${t.key}${rule ? `&rule=${rule}` : ''}`} className={cn('rounded-full border px-3 py-1.5 text-sm', tab === t.key ? 'border-brand-600 bg-brand-600 text-white' : 'border-line bg-surface text-muted hover:text-ink')}>
            {t.label} <span className="ml-1 tabular-nums opacity-80">{count(t.key)}</span>
          </Link>
        ))}
        <span className="mx-1 hidden h-8 w-px bg-line sm:block" />
        <Link href={`/sales/follow-ups?tab=${tab}`} className={cn('rounded-full px-3 py-1.5 text-sm', !rule ? 'bg-surface-muted text-ink' : 'text-muted')}>All rules</Link>
        {listRules().filter((r) => r.id !== 'r_welcome').map((r) => (
          <Link key={r.id} href={`/sales/follow-ups?tab=${tab}&rule=${r.id}`} className={cn('rounded-full px-3 py-1.5 text-sm', rule === r.id ? 'bg-surface-muted text-ink' : 'text-muted hover:text-ink')}>{r.name}</Link>
        ))}
      </nav>
      {rows.length ? (
        <Card>
          <Table>
            <THead><TR><TH>Follow-up</TH><TH>Lead</TH><TH className="hidden md:table-cell">Rule</TH><TH className="hidden sm:table-cell">{tab === 'done' ? 'Done' : 'Due'}</TH><TH className="hidden lg:table-cell">Owner</TH><TH><span className="sr-only">Action</span></TH></TR></THead>
            <TBody>{rows.map(({ f, st }) => {
              const l = getLead(f.leadId)!;
              const Icon = CH[f.channel];
              return (
                <TR key={f.id} data-testid="followup-row">
                  <TD><div className="flex items-center gap-2"><Icon className="size-4 shrink-0 text-muted" aria-hidden /><span className="font-medium text-ink">{f.title}</span></div>
                    {st === 'overdue' && <Badge tone="danger" className="mt-1">Overdue</Badge>}</TD>
                  <TD><Link href={`/sales/leads/${l.id}`} className="font-medium text-ink hover:text-brand-700">{l.parentName}</Link><div className="mt-0.5 flex items-center gap-2 text-xs text-muted"><span>{l.studentName}</span><StatusBadge status={l.status} /></div></TD>
                  <TD className="hidden md:table-cell text-sm text-muted">{getRule(f.ruleId)?.name}</TD>
                  <TD className="hidden sm:table-cell text-sm tabular-nums">{fmtDateTime(tab === 'done' ? f.doneUtc : f.dueUtc)}</TD>
                  <TD className="hidden lg:table-cell text-sm">{repName(f.ownerId)}</TD>
                  <TD className="text-right">{f.status === 'open' && (
                    <form action={completeFollowUp}><input type="hidden" name="id" value={f.id} /><input type="hidden" name="leadId" value={l.id} /><Submit size="sm" variant="secondary">{f.channel === 'whatsapp' ? 'Send' : 'Done'}</Submit></form>
                  )}</TD>
                </TR>
              );
            })}</TBody>
          </Table>
        </Card>
      ) : <EmptyState title="Nothing here" description="No follow-ups in this view." />}
    </>
  );
}
