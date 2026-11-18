/**
 * W3-P personas: regenerates data/personas/** from traits, deterministically (seed "learnibility-2026").
 *
 *   npx tsx scripts/personas/simulate.ts            write data/personas/** (+ fixture items for unvalidated banks)
 *   npx tsx scripts/personas/simulate.ts --search [lrn_id ...]   report, per student, the first seed variant whose story holds
 *
 * Every number (attempts, gaps, mastery, ALR, plans, timetables, careers) comes from the real engines via
 * scripts/personas/lib.ts. Hand-written demo content (meetings, messages, tutor tracks, applications) is in
 * scripts/personas/content.ts and scripts/personas/content/*.json, dated and keyed to the simulated history.
 * Questions: the real bank where data/questions/{subjectId}/_status.json says validated; otherwise the W2-0
 * fixture items, written to data/fixtures/questions/{subjectId}.json so their IDs resolve (docs/personas.md).
 */
import fs from 'node:fs';
import path from 'node:path';
import { careerGap, mapCareers } from '@/lib/engines';
import type { Career, EvidenceEvent, PersonaSummary, ProfileParameter, ProfileValue } from '@/lib/types';
import { getSubject } from '@/lib/data/catalogue';
import { addDaysLocal } from '@/lib/data/derive';
import type { Adult, BackgroundStudent, CareerMatches, Consent, DocumentRecord, Section, Student } from '@/lib/data/types';
import { CAST, ZOYA, type Cast } from './cast';
import { bankFor, clamp, istUtc, loadedBanks, NOW, rng, ROOT, round1, simulate, TODAY, type SimOutput } from './lib';
import { failures } from './stories';
import { contentFor, ADULTS, CONTRIB_MOVED, type Extra } from './content';

const OUT = path.join(ROOT, 'data', 'personas');
const GEN = 'scripts/personas/simulate.ts';

function write(rel: string, items: unknown[], extra: Record<string, unknown> = {}) {
  const f = path.join(OUT, rel);
  fs.mkdirSync(path.dirname(f), { recursive: true });
  fs.writeFileSync(f, JSON.stringify({ schemaVersion: 1, generatedBy: GEN, ...extra, items }, null, 1) + '\n');
}
const STUDENT_FILES = ['alr', 'attempts', 'bookings', 'careers', 'consents', 'documents', 'events', 'gaps', 'invoices', 'mastery', 'meetings', 'messages', 'plans', 'profile', 'requests', 'sessions', 'shortlist', 'student', 'tasks', 'timetable'] as const;
const OPTIONAL_FILES = ['applications', 'finance', 'assignments', 'tutorNotes', 'approvals', 'comments'] as const;

const simInput = (c: Cast) => ({
  student: c.student, start: c.start, subjects: c.subjects, traits: c.traits, seed: c.seed,
  profile: Object.entries(c.profile).map(([paramId, value]) => ({ paramId, value, asOfUtc: c.student.joinedUtc })),
});

// ------------------------------------------------------------------ profile values (~200 per student)

let PARAMS: ProfileParameter[] = [];
function profileFor(c: Cast, o: SimOutput): ProfileValue[] {
  const s = c.student;
  const r = rng(`profile-${s.id}`);
  const pick = <T>(xs: T[]) => xs[Math.floor(r() * xs.length)];
  const pct = (xs: { score: number; maxScore: number }[]) => (xs.length ? Math.round((xs.reduce((a, x) => a + x.score / Math.max(1, x.maxScore), 0) / xs.length) * 100) : 0);
  const recent = o.attempts.filter((a) => a.submittedUtc >= istUtc(addDaysLocal(TODAY, -42), '00:00'));
  const covered = c.subjects.reduce((a, x) => a + x.chapters, 0) / Math.max(1, c.subjects.reduce((a, x) => a + (getSubject(x.subjectId)?.chapters.length ?? 12), 0));
  const tasksDone = o.tasks.filter((t) => t.dueDate < TODAY);
  const evidence: Record<string, unknown> = {
    p8: pct(recent.length ? recent : o.attempts), p20: Math.round(covered * 100), p60: tasksDone.length ? Math.round((tasksDone.filter((t) => t.status === 'done').length / tasksDone.length) * 100) : 0,
  };
  const fixed: Record<string, unknown> = {
    p1: `Grade ${s.grade}`, p2: `${s.school}, ${s.city}`, p3: s.board.toUpperCase(), p5: s.stream === 'none' ? s.subjects.map((x) => x.subjectId).join(', ') : `${s.stream} stream`,
    ...c.profile,
  };
  const generic = (p: ProfileParameter): unknown => {
    const t = p.dataType.toLowerCase();
    if (t.includes('scale 1-5')) return 1 + Math.floor(r() * 5);
    if (t.includes('%') || t.includes('0-100')) return 40 + Math.floor(r() * 55);
    if (t.includes('number') || t.includes('minutes') || t.includes('hours')) return round1(1 + r() * 4);
    if (t.includes('bool') || t.includes('y/n')) return r() < 0.6;
    if (t.includes('band')) return pick(['Low', 'Medium', 'High']);
    return pick(['Low', 'Moderate', 'High']);
  };
  // onboarding seeds ~110 low-confidence values (M1/M2/M9); evidence and later forms fill the rest
  const pool = PARAMS.filter((p) => p.tier !== 'C' && p.tier !== 'T3');
  const onboarding = pool.filter((p) => p.number % 3 === 0 || ['Academic Profile', 'Learning Behaviour'].includes(p.section)).slice(0, 110);
  const later = pool.filter((p) => !onboarding.includes(p) && p.number % 2 === 0).slice(0, 60 + Math.round(s.profileCompletionPct / 2));
  const out: ProfileValue[] = [];
  const seen = new Set<string>();
  const push = (id: string, value: unknown, source: ProfileValue['source'], asOfUtc: string, confidence: ProfileValue['confidence']) => {
    const p = PARAMS.find((x) => x.id === id);
    if (!p || seen.has(id)) return;
    seen.add(id);
    out.push({ learnerId: s.id, paramId: id, value, source, asOfUtc, confidence, tier: p.tier });
  };
  for (const [id, v] of Object.entries(evidence)) push(id, v, 'M14', NOW, 'high');
  for (const [id, v] of Object.entries(fixed)) push(id, v, 'M2', s.joinedUtc, 'medium');
  for (const [id, v] of Object.entries(c.t3 ?? {})) push(id, v, 'M11', istUtc(addDaysLocal(TODAY, -14), '15:00'), 'medium');
  for (const p of onboarding) push(p.id, generic(p), (p.phase1Default ?? p.methods[0] ?? 'M1') as ProfileValue['source'], s.joinedUtc, 'low');
  const mid = new Date((Date.parse(s.joinedUtc) + Date.parse(NOW)) / 2).toISOString();
  for (const p of later) push(p.id, generic(p), (p.methods.includes('M16') ? 'M16' : p.methods[0] ?? 'M2') as ProfileValue['source'], mid, 'medium');
  return out;
}

// ------------------------------------------------------------------ classes: persona + ~29 background students

const FIRST = ['Aditi', 'Arnav', 'Diya', 'Ishaan', 'Kavya', 'Manav', 'Naina', 'Pranav', 'Riya', 'Siddharth', 'Tanvi', 'Vivaan', 'Yash', 'Zara', 'Aryan', 'Meher', 'Kunal', 'Sneha', 'Rhea', 'Advait', 'Anika', 'Dhruv', 'Ira', 'Kabir', 'Mira', 'Neel', 'Saanvi', 'Reyansh', 'Avni', 'Shaurya', 'Tara', 'Vihan', 'Nysa', 'Aahan', 'Pari'];
const LAST = ['Verma', 'Gupta', 'Malhotra', 'Chawla', 'Nair', 'Bhatia', 'Joshi', 'Iyer', 'Sethi', 'Rao', 'Mehra', 'Kapur', 'Agarwal', 'Sheikh', 'Saxena', 'Gill', 'Bajaj', 'Pillai', 'Menon', 'Bose', 'Dutta', 'Kulkarni', 'Mishra', 'Banerjee', 'Shetty', 'Chopra', 'Dsouza', 'Thomas', 'Ahmed', 'Grewal'];

function backgroundStudents(sectionId: string, subjectId: string, chapters: number, count: number, cluster?: { subtopicId: string; size: number }): BackgroundStudent[] {
  const R = rng(`bg-${sectionId}`);
  const subj = getSubject(subjectId)!;
  const coveredChs = subj.chapters.slice(0, chapters);
  const covered = new Set(coveredChs.map((c) => c.id));
  const subs = subj.subtopics.filter((s) => covered.has(s.chapterId));
  const used = new Set<string>();
  return Array.from({ length: count }, (_, i) => {
    let name = '';
    do name = `${FIRST[Math.floor(R() * FIRST.length)]} ${LAST[Math.floor(R() * LAST.length)]}`; while (used.has(name));
    used.add(name);
    const id = `lrn_bg_${name.toLowerCase().replace(/[^a-z ]/g, '').replace(' ', '_')}_${sectionId.replace(/^sec-/, '').replace(/-/g, '_')}`;
    const ability = 0.62 + R() * 0.36;
    const mastery: BackgroundStudent['mastery'] = {};
    const gaps: BackgroundStudent['gaps'] = [];
    for (const s of subs) {
      let lvl = clamp(Math.round(ability * 5 + (R() - 0.5) * 1.8), 0, 5);
      if (cluster && s.id === cluster.subtopicId && i < cluster.size) lvl = 2;
      const level = lvl as 0 | 1 | 2 | 3 | 4 | 5;
      mastery[s.id] = { level, pMastery: Math.round(clamp(level / 5 + (R() - 0.5) * 0.1, 0, 1) * 100) / 100, lastTestedUtc: istUtc(addDaysLocal(TODAY, -Math.floor(R() * 40) - 1), '17:30') };
      const code = ({ 0: 'G1', 1: 'G2', 2: 'G3', 3: 'G5' } as Record<number, 'G1' | 'G2' | 'G3' | 'G5'>)[level];
      // level 3 is only flagged when the transfer item was actually attempted and missed (about a third of the time)
      if (code && (level < 3 || R() < 0.35)) gaps.push({ subtopicId: s.id, code, level, hoursToClose: round1((5 - level) * 0.9), status: 'suspected' });
    }
    const testScores = coveredChs.map((c, k) => ({ title: `Chapter check: ${c.name}`, date: addDaysLocal(TODAY, -7 * (coveredChs.length - k) - 1), pct: Math.round(clamp(ability * 100 + (R() - 0.5) * 20, 20, 99)) }));
    return { id, name, mastery, gaps, testScores };
  });
}

// ------------------------------------------------------------------ main

function main() {
  const search = process.argv.includes('--search');
  PARAMS = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'profile', 'parameters.json'), 'utf8')).items;
  const careers: Career[] = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'catalogues', 'careers.json'), 'utf8')).items;

  if (search) {
    const only = process.argv.slice(2).filter((a) => a.startsWith('lrn_'));
    for (const c of CAST.filter((x) => !only.length || only.includes(x.student.id))) {
      for (let i = 0; i <= 60; i++) {
        const seed = i ? `v${i}` : undefined;
        const o = simulate({ ...simInput(c), seed });
        const f = failures(c.student.id, { student: { ...c.student, band: o.band }, ...o });
        if (!f.length || i === 60) { console.log(c.student.id.padEnd(20), f.length ? `no seed found: ${f.join(' | ')}` : `seed ${seed ?? '(default)'}`); break; }
      }
    }
    return;
  }

  fs.rmSync(path.join(OUT, 'students'), { recursive: true, force: true });
  fs.rmSync(path.join(OUT, 'adults'), { recursive: true, force: true });
  fs.rmSync(path.join(OUT, 'classes'), { recursive: true, force: true });

  const built = new Map<string, { c: Cast; o: SimOutput; student: Student }>();
  const storyFail: string[] = [];
  for (const c of CAST) {
    const o = simulate(simInput(c));
    const student: Student = { ...c.student, band: o.band, onboardedUtc: c.student.joinedUtc };
    built.set(c.student.id, { c, o, student });
    const f = failures(c.student.id, { student, ...o });
    if (f.length) storyFail.push(`${c.student.id}: ${f.join(' | ')}`);
  }

  for (const { c, o, student } of built.values()) {
    const id = student.id;
    const profile = profileFor(c, o);
    const ex: Extra = contentFor(c, o, built);
    const files: Record<string, unknown[]> = {};
    files.student = [{ ...student, tutorIds: [...new Set([...student.tutorIds, ...ex.bookings.filter((b) => b.status === 'active').map((b) => b.tutorId)])] }];
    files.profile = profile;
    const seedEvents: EvidenceEvent[] = [
      { eventId: `evt_${id}_signup`, learnerId: id, timestampUtc: student.joinedUtc, sourceMethod: 'M1', type: 'account_created', payload: { parameterIds: ['p1', 'p2', 'p3'] } },
      { eventId: `evt_${id}_onboarding_form`, learnerId: id, timestampUtc: student.joinedUtc, sourceMethod: 'M2', type: 'onboarding_form', payload: { parameterIds: profile.filter((p) => p.source !== 'M14' && p.asOfUtc === student.joinedUtc).map((p) => p.paramId) } },
    ];
    files.events = [...seedEvents, ...o.events, ...ex.events].sort((a, z) => a.timestampUtc.localeCompare(z.timestampUtc) || a.eventId.localeCompare(z.eventId));
    files.attempts = o.attempts;
    files.mastery = o.mastery;
    files.alr = o.alr;
    files.gaps = o.gaps.map((g) => ex.validations[g.subtopicId] ? { ...g, validation: ex.validations[g.subtopicId] } : g);
    files.plans = o.plans;
    files.timetable = o.timetable;
    files.tasks = [...o.tasks, ...ex.tasks];

    // careers from the non-sensitive profile
    const prof = profile.filter((p) => p.tier !== 'T3' && p.tier !== 'C');
    const fits = mapCareers(prof, careers, { grade: student.grade, stream: student.stream, limit: 8 });
    const cm: CareerMatches = {
      learnerId: id, computedUtc: NOW, fits, shortlist: ex.careerShortlist,
      gaps: Object.fromEntries(ex.careerShortlist.map((cid) => [cid, careerGap(prof, careers.find((x) => x.id === cid)!, { grade: student.grade, stream: student.stream })])),
    };
    files.careers = [cm];
    files.sessions = ex.sessions;
    files.meetings = ex.meetings;
    files.requests = ex.requests;
    files.documents = [
      { id: `doc_${id.slice(4)}_rc`, learnerId: id, folder: 'academics', title: student.board === 'cbse' ? 'Term 1 report card' : 'Mid-year report', fileName: 'report-card-term1.pdf', kind: 'report_card', uploadedUtc: istUtc(student.board === 'cbse' ? '2026-10-03' : '2026-10-24', '18:00'), source: 'M5', sizeKb: 412 },
      ...o.attempts.filter((a) => a.kind === 'chapter_check' || a.kind === 'mock').map((a) => ({ id: `doc_${a.id}`, learnerId: id, folder: 'academics' as const, title: `${a.title} result`, fileName: `${a.id}.pdf`, kind: 'test_result' as const, uploadedUtc: a.submittedUtc, source: 'auto' as const, sizeKb: 96, refId: a.id })),
      ...ex.documents,
    ] satisfies DocumentRecord[];
    files.consents = consentsFor(id, c.parent.id, student.joinedUtc, ex.extraConsents);
    files.invoices = ex.invoices;
    files.bookings = ex.bookings;
    files.messages = ex.messages;
    files.shortlist = ex.shortlist;
    for (const name of STUDENT_FILES) write(`students/${id}/${name}.json`, files[name] ?? []);
    const opt: Record<string, unknown[]> = { applications: ex.applications, finance: ex.finance, assignments: ex.assignments, tutorNotes: ex.tutorNotes, approvals: ex.approvals, comments: [] };
    for (const name of OPTIONAL_FILES) if (opt[name]?.length) write(`students/${id}/${name}.json`, opt[name]);
  }

  // Zoya: account, parent and consent only
  {
    const z = ZOYA.student;
    const files: Record<string, unknown[]> = {
      student: [z],
      consents: [{ id: 'cns_zoya_fernandes_1', learnerId: z.id, grantedById: ZOYA.parent.id, scope: 'edu_personalisation', version: 'v1.2', grantedUtc: '2026-11-18T03:12:00.000Z' } satisfies Consent],
      events: [{ eventId: `evt_${z.id}_signup`, learnerId: z.id, timestampUtc: z.joinedUtc, sourceMethod: 'M1', type: 'account_created', payload: { parameterIds: ['p1', 'p2', 'p3'] } }],
    };
    for (const name of STUDENT_FILES) write(`students/${z.id}/${name}.json`, files[name] ?? []);
  }

  // adults
  const students = [...built.values()].map((b) => b.student);
  const parents: Adult[] = [];
  for (const c of [...CAST, ZOYA]) {
    if (parents.some((p) => p.id === c.parent.id)) continue;
    const kids = [...CAST, ZOYA].filter((x) => x.parent.id === c.parent.id).map((x) => x.student.id);
    const [firstName, ...rest] = c.parent.name.split(' ');
    parents.push({ id: c.parent.id, role: 'parent', firstName, lastName: rest.join(' '), name: c.parent.name, city: c.student.city, learnerIds: kids, relation: Object.fromEntries(kids.map((k) => [k, c.parent.relation])), email: `${firstName.toLowerCase()}.${rest.join('').toLowerCase()}@example.in` });
  }
  write('adults/parents.json', parents);
  write('adults/teachers.json', ADULTS.teachers);
  write('adults/counsellors.json', ADULTS.counsellors(students.map((s) => s.id).concat(ZOYA.student.id)));
  write('adults/mentors.json', ADULTS.mentors);

  // classes
  for (const sec of ADULTS.sections) {
    const persona = built.get(sec.personaId)!;
    const chapters = persona.c.subjects.find((x) => x.subjectId === sec.subjectId)?.chapters ?? 3;
    const bg = backgroundStudents(sec.id, sec.subjectId, chapters, 29, sec.cluster);
    write(`classes/${sec.id}.json`, [{ id: sec.id, name: sec.name, teacherId: sec.teacherId, subjectId: sec.subjectId, board: sec.board, grade: sec.grade, school: sec.school, learnerIds: [sec.personaId, ...bg.map((x) => x.id)], background: bg } satisfies Section]);
  }

  // persona picker: keep entries this script does not own (e.g. W3-CRM sales personas)
  const idxFile = path.join(OUT, 'index.json');
  const prev: PersonaSummary[] = fs.existsSync(idxFile) ? JSON.parse(fs.readFileSync(idxFile, 'utf8')).items : [];
  const initials = (n: string) => n.split(' ').map((w) => w[0]).join('').slice(0, 2).toUpperCase();
  const mine: (PersonaSummary & { initials: string })[] = [
    ...[...CAST, ZOYA].map((c) => ({ id: c.student.id, role: 'student' as const, name: c.student.name, story: c.persona.story, grade: c.student.grade, board: c.student.board, stream: c.student.stream, programme: c.persona.programme, order: c.persona.order })),
    ...parents.map((p, i) => ({ id: p.id, role: 'parent' as const, name: p.name, story: `Parent of ${p.learnerIds.map((l) => [...CAST, ZOYA].find((c) => c.student.id === l)!.student.firstName).join(' and ')}.${p.learnerIds.length > 1 ? ' One account, two children.' : ''}`, linkedLearnerIds: p.learnerIds, order: i + 1 })),
    ...ADULTS.pickerEntries(students),
  ].map((p) => ({ ...p, initials: initials(p.name) }));
  const mineIds = new Set(mine.map((p) => p.id));
  const keep = prev.filter((p) => !mineIds.has(p.id) && !['student', 'parent', 'teacher', 'counsellor', 'mentor', 'tutor'].includes(p.role));
  fs.writeFileSync(idxFile, JSON.stringify({ schemaVersion: 1, generatedBy: GEN, items: [...mine, ...keep] }, null, 1) + '\n');

  // fixture items for subjects whose bank is not validated yet
  for (const b of loadedBanks()) if (b.source === 'fixture') {
    const f = path.join(ROOT, 'data', 'fixtures', 'questions', `${b.subjectId}.json`);
    fs.writeFileSync(f, JSON.stringify({ schemaVersion: 1, generatedBy: `${GEN} (fixture items until the real bank is validated)`, items: b.questions }, null, 1) + '\n');
  }
  write('_sources.json', loadedBanks().map((b) => ({ subjectId: b.subjectId, source: b.source })).sort((a, z) => a.subjectId.localeCompare(z.subjectId)));

  // moved contrib entries (now in persona files)
  for (const [file, ids] of Object.entries(CONTRIB_MOVED)) {
    const f = path.join(ROOT, 'data', 'fixtures', 'contrib', file);
    if (!fs.existsSync(f)) continue;
    const d = JSON.parse(fs.readFileSync(f, 'utf8'));
    let changed = false;
    for (const [k, v] of Object.entries(d.collections as Record<string, { learnerId?: string }[]>)) {
      const kept = v.filter((r) => !(r.learnerId && ids.includes(r.learnerId)));
      if (kept.length !== v.length) { d.collections[k] = kept; changed = true; }
    }
    if (changed) fs.writeFileSync(f, JSON.stringify(d, null, 2) + '\n');
  }

  for (const { c, o, student } of built.values()) {
    const open = o.gaps.filter((g) => g.status !== 'closed');
    const plan = o.plans[o.plans.length - 1];
    console.log(`${student.id.padEnd(20)} attempts ${String(o.attempts.length).padStart(3)}  open gaps ${String(open.length).padStart(2)} [${[...new Set(open.map((g) => g.code))].join(',')}]  band ${student.band}  paid ${plan?.plan.paidTuition.recommended ?? '-'}  questions ${c.subjects.map((s) => `${s.subjectId}:${bankFor(s.subjectId).source}`).join(' ')}`);
  }
  if (storyFail.length) {
    console.error(`\nSTORY DRIFT (run with --search and update the seed in cast.ts):\n${storyFail.join('\n')}`);
    process.exitCode = 1;
  }
}

function consentsFor(id: string, parentId: string, joined: string, extra: Consent['scope'][]): Consent[] {
  const k = id.slice(4);
  const out: Consent[] = [
    { id: `cns_${k}_1`, learnerId: id, grantedById: parentId, scope: 'edu_personalisation', version: 'v1.2', grantedUtc: joined },
    { id: `cns_${k}_2`, learnerId: id, grantedById: parentId, scope: 'share_with_school', version: 'v1.2', grantedUtc: joined },
    { id: `cns_${k}_3`, learnerId: id, grantedById: parentId, scope: 'wellbeing_screening', version: 'v1.0', grantedUtc: joined },
    { id: `cns_${k}_4`, learnerId: id, grantedById: parentId, scope: 'marketing', version: 'v1.0', grantedUtc: joined, revokedUtc: new Date(Date.parse(joined) + 30 * 86_400_000).toISOString() },
  ];
  extra.forEach((scope, i) => out.push({ id: `cns_${k}_${5 + i}`, learnerId: id, grantedById: parentId, scope, version: 'v1.0', grantedUtc: new Date(Date.parse(joined) + 7 * 86_400_000).toISOString() }));
  return out;
}

main();
