import { Badge, Card, CardBody, CardHeader, Progress } from '@/components/ui';
import type { Career } from '@/lib/types';
import type { CareerFit, CareerGapResult } from '@/lib/engines';
import { formatHours, formatInr } from '@/lib/format';

const PART_MAX = { interests: 35, aptitudeAcademics: 35, skills: 15, feasibility: 15 } as const;
const PART_LABEL = { interests: 'Interests', aptitudeAcademics: 'Aptitude and academics', skills: 'Skill evidence', feasibility: 'Feasibility' } as const;

/** Side-by-side career comparison: fit parts from mapCareers, routes and pathways from careerGap. */
export function CareerColumn({ career, fit, gap }: { career: Career; fit?: CareerFit; gap?: CareerGapResult }) {
  return (
    <Card className="min-w-0">
      <CardHeader title={career.title} description={`${career.cluster} · demand ${career.demand}`}
        action={fit && <div className="text-right"><div className="text-2xl font-semibold text-ink">{fit.score}</div><div className="text-xs text-muted">fit / 100</div></div>} />
      <CardBody className="space-y-5">
        <p className="text-sm text-muted">{career.summary}</p>
        {fit && (
          <div className="space-y-2">
            {(Object.keys(PART_MAX) as (keyof typeof PART_MAX)[]).map((k) => (
              <div key={k}>
                <div className="mb-1 flex justify-between text-xs text-muted"><span>{PART_LABEL[k]}</span><span>{Math.round(fit.parts[k])} / {PART_MAX[k]}</span></div>
                <Progress value={fit.parts[k] / PART_MAX[k]} />
              </div>
            ))}
            <div className="flex flex-wrap items-center gap-2 pt-1"><Badge tone={fit.confidence === 'high' ? 'success' : fit.confidence === 'medium' ? 'info' : 'warning'}>{fit.confidence} confidence</Badge></div>
            <ul className="list-disc space-y-1 pl-5 text-sm text-ink">{fit.reasons.slice(0, 3).map((r) => <li key={r}>{r}</li>)}</ul>
          </div>
        )}
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="rounded-lg bg-surface-muted p-3"><div className="text-xs text-muted">Entry salary</div><div className="font-medium text-ink">{formatInr(career.salaryInr.entryLow)} to {formatInr(career.salaryInr.entryHigh)}</div></div>
          <div className="rounded-lg bg-surface-muted p-3"><div className="text-xs text-muted">Mid career</div><div className="font-medium text-ink">{formatInr(career.salaryInr.mid)}</div></div>
        </div>
        {gap && (
          <>
            <div>
              <p className="mb-2 text-xs font-medium uppercase tracking-wide text-subtle">Skill gap</p>
              <ul className="space-y-1.5 text-sm">
                {gap.skills.map((s) => (
                  <li key={s.skillId} className="flex items-center justify-between gap-2">
                    <span className="min-w-0 truncate text-ink">{s.name}{s.importance === 'core' && <span className="ml-1 text-xs text-subtle">core</span>}</span>
                    <span className="shrink-0 text-xs text-muted">L{s.currentLevel} → L{s.targetLevel} · {formatHours(s.hours)}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div className="rounded-lg border border-success-600/20 bg-success-50 p-3"><div className="text-xs text-success-700">Free route</div><div className="font-medium text-ink">{formatHours(gap.free.hours)} · {gap.free.months} months</div><div className="text-xs text-muted">₹0</div></div>
              <div className="rounded-lg border border-brand-200 bg-brand-50 p-3"><div className="text-xs text-brand-700">Paid route</div><div className="font-medium text-ink">{formatHours(gap.paid.hours)} · {gap.paid.months} months</div><div className="text-xs text-muted">{formatInr(gap.paid.inr)}</div></div>
            </div>
            <div>
              <p className="mb-2 text-xs font-medium uppercase tracking-wide text-subtle">Pathways</p>
              <ul className="space-y-2 text-sm">
                {gap.pathways.map((p) => (
                  <li key={p.id} className="rounded-lg border border-line p-3">
                    <div className="font-medium text-ink">{p.label}</div>
                    <div className="text-xs text-muted">{p.yearsToEntry} years to entry · typical {formatInr(p.costInr.typical)}{p.examPrepHours ? ` · exam prep ${formatHours(p.examPrepHours)}` : ''}</div>
                  </li>
                ))}
              </ul>
            </div>
          </>
        )}
      </CardBody>
    </Card>
  );
}
