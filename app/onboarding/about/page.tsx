import type { Metadata } from 'next';
import { cookies } from 'next/headers';
import { AboutForm } from '@/components/onboarding/about-form';
import { DRAFT_COOKIE, parseDraft } from '@/components/onboarding/draft';
import { Stepper } from '@/components/onboarding/stepper';
import { getStudent } from '@/lib/data';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'About you · Learnibility' };

/** PDF 1e: name, class, board, age and main target (a dropdown, so it can drive Home and the timetable). */
export default async function AboutPage() {
  const saved = parseDraft((await cookies()).get(DRAFT_COOKIE)?.value);
  // A learner the sales team already converted has name, class and board on record: start from those.
  const persona = await currentPersona();
  const known = persona?.role === 'student' ? getStudent(persona.id) : undefined;
  const draft = known
    ? { name: known.name, grade: known.grade, board: known.board, stream: known.stream, ...Object.fromEntries(Object.entries(saved).filter(([, v]) => v !== undefined && v !== '')) }
    : saved;
  return (
    <>
      <Stepper current={0} />
      <h1 className="text-2xl font-semibold tracking-tight text-ink">Tell us about you</h1>
      <p className="mt-1 text-sm text-muted">This sets your syllabus, your starting test and your first timetable.</p>
      <AboutForm draft={draft} />
    </>
  );
}
