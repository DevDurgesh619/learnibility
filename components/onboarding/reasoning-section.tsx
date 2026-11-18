'use client';

import { useEffect, useRef, useState } from 'react';
import { ChevronLeft, ChevronRight, Clock, Wand2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { cn } from '@/lib/utils';
import type { OnboardingReasoningItem } from '@/lib/types/onboarding';
import type { ReasoningResponse } from '@/lib/onboarding/score';
import { formatClock } from '@/components/assessment/test-player';
import { demoNumber } from './demo-answers';

const LETTERS = ['A', 'B', 'C', 'D', 'E'];
const DOMAIN_LABEL = { numerical: 'Numbers', verbal: 'Words', abstract: 'Patterns', spatial: 'Shapes and space' } as const;

/** Part B reasoning: 16 timed items across four domains. Speed on right answers feeds processing speed (p69). */
export function ReasoningSection({ items, minutes, onDone, seed }: { items: OnboardingReasoningItem[]; minutes: number; onDone: (r: ReasoningResponse[]) => void; seed: string }) {
  const [i, setI] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [seconds, setSeconds] = useState<Record<string, number>>({});
  const [left, setLeft] = useState(minutes * 60);
  const done = useRef(false);
  const item = items[i];

  const finish = (a = answers, s = seconds) => {
    if (done.current) return;
    done.current = true;
    onDone(items.map((it) => ({ questionId: it.id, answer: a[it.id] ?? '', secondsTaken: Math.round(s[it.id] ?? it.seconds * 2) })));
  };

  useEffect(() => {
    const t = setInterval(() => {
      setLeft((l) => l - 1);
      setSeconds((s) => ({ ...s, [items[i].id]: (s[items[i].id] ?? 0) + 1 }));
    }, 1000);
    return () => clearInterval(t);
  }, [i, items]);

  useEffect(() => {
    if (left <= 0) finish();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [left]);

  const autoFinish = () => {
    const a = { ...answers };
    const s = { ...seconds };
    for (const it of items) {
      if (a[it.id]) continue;
      const r = demoNumber(seed, it.id);
      a[it.id] = r < 0.7 ? it.answer : it.options.find((o) => o !== it.answer) ?? it.answer;
      s[it.id] = Math.round(it.seconds * (0.6 + r));
    }
    finish(a, s);
  };

  return (
    <div className="flex flex-col gap-5">
      <div>
        <div className="flex items-center justify-between text-sm">
          <span className="font-medium text-ink">Reasoning · {DOMAIN_LABEL[item.domain]}</span>
          <span className="inline-flex items-center gap-1 tabular-nums text-muted"><Clock className="size-4" /> {formatClock(left)}</span>
        </div>
        <Progress value={i / items.length} className="mt-2" />
      </div>
      <div className="rounded-2xl border border-line bg-surface p-5 sm:p-6">
        <p className="text-xs text-subtle">Question {i + 1} of {items.length}</p>
        <p className="mt-2 text-lg leading-relaxed text-ink">{item.stem}</p>
        {item.svg && <div className="mt-4 rounded-lg border border-line p-3 [&_svg]:mx-auto [&_svg]:h-auto [&_svg]:max-w-full" dangerouslySetInnerHTML={{ __html: item.svg }} />}
        <div role="radiogroup" className="mt-4 grid gap-2 sm:grid-cols-2">
          {item.options.map((opt, k) => {
            const on = answers[item.id] === opt;
            return (
              <button key={opt} type="button" role="radio" aria-checked={on} onClick={() => setAnswers((a) => ({ ...a, [item.id]: opt }))}
                className={cn('flex items-start gap-3 rounded-xl border p-3 text-left text-sm transition', on ? 'border-brand-500 bg-brand-50 ring-2 ring-brand-200' : 'border-line hover:border-brand-300')}>
                <span className={cn('flex size-6 shrink-0 items-center justify-center rounded-full border text-xs font-semibold', on ? 'border-brand-600 bg-brand-600 text-white' : 'border-line text-muted')}>{LETTERS[k]}</span>
                <span className="pt-0.5">{opt}</span>
              </button>
            );
          })}
        </div>
      </div>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <Button variant="ghost" size="sm" onClick={autoFinish}><Wand2 /> Answer the rest for me (demo)</Button>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => setI((x) => Math.max(0, x - 1))} disabled={i === 0}><ChevronLeft /> Prev</Button>
          {i < items.length - 1 ? (
            <Button onClick={() => setI((x) => x + 1)}>Next <ChevronRight /></Button>
          ) : (
            <Button onClick={() => finish()}>Finish section</Button>
          )}
        </div>
      </div>
    </div>
  );
}
