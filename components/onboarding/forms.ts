import 'server-only';
import path from 'node:path';
import type { Board, Grade, Stream } from '@/lib/types';
import { readDataText } from '@/lib/data/source';
import type { OnboardingFormFile } from '@/lib/types/onboarding';
import indexFile from '@/data/questions/onboarding/index.json';

interface FormIndexRow {
  formId: string;
  board: Board;
  grade: Grade;
  stream: Stream;
  title: string;
  path: string;
}

const FORMS = (indexFile as { items: FormIndexRow[] }).items;

/**
 * The onboarding form for a student. Exact board/grade/stream first; while the question-bank thread is
 * still generating forms, falls back to the same board's nearest grade (then any board) so the demo runs.
 */
export function pickOnboardingForm(board: Board, grade: Grade, stream: Stream = 'none'): { row: FormIndexRow; exact: boolean } | null {
  const s: Stream = grade >= 11 ? stream : 'none';
  const exact = FORMS.find((f) => f.board === board && f.grade === grade && f.stream === s);
  if (exact) return { row: exact, exact: true };
  const ranked = [...FORMS].sort(
    (a, b) => Number(b.board === board) - Number(a.board === board) || Math.abs(a.grade - grade) - Math.abs(b.grade - grade),
  );
  return ranked[0] ? { row: ranked[0], exact: false } : null;
}

const cache = new Map<string, OnboardingFormFile>();

export async function loadOnboardingForm(formId: string): Promise<OnboardingFormFile | null> {
  if (cache.has(formId)) return cache.get(formId)!;
  const row = FORMS.find((f) => f.formId === formId);
  if (!row) return null;
  const text = readDataText(path.join(process.cwd(), row.path));
  if (text === undefined) return null;
  const file = JSON.parse(text) as OnboardingFormFile;
  cache.set(formId, file);
  return file;
}
