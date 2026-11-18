import Link from 'next/link';
import { FileUp, Search } from 'lucide-react';
import { Badge, Card, EmptyState, PageHeader, Table, TBody, TD, TH, THead, TR, buttonVariants } from '@/components/ui';
import { Submit } from '@/components/crm/submit';
import { fmtDate, inputCls, relDays, ScorePill, StatusBadge } from '@/components/crm/ui';
import { bulkAssign, importCsv } from '@/lib/actions/crm';
import { INTEREST_LABEL, INTERESTS, LEAD_STATUSES, SOURCE_LABEL, SOURCES, STATUS_LABEL, listLeads, listTeam, repName } from '@/lib/data/crm';
import { DEMO_NOW_ISO } from '@/lib/demo-clock';
import { formatInr } from '@/lib/format';

type SP = Promise<Record<string, string | string[] | undefined>>;
const PAGE = 25;

export default async function LeadsPage({ searchParams }: { searchParams: SP }) {
  const sp = await searchParams;
  const get = (k: string) => (typeof sp[k] === 'string' ? (sp[k] as string) : '');
  const f = { q: get('q'), status: get('status') || 'open', source: get('source'), owner: get('owner'), interest: get('interest') };
  const all = listLeads(f);
  const page = Math.max(1, Number(get('page')) || 1);
  const rows = all.slice((page - 1) * PAGE, page * PAGE);
  const pages = Math.ceil(all.length / PAGE);
  const team = listTeam();
  const qs = (p: number) => `?${new URLSearchParams({ ...Object.fromEntries(Object.entries(f).filter(([, v]) => v)), page: String(p) })}`;
  const imported = get('imported');

  return (
    <>
      <PageHeader
        eyebrow="Sales"
        title="Leads"
        description={`${all.length} leads match. Website, ads, social, referrals, schools and webinars all land here.`}
        actions={<form action={importCsv}><Submit variant="secondary" size="sm" pendingText="Importing…"><FileUp /> Import CSV</Submit></form>}
      />
      {imported && (
        <div className="mb-4 rounded-lg border border-success-600/20 bg-success-50 px-4 py-3 text-sm text-success-700">
          {imported === '0' ? 'That file was already imported.' : `Imported ${imported} leads from edufair-signups-nov.csv. Welcome messages went out automatically.`}
        </div>
      )}

      <Card className="mb-4 p-4">
        <form className="grid grid-cols-2 gap-3 md:grid-cols-6" method="get">
          <label className="relative col-span-2">
            <Search className="pointer-events-none absolute left-3 top-2.5 size-4 text-subtle" aria-hidden />
            <input name="q" defaultValue={f.q} placeholder="Name, phone, city, campaign" className={`${inputCls} pl-9`} aria-label="Search leads" />
          </label>
          <select name="status" defaultValue={f.status} className={inputCls} aria-label="Status">
            <option value="open">Open deals</option>
            <option value="won">Won and converted</option>
            <option value="all">All statuses</option>
            {LEAD_STATUSES.map((s) => <option key={s} value={s}>{STATUS_LABEL[s]}</option>)}
          </select>
          <select name="source" defaultValue={f.source || 'all'} className={inputCls} aria-label="Source">
            <option value="all">All sources</option>
            {SOURCES.map((s) => <option key={s} value={s}>{SOURCE_LABEL[s]}</option>)}
          </select>
          <select name="owner" defaultValue={f.owner || 'all'} className={inputCls} aria-label="Owner">
            <option value="all">All owners</option>
            {team.map((m) => <option key={m.id} value={m.id}>{m.name}</option>)}
          </select>
          <div className="flex gap-2">
            <select name="interest" defaultValue={f.interest || 'all'} className={inputCls} aria-label="Interest">
              <option value="all">All interests</option>
              {INTERESTS.map((s) => <option key={s} value={s}>{INTEREST_LABEL[s]}</option>)}
            </select>
            <button className={buttonVariants({ size: 'sm', className: 'h-9' })} type="submit">Filter</button>
          </div>
        </form>
      </Card>

      {rows.length ? (
        <form action={bulkAssign}>
          <Card>
            <div className="flex flex-wrap items-center gap-2 border-b border-line px-4 py-3 text-sm">
              <span className="text-muted">Bulk assign selected to</span>
              <select name="owner" className={`${inputCls} w-auto`} aria-label="Assign to" defaultValue="">
                <option value="" disabled>Choose a rep</option>
                {team.map((m) => <option key={m.id} value={m.id}>{m.name}</option>)}
              </select>
              <Submit size="sm" variant="secondary" pendingText="Assigning…">Assign</Submit>
            </div>
            <Table>
              <THead>
                <TR>
                  <TH className="w-8"><span className="sr-only">Select</span></TH>
                  <TH>Lead</TH>
                  <TH className="hidden md:table-cell">Interest</TH>
                  <TH className="hidden lg:table-cell">Source</TH>
                  <TH>Status</TH>
                  <TH className="hidden sm:table-cell text-right">Score</TH>
                  <TH className="hidden xl:table-cell text-right">Value</TH>
                  <TH className="hidden lg:table-cell">Owner</TH>
                  <TH className="hidden md:table-cell">Last contact</TH>
                </TR>
              </THead>
              <TBody>{rows.map((l) => (
                <TR key={l.id} data-testid="lead-row">
                  <TD className="pr-0"><input type="checkbox" name="ids" value={l.id} aria-label={`Select ${l.studentName}`} className="size-4 rounded border-line" /></TD>
                  <TD>
                    <Link href={`/sales/leads/${l.id}`} className="font-medium text-ink hover:text-brand-700">{l.parentName}</Link>
                    <p className="text-xs text-muted">{l.studentName} · Class {l.grade} {l.board.toUpperCase()} · {l.city}</p>
                    {l.personaFamily && <Badge tone="brand" className="mt-1">Demo family</Badge>}
                  </TD>
                  <TD className="hidden md:table-cell">{INTEREST_LABEL[l.interest]}</TD>
                  <TD className="hidden lg:table-cell"><p>{SOURCE_LABEL[l.source]}</p><p className="max-w-48 truncate text-xs text-muted">{l.campaign}</p></TD>
                  <TD><StatusBadge status={l.status} /></TD>
                  <TD className="hidden sm:table-cell text-right"><ScorePill score={l.score} /></TD>
                  <TD className="hidden xl:table-cell text-right tabular-nums">{l.valueInr ? formatInr(l.valueInr) : '—'}</TD>
                  <TD className="hidden lg:table-cell text-sm">{repName(l.ownerId)}</TD>
                  <TD className="hidden md:table-cell text-xs text-muted">{l.lastContactedUtc ? relDays(l.lastContactedUtc, DEMO_NOW_ISO) : `Created ${fmtDate(l.createdUtc)}`}</TD>
                </TR>
              ))}</TBody>
            </Table>
            {pages > 1 && (
              <div className="flex items-center justify-between border-t border-line px-4 py-3 text-sm text-muted">
                <span>Page {page} of {pages}</span>
                <div className="flex gap-2">
                  {page > 1 && <Link className={buttonVariants({ variant: 'secondary', size: 'sm' })} href={qs(page - 1)}>Previous</Link>}
                  {page < pages && <Link className={buttonVariants({ variant: 'secondary', size: 'sm' })} href={qs(page + 1)}>Next</Link>}
                </div>
              </div>
            )}
          </Card>
        </form>
      ) : (
        <EmptyState title="No leads match" description="Try another status or clear the search." action={<Link href="/sales/leads?status=all" className={buttonVariants({ variant: 'secondary', size: 'sm' })}>Show all leads</Link>} />
      )}
    </>
  );
}
