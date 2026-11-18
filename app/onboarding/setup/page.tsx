import type { Metadata } from 'next';
import { cookies } from 'next/headers';
import { DRAFT_COOKIE, parseDraft } from '@/components/onboarding/draft';
import { pickOnboardingForm } from '@/components/onboarding/forms';
import { SetupProgress } from '@/components/onboarding/setup-progress';
import { NEW_STUDENT_PERSONA_ID } from '@/components/onboarding/demo-auth';
import { SESSION_COOKIE } from '@/lib/session';

export const metadata: Metadata = { title: 'Setting up your space · Learnibility' };

/** PDF 1i: a short transition that saves everything and explains why Home already has a plan. */
export default async function SetupPage() {
  const jar = await cookies();
  const draft = parseDraft(jar.get(DRAFT_COOKIE)?.value);
  const formId = draft.board && draft.grade ? pickOnboardingForm(draft.board, draft.grade, draft.stream ?? 'none')?.row.formId ?? null : null;
  const learnerId = jar.get(SESSION_COOKIE)?.value ?? NEW_STUDENT_PERSONA_ID;
  return <SetupProgress formId={formId} learnerId={learnerId} firstName={(draft.name ?? '').split(' ')[0]} />;
}
