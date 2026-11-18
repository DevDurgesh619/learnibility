import type { ReactNode } from 'react';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { Logo } from '@/components/shell/logo';
import { SESSION_COOKIE, currentPersona } from '@/lib/session';
import { NEW_STUDENT_PERSONA_ID } from '@/components/onboarding/demo-auth';

/** Onboarding frame (PDF 1e-1i): logo and stepper, no sidebar. Only the signed-up student gets here. */
export default async function OnboardingLayout({ children }: { children: ReactNode }) {
  const persona = await currentPersona();
  const jar = await cookies();
  const signedUp = jar.get(SESSION_COOKIE)?.value === NEW_STUDENT_PERSONA_ID;
  if (!signedUp && persona?.role !== 'student') redirect('/signup');
  return (
    <div className="min-h-screen bg-canvas">
      <header className="mx-auto flex max-w-6xl items-center justify-between p-4 sm:p-6">
        <Logo href="/welcome" />
        <span className="text-xs text-subtle">You can change any of this later from your profile.</span>
      </header>
      <main className="mx-auto w-full max-w-2xl px-4 pb-16 sm:px-6">{children}</main>
    </div>
  );
}
