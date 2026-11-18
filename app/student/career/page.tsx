import Link from 'next/link';
import { Search, Sparkles } from 'lucide-react';
import { Card, CardBody, EmptyState, Progress } from '@/components/ui';
import { CareerTabs, FitPill, SkillChip } from '@/components/career/career-tabs';
import {
  careerMatches, careers, DEMAND_LABEL, lpa, lpaRange, skillName, studentCtx, universities,
} from '@/components/student/load';
import { LinkButton } from '@/components/student/link-button';
import { cn } from '@/lib/utils';

export const metadata = { title: 'Career · Learnibility' };

const field = 'h-10 w-full min-w-0 rounded-lg border border-line bg-surface px-3 text-sm text-ink placeholder:text-subtle focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-100';

export default async function CareerPage({ searchParams }: { searchParams: Promise<{ tab?: string; uni?: string; role?: string; city?: string }> }) {
  const sp = await searchParams;
  if (sp.tab === 'insights') return <JobInsights uni={sp.uni} role={sp.role} city={sp.city} />;
  const ctx = await studentCtx();
  const top = careerMatches(ctx, 3);
  const allCareers = careers();

  return (
    <>
      <h1 className="mb-4 text-2xl font-semibold tracking-tight text-ink">Career</h1>
      <CareerTabs active="fit" />
      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Explore careers</h2>
            <p className="mt-1 text-sm text-muted">Search by skills, filter and browse every role ({allCareers.length} careers).</p>
            <form action="/student/career/search" className="mt-4 flex flex-col gap-2 sm:flex-row">
              <input name="q" placeholder="Type your skills: Python, SQL, accounting…" className={cn(field, 'flex-1')} />
              <div className="flex gap-2">
                <button className="inline-flex h-10 items-center gap-2 rounded-lg bg-brand-600 px-4 text-sm font-medium text-white hover:bg-brand-700"><Search className="size-4" />Search</button>
                <LinkButton href="/student/career/search" variant="secondary">Browse all</LinkButton>
              </div>
            </form>
          </CardBody>
        </Card>
        <Card className="border-success-600/30 bg-success-50/40">
          <CardBody>
            <h2 className="flex items-center gap-2 text-base font-semibold text-ink"><Sparkles className="size-4 text-success-700" />Made for you</h2>
            <p className="mt-1 text-sm text-muted">Smart matches from your profile, tests and interests.{ctx.firstVisit ? ' Take your first assessment to sharpen them.' : ''}</p>
            <ol className="mt-3 divide-y divide-line">
              {top.map((m, i) => (
                <li key={m.careerId} className="flex items-center justify-between gap-3 py-2 text-sm">
                  <Link href={`/student/career/${m.careerId}`} className="text-ink hover:text-brand-700">{i + 1}. {m.title}</Link>
                  <FitPill score={m.score} />
                </li>
              ))}
            </ol>
            <LinkButton href="/student/career/search?mine=1" variant="secondary" size="sm" className="mt-3 border-success-600/40 text-success-700">View my matches</LinkButton>
          </CardBody>
        </Card>
      </div>
    </>
  );
}

/** PDF 9e (university only) and 9f (university × role × location). */
async function JobInsights({ uni, role, city }: { uni?: string; role?: string; city?: string }) {
  const ctx = await studentCtx();
  const allCareers = careers();
  const withOutcomes = universities().filter((u) => u.outcomes).sort((a, b) => a.name.localeCompare(b.name));
  const u = withOutcomes.find((x) => x.id === uni);
  const c = allCareers.find((x) => x.id === role);
  const cities = [...new Set(allCareers.flatMap((x) => x.topCities.map((t) => t.city)))].sort();
  const fit = c ? careerMatches(ctx).find((m) => m.careerId === c.id) : undefined;
  const cityShare = c && city ? c.topCities.find((t) => t.city === city)?.sharePct ?? 0 : undefined;
  const any = u || c;

  return (
    <>
      <h1 className="mb-4 text-2xl font-semibold tracking-tight text-ink">Career</h1>
      <CareerTabs active="insights" />
      <p className="mb-3 text-sm text-muted">Combine a university, a role and a city to see real outcomes. Pick one or all three.</p>
      <form className="mb-6 grid grid-cols-1 gap-2 sm:grid-cols-[1fr_1fr_1fr_auto]">
        <input type="hidden" name="tab" value="insights" />
        <select name="uni" defaultValue={uni ?? ''} className={field} aria-label="University">
          <option value="">University: any</option>
          {withOutcomes.map((x) => <option key={x.id} value={x.id}>{x.name}</option>)}
        </select>
        <select name="role" defaultValue={role ?? ''} className={field} aria-label="Job role">
          <option value="">Job role: any</option>
          {[...allCareers].sort((a, b) => a.title.localeCompare(b.title)).map((x) => <option key={x.id} value={x.id}>{x.title}</option>)}
        </select>
        <select name="city" defaultValue={city ?? ''} className={field} aria-label="Location">
          <option value="">Location: any</option>
          {cities.map((x) => <option key={x}>{x}</option>)}
        </select>
        <button className="h-10 rounded-lg bg-brand-600 px-5 text-sm font-medium text-white hover:bg-brand-700">Search</button>
      </form>

      {!any && <EmptyState icon={<Search />} title="Pick a university, a role or a city" description="For example IIT Bombay × Data Analyst × Bengaluru." />}

      {u?.outcomes && (
        <Card className="mb-4">
          <CardBody>
            <div className="flex items-center justify-between"><h2 className="text-lg font-semibold text-ink">{u.name}</h2><span className="text-xs text-subtle">university outcomes</span></div>
            <div className="mt-4 grid gap-6 sm:grid-cols-2">
              <div>
                <p className="text-sm text-muted">Employment rate</p>
                <div className="mt-1 flex items-center gap-3"><Progress value={u.outcomes.employmentRatePct.value / 100} /><span className="text-sm font-semibold text-ink">{u.outcomes.employmentRatePct.value}%</span></div>
                <p className="mt-1 text-xs text-subtle">{u.outcomes.employmentRatePct.note}</p>
              </div>
              <div>
                <p className="text-sm text-muted">Median early-career salary</p>
                <p className="text-2xl font-semibold text-ink">{lpa(u.outcomes.medianStartingSalaryInr.value)}</p>
                <p className="mt-1 text-xs text-subtle">Top recruiters: {u.outcomes.topRecruiters.slice(0, 4).join(', ')}</p>
              </div>
            </div>
            <p className="mt-4 text-xs text-subtle">Source: <a className="underline" href={u.outcomes.employmentRatePct.sourceUrl} target="_blank" rel="noreferrer">{new URL(u.outcomes.employmentRatePct.sourceUrl).hostname}</a> · as of {u.outcomes.employmentRatePct.asOf}{u.outcomes.employmentRatePct.verified ? '' : ' · estimate'}</p>
          </CardBody>
        </Card>
      )}

      {c && (
        <>
          <div className="mb-4 grid grid-cols-2 gap-3 lg:grid-cols-4">
            <Card className="p-4"><p className="text-sm text-muted">Path fit score</p><p className="text-2xl font-semibold text-ink">{fit ? Math.round(fit.score) : '—'}<span className="text-sm text-subtle">/100</span></p></Card>
            <Card className="p-4"><p className="text-sm text-muted">Feasibility</p><p className="text-2xl font-semibold text-ink">{fit ? Math.round((fit.parts.feasibility / 15) * 100) : '—'}<span className="text-sm text-subtle">/100</span></p></Card>
            <Card className="p-4"><p className="text-sm text-muted">Expected starting salary</p><p className="text-2xl font-semibold text-ink">{lpaRange(c.salaryInr.entryLow, c.salaryInr.entryHigh)}</p></Card>
            <Card className="p-4"><p className="text-sm text-muted">Employment rate</p><p className="text-2xl font-semibold text-ink">{u?.outcomes ? `${u.outcomes.employmentRatePct.value}%` : '—'}</p>{!u && <p className="text-xs text-subtle">Pick a university</p>}</Card>
          </div>
          <div className="mb-4 grid gap-3 lg:grid-cols-2">
            <Card className="p-4">
              <p className="text-sm font-medium text-ink">{c.title} openings by city</p>
              <ul className="mt-3 flex flex-col gap-2">
                {c.topCities.map((t) => (
                  <li key={t.city} className={cn('grid grid-cols-[7rem_1fr_3rem] items-center gap-2 text-sm', t.city === city && 'font-semibold')}>
                    <span className="truncate text-muted">{t.city}</span><Progress value={t.sharePct / 100} tone={t.city === city ? 'success' : 'brand'} /><span className="text-right text-ink">{t.sharePct}%</span>
                  </li>
                ))}
              </ul>
              {city && cityShare === 0 && <p className="mt-2 text-xs text-subtle">{city} is not among the main hiring cities for this role.</p>}
            </Card>
            <Card className="p-4">
              <p className="text-sm font-medium text-ink">Demand for the role</p>
              <div className="mt-2 flex items-center gap-3"><Progress value={{ very_high: 1, high: 0.8, medium: 0.55, low: 0.3 }[c.demand]} /><span className="text-sm font-semibold text-ink">{DEMAND_LABEL[c.demand]}</span></div>
              <p className="mt-2 text-sm text-muted">Openings growing about {c.growthPct}% a year. Recruiters: {c.topRecruiters.slice(0, 4).join(', ')}.</p>
              <p className="mt-2 text-xs text-subtle">Sources: {c.sources.map((s) => s.label).slice(0, 2).join('; ')}</p>
            </Card>
          </div>
          <Card className="border-success-600/30 bg-success-50/40 p-4">
            <p className="text-sm font-semibold text-ink">Skills to arrive with</p>
            <div className="mt-2 flex flex-wrap gap-2">{c.skills.filter((s) => s.importance === 'core').map((s) => <SkillChip key={s.skillId}>{skillName(s.skillId)}</SkillChip>)}</div>
            <Link href={`/student/career/${c.id}/gap`} className="mt-3 inline-block text-sm font-medium text-brand-700 hover:text-brand-800">See my skill gap for {c.title} →</Link>
          </Card>
        </>
      )}
      {u && !c && <p className="text-sm text-muted">Add a role and a city to see fit score, demand and expected salary.</p>}
    </>
  );
}
