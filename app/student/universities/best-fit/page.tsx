import Link from 'next/link';
import { redirect } from 'next/navigation';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Table, TBody, TD, TH, THead, TR } from '@/components/ui/table';
import { fitInputs, isPaid, studentCtx } from '@/components/applications/data';
import { readiness } from '@/components/applications/fit';
import { FitHeader } from '@/components/applications/fit-header';
import { currentPersona } from '@/lib/session';
import { cn } from '@/lib/utils';

export const metadata = { title: 'Best fit · University Fit · Learnibility' };

export default async function Page() {
  const persona = (await currentPersona())!;
  if (isPaid(studentCtx(persona.id).plan)) redirect('/student/applications');
  const { profile, sources } = fitInputs(persona.id);
  const r = readiness(profile, sources);
  return (
    <>
      <FitHeader active="best-fit" />
      <Card>
        <CardBody className="space-y-5">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-base font-semibold text-ink">Your profile is {r.pct}% ready</h2>
              <p className="text-sm text-muted">Fit is only as good as your profile. Add what&apos;s missing for a real estimate.</p>
            </div>
            <Progress value={r.pct / 100} className="h-3 sm:w-72" tone={r.pct >= 75 ? 'success' : r.pct >= 50 ? 'brand' : 'warning'} />
          </div>
          <Table>
            <THead><TR><TH>Signal</TH><TH>Rating</TH><TH>Where it comes from</TH></TR></THead>
            <TBody>
              {r.signals.map((s) => (
                <TR key={s.key}>
                  <TD className="font-medium text-ink">{s.label}</TD>
                  <TD className={cn(s.missing && 'font-medium text-danger-600')}>{s.missing ? 'Missing' : s.rating}</TD>
                  <TD className="text-muted">
                    {s.missing
                      ? <Link href="/student/universities/best-fit/profile" className="font-medium text-brand-700 underline-offset-2 hover:underline">{s.key === 'tests' ? 'Add SAT or IELTS score' : s.key === 'essay' ? 'Paste an essay draft' : s.key === 'activities' ? 'Add activities' : 'Add your grades'}</Link>
                      : s.source ?? 'from your profile'}
                  </TD>
                </TR>
              ))}
            </TBody>
          </Table>
          <div className="flex flex-wrap items-center gap-3">
            <Link href="/student/universities/best-fit/profile" className={buttonVariants({ variant: 'secondary' })}>Complete profile</Link>
            <Link href="/student/universities/best-fit/results" className={cn(buttonVariants(), r.pct === 0 && 'pointer-events-none opacity-50')} aria-disabled={r.pct === 0}>Check my best fit</Link>
            <span className="text-xs text-subtle">Wellbeing, family and budget answers are never used to score your fit.</span>
          </div>
        </CardBody>
      </Card>
    </>
  );
}
