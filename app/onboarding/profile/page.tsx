import type { Metadata } from 'next';
import { cookies } from 'next/headers';
import { DRAFT_COOKIE, parseDraft } from '@/components/onboarding/draft';
import { ProfileForm } from '@/components/onboarding/profile-form';
import { PhotoPicker } from '@/components/onboarding/photo-picker';
import { Stepper } from '@/components/onboarding/stepper';
import { subjectsForStudent } from '@/components/onboarding/subjects';
import { photoFor } from '@/lib/media';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Your profile · Learnibility' };

/** PDF 1g (option A, chosen): in-depth profile questions with Skip; no paywall. Completion shows on Home. */
export default async function ProfilePage() {
  const draft = parseDraft((await cookies()).get(DRAFT_COOKIE)?.value);
  const persona = await currentPersona();
  const subjects = draft.board && draft.grade ? subjectsForStudent(draft.board, draft.grade, draft.stream ?? 'none') : [];
  return (
    <>
      <Stepper current={2} />
      <h1 className="text-2xl font-semibold tracking-tight text-ink">A few more details for better recommendations</h1>
      <p className="mt-1 text-sm text-muted">Takes about 2 minutes. You can finish this later from Home.</p>
      <div className="mt-6"><PhotoPicker name={draft.name ?? persona?.name ?? 'You'} demoPhoto={photoFor(persona?.id) ?? photoFor('lrn_zoya_fernandes')} /></div>
      <ProfileForm draft={draft} subjects={subjects.map((s) => ({ id: s.id, name: s.name }))} />
    </>
  );
}
