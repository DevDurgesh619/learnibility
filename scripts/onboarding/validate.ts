/**
 * Onboarding forms validator (QB-ONB).
 *
 *   node scripts/onboarding/validate.ts            validate every form in data/questions/onboarding
 *   node scripts/onboarding/validate.ts --write    also write data/questions/onboarding/_status.json
 *
 * Plain Node 22 (type stripping), no dependencies. Reuses the per-question checks of the shared
 * question-bank validator (scripts/questions/validate.ts).
 *
 * Checks:
 *  1. Envelope { schemaVersion: 1, generatedBy, form, items }; formId = onb-{board}-g{grade}-{stream} = file name.
 *  2. Item IDs are {formId}-qNN, numbered 01.. without gaps; parts in order A, B, C, P.
 *  3. Part A: every Question field (shared checkQuestion); 3 or 4 groups (4 for grades 8-10); per group
 *     8 slots with the ladder pool (slot 1: D2; slot 2: D1 D2; slots 3-8: D1 D2 D3) = 21 items;
 *     C1/C2/C3 match D1/D2/D3; slots 1-4 'prerequisite', 5-8 'current'; subjectId on the form's board,
 *     prerequisites from the previous grade (grade 8: same grade + prerequisiteNote), current items from
 *     this grade; subject exists in targets.json and the chapter number is within its chapter count;
 *     subtopicId resolves in data/curriculum when that subject's file exists (else counted as unlinked).
 *  4. No duplicate stems in a form; near-duplicates (3-gram Jaccard >= 0.85) only inside the same slot.
 *  5. Part B: 16 items, 4 per domain, 4 distinct options, answer is one of them, paramIds exist.
 *  6. Part C: 30 items, 12 RIASEC items (2 per letter); every paramId exists and its tier matches
 *     parameters.json; T3 items are screened and optional.
 *  7. Parent form: 12 to 18 items, all M2-capable parameters, p30 guardian consent present and required.
 *  8. Scoring map: band cut-offs 80/65/45/0, ladder D2 start, every write/reasoning/RIASEC reference resolves.
 *  9. index.json lists every form file; all 15 designs present once the build is complete.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
// Loaded at runtime by URL so tsc/next build never sees a '.ts' import specifier (Node 22 needs the extension).
const SHARED_VALIDATOR = new URL('../questions/validate.ts', import.meta.url).href;
const { checkQuestion, loadCurriculum, normaliseStem } = await import(SHARED_VALIDATOR);

type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const DIR = process.env.ONB_DIR ?? path.join(ROOT, 'data', 'questions', 'onboarding');
const readJson = (f: string): Json => JSON.parse(fs.readFileSync(f, 'utf8'));

const LEVELS: Record<number, string[]> = { 1: ['D2'], 2: ['D1', 'D2'] };
for (let s = 3; s <= 8; s++) LEVELS[s] = ['D1', 'D2', 'D3'];
const C_OF: Record<string, string> = { D1: 'C1', D2: 'C2', D3: 'C3' };
const DESIGNS = [
  'g8-cbse', 'g8-cambridge', 'g8-ib', 'g9-cbse', 'g9-cambridge', 'g9-ib', 'g10-cbse', 'g10-cambridge', 'g10-ib',
  'g11-science', 'g11-commerce', 'g11-humanities', 'g12-science', 'g12-commerce', 'g12-humanities',
];

function shingles(norm: string): Set<string> {
  const w = norm.split(' ');
  const out = new Set<string>();
  if (w.length < 3) return new Set([norm]);
  for (let i = 0; i + 2 < w.length; i++) out.add(`${w[i]} ${w[i + 1]} ${w[i + 2]}`);
  return out;
}
function jaccard(a: Set<string>, b: Set<string>): number {
  let inter = 0;
  for (const x of a) if (b.has(x)) inter++;
  return inter / (a.size + b.size - inter || 1);
}

export interface FormReport {
  formId: string;
  errors: string[];
  warnings: string[];
  counts: Record<string, number>;
}

export function validateForm(file: string, ctx: { params: Map<string, Json>; targets: Map<string, Json> }): FormReport {
  const name = path.basename(file, '.json');
  const r: FormReport = { formId: name, errors: [], warnings: [], counts: {} };
  const e = (m: string) => r.errors.push(m);
  let data: Json;
  try {
    data = readJson(file);
  } catch (err) {
    e(`not valid JSON (${(err as Error).message})`);
    return r;
  }
  if (data.schemaVersion !== 1) e('schemaVersion must be 1');
  if (!data.generatedBy) e('generatedBy missing');
  const form = data.form;
  const items: Json[] = Array.isArray(data.items) ? data.items : [];
  if (!form) {
    e('form metadata missing');
    return r;
  }
  const m = /^onb-(cbse|cambridge|ib)-g(8|9|10|11|12)-(none|science|commerce|humanities)$/.exec(form.formId ?? '');
  if (!m) e(`bad formId ${form.formId}`);
  if (form.formId !== name) e(`formId ${form.formId} != file name ${name}`);
  const [board, grade, stream] = m ? [m[1], Number(m[2]), m[3]] : [form.board, form.grade, form.stream];
  if (form.board !== board || form.grade !== grade || form.stream !== stream) e('board/grade/stream disagree with formId');
  if ((grade <= 10) !== (stream === 'none')) e('grades 8-10 use stream none; 11-12 need a stream');

  // 2. IDs and part order
  const order = { A: 0, B: 1, C: 2, P: 3 } as Record<string, number>;
  let lastPart = -1;
  items.forEach((it, i) => {
    const want = `${form.formId}-q${String(i + 1).padStart(2, '0')}`;
    if (it.id !== want) e(`item ${i + 1}: id ${it.id}, expected ${want}`);
    const p = order[it.part];
    if (p === undefined) e(`${it.id}: bad part ${it.part}`);
    else if (p < lastPart) e(`${it.id}: part ${it.part} out of order`);
    else lastPart = p;
  });
  const A = items.filter((it) => it.part === 'A');
  const B = items.filter((it) => it.part === 'B');
  const C = items.filter((it) => it.part === 'C');
  const P = items.filter((it) => it.part === 'P');
  r.counts = { total: items.length, A: A.length, B: B.length, C: C.length, P: P.length };

  // 3. Part A
  const groups = new Map<string, Json[]>();
  for (const q of A) {
    checkQuestion(q, 'A', r.errors, false);
    if (q.set !== 'onboarding') e(`${q.id}: set must be onboarding`);
    if (C_OF[q.difficulty] !== q.conceptGroup) e(`${q.id}: ${q.difficulty} should be ${C_OF[q.difficulty]}, is ${q.conceptGroup}`);
    const half = q.slot <= 4 ? 'prerequisite' : 'current';
    if (q.half !== half) e(`${q.id}: slot ${q.slot} should be ${half}`);
    if (!q.subtopicHint) e(`${q.id}: subtopicHint missing`);
    if (typeof q.contentKey !== 'string') e(`${q.id}: contentKey missing`);
    const sm = /^(cbse|cambridge|ib)-g(\d+)-([a-z0-9-]+)$/.exec(q.subjectId ?? '');
    if (!sm) e(`${q.id}: bad subjectId ${q.subjectId}`);
    else {
      if (sm[1] !== board) e(`${q.id}: subject ${q.subjectId} is not on board ${board}`);
      const g = Number(sm[2]);
      const wantGrade = half === 'current' ? grade : grade === 8 ? 8 : grade - 1;
      if (g !== wantGrade) e(`${q.id}: ${half} item should be from grade ${wantGrade}, is ${q.subjectId}`);
      if (half === 'prerequisite' && grade === 8 && !q.prerequisiteNote) e(`${q.id}: grade 8 prerequisite needs prerequisiteNote`);
      const t = ctx.targets.get(q.subjectId);
      if (!t) e(`${q.id}: subject ${q.subjectId} not in targets.json`);
      const cm = /-ch(\d{2})$/.exec(q.chapterId ?? '');
      if (!cm || !q.chapterId.startsWith(`${q.subjectId}-ch`)) e(`${q.id}: chapterId ${q.chapterId} does not belong to ${q.subjectId}`);
      else if (t && Number(cm[1]) > t.chapters) e(`${q.id}: chapter ${cm[1]} beyond ${t.chapters} chapters of ${q.subjectId}`);
      if (!String(q.subtopicId).startsWith(`${q.chapterId}-st`)) e(`${q.id}: subtopicId ${q.subtopicId} not in ${q.chapterId}`);
    }
    const list = groups.get(q.group) ?? [];
    list.push(q);
    groups.set(q.group, list);
  }
  const wantGroups = grade <= 10 ? [4] : [3, 4];
  if (!wantGroups.includes(groups.size)) e(`Part A has ${groups.size} groups, expected ${wantGroups.join(' or ')}`);
  for (const [g, list] of groups) {
    if (list.length !== 21) e(`group ${g}: ${list.length} items, expected 21`);
    for (let s = 1; s <= 8; s++) {
      const lv = list.filter((q) => q.slot === s).map((q) => q.difficulty);
      if (lv.join(',') !== LEVELS[s].join(',')) e(`group ${g} slot ${s}: levels ${lv.join(',') || 'none'}, expected ${LEVELS[s].join(',')}`);
      const sub = new Set(list.filter((q) => q.slot === s).map((q) => q.subtopicId));
      if (sub.size > 1) e(`group ${g} slot ${s}: items point at ${sub.size} different subtopics`);
    }
  }
  // subtopic resolution
  let linked = 0;
  let unlinked = 0;
  const curCache = new Map<string, Json>();
  for (const q of A) {
    if (!curCache.has(q.subjectId)) curCache.set(q.subjectId, loadCurriculum(q.subjectId));
    const cur = curCache.get(q.subjectId);
    if (!cur) {
      unlinked++;
      continue;
    }
    if (!cur.subtopics.has(q.subtopicId)) e(`${q.id}: subtopic ${q.subtopicId} not in data/curriculum/${q.subjectId}.json (hint: ${q.subtopicHint})`);
    else if (!q.subtopicLinked) r.warnings.push(`${q.id}: resolves but subtopicLinked is false; rerun link-curriculum`);
    else linked++;
  }
  r.counts.linked = linked;
  r.counts.unlinked = unlinked;
  if (unlinked) r.warnings.push(`${unlinked} Part A items wait for curriculum files to link their subtopics`);

  // 4. duplicates
  const norms = A.map((q) => ({ q, n: normaliseStem(q.stem), sh: shingles(normaliseStem(q.stem)) }));
  const seen = new Map<string, string>();
  for (const x of norms) {
    if (seen.has(x.n)) e(`${x.q.id}: duplicate stem of ${seen.get(x.n)}`);
    else seen.set(x.n, x.q.id);
  }
  for (let i = 0; i < norms.length; i++) {
    for (let j = i + 1; j < norms.length; j++) {
      const a = norms[i].q;
      const b = norms[j].q;
      if (a.group === b.group && a.slot === b.slot) continue;
      if (jaccard(norms[i].sh, norms[j].sh) >= 0.85) e(`${b.id}: near-duplicate of ${a.id}`);
    }
  }

  // 5. Part B
  if (B.length !== 16) e(`Part B has ${B.length} items, expected 16`);
  for (const d of ['numerical', 'verbal', 'abstract', 'spatial']) {
    const n = B.filter((b) => b.domain === d).length;
    if (n !== 4) e(`Part B ${d}: ${n} items, expected 4`);
  }
  for (const b of B) {
    if (!Array.isArray(b.options) || b.options.length !== 4 || new Set(b.options).size !== 4) e(`${b.id}: needs 4 distinct options`);
    else if (b.options.filter((o: string) => o === b.answer).length !== 1) e(`${b.id}: answer not exactly one option`);
    if (!b.stem || !b.explanation) e(`${b.id}: stem/explanation missing`);
    if (!(b.seconds > 0)) e(`${b.id}: seconds missing`);
    for (const p of b.paramIds ?? []) if (!ctx.params.has(p)) e(`${b.id}: unknown parameter ${p}`);
  }

  // 6, 7. Part C and parent
  const checkSurvey = (s: Json) => {
    const p = ctx.params.get(s.paramId);
    if (!p) return e(`${s.id}: unknown parameter ${s.paramId}`);
    if (s.tier !== p.tier) e(`${s.id}: tier ${s.tier} != ${p.tier} for ${s.paramId}`);
    if (p.tier === 'T3' && (!s.screened || !s.optional)) e(`${s.id}: T3 item must be screened and optional`);
    for (const a of s.alsoInforms ?? []) if (!ctx.params.has(a)) e(`${s.id}: unknown parameter ${a}`);
    if (['single', 'multi', 'scale', 'consent'].includes(s.responseType) && !(s.options?.length >= 2)) e(`${s.id}: needs options`);
    if (!s.prompt) e(`${s.id}: prompt missing`);
  };
  if (C.length !== 30) e(`Part C has ${C.length} items, expected 30`);
  C.forEach((s) => {
    checkSurvey(s);
    if (s.respondent !== 'student') e(`${s.id}: Part C respondent must be student`);
  });
  for (const L of 'RIASEC') {
    const n = C.filter((s) => s.riasec === L).length;
    if (n !== 2) e(`RIASEC ${L}: ${n} items, expected 2`);
  }
  if (P.length < 12 || P.length > 18) e(`parent form has ${P.length} items, expected about 15`);
  P.forEach((s) => {
    checkSurvey(s);
    if (s.respondent !== 'parent') e(`${s.id}: parent item respondent must be parent`);
    const p = ctx.params.get(s.paramId);
    if (p && !p.methods.includes('M2')) r.warnings.push(`${s.id}: ${s.paramId} does not list M2 as a method`);
  });
  const consent = P.find((s) => s.paramId === 'p30');
  if (!consent) e('parent form must collect p30 guardian consent');
  else if (consent.optional) e('p30 guardian consent must be required');

  // 8. scoring map
  const sc = form.scoring ?? {};
  const cut = (sc.bandCutoffs ?? []).map((c: Json) => `${c.band}:${c.minPercent}`).sort().join(',');
  if (cut !== 'above_avg:65,average:45,below_avg:0,excellent:80') e(`band cut-offs ${cut}`);
  if (sc.ladder?.start !== 'D2' || sc.ladder?.hitsToStepUp !== 2) e('ladder must start at D2 and step up after 2 hits');
  const ids = new Set(items.map((it) => it.id));
  for (const w of sc.writes ?? []) if (!ctx.params.has(w.paramId)) e(`scoring writes unknown parameter ${w.paramId}`);
  for (const rr of sc.reasoning ?? []) for (const id of rr.itemIds) if (!ids.has(id)) e(`scoring reasoning refers to missing ${id}`);
  for (const L of Object.keys(sc.riasec ?? {})) for (const id of sc.riasec[L]) if (!ids.has(id)) e(`scoring riasec refers to missing ${id}`);
  const gs = new Set((sc.groups ?? []).map((g: Json) => g.group));
  for (const g of groups.keys()) if (!gs.has(g)) e(`scoring map missing group ${g}`);
  if (form.partA?.pool !== A.length) e(`form.partA.pool ${form.partA?.pool} != ${A.length}`);
  return r;
}

function main(argv: string[]): number {
  const params = new Map<string, Json>(readJson(path.join(ROOT, 'data', 'profile', 'parameters.json')).items.map((p: Json) => [p.id, p]));
  const targets = new Map<string, Json>(readJson(path.join(ROOT, 'data', 'questions', 'targets.json')).items.map((t: Json) => [t.subjectId, t]));
  const files = fs.readdirSync(DIR).filter((f) => /^onb-.*\.json$/.test(f)).sort();
  const reports = files.map((f) => validateForm(path.join(DIR, f), { params, targets }));
  let failed = 0;
  for (const r of reports) {
    if (r.errors.length) failed++;
    console.log(`${r.errors.length ? 'FAIL' : 'ok  '} ${r.formId}  A ${r.counts.A} B ${r.counts.B} C ${r.counts.C} P ${r.counts.P}  linked ${r.counts.linked}/${r.counts.A}`);
    for (const x of r.errors.slice(0, 30)) console.log(`     ✗ ${x}`);
    if (r.errors.length > 30) console.log(`     … ${r.errors.length - 30} more`);
  }
  // 9. index and design coverage
  const indexErrors: string[] = [];
  const idxFile = path.join(DIR, 'index.json');
  const designs = new Set<string>();
  if (!fs.existsSync(idxFile)) indexErrors.push('index.json missing');
  else {
    const idx = readJson(idxFile).items as Json[];
    const listed = new Set(idx.map((x) => `${x.formId}.json`));
    for (const f of files) if (!listed.has(f)) indexErrors.push(`index.json does not list ${f}`);
    for (const x of idx) designs.add(x.designId);
  }
  const missingDesigns = DESIGNS.filter((d) => !designs.has(d));
  const complete = files.length === 27 && missingDesigns.length === 0;
  for (const x of indexErrors) console.log(`FAIL ${x}`);
  console.log(`${reports.length - failed}/${reports.length} forms valid; designs ${designs.size}/15${missingDesigns.length ? ` (missing ${missingDesigns.join(', ')})` : ''}`);
  if (argv.includes('--write')) {
    const status = {
      schemaVersion: 1,
      generatedBy: 'scripts/onboarding/validate.ts',
      validated: failed === 0 && indexErrors.length === 0 && complete,
      complete,
      designs: [...designs].sort(),
      forms: reports.map((r) => ({ formId: r.formId, validated: r.errors.length === 0, counts: r.counts, errors: r.errors.length })),
      totals: reports.reduce((s, r) => {
        for (const k of ['total', 'A', 'B', 'C', 'P', 'linked']) s[k] = (s[k] ?? 0) + (r.counts[k] ?? 0);
        return s;
      }, {} as Record<string, number>),
      items: [],
    };
    fs.writeFileSync(path.join(DIR, '_status.json'), JSON.stringify(status, null, 2) + '\n');
  }
  return failed || indexErrors.length ? 1 : 0;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exit(main(process.argv.slice(2)));
}
