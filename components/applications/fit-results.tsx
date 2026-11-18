'use client';

import Link from 'next/link';
import { useEffect, useState, type ReactNode } from 'react';
import { Loader2 } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import type { FitBand } from './fit';

export interface FitCard {
  universityId: string;
  shortName: string;
  programme: string;
  country: string;
  band: FitBand;
  chancePct: number;
  reason: string;
}

const STEPS = ['Reading your grades and test scores', 'Comparing with each programme\'s typical offer', 'Weighing admit rates and test policies', 'Grouping into Reach, Target and Safe'];

/** PDF 6f then 6g: a short computing state, then grouped results. */
export function FitResults({ groups, readinessPct, footer, instant }: { groups: Record<FitBand, FitCard[]>; readinessPct: number; footer: ReactNode; instant?: boolean }) {
  const [step, setStep] = useState(instant ? STEPS.length : 0);
  const [band, setBand] = useState<FitBand | 'all'>('all');
  useEffect(() => {
    if (step >= STEPS.length) return;
    const t = setTimeout(() => setStep((s) => s + 1), 450);
    return () => clearTimeout(t);
  }, [step]);

  if (step < STEPS.length) {
    return (
      <Card className="mx-auto max-w-lg p-8 text-center" aria-live="polite">
        <Loader2 className="mx-auto size-8 animate-spin text-brand-600" />
        <p className="mt-4 text-base font-semibold text-ink">Calculating your fit</p>
        <ul className="mt-4 space-y-2 text-left text-sm">
          {STEPS.map((s, i) => (
            <li key={s} className={cn('flex items-center gap-2', i < step ? 'text-ink' : i === step ? 'text-brand-700' : 'text-subtle')}>
              <span className={cn('inline-block size-2 rounded-full', i < step ? 'bg-success-600' : i === step ? 'bg-brand-600' : 'bg-line')} />{s}
            </li>
          ))}
        </ul>
      </Card>
    );
  }

  const order: FitBand[] = ['reach', 'target', 'safe'];
  const shown = band === 'all' ? order : [band];
  return (
    <>
      <div className="mb-4 flex flex-wrap items-center gap-2">
        {order.map((b) => (
          <button key={b} type="button" onClick={() => setBand(band === b ? 'all' : b)}
            className={cn('rounded-full border px-3 py-1 text-sm font-medium', band === b ? 'border-brand-600 bg-brand-50 text-brand-700' : 'border-line bg-surface text-ink hover:bg-surface-muted')}>
            {b[0]!.toUpperCase() + b.slice(1)} {groups[b].length}
          </button>
        ))}
        <span className="text-xs text-muted">Based on profile {readinessPct}% · <Link href="/student/universities/best-fit/profile" className="underline">Edit</Link></span>
      </div>
      {shown.map((b) => (
        <section key={b} className="mb-6">
          <h2 className="mb-2 text-sm font-semibold tracking-wide text-muted uppercase">{b} · {groups[b].length}</h2>
          {groups[b].length === 0 ? (
            <p className="rounded-lg border border-dashed border-line px-4 py-3 text-sm text-muted">No {b} universities with this filter. {b === 'safe' ? 'Add a country or course to widen the search.' : ''}</p>
          ) : (
            <div className="grid grid-cols-[minmax(0,1fr)] gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {groups[b].map((c) => (
                <Card key={c.universityId} className={cn('flex flex-col p-4', b === 'target' && 'border-info-600/30')}>
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0">
                      <p className="truncate font-semibold text-ink">{c.shortName}</p>
                      <p className="truncate text-xs text-subtle">{c.programme}</p>
                    </div>
                    <span className={cn('shrink-0 rounded-full px-2 py-0.5 text-xs font-medium', b === 'reach' ? 'bg-danger-50 text-danger-700' : b === 'target' ? 'bg-info-50 text-info-600' : 'bg-success-50 text-success-700')}>{b[0]!.toUpperCase() + b.slice(1)}</span>
                  </div>
                  <p className="mt-2 text-2xl font-semibold tracking-tight text-ink">{c.chancePct}%</p>
                  <p className="mt-1 flex-1 text-xs text-muted">{c.reason}</p>
                  <Link href={`/student/universities/${c.universityId}`} className="mt-3 text-sm font-medium text-brand-700 hover:underline">Details ›</Link>
                </Card>
              ))}
            </div>
          )}
        </section>
      ))}
      {footer}
    </>
  );
}
