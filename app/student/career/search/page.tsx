import Link from 'next/link';
import { SlidersHorizontal } from 'lucide-react';
import { Card, EmptyState } from '@/components/ui';
import { CareerTabs, FitPill } from '@/components/career/career-tabs';
import { careerMatches, careers, DEMAND_LABEL, lpaRange, skillName, skills, studentCtx } from '@/components/student/load';
import { LinkButton } from '@/components/student/link-button';
import { cn } from '@/lib/utils';

export const metadata = { title: 'Career Fit · Learnibility' };

const arr = (v: string | string[] | undefined) => (v === undefined ? [] : Array.isArray(v) ? v : [v]);

/** PDF 9b: search and results on one screen, filters on the left (skills grouped by category, cluster, demand). */
export default async function CareerSearch({ searchParams }: { searchParams: Promise<Record<string, string | string[] | undefined>> }) {
  const sp = await searchParams;
  const q = (typeof sp.q === 'string' ? sp.q : '').trim();
  const pickedSkills = arr(sp.skill);
  const pickedClusters = arr(sp.cluster);
  const mine = sp.mine === '1';
  const ctx = await studentCtx();
  const fit = new Map(careerMatches(ctx).map((m) => [m.careerId, m]));

  const allCareers = careers();
  const allSkills = skills();
  const terms = q.toLowerCase().split(/[,\s]+/).filter((t) => t.length > 1);
  const used = new Set(allCareers.flatMap((c) => c.skills.map((s) => s.skillId)));
  const groups = [...new Set(allSkills.filter((s) => used.has(s.id) && s.kind !== 'academic').map((s) => s.category))].sort();
  const clusters = [...new Set(allCareers.map((c) => c.cluster))].sort();

  let results = allCareers.filter((c) => {
    if (pickedClusters.length && !pickedClusters.includes(c.cluster)) return false;
    if (pickedSkills.length && !pickedSkills.every((id) => c.skills.some((s) => s.skillId === id))) return false;
    if (!terms.length) return true;
    const hay = [c.title, c.cluster, c.summary, ...c.skills.map((s) => skillName(s.skillId))].join(' ').toLowerCase();
    return terms.some((t) => hay.includes(t));
  });
  results = results.sort((a, b) => (fit.get(b.id)?.score ?? 0) - (fit.get(a.id)?.score ?? 0));
  if (mine) results = results.slice(0, 10);

  const box = 'size-4 rounded border-line text-brand-600 focus:ring-brand-200';
  return (
    <>
      <Link href="/student/career" className="mb-2 inline-block text-sm text-muted hover:text-ink">‹ Career</Link>
      <CareerTabs active="fit" />
      <form className="grid gap-4 lg:grid-cols-[260px_1fr]">
        <div className="lg:col-span-2 flex gap-2">
          <input name="q" defaultValue={q} placeholder="Python, SQL, statistics…" className="h-10 flex-1 rounded-lg border border-line bg-surface px-3 text-sm focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-100" />
          <button className="h-10 rounded-lg bg-brand-600 px-5 text-sm font-medium text-white hover:bg-brand-700">Search</button>
        </div>
        <details className="group rounded-[var(--radius-card)] border border-line bg-surface p-4 lg:self-start" open>
          <summary className="flex cursor-pointer list-none items-center gap-2 text-sm font-semibold text-ink lg:pointer-events-none"><SlidersHorizontal className="size-4" />Filters</summary>
          <fieldset className="mt-3">
            <legend className="text-xs font-semibold uppercase tracking-wide text-subtle">Field</legend>
            {clusters.map((c) => (
              <label key={c} className="mt-1.5 flex items-center gap-2 text-sm text-ink"><input type="checkbox" name="cluster" value={c} defaultChecked={pickedClusters.includes(c)} className={box} />{c}</label>
            ))}
          </fieldset>
          {groups.map((g) => (
            <fieldset key={g} className="mt-4">
              <legend className="text-xs font-semibold uppercase tracking-wide text-subtle">{g} skills</legend>
              {allSkills.filter((s) => s.category === g && used.has(s.id) && s.kind !== 'academic').map((s) => (
                <label key={s.id} className="mt-1.5 flex items-center gap-2 text-sm text-ink"><input type="checkbox" name="skill" value={s.id} defaultChecked={pickedSkills.includes(s.id)} className={box} />{s.name}</label>
              ))}
            </fieldset>
          ))}
          <button className="mt-4 h-9 w-full rounded-lg border border-line text-sm font-medium text-ink hover:bg-surface-muted">Apply filters</button>
        </details>

        <section>
          <div className="mb-2 flex items-baseline justify-between border-b border-dashed border-line pb-1">
            <h2 className="text-sm font-semibold text-ink">{mine ? 'Your top matches' : 'Top matches'}</h2>
            <span className="text-xs text-subtle">{results.length} career{results.length === 1 ? '' : 's'} · ranked by your fit</span>
          </div>
          {results.length === 0 ? (
            <EmptyState title="No careers match" description="Try fewer filters or a broader skill, like “data” or “design”." action={<LinkButton href="/student/career/search" variant="secondary">Clear filters</LinkButton>} />
          ) : (
            <ol className="flex flex-col gap-3">
              {results.map((c, i) => {
                const f = fit.get(c.id);
                return (
                  <li key={c.id}>
                    <Card className="p-4">
                      <div className="flex items-start justify-between gap-3">
                        <div className="min-w-0">
                          <p className="text-sm font-semibold text-ink">{i + 1}. {c.title} {f && <FitPill score={f.score} />}</p>
                          <p className="mt-1 text-sm text-muted">Salary {lpaRange(c.salaryInr.entryLow, c.salaryInr.entryHigh)} · Skills: {c.skills.filter((s) => s.importance === 'core').slice(0, 4).map((s) => skillName(s.skillId)).join(', ')} · Demand: {DEMAND_LABEL[c.demand]?.toLowerCase()}</p>
                          {f?.reasons[0] && <p className={cn('mt-1 text-xs text-subtle')}>{f.reasons.slice(0, 2).join(' · ')}</p>}
                        </div>
                        <LinkButton href={`/student/career/${c.id}`} variant="secondary" size="sm">More details</LinkButton>
                      </div>
                    </Card>
                  </li>
                );
              })}
            </ol>
          )}
        </section>
      </form>
    </>
  );
}
