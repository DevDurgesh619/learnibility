import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound, redirect } from 'next/navigation';
import { ArrowRight, ChevronLeft, Lock } from 'lucide-react';
import { buttonVariants } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { getStudent } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import { getAssessment, testHref } from '@/components/assessment/catalog';

export const metadata: Metadata = { title: 'Test overview · Learnibility' };

const RESULT: Record<string, string> = {
  onboarding: 'Your starting level in this subject, suspected gaps, and a first plan in your timetable',
  chapter_check: 'Gap analysis per subtopic (what kind of gap and hours to close it), a re-planned week and tutor suggestions',
  practice_form: 'Score per subtopic and whether last week’s plan worked',
  mock: 'Exam-style score, gap analysis per chapter and time management',
  assigned: 'Gap analysis per topic, shared with whoever assigned it',
};

/** PDF 8b: same facts as the PDF plus "What you'll get". */
export default async function TestOverviewPage({ params }: { params: Promise<{ testId: string }> }) {
  const persona = await currentPersona();
  if (!persona) redirect('/login');
  const testId = decodeURIComponent((await params).testId);
  const test = await getAssessment(testId, persona.id);
  if (!test) notFound();
  const locked = test.tier === 'paid' && getStudent(persona.id)?.plan !== 'full_package';
  const rows: [string, string][] = [
    ['Questions', String(test.questions)],
    ['Type', test.questionTypes.join(', ')],
    ['Time', `${test.minutes} min · the timer starts when you begin`],
    ['Marks', String(test.marks)],
    ['Topics', test.topics.slice(0, 8).join(' · ') + (test.topics.length > 8 ? ` and ${test.topics.length - 8} more` : '')],
    ['What you get', RESULT[test.kind] ?? 'Gap analysis per topic and recommendations'],
  ];
  return (
    <>
      <Link href="/student/assessments" className="mb-3 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" /> Assessments</Link>
      <h1 className="text-2xl font-semibold tracking-tight text-ink">{test.title}</h1>
      <p className="mt-1 text-sm text-muted">{test.subtitle}</p>
      <Card className="mt-6 overflow-hidden">
        <dl className="divide-y divide-line">
          {rows.filter(([, v]) => v).map(([k, v]) => (
            <div key={k} className="grid gap-1 px-5 py-3 text-sm sm:grid-cols-[160px_1fr]">
              <dt className="text-muted">{k}</dt>
              <dd className="font-medium text-ink">{v}</dd>
            </div>
          ))}
        </dl>
      </Card>
      <div className="mt-6 flex justify-end">
        {locked ? (
          <span className={buttonVariants({ variant: 'secondary' })}><Lock /> Part of the Full package</span>
        ) : (
          <Link href={`${testHref(test.id)}/instructions`} className={buttonVariants()}>Continue <ArrowRight /></Link>
        )}
      </div>
    </>
  );
}
