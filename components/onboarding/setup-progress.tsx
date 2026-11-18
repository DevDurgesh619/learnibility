'use client';

import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Check, Loader2 } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { completeOnboarding } from '@/lib/actions/onboarding';
import type { OnboardingResponses } from '@/lib/onboarding/score';
import { runStorageKey } from './test-runner';

const STEPS = ['Saving your profile', 'Finding where each subject starts', 'Drafting your first weekly timetable', 'Finding tutors and next steps for you'];
const MIN_MS = 2600;

export function SetupProgress({ formId, learnerId, firstName }: { formId: string | null; learnerId: string; firstName: string }) {
  const router = useRouter();
  const [step, setStep] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const started = useRef(false);

  useEffect(() => {
    if (started.current) return;
    started.current = true;
    const t0 = Date.now();
    const timer = setInterval(() => setStep((s) => Math.min(STEPS.length - 1, s + 1)), MIN_MS / STEPS.length);
    let responses: OnboardingResponses = { academic: [], reasoning: [], survey: [] };
    const key = formId ? runStorageKey(learnerId, formId) : null;
    try {
      if (key) responses = { ...responses, ...JSON.parse(localStorage.getItem(key) ?? '{}') };
    } catch {
      /* start empty */
    }
    completeOnboarding({ formId, responses })
      .then((r) => {
        if (key) localStorage.removeItem(key);
        setSummary(r.openGaps ? `${r.openGaps} starting gaps found and planned into your week.` : 'Your week is ready. Take the starting test any time from Assessments.');
        const wait = Math.max(0, MIN_MS - (Date.now() - t0));
        setTimeout(() => {
          clearInterval(timer);
          setStep(STEPS.length);
          setTimeout(() => router.replace('/student'), 700);
        }, wait);
      })
      .catch(() => {
        clearInterval(timer);
        setError('Something went wrong while saving. Your answers are still on this device.');
      });
    return () => clearInterval(timer);
  }, [formId, learnerId, router]);

  return (
    <div className="flex min-h-[70vh] items-center justify-center">
      <Card className="w-full max-w-md p-6 sm:p-8">
        <div className="mx-auto flex size-14 items-center justify-center rounded-full bg-brand-50">
          {step >= STEPS.length ? <Check className="size-7 text-success-700" /> : <Loader2 className="size-7 animate-spin text-brand-600" />}
        </div>
        <h1 className="mt-4 text-center text-xl font-semibold text-ink">{step >= STEPS.length ? `You're all set${firstName ? `, ${firstName}` : ''}` : 'Setting things up…'}</h1>
        <ul className="mt-6 flex flex-col gap-3">
          {STEPS.map((s, i) => {
            const done = i < step;
            const active = i === step;
            return (
              <li key={s} className="flex items-center gap-3 border-b border-dashed border-line pb-3 text-sm last:border-0">
                <span className={cn('flex size-5 items-center justify-center rounded', done ? 'bg-brand-600 text-white' : 'border border-line')}>
                  {done ? <Check className="size-3.5" /> : active ? <Loader2 className="size-3.5 animate-spin text-brand-600" /> : null}
                </span>
                <span className={done || active ? 'text-ink' : 'text-subtle'}>{s}</span>
              </li>
            );
          })}
        </ul>
        {summary && <p className="mt-4 text-center text-sm text-muted">{summary}</p>}
        {error && <p className="mt-4 text-center text-sm text-danger-700" role="alert">{error}</p>}
      </Card>
    </div>
  );
}
