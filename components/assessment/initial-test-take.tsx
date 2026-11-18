'use client';

import { useState, useTransition } from 'react';
import { Loader2 } from 'lucide-react';
import { Logo } from '@/components/shell/logo';
import type { OnboardingResponses } from '@/lib/onboarding/score';
import { AdaptiveSection } from '@/components/onboarding/adaptive-section';
import { ReasoningSection } from '@/components/onboarding/reasoning-section';
import { SurveySection } from '@/components/onboarding/survey-section';
import type { RunnerData } from '@/components/onboarding/test-runner';

/** One initial-test section taken from Assessments (8a "Initial tests"), full screen like 8d. */
export function InitialTestTake({ data, learnerId, section, title, onSubmit }: {
  data: RunnerData; learnerId: string; section: string; title: string;
  onSubmit: (r: OnboardingResponses) => Promise<void>;
}) {
  const [pending, start] = useTransition();
  const [error, setError] = useState<string | null>(null);
  const s = data.sections.find((x) => x.key === section);
  const seed = `${learnerId}:${data.formId}`;
  const send = (patch: Partial<OnboardingResponses>) =>
    start(async () => {
      try {
        await onSubmit({ academic: [], reasoning: [], survey: [], ...patch });
      } catch (e) {
        if (e && typeof e === 'object' && 'digest' in e) throw e;
        setError('Could not save. Try again.');
      }
    });
  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-canvas">
      <header className="flex items-center justify-between border-b border-line bg-surface px-4 py-3 sm:px-6">
        <Logo href="/student/assessments" />
        <p className="text-sm font-medium text-ink">{title} · starting test</p>
      </header>
      <main className="mx-auto max-w-2xl px-4 py-8 sm:px-6">
        {pending ? (
          <p className="flex items-center justify-center gap-2 py-20 text-muted"><Loader2 className="size-5 animate-spin" /> Saving your answers and updating your plan…</p>
        ) : !s ? null : s.kind === 'academic' ? (
          <AdaptiveSection label={s.label} rule={data.rule} seed={seed} items={data.academic.filter((i) => i.group === s.key)} onDone={(academic) => send({ academic })} />
        ) : s.kind === 'reasoning' ? (
          <ReasoningSection items={data.reasoning} minutes={data.reasoningMinutes} seed={seed} onDone={(reasoning) => send({ reasoning })} />
        ) : (
          <SurveySection items={data.survey} seed={seed} onDone={(survey) => send({ survey })} />
        )}
        {error && <p className="mt-4 text-sm text-danger-700">{error}</p>}
      </main>
    </div>
  );
}
