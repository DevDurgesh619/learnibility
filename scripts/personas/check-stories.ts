/**
 * W3-P: asserts the written persona files.
 *
 *   npx tsx scripts/personas/check-stories.ts
 *
 * 1. Each student's headline facts (scripts/personas/stories.ts), read back from data/personas/students/.
 * 2. Zoya is brand new (account, parent and consent only); Aarav and Ananya share one parent account.
 * 3. Privacy: no T3 value appears in any parent-, teacher-, tutor- or mentor-facing file or record.
 * 4. Every ID resolves: questions, subtopics, chapters, subjects, tutors, adults, sections, universities,
 *    programmes, careers, bookings, meeting notes and homework tasks.
 * Exit code 1 on any failure.
 */
import fs from 'node:fs';
import path from 'node:path';
import { failures, STORIES } from './stories';

const ROOT = process.cwd();
const D = (...p: string[]) => path.join(ROOT, 'data', ...p);
const items = <T = Record<string, any>>(f: string): T[] => (fs.existsSync(f) ? JSON.parse(fs.readFileSync(f, 'utf8')).items : []);
const errors: string[] = [];
const fail = (m: string) => errors.push(m);

const FILES = ['alr', 'attempts', 'bookings', 'careers', 'consents', 'documents', 'events', 'gaps', 'invoices', 'mastery', 'meetings', 'messages', 'plans', 'profile', 'requests', 'sessions', 'shortlist', 'student', 'tasks', 'timetable'];
const OPTIONAL = ['applications', 'finance', 'assignments', 'tutorNotes', 'approvals', 'comments'];

// ------------------------------------------------------------------ catalogues and curriculum
const subjects = new Set(items(D('curriculum', 'subjects.json')).map((s) => s.id));
const chapters = new Set<string>();
const subtopics = new Set<string>();
const subjectFiles = new Map<string, boolean>();
const loadSubject = (sid: string) => {
  if (subjectFiles.has(sid)) return;
  const f = D('curriculum', `${sid}.json`);
  subjectFiles.set(sid, fs.existsSync(f));
  if (!fs.existsSync(f)) return;
  const j = JSON.parse(fs.readFileSync(f, 'utf8'));
  for (const c of j.items) chapters.add(c.id);
  for (const s of j.subtopics) subtopics.add(s.id);
};
const questionIds = new Set<string>();
const loadQuestions = (sid: string) => {
  const dir = D('questions', sid);
  if (fs.existsSync(dir)) for (const f of fs.readdirSync(dir)) if (f.endsWith('.json') && !f.startsWith('_')) for (const q of items(path.join(dir, f))) questionIds.add(q.id);
  for (const q of items(D('fixtures', 'questions', `${sid}.json`))) questionIds.add(q.id);
};
const tutors = new Set(items(D('catalogues', 'tutors.json')).map((t) => t.id));
const careers = new Set(items(D('catalogues', 'careers.json')).map((t) => t.id));
const unis = items(D('catalogues', 'universities.json'));
const uniIds = new Set(unis.map((u) => u.id));
const progIds = new Set(unis.flatMap((u) => (u.programmes ?? []).map((p: { id: string }) => p.id)));
const params = new Map(items(D('profile', 'parameters.json')).map((p) => [p.id, p.tier]));

// ------------------------------------------------------------------ people
const adults = ['parents', 'teachers', 'counsellors', 'mentors'].flatMap((f) => items(D('personas', 'adults', `${f}.json`)));
const adultIds = new Set(adults.map((a) => a.id));
const studentDirs = fs.readdirSync(D('personas', 'students')).filter((d) => d.startsWith('lrn_'));
const studentIds = new Set(studentDirs);
const sectionFiles = fs.readdirSync(D('personas', 'classes')).filter((f) => f.endsWith('.json'));
const sections = sectionFiles.flatMap((f) => items(D('personas', 'classes', f)));
const sectionIds = new Set(sections.map((s) => s.id));
const personIds = new Set([...adultIds, ...studentIds, ...tutors]);
const index = items(D('personas', 'index.json'));

if (studentDirs.length !== 14) fail(`expected 14 student folders, found ${studentDirs.length}`);
for (const id of Object.keys(STORIES)) if (!studentIds.has(id)) fail(`${id}: no persona folder`);

const L = (id: string, f: string) => items(D('personas', 'students', id, `${f}.json`));
let checked = 0;
const t3Values: { learnerId: string; paramId: string; text: string }[] = [];
const t3Meetings: { learnerId: string; id: string; summary: string }[] = [];

for (const id of studentDirs) {
  for (const f of FILES) if (!fs.existsSync(D('personas', 'students', id, `${f}.json`))) fail(`${id}: missing ${f}.json`);
  for (const f of fs.readdirSync(D('personas', 'students', id))) if (![...FILES, ...OPTIONAL].includes(f.replace(/\.json$/, ''))) fail(`${id}: unexpected file ${f}`);
  const [student] = L(id, 'student');
  if (!student || student.id !== id) { fail(`${id}: student.json missing or wrong id`); continue; }
  for (const x of student.subjects) { if (!subjects.has(x.subjectId)) fail(`${id}: unknown subject ${x.subjectId}`); loadSubject(x.subjectId); loadQuestions(x.subjectId); }
  for (const p of student.parentIds) if (!adultIds.has(p)) fail(`${id}: parent ${p} missing`);
  for (const p of [...student.counsellorIds, ...student.mentorIds]) if (!adultIds.has(p)) fail(`${id}: ${p} missing`);
  for (const t of student.tutorIds) if (!tutors.has(t)) fail(`${id}: tutor ${t} not in catalogue`);
  for (const s of student.sectionIds) if (!sectionIds.has(s)) fail(`${id}: section ${s} missing`);
  for (const ch of student.currentChapterIds ?? []) if (!chapters.has(ch)) fail(`${id}: current chapter ${ch} unknown`);

  const data = { student, attempts: L(id, 'attempts'), gaps: L(id, 'gaps'), mastery: L(id, 'mastery'), alr: L(id, 'alr'), plans: L(id, 'plans') } as never;
  if (STORIES[id]) { for (const f of failures(id, data)) fail(`${id}: story: ${f}`); checked++; }

  // ids resolve
  for (const a of L(id, 'attempts')) for (const q of a.questionIds) if (!questionIds.has(q) && !q.startsWith('onb-')) { fail(`${id}: ${a.id} question ${q} does not resolve`); break; }
  for (const g of L(id, 'gaps')) { if (!subtopics.has(g.subtopicId)) fail(`${id}: gap subtopic ${g.subtopicId}`); if (g.validation && !adultIds.has(g.validation.byId)) fail(`${id}: validator ${g.validation.byId}`); }
  for (const m of L(id, 'mastery')) if (!subtopics.has(m.subtopicId)) fail(`${id}: mastery subtopic ${m.subtopicId}`);
  for (const r of L(id, 'alr')) if (!chapters.has(r.chapterId)) fail(`${id}: ALR chapter ${r.chapterId}`);
  const meetings = L(id, 'meetings');
  const meetingIds = new Set(meetings.map((m) => m.id));
  const tasks = L(id, 'tasks');
  const taskIds = new Set(tasks.map((t) => t.id));
  for (const t of tasks) for (const q of t.questionIds ?? []) if (!questionIds.has(q)) fail(`${id}: task ${t.id} question ${q}`);
  const bookings = L(id, 'bookings');
  const bookingIds = new Set(bookings.map((b) => b.id));
  for (const b of bookings) { if (!tutors.has(b.tutorId)) fail(`${id}: booking tutor ${b.tutorId}`); for (const p of b.sharedParamIds ?? []) if (params.get(p) === 'T3') fail(`${id}: booking ${b.id} shares T3 parameter ${p}`); }
  for (const s of L(id, 'sessions')) {
    if (!personIds.has(s.hostId)) fail(`${id}: session host ${s.hostId}`);
    for (const l of s.learnerIds) if (!studentIds.has(l) && !l.startsWith('lrn_')) fail(`${id}: session learner ${l}`);
    if (s.meetingNoteId && !meetingIds.has(s.meetingNoteId)) fail(`${id}: session ${s.id} note ${s.meetingNoteId}`);
    if (s.bookingId && s.learnerId === id && !bookingIds.has(s.bookingId)) fail(`${id}: session ${s.id} booking ${s.bookingId}`);
    for (const h of s.report?.homeworkTaskIds ?? []) if (s.learnerIds.length === 1 && !taskIds.has(h)) fail(`${id}: session ${s.id} homework ${h}`);
  }
  for (const m of meetings) {
    if (!adultIds.has(m.staffId)) fail(`${id}: meeting staff ${m.staffId}`);
    if (m.tier === 'T3') { t3Meetings.push({ learnerId: id, id: m.id, summary: m.summary }); if (!m.staffId.startsWith('csl_')) fail(`${id}: T3 note ${m.id} held by ${m.staffId}`); }
  }
  for (const a of L(id, 'applications')) { if (!uniIds.has(a.universityId)) fail(`${id}: university ${a.universityId}`); if (!progIds.has(a.programmeId)) fail(`${id}: programme ${a.programmeId}`); }
  for (const sl of L(id, 'shortlist')) { if (!uniIds.has(sl.universityId)) fail(`${id}: shortlist ${sl.universityId}`); if (sl.programmeId && !progIds.has(sl.programmeId)) fail(`${id}: shortlist programme ${sl.programmeId}`); }
  for (const c of L(id, 'careers')) for (const x of [...c.shortlist, ...c.fits.map((f: { careerId: string }) => f.careerId)]) if (!careers.has(x)) fail(`${id}: career ${x}`);
  for (const inv of L(id, 'invoices')) if (!adultIds.has(inv.payerId)) fail(`${id}: invoice payer ${inv.payerId}`);
  for (const p of L(id, 'profile')) if (p.tier === 'T3') { const text = String(Array.isArray(p.value) ? p.value.join(', ') : p.value); if (text.length >= 3) t3Values.push({ learnerId: id, paramId: p.paramId, text }); }
}

// ------------------------------------------------------------------ Zoya, siblings, picker
{
  const z = 'lrn_zoya_fernandes';
  if (L(z, 'attempts').length || L(z, 'gaps').length || L(z, 'timetable').length) fail('zoya: should have no history');
  if (L(z, 'consents').length !== 1) fail('zoya: exactly one parent consent expected');
  if (L(z, 'student')[0]?.onboardedUtc) fail('zoya: onboarding should not be done');
  const k = adults.filter((a) => a.role === 'parent' && a.learnerIds.includes('lrn_aarav_kapoor') && a.learnerIds.includes('lrn_ananya_kapoor'));
  if (k.length !== 1) fail('Kapoor siblings should share one parent account');
  if (adults.filter((a) => a.role === 'parent').length !== 13) fail(`expected 13 parent accounts, found ${adults.filter((a) => a.role === 'parent').length}`);
  for (const t of ['tch_suresh_pillai', 'tch_anjali_bose', 'tch_grace_dsouza', 'tch_tom_hayes']) if (!adultIds.has(t)) fail(`teacher ${t} missing`);
  for (const p of index) {
    if (!['sales'].includes(p.role) && !personIds.has(p.id)) fail(`index: ${p.id} does not resolve`);
    for (const l of p.linkedLearnerIds ?? []) if (!studentIds.has(l) && !l.startsWith('lrn_')) fail(`index: ${p.id} links ${l}`);
  }
  for (const id of studentIds) if (!index.some((p) => p.id === id)) fail(`index: ${id} missing`);
  for (const a of adults) for (const l of a.learnerIds) if (!studentIds.has(l)) fail(`${a.id}: learner ${l} missing`);
  for (const s of sections) {
    if (!adultIds.has(s.teacherId)) fail(`${s.id}: teacher ${s.teacherId}`);
    if (s.background.length < 25) fail(`${s.id}: only ${s.background.length} background students`);
    for (const b of s.background) { if (studentIds.has(b.id)) fail(`${s.id}: background id ${b.id} is a persona`); for (const st of Object.keys(b.mastery)) if (!subtopics.has(st)) { loadSubject(s.subjectId); if (!subtopics.has(st)) fail(`${s.id}: ${st}`); } }
  }
}

// ------------------------------------------------------------------ privacy: no T3 in anything a parent, teacher, tutor or mentor reads
{
  const facing: { where: string; text: string }[] = [];
  for (const f of ['parents', 'teachers', 'mentors'].map((x) => D('personas', 'adults', `${x}.json`))) facing.push({ where: path.relative(ROOT, f), text: fs.readFileSync(f, 'utf8') });
  for (const f of sectionFiles) facing.push({ where: `classes/${f}`, text: fs.readFileSync(D('personas', 'classes', f), 'utf8') });
  for (const id of studentDirs) {
    const parentIds = new Set(L(id, 'student')[0]?.parentIds ?? []);
    for (const m of L(id, 'messages')) if (m.toIds.some((t: string) => parentIds.has(t) || t.startsWith('tut_') || t.startsWith('mnt_') || t.startsWith('tch_')) || m.from.startsWith('tut_') || m.from.startsWith('mnt_')) facing.push({ where: `${id} message ${m.id}`, text: m.text });
    for (const b of L(id, 'bookings')) facing.push({ where: `${id} booking ${b.id}`, text: JSON.stringify(b) });
    for (const s of L(id, 'sessions')) if (s.hostRole === 'tutor' || s.hostRole === 'mentor') facing.push({ where: `${id} session ${s.id}`, text: JSON.stringify(s) });
    for (const n of L(id, 'tutorNotes')) facing.push({ where: `${id} tutor note ${n.id}`, text: n.text });
    for (const m of L(id, 'meetings')) if (m.staffId.startsWith('mnt_')) facing.push({ where: `${id} mentor note ${m.id}`, text: JSON.stringify(m) });
    for (const t of L(id, 'tasks')) if (t.source === 'tutor' || t.source === 'mentor' || t.source === 'teacher') facing.push({ where: `${id} task ${t.id}`, text: JSON.stringify(t) });
    for (const i of L(id, 'invoices')) facing.push({ where: `${id} invoice ${i.id}`, text: JSON.stringify(i) });
  }
  for (const f of facing) {
    for (const v of t3Values) if (f.text.includes(v.text)) fail(`privacy: T3 value ${v.learnerId}.${v.paramId} ("${v.text}") appears in ${f.where}`);
    for (const m of t3Meetings) { const probe = m.summary.slice(0, 40); if (f.text.includes(probe) || f.text.includes(m.id)) fail(`privacy: T3 note ${m.id} appears in ${f.where}`); }
  }
}

if (errors.length) {
  console.error(`check-stories: ${errors.length} problem(s)\n` + errors.map((e) => `  - ${e}`).join('\n'));
  process.exit(1);
}
console.log(`check-stories: ${checked} student stories hold, Zoya is new, IDs resolve across ${studentDirs.length} students, ${adults.length} adults and ${sections.length} classes; no T3 value in parent, teacher, tutor or mentor-facing data.`);
