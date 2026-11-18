import Link from 'next/link';
import { redirect } from 'next/navigation';
import { CheckCircle2, ChevronLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { APPLICATION_SUPPORT_PRICE_INR, SHOW_COSTS } from '@/components/applications/config';
import { isPaid, nameOf, studentCtx } from '@/components/applications/data';
import { formatInr } from '@/lib/format';
import { upgradeToApplicationSupport } from '@/lib/actions/applications';
import { currentPersona } from '@/lib/session';

export const metadata = { title: 'Application Support · Learnibility' };

const FEATURES = [
  ['A counsellor on your side', 'Builds your Reach, Target and Safe list with you and meets you through the season.'],
  ['Applications board', 'Every university from shortlist to decision, with checklists, risk flags and a QA check before you submit.'],
  ['Essay reviews', 'Write in the draft studio, get an instant AI pre-pass, then counsellor comments anchored to your text.'],
  ['Recommendation letters', 'Track who you asked, what is drafted and what has arrived.'],
  ['Meeting notes that turn into tasks', 'Action items from each meeting land in your timetable.'],
  ['Finance and visa', 'Scholarship forms, visa steps and appointments for the university you accept.'],
];

export default async function Page() {
  const persona = (await currentPersona())!;
  const ctx = studentCtx(persona.id);
  if (isPaid(ctx.plan)) redirect('/student/applications');

  async function start() {
    'use server';
    await upgradeToApplicationSupport();
    redirect('/student/applications');
  }

  return (
    <>
      <Link href="/student/universities/best-fit" className="mb-3 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" />University Fit</Link>
      <div className="grid grid-cols-[minmax(0,1fr)] gap-6 lg:grid-cols-[minmax(0,1fr)_340px]">
        <div>
          <p className="mb-1 text-xs font-medium tracking-wide text-brand-600 uppercase">Application Support</p>
          <h1 className="text-2xl font-semibold tracking-tight text-ink">Turn your fit results into applications</h1>
          <p className="mt-2 max-w-2xl text-sm text-muted">Everything you saved while exploring moves onto your applications board, and {ctx.counsellorId ? nameOf(ctx.counsellorId) : 'your counsellor'} picks it up from there.</p>
          <ul className="mt-6 grid gap-4 sm:grid-cols-2">
            {FEATURES.map(([t, d]) => (
              <li key={t} className="flex gap-3">
                <CheckCircle2 className="mt-0.5 size-5 shrink-0 text-success-600" />
                <div><p className="text-sm font-semibold text-ink">{t}</p><p className="text-sm text-muted">{d}</p></div>
              </li>
            ))}
          </ul>
        </div>
        <Card className="h-fit">
          <CardBody className="space-y-4">
            <p className="text-base font-semibold text-ink">Start Application Support</p>
            {SHOW_COSTS && <p><span className="text-3xl font-semibold tracking-tight text-ink">{formatInr(APPLICATION_SUPPORT_PRICE_INR)}</span><span className="text-sm text-muted"> / month</span></p>}
            <p className="text-sm text-muted">Your University Fit tab becomes your application command center. Your saved universities come with you.</p>
            <form action={start}><Button type="submit" className="w-full">Start Application Support</Button></form>
            <p className="text-xs text-subtle">Demo: no payment is taken. Reset the demo to go back to the free plan.</p>
          </CardBody>
        </Card>
      </div>
    </>
  );
}
