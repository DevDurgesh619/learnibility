/**
 * Demo marker (W2-S1). MCQ is exact. Numerical and short answers compare the final number or the normalised text.
 * Explain, multi-step, case and long answers stand in for AI marking: right when the final number matches the
 * key's final number, or when at least half of the key's content words appear in the answer.
 * Pure; safe on server and client.
 */
import type { Question } from '@/lib/types';

const STOP = new Set(['the', 'and', 'that', 'this', 'with', 'from', 'then', 'there', 'their', 'which', 'when', 'what', 'have', 'into', 'your', 'they', 'will', 'each', 'than', 'only', 'also', 'here', 'because', 'same']);

export function normaliseText(s: string): string {
  return s.toLowerCase().replace(/[^\p{L}\p{N}.\-/ ]+/gu, ' ').replace(/\s+/g, ' ').trim();
}

export function numbersIn(s: string): number[] {
  const m = s.replace(/,(?=\d{3})/g, '').replace(/−/g, '-').match(/-?\d+(?:\.\d+)?(?:\/\d+)?/g) ?? [];
  return m.map((x) => {
    if (x.includes('/')) {
      const [a, b] = x.split('/').map(Number);
      return b ? a / b : NaN;
    }
    return Number(x);
  }).filter((n) => Number.isFinite(n));
}

const close = (a: number, b: number) => Math.abs(a - b) <= Math.max(1e-6, Math.abs(b) * 0.005);

function contentWords(s: string): string[] {
  return [...new Set(normaliseText(s).split(' ').filter((w) => w.length >= 4 && !STOP.has(w)))];
}

export function markAnswer(q: Pick<Question, 'type' | 'answer' | 'markingKey'>, raw: string | undefined): boolean {
  const answer = (raw ?? '').trim();
  if (!answer) return false;
  if (q.type === 'mcq') return answer === q.answer.trim();

  const keyNums = numbersIn(q.answer);
  const ansNums = numbersIn(answer);
  const finalKey = keyNums[keyNums.length - 1];

  if (q.type === 'numerical') {
    if (finalKey === undefined) return normaliseText(answer) === normaliseText(q.answer);
    return ansNums.length > 0 && close(ansNums[ansNums.length - 1], finalKey);
  }
  if (q.type === 'short') {
    const a = normaliseText(answer);
    const k = normaliseText(q.answer);
    if (a === k || (k.length <= 30 && a.includes(k))) return true;
    if (finalKey !== undefined && keyNums.length <= 2) return ansNums.some((n) => close(n, finalKey));
    return overlap(answer, q.answer) >= 0.6;
  }
  // explain, multi_step, case, long
  if (finalKey !== undefined && ansNums.some((n) => close(n, finalKey)) && overlap(answer, `${q.answer} ${q.markingKey}`) >= 0.15) return true;
  if (finalKey !== undefined && keyNums.length <= 3 && ansNums.length && close(ansNums[ansNums.length - 1], finalKey)) return true;
  return overlap(answer, q.answer) >= 0.5;
}

/** Share of the key's content words that appear in the answer. */
export function overlap(answer: string, key: string): number {
  const k = contentWords(key);
  if (!k.length) return 0;
  const a = new Set(contentWords(answer));
  return k.filter((w) => a.has(w)).length / k.length;
}
