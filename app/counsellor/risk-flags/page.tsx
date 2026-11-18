import Link from 'next/link';
import { AlertTriangle, ShieldCheck } from 'lucide-react';
import { FilterChips } from '@/components/counsellor/filter-chips';
import { loadRiskFlags } from '@/components/counsellor/load';
import { RISK_KIND_LABEL, type RiskKind } from '@/components/counsellor/risk';
import { Avatar, Badge, Card, EmptyState, PageHeader, StatTile } from '@/components/ui';

export const dynamic = 'force-dynamic';

const SEV_TONE = { high: 'danger', medium: 'warning', low: 'neutral' } as const;
const KINDS: RiskKind[] = ['deadline', 'wellbeing', 'data', 'learning', 'request'];

export default async function RiskFlagsPage({ searchParams }: { searchParams: Promise<{ kind?: string; sev?: string }> }) {
  const sp = await searchParams;
  const { flags, names } = await loadRiskFlags();
  const kind = KINDS.find((k) => k === sp.kind);
  const list = flags.filter((f) => (!kind || f.kind === kind) && (!sp.sev || f.severity === sp.sev));
  const count = (k: RiskKind) => flags.filter((f) => f.kind === k).length;

  return (
    <>
      <PageHeader eyebrow="Counsellor" title="Risk flags" description="Deadlines under 14 days with open items, wellbeing check-ins and thin evidence, across your caseload." />
      <div className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatTile label="High" value={flags.filter((f) => f.severity === 'high').length} hint="act today" icon={<AlertTriangle />} />
        <StatTile label="Deadlines" value={count('deadline')} hint="under 14 days" />
        <StatTile label="Wellbeing" value={count('wellbeing')} hint="counsellor only" />
        <StatTile label="Data sparsity" value={count('data')} hint="thin evidence" />
      </div>
      <div className="mb-4 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <FilterChips base="/counsellor/risk-flags" param="kind" value={kind} keep={{ sev: sp.sev }} options={[{ value: '', label: 'All', count: flags.length }, ...KINDS.map((k) => ({ value: k, label: RISK_KIND_LABEL[k], count: count(k) }))]} />
        <FilterChips base="/counsellor/risk-flags" param="sev" value={sp.sev} keep={{ kind }} options={[{ value: '', label: 'Any severity' }, { value: 'high', label: 'High' }, { value: 'medium', label: 'Medium' }, { value: 'low', label: 'Low' }]} />
      </div>
      <p className="mb-4 flex items-start gap-2 text-xs text-muted"><ShieldCheck className="mt-0.5 size-3.5 shrink-0" />Wellbeing flags come from T3 screening. They are for support only and are never shown to parents, teachers or tutors verbatim.</p>
      {list.length === 0 ? <EmptyState icon={<ShieldCheck />} title="No flags here" description="Nothing in this filter needs you right now." /> : (
        <Card className="overflow-hidden">
          <ul className="divide-y divide-line">
            {list.map((f) => (
              <li key={f.id} className="flex flex-col gap-3 p-4 sm:flex-row sm:items-center">
                <div className="flex min-w-0 flex-1 items-start gap-3">
                  <Avatar name={names[f.learnerId] ?? f.learnerId} size="sm" />
                  <div className="min-w-0">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="font-medium text-ink">{names[f.learnerId] ?? f.learnerId}</span>
                      <Badge tone={SEV_TONE[f.severity]}>{f.severity}</Badge>
                      <Badge>{RISK_KIND_LABEL[f.kind]}</Badge>
                    </div>
                    <p className="mt-1 text-sm text-ink">{f.title}</p>
                    <p className="text-xs text-muted">{f.detail}</p>
                  </div>
                </div>
                <Link href={f.href ?? `/counsellor/student-360?student=${f.learnerId}`} className="shrink-0 text-sm font-medium text-brand-700 hover:underline">
                  {f.kind === 'deadline' ? 'Open applications' : f.kind === 'request' ? 'Review request' : 'Open Student 360'}
                </Link>
              </li>
            ))}
          </ul>
        </Card>
      )}
    </>
  );
}
