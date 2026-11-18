import type { Metadata } from 'next';
import { redirect } from 'next/navigation';
import { AuthFrame } from '@/components/onboarding/auth-card';
import { OtpForm } from '@/components/onboarding/otp-form';
import { isValidIndianMobile, normalisePhone } from '@/components/onboarding/demo-auth';

export const metadata: Metadata = { title: 'Verify your number · Learnibility' };

/** PDF 1c: 6-digit code with error and resend states. */
export default async function VerifyPage({ searchParams }: { searchParams: Promise<{ phone?: string }> }) {
  const phone = normalisePhone((await searchParams).phone ?? '');
  if (!isValidIndianMobile(phone)) redirect('/signup');
  return (
    <AuthFrame>
      <OtpForm phone={phone} />
    </AuthFrame>
  );
}
