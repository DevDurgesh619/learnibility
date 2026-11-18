import type { Metadata } from 'next';
import { cookies } from 'next/headers';
import { AboutForm } from '@/components/onboarding/about-form';
import { DRAFT_COOKIE, parseDraft } from '@/components/onboarding/draft';
import { Stepper } from '@/components/onboarding/stepper';

export const metadata: Metadata = { title: 'About you · Learnibility' };

/** PDF 1e: name, class, board, age and main target (a dropdown, so it can drive Home and the timetable). */
export default async function AboutPage() {
  const draft = parseDraft((await cookies()).get(DRAFT_COOKIE)?.value);
  return (
    <>
      <Stepper current={0} />
      <h1 className="text-2xl font-semibold tracking-tight text-ink">Tell us about you</h1>
      <p className="mt-1 text-sm text-muted">This sets your syllabus, your starting test and your first timetable.</p>
      <AboutForm draft={draft} />
    </>
  );
}
