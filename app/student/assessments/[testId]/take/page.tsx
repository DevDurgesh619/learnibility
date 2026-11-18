import type { Metadata } from 'next';
import { notFound, redirect } from 'next/navigation';
import { getQuestion, getStudent } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import type { Question } from '@/lib/types';
import { submitInitialTest, submitTest } from '@/lib/actions/assessment';
import { getAssessment, testHref } from '@/components/assessment/catalog';
import { TestPlayer } from '@/components/assessment/test-player';
import type { PlayerItem } from '@/components/assessment/types';
import { InitialTestTake } from '@/components/assessment/initial-test-take';
import { loadOnboardingForm } from '@/components/onboarding/forms';
import { runnerData } from '@/components/onboarding/runner-data';
import { getChapter } from '@/lib/data';

export const metadata: Metadata = { title: 'Test in progress · Learnibility' };

function toItem(q: Question): PlayerItem {
  const sub = getChapter(q.chapterId)?.subtopics.find((s) => s.id === q.subtopicId);
  return {
    id: q.id,
    topic: sub?.name ?? getChapter(q.chapterId)?.chapter.name ?? '',
    kind: q.type === 'mcq' && q.options?.length ? 'mcq' : q.type === 'numerical' ? 'numerical' : 'text',
    stem: q.stem,
    options: q.options,
    marks: q.marks,
    minutes: q.minutes,
  };
}

/** PDF 8d-8e: full-screen test with timer, number strip, flag and confidence. Answers never reach the browser. */
export default async function TakeTestPage({ params }: { params: Promise<{ testId: string }> }) {
  const persona = await currentPersona();
  if (!persona) redirect('/login');
  const testId = decodeURIComponent((await params).testId);
  const test = await getAssessment(testId, persona.id);
  if (!test) notFound();
  if (test.tier === 'paid' && getStudent(persona.id)?.plan !== 'full_package') redirect(testHref(test.id));

  if (test.kind === 'onboarding' && test.formId && test.section) {
    const file = await loadOnboardingForm(test.formId);
    if (!file) notFound();
    return (
      <InitialTestTake
        data={runnerData(file)}
        learnerId={persona.id}
        section={test.section}
        title={test.title}
        onSubmit={submitInitialTest.bind(null, test.formId, test.section)}
      />
    );
  }

  const items = test.questionIds.map(getQuestion).filter((q): q is Question => !!q).map(toItem);
  return (
    <TestPlayer
      title={test.title}
      minutes={test.minutes}
      items={items}
      storageKey={`learnibility:test:${persona.id}:${test.id}`}
      onSubmit={submitTest.bind(null, test.id)}
      exitHref={testHref(test.id)}
    />
  );
}
