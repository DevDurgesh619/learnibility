/**
 * Curriculum, question and catalogue readers (server only).
 * Curriculum hours: when a subtopic's learnHours/masterHours are empty, they are filled with the
 * mastery-time engine on read, so every screen shows the same hours.
 */
import path from 'node:path';
import { withMasteryHours } from '@/lib/engines';
import type {
  Career,
  Chapter,
  EntranceExam,
  Question,
  QuestionSet,
  Resource,
  Skill,
  Subject,
  Subtopic,
  Tutor,
  University,
} from '@/lib/types';
import { dataRoot, itemsOf, jsonFilesIn, readJson } from './source';

interface SubjectFile {
  subject: Subject;
  items: Chapter[];
  subtopics: Subtopic[];
}

export interface SubjectBundle {
  subject: Subject;
  chapters: Chapter[];
  subtopics: Subtopic[];
}

export interface ChapterBundle {
  subject: Subject;
  chapter: Chapter;
  subtopics: Subtopic[];
}

const hoursEmpty = (h: Record<string, number> | undefined) => !h || Object.keys(h).length === 0;

function fillHours(s: Subtopic): Subtopic {
  return hoursEmpty(s.learnHours) || hoursEmpty(s.masterHours) ? withMasteryHours(s) : s;
}

const subjectCache = new Map<string, SubjectBundle | null>();

export function listSubjects(filter: { board?: string; grade?: number; stream?: string } = {}): Subject[] {
  return itemsOf<Subject>(path.join(dataRoot(), 'curriculum', 'subjects.json')).filter(
    (s) => (!filter.board || s.board === filter.board) && (!filter.grade || s.grade === filter.grade) && (!filter.stream || s.stream === filter.stream || s.stream === 'none'),
  );
}

/** One subject with its chapters and subtopics (hours filled). Undefined when the file is not built. */
export function getSubject(subjectId: string): SubjectBundle | undefined {
  const file = readJson<SubjectFile>(path.join(dataRoot(), 'curriculum', `${subjectId}.json`));
  if (!file) return listSubjects().find((s) => s.id === subjectId) ? { subject: listSubjects().find((s) => s.id === subjectId)!, chapters: [], subtopics: [] } : undefined;
  const cached = subjectCache.get(subjectId);
  if (cached && cached.subject === file.subject) return cached;
  const bundle: SubjectBundle = {
    subject: file.subject,
    chapters: [...file.items].sort((a, b) => a.order - b.order),
    subtopics: file.subtopics.map(fillHours),
  };
  subjectCache.set(subjectId, bundle);
  return bundle;
}

/** subjectId from any chapter / subtopic / question id. */
export function subjectIdOf(id: string): string {
  return id.replace(/-ch\d+.*$/, '').replace(/-mock\d+.*$/, '');
}

export function getChapter(chapterId: string): ChapterBundle | undefined {
  const b = getSubject(subjectIdOf(chapterId));
  const chapter = b?.chapters.find((c) => c.id === chapterId);
  if (!b || !chapter) return undefined;
  const ids = new Set(chapter.subtopicIds);
  return { subject: b.subject, chapter, subtopics: b.subtopics.filter((s) => ids.has(s.id)).sort((a, b2) => a.order - b2.order) };
}

export function getSubtopic(subtopicId: string): (Subtopic & { chapterName: string; subjectId: string }) | undefined {
  const b = getSubject(subjectIdOf(subtopicId));
  const s = b?.subtopics.find((x) => x.id === subtopicId);
  if (!b || !s) return undefined;
  return { ...s, chapterName: b.chapters.find((c) => c.id === s.chapterId)?.name ?? '', subjectId: b.subject.id };
}

/** Display names for subtopics and chapters, keyed by id (engines take this as `names`). */
export function namesFor(subjectIds: string[]): Record<string, string> {
  const out: Record<string, string> = {};
  for (const id of subjectIds) {
    const b = getSubject(id);
    if (!b) continue;
    out[id] = b.subject.name;
    for (const c of b.chapters) out[c.id] = c.name;
    for (const s of b.subtopics) out[s.id] = s.name;
  }
  return out;
}

// ------------------------------------------------------------------ questions

export interface QuestionFilter {
  subjectId?: string;
  chapterId?: string;
  subtopicIds?: string[];
  set?: QuestionSet | QuestionSet[];
  ids?: string[];
  /** Include fixture questions even when the real bank exists (history review). Default false. */
  includeFixtures?: boolean;
  limit?: number;
}

function bankQuestions(subjectId: string): Question[] {
  const dir = path.join(dataRoot(), 'questions', subjectId);
  return jsonFilesIn(dir).flatMap((f) => itemsOf<Question>(f));
}

function fixtureQuestions(subjectId: string): Question[] {
  return itemsOf<Question>(path.join(dataRoot(), 'fixtures', 'questions', `${subjectId}.json`));
}

function onboardingQuestions(): Question[] {
  return jsonFilesIn(path.join(dataRoot(), 'questions', 'onboarding'))
    .filter((f) => path.basename(f).startsWith('onb-'))
    .flatMap((f) => itemsOf<Question>(f));
}

/** Questions for a subject: the real bank when it exists, else the fixture set. */
export function getQuestions(filter: QuestionFilter): Question[] {
  let qs: Question[];
  if (filter.ids) {
    qs = filter.ids.map(getQuestion).filter((q): q is Question => !!q);
  } else {
    const subjectId = filter.subjectId ?? (filter.chapterId ? subjectIdOf(filter.chapterId) : filter.subtopicIds?.[0] ? subjectIdOf(filter.subtopicIds[0]) : undefined);
    const sets = filter.set ? (Array.isArray(filter.set) ? filter.set : [filter.set]) : undefined;
    if (sets?.length === 1 && sets[0] === 'onboarding') qs = onboardingQuestions();
    else if (!subjectId) return [];
    else {
      const bank = bankQuestions(subjectId);
      qs = bank.length && !filter.includeFixtures ? bank : [...bank, ...fixtureQuestions(subjectId)];
    }
    if (filter.chapterId) qs = qs.filter((q) => q.chapterId === filter.chapterId);
    if (filter.subtopicIds) {
      const s = new Set(filter.subtopicIds);
      qs = qs.filter((q) => s.has(q.subtopicId));
    }
    if (sets) qs = qs.filter((q) => sets.includes(q.set));
  }
  return filter.limit ? qs.slice(0, filter.limit) : qs;
}

const qIndex = new Map<string, Map<string, Question>>();

/** Any question by id: bank, fixture or onboarding. */
export function getQuestion(id: string): Question | undefined {
  if (id.startsWith('onb-')) return onboardingQuestions().find((q) => q.id === id);
  const sid = subjectIdOf(id);
  let m = qIndex.get(sid);
  if (!m || process.env.NODE_ENV !== 'production') {
    m = new Map([...fixtureQuestions(sid), ...bankQuestions(sid)].map((q) => [q.id, q]));
    qIndex.set(sid, m);
  }
  return m.get(id);
}

// ------------------------------------------------------------------ catalogues

function catalogue<T>(name: string): T[] {
  return itemsOf<T>(path.join(dataRoot(), 'catalogues', `${name}.json`));
}

export interface TutorFilter {
  subjectSlug?: string;
  board?: string;
  grade?: number;
  maxPriceInr?: number;
  minRating?: number;
  mode?: 'online' | 'offline';
  format?: 'one_to_one' | 'group';
  q?: string;
}

export function listTutors(f: TutorFilter = {}): Tutor[] {
  const q = f.q?.toLowerCase();
  return catalogue<Tutor>('tutors').filter((t) => {
    if (f.subjectSlug || f.board || f.grade) {
      const ok = t.subjects.some(
        (s) => (!f.subjectSlug || s.subjectSlug === f.subjectSlug) && (!f.board || s.boards.includes(f.board as never)) && (!f.grade || s.grades.includes(f.grade as never)),
      );
      if (!ok) return false;
    }
    if (f.maxPriceInr !== undefined && t.pricing.oneToOnePerHourInr > f.maxPriceInr) return false;
    if (f.minRating !== undefined && t.rating < f.minRating) return false;
    if (f.mode && !t.modes.includes(f.mode)) return false;
    if (f.format && !t.formats.includes(f.format)) return false;
    if (q && !`${t.displayName} ${t.headline} ${t.city}`.toLowerCase().includes(q)) return false;
    return true;
  });
}

export const getTutor = (id: string) => catalogue<Tutor>('tutors').find((t) => t.id === id);
export const listCareers = (f: { q?: string } = {}) =>
  catalogue<Career>('careers').filter((c) => !f.q || c.title.toLowerCase().includes(f.q.toLowerCase()));
export const getCareer = (id: string) => catalogue<Career>('careers').find((c) => c.id === id);
export const listSkills = () => catalogue<Skill>('skills');
export const listExams = () => catalogue<EntranceExam>('exams');
export const listResources = (f: { skillId?: string; free?: boolean } = {}) =>
  catalogue<Resource>('resources').filter((r) => {
    const rr = r as unknown as { skillIds?: string[]; priceInr?: number };
    if (f.skillId && !(rr.skillIds ?? []).includes(f.skillId)) return false;
    if (f.free !== undefined && (rr.priceInr ?? 0) === 0) return f.free;
    if (f.free !== undefined) return !f.free;
    return true;
  });

export interface UniversityFilter {
  country?: string | string[];
  field?: string;
  q?: string;
  selectivity?: University['selectivity'][];
  maxTotalCostInr?: number;
}

export function listUniversities(f: UniversityFilter = {}): University[] {
  const countries = f.country ? (Array.isArray(f.country) ? f.country : [f.country]) : undefined;
  const q = f.q?.toLowerCase();
  return catalogue<University>('universities').filter(
    (u) =>
      (!countries || countries.includes(u.country)) &&
      (!f.field || u.programmes.some((p) => p.field === f.field)) &&
      (!q || `${u.name} ${u.shortName} ${u.city}`.toLowerCase().includes(q)) &&
      (!f.selectivity || f.selectivity.includes(u.selectivity)) &&
      (f.maxTotalCostInr === undefined || u.totalCostInr <= f.maxTotalCostInr),
  );
}

export const getUniversity = (id: string) => catalogue<University>('universities').find((u) => u.id === id);
