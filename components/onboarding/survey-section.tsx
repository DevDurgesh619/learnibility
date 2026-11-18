'use client';

import { useState } from 'react';
import { ChevronLeft, ChevronRight, Lock, Wand2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { cn } from '@/lib/utils';
import type { OnboardingSurveyItem } from '@/lib/types/onboarding';
import type { SurveyResponse } from '@/lib/onboarding/score';
import { demoNumber } from './demo-answers';

const PAGE = 5;
type Value = SurveyResponse['value'];

/** Part C "About me": habits, preferences and the 12 career-interest items. Screened (T3) items say they can be skipped. */
export function SurveySection({ items, onDone, seed }: { items: OnboardingSurveyItem[]; onDone: (r: SurveyResponse[]) => void; seed: string }) {
  const [page, setPage] = useState(0);
  const [vals, setVals] = useState<Record<string, Value>>({});
  const pages = Math.ceil(items.length / PAGE);
  const slice = items.slice(page * PAGE, page * PAGE + PAGE);
  const missing = slice.filter((it) => !it.optional && (vals[it.id] === undefined || (Array.isArray(vals[it.id]) && (vals[it.id] as Value[]).length === 0)));

  const finish = (v = vals) => onDone(Object.entries(v).map(([questionId, value]) => ({ questionId, value })));

  const autoFinish = () => {
    const v = { ...vals };
    for (const it of items) {
      if (v[it.id] !== undefined || it.screened) continue;
      const opts = it.options ?? [];
      const r = demoNumber(seed, it.id);
      if (it.responseType === 'multi') v[it.id] = opts.slice(0, 2).map((o) => o.value);
      else if (it.responseType === 'number') v[it.id] = Math.round((it.min ?? 0) + r * ((it.max ?? 10) - (it.min ?? 0)));
      else if (it.responseType === 'consent') v[it.id] = opts[0]?.value ?? 'yes';
      else if (opts.length) v[it.id] = opts[Math.min(opts.length - 1, Math.floor(r * opts.length))].value;
    }
    finish(v);
  };

  const set = (it: OnboardingSurveyItem, value: string | number) =>
    setVals((v) => {
      if (it.responseType !== 'multi') return { ...v, [it.id]: value };
      const cur = (v[it.id] as (string | number)[] | undefined) ?? [];
      const next = cur.includes(value) ? cur.filter((x) => x !== value) : cur.length >= 3 ? cur : [...cur, value];
      return { ...v, [it.id]: next };
    });

  return (
    <div className="flex flex-col gap-5">
      <div>
        <div className="flex items-center justify-between text-sm">
          <span className="font-medium text-ink">About you</span>
          <span className="text-muted">Page {page + 1} of {pages}</span>
        </div>
        <Progress value={page / pages} className="mt-2" />
        <p className="mt-2 text-xs text-subtle">No right or wrong answers. This shapes your timetable, tutor matches and career suggestions.</p>
      </div>
      {slice.map((it) => {
        const v = vals[it.id];
        const scale = it.responseType === 'scale';
        return (
          <fieldset key={it.id} className="rounded-2xl border border-line bg-surface p-5">
            <legend className="sr-only">{it.prompt}</legend>
            <p className="font-medium text-ink">{it.prompt}</p>
            {(it.helpText || it.screened) && (
              <p className="mt-1 flex items-start gap-1.5 text-xs text-muted">
                {it.screened && <Lock className="mt-0.5 size-3.5 shrink-0" />}
                {it.helpText ?? 'Optional. You can skip this.'}
                {it.screened && ' Only you and your counsellor can see this answer.'}
              </p>
            )}
            {it.responseType === 'number' ? (
              <input type="number" min={it.min} max={it.max} value={(v as number | undefined) ?? ''} onChange={(e) => set(it, Number(e.target.value))}
                className="mt-3 h-11 w-40 rounded-lg border border-line px-3 text-sm outline-none focus:border-brand-500" aria-label={it.prompt} />
            ) : (
              <div className={cn('mt-3 gap-2', scale ? 'grid grid-cols-5' : 'flex flex-wrap')}>
                {(it.options ?? []).map((o) => {
                  const on = Array.isArray(v) ? v.includes(o.value) : v === o.value;
                  return (
                    <button key={String(o.value)} type="button" aria-pressed={on} onClick={() => set(it, o.value)}
                      className={cn('rounded-lg border px-3 py-2 text-sm transition', scale && 'px-1 text-center text-xs sm:text-sm', on ? 'border-brand-500 bg-brand-50 font-medium text-brand-700' : 'border-line text-muted hover:border-brand-300')}>
                      {o.label}
                    </button>
                  );
                })}
              </div>
            )}
            {it.optional && <p className="mt-2 text-xs text-subtle">Optional</p>}
          </fieldset>
        );
      })}
      <div className="flex flex-wrap items-center justify-between gap-2">
        <Button variant="ghost" size="sm" onClick={autoFinish}><Wand2 /> Fill the rest for me (demo)</Button>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => setPage((p) => p - 1)} disabled={page === 0}><ChevronLeft /> Back</Button>
          {page < pages - 1 ? (
            <Button onClick={() => setPage((p) => p + 1)} disabled={missing.length > 0}>Next <ChevronRight /></Button>
          ) : (
            <Button onClick={() => finish()} disabled={missing.length > 0}>Finish</Button>
          )}
        </div>
      </div>
    </div>
  );
}
