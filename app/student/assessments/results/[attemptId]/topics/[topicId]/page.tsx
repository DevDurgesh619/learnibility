import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound, redirect } from 'next/navigation';
import { BookOpen, CheckCircle2, ChevronLeft, Star, XCircle } from 'lucide-react';
import { Avatar } from '@/components/ui/avatar';
import { GapBadge, LEVEL_LABEL } from '@/components/ui/badge';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { getAttempt, getCurrentPlan, getStudent, getTutor, getTutorMatches } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import { formatHours, formatInr } from '@/lib/format';
import { cn } from '@/lib/utils';
import { STRENGTH_CLASS, buildReport, plainCause } from '@/components/assessment/results';
import { resultHref, testHref } from '@/components/assessment/catalog';

export const metadata: Metadata = { title: 'Topic detail · Learnibility' };

const LETTERS = ['A', 'B', 'C', 'D', 'E'];

function optionLabel(options: string[] | undefined, v: string | undefined): string {
  if (!v) return 'Blank';
  const i = options?.indexOf(v) ?? -1;
  return i >= 0 ? `${LETTERS[i]} · ${v}` : v;
}

/** PDF 8h: each question with your answer, the right one and "why you chose this", the fix, and a matched tutor. */
export default async function TopicDetailPage({ params }: { params: Promise<{ attemptId: string; topicId: string }> }) {
  const persona = await currentPersona();
  if (!persona) redirect('/login');
  const p = await params;
  const attempt = getAttempt(decodeURIComponent(p.attemptId));
  if (!attempt || attempt.learnerId !== persona.id) notFound();
  const topicId = decodeURIComponent(p.topicId);
  const r = buildReport(attempt);
  const topic = r.topics.find((t) => t.id === topicId);
  if (!topic) notFound();
  const items = r.items.filter((i) => i.question.subtopicId === topicId || i.question.chapterId === topicId);
  const wrong = items.filter((i) => !i.correct);
  const right = items.filter((i) => i.correct);

  const student = getStudent(persona.id);
  const gap = topic.gap;
  const gapPlan = gap ? getCurrentPlan(persona.id)?.plan.gaps.find((g) => g.gapId === gap.id || g.subtopicId === gap.subtopicId) : undefined;
  const match = topic.strength !== 'Strong' ? getTutorMatches(persona.id, { subjectId: attempt.subjectId, limit: 1 })[0] : undefined;
  const tutor = match ? getTutor(match.tutorId) : undefined;
  const chapterCheck = items[0] ? `chk.${items[0].question.chapterId}` : undefined;

  return (
    <>
      <Link href={`${resultHref(attempt.id)}/gaps`} className="mb-3 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" /> Gap analysis</Link>
      <h1 className="text-2xl font-semibold tracking-tight text-ink">
        {topic.name} · {topic.correct}/{topic.questions} correct · <span className={STRENGTH_CLASS[topic.strength]}>{topic.strength}</span>
      </h1>
      <p className="mt-1 text-sm text-muted">{r.title}</p>

      <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_340px]">
        <div className="flex flex-col gap-3">
          {items.length === 0 && <Card className="p-5 text-sm text-muted">No questions from this topic in the test.</Card>}
          {[...wrong, ...right].map((it) => (
            <Card key={it.question.id} className={cn('p-4', !it.correct && 'border-danger-600/30')}>
              <div className="flex items-start gap-2">
                {it.correct ? <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-success-700" /> : <XCircle className="mt-0.5 size-4 shrink-0 text-danger-600" />}
                <p className="whitespace-pre-line text-sm text-ink"><span className="font-semibold">Q{it.n}</span> {it.question.stem}</p>
              </div>
              <div className="mt-3 flex flex-wrap gap-2 pl-6 text-xs">
                <span className={cn('rounded-full px-2.5 py-1 ring-1', it.correct ? 'bg-success-50 text-success-700 ring-success-600/20' : 'bg-danger-50 text-danger-700 ring-danger-600/20')}>
                  Your answer: {optionLabel(it.question.options, it.answer)}
                </span>
                {!it.correct && (
                  <span className="rounded-full bg-success-50 px-2.5 py-1 text-success-700 ring-1 ring-success-600/20">Correct: {optionLabel(it.question.options, it.question.answer)}</span>
                )}
                <span className="rounded-full bg-surface-muted px-2.5 py-1 text-muted">{it.blank ? 'Not answered' : `${it.secondsTaken} s${it.confidence ? ` · sure ${it.confidence}/5` : ''}`}</span>
              </div>
              {!it.correct && (
                <div className="mt-3 pl-6 text-sm">
                  <p className="text-muted"><span className="font-medium text-ink">Why you likely missed it:</span> {it.why}</p>
                  <p className="mt-2 text-muted"><span className="font-medium text-ink">Worked answer:</span> {it.question.markingKey}</p>
                </div>
              )}
            </Card>
          ))}
        </div>

        <aside className="flex flex-col gap-4">
          {(gap || topic.diagnosis) && (
            <Card>
              <CardHeader title="What we found" />
              <CardBody className="flex flex-col gap-2 pt-3 text-sm">
                <div className="flex flex-wrap gap-2">
                  {gap ? <GapBadge code={gap.code} /> : topic.diagnosis?.primary && <GapBadge code={topic.diagnosis.primary} />}
                  {(gap?.secondaryFlags ?? topic.diagnosis?.secondaryFlags ?? []).map((f) => <GapBadge key={f} code={f} />)}
                </div>
                <p className="text-muted">Level: {LEVEL_LABEL[gap?.level ?? topic.diagnosis?.level ?? 0]}</p>
                {gap && <p className="text-muted">About {formatHours(gap.hoursToClose)} to close{gap.weeks ? `, over ${gap.weeks} weeks` : ''}. Status: {gap.status === 'suspected' ? 'suspected, a chapter check confirms it' : gap.status}.</p>}
                {plainCause(gap?.likelyCauses ?? topic.diagnosis?.likelyCauses) && <p className="text-muted">Likely cause: {plainCause(gap?.likelyCauses ?? topic.diagnosis?.likelyCauses)}</p>}
              </CardBody>
            </Card>
          )}

          {match && tutor && (
            <Card className="border-success-600/30 bg-success-50/50">
              <CardHeader title="Learn from our recommendation" />
              <CardBody className="pt-3">
                <div className="flex items-center gap-3">
                  <Avatar name={tutor.displayName} personId={tutor.id} photo />
                  <div className="min-w-0">
                    <p className="font-medium text-ink">{tutor.displayName}</p>
                    <p className="flex items-center gap-1 text-xs text-muted"><Star className="size-3 fill-current text-warning-600" /> {tutor.rating} · {formatInr(match.pricePerHourInr)}/hr</p>
                  </div>
                </div>
                <p className="mt-3 text-sm text-muted">{match.reason}</p>
                <Link href={`/student/tutors/${tutor.id}`} className={cn(buttonVariants({ size: 'sm' }), 'mt-4')}>Book a free demo</Link>
              </CardBody>
            </Card>
          )}

          <Card>
            <CardHeader title="Practice" description={gapPlan ? 'Free steps from your plan' : 'Close this topic for free'} />
            <CardBody className="flex flex-col gap-3 pt-3 text-sm">
              {gapPlan ? (
                gapPlan.steps.slice(0, 2).map((s) => (
                  <div key={s.interventionId} className="flex gap-2">
                    <BookOpen className="mt-0.5 size-4 shrink-0 text-brand-600" />
                    <div>
                      <p className="font-medium text-ink">{s.name}</p>
                      <p className="text-xs text-muted">{s.timeCost}</p>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-muted">{items.length} questions on {topic.name}. Redo the ones you missed, then take the chapter check again in a week.</p>
              )}
              {gapPlan && <p className="text-xs text-subtle">{gapPlan.retestRule}</p>}
              {chapterCheck && <Link href={testHref(chapterCheck)} className={buttonVariants({ size: 'sm', variant: 'secondary' })}>Take the chapter check</Link>}
            </CardBody>
          </Card>
          {!student?.onboardedUtc && <p className="text-xs text-subtle">Tip: finish your starting tests so tutor matches use all your subjects.</p>}
        </aside>
      </div>
    </>
  );
}
