import type { Metadata } from 'next';
import Link from 'next/link';
import { Clock } from 'lucide-react';
import { getTutor } from '@/components/marketplace/queries';
import { OnboardingFlow } from '@/components/tutor/onboarding-flow';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { saveTutorPrefs } from '@/lib/actions/tutor';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Set up your profile · Tutor' };

/** Tutor HTML 1a-1h (flow) and 1i (published, under review). */
export default async function OnboardingPage({ searchParams }: { searchParams: Promise<{ step?: string }> }) {
  const sp = await searchParams;
  const persona = (await currentPersona())!;
  const t = getTutor(persona.id)!;
  if (sp.step === 'done') {
    return (
      <Card className="mx-auto max-w-xl"><CardBody className="py-10 text-center">
        <div className="mx-auto mb-3 flex size-12 items-center justify-center rounded-full bg-brand-50 text-brand-600"><Clock className="size-6" /></div>
        <h1 className="text-xl font-semibold text-ink">You&apos;re published. Verification takes up to 24 hours.</h1>
        <p className="mx-auto mt-2 max-w-md text-sm text-muted">Students can already find you and book a demo. Your Verified badge appears once documents are checked. We&apos;ll notify you.</p>
        <div className="mt-6 flex justify-center gap-2"><Link href="/tutor" className={buttonVariants()}>Go to Home</Link><Link href="/tutor/profile" className={buttonVariants({ variant: 'secondary' })}>Edit profile</Link></div>
      </CardBody></Card>
    );
  }
  return <OnboardingFlow action={saveTutorPrefs} seed={{ name: t.displayName, city: t.city, availability: t.availability, oneToOne: t.pricing.oneToOnePerHourInr, group: t.pricing.groupPerStudentPerHourInr, feeRate: t.platformFeeRate ?? 0.15, identityDone: false }} />;
}
