import Link from 'next/link';
import { notFound } from 'next/navigation';
import { Card, CardBody, CardHeader } from '@/components/ui';
import { SkillChip } from '@/components/career/career-tabs';
import { careerGapFor, resourceById, studentCtx, trainersFor } from '@/components/student/load';
import { LinkButton } from '@/components/student/link-button';
import { formatHours, formatInr } from '@/lib/format';

export const metadata = { title: 'Skill gap · Learnibility' };

/** PDF 9d: your skills · required · must-have to add, then the free and the paid route in hours, months and rupees. */
export default async function SkillGapPage({ params }: { params: Promise<{ careerId: string }> }) {
  const { careerId } = await params;
  const ctx = await studentCtx();
  const res = await careerGapFor(ctx, careerId);
  if (!res) notFound();
  const { career, gap } = res;
  const have = gap.skills.filter((s) => s.currentLevel > 0);
  const missing = gap.skills.filter((s) => s.levelsToClimb > 0);
  const mustAdd = missing.filter((s) => s.importance === 'core');
  const freeIds = [...new Set(missing.flatMap((s) => s.freeRoute.resourceIds))];
  const freeRes = (await Promise.all(freeIds.map(resourceById))).filter((r) => !!r).slice(0, 4);
  const paidRes = (await Promise.all([...new Set(missing.map((s) => s.paidRoute.resourceId).filter((x): x is string => !!x))].map(resourceById))).filter((r) => !!r).slice(0, 3);
  const trainers = await trainersFor(career, missing.map((s) => s.skillId));

  return (
    <>
      <Link href={`/student/career/${career.id}`} className="mb-2 inline-block text-sm text-muted hover:text-ink">‹ {career.title}</Link>
      <h1 className="mb-4 text-2xl font-semibold tracking-tight text-ink">Your skill gap for {career.title}</h1>

      <div className="mb-4 grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title="Your skills" description="From your profile, tests and Inventory projects" />
          <CardBody className="flex flex-wrap gap-2">
            {have.length ? have.map((s) => <SkillChip key={s.skillId} tone="solid">{s.name} · L{s.currentLevel}</SkillChip>) : <p className="text-sm text-muted">No evidence yet. Add projects to your Inventory to count them.</p>}
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Required" description="Level 1 to 5 the job expects" />
          <CardBody className="flex flex-wrap gap-2">
            {gap.skills.map((s) => <SkillChip key={s.skillId} tone={s.levelsToClimb === 0 ? 'solid' : 'outline'}>{s.name} · L{s.targetLevel}</SkillChip>)}
          </CardBody>
        </Card>
      </div>

      <Card className="mb-4 border-success-600/30 bg-success-50/40">
        <CardBody>
          <p className="text-sm font-semibold text-ink">{mustAdd.length ? `Must-have skills to add: ${mustAdd.map((s) => s.name).join(', ')}` : 'You already meet every core skill. Polish the helpful ones.'}</p>
          <ul className="mt-2 grid gap-1 text-sm text-muted sm:grid-cols-2">
            {missing.map((s) => <li key={s.skillId}>{s.name}: level {s.currentLevel} → {s.targetLevel} · about {formatHours(s.hours)}</li>)}
          </ul>
        </CardBody>
      </Card>

      <div className="mb-4 grid gap-3 sm:grid-cols-2">
        <Card className="p-4">
          <p className="text-sm font-semibold text-ink">Free route</p>
          <p className="mt-1 text-2xl font-semibold text-ink">{formatHours(gap.free.hours)} · {gap.free.months} months</p>
          <p className="text-sm text-muted">₹0 · free channels and courses at 5 hours a week</p>
        </Card>
        <Card className="p-4">
          <p className="text-sm font-semibold text-ink">Paid route</p>
          <p className="mt-1 text-2xl font-semibold text-ink">{formatHours(gap.paid.hours)} · {gap.paid.months} months</p>
          <p className="text-sm text-muted">{formatInr(gap.paid.inr)} · structured courses with certificates</p>
        </Card>
      </div>

      <h2 className="mb-2 border-b border-dashed border-line pb-1 text-sm font-semibold text-ink">Recommended to fill the gap</h2>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {freeRes.map((r) => (
          <Card key={r.id} className="flex flex-col p-4">
            <p className="text-sm font-semibold text-ink">{r.title}</p>
            <p className="mt-1 flex-1 text-xs text-muted">Free · {r.provider} · {formatHours(r.hours)}</p>
            <a href={r.url} target="_blank" rel="noreferrer" className="mt-3 self-start rounded-lg border border-line px-3 py-1.5 text-sm font-medium text-ink hover:bg-surface-muted">Open</a>
          </Card>
        ))}
        {paidRes.map((r) => (
          <Card key={r.id} className="flex flex-col p-4">
            <p className="text-sm font-semibold text-ink">{r.title}</p>
            <p className="mt-1 flex-1 text-xs text-muted">{formatInr(r.priceInr)} · {r.provider} · {formatHours(r.hours)}{r.certificate ? ' · certificate' : ''}</p>
            <a href={r.url} target="_blank" rel="noreferrer" className="mt-3 self-start rounded-lg border border-line px-3 py-1.5 text-sm font-medium text-ink hover:bg-surface-muted">View course</a>
          </Card>
        ))}
        {trainers.map((t) => (
          <Card key={t.id} className="flex flex-col p-4">
            <p className="text-sm font-semibold text-ink">Trainer: {t.displayName}</p>
            <p className="mt-1 flex-1 text-xs text-muted">On platform · {formatInr(t.pricing.oneToOnePerHourInr)}/hr · {t.headline}</p>
            <LinkButton href={`/student/tutors/${t.id}`} variant="secondary" size="sm" className="mt-3 self-start border-success-600/40 text-success-700">Book demo</LinkButton>
          </Card>
        ))}
      </div>

      {gap.pathways.length > 0 && (
        <Card className="mt-4">
          <CardHeader title="And the degree route" description="Cost from class 12 to the first job" />
          <CardBody className="pt-2">
            <ul className="divide-y divide-line text-sm">
              {gap.pathways.map((p) => (
                <li key={p.id} className="flex flex-col gap-1 py-2 sm:flex-row sm:justify-between">
                  <span className="text-ink">{p.label}</span>
                  <span className="text-muted">{p.yearsToEntry} yrs · {formatInr(p.costInr.typical)}{p.examPrepHours ? ` · ${formatHours(p.examPrepHours)} exam prep` : ''}{p.examFeesInr ? ` · fees ${formatInr(p.examFeesInr)}` : ''}</span>
                </li>
              ))}
            </ul>
          </CardBody>
        </Card>
      )}
    </>
  );
}
