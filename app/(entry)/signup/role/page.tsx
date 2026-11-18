import type { Metadata } from 'next';
import { AuthFrame } from '@/components/onboarding/auth-card';
import { RolePicker } from '@/components/onboarding/role-picker';

export const metadata: Metadata = { title: 'Who are you? · Learnibility' };

/** PDF 1d: branches into four flows; the student flow continues into onboarding. */
export default function RolePage() {
  return (
    <AuthFrame wide>
      <RolePicker />
    </AuthFrame>
  );
}
