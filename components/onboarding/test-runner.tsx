'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Brain, Check, Clock, ListChecks, Play, SkipForward, UserRound } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import type { OnboardingResponses } from '@/lib/onboarding/score';
import type { LadderRule, OnboardingAcademicItem, OnboardingReasoningItem, OnboardingSurveyItem } from '@/lib/types/onboarding';
import { AdaptiveSection } from './adaptive-section';
import { ReasoningSection } from './reasoning-section';
import { SurveySection } from './survey-section';

export interface RunnerSection {
  key: string; // group slug, 'reasoning' or 'about'
  kind: 'academic' | 'reasoning' | 'about';
  label: string;
  minutes: number;
  questions: number;
}

export interface RunnerData {
  formId: string;
  title: string;
  rule: LadderRule;
  sections: RunnerSection[];
  academic: OnboardingAcademicItem[];
  reasoning: OnboardingReasoningItem[];
  survey: OnboardingSurveyItem[];
  reasoningMinutes: number;
}

interface RunState extends OnboardingResponses {
  done: string[];
}

export const runStorageKey = (learnerId: string, formId: string) => `learnibility:onb:${learnerId}:${formId}`;

const ICON = { academic: ListChecks, reasoning: Brain, about: UserRound };

/** Runs the onboarding test section by section; answers stay on the device until `finishHref` saves them. */
export function OnboardingRunner({ data, learnerId, finishHref, only }: { data: RunnerData; learnerId: string; finishHref: string; only?: string[] }) {
  const router = useRouter();
  const key = runStorageKey(learnerId, data.formId);
  const sections = only ? data.sections.filter((s) => only.includes(s.key)) : data.sections;
  const [run, setRun] = useState<RunState | null>(null);
  const [active, setActive] = useState<string | null>(null);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(key);
      setRun(raw ? (JSON.parse(raw) as RunState) : { academic: [], reasoning: [], survey: [], done: [] });
    } catch {
      setRun({ academic: [], reasoning: [], survey: [], done: [] });
    }
  }, [key]);

  useEffect(() => {
    if (run) localStorage.setItem(key, JSON.stringify(run));
  }, [run, key]);

  if (!run) return null;

  const complete = (sectionKey: string, patch: Partial<OnboardingResponses>) => {
    setRun((r) => {
      if (!r) return r;
      return {
        academic: [...r.academic.filter((x) => !patch.academic?.some((p) => p.questionId === x.questionId)), ...(patch.academic ?? [])],
        reasoning: patch.reasoning ?? r.reasoning,
        survey: patch.survey ?? r.survey,
        done: [...new Set([...r.done, sectionKey])],
      };
    });
    setActive(null);
    window.scrollTo({ top: 0 });
  };

  const section = sections.find((s) => s.key === active);
  if (section) {
    const seed = `${learnerId}:${data.formId}`;
    if (section.kind === 'academic')
      return <AdaptiveSection key={section.key} label={section.label} rule={data.rule} seed={seed} items={data.academic.filter((i) => i.group === section.key)} onDone={(academic) => complete(section.key, { academic })} />;
    if (section.kind === 'reasoning') return <ReasoningSection items={data.reasoning} minutes={data.reasoningMinutes} seed={seed} onDone={(reasoning) => complete('reasoning', { reasoning })} />;
    return <SurveySection items={data.survey} seed={seed} onDone={(survey) => complete('about', { survey })} />;
  }

  const remaining = sections.filter((s) => !run.done.includes(s.key));
  const minutesLeft = remaining.reduce((s, x) => s + x.minutes, 0);
  const anyDone = sections.some((s) => run.done.includes(s.key));

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-wrap items-center gap-2 text-sm text-muted">
        <Clock className="size-4" /> {remaining.length ? `About ${minutesLeft} minutes left · take the parts in any order, with breaks` : 'All parts done'}
      </div>
      <div className="grid gap-3">
        {sections.map((s) => {
          const done = run.done.includes(s.key);
          const Icon = ICON[s.kind];
          return (
            <Card key={s.key} className="flex items-center gap-4 p-4">
              <span className={done ? 'flex size-10 items-center justify-center rounded-full bg-success-50 text-success-700' : 'flex size-10 items-center justify-center rounded-full bg-brand-50 text-brand-600'}>
                {done ? <Check className="size-5" /> : <Icon className="size-5" />}
              </span>
              <div className="min-w-0 flex-1">
                <p className="font-medium text-ink">{s.label}</p>
                <p className="text-xs text-muted">
                  {s.questions} questions · about {s.minutes} min{s.kind === 'academic' ? ' · adapts to your answers' : ''}
                </p>
              </div>
              {done ? (
                <Badge tone="success">Done</Badge>
              ) : (
                <Button size="sm" variant={s.key === remaining[0]?.key ? 'primary' : 'secondary'} onClick={() => setActive(s.key)}>
                  <Play /> Start
                </Button>
              )}
            </Card>
          );
        })}
      </div>
      <div className="mt-2 flex flex-wrap items-center justify-end gap-2">
        {remaining.length > 0 && anyDone && (
          <Button variant="ghost" onClick={() => router.push(finishHref)}>
            <SkipForward /> Finish with what I have
          </Button>
        )}
        {remaining.length === 0 && <Button size="lg" onClick={() => router.push(finishHref)}>See my results and plan</Button>}
      </div>
    </div>
  );
}
