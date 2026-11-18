import 'server-only';
import { getAttempts, getChapter, getQuestion, getQuestions, getStudent, getSubject, getTasks, type Attempt, type AttemptKind, type Student } from '@/lib/data';
import type { Question, Subtopic } from '@/lib/types';
import { loadOnboardingForm, pickOnboardingForm } from '@/components/onboarding/forms';
import { runnerData } from '@/components/onboarding/runner-data';

/**
 * Which tests a student can take (PDF 8a), and the exact questions in each.
 *
 * Test IDs (URL-safe):  onb.{formId}.{section}  initial test (one onboarding section)
 *                       chk.{chapterId}         chapter check: the student-check path per subtopic (L 5, S 6, H 8 items)
 *                       pfa.{chapterId} / pfb.{chapterId}  practice forms A and B
 *                       mock.{subjectId}.{n}    full-syllabus mock (paid)
 *                       task.{taskId}           a test assigned as a task (teacher, tutor), questions from the task
 */
export interface AssessmentDef {
  id: string;
  kind: AttemptKind;
  title: string;
  /** e.g. "Mathematics · Chapter 3" */
  subtitle: string;
  subjectId: string;
  subjectName: string;
  chapterId?: string;
  questionIds: string[];
  questions: number;
  minutes: number;
  marks: number;
  /** Subtopic or chapter names covered. */
  topics: string[];
  questionTypes: string[];
  tier: 'free' | 'paid';
  /** Onboarding sections only. */
  formId?: string;
  section?: string;
}

const PATH_LENGTH: Record<Subtopic['weight'], number> = { L: 5, S: 6, H: 8 };
const TYPE_LABEL: Record<string, string> = { mcq: 'Multiple choice', short: 'Short answer', numerical: 'Numerical', explain: 'Explain', multi_step: 'Multi-step', case: 'Case-based', long: 'Long answer' };

/** The student-check path of each subtopic: first N mastery-bank items in bank order (C1 → C4, from D2). */
export function chapterCheckQuestions(chapterId: string): Question[] {
  const ch = getChapter(chapterId);
  if (!ch) return [];
  const bank = getQuestions({ chapterId, set: 'mastery_bank' });
  return ch.subtopics.flatMap((st) => bank.filter((q) => q.subtopicId === st.id).sort((a, b) => a.id.localeCompare(b.id)).slice(0, PATH_LENGTH[st.weight] ?? 6));
}

function def(base: Omit<AssessmentDef, 'questionIds' | 'questions' | 'minutes' | 'marks' | 'questionTypes'>, qs: Question[]): AssessmentDef {
  return {
    ...base,
    questionIds: qs.map((q) => q.id),
    questions: qs.length,
    minutes: Math.max(5, Math.ceil(qs.reduce((s, q) => s + q.minutes, 0))),
    marks: qs.reduce((s, q) => s + q.marks, 0),
    questionTypes: [...new Set(qs.map((q) => TYPE_LABEL[q.type] ?? q.type))],
  };
}

export async function getAssessment(testId: string, learnerId: string): Promise<AssessmentDef | undefined> {
  const [kind, ...rest] = testId.split('.');
  if (kind === 'onb') {
    const [formId, section] = rest;
    const initial = await initialTests(learnerId);
    return initial.find((t) => t.formId === formId && t.section === section);
  }
  if (kind === 'chk' || kind === 'pfa' || kind === 'pfb') {
    const chapterId = rest.join('.');
    const ch = getChapter(chapterId);
    if (!ch) return undefined;
    const qs = kind === 'chk' ? chapterCheckQuestions(chapterId) : getQuestions({ chapterId, set: kind === 'pfa' ? 'practice_form_a' : 'practice_form_b' });
    if (!qs.length) return undefined;
    const label = kind === 'chk' ? 'Chapter check' : `Practice test ${kind === 'pfa' ? 'A' : 'B'}`;
    return def(
      {
        id: testId, kind: kind === 'chk' ? 'chapter_check' : 'practice_form', title: `${ch.chapter.name} · ${label}`,
        subtitle: `${ch.subject.name} · Chapter ${ch.chapter.order}`, subjectId: ch.subject.id, subjectName: ch.subject.name, chapterId,
        topics: ch.subtopics.map((s) => s.name), tier: 'free',
      },
      qs,
    );
  }
  if (kind === 'task') {
    // A test someone assigned (teacher re-teach set, tutor test): the task carries its question IDs.
    const task = getTasks(learnerId).find((t) => t.id === rest.join('.'));
    const qs = (task?.questionIds ?? []).map(getQuestion).filter((q): q is Question => !!q);
    if (!task || !qs.length) return undefined;
    const ch = getChapter(qs[0].chapterId);
    return def(
      {
        id: testId, kind: 'assigned', title: task.title, subtitle: `${ch?.subject.name ?? ''}${task.detail ? ` · ${task.detail}` : ''}`,
        subjectId: qs[0].subjectId, subjectName: ch?.subject.name ?? qs[0].subjectId, chapterId: new Set(qs.map((q) => q.chapterId)).size === 1 ? qs[0].chapterId : undefined,
        topics: [...new Set(qs.map((q) => getChapter(q.chapterId)?.subtopics.find((s) => s.id === q.subtopicId)?.name ?? q.subtopicId))], tier: 'free',
      },
      qs,
    );
  }
  if (kind === 'mock') {
    const [subjectId, n] = rest;
    const sub = getSubject(subjectId);
    const qs = getQuestions({ subjectId, set: 'mock' }).filter((q) => q.id.startsWith(`${subjectId}-mock${n}-`));
    if (!sub || !qs.length) return undefined;
    return def(
      { id: testId, kind: 'mock', title: `${sub.subject.name} · Mock ${n}`, subtitle: `${sub.subject.programme} · full syllabus`, subjectId, subjectName: sub.subject.name, topics: sub.chapters.map((c) => c.name), tier: 'paid' },
      qs,
    );
  }
  return undefined;
}

/** Initial tests: one card per onboarding section (PDF 8a "Initial tests · free"). */
export async function initialTests(learnerId: string): Promise<AssessmentDef[]> {
  const student = getStudent(learnerId);
  if (!student) return [];
  const picked = pickOnboardingForm(student.board, student.grade, student.stream);
  const file = picked && (await loadOnboardingForm(picked.row.formId));
  if (!file) return [];
  const data = runnerData(file);
  return data.sections.map((s) => {
    const group = file.form.scoring.groups.find((g) => g.group === s.key);
    const ids =
      s.kind === 'academic' ? data.academic.filter((a) => a.group === s.key).map((a) => a.id) : s.kind === 'reasoning' ? data.reasoning.map((r) => r.id) : data.survey.map((r) => r.id);
    return {
      id: `onb.${file.form.formId}.${s.key}`,
      kind: 'onboarding' as const,
      title: s.kind === 'academic' ? s.label : s.kind === 'reasoning' ? 'Reasoning' : 'About you',
      subtitle: s.kind === 'academic' ? 'Starting test · adapts to your answers' : s.kind === 'reasoning' ? 'Numbers, words, patterns, shapes' : 'Habits, interests and goals',
      subjectId: group?.subjectIds[0] ?? 'general',
      subjectName: s.label,
      questionIds: ids,
      questions: s.questions,
      minutes: s.minutes,
      marks: s.questions,
      topics: s.kind === 'academic' ? [...new Set(data.academic.filter((a) => a.group === s.key).map((a) => a.subtopicHint))].slice(0, 6) : [],
      questionTypes: [s.kind === 'about' ? 'Survey' : 'Multiple choice'],
      tier: 'free' as const,
      formId: file.form.formId,
      section: s.key,
    };
  });
}

export interface SubjectTests {
  subjectId: string;
  subjectName: string;
  /** Chapters in order, with what can be taken for each. */
  chapters: { chapterId: string; order: number; name: string; current: boolean; check?: AssessmentDef; practice: AssessmentDef[]; lastAttempt?: Attempt }[];
  mocks: AssessmentDef[];
}

/** Chapter checks, practice tests and mocks per subject the student takes. */
export async function subjectTests(student: Student): Promise<SubjectTests[]> {
  const attempts = getAttempts(student.id);
  const out: SubjectTests[] = [];
  for (const { subjectId } of student.subjects) {
    const sub = getSubject(subjectId);
    if (!sub) continue;
    const current = new Set(student.currentChapterIds ?? []);
    const chapters = [];
    for (const ch of sub.chapters) {
      const check = await getAssessment(`chk.${ch.id}`, student.id);
      const practice = (await Promise.all([getAssessment(`pfa.${ch.id}`, student.id), getAssessment(`pfb.${ch.id}`, student.id)])).filter((x): x is AssessmentDef => !!x);
      chapters.push({ chapterId: ch.id, order: ch.order, name: ch.name, current: current.has(ch.id), check, practice, lastAttempt: attempts.find((a) => a.chapterId === ch.id) });
    }
    const mockNums = [...new Set(getQuestions({ subjectId, set: 'mock' }).map((q) => q.id.match(/-mock(\d+)-/)?.[1]).filter(Boolean))] as string[];
    const mocks = (await Promise.all(mockNums.map((n) => getAssessment(`mock.${subjectId}.${n}`, student.id)))).filter((x): x is AssessmentDef => !!x);
    out.push({ subjectId, subjectName: sub.subject.name, chapters, mocks });
  }
  return out;
}

export const testHref = (testId: string) => `/student/assessments/${encodeURIComponent(testId)}`;
export const resultHref = (attemptId: string) => `/student/assessments/results/${encodeURIComponent(attemptId)}`;
