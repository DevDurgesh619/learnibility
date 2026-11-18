import type { Metadata } from 'next';
import { cookies } from 'next/headers';
import { DRAFT_COOKIE, parseDraft } from '@/components/onboarding/draft';
import { NeedsForm } from '@/components/onboarding/needs-form';
import { Stepper } from '@/components/onboarding/stepper';

export const metadata: Metadata = { title: 'What do you want help with? · Learnibility' };

/** PDF 1f: a saved preference (multi-select). Nothing is hidden; it only sets where Home starts. */
export default async function NeedsPage() {
  const draft = parseDraft((await cookies()).get(DRAFT_COOKIE)?.value);
  return (
    <>
      <Stepper current={1} />
      <h1 className="text-2xl font-semibold tracking-tight text-ink">What do you want help with?</h1>
      <p className="mt-1 text-sm text-muted">Pick any. You&apos;ll still see everything; this just tells us where to start.</p>
      <NeedsForm initial={draft.needs ?? ['progress']} grade={draft.grade} />
    </>
  );
}
