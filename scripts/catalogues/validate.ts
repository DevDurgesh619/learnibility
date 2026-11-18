/**
 * Validates /data/catalogues/*.json: IDs follow the contract, every reference resolves, values are in range.
 * Run: npx tsx scripts/catalogues/validate.ts   (exits 1 on any error)
 */
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseCatalogueId, parseParamId, parsePersonId } from '../../lib/ids';
import { BOARDS, GRADES } from '../../lib/types/enums';
import type { Career, EntranceExam, Resource, Skill, Sourced, Tutor, University } from '../../lib/types/catalogue';
import { RESOURCE_FORMATS, TEACHING_STYLES } from '../../lib/types/catalogue';

const root = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const dir = join(root, 'data', 'catalogues');
const load = <T>(name: string): T[] => JSON.parse(readFileSync(join(dir, `${name}.json`), 'utf8')).items as T[];

/** W2 owns subject slugs. Use its curriculum files when present; otherwise the contract list. */
function subjectSlugs(): Set<string> {
  const base = ['maths', 'science', 'physics', 'chemistry', 'biology', 'english', 'hindi', 'social-science', 'history', 'geography', 'economics', 'computer-science', 'psychology', 'environmental', 'accountancy', 'business', 'informatics', 'applied-maths', 'legal-studies', 'entrepreneurship', 'political-science', 'sociology', 'humanities'];
  const cur = join(root, 'data', 'curriculum');
  const found = new Set(base);
  if (existsSync(cur)) {
    for (const f of readdirSync(cur).filter((f) => f.endsWith('.json'))) {
      try {
        const items = JSON.parse(readFileSync(join(cur, f), 'utf8')).items ?? [];
        for (const it of items) if (typeof it?.slug === 'string' && typeof it?.board === 'string') found.add(it.slug);
      } catch { /* not a subject file */ }
    }
  }
  return found;
}

const errors: string[] = [];
const warnings: string[] = [];
const err = (where: string, msg: string) => errors.push(`${where}: ${msg}`);
const warn = (where: string, msg: string) => warnings.push(`${where}: ${msg}`);

const exams = load<EntranceExam>('exams');
const skills = load<Skill>('skills');
const careers = load<Career>('careers');
const tutors = load<Tutor>('tutors');
const resources = load<Resource>('resources');
const unis = load<University>('universities');

const SUBJECTS = subjectSlugs();
const examIds = new Set(exams.map((e) => e.id));
const skillIds = new Set(skills.map((s) => s.id));
const careerIds = new Set(careers.map((c) => c.id));
const uniIds = new Set(unis.map((u) => u.id));
const resIds = new Set(resources.map((r) => r.id));

const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/;
const HHMM = /^([01]\d|2[0-3]):[0-5]\d$/;
const isInt = (n: unknown) => Number.isInteger(n);

function unique(kind: string, ids: string[]) {
  const seen = new Set<string>();
  for (const id of ids) {
    if (seen.has(id)) err(kind, `duplicate id ${id}`);
    seen.add(id);
  }
}
function refs(where: string, kind: string, ids: string[], set: Set<string>) {
  for (const id of ids) if (!set.has(id)) err(where, `unknown ${kind} "${id}"`);
}
function sourced(where: string, s: Sourced<unknown> | undefined, required = true) {
  if (!s) {
    if (required) err(where, 'missing sourced fact');
    return;
  }
  if (!/^https:\/\/[^\s]+$/.test(s.sourceUrl)) err(where, `bad sourceUrl "${s.sourceUrl}"`);
  if (!ISO_DATE.test(s.asOf)) err(where, `bad asOf "${s.asOf}"`);
  if (typeof s.verified !== 'boolean') err(where, 'verified must be boolean');
}

// ---------------------------------------------------------------- exams
unique('exams', exams.map((e) => e.id));
for (const e of exams) {
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(e.id)) err(`exam ${e.id}`, 'id must be a kebab slug');
  if (!isInt(e.feeInr) || e.feeInr <= 0) err(`exam ${e.id}`, 'feeInr must be a positive integer');
}

// ---------------------------------------------------------------- skills
unique('skills', skills.map((s) => s.id));
for (const s of skills) {
  const w = `skill ${s.id}`;
  if (parseCatalogueId(s.id)?.kind !== 'skill') err(w, 'id must be skill-{slug}');
  if (s.levelDescriptors.length !== 5) err(w, 'needs 5 level descriptors');
  if (s.hoursPerLevel.length !== 5 || s.hoursPerLevel.some((h) => h <= 0)) err(w, 'hoursPerLevel needs 5 positive values');
  for (const sl of s.subjectSlugs) if (!SUBJECTS.has(sl)) err(w, `unknown subject slug "${sl}"`);
  for (const p of s.profileParamIds) if (parseParamId(p) === null) err(w, `bad profile parameter "${p}"`);
  refs(w, 'resource', s.resourceIds, resIds);
  if (s.resourceIds.length === 0) warn(w, 'no resource builds this skill');
}

// ---------------------------------------------------------------- careers
unique('careers', careers.map((c) => c.id));
for (const c of careers) {
  const w = `career ${c.id}`;
  if (parseCatalogueId(c.id)?.kind !== 'career') err(w, 'id must be career-{slug}');
  refs(w, 'skill', c.skills.map((s) => s.skillId), skillIds);
  refs(w, 'related career', c.relatedCareerIds, careerIds);
  for (const s of c.subjects) if (!SUBJECTS.has(s.subjectSlug)) err(w, `unknown subject slug "${s.subjectSlug}"`);
  for (const p of c.aptitudeParamIds) if (parseParamId(p) === null) err(w, `bad aptitude parameter "${p}"`);
  if (c.skills.filter((s) => s.importance === 'core').length < 3) err(w, 'needs at least 3 core skills');
  if (!c.pathways.some((p) => p.region === 'india')) err(w, 'needs an India pathway');
  for (const p of c.pathways) {
    refs(`${w} / ${p.id}`, 'exam', p.examIds, examIds);
    refs(`${w} / ${p.id}`, 'university', p.universityIds, uniIds);
    const { low, typical, high } = p.costInr;
    if (![low, typical, high].every(isInt) || !(low <= typical && typical <= high)) err(`${w} / ${p.id}`, 'costInr must be integer low <= typical <= high');
    if ((p.region === 'india') !== (p.country === 'in')) err(`${w} / ${p.id}`, 'region and country disagree');
  }
  const sal = c.salaryInr;
  if (!(sal.entryLow <= sal.entryHigh && sal.entryHigh <= sal.senior)) err(w, 'salary band out of order');
  const share = c.topCities.reduce((a, b) => a + b.sharePct, 0);
  if (share > 100) err(w, `topCities shares sum to ${share}`);
}

// ---------------------------------------------------------------- tutors
unique('tutors', tutors.map((t) => t.id));
for (const t of tutors) {
  const w = `tutor ${t.id}`;
  if (parsePersonId(t.id)?.kind !== 'tutor') err(w, 'id must be tut_{first}_{last}');
  for (const s of t.subjects) {
    if (!SUBJECTS.has(s.subjectSlug)) err(w, `unknown subject slug "${s.subjectSlug}"`);
    for (const b of s.boards) if (!(BOARDS as readonly string[]).includes(b)) err(w, `bad board ${b}`);
    for (const g of s.grades) if (!(GRADES as readonly number[]).includes(g)) err(w, `bad grade ${g}`);
    if (s.topicStrengths.length === 0) err(w, `no topic strengths for ${s.subjectSlug}`);
  }
  refs(w, 'exam', t.examPrep, examIds);
  for (const st of t.teachingStyles) if (!(TEACHING_STYLES as readonly string[]).includes(st)) err(w, `bad style ${st}`);
  const p = t.pricing;
  if (!isInt(p.oneToOnePerHourInr) || p.oneToOnePerHourInr < 300 || p.oneToOnePerHourInr > 1500) err(w, `1:1 price ₹${p.oneToOnePerHourInr} outside ₹300-1,500`);
  if (t.formats.includes('group') !== (p.groupPerStudentPerHourInr !== null)) err(w, 'group price must exist exactly when format includes group');
  if (p.groupPerStudentPerHourInr !== null && p.groupPerStudentPerHourInr >= p.oneToOnePerHourInr) err(w, 'group price should be below 1:1');
  if (t.rating < 0 || t.rating > 5) err(w, 'rating out of range');
  if (t.rebookPct < 0 || t.rebookPct > 100) err(w, 'rebookPct out of range');
  if (t.availability.length === 0) err(w, 'no availability');
  for (const a of t.availability) if (!HHMM.test(a.start) || !HHMM.test(a.end) || a.start >= a.end) err(w, `bad slot ${a.day} ${a.start}-${a.end}`);
  if (t.modes.includes('offline') && !t.offlineArea) err(w, 'offline tutor needs offlineArea');
  if (t.reviews.length === 0) warn(w, 'no sample reviews');
}

// ---------------------------------------------------------------- resources
unique('resources', resources.map((r) => r.id));
for (const r of resources) {
  const w = `resource ${r.id}`;
  const kind = parseCatalogueId(r.id)?.kind;
  if (r.kind === 'free_resource' && (kind !== 'res' || r.priceInr !== 0)) err(w, 'free resources are res-{slug} and ₹0');
  if (r.kind === 'paid_course' && (kind !== 'course' || r.priceInr <= 0)) err(w, 'paid courses are course-{slug} with a price');
  if (!isInt(r.priceInr)) err(w, 'priceInr must be an integer');
  if (!(RESOURCE_FORMATS as readonly string[]).includes(r.format)) err(w, `bad format ${r.format}`);
  for (const s of r.subjectSlugs) if (!SUBJECTS.has(s)) err(w, `unknown subject slug "${s}"`);
  refs(w, 'skill', r.skillOutcomes.map((o) => o.skillId), skillIds);
  refs(w, 'exam', r.examIds, examIds);
  if (!/^https:\/\//.test(r.url)) err(w, 'url must be https');
}

// ---------------------------------------------------------------- universities
unique('universities', unis.map((u) => u.id));
for (const u of unis) {
  const w = `uni ${u.id}`;
  const parsed = parseCatalogueId(u.id);
  if (parsed?.kind !== 'uni' || parsed.country !== u.country) err(w, 'id must be uni-{country}-{slug} matching country');
  sourced(`${w} qsWorldRank`, u.qsWorldRank);
  sourced(`${w} acceptanceRatePct`, u.acceptanceRatePct);
  sourced(`${w} intlStudentPct`, u.intlStudentPct);
  sourced(`${w} tuition`, u.tuition);
  if (u.nirfRank) sourced(`${w} nirfRank`, u.nirfRank);
  for (const n of ['tuitionInrPerYear', 'livingInrPerYear', 'totalCostInr'] as const) if (!isInt(u[n]) || u[n] <= 0) err(w, `${n} must be a positive integer`);
  if (u.programmes.length === 0) err(w, 'no programmes');
  for (const p of u.programmes) {
    if (!p.id.startsWith(`${u.id}-`)) err(w, `programme id ${p.id} must start with ${u.id}-`);
    refs(`${w} / ${p.id}`, 'career', p.careerIds, careerIds);
    refs(`${w} / ${p.id}`, 'exam', p.entryExamIds, examIds);
    if (p.cutoff) sourced(`${w} / ${p.id} cutoff`, p.cutoff);
  }
  if (u.applicationRoutes.length === 0) err(w, 'no application routes');
  for (const r of u.applicationRoutes) {
    sourced(`${w} ${r.type} deadline`, r.deadline);
    if (!ISO_DATE.test(r.deadline.value)) err(w, `${r.type} deadline "${r.deadline.value}" is not YYYY-MM-DD`);
    else if (r.deadline.value < '2026-08-01' || r.deadline.value > '2027-08-31') warn(w, `${r.type} deadline ${r.deadline.value} is outside the 2027-intake window`);
    refs(`${w} ${r.type}`, 'exam', r.requirements.examIds, examIds);
    if (!isInt(r.requirements.applicationFeeInr)) err(w, `${r.type} applicationFeeInr must be an integer`);
  }
  for (const s of u.scholarships) sourced(`${w} scholarship ${s.name}`, s.amount);
}

// ---------------------------------------------------------------- coverage checks from the brief
const families = new Set(tutors.flatMap((t) => t.subjects.map((s) => s.subjectSlug)));
for (const need of ['maths', 'physics', 'chemistry', 'biology', 'science', 'english', 'hindi', 'accountancy', 'economics', 'business', 'history', 'political-science', 'geography', 'psychology', 'computer-science', 'legal-studies', 'social-science'])
  if (!families.has(need)) err('tutors', `no tutor teaches ${need}`);
for (const b of BOARDS) if (!tutors.some((t) => t.subjects.some((s) => s.boards.includes(b)))) err('tutors', `no tutor covers board ${b}`);
for (const st of ['science', 'commerce', 'humanities'] as const) if (!careers.some((c) => c.streams.includes(st))) err('careers', `no career for ${st}`);
if (!tutors.some((t) => t.id === 'tut_rahul_verma')) err('tutors', 'Rahul Verma missing');

const verified = unis.flatMap((u) => [u.qsWorldRank, u.acceptanceRatePct, u.intlStudentPct, u.tuition, ...u.applicationRoutes.map((r) => r.deadline)]).filter((s) => s.verified).length;
console.log(`exams ${exams.length} · skills ${skills.length} · careers ${careers.length} · tutors ${tutors.length} · resources ${resources.length} · universities ${unis.length} (${verified} core facts verified)`);
for (const x of warnings) console.log(`warn  ${x}`);
for (const x of errors) console.log(`ERROR ${x}`);
console.log(errors.length ? `\n${errors.length} errors` : '\nOK: catalogues valid');
process.exit(errors.length ? 1 : 0);
