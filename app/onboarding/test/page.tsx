import type { Metadata } from 'next';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { Info } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { DRAFT_COOKIE, parseDraft } from '@/components/onboarding/draft';
import { loadOnboardingForm, pickOnboardingForm } from '@/components/onboarding/forms';
import { runnerData } from '@/components/onboarding/runner-data';
import { Stepper } from '@/components/onboarding/stepper';
import { OnboardingRunner } from '@/components/onboarding/test-runner';
import { NEW_STUDENT_PERSONA_ID } from '@/components/onboarding/demo-auth';
import { deferTest } from '@/lib/actions/onboarding';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Your starting test · Learnibility' };

/** Onboarding test (blueprint "Onboarding test and starting profile"): Part A adaptive per subject, Part B reasoning, Part C about you. */
export default async function OnboardingTestPage() {
  const draft = parseDraft((await cookies()).get(DRAFT_COOKIE)?.value);
  if (!draft.board || !draft.grade) redirect('/onboarding/about');
  const picked = pickOnboardingForm(draft.board, draft.grade, draft.stream ?? 'none');
  const file = picked && (await loadOnboardingForm(picked.row.formId));
  if (!file) redirect('/onboarding/setup');
  const data = runnerData(file);
  const learnerId = (await currentPersona())?.id ?? NEW_STUDENT_PERSONA_ID;
  return (
    <>
      <Stepper current={3} />
      <h1 className="text-2xl font-semibold tracking-tight text-ink">Your starting test</h1>
      <p className="mt-1 text-sm text-muted">
        Not an exam. It finds where each subject starts for you, so your first timetable works on the right things. Questions get easier or harder as you go.
      </p>
      {!picked!.exact && (
        <p className="mt-3 flex items-start gap-2 rounded-lg bg-info-50 p-3 text-xs text-info-600">
          <Info className="mt-0.5 size-4 shrink-0" /> The class {draft.grade} form is still being written, so this demo uses the {file.form.title}.
        </p>
      )}
      <div className="mt-6">
        <OnboardingRunner data={data} learnerId={learnerId} finishHref="/onboarding/setup" />
      </div>
      <form action={deferTest} className="mt-6 border-t border-line pt-4 text-center">
        <Button variant="link" type="submit">Do it later from Assessments</Button>
      </form>
    </>
  );
}
