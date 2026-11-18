import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound, redirect } from 'next/navigation';
import { ArrowRight, CalendarCheck2, ChevronLeft, Clock, Target } from 'lucide-react';
import { BandBadge } from '@/components/ui/badge';
import { buttonVariants } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { getAttempt, getGaps } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import { formatHours } from '@/lib/format';
import { buildReport } from '@/components/assessment/results';
import { resultHref } from '@/components/assessment/catalog';

export const metadata: Metadata = { title: 'Result · Learnibility' };

/** PDF 8f: score, band and time used, one line of takeaway, then on to the gap analysis. Feeds Home metrics. */
export default async function ResultPage({ params }: { params: Promise<{ attemptId: string }> }) {
  const persona = await currentPersona();
  if (!persona) redirect('/login');
  const attempt = getAttempt(decodeURIComponent((await params).attemptId));
  if (!attempt || attempt.learnerId !== persona.id) notFound();
  const r = buildReport(attempt);
  const newGaps = getGaps(persona.id, { status: 'open' }).filter((g) => g.attemptId === attempt.id || (attempt.kind === 'onboarding' && g.subjectId === attempt.subjectId));
  const hours = newGaps.reduce((s, g) => s + g.hoursToClose, 0);
  const strong = r.topics.filter((t) => t.strength === 'Strong').slice(0, 2);
  return (
    <>
      <Link href="/student/assessments" className="mb-3 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" /> Assessments</Link>
      <div className="mx-auto flex max-w-2xl flex-col items-center text-center">
        <p className="text-sm text-muted">{r.subjectName}</p>
        <h1 className="mt-1 text-2xl font-semibold tracking-tight text-ink">{r.title} done</h1>
        <div className="mt-6 grid w-full grid-cols-3 gap-3">
          <Card className="p-4">
            <p className="text-2xl font-semibold tabular-nums text-ink sm:text-3xl">{r.score}<span className="text-base text-muted">/{r.maxScore}</span></p>
            <p className="mt-1 text-xs text-muted">score · {r.percent}%</p>
          </Card>
          <Card className="flex flex-col items-center justify-center p-4">
            <BandBadge band={r.band} />
            <p className="mt-2 text-xs text-muted">overall band</p>
          </Card>
          <Card className="p-4">
            <p className="text-2xl font-semibold tabular-nums text-ink sm:text-3xl">{r.minutesUsed}<span className="text-base text-muted"> min</span></p>
            <p className="mt-1 text-xs text-muted">of {attempt.minutesAllotted} allowed</p>
          </Card>
        </div>
        <p className="mt-5 text-sm text-muted">
          {strong.length > 0 && <>Strong in {strong.map((t) => t.name).join(' and ')}. </>}
          {r.focus && <>Weakest: {r.focus.name}. </>}
          Saved to your Inventory.
        </p>
        {newGaps.length > 0 && (
          <Card className="mt-6 w-full border-brand-200 bg-brand-50/60 p-4 text-left">
            <p className="flex items-center gap-2 text-sm font-semibold text-ink"><CalendarCheck2 className="size-4 text-brand-600" /> Your week has been re-planned</p>
            <p className="mt-1 text-sm text-muted">
              {newGaps.length} {newGaps.length === 1 ? 'gap' : 'gaps'} to work on, about {formatHours(Math.round(hours * 10) / 10)} in total, now in your timetable as short blocks.
            </p>
          </Card>
        )}
        <div className="mt-6 flex flex-wrap justify-center gap-2">
          <Link href={`${resultHref(attempt.id)}/gaps`} className={buttonVariants()}><Target /> See gap analysis</Link>
          <Link href="/student/timetable" className={buttonVariants({ variant: 'secondary' })}><Clock /> Open timetable</Link>
          <Link href="/student/assessments" className={buttonVariants({ variant: 'ghost' })}>Back to Assessments <ArrowRight /></Link>
        </div>
      </div>
    </>
  );
}
