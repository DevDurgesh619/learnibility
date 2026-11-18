'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { newId, nowStamp, putRecord, recomputeLearner, appendEvent } from '@/lib/actions/core';
import { getQuestion, getStudent, getTasks, type Attempt } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import type { ItemResponse } from '@/lib/types';
import { getAssessment, resultHref } from '@/components/assessment/catalog';
import { markAnswer } from '@/components/assessment/marking';
import type { PlayerSubmission } from '@/components/assessment/types';
import { completeOnboardingFor } from '@/components/onboarding/complete';
import { loadOnboardingForm } from '@/components/onboarding/forms';
import type { OnboardingResponses } from '@/lib/onboarding/score';

async function learner() {
  const p = await currentPersona();
  if (!p || p.role !== 'student') redirect('/login');
  return p.id;
}

/**
 * PDF 8d → 8f. Marks the submission on the server, writes the attempt, re-runs gaps, plan and timetable
 * (recomputeLearner), closes the matching test task if one was due, and opens the result summary.
 */
export async function submitTest(testId: string, submission: PlayerSubmission): Promise<void> {
  const learnerId = await learner();
  const test = await getAssessment(testId, learnerId);
  if (!test) redirect('/student/assessments');
  const submitted = nowStamp();
  const responses: ItemResponse[] = test.questionIds.map((id) => {
    const q = getQuestion(id);
    const r = submission.responses.find((x) => x.questionId === id);
    const answer = r?.answer?.trim() || undefined;
    return {
      questionId: id,
      correct: q ? markAnswer(q, answer) : false,
      secondsTaken: Math.max(0, Math.round(r?.secondsTaken ?? 0)),
      ...(r?.confidence ? { confidence: r.confidence } : {}),
      ...(answer ? { answer } : {}),
    };
  });
  const marks = (id: string) => getQuestion(id)?.marks ?? 1;
  const task = getTasks(learnerId, undefined, { status: 'todo' }).find(
    (t) => testId === `task.${t.id}` || t.refId === testId || t.href?.includes(encodeURIComponent(testId)) || t.href?.endsWith(testId),
  );
  const attempt: Attempt = {
    id: newId('att'),
    learnerId,
    kind: test.kind,
    title: test.title,
    subjectId: test.subjectId,
    ...(test.chapterId ? { chapterId: test.chapterId } : {}),
    ...(task ? { taskId: task.id, ...(task.createdBy ? { assignedBy: task.createdBy } : {}) } : {}),
    questionIds: test.questionIds,
    responses,
    startedUtc: new Date(Date.parse(submitted) - submission.elapsedSeconds * 1000).toISOString(),
    submittedUtc: submitted,
    minutesAllotted: test.minutes,
    score: responses.reduce((s, r) => s + (r.correct ? marks(r.questionId) : 0), 0),
    maxScore: test.questionIds.reduce((s, id) => s + marks(id), 0),
    status: 'submitted',
  };
  putRecord('attempts', attempt);
  appendEvent(learnerId, {
    sourceMethod: 'M9',
    type: 'test_submitted',
    payload: { attemptId: attempt.id, testId, autoSubmitted: submission.autoSubmitted, flagged: submission.responses.filter((r) => r.flagged).map((r) => r.questionId) },
  });
  if (task) putRecord('tasks', { ...task, status: 'done', completedUtc: submitted });
  recomputeLearner(learnerId);
  revalidatePath('/student', 'layout');
  redirect(resultHref(attempt.id));
}

/** An initial (onboarding) test section taken from Assessments: re-scores the starting profile with the new answers. */
export async function submitInitialTest(formId: string, section: string, responses: OnboardingResponses): Promise<void> {
  const learnerId = await learner();
  const student = getStudent(learnerId);
  const file = await loadOnboardingForm(formId);
  if (!student || !file) redirect('/student/assessments');
  const byId = new Map(file.items.map((i) => [i.id, i]));
  const academic = responses.academic.map((r) => {
    const it = byId.get(r.questionId) as { answer?: string } | undefined;
    const answer = (r as { answer?: string }).answer;
    return { ...r, correct: answer !== undefined && it?.answer !== undefined ? answer === it.answer : r.correct };
  });
  completeOnboardingFor({
    learnerId,
    draft: { name: student.name, board: student.board, grade: student.grade, stream: student.stream, school: student.school || undefined },
    file,
    responses: { academic, reasoning: responses.reasoning, survey: responses.survey },
  });
  revalidatePath('/student', 'layout');
  const isAcademic = file.form.scoring.groups.some((g) => g.group === section);
  redirect(isAcademic ? resultHref(`att_${learnerId.replace(/^lrn_/, '')}_onb_${section}`) : '/student/assessments?done=' + section);
}
