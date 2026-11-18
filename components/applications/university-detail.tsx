import Link from 'next/link';
import { ChevronLeft } from 'lucide-react';
import { TrendChart } from '@/components/charts';
import { Badge } from '@/components/ui/badge';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { Table, TBody, TD, TH, THead, TR } from '@/components/ui/table';
import { toggleShortlist, addToBoard } from '@/lib/actions/applications';
import { DEMO_NOW } from '@/lib/demo-clock';
import { formatInr } from '@/lib/format';
import type { ApplicationType, University } from '@/lib/types';
import { cn } from '@/lib/utils';
import { ActionButton } from './action-button';
import { SHOW_COSTS } from './config';
import { fieldLabel } from './fields';
import { computeFit, mainRoute, type FitProfile } from './fit';
import { daysUntil, fmtDate } from './logic';
import { COUNTRY_NAME, DaysLeft, FitBadge, LinkTabs, money, SourceLine, SourcedFact, UniMark } from './ui';

export const ROUTE_LABEL: Record<ApplicationType, string> = {
  early_decision: 'Early Decision (binding)', early_decision_2: 'Early Decision II (binding)', early_action: 'Early Action',
  restrictive_early_action: 'Restrictive Early Action', regular: 'Regular Decision', rolling: 'Rolling admission',
  ucas_oxbridge_medicine: 'UCAS 15 October deadline', ucas_equal_consideration: 'UCAS equal consideration', ouac: 'OUAC (Ontario)',
  direct: 'Direct application', josaa: 'JoSAA counselling', cuet: 'CUET', institutional_exam: 'Entrance exam', merit: 'Merit list',
};

const PLATFORM_LABEL: Record<string, string> = {
  common_app: 'Common App', uc_application: 'UC Application', coalition: 'Coalition', ucas: 'UCAS', ouac: 'OUAC', university_portal: 'University portal',
  josaa: 'JoSAA', cuet_samarth: 'CUET (Samarth)', csab: 'CSAB',
};

type Tab = 'overview' | 'courses' | 'admissions' | 'costs';

export function UniversityDetail({
  uni, tab, base, mode, saved, onBoard, fitProfile, backHref, backLabel,
}: {
  uni: University;
  tab: Tab;
  base: string;
  mode: 'free' | 'paid' | 'readonly';
  saved: boolean;
  onBoard: Set<string>;
  fitProfile?: FitProfile;
  backHref: string;
  backLabel: string;
}) {
  const route = mainRoute(uni);
  const req = route?.requirements;
  const days = route ? daysUntil(route.deadline.value, DEMO_NOW) : null;
  const best = fitProfile && Object.keys(fitProfile).length
    ? uni.programmes.map((p) => computeFit(uni, p, fitProfile)).sort((a, b) => b.chancePct - a.chancePct)[0]
    : undefined;

  return (
    <>
      <Link href={backHref} className="mb-3 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" />{backLabel}</Link>
      <div className="mb-5 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="flex min-w-0 items-start gap-3">
          <UniMark uni={uni} size="lg" />
          <div className="min-w-0">
            <h1 className="text-2xl font-semibold tracking-tight text-ink">{uni.name}</h1>
            <p className="mt-1 text-sm text-muted">
              {uni.city}, {COUNTRY_NAME[uni.country]} · {uni.type === 'private' ? 'Private' : 'Public'} ·{' '}
              {uni.qsWorldRank.value ? <SourcedFact fact={uni.qsWorldRank}>{`#${uni.qsWorldRank.value} QS world`}</SourcedFact> : uni.nirfRank?.value ? <SourcedFact fact={uni.nirfRank}>{`#${uni.nirfRank.value} NIRF`}</SourcedFact> : 'Unranked'}
              {' · '}Admission rate <SourcedFact fact={uni.acceptanceRatePct}>{uni.acceptanceRatePct.value === null ? 'not published' : `${uni.acceptanceRatePct.value}%`}</SourcedFact>
            </p>
            {best && <p className="mt-2 flex items-center gap-2 text-sm"><FitBadge band={best.band} /><span className="text-muted">{best.chancePct}% · {best.reason}</span></p>}
          </div>
        </div>
        <div className="flex shrink-0 flex-wrap gap-2">
          {mode === 'free' && (
            <>
              <Link href="/student/universities/best-fit" className={cn(buttonVariants({ variant: 'secondary' }), 'border-success-600/40 text-success-700')}>Check my fit</Link>
              <ActionButton variant={saved ? 'secondary' : 'primary'} action={toggleShortlist.bind(null, uni.id, best?.programmeId ?? uni.programmes[0]?.id, best?.band)}>{saved ? 'Saved ✓' : 'Save'}</ActionButton>
            </>
          )}
          {mode === 'paid' && (
            onBoard.has(uni.id)
              ? <Link href="/student/applications/board" className={buttonVariants({ variant: 'secondary' })}>On your board ✓</Link>
              : <ActionButton action={addToBoard.bind(null, uni.id, best?.programmeId ?? uni.programmes[0]!.id)}>Shortlist</ActionButton>
          )}
        </div>
      </div>

      <LinkTabs
        active={tab}
        tabs={(['overview', 'courses', 'admissions', ...(SHOW_COSTS ? ['costs'] : [])] as Tab[]).map((t) => ({ key: t, label: t[0]!.toUpperCase() + t.slice(1), href: `${base}?tab=${t}` }))}
      />

      {tab === 'overview' && (
        <div className="grid grid-cols-[minmax(0,1fr)] gap-6 lg:grid-cols-[minmax(0,1fr)_360px]">
          <div className="space-y-6">
            <div className={cn('grid grid-cols-2 gap-3', SHOW_COSTS ? 'sm:grid-cols-4' : 'sm:grid-cols-3')}>
              <Card className="p-4">
                <p className="text-xs text-muted">Deadline</p>
                <p className="mt-1 font-semibold text-ink">{route ? fmtDate(route.deadline.value) : '—'}</p>
                <p className="text-xs text-subtle">{route ? ROUTE_LABEL[route.type] : ''}</p>
                {days !== null && <DaysLeft days={days} />}
              </Card>
              <Card className="p-4">
                <p className="text-xs text-muted">{req?.satMid50 ? 'SAT middle 50%' : 'Typical offer'}</p>
                <p className="mt-1 font-semibold text-ink">{req?.satMid50 ? `${req.satMid50[0]}-${req.satMid50[1]}` : req?.typicalOffer?.split(';')[0] ?? (req?.minBoardPercent ? `${req.minBoardPercent}% boards` : '—')}</p>
                <p className="text-xs text-subtle">{req?.testPolicy === 'optional' ? 'Test-optional' : req?.testPolicy === 'required' ? 'Test required' : req?.testPolicy === 'blind' ? 'Test-blind' : 'No SAT'}</p>
              </Card>
              {SHOW_COSTS && <Card className="p-4">
                <p className="text-xs text-muted">Tuition</p>
                <p className="mt-1 font-semibold text-ink"><SourcedFact fact={uni.tuition}>{`${money(uni.tuition.value.amount, uni.tuition.value.currency)} / yr`}</SourcedFact></p>
                <p className="text-xs text-subtle">{formatInr(uni.tuitionInrPerYear)}</p>
              </Card>}
              <Card className="p-4">
                <p className="text-xs text-muted">Intl students</p>
                <p className="mt-1 font-semibold text-ink"><SourcedFact fact={uni.intlStudentPct}>{uni.intlStudentPct.value === null ? '—' : `${uni.intlStudentPct.value}%`}</SourcedFact></p>
                <p className="text-xs text-subtle">Founded {uni.founded}</p>
              </Card>
            </div>
            <Card>
              <CardHeader title="Known for" />
              <CardBody className="flex flex-wrap gap-2 pt-3">{uni.strengths.map((s) => <Badge key={s} tone="brand">{s}</Badge>)}</CardBody>
            </Card>
            {uni.outcomes && (
              <Card>
                <CardHeader title="Graduate outcomes" />
                <CardBody className="grid gap-4 pt-3 sm:grid-cols-3">
                  <div><p className="text-xs text-muted">Employed or studying</p><p className="text-lg font-semibold">{uni.outcomes.employmentRatePct.value}%</p><SourceLine fact={uni.outcomes.employmentRatePct} /></div>
                  <div><p className="text-xs text-muted">Median starting salary</p><p className="text-lg font-semibold">{formatInr(uni.outcomes.medianStartingSalaryInr.value)}</p><SourceLine fact={uni.outcomes.medianStartingSalaryInr} /></div>
                  <div><p className="text-xs text-muted">Top recruiters</p><p className="text-sm text-ink">{uni.outcomes.topRecruiters.slice(0, 4).join(', ')}</p></div>
                </CardBody>
              </Card>
            )}
          </div>
          <Card>
            <CardHeader title="Admit rate trend" description="Share of applicants admitted, by entry year" />
            <CardBody>
              {uni.admitTrend?.length ? (
                <TrendChart
                  data={uni.admitTrend.map((p) => ({ x: String(p.year), rate: p.ratePct / 100 }))}
                  series={[{ key: 'rate', label: 'Admit rate' }]}
                  format="percent"
                  height={220}
                  domain={[0, Math.min(1, (Math.max(...uni.admitTrend.map((p) => p.ratePct)) / 100) * 1.6 + 0.01)]}
                />
              ) : <p className="text-sm text-muted">No published trend.</p>}
              <SourceLine fact={uni.acceptanceRatePct} />
            </CardBody>
          </Card>
        </div>
      )}

      {tab === 'courses' && (
        <Card>
          <Table>
            <THead><TR><TH>Programme</TH><TH>Field</TH><TH>Length</TH><TH>Typical offer or cut-off</TH><TH>Entry exams</TH>{fitProfile && <TH>Your fit</TH>}</TR></THead>
            <TBody>
              {uni.programmes.map((p) => {
                const f = fitProfile && Object.keys(fitProfile).length ? computeFit(uni, p, fitProfile) : undefined;
                return (
                  <TR key={p.id}>
                    <TD className="font-medium text-ink">{p.name}</TD>
                    <TD>{fieldLabel(p.field)}</TD>
                    <TD>{p.durationYears} yrs</TD>
                    <TD className="max-w-xs">{p.cutoff ? <SourcedFact fact={p.cutoff} /> : p.typicalOffer ?? req?.typicalOffer ?? '—'}</TD>
                    <TD>{p.entryExamIds.length ? p.entryExamIds.join(', ').toUpperCase() : '—'}</TD>
                    {fitProfile && <TD>{f ? <span className="inline-flex items-center gap-2"><FitBadge band={f.band} /><span className="text-xs text-muted">{f.chancePct}%</span></span> : '—'}</TD>}
                  </TR>
                );
              })}
            </TBody>
          </Table>
        </Card>
      )}

      {tab === 'admissions' && (
        <div className="space-y-4">
          {uni.applicationRoutes.map((r, i) => (
            <Card key={i}>
              <CardHeader
                title={ROUTE_LABEL[r.type]}
                description={`${PLATFORM_LABEL[r.platform] ?? r.platform}${r.binding ? ' · binding' : ''}${r.decisionBy ? ` · decisions by ${fmtDate(r.decisionBy)}` : ''}`}
                action={<DaysLeft days={daysUntil(r.deadline.value, DEMO_NOW)} />}
              />
              <CardBody className="grid gap-4 pt-3 sm:grid-cols-2">
                <div className="space-y-2 text-sm">
                  <p><span className="text-muted">Deadline:</span> <SourcedFact fact={r.deadline}>{fmtDate(r.deadline.value)}</SourcedFact></p>
                  {r.requirements.typicalOffer && <p><span className="text-muted">Typical offer:</span> {r.requirements.typicalOffer}</p>}
                  {r.requirements.minBoardPercent && <p><span className="text-muted">Board marks:</span> {r.requirements.minBoardPercent}% or more</p>}
                  {r.requirements.satMid50 && <p><span className="text-muted">SAT middle 50%:</span> {r.requirements.satMid50.join('-')} ({r.requirements.testPolicy})</p>}
                  {(r.requirements.ielts || r.requirements.toefl) && <p><span className="text-muted">English:</span> {[r.requirements.ielts && `IELTS ${r.requirements.ielts}`, r.requirements.toefl && `TOEFL ${r.requirements.toefl}`].filter(Boolean).join(' or ')}</p>}
                  <p><span className="text-muted">Recommendations:</span> {r.requirements.recommendations || 'none'}</p>
                  {SHOW_COSTS && <p><span className="text-muted">Application fee:</span> {formatInr(r.requirements.applicationFeeInr)}</p>}
                  <SourceLine fact={r.deadline} />
                </div>
                <div className="space-y-2 text-sm">
                  {r.requirements.essays.length > 0 && (
                    <div>
                      <p className="font-medium text-ink">Essays</p>
                      <ul className="mt-1 list-disc space-y-1 pl-5 text-muted">{r.requirements.essays.map((e, j) => <li key={j}>{e.prompt} <span className="text-subtle">({e.wordLimit} words)</span></li>)}</ul>
                    </div>
                  )}
                  {r.requirements.otherItems.length > 0 && (
                    <div>
                      <p className="font-medium text-ink">Also needed</p>
                      <ul className="mt-1 list-disc space-y-1 pl-5 text-muted">{r.requirements.otherItems.map((o, j) => <li key={j}>{o}</li>)}</ul>
                    </div>
                  )}
                </div>
              </CardBody>
            </Card>
          ))}
        </div>
      )}

      {tab === 'costs' && SHOW_COSTS && (
        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader title="Cost per year" description="International undergraduate, before aid" />
            <CardBody className="space-y-3 pt-3 text-sm">
              <div className="flex justify-between"><span className="text-muted">Tuition</span><span className="font-medium"><SourcedFact fact={uni.tuition}>{`${money(uni.tuition.value.amount, uni.tuition.value.currency)} (${formatInr(uni.tuitionInrPerYear)})`}</SourcedFact></span></div>
              <div className="flex justify-between"><span className="text-muted">Living (estimate)</span><span className="font-medium">{formatInr(uni.livingInrPerYear)}</span></div>
              <div className="flex justify-between border-t border-line pt-3"><span className="text-ink">Whole degree, typical</span><span className="font-semibold">{formatInr(uni.totalCostInr)}</span></div>
              <SourceLine fact={uni.tuition} />
            </CardBody>
          </Card>
          <Card>
            <CardHeader title="Scholarships" />
            <CardBody className="pt-3">
              {uni.scholarships.length === 0 ? <p className="text-sm text-muted">No scholarships listed for international students.</p> : (
                <ul className="space-y-4">
                  {uni.scholarships.map((s) => (
                    <li key={s.name} className="text-sm">
                      <p className="font-medium text-ink">{s.name} {s.needBased && <Badge tone="info" className="ml-1">Need-based</Badge>}</p>
                      <p className="text-muted"><SourcedFact fact={s.amount} /></p>
                      <p className="text-xs text-subtle">{s.eligibility}{s.deadline ? ` · apply by ${fmtDate(s.deadline)}` : ''}</p>
                    </li>
                  ))}
                </ul>
              )}
            </CardBody>
          </Card>
        </div>
      )}
    </>
  );
}
