import Link from 'next/link';
import { notFound } from 'next/navigation';
import { BarChart } from '@/components/charts';
import { Card, CardBody, CardHeader } from '@/components/ui';
import { CareerTabs, FitPill, SkillChip } from '@/components/career/career-tabs';
import { careerById, careerMatches, DEMAND_LABEL, lpaRange, skillName, studentCtx, universityById } from '@/components/student/load';
import { LinkButton } from '@/components/student/link-button';
import { formatInr } from '@/lib/format';

export const metadata = { title: 'Career detail · Learnibility' };

/** PDF 9c: demand, salary, entry level, skills, job market by city, best universities. */
export default async function CareerDetail({ params }: { params: Promise<{ careerId: string }> }) {
  const { careerId } = await params;
  const c = await careerById(careerId);
  if (!c) notFound();
  const ctx = await studentCtx();
  const fit = (await careerMatches(ctx)).find((m) => m.careerId === c.id);
  const india = c.pathways.find((p) => p.region === 'india') ?? c.pathways[0];
  const unis = (await Promise.all(c.pathways.flatMap((p) => p.universityIds).slice(0, 12).map(universityById))).filter((u) => !!u).slice(0, 5);

  return (
    <>
      <Link href="/student/career/search" className="mb-2 inline-block text-sm text-muted hover:text-ink">‹ Results</Link>
      <CareerTabs active="fit" />
      <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h1 className="flex flex-wrap items-center gap-2 text-2xl font-semibold tracking-tight text-ink">{c.title}{fit && <FitPill score={fit.score} />}</h1>
          <p className="mt-1 max-w-2xl text-sm text-muted">{c.summary}</p>
          {fit && fit.reasons.length > 0 && <p className="mt-1 text-xs text-subtle">Why this fits: {fit.reasons.join(' · ')}</p>}
        </div>
        <LinkButton href={`/student/career/${c.id}/gap`}>See my skill gap</LinkButton>
      </div>

      <div className="mb-4 grid gap-3 sm:grid-cols-3">
        <Card className="p-4"><p className="text-sm text-muted">Demand</p><p className="text-lg font-semibold text-ink">{DEMAND_LABEL[c.demand]} · +{c.growthPct}% / yr</p></Card>
        <Card className="p-4"><p className="text-sm text-muted">Starting salary</p><p className="text-lg font-semibold text-ink">{lpaRange(c.salaryInr.entryLow, c.salaryInr.entryHigh)}</p><p className="text-xs text-subtle">Mid-career {formatInr(c.salaryInr.mid)} a year</p></Card>
        <Card className="p-4"><p className="text-sm text-muted">Entry level</p><p className="text-lg font-semibold text-ink">{india?.degree ?? '—'}</p><p className="text-xs text-subtle">{india ? `${india.yearsToEntry} years after class 12` : ''}</p></Card>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="flex flex-col gap-4">
          <Card>
            <CardHeader title="Skills" description="Core skills first" />
            <CardBody className="flex flex-wrap gap-2">
              {[...c.skills].sort((a, b) => (a.importance === b.importance ? 0 : a.importance === 'core' ? -1 : 1)).map((s) => (
                <SkillChip key={s.skillId} tone={s.importance === 'core' ? 'solid' : 'outline'}>{skillName(s.skillId)}</SkillChip>
              ))}
            </CardBody>
          </Card>
          <Card>
            <CardHeader title="Job market by location" description="Share of openings in India" />
            <CardBody><BarChart data={c.topCities.map((t) => ({ x: t.city, share: t.sharePct / 100 }))} series={[{ key: 'share', label: 'Openings' }]} format="percent" height={220} /></CardBody>
          </Card>
          <Card>
            <CardHeader title="A day in the job" />
            <CardBody className="pt-2 text-sm text-muted">{c.dayInLife}</CardBody>
          </Card>
        </div>
        <div className="flex flex-col gap-4">
          <Card>
            <CardHeader title="Best universities to study this" />
            <CardBody className="pt-2">
              <ul className="divide-y divide-line text-sm">
                {unis.map((u) => <li key={u.id} className="py-2 text-ink">{u.name}<span className="text-muted"> · {u.city}</span></li>)}
              </ul>
              <Link href="/student/universities" className="mt-2 inline-block text-sm font-medium text-brand-700 hover:text-brand-800">Check fit in University Fit →</Link>
            </CardBody>
          </Card>
          <Card>
            <CardHeader title="Ways in" />
            <CardBody className="pt-2">
              <ul className="divide-y divide-line text-sm">
                {c.pathways.map((p) => (
                  <li key={p.id} className="py-2">
                    <p className="font-medium text-ink">{p.label}</p>
                    <p className="text-muted">{p.yearsToEntry} yrs · typical cost {formatInr(p.costInr.typical)}{p.examIds.length ? ` · exams: ${p.examIds.join(', ').toUpperCase()}` : ''}</p>
                  </li>
                ))}
              </ul>
            </CardBody>
          </Card>
          <p className="text-xs text-subtle">Sources: {c.sources.map((s, i) => <span key={s.url}>{i > 0 && '; '}<a href={s.url} target="_blank" rel="noreferrer" className="underline">{s.label}</a> (as of {s.asOf})</span>)}</p>
        </div>
      </div>
    </>
  );
}
