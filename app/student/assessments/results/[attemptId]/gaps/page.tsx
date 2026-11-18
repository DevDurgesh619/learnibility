import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound, redirect } from 'next/navigation';
import { ChevronLeft, ChevronRight, Target } from 'lucide-react';
import { Badge, GapBadge } from '@/components/ui/badge';
import { buttonVariants } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Table, TBody, TD, TH, THead, TR } from '@/components/ui/table';
import { getAttempt } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import { formatHours } from '@/lib/format';
import { cn } from '@/lib/utils';
import { STRENGTH_CLASS, buildReport, plainCause } from '@/components/assessment/results';
import { resultHref } from '@/components/assessment/catalog';

export const metadata: Metadata = { title: 'Gap analysis · Learnibility' };

/** PDF 8g: topic · questions · correct · incorrect · band, a "focus first" takeaway and the tutor link from 8h. */
export default async function GapAnalysisPage({ params }: { params: Promise<{ attemptId: string }> }) {
  const persona = await currentPersona();
  if (!persona) redirect('/login');
  const attempt = getAttempt(decodeURIComponent((await params).attemptId));
  if (!attempt || attempt.learnerId !== persona.id) notFound();
  const r = buildReport(attempt);
  const base = resultHref(attempt.id);
  const focus = r.focus;
  const focusWrong = focus ? focus.incorrect + focus.blank : 0;
  const subjectSlug = attempt.subjectId.replace(/^(cbse|cambridge|ib)-g\d+-/, '');

  return (
    <>
      <Link href={base} className="mb-3 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" /> Result</Link>
      <div className="mb-6 flex flex-wrap items-end justify-between gap-2">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-ink">Gap analysis · {r.title}</h1>
          <p className="mt-1 text-sm text-muted">{r.subjectName}</p>
        </div>
        <p className="text-sm text-muted">{r.score}/{r.maxScore} · {r.strength}</p>
      </div>

      <Card className="overflow-x-auto">
        <Table>
          <THead>
            <TR>
              <TH>Topic</TH>
              <TH className="hidden text-right sm:table-cell">Questions</TH>
              <TH className="text-right">Correct</TH>
              <TH className="hidden text-right sm:table-cell">Incorrect</TH>
              <TH>Band</TH>
              <TH className="hidden md:table-cell">Gap found</TH>
              <TH><span className="sr-only">Open</span></TH>
            </TR>
          </THead>
          <TBody>
            {r.topics.map((t) => (
              <TR key={t.id} className={cn(focus?.id === t.id && 'bg-danger-50/40')}>
                <TD className="max-w-[220px]">
                  <Link href={`${base}/topics/${encodeURIComponent(t.id)}`} className="font-medium text-ink hover:text-brand-700">{t.name}</Link>
                </TD>
                <TD className="hidden text-right tabular-nums sm:table-cell">{t.questions}</TD>
                <TD className="text-right tabular-nums">{t.correct}<span className="text-subtle sm:hidden">/{t.questions}</span></TD>
                <TD className="hidden text-right tabular-nums sm:table-cell">{t.incorrect + t.blank}</TD>
                <TD className={cn('font-semibold', STRENGTH_CLASS[t.strength])}>{t.strength}</TD>
                <TD className="hidden md:table-cell">
                  {t.gap ? <GapBadge code={t.gap.code} /> : t.diagnosis?.primary ? <GapBadge code={t.diagnosis.primary} /> : <span className="text-xs text-subtle">None</span>}
                </TD>
                <TD className="w-8 text-right">
                  <Link href={`${base}/topics/${encodeURIComponent(t.id)}`} aria-label={`Open ${t.name}`} className="text-subtle hover:text-ink"><ChevronRight className="size-4" /></Link>
                </TD>
              </TR>
            ))}
          </TBody>
        </Table>
      </Card>

      {focus ? (
        <Card className="mt-6 border-success-600/30 bg-success-50/60 p-5">
          <p className="flex items-center gap-2 font-semibold text-ink"><Target className="size-4 text-success-700" /> Focus first: {focus.name}</p>
          <p className="mt-1 text-sm text-muted">
            {focusWrong} of {focus.questions} wrong
            {focus.gap ? `, a ${focus.gap.code} gap (${plainCause(focus.gap.likelyCauses) ?? 'see the topic detail'}). About ${formatHours(focus.gap.hoursToClose)} to close, already planned into your timetable.` : '.'}
            {' '}Tap the row to see each question, or get help from a tutor who is strong in it.
          </p>
          <div className="mt-4 flex flex-wrap gap-2">
            <Link href={`${base}/topics/${encodeURIComponent(focus.id)}`} className={buttonVariants({ size: 'sm' })}>See these questions</Link>
            <Link href={`/student/tutors?subject=${subjectSlug}&topic=${encodeURIComponent(focus.name)}`} className={buttonVariants({ size: 'sm', variant: 'secondary' })}>Find a tutor for this</Link>
          </div>
        </Card>
      ) : (
        <Card className="mt-6 p-5">
          <p className="font-semibold text-ink">No weak topics in this test</p>
          <p className="mt-1 text-sm text-muted">Everything came out Strong. A review check in 7 days makes sure it sticks.</p>
        </Card>
      )}

      <div className="mt-4 flex flex-wrap items-center gap-2 text-xs text-subtle">
        <Badge>Band: Strong 75%+, Medium 50 to 74%, Weak under 50%</Badge>
        <span>Gap types follow the learning-science ladder (G1 prerequisite to G10 engagement).</span>
      </div>
    </>
  );
}
