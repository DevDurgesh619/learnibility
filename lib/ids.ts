/**
 * ID builders and parsers for the Learnibility shared contract (docs/contracts.md).
 * IDs are lowercase, kebab-case, stable and never reused.
 *
 *   Subject     {board}-g{grade}-{subjectSlug}          cbse-g8-maths
 *   Chapter     {subjectId}-ch{NN}                       cbse-g8-maths-ch01
 *   Subtopic    {chapterId}-st{N}                        cbse-g8-maths-ch01-st2
 *   Question    {subtopicId}-q{NN}                       cbse-g8-maths-ch01-st2-q03
 *   Practice    {chapterId}-pf{A|B}-q{NN}                cbse-g8-maths-ch01-pfa-q01
 *   Mock        {subjectId}-mock{N}-q{NN}                cbse-g10-science-mock1-q12
 *   Onboarding  onb-{board}-g{grade}-{stream}-q{NN}      onb-cbse-g8-none-q01
 *   People      lrn_ par_ tch_ csl_ tut_ mnt_ + {first}_{last}
 *   Catalogue   career-, skill-, uni-{country}-, course-, res- + {slug}
 *   Parameter   p{ID}                                    p279
 *
 * Note on practice forms: IDs are lowercase, so form A is written "pfa" and form B "pfb".
 */
import { BOARDS, GRADES, STREAMS, type Board, type Grade, type Stream } from './types/enums';

// ---------- helpers ----------

const pad = (n: number, width: number) => String(n).padStart(width, '0');

function assertPositiveInt(n: number, what: string): void {
  if (!Number.isInteger(n) || n < 1) throw new Error(`${what} must be a positive integer, got ${n}`);
}

/** Lowercase kebab slug: "Computer Science" -> "computer-science". */
export function slugify(text: string): string {
  return text
    .normalize('NFKD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/&/g, ' and ')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

const SLUG = '[a-z0-9]+(?:-[a-z0-9]+)*';
const SLUG_RE = new RegExp(`^${SLUG}$`);

export function isSlug(s: string): boolean {
  return SLUG_RE.test(s);
}

function assertSlug(s: string, what: string): void {
  if (!isSlug(s)) throw new Error(`${what} must be a lowercase kebab slug, got "${s}"`);
}

const isBoard = (s: string): s is Board => (BOARDS as readonly string[]).includes(s);
const isGrade = (n: number): n is Grade => (GRADES as readonly number[]).includes(n);
const isStream = (s: string): s is Stream => (STREAMS as readonly string[]).includes(s);

// ---------- curriculum ----------

export interface SubjectIdParts { board: Board; grade: Grade; slug: string }
export interface ChapterIdParts extends SubjectIdParts { subjectId: string; chapter: number }
export interface SubtopicIdParts extends ChapterIdParts { chapterId: string; subtopic: number }

export function subjectId(board: Board, grade: Grade, slug: string): string {
  if (!isBoard(board)) throw new Error(`Unknown board "${board}"`);
  if (!isGrade(grade)) throw new Error(`Unknown grade ${grade}`);
  assertSlug(slug, 'Subject slug');
  return `${board}-g${grade}-${slug}`;
}

export function chapterId(subject: string, chapter: number): string {
  parseSubjectIdOrThrow(subject);
  assertPositiveInt(chapter, 'Chapter number');
  return `${subject}-ch${pad(chapter, 2)}`;
}

export function subtopicId(chapter: string, subtopic: number): string {
  parseChapterIdOrThrow(chapter);
  assertPositiveInt(subtopic, 'Subtopic number');
  return `${chapter}-st${subtopic}`;
}

const SUBJECT_RE = new RegExp(`^(cbse|cambridge|ib)-g(8|9|10|11|12)-(${SLUG})$`);
const CHAPTER_RE = new RegExp(`^(.+)-ch(\\d{2,})$`);
const SUBTOPIC_RE = new RegExp(`^(.+)-st(\\d+)$`);

export function parseSubjectId(id: string): SubjectIdParts | null {
  const m = SUBJECT_RE.exec(id);
  if (!m) return null;
  const slug = m[3];
  // A subject slug never ends in a chapter/subtopic/question suffix.
  if (/(^|-)(ch\d+|st\d+|q\d+|pf[ab]|mock\d+)(-|$)/.test(slug)) return null;
  return { board: m[1] as Board, grade: Number(m[2]) as Grade, slug };
}

export function parseChapterId(id: string): ChapterIdParts | null {
  const m = CHAPTER_RE.exec(id);
  if (!m) return null;
  const subject = parseSubjectId(m[1]);
  const n = Number(m[2]);
  if (!subject || n < 1 || chapterSegment(n) !== `ch${m[2]}`) return null;
  return { ...subject, subjectId: m[1], chapter: n };
}

export function parseSubtopicId(id: string): SubtopicIdParts | null {
  const m = SUBTOPIC_RE.exec(id);
  if (!m) return null;
  const chapter = parseChapterId(m[1]);
  const n = Number(m[2]);
  if (!chapter || n < 1 || String(n) !== m[2]) return null;
  return { ...chapter, chapterId: m[1], subtopic: n };
}

const chapterSegment = (n: number) => `ch${pad(n, 2)}`;
const qSegment = (n: number) => `q${pad(n, 2)}`;

function parseSubjectIdOrThrow(id: string) {
  const p = parseSubjectId(id);
  if (!p) throw new Error(`Not a subject ID: "${id}"`);
  return p;
}
function parseChapterIdOrThrow(id: string) {
  const p = parseChapterId(id);
  if (!p) throw new Error(`Not a chapter ID: "${id}"`);
  return p;
}
function parseSubtopicIdOrThrow(id: string) {
  const p = parseSubtopicId(id);
  if (!p) throw new Error(`Not a subtopic ID: "${id}"`);
  return p;
}

// ---------- questions ----------

export type PracticeForm = 'A' | 'B';

export function questionId(subtopic: string, n: number): string {
  parseSubtopicIdOrThrow(subtopic);
  assertPositiveInt(n, 'Question number');
  return `${subtopic}-${qSegment(n)}`;
}

export function practiceQuestionId(chapter: string, form: PracticeForm, n: number): string {
  parseChapterIdOrThrow(chapter);
  if (form !== 'A' && form !== 'B') throw new Error(`Practice form must be A or B, got "${form}"`);
  assertPositiveInt(n, 'Question number');
  return `${chapter}-pf${form.toLowerCase()}-${qSegment(n)}`;
}

export function mockQuestionId(subject: string, mock: number, n: number): string {
  parseSubjectIdOrThrow(subject);
  assertPositiveInt(mock, 'Mock number');
  assertPositiveInt(n, 'Question number');
  return `${subject}-mock${mock}-${qSegment(n)}`;
}

export function onboardingQuestionId(board: Board, grade: Grade, stream: Stream, n: number): string {
  if (!isBoard(board)) throw new Error(`Unknown board "${board}"`);
  if (!isGrade(grade)) throw new Error(`Unknown grade ${grade}`);
  if (!isStream(stream)) throw new Error(`Unknown stream "${stream}"`);
  if ((grade <= 10) !== (stream === 'none')) {
    throw new Error(`Grades 8-10 use stream "none"; grades 11-12 need a stream (got g${grade} ${stream})`);
  }
  assertPositiveInt(n, 'Question number');
  return `onb-${board}-g${grade}-${stream}-${qSegment(n)}`;
}

export type QuestionIdParts =
  | ({ kind: 'bank'; subtopicId: string; number: number } & SubtopicIdParts)
  | ({ kind: 'practice'; chapterId: string; form: PracticeForm; number: number } & ChapterIdParts)
  | ({ kind: 'mock'; subjectId: string; mock: number; number: number } & SubjectIdParts)
  | { kind: 'onboarding'; board: Board; grade: Grade; stream: Stream; number: number };

const Q_SUFFIX_RE = /^(.+)-q(\d{2,})$/;
const ONB_RE = /^onb-(cbse|cambridge|ib)-g(8|9|10|11|12)-(none|science|commerce|humanities)$/;

export function parseQuestionId(id: string): QuestionIdParts | null {
  const m = Q_SUFFIX_RE.exec(id);
  if (!m) return null;
  const [, head, num] = m;
  const number = Number(num);
  if (number < 1 || qSegment(number) !== `q${num}`) return null;

  const onb = ONB_RE.exec(head);
  if (onb) {
    const grade = Number(onb[2]) as Grade;
    const stream = onb[3] as Stream;
    if ((grade <= 10) !== (stream === 'none')) return null;
    return { kind: 'onboarding', board: onb[1] as Board, grade, stream, number };
  }

  const pf = /^(.+)-pf([ab])$/.exec(head);
  if (pf) {
    const ch = parseChapterId(pf[1]);
    return ch ? { kind: 'practice', ...ch, chapterId: pf[1], form: pf[2].toUpperCase() as PracticeForm, number } : null;
  }

  const mock = /^(.+)-mock(\d+)$/.exec(head);
  if (mock) {
    const subj = parseSubjectId(mock[1]);
    const mockN = Number(mock[2]);
    if (!subj || mockN < 1 || String(mockN) !== mock[2]) return null;
    return { kind: 'mock', ...subj, subjectId: mock[1], mock: mockN, number };
  }

  const st = parseSubtopicId(head);
  return st ? { kind: 'bank', ...st, subtopicId: head, number } : null;
}

// ---------- people ----------

export const PERSON_PREFIXES = {
  learner: 'lrn',
  parent: 'par',
  teacher: 'tch',
  counsellor: 'csl',
  tutor: 'tut',
  mentor: 'mnt',
} as const;
export type PersonKind = keyof typeof PERSON_PREFIXES;

const nameSlug = (s: string) => slugify(s).replace(/-/g, '');

/** personId('tutor', 'Rahul', 'Verma') -> "tut_rahul_verma". */
export function personId(kind: PersonKind, firstName: string, lastName: string): string {
  const prefix = PERSON_PREFIXES[kind];
  if (!prefix) throw new Error(`Unknown person kind "${kind}"`);
  const first = nameSlug(firstName);
  const last = nameSlug(lastName);
  if (!first || !last) throw new Error(`Person needs a first and last name, got "${firstName}" "${lastName}"`);
  return `${prefix}_${first}_${last}`;
}

export const learnerId = (firstName: string, lastName: string) => personId('learner', firstName, lastName);

const PERSON_RE = /^(lrn|par|tch|csl|tut|mnt)_([a-z0-9]+)_([a-z0-9]+)$/;

export function parsePersonId(id: string): { kind: PersonKind; first: string; last: string } | null {
  const m = PERSON_RE.exec(id);
  if (!m) return null;
  const kind = (Object.keys(PERSON_PREFIXES) as PersonKind[]).find((k) => PERSON_PREFIXES[k] === m[1])!;
  return { kind, first: m[2], last: m[3] };
}

// ---------- catalogue ----------

export type CatalogueKind = 'career' | 'skill' | 'uni' | 'course' | 'res';

export function catalogueId(kind: Exclude<CatalogueKind, 'uni'>, slug: string): string {
  if (!['career', 'skill', 'course', 'res'].includes(kind)) throw new Error(`Unknown catalogue kind "${kind}"`);
  assertSlug(slug, 'Catalogue slug');
  return `${kind}-${slug}`;
}

/** country is a two-letter lowercase code: in, us, uk, ca, au ... */
export function universityId(country: string, slug: string): string {
  if (!/^[a-z]{2}$/.test(country)) throw new Error(`Country must be a two-letter lowercase code, got "${country}"`);
  assertSlug(slug, 'University slug');
  return `uni-${country}-${slug}`;
}

export type CatalogueIdParts =
  | { kind: Exclude<CatalogueKind, 'uni'>; slug: string }
  | { kind: 'uni'; country: string; slug: string };

export function parseCatalogueId(id: string): CatalogueIdParts | null {
  const uni = new RegExp(`^uni-([a-z]{2})-(${SLUG})$`).exec(id);
  if (uni) return { kind: 'uni', country: uni[1], slug: uni[2] };
  const m = new RegExp(`^(career|skill|course|res)-(${SLUG})$`).exec(id);
  return m ? { kind: m[1] as Exclude<CatalogueKind, 'uni'>, slug: m[2] } : null;
}

// ---------- profile parameters ----------

export function paramId(n: number): string {
  if (!Number.isInteger(n) || n < 1 || n > 430) throw new Error(`Profile parameter must be 1..430, got ${n}`);
  return `p${n}`;
}

export function parseParamId(id: string): number | null {
  const m = /^p([1-9]\d{0,2})$/.exec(id);
  if (!m) return null;
  const n = Number(m[1]);
  return n <= 430 ? n : null;
}

// ---------- generic ----------

export type IdKind = 'subject' | 'chapter' | 'subtopic' | 'question' | 'person' | 'catalogue' | 'param';

/** Classify any contract ID; null when it matches no pattern. */
export function idKind(id: string): IdKind | null {
  if (parseParamId(id) !== null) return 'param';
  if (parsePersonId(id)) return 'person';
  if (parseCatalogueId(id)) return 'catalogue';
  if (parseQuestionId(id)) return 'question';
  if (parseSubtopicId(id)) return 'subtopic';
  if (parseChapterId(id)) return 'chapter';
  if (parseSubjectId(id)) return 'subject';
  return null;
}
