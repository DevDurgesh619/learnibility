import 'server-only';
import type { OnboardingAcademicItem, OnboardingFormFile, OnboardingReasoningItem, OnboardingSurveyItem } from '@/lib/types/onboarding';
import { DEFAULT_LADDER } from '@/lib/onboarding/ladder';
import type { RunnerData, RunnerSection } from './test-runner';

const SLOTS = 8;

/** Turns an onboarding form file into the sections the runner shows (Part A per group, Part B, Part C). */
export function runnerData(file: OnboardingFormFile): RunnerData {
  const { form } = file;
  const academic = file.items.filter((i): i is OnboardingAcademicItem => i.part === 'A');
  const reasoning = file.items.filter((i): i is OnboardingReasoningItem => i.part === 'B');
  const survey = file.items.filter((i): i is OnboardingSurveyItem => i.part === 'C');
  const groups = form.scoring.groups.filter((g) => academic.some((a) => a.group === g.group));
  const perGroup = Math.max(4, Math.round(form.minutes.A / Math.max(1, groups.length)));
  const sections: RunnerSection[] = [
    ...groups.map((g) => ({ key: g.group, kind: 'academic' as const, label: g.label, minutes: perGroup, questions: SLOTS })),
    ...(reasoning.length ? [{ key: 'reasoning', kind: 'reasoning' as const, label: 'Reasoning', minutes: form.minutes.B, questions: reasoning.length }] : []),
    ...(survey.length ? [{ key: 'about', kind: 'about' as const, label: 'About you: habits, interests and goals', minutes: form.minutes.C, questions: survey.length }] : []),
  ];
  return { formId: form.formId, title: form.title, rule: form.scoring.ladder ?? DEFAULT_LADDER, sections, academic, reasoning, survey, reasoningMinutes: form.minutes.B };
}
