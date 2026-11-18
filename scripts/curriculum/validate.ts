/**
 * Curriculum map validator (W2).
 *
 *   npx tsx scripts/curriculum/validate.ts            every subject must have its file
 *   npx tsx scripts/curriculum/validate.ts --partial  skip subjects whose file is not built yet
 *
 * Runs on Node 22+ (type stripping) or tsx. No dependencies. Exit code 1 on any error.
 * Checks:
 *  1. Envelope { schemaVersion: 1, generatedBy, items } on every file.
 *  2. subjects.json: 157 counted subjects, contract fields and enums, IDs {board}-g{grade}-{slug}.
 *  3. questionTarget per subject equals the cost sheet; board sums CBSE 63,582, Cambridge 62,540,
 *     IB 53,893, all 180,015 (data/curriculum/sheet-reference.json, built from the xlsx).
 *  4. Chapter count equals the sheet; where the sheet names chapters, each chapter maps 1:1 in order.
 *  5. Chapter and subtopic IDs, order, parent links, 3-5 subtopics, weights, periods (chapter = sum).
 *  6. Every prerequisite ID resolves, is the same board, not a later grade, earlier within the same
 *     subject, and the whole graph is acyclic; every subtopic has a prerequisiteNote.
 *  7. cbse-g8-maths reproduces the workbook: 14 chapters, 45 subtopics, 145 periods, same weights.
 *  9. Each chapter's student-check paths (L 5, S 6, H 8 bank items) fit the sheet's bank per chapter.
 *  8. streams.json offerings resolve to subjects; every subject is offered somewhere.
 */
import { readFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import type { Subject, Chapter, Subtopic } from '../../lib/types';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const DIR = join(ROOT, 'data', 'curriculum');
const partial = process.argv.includes('--partial');
const errors: string[] = [];
const err = (m: string) => errors.push(m);

const BOARDS = ['cbse', 'cambridge', 'ib'];
const GRADES = [8, 9, 10, 11, 12];
const STREAMS = ['none', 'science', 'commerce', 'humanities'];
const WEIGHTS = ['L', 'S', 'H'];
const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const ST_RE = /^(cbse|cambridge|ib)-g(8|9|10|11|12)-([a-z0-9-]+)-ch(\d{2})-st(\d)$/;
const G8_MATHS_WEIGHTS = 'SHSSHSSLHSSSHSSSSSSHSSHSSLSHSSHHLSLSSSHHHSSHH';

function load(name: string): any {
  const p = join(DIR, name);
  const j = JSON.parse(readFileSync(p, 'utf8'));
  if (j.schemaVersion !== 1 || typeof j.generatedBy !== 'string' || !Array.isArray(j.items))
    err(`${name}: missing { schemaVersion: 1, generatedBy, items } envelope`);
  return j;
}

const subjects: Subject[] = load('subjects.json').items;
const ref = load('sheet-reference.json');
const refById = new Map<string, any>(ref.items.map((r: any) => [r.subjectId, r]));

// 2-3 subjects and totals
if (subjects.length !== 157) err(`subjects.json has ${subjects.length} subjects, cost sheet counts 157`);
const seen = new Set<string>();
const boardSum: Record<string, number> = { cbse: 0, cambridge: 0, ib: 0 };
for (const s of subjects) {
  if (seen.has(s.id)) err(`${s.id}: duplicate subject`);
  seen.add(s.id);
  if (!BOARDS.includes(s.board) || !GRADES.includes(s.grade) || !STREAMS.includes(s.stream)) err(`${s.id}: bad enum`);
  if (!SLUG.test(s.slug) || s.id !== `${s.board}-g${s.grade}-${s.slug}`) err(`${s.id}: id does not match board/grade/slug`);
  if ((s.grade <= 10) !== (s.stream === 'none')) err(`${s.id}: stream must be 'none' exactly for grades 8-10`);
  if (!s.name || !s.programme) err(`${s.id}: name and programme required`);
  const r = refById.get(s.id);
  if (!r) { err(`${s.id}: not in sheet-reference`); continue; }
  if (s.questionTarget !== r.questionTarget) err(`${s.id}: questionTarget ${s.questionTarget} != sheet ${r.questionTarget}`);
  if (s.chapterCount !== r.chapterCount) err(`${s.id}: chapterCount ${s.chapterCount} != sheet ${r.chapterCount}`);
  boardSum[s.board] += s.questionTarget;
}
for (const b of BOARDS)
  if (boardSum[b] !== ref.boardTotals[b]) err(`${b}: question targets sum to ${boardSum[b]}, sheet says ${ref.boardTotals[b]}`);
const grand = Object.values(boardSum).reduce((a, b) => a + b, 0);
if (grand !== ref.grandTotal) err(`all boards: ${grand} questions, sheet says ${ref.grandTotal}`);

// 4-5 per-subject files
const allSt = new Map<string, Subtopic>();
const stSubject = new Map<string, Subject>();
let built = 0, nCh = 0;
for (const s of subjects) {
  const file = `${s.id}.json`;
  if (!existsSync(join(DIR, file))) { if (!partial) err(`${s.id}: ${file} missing`); continue; }
  built++;
  const j = load(file);
  const chapters: Chapter[] = j.items;
  const sts: Subtopic[] = j.subtopics ?? [];
  if (JSON.stringify(j.subject) !== JSON.stringify(s)) err(`${s.id}: subject record differs from subjects.json`);
  const r = refById.get(s.id);
  if (chapters.length !== s.chapterCount) err(`${s.id}: ${chapters.length} chapters, sheet says ${s.chapterCount}`);
  if (r?.sheetChapterNames) {
    const map = r.chapterNames ?? [];
    r.sheetChapterNames.forEach((n: string, i: number) => {
      if (map[i]?.sheet !== n) err(`${s.id}: chapter ${i + 1} not mapped to sheet name "${n}"`);
      if (chapters[i] && map[i] && chapters[i].name !== map[i].name) err(`${s.id}: chapter ${i + 1} name differs from mapping`);
    });
  }
  const stById = new Map(sts.map((t) => [t.id, t]));
  chapters.forEach((c, i) => {
    nCh++;
    const cid = `${s.id}-ch${String(i + 1).padStart(2, '0')}`;
    if (c.id !== cid || c.order !== i + 1 || c.subjectId !== s.id) err(`${cid}: id/order/subjectId wrong`);
    if (!c.name) err(`${cid}: no name`);
    if (c.subtopicIds.length < 3 || c.subtopicIds.length > 5) err(`${cid}: ${c.subtopicIds.length} subtopics (3-5)`);
    let sum = 0;
    c.subtopicIds.forEach((tid, k) => {
      const t = stById.get(tid);
      if (!t) return err(`${cid}: subtopic ${tid} missing`);
      if (t.id !== `${cid}-st${k + 1}` || t.order !== k + 1 || t.chapterId !== cid) err(`${tid}: id/order/chapterId wrong`);
      if (!t.name) err(`${tid}: no name`);
      if (!WEIGHTS.includes(t.weight)) err(`${tid}: bad weight`);
      if (!Number.isInteger(t.teachingPeriods) || t.teachingPeriods < 1) err(`${tid}: bad teachingPeriods`);
      if (!t.prerequisiteNote) err(`${tid}: prerequisiteNote missing`);
      sum += t.teachingPeriods;
      allSt.set(t.id, t);
      stSubject.set(t.id, s);
    });
    const path = c.subtopicIds.reduce((a, tid) => a + ({ L: 5, S: 6, H: 8 } as Record<string, number>)[stById.get(tid)?.weight ?? 'S'], 0);
    if (r && path > r.questionPlan.perChapter) err(`${cid}: check paths need ${path} bank items, sheet allows ${r.questionPlan.perChapter}`);
    if (sum !== c.teachingPeriods) err(`${cid}: teachingPeriods ${c.teachingPeriods} != subtopic sum ${sum}`);
  });
  if (sts.length !== chapters.reduce((a, c) => a + c.subtopicIds.length, 0)) err(`${s.id}: stray subtopics`);
}

// 6 prerequisites
for (const [id, t] of allSt) {
  const s = stSubject.get(id)!;
  for (const p of t.prerequisiteIds) {
    const m = ST_RE.exec(p);
    if (!m) { err(`${id}: bad prerequisite id ${p}`); continue; }
    const target = allSt.get(p);
    if (!target) { if (!partial || existsSync(join(DIR, `${p.replace(/-ch\d{2}-st\d$/, '')}.json`))) err(`${id}: prerequisite ${p} does not resolve`); continue; }
    const ps = stSubject.get(p)!;
    if (ps.board !== s.board) err(`${id}: prerequisite ${p} is another board`);
    if (ps.grade > s.grade) err(`${id}: prerequisite ${p} is a later grade`);
    if (ps.id === s.id && p >= id) err(`${id}: prerequisite ${p} is not earlier in the subject`);
  }
}
const state = new Map<string, number>();
const visit = (n: string, path: string[]): void => {
  state.set(n, 1);
  for (const m of allSt.get(n)?.prerequisiteIds ?? []) {
    if (state.get(m) === 1) err(`cycle: ${[...path, m].join(' -> ')}`);
    else if (!state.get(m) && allSt.has(m)) visit(m, [...path, m]);
  }
  state.set(n, 2);
};
for (const n of allSt.keys()) if (!state.get(n)) visit(n, [n]);

// 7 workbook reproduction
if (existsSync(join(DIR, 'cbse-g8-maths.json'))) {
  const j = JSON.parse(readFileSync(join(DIR, 'cbse-g8-maths.json'), 'utf8'));
  const w = j.subtopics.map((t: Subtopic) => t.weight).join('');
  const periods = j.subtopics.reduce((a: number, t: Subtopic) => a + t.teachingPeriods, 0);
  if (j.items.length !== 14 || j.subtopics.length !== 45 || periods !== 145 || w !== G8_MATHS_WEIGHTS)
    err('cbse-g8-maths: does not reproduce the workbook (14 chapters, 45 subtopics, 145 periods, weights)');
}

// 8 streams
const offered = new Set<string>();
for (const g of load('streams.json').items)
  for (const o of g.offerings) {
    if (o.subjectId === null) continue;
    if (!seen.has(o.subjectId)) err(`streams: ${g.board} g${g.grade} ${g.stream} offers unknown ${o.subjectId}`);
    offered.add(o.subjectId);
  }
for (const s of subjects) if (!offered.has(s.id)) err(`${s.id}: not offered in streams.json`);

for (const e of errors) console.log('ERROR', e);
console.log(`curriculum: ${subjects.length} subjects, ${built} subject files, ${nCh} chapters, ${allSt.size} subtopics, ` +
  `targets ${grand.toLocaleString('en-IN')} — ${errors.length} error(s)${partial ? ' (partial)' : ''}`);
process.exit(errors.length ? 1 : 0);
