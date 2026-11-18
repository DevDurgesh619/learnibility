import 'server-only';
import { getChapter, getGaps, getQuestion, getStudent, getSubject, getSubtopic, type Attempt, type GapRecord } from '@/lib/data';
import { GAP_TAXONOMY, diagnoseGaps, type Diagnosis } from '@/lib/engines';
import { bandFor } from '@/lib/onboarding/score';
import type { Band, GapCode, Question } from '@/lib/types';

/** PDF 8f-8h view model for one submitted attempt. */
export type Strength = 'Strong' | 'Medium' | 'Weak';

export interface ItemReview {
  n: number;
  question: Question;
  answer?: string;
  correct: boolean;
  blank: boolean;
  secondsTaken: number;
  confidence?: number;
  /** "Why you chose this": one plain sentence from timing, confidence and the item's likely gap. */
  why: string;
  likelyGap?: GapCode;
}

export interface TopicRow {
  /** subtopicId (chapter tests) or chapterId (mocks and onboarding). */
  id: string;
  name: string;
  questions: number;
  correct: number;
  incorrect: number;
  blank: number;
  percent: number;
  strength: Strength;
  diagnosis?: Diagnosis;
  gap?: GapRecord;
}

export interface AttemptReport {
  attempt: Attempt;
  title: string;
  subjectName: string;
  score: number;
  maxScore: number;
  percent: number;
  correct: number;
  total: number;
  band: Band;
  strength: Strength;
  minutesUsed: number;
  topics: TopicRow[];
  focus?: TopicRow;
  strongest?: TopicRow;
  items: ItemReview[];
}

export const STRENGTH_CLASS: Record<Strength, string> = { Strong: 'text-success-700', Medium: 'text-warning-700', Weak: 'text-danger-700' };

/** Engine cause text cites 430-file parameter numbers ("#279, #20"); students see the words only. */
export function plainCause(s: string | null | undefined): string | null {
  if (!s) return null;
  return s.replace(/\s*\((?:#\d+[,\s]*)+\)/g, '').replace(/:\s*(?:#\d+[,\s]*)+$/g, '').replace(/\s*#\d+(?:,\s*#\d+)*/g, '').trim() || null;
}

export const strengthOf = (percent: number): Strength => (percent >= 75 ? 'Strong' : percent >= 50 ? 'Medium' : 'Weak');

function why(q: Question, r: { correct: boolean; secondsTaken: number; confidence?: number; blank: boolean }): string {
  if (r.correct) {
    if (r.confidence !== undefined && r.confidence <= 2) return 'Right, but you were unsure. Trust this method next time.';
    return r.secondsTaken > q.minutes * 60 * 1.5 ? `Right, but slow: ${r.secondsTaken} s against about ${Math.round(q.minutes * 60)} s suggested.` : 'Right.';
  }
  if (r.blank) return 'Left blank. Blanks on several questions point to running out of time or avoiding the topic.';
  if (r.secondsTaken > 0 && r.secondsTaken < 6) return `Answered in ${r.secondsTaken} s, which looks like a guess.`;
  if ((r.confidence ?? 0) >= 4) return `You were sure (${r.confidence}/5) but it was wrong. Over-confidence on this kind of question is worth watching.`;
  if (r.secondsTaken > q.minutes * 60 * 1.2) return `Took ${r.secondsTaken} s against about ${Math.round(q.minutes * 60)} s suggested: time pressure may have played a part.`;
  const g = q.likelyGapOnWrong;
  return g ? `Most students who miss this have a ${GAP_TAXONOMY[g].name.toLowerCase()}: ${GAP_TAXONOMY[g].causes.toLowerCase()}.` : 'Check the worked answer below.';
}

/** Topic name for an id: subtopic, else chapter, else the id. */
function topicName(id: string, fallback?: string): string {
  return getSubtopic(id)?.name ?? getChapter(id)?.chapter.name ?? fallback ?? id;
}

export function buildReport(attempt: Attempt): AttemptReport {
  const student = getStudent(attempt.learnerId);
  const questions = attempt.questionIds.map((id) => getQuestion(id)).filter((q): q is Question => !!q);
  const respById = new Map(attempt.responses.map((r) => [r.questionId, r]));

  const items: ItemReview[] = questions.map((q, i) => {
    const r = respById.get(q.id);
    const blank = !r || ((r.answer ?? '').trim() === '' && !r.correct);
    const correct = !!r?.correct;
    return {
      n: i + 1,
      question: q,
      answer: r?.answer,
      correct,
      blank,
      secondsTaken: r?.secondsTaken ?? 0,
      confidence: r?.confidence,
      why: why(q, { correct, secondsTaken: r?.secondsTaken ?? 0, confidence: r?.confidence, blank }),
      likelyGap: correct ? undefined : q.likelyGapOnWrong,
    };
  });

  // Group by subtopic for single-chapter tests, by chapter otherwise.
  const chapters = new Set(questions.map((q) => q.chapterId));
  const bySubtopic = chapters.size === 1 || attempt.kind === 'onboarding';
  const keyOf = (q: Question) => (bySubtopic ? q.subtopicId : q.chapterId);

  // Engine diagnosis per subtopic (insufficient evidence on short tests is fine; we only show what it found).
  let diagnoses: Diagnosis[] = [];
  if (student && attempt.kind !== 'onboarding') {
    const subs: Record<string, NonNullable<ReturnType<typeof getSubtopic>>> = {};
    for (const q of questions) {
      const s = getSubtopic(q.subtopicId);
      if (s) subs[s.id] = s;
    }
    try {
      diagnoses = diagnoseGaps(attempt.responses, questions.filter((q) => subs[q.subtopicId]), { learnerId: student.id, band: student.band, subtopics: subs });
    } catch {
      diagnoses = [];
    }
  }
  const gaps = getGaps(attempt.learnerId);
  const gapFor = (id: string) => gaps.find((g) => (g.attemptId === attempt.id || attempt.kind === 'onboarding') && (g.subtopicId === id || g.chapterId === id) && g.status !== 'closed')
    ?? gaps.find((g) => g.subtopicId === id && g.status !== 'closed');

  const groups = new Map<string, ItemReview[]>();
  for (const it of items) groups.set(keyOf(it.question), [...(groups.get(keyOf(it.question)) ?? []), it]);
  const topics: TopicRow[] = [...groups.entries()].map(([id, list]) => {
    const marks = list.reduce((s, x) => s + x.question.marks, 0);
    const got = list.reduce((s, x) => s + (x.correct ? x.question.marks : 0), 0);
    const percent = marks ? Math.round((100 * got) / marks) : 0;
    return {
      id,
      name: topicName(id, (list[0].question as Question & { subtopicHint?: string }).subtopicHint),
      questions: list.length,
      correct: list.filter((x) => x.correct).length,
      incorrect: list.filter((x) => !x.correct && !x.blank).length,
      blank: list.filter((x) => x.blank).length,
      percent,
      strength: strengthOf(percent),
      diagnosis: diagnoses.find((d) => d.subtopicId === id),
      gap: gapFor(id),
    };
  });

  const percent = attempt.maxScore ? Math.round((100 * attempt.score) / attempt.maxScore) : 0;
  const weak = [...topics].sort((a, b) => a.percent - b.percent || b.questions - a.questions);
  const firstSeen = attempt.responses.length ? attempt.responses.reduce((s, r) => s + r.secondsTaken, 0) : 0;
  const subjectName = getChapter(attempt.chapterId ?? '')?.subject.name ?? getSubject(attempt.subjectId)?.subject.name ?? attempt.title.split(' · ')[0];

  return {
    attempt,
    title: attempt.title,
    subjectName,
    score: attempt.score,
    maxScore: attempt.maxScore,
    percent,
    correct: items.filter((i) => i.correct).length,
    total: items.length,
    band: bandFor(percent),
    strength: strengthOf(percent),
    minutesUsed: Math.max(1, Math.round((Date.parse(attempt.submittedUtc) - Date.parse(attempt.startedUtc)) / 60000) || Math.round(firstSeen / 60)),
    topics,
    focus: weak[0] && weak[0].percent < 75 ? weak[0] : undefined,
    strongest: [...topics].sort((a, b) => b.percent - a.percent)[0],
    items,
  };
}

/** Subject id behind a question's subtopic, used for the tutor link. */
export function subjectSlugOf(q: Question): string {
  return q.subjectId.replace(/^(cbse|cambridge|ib)-g\d+-/, '');
}

export type { Diagnosis };
