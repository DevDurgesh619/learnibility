import Link from 'next/link';
import { Card } from '@/components/ui/card';
import { applicationsBundle, firstName, fitInputs, listUniversities, uniMap } from '@/components/applications/data';
import { UniversityExplorer } from '@/components/applications/explorer';
import { fitAll } from '@/components/applications/fit';
import { requireSubscriber } from '@/components/applications/guard';
import { daysUntil, fmtDate, STATUS_LABEL } from '@/components/applications/logic';
import { uniRow } from '@/components/applications/rows';
import { SupportHeader } from '@/components/applications/support-header';
import { DaysLeft, FitBadge, UniMark } from '@/components/applications/ui';
import { ActionButton } from '@/components/applications/action-button';
import { addToBoard } from '@/lib/actions/applications';
import { DEMO_NOW } from '@/lib/demo-clock';
import { cn } from '@/lib/utils';

export const metadata = { title: 'Universities · Application Support · Learnibility' };

const STREAM_FIELDS: Record<string, string[]> = {
  commerce: ['business', 'accounting', 'commerce', 'economics', 'finance', 'management'],
  science: ['computer-science', 'mechanical-engineering', 'electrical-engineering', 'data-science'],
  humanities: ['law', 'politics', 'psychology', 'economics', 'liberal-arts'],
};

export default async function Page({ searchParams }: { searchParams: Promise<{ view?: string }> }) {
  const { view = 'search' } = await searchParams;
  const { persona, ctx, counsellorName } = await requireSubscriber();
  const b = applicationsBundle(persona.id);
  const unis = listUniversities();
  const map = uniMap();
  const onBoard = b.applications.map((a) => a.universityId);
  const boardFields = b.applications.map((a) => map.get(a.universityId)?.programmes.find((p) => p.id === a.programmeId)?.field).filter((x): x is string => !!x);
  const fields = boardFields.length ? [...new Set(boardFields)] : STREAM_FIELDS[ctx.student?.stream ?? ''] ?? [];
  const { profile, countries } = fitInputs(persona.id);
  const rows = unis.map((u) => uniRow(u, new Set(onBoard), fields));
  const allFields = [...new Set(unis.flatMap((u) => u.programmes.map((p) => p.field)))].sort();
  const fit = fitAll(unis, profile, { fields, countries });
  const recs = [...fit.reach.slice(-2), ...fit.target.slice(0, 4), ...fit.safe.slice(0, 2)].filter((r) => !onBoard.includes(r.universityId));
  const cFirst = firstName(ctx.counsellorId);
  const milestones = b.applications.flatMap((a) => {
    const u = map.get(a.universityId);
    const route = u?.applicationRoutes.find((r) => r.type === a.routeType);
    const out: { date: string; label: string; app: typeof a; kind: 'deadline' | 'decision' }[] = [{ date: a.deadline, label: `${u?.shortName}: submit`, app: a, kind: 'deadline' }];
    if (route?.decisionBy) out.push({ date: route.decisionBy, label: `${u?.shortName}: decision expected`, app: a, kind: 'decision' });
    return out;
  }).sort((x, y) => x.date.localeCompare(y.date));

  const sub = [
    { key: 'search', label: 'Search' },
    { key: 'recommended', label: `${cFirst}'s recommendations · ${recs.length}` },
    { key: 'milestones', label: 'Decision milestones' },
  ];

  return (
    <>
      <SupportHeader active="universities" counsellorName={counsellorName} />
      <div className="mb-5 flex flex-wrap gap-2">
        {sub.map((s) => (
          <Link key={s.key} href={`?view=${s.key}`} className={cn('rounded-full border px-3 py-1 text-sm font-medium', view === s.key ? 'border-ink bg-ink text-white' : 'border-line bg-surface text-ink hover:bg-surface-muted')}>{s.label}</Link>
        ))}
      </div>

      {view === 'search' && (
        <UniversityExplorer rows={rows} fields={allFields} detailBase="/student/universities" mode="paid" initialFilters={{ country: countries }} shortlist={{ action: addToBoard, onBoard }} />
      )}

      {view === 'recommended' && (
        <>
          <p className="mb-3 text-sm text-muted">Balanced list for your course and countries, from the same fit rule as your results. {cFirst} goes through it with you in your next meeting.</p>
          {recs.length === 0 ? <p className="rounded-lg border border-dashed border-line p-4 text-sm text-muted">Everything we would recommend is already on your board.</p> : (
            <Card className="divide-y divide-line">
              {recs.map((r) => (
                <div key={r.universityId} className="flex flex-col gap-3 p-4 sm:flex-row sm:items-center sm:justify-between">
                  <div className="flex min-w-0 items-center gap-3">
                    <UniMark uni={r.university} size="sm" />
                    <div className="min-w-0">
                      <p className="font-medium text-ink"><Link href={`/student/universities/${r.universityId}`} className="hover:underline">{r.university.shortName}</Link> · <span className="font-normal text-muted">{r.programme.name}</span></p>
                      <p className="text-xs text-muted">{r.chancePct}% · {r.reason}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2"><FitBadge band={r.band} /><ActionButton size="sm" action={addToBoard.bind(null, r.universityId, r.programmeId)}>Shortlist</ActionButton></div>
                </div>
              ))}
            </Card>
          )}
        </>
      )}

      {view === 'milestones' && (
        milestones.length === 0 ? <p className="rounded-lg border border-dashed border-line p-4 text-sm text-muted">Shortlist universities to see their deadlines and decision dates here.</p> : (
          <ol className="relative ml-3 border-l border-line">
            {milestones.map((m, i) => {
              const d = daysUntil(m.date, DEMO_NOW);
              return (
                <li key={i} className="mb-5 ml-5">
                  <span className={cn('absolute -left-[7px] mt-1.5 size-3.5 rounded-full border-2 border-surface', d < 0 ? 'bg-subtle' : m.kind === 'decision' ? 'bg-success-600' : d < 14 ? 'bg-danger-600' : 'bg-brand-600')} />
                  <p className="text-xs text-subtle">{fmtDate(m.date)}</p>
                  <p className="font-medium text-ink"><Link href={`/student/applications/${m.app.id}`} className="hover:underline">{m.label}</Link></p>
                  <p className="flex items-center gap-2 text-xs text-muted">{STATUS_LABEL[m.app.status]}{d >= 0 && <DaysLeft days={d} />}</p>
                </li>
              );
            })}
          </ol>
        )
      )}
    </>
  );
}
