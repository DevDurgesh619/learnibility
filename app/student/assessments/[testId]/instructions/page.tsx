import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound, redirect } from 'next/navigation';
import { ChevronLeft } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { currentPersona } from '@/lib/session';
import { getAssessment, testHref } from '@/components/assessment/catalog';
import { StartForm } from '@/components/assessment/start-form';

export const metadata: Metadata = { title: 'Before you start · Learnibility' };

/** PDF 8c: real instruction copy and the "I've read the instructions" check. */
export default async function InstructionsPage({ params }: { params: Promise<{ testId: string }> }) {
  const persona = await currentPersona();
  if (!persona) redirect('/login');
  const testId = decodeURIComponent((await params).testId);
  const test = await getAssessment(testId, persona.id);
  if (!test) notFound();
  const adaptive = test.kind === 'onboarding';
  const lines = adaptive
    ? [
        `About ${test.minutes} minutes. Pick a quiet time; you can stop between parts but not inside one.`,
        'Questions get easier or harder depending on your answers, so you cannot go back.',
        'If you have no idea, choose "I don\'t know" instead of guessing. It makes your plan more accurate.',
        'After each answer, tell us how sure you were (1 to 5). Being honest here matters as much as being right.',
      ]
    : [
        `You can't pause. Keep ${test.minutes} minutes free; the test submits itself when time runs out.`,
        'Move between questions with Prev and Next, or jump with the number strip at the top.',
        'Flag a question to come back to it. Flagged questions are listed before you submit.',
        'For each answer, tap how sure you are (1 to 5). It helps find careless slips and over-confidence.',
        'Write your working for long answers; marks are given for method, not only the final answer.',
        "Unanswered questions count as incorrect. There's no negative marking.",
      ];
  return (
    <>
      <Link href={testHref(test.id)} className="mb-3 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" /> {test.title}</Link>
      <h1 className="text-2xl font-semibold tracking-tight text-ink">Before you start</h1>
      <Card className="mt-6 p-5">
        <ol className="flex flex-col divide-y divide-dashed divide-line text-sm">
          {lines.map((l, i) => (
            <li key={i} className="flex gap-3 py-3 first:pt-0 last:pb-0">
              <span className="flex size-6 shrink-0 items-center justify-center rounded-full bg-brand-50 text-xs font-semibold text-brand-700">{i + 1}</span>
              <span className="pt-0.5 text-ink">{l}</span>
            </li>
          ))}
        </ol>
      </Card>
      <StartForm href={`${testHref(test.id)}/take`} />
    </>
  );
}
