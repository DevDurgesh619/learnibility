/**
 * Shared question-bank validator (QB-CBSE, QB-CAM, QB-IB, QB-ONB all run this).
 *
 *   node scripts/questions/validate.ts cbse-g8-maths           one subject
 *   node scripts/questions/validate.ts --board cbse            every subject of a board that has files
 *   node scripts/questions/validate.ts --all                   every subject that has files
 *   add --write    to record the result in data/questions/{subjectId}/_status.json (validated, counts, errors)
 *   add --totals   to also check board totals against the cost sheet (only passes when the whole board is done)
 *   add --quiet    to print only failing subjects
 *
 * Runs on plain Node 22+ (type stripping) or `npx tsx`. No dependencies.
 *
 * Checks (brief: build/question-bank-briefs.md, "Quality"):
 *  1. Envelope { schemaVersion: 1, generatedBy, items } on every file.
 *  2. Every Question field present and typed; enums valid; likelyGapOnWrong present.
 *  3. IDs follow the contract (bank {subtopicId}-qNN, practice {chapterId}-pfa|pfb-qNN,
 *     mocks {subjectId}-mockN-qNN) and agree with subtopicId / chapterId / subjectId / set / file.
 *  4. Every subtopicId and chapterId resolves in data/curriculum/{subjectId}.json.
 *  5. Counts equal the cost sheet (data/questions/targets.json): bank per chapter,
 *     questions per practice form, mocks x questions per mock, subject total, and
 *     the subject total equals questionTarget in data/curriculum/subjects.json when present.
 *  6. Tag mix of the mastery bank within +-5 points of target
 *     (C1 15, C2 30, C3 35, C4 20; D1 10, D2 40, D3 35, D4 12, D5 3).
 *  7. Each subtopic's bank has the student-check path (L 5, S 6, H 8 items at least) and all of C1-C4;
 *     1 to 4 retention probes per subtopic; transfer probes only on C3-D4/D5 or C4-D3+.
 *  8. Practice Form A and Form B are parallel: same subtopic, C and D at every position.
 *  9. No duplicate or near-duplicate stems within a subject (normalised text; word 3-gram Jaccard >= 0.85
 *     within a chapter).
 * 10. MCQs have exactly 4 distinct options and the answer equals exactly one of them.
 * 11. Marks and minutes are positive and sane; every mock carries the same total marks.
 * 12. Hindi subjects: stems are written in Devanagari.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
/** Overridable for tests: QB_QUESTIONS_DIR, QB_CURRICULUM_DIR. */
const Q_DIR = process.env.QB_QUESTIONS_DIR ?? path.join(ROOT, 'data', 'questions');
const CUR_DIR = process.env.QB_CURRICULUM_DIR ?? path.join(ROOT, 'data', 'curriculum');
const TARGETS = path.join(ROOT, 'data', 'questions', 'targets.json');

const CONCEPT_GROUPS = ['C1', 'C2', 'C3', 'C4'];
const DIFFICULTIES = ['D1', 'D2', 'D3', 'D4', 'D5'];
const ALR_ROLES = ['practised', 'retention_probe', 'transfer_probe'];
const GAP_CODES = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10'];
const TYPES = ['mcq', 'short', 'explain', 'numerical', 'multi_step', 'case', 'long'];
const SETS = ['mastery_bank', 'practice_form_a', 'practice_form_b', 'mock', 'onboarding'];
const C_TARGET: Record<string, number> = { C1: 15, C2: 30, C3: 35, C4: 20 };
const D_TARGET: Record<string, number> = { D1: 10, D2: 40, D3: 35, D4: 12, D5: 3 };
const CHECK_PATH: Record<string, number> = { L: 5, S: 6, H: 8 };
const MIX_TOLERANCE = 5;
const NEAR_DUP = 0.85;
const BOARD_TOTALS: Record<string, number> = { cbse: 63582, cambridge: 62540, ib: 53893 };

export interface Report {
  subjectId: string;
  errors: string[];
  warnings: string[];
  counts: Record<string, number>;
  mix?: { C: Record<string, number>; D: Record<string, number> };
}

// ---------- helpers ----------

function readJson(file: string): Json {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function envelopeItems(file: string, errors: string[]): Json[] {
  let data: Json;
  try {
    data = readJson(file);
  } catch (e) {
    errors.push(`${rel(file)}: not valid JSON (${(e as Error).message})`);
    return [];
  }
  if (data?.schemaVersion !== 1) errors.push(`${rel(file)}: schemaVersion must be 1`);
  if (typeof data?.generatedBy !== 'string' || !data.generatedBy) errors.push(`${rel(file)}: generatedBy missing`);
  if (!Array.isArray(data?.items)) {
    errors.push(`${rel(file)}: items must be an array`);
    return [];
  }
  return data.items;
}

const rel = (f: string) => path.relative(ROOT, f);

/** Lowercase, drop punctuation and option letters, collapse spaces. Digits are kept. */
export function normaliseStem(s: string): string {
  return s
    .normalize('NFKC')
    .toLowerCase()
    .replace(/\([a-d]\)/g, ' ')
    .replace(/[^\p{L}\p{N}\p{M}]+/gu, ' ')
    .trim()
    .replace(/\s+/g, ' ');
}

/**
 * Text compared for duplicates: the stem, plus the options for MCQs (two MCQs may share a stem such as
 * "Which of these is a perfect cube?" when their options differ). Assertion-Reason items share the four
 * standard options, so only their stem is compared.
 */
export function dupText(q: Json): string {
  const opts = Array.isArray(q.options) && !/^Assertion \(A\)/.test(q.stem) ? ' ' + [...q.options].map(String).sort().join(' ') : '';
  return String(q.stem) + opts;
}

function shingles(norm: string): Set<string> {
  const w = norm.split(' ');
  const out = new Set<string>();
  if (w.length < 3) {
    out.add(norm);
    return out;
  }
  for (let i = 0; i + 2 < w.length; i++) out.add(`${w[i]} ${w[i + 1]} ${w[i + 2]}`);
  return out;
}

function jaccard(a: Set<string>, b: Set<string>): number {
  let inter = 0;
  for (const x of a) if (b.has(x)) inter++;
  return inter / (a.size + b.size - inter || 1);
}

export function devanagariShare(s: string): number {
  const letters = s.match(/\p{L}/gu) ?? [];
  if (!letters.length) return 0;
  const dev = s.match(/[ऀ-ॿ]/gu) ?? [];
  const devLetters = dev.filter((c) => /\p{L}/u.test(c)).length;
  return devLetters / letters.length;
}

const pct = (n: number, d: number) => (d ? Math.round((1000 * n) / d) / 10 : 0);

// ---------- curriculum ----------

interface Curriculum {
  chapters: Map<string, Json>;
  subtopics: Map<string, Json>;
}

const CH_RE = /^[a-z]+-g\d+-[a-z0-9-]+-ch\d{2}$/;
const ST_RE = /^[a-z]+-g\d+-[a-z0-9-]+-ch\d{2}-st\d+$/;

/** Collect chapters and subtopics from a W2 curriculum file, whatever its exact nesting. */
export function loadCurriculum(subjectId: string): Curriculum | null {
  const file = path.join(CUR_DIR, `${subjectId}.json`);
  if (!fs.existsSync(file)) return null;
  const cur: Curriculum = { chapters: new Map(), subtopics: new Map() };
  const walk = (v: Json) => {
    if (Array.isArray(v)) return v.forEach(walk);
    if (!v || typeof v !== 'object') return;
    if (typeof v.id === 'string') {
      if (ST_RE.test(v.id)) cur.subtopics.set(v.id, v);
      else if (CH_RE.test(v.id)) cur.chapters.set(v.id, v);
    }
    for (const k of Object.keys(v)) if (typeof v[k] === 'object') walk(v[k]);
  };
  walk(readJson(file));
  return cur;
}

function subjectsIndex(): Map<string, Json> {
  const file = path.join(CUR_DIR, 'subjects.json');
  const m = new Map<string, Json>();
  if (!fs.existsSync(file)) return m;
  const data = readJson(file);
  for (const s of data.items ?? []) m.set(s.id, s);
  return m;
}

function targetsIndex(): Map<string, Json> {
  const m = new Map<string, Json>();
  const data = readJson(TARGETS);
  for (const t of data.items) m.set(t.subjectId, t);
  return m;
}

// ---------- per-question checks ----------

export function checkQuestion(q: Json, where: string, errors: string[], hindi: boolean): void {
  const id = q?.id ?? '(no id)';
  const e = (msg: string) => errors.push(`${where} ${id}: ${msg}`);
  for (const f of ['id', 'subtopicId', 'chapterId', 'subjectId', 'stem', 'answer', 'markingKey']) {
    if (typeof q[f] !== 'string' || !q[f].trim()) e(`${f} missing or empty`);
  }
  if (!CONCEPT_GROUPS.includes(q.conceptGroup)) e(`bad conceptGroup ${q.conceptGroup}`);
  if (!DIFFICULTIES.includes(q.difficulty)) e(`bad difficulty ${q.difficulty}`);
  if (!TYPES.includes(q.type)) e(`bad type ${q.type}`);
  if (!SETS.includes(q.set)) e(`bad set ${q.set}`);
  if (!ALR_ROLES.includes(q.alrRole)) e(`bad alrRole ${q.alrRole}`);
  if (!GAP_CODES.includes(q.likelyGapOnWrong)) e(`likelyGapOnWrong missing or bad (${q.likelyGapOnWrong})`);
  if (q.legacyId !== undefined && typeof q.legacyId !== 'string') e('legacyId must be a string');
  if (typeof q.marks !== 'number' || !(q.marks > 0) || q.marks > 20) e(`marks out of range (${q.marks})`);
  if (typeof q.minutes !== 'number' || !(q.minutes > 0) || q.minutes > 60) e(`minutes out of range (${q.minutes})`);
  if (q.type === 'mcq') {
    if (!Array.isArray(q.options) || q.options.length !== 4) e('MCQ needs exactly 4 options');
    else {
      if (new Set(q.options.map((o: string) => String(o).normalize('NFKC').toLowerCase().replace(/\s+/g, ' ').trim())).size !== 4) e('MCQ options not distinct');
      const hits = q.options.filter((o: string) => o === q.answer).length;
      if (hits !== 1) e(`MCQ answer must equal exactly one option (matches ${hits})`);
    }
  } else if (q.options !== undefined && (!Array.isArray(q.options) || q.options.length === 0)) {
    e('options, when present, must be a non-empty array');
  }
  if (q.alrRole === 'transfer_probe') {
    const d = Number(String(q.difficulty).slice(1));
    const ok = (q.conceptGroup === 'C3' && d >= 4) || (q.conceptGroup === 'C4' && d >= 3);
    if (!ok) e(`transfer probe must be C3-D4/D5 or C4-D3+ (is ${q.conceptGroup}-${q.difficulty})`);
  }
  if (hindi && typeof q.stem === 'string' && devanagariShare(q.stem) < 0.6) {
    e(`Hindi stem not in Devanagari (${Math.round(devanagariShare(q.stem) * 100)}%)`);
  }
}

// ---------- subject ----------

export function validateSubject(subjectId: string, opts: { targets?: Map<string, Json>; subjects?: Map<string, Json> } = {}): Report {
  const errors: string[] = [];
  const warnings: string[] = [];
  const counts: Record<string, number> = {};
  const report: Report = { subjectId, errors, warnings, counts };
  const targets = opts.targets ?? targetsIndex();
  const subjects = opts.subjects ?? subjectsIndex();
  const t = targets.get(subjectId);
  if (!t) {
    errors.push(`no cost-sheet target for ${subjectId} in data/questions/targets.json`);
    return report;
  }
  const subj = subjects.get(subjectId);
  if (subj && subj.questionTarget !== t.total) {
    errors.push(`subjects.json questionTarget ${subj.questionTarget} != cost sheet ${t.total}`);
  }
  const hindi = /-hindi(-b)?$/.test(subjectId);
  const dir = path.join(Q_DIR, subjectId);
  if (!fs.existsSync(dir)) {
    errors.push(`no folder data/questions/${subjectId}`);
    return report;
  }
  const cur = loadCurriculum(subjectId);
  if (!cur) errors.push(`curriculum file data/curriculum/${subjectId}.json missing`);
  else if (cur.chapters.size !== t.chapters) {
    errors.push(`curriculum has ${cur.chapters.size} chapters, cost sheet ${t.chapters}`);
  }

  const all: Json[] = [];
  const ids = new Set<string>();
  const add = (q: Json, where: string) => {
    if (ids.has(q?.id)) errors.push(`${where} ${q?.id}: duplicate id`);
    ids.add(q?.id);
    all.push(q);
    checkQuestion(q, where, errors, hindi);
    if (q?.subjectId !== subjectId) errors.push(`${where} ${q?.id}: subjectId ${q?.subjectId} != ${subjectId}`);
    if (cur && q?.subtopicId) {
      const st = cur.subtopics.get(q.subtopicId);
      if (!st) errors.push(`${where} ${q.id}: subtopicId ${q.subtopicId} not in curriculum`);
      else if (!q.subtopicId.startsWith(`${q.chapterId}-st`)) {
        errors.push(`${where} ${q.id}: subtopic ${q.subtopicId} not in chapter ${q.chapterId}`);
      }
    }
  };

  // Chapter files
  const chapterIds = cur ? [...cur.chapters.keys()].sort() : [];
  const files = fs.readdirSync(dir).filter((f) => f.endsWith('.json') && !f.startsWith('_'));
  for (const f of files) {
    if (f === 'mocks.json') continue;
    const chId = f.replace(/\.json$/, '');
    if (!CH_RE.test(chId) || !chId.startsWith(`${subjectId}-ch`)) errors.push(`unexpected file ${f}`);
    else if (cur && !cur.chapters.has(chId)) errors.push(`${f}: chapter not in curriculum`);
  }
  const expectedChapters = chapterIds.length ? chapterIds : files.filter((f) => f !== 'mocks.json').map((f) => f.slice(0, -5));
  const bank: Json[] = [];
  let practiceTotal = 0;
  for (const chId of expectedChapters) {
    const file = path.join(dir, `${chId}.json`);
    if (!fs.existsSync(file)) {
      errors.push(`${chId}: file missing`);
      continue;
    }
    const items = envelopeItems(file, errors);
    const where = `${chId}.json`;
    const chBank: Json[] = [];
    const formA: Json[] = [];
    const formB: Json[] = [];
    for (const q of items) {
      add(q, where);
      if (q?.chapterId !== chId) errors.push(`${where} ${q?.id}: chapterId ${q?.chapterId} != ${chId}`);
      const id = String(q?.id ?? '');
      if (q.set === 'mastery_bank') {
        chBank.push(q);
        if (!new RegExp(`^${q.subtopicId}-q\\d{2,}$`).test(id)) errors.push(`${where} ${id}: bank id must be {subtopicId}-qNN`);
      } else if (q.set === 'practice_form_a' || q.set === 'practice_form_b') {
        const form = q.set === 'practice_form_a' ? 'a' : 'b';
        (form === 'a' ? formA : formB).push(q);
        if (!new RegExp(`^${chId}-pf${form}-q\\d{2,}$`).test(id)) errors.push(`${where} ${id}: practice id must be ${chId}-pf${form}-qNN`);
      } else errors.push(`${where} ${id}: set ${q.set} does not belong in a chapter file`);
    }
    bank.push(...chBank);
    practiceTotal += formA.length + formB.length;
    if (chBank.length !== t.bankPerChapter) errors.push(`${chId}: mastery bank ${chBank.length}, cost sheet ${t.bankPerChapter}`);
    if (formA.length !== t.questionsPerForm) errors.push(`${chId}: Form A ${formA.length}, cost sheet ${t.questionsPerForm}`);
    if (formB.length !== t.questionsPerForm) errors.push(`${chId}: Form B ${formB.length}, cost sheet ${t.questionsPerForm}`);
    // parallel forms
    const byNum = (a: Json, b: Json) => a.id.localeCompare(b.id);
    formA.sort(byNum);
    formB.sort(byNum);
    for (let i = 0; i < Math.min(formA.length, formB.length); i++) {
      const a = formA[i];
      const b = formB[i];
      if (a.subtopicId !== b.subtopicId || a.conceptGroup !== b.conceptGroup || a.difficulty !== b.difficulty) {
        errors.push(`${chId}: forms not parallel at position ${i + 1} (${a.id} vs ${b.id})`);
      }
    }
    // per-subtopic path and probes
    if (cur) {
      const chapter = cur.chapters.get(chId);
      const stIds: string[] = chapter?.subtopicIds ?? [...cur.subtopics.keys()].filter((s) => s.startsWith(`${chId}-st`));
      for (const stId of stIds) {
        const st = cur.subtopics.get(stId);
        const items = chBank.filter((q) => q.subtopicId === stId);
        const need = CHECK_PATH[st?.weight] ?? 5;
        if (items.length < need) errors.push(`${stId}: ${items.length} bank items, check path needs ${need}`);
        const groups = new Set(items.map((q) => q.conceptGroup));
        for (const c of CONCEPT_GROUPS) if (!groups.has(c)) errors.push(`${stId}: no ${c} item in bank`);
        const probes = items.filter((q) => q.alrRole === 'retention_probe').length;
        if (probes < 1 || probes > 4) errors.push(`${stId}: ${probes} retention probes (want about 2)`);
        if (!items.some((q) => q.alrRole === 'transfer_probe')) warnings.push(`${stId}: no transfer probe`);
      }
    }
  }

  // Mocks
  const mockFile = path.join(dir, 'mocks.json');
  let mockTotal = 0;
  if (!fs.existsSync(mockFile)) errors.push('mocks.json missing');
  else {
    const items = envelopeItems(mockFile, errors);
    const byMock = new Map<number, Json[]>();
    for (const q of items) {
      add(q, 'mocks.json');
      const m = new RegExp(`^${subjectId}-mock(\\d+)-q\\d{2,}$`).exec(String(q?.id));
      if (!m) {
        errors.push(`mocks.json ${q?.id}: id must be ${subjectId}-mockN-qNN`);
        continue;
      }
      if (q.set !== 'mock') errors.push(`mocks.json ${q.id}: set must be mock`);
      const n = Number(m[1]);
      if (!byMock.has(n)) byMock.set(n, []);
      byMock.get(n)!.push(q);
    }
    mockTotal = items.length;
    if (byMock.size !== t.mocks) errors.push(`mocks.json: ${byMock.size} mocks, cost sheet ${t.mocks}`);
    const marks = new Set<number>();
    for (const [n, qs] of byMock) {
      if (n < 1 || n > t.mocks) errors.push(`mocks.json: unexpected mock${n}`);
      if (qs.length !== t.questionsPerMock) errors.push(`mock${n}: ${qs.length} questions, cost sheet ${t.questionsPerMock}`);
      marks.add(qs.reduce((s, q) => s + (Number(q.marks) || 0), 0));
    }
    if (marks.size > 1) errors.push(`mocks carry different total marks (${[...marks].join(', ')})`);
  }

  // Duplicates
  const seen = new Map<string, string>();
  for (const q of all) {
    if (typeof q?.stem !== 'string') continue;
    const n = normaliseStem(dupText(q));
    const prev = seen.get(n);
    if (prev) errors.push(`duplicate stem: ${q.id} = ${prev}`);
    else seen.set(n, q.id);
  }
  const byChapter = new Map<string, { id: string; sh: Set<string>; len: number }[]>();
  for (const q of all) {
    if (typeof q?.stem !== 'string') continue;
    const key = q.chapterId;
    if (!byChapter.has(key)) byChapter.set(key, []);
    const norm = normaliseStem(dupText(q));
    byChapter.get(key)!.push({ id: q.id, sh: shingles(norm), len: norm.length });
  }
  for (const list of byChapter.values()) {
    for (let i = 0; i < list.length; i++) {
      for (let j = i + 1; j < list.length; j++) {
        const a = list[i];
        const b = list[j];
        if (Math.min(a.len, b.len) / Math.max(a.len, b.len) < 0.7) continue;
        if (a.sh.size === b.sh.size && [...a.sh].every((x) => b.sh.has(x))) continue; // exact duplicate, reported above
        if (jaccard(a.sh, b.sh) >= NEAR_DUP) errors.push(`near-duplicate stems: ${a.id} ~ ${b.id}`);
      }
    }
  }

  // Tag mix
  const cMix: Record<string, number> = {};
  const dMix: Record<string, number> = {};
  for (const c of CONCEPT_GROUPS) cMix[c] = pct(bank.filter((q) => q.conceptGroup === c).length, bank.length);
  for (const d of DIFFICULTIES) dMix[d] = pct(bank.filter((q) => q.difficulty === d).length, bank.length);
  report.mix = { C: cMix, D: dMix };
  if (bank.length) {
    for (const c of CONCEPT_GROUPS) {
      if (Math.abs(cMix[c] - C_TARGET[c]) > MIX_TOLERANCE) errors.push(`tag mix ${c} ${cMix[c]}% (target ${C_TARGET[c]} +-${MIX_TOLERANCE})`);
    }
    for (const d of DIFFICULTIES) {
      if (Math.abs(dMix[d] - D_TARGET[d]) > MIX_TOLERANCE) errors.push(`tag mix ${d} ${dMix[d]}% (target ${D_TARGET[d]} +-${MIX_TOLERANCE})`);
    }
  }

  counts.mastery_bank = bank.length;
  counts.practice = practiceTotal;
  counts.mock = mockTotal;
  counts.total = all.length;
  if (all.length !== t.total) errors.push(`subject total ${all.length}, cost sheet ${t.total}`);
  return report;
}

function writeStatus(r: Report): void {
  const file = path.join(Q_DIR, r.subjectId, '_status.json');
  if (!fs.existsSync(path.dirname(file))) return;
  const prev = fs.existsSync(file) ? readJson(file) : {};
  const next = {
    ...prev,
    subjectId: r.subjectId,
    counts: r.counts,
    mix: r.mix,
    validated: r.errors.length === 0,
    validatedAt: new Date().toISOString(),
    validationErrors: r.errors.slice(0, 200),
    validationErrorCount: r.errors.length,
    validationWarnings: r.warnings.slice(0, 50),
  };
  fs.writeFileSync(file, JSON.stringify(next, null, 2) + '\n');
}

function main(argv: string[]): number {
  const flags = new Set(argv.filter((a) => a.startsWith('--')));
  const args = argv.filter((a) => !a.startsWith('--'));
  const boardIdx = argv.indexOf('--board');
  const board = boardIdx >= 0 ? argv[boardIdx + 1] : undefined;
  const targets = targetsIndex();
  const subjects = subjectsIndex();
  let ids: string[] = args.filter((a) => a !== board);
  if (flags.has('--all') || board) {
    ids = [...targets.keys()].filter((id) => (!board || id.startsWith(`${board}-`)) && fs.existsSync(path.join(Q_DIR, id)));
  }
  if (!ids.length) {
    console.error('usage: node scripts/questions/validate.ts <subjectId...> | --board <b> | --all [--write] [--totals] [--quiet]');
    return 2;
  }
  let failed = 0;
  const totals: Record<string, number> = {};
  for (const id of ids) {
    const r = validateSubject(id, { targets, subjects });
    if (flags.has('--write')) writeStatus(r);
    const b = id.split('-')[0];
    totals[b] = (totals[b] ?? 0) + (r.errors.length ? 0 : r.counts.total ?? 0);
    if (r.errors.length) failed++;
    if (r.errors.length || !flags.has('--quiet')) {
      const mix = r.mix ? ` C ${Object.values(r.mix.C).join('/')} D ${Object.values(r.mix.D).join('/')}` : '';
      console.log(`${r.errors.length ? 'FAIL' : 'ok  '} ${id}  ${r.counts.total ?? 0} questions${mix}`);
      for (const e of r.errors.slice(0, 25)) console.log(`     ✗ ${e}`);
      if (r.errors.length > 25) console.log(`     … ${r.errors.length - 25} more`);
      if (!flags.has('--quiet')) for (const w of r.warnings.slice(0, 5)) console.log(`     ! ${w}`);
    }
  }
  if (flags.has('--totals')) {
    for (const [b, want] of Object.entries(BOARD_TOTALS)) {
      if (board && b !== board) continue;
      const got = totals[b] ?? 0;
      console.log(`${got === want ? 'ok  ' : 'FAIL'} ${b} validated total ${got} / ${want}`);
      if (got !== want) failed++;
    }
  }
  console.log(`${ids.length - failed}/${ids.length} subjects valid`);
  return failed ? 1 : 0;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exit(main(process.argv.slice(2)));
}
