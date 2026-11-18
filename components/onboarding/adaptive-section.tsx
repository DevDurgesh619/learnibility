'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import { ChevronRight, Wand2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { cn } from '@/lib/utils';
import { nextItem } from '@/lib/onboarding/ladder';
import type { LadderRule, OnboardingAcademicItem } from '@/lib/types/onboarding';
import type { AcademicResponse } from '@/lib/onboarding/score';
import { demoCorrect } from './demo-answers';

const LETTERS = ['A', 'B', 'C', 'D'];
const SLOTS = 8;

/**
 * One Part A subject group on the adaptive ladder: 8 questions, one per slot, starting at D2,
 * one step easier after a miss and one harder after two hits. No going back (the next item depends on the answer).
 */
export function AdaptiveSection({
  label,
  items,
  rule,
  onDone,
  seed,
}: {
  label: string;
  items: OnboardingAcademicItem[];
  rule: LadderRule;
  onDone: (responses: AcademicResponse[]) => void;
  seed: string;
}) {
  const [answered, setAnswered] = useState<Record<string, boolean>>({});
  const [responses, setResponses] = useState<(AcademicResponse & { answer?: string })[]>([]);
  const [choice, setChoice] = useState<string | null>(null);
  const [conf, setConf] = useState<1 | 2 | 3 | 4 | 5 | undefined>();
  const shownAt = useRef(Date.now());
  const current = useMemo(() => nextItem(items, answered, rule), [items, answered, rule]);

  useEffect(() => {
    shownAt.current = Date.now();
    setChoice(null);
    setConf(undefined);
  }, [current?.id]);

  useEffect(() => {
    if (!current) onDone(responses);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [current]);

  if (!current) return null;

  const record = (answer: string | null, confidence?: 1 | 2 | 3 | 4 | 5, seconds?: number) => {
    const correct = answer === current.answer;
    setResponses((r) => [...r, { questionId: current.id, correct, answer: answer ?? undefined, secondsTaken: seconds ?? Math.round((Date.now() - shownAt.current) / 1000), confidence }]);
    setAnswered((a) => ({ ...a, [current.id]: correct }));
  };

  /** Demo: answer the remaining slots with a plausible pattern so the flow can be shown quickly. */
  const autoFinish = () => {
    const ans = { ...answered };
    const out = [...responses];
    for (let it = nextItem(items, ans, rule); it; it = nextItem(items, ans, rule)) {
      const ok = demoCorrect(seed, it);
      ans[it.id] = ok;
      out.push({ questionId: it.id, correct: ok, answer: ok ? it.answer : (it.options ?? []).find((o) => o !== it.answer), secondsTaken: Math.round(it.minutes * 60 * (ok ? 0.8 : 1.3)), confidence: ok ? 4 : 3 });
    }
    setResponses(out);
    setAnswered(ans);
  };

  const n = responses.length + 1;
  return (
    <div className="flex flex-col gap-5">
      <div>
        <div className="flex items-center justify-between text-sm">
          <span className="font-medium text-ink">{label}</span>
          <span className="text-muted">Question {n} of {SLOTS}</span>
        </div>
        <Progress value={(n - 1) / SLOTS} className="mt-2" />
      </div>

      <div className="rounded-2xl border border-line bg-surface p-5 sm:p-6">
        <p className="text-xs font-medium uppercase tracking-wide text-brand-600">
          {current.half === 'prerequisite' ? 'From earlier years' : 'This year'} · {current.subtopicHint}
        </p>
        <p className="mt-2 text-lg leading-relaxed text-ink">{current.stem}</p>
        <div role="radiogroup" aria-label="Options" className="mt-4 grid gap-2 sm:grid-cols-2">
          {(current.options ?? []).map((opt, i) => {
            const on = choice === opt;
            return (
              <button key={opt} type="button" role="radio" aria-checked={on} onClick={() => setChoice(opt)}
                className={cn('flex items-start gap-3 rounded-xl border p-3 text-left text-sm transition', on ? 'border-brand-500 bg-brand-50 ring-2 ring-brand-200' : 'border-line hover:border-brand-300')}>
                <span className={cn('flex size-6 shrink-0 items-center justify-center rounded-full border text-xs font-semibold', on ? 'border-brand-600 bg-brand-600 text-white' : 'border-line text-muted')}>{LETTERS[i]}</span>
                <span className="pt-0.5">{opt}</span>
              </button>
            );
          })}
        </div>
        <div className="mt-4 flex flex-wrap items-center gap-2 text-sm">
          <span className="text-muted">How sure are you?</span>
          {([1, 2, 3, 4, 5] as const).map((c) => (
            <button key={c} type="button" aria-pressed={conf === c} onClick={() => setConf(c)}
              className={cn('size-8 rounded-full border text-sm font-medium', conf === c ? 'border-brand-600 bg-brand-600 text-white' : 'border-line text-muted hover:border-brand-300')}>
              {c}
            </button>
          ))}
        </div>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-2">
        <Button variant="ghost" size="sm" onClick={autoFinish} title="Demo shortcut">
          <Wand2 /> Answer the rest for me (demo)
        </Button>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => record(null, conf)}>I don&apos;t know</Button>
          <Button onClick={() => record(choice, conf)} disabled={!choice}>
            Next <ChevronRight />
          </Button>
        </div>
      </div>
    </div>
  );
}
