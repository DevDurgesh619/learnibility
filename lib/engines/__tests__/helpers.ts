import fx from '../__fixtures__/maths8.json';
import type { ItemResponse, Question, Weight } from '../../types';
import type { SubtopicLike } from '../diagnoseGaps';

export const questions = fx.questions as unknown as Question[];
export const subtopics: SubtopicLike[] = fx.subtopics.map((s) => ({ id: s.id, chapterId: s.chapterId, weight: s.weight as Weight, teachingPeriods: s.teachingPeriods, name: s.name }));
export const pathFor = (subtopicId: string) => questions.filter((q) => q.subtopicId === subtopicId).sort((a, b) => a.id.localeCompare(b.id));

/** Turn the workbook's 1 / 0 / blank list into ItemResponses on the subtopic's path. */
export function responsesFrom(subtopicId: string, results: (number | null)[], opts: { confidenceWrong?: 1 | 2 | 3 | 4 | 5; seconds?: number[] } = {}): ItemResponse[] {
  const path = pathFor(subtopicId);
  const out: ItemResponse[] = [];
  results.forEach((r, i) => {
    if (r === null || r === undefined) return;
    out.push({ questionId: path[i].id, correct: r === 1, secondsTaken: opts.seconds?.[i] ?? path[i].minutes * 60, ...(r === 0 && opts.confidenceWrong ? { confidence: opts.confidenceWrong } : {}) });
  });
  return out;
}
