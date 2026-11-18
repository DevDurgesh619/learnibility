import type { Metadata } from 'next';
import { AuthFrame } from '@/components/onboarding/auth-card';
import { PhoneForm } from '@/components/onboarding/phone-form';

export const metadata: Metadata = { title: 'Log in or sign up · Learnibility' };

/** PDF 1b: one door for new and returning users. */
export default function SignupPage() {
  return (
    <AuthFrame>
      <PhoneForm />
    </AuthFrame>
  );
}
