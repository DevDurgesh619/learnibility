import { ShieldAlert } from 'lucide-react';
import { Badge, Card, CardBody, CardHeader, Progress, TierBadge } from '@/components/ui';
import { cn } from '@/lib/utils';
import type { Section360 } from './profile360';
import { displayValue } from './profile360';
import { formatDate } from './format';

const DENSITY_TONE = { Sparse: 'danger', Thin: 'warning', Good: 'info', Rich: 'success' } as const;
const CONF_TONE = { low: 'danger', medium: 'warning', high: 'success' } as const;

/** Evidence density per section: one bar each, clickable to the section below. */
export function DensityOverview({ sections }: { sections: Section360[] }) {
  return (
    <Card>
      <CardHeader title="Evidence density" description="Share of parameters with a value, per section" />
      <CardBody className="grid gap-x-8 gap-y-3 sm:grid-cols-2">
        {sections.map((s) => (
          <a key={s.section} href={`#sec-${slug(s.section)}`} className="group block min-w-0">
            <div className="mb-1 flex items-center justify-between gap-2 text-sm">
              <span className="truncate text-ink group-hover:text-brand-700">{s.section}</span>
              <span className="shrink-0 text-xs text-muted">{s.filled}/{s.total}</span>
            </div>
            <Progress value={s.density} tone={s.density < 0.25 ? 'danger' : s.density < 0.5 ? 'warning' : s.density < 0.75 ? 'brand' : 'success'} />
          </a>
        ))}
      </CardBody>
    </Card>
  );
}

export function slug(s: string) {
  return s.toLowerCase().replace(/[^a-z0-9]+/g, '-');
}

export function SectionTable({ section, open, filledOnly }: { section: Section360; open?: boolean; filledOnly?: boolean }) {
  const rows = filledOnly ? section.rows.filter((r) => r.value) : section.rows;
  return (
    <details id={`sec-${slug(section.section)}`} open={open} className="group scroll-mt-24 rounded-[var(--radius-card)] border border-line bg-surface shadow-[var(--shadow-card)]">
      <summary className="flex cursor-pointer list-none flex-wrap items-center gap-x-4 gap-y-2 px-5 py-4 [&::-webkit-details-marker]:hidden">
        <span className="min-w-0 flex-1 font-semibold text-ink">{section.section}</span>
        <Badge tone={DENSITY_TONE[section.densityLabel]}>{section.densityLabel} · {Math.round(section.density * 100)}%</Badge>
        <span className="text-xs text-muted">{section.filled} of {section.total} filled</span>
        {section.lowConfidence > 0 && <span className="text-xs text-warning-700">{section.lowConfidence} low confidence</span>}
        {section.stale > 0 && <span className="text-xs text-danger-700">{section.stale} stale</span>}
        {section.tiers.T3 > 0 && <span className="inline-flex items-center gap-1 text-xs text-danger-700"><ShieldAlert className="size-3.5" />{section.tiers.T3} T3</span>}
        <span className="text-subtle transition-transform group-open:rotate-90" aria-hidden>›</span>
      </summary>
      <div className="border-t border-line">
        {/* Desktop table */}
        <div className="hidden overflow-x-auto md:block">
          <table className="w-full text-sm">
            <thead className="bg-surface-muted/60 text-left text-xs font-medium uppercase tracking-wide text-subtle">
              <tr><th className="h-10 px-4">#</th><th className="px-4">Parameter</th><th className="px-4">Value</th><th className="px-4">Source</th><th className="px-4">As of</th><th className="px-4">Confidence</th><th className="px-4">Tier</th></tr>
            </thead>
            <tbody className="divide-y divide-line">
              {rows.map((r) => (
                <tr key={r.param.id} className={cn(!r.value && 'text-subtle')}>
                  <td className="px-4 py-2.5 align-top text-xs text-subtle">{r.param.number}</td>
                  <td className="px-4 py-2.5 align-top">
                    <div className={cn('font-medium', r.value ? 'text-ink' : 'text-muted')}>{r.param.name}</div>
                    <div className="text-xs text-subtle">{r.param.category} · {r.param.cadence}</div>
                  </td>
                  <td className="max-w-xs px-4 py-2.5 align-top">
                    {r.value ? (r.value.mode === 'summary' ? <span className="italic text-muted">Summary only</span> : <span className="break-words text-ink">{displayValue(r.value.value)}</span>)
                      : <span className="text-xs">Not collected · plan {r.param.phase1Default ?? r.param.methods[0] ?? '—'}</span>}
                  </td>
                  <td className="px-4 py-2.5 align-top text-xs">{r.value?.source ?? '—'}</td>
                  <td className="px-4 py-2.5 align-top text-xs whitespace-nowrap">
                    {r.value?.asOfUtc ? formatDate(r.value.asOfUtc) : '—'}
                    {r.stale && <Badge tone="danger" className="ml-1">Stale</Badge>}
                  </td>
                  <td className="px-4 py-2.5 align-top">{r.value?.confidence ? <Badge tone={CONF_TONE[r.value.confidence]}>{r.value.confidence}</Badge> : '—'}</td>
                  <td className="px-4 py-2.5 align-top"><TierBadge tier={r.param.tier} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {/* Mobile list */}
        <ul className="divide-y divide-line md:hidden">
          {rows.map((r) => (
            <li key={r.param.id} className="px-4 py-3">
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <div className={cn('text-sm font-medium', r.value ? 'text-ink' : 'text-muted')}>{r.param.number}. {r.param.name}</div>
                  <div className="mt-0.5 break-words text-sm text-ink">
                    {r.value ? (r.value.mode === 'summary' ? 'Summary only' : displayValue(r.value.value)) : <span className="text-xs text-subtle">Not collected</span>}
                  </div>
                </div>
                <TierBadge tier={r.param.tier} />
              </div>
              {r.value && (
                <div className="mt-1 flex flex-wrap gap-2 text-xs text-muted">
                  <span>{r.value.source}</span>
                  {r.value.asOfUtc && <span>{formatDate(r.value.asOfUtc)}</span>}
                  {r.value.confidence && <Badge tone={CONF_TONE[r.value.confidence]}>{r.value.confidence}</Badge>}
                  {r.stale && <Badge tone="danger">Stale</Badge>}
                </div>
              )}
            </li>
          ))}
        </ul>
        {rows.length === 0 && <p className="px-5 py-6 text-center text-sm text-muted">Nothing collected in this section yet.</p>}
      </div>
    </details>
  );
}
