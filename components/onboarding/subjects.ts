import subjectsFile from '@/data/curriculum/subjects.json';
import type { Board, Grade, Stream, Subject } from '@/lib/types';

const SUBJECTS = (subjectsFile as { items: Subject[] }).items;

/** Subjects a student of this board, grade and stream takes (curriculum map, subjects.json). */
export function subjectsForStudent(board: Board, grade: Grade, stream: Stream): Subject[] {
  return SUBJECTS.filter((s) => s.board === board && s.grade === grade && (grade < 11 || s.stream === stream || s.stream === 'none'));
}

export function subjectName(id: string): string {
  return SUBJECTS.find((s) => s.id === id)?.name ?? id;
}
