/**
 * W3-P: hand-written demo content around the simulated history: counsellor, mentor and application meetings,
 * tutor tracks (bookings, sessions with reports, homework, notes, invoices), messages, requests, tasks and
 * applications. Dates and gap references are taken from each student's simulation, so what a tutor or
 * counsellor talks about is what the engines found. Nothing sensitive (T3) is written to anything a parent,
 * teacher, tutor or mentor reads; check-stories.ts asserts it.
 */
import fs from 'node:fs';
import path from 'node:path';
import type { EvidenceEvent, GapCode } from '@/lib/types';
import { getSubject, getSubtopic } from '@/lib/data/catalogue';
import { addDaysLocal, localDateOf, weekStartOf } from '@/lib/data/derive';
import type {
  Adult, Application, Approval, Assignment, Booking, Consent, DocumentRecord, FinanceVisa, GapRecord, Invoice, MeetingNote, Message,
  Session, SessionReport, ShortlistEntry, Student, Task, TimetableRequest, TutorNote,
} from '@/lib/data/types';
import type { PersonaSummary } from '@/lib/types';
import type { Cast } from './cast';
import { istUtc, NOW, ROOT, TODAY, type SimOutput } from './lib';


export interface Extra {
  bookings: Booking[]; sessions: Session[]; meetings: MeetingNote[]; messages: Message[]; tasks: Task[]; requests: TimetableRequest[];
  invoices: Invoice[]; documents: DocumentRecord[]; shortlist: ShortlistEntry[]; applications: Application[]; finance: FinanceVisa[];
  assignments: Assignment[]; tutorNotes: TutorNote[]; approvals: Approval[]; events: EvidenceEvent[];
  validations: Record<string, NonNullable<GapRecord['validation']>>; careerShortlist: string[]; extraConsents: Consent['scope'][];
}
type Built = Map<string, { c: Cast; o: SimOutput; student: Student }>;

/** Contrib entries now owned by persona files (removed from contrib by simulate.ts). */
export const CONTRIB_MOVED: Record<string, string[]> = { 'w2a-applications.json': ['lrn_nikhil_reddy', 'lrn_ananya_kapoor'] };

const readCollections = (rel: string): Record<string, Record<string, unknown>[]> => {
  const f = path.join(ROOT, rel);
  return fs.existsSync(f) ? JSON.parse(fs.readFileSync(f, 'utf8')).collections : {};
};
const W2T = readCollections('data/fixtures/contrib/w2t-tutors.json');
const W2A = readCollections('scripts/personas/content/w2a-moved.json');
const TARA = readCollections('scripts/personas/content/tara-applications.json');
const fromCollections = <T>(src: Record<string, Record<string, unknown>[]>, name: string, id: string): T[] =>
  (src[name] ?? []).filter((r) => r.learnerId === id) as T[];

const nameOf = (sid: string) => getSubtopic(sid)?.name ?? sid;
const subjectName = (id: string) => getSubject(id)?.subject.name ?? id;
const first = (n: string) => n.split(' ')[0];
const dow = (date: string) => (new Date(date + 'T00:00:00Z').getUTCDay() + 6) % 7; // Mon 0

// ------------------------------------------------------------------ people

const TEACHERS: Adult[] = [
  { id: 'tch_suresh_pillai', role: 'teacher', firstName: 'Suresh', lastName: 'Pillai', name: 'Suresh Pillai', city: 'New Delhi', headline: 'CBSE Maths teacher, grades 9 and 10', school: 'Delhi Public School, Dwarka', learnerIds: ['lrn_kabir_singh', 'lrn_rohan_das'], sectionIds: ['sec-cbse-g9-maths-a', 'sec-cbse-g10-maths-b'], subjectIds: ['cbse-g9-maths', 'cbse-g10-maths'] },
  { id: 'tch_anjali_bose', role: 'teacher', firstName: 'Anjali', lastName: 'Bose', name: 'Anjali Bose', city: 'Gurugram', headline: 'CBSE Science teacher, grades 8 and 10', school: 'Delhi Public School, Sector 45', learnerIds: ['lrn_aarav_kapoor', 'lrn_rohan_das'], sectionIds: ['sec-cbse-g8-science-a', 'sec-cbse-g10-science-b'], subjectIds: ['cbse-g8-science', 'cbse-g10-science'] },
  { id: 'tch_grace_dsouza', role: 'teacher', firstName: 'Grace', lastName: 'D’Souza', name: 'Grace D’Souza', city: 'Bengaluru', headline: 'Cambridge English teacher, Stage 9 and IGCSE', school: 'Indus International School', learnerIds: ['lrn_ishita_rao', 'lrn_ananya_kapoor'], sectionIds: ['sec-cambridge-g8-english-a', 'sec-cambridge-g10-english-a'], subjectIds: ['cambridge-g8-english', 'cambridge-g10-english'] },
  { id: 'tch_tom_hayes', role: 'teacher', firstName: 'Tom', lastName: 'Hayes', name: 'Tom Hayes', city: 'Kochi', headline: 'IB DP Economics teacher', school: 'Choice International School', learnerIds: ['lrn_arjun_nair'], sectionIds: ['sec-ib-g11-economics-a'], subjectIds: ['ib-g11-economics'] },
];
const SECTIONS = [
  { id: 'sec-cbse-g9-maths-a', name: '9A Maths', teacherId: 'tch_suresh_pillai', subjectId: 'cbse-g9-maths', board: 'cbse' as const, grade: 9 as const, school: 'Delhi Public School, Dwarka', personaId: 'lrn_kabir_singh', cluster: { subtopicId: 'cbse-g9-maths-ch05-st3', size: 9 } },
  { id: 'sec-cbse-g10-maths-b', name: '10B Maths', teacherId: 'tch_suresh_pillai', subjectId: 'cbse-g10-maths', board: 'cbse' as const, grade: 10 as const, school: 'Delhi Public School, Dwarka', personaId: 'lrn_rohan_das', cluster: { subtopicId: 'cbse-g10-maths-ch04-st1', size: 6 } },
  { id: 'sec-cbse-g8-science-a', name: '8A Science', teacherId: 'tch_anjali_bose', subjectId: 'cbse-g8-science', board: 'cbse' as const, grade: 8 as const, school: 'Delhi Public School, Sector 45', personaId: 'lrn_aarav_kapoor', cluster: { subtopicId: 'cbse-g8-science-ch04-st2', size: 6 } },
  { id: 'sec-cbse-g10-science-b', name: '10B Science', teacherId: 'tch_anjali_bose', subjectId: 'cbse-g10-science', board: 'cbse' as const, grade: 10 as const, school: 'Kendriya Vidyalaya, Salt Lake', personaId: 'lrn_rohan_das', cluster: { subtopicId: 'cbse-g10-science-ch01-st2', size: 6 } },
  { id: 'sec-cambridge-g8-english-a', name: 'Stage 9 English A', teacherId: 'tch_grace_dsouza', subjectId: 'cambridge-g8-english', board: 'cambridge' as const, grade: 8 as const, school: 'Indus International School', personaId: 'lrn_ishita_rao', cluster: undefined },
  { id: 'sec-cambridge-g10-english-a', name: 'IGCSE English A', teacherId: 'tch_grace_dsouza', subjectId: 'cambridge-g10-english', board: 'cambridge' as const, grade: 10 as const, school: 'The Shri Ram School, Moulsari', personaId: 'lrn_ananya_kapoor', cluster: undefined },
  { id: 'sec-ib-g11-economics-a', name: 'DP1 Economics', teacherId: 'tch_tom_hayes', subjectId: 'ib-g11-economics', board: 'ib' as const, grade: 11 as const, school: 'Choice International School', personaId: 'lrn_arjun_nair', cluster: { subtopicId: 'ib-g11-economics-ch02-st2', size: 6 } },
];
const APPS_CASELOAD = ['lrn_ananya_kapoor', 'lrn_nikhil_reddy', 'lrn_tara_menon', 'lrn_arjun_nair'];
const MENTEES = ['lrn_sara_khan', 'lrn_arjun_nair', 'lrn_kunal_verma'];
/** Tutors with persona students (catalogue ids). */
const TUTOR_PICKER: { id: string; name: string; story: string; learners: string[] }[] = [
  { id: 'tut_rahul_verma', name: 'Rahul Verma', story: 'Maths and Physics tutor in Delhi. Rohan one to one, Kabir in a small group.', learners: ['lrn_rohan_das', 'lrn_kabir_singh'] },
  { id: 'tut_meenakshi_rao', name: 'Meenakshi Rao', story: 'Chemistry tutor. Vihaan twice a week, retention-first.', learners: ['lrn_vihaan_joshi'] },
  { id: 'tut_fatima_sheikh', name: 'Fatima Sheikh', story: 'Physics tutor for NEET and boards. Diya on weekends.', learners: ['lrn_diya_sharma'] },
  { id: 'tut_farhan_ali', name: 'Farhan Ali', story: 'English tutor: academic writing for students moving from Hindi medium. Kunal.', learners: ['lrn_kunal_verma'] },
  { id: 'tut_sunita_gupta', name: 'Sunita Gupta', story: 'CBSE Science tutor. Rohan has asked for her; waiting for his parent.', learners: ['lrn_rohan_das'] },
];

export const ADULTS = {
  teachers: TEACHERS,
  sections: SECTIONS,
  counsellors: (all: string[]): Adult[] => [
    { id: 'csl_heena_qureshi', role: 'counsellor', firstName: 'Heena', lastName: 'Qureshi', name: 'Heena Qureshi', headline: 'Academic and wellbeing counsellor', focus: 'academic_wellbeing', learnerIds: all },
    { id: 'csl_farah_siddiqui', role: 'counsellor', firstName: 'Farah', lastName: 'Siddiqui', name: 'Farah Siddiqui', headline: 'University applications counsellor (UK, US, Canada)', focus: 'applications', learnerIds: APPS_CASELOAD },
  ],
  mentors: [{ id: 'mnt_kelvin_thomas', role: 'mentor', firstName: 'Kelvin', lastName: 'Thomas', name: 'Kelvin Thomas', headline: 'Career mentor', focus: 'careers', learnerIds: MENTEES }] as Adult[],
  pickerEntries: (students: Student[]): PersonaSummary[] => [
    ...TEACHERS.map((t, i) => ({ id: t.id, role: 'teacher' as const, name: t.name, story: `${t.headline}. ${SECTIONS.filter((s) => s.teacherId === t.id).map((s) => s.name).join(' and ')}, about 30 students each.`, linkedLearnerIds: t.learnerIds, order: i + 1 })),
    { id: 'csl_heena_qureshi', role: 'counsellor', name: 'Heena Qureshi', story: 'Academic and wellbeing counsellor for all 14 students.', linkedLearnerIds: students.map((s) => s.id).concat('lrn_zoya_fernandes'), order: 1 },
    { id: 'csl_farah_siddiqui', role: 'counsellor', name: 'Farah Siddiqui', story: 'Applications counsellor: Ananya, Nikhil, Tara and Arjun.', linkedLearnerIds: APPS_CASELOAD, order: 2 },
    { id: 'mnt_kelvin_thomas', role: 'mentor', name: 'Kelvin Thomas', story: 'Career mentor for Sara, Arjun and Kunal.', linkedLearnerIds: MENTEES, order: 1 },
    ...TUTOR_PICKER.map((t, i) => ({ id: t.id, role: 'tutor' as const, name: t.name, story: t.story, linkedLearnerIds: t.learners, order: i + 1 })),
  ],
};

// ------------------------------------------------------------------ builders

function empty(): Extra {
  return { bookings: [], sessions: [], meetings: [], messages: [], tasks: [], requests: [], invoices: [], documents: [], shortlist: [], applications: [], finance: [], assignments: [], tutorNotes: [], approvals: [], events: [], validations: {}, careerShortlist: [], extraConsents: [] };
}

const openGaps = (o: SimOutput, subjectId?: string) => o.gaps.filter((g) => g.status !== 'closed' && (!subjectId || g.subjectId === subjectId)).sort((a, b) => b.size - a.size || a.subtopicId.localeCompare(b.subtopicId));

/** Monthly check-ins with Heena (completed, T1 notes) and the next one. */
function heenaTrack(x: Extra, s: Student, o: SimOutput, start: string) {
  const k = s.id.slice(4);
  let n = 0;
  for (let d = addDaysLocal(start, 24); d < addDaysLocal(TODAY, -3); d = addDaysLocal(d, 28)) {
    n++;
    const date = addDaysLocal(weekStartOf(d), 2); // Wednesdays
    const gapsThen = o.gaps.filter((g) => g.detectedUtc <= istUtc(date, '16:00') && (!g.closedUtc || g.closedUtc > istUtc(date, '16:00')));
    const top = gapsThen.sort((a, b) => b.size - a.size)[0];
    x.sessions.push({ id: `ses_${k}_csl_${n}`, code: `C-${n}`, learnerId: s.id, learnerIds: [s.id], hostId: 'csl_heena_qureshi', hostRole: 'counsellor', kind: 'counselling', title: n === 1 ? 'First check-in with Heena' : 'Monthly check-in with Heena', startUtc: istUtc(date, '16:00'), minutes: 30, status: 'completed', mode: 'online', meetingNoteId: `mtg_${k}_${n}` });
    x.meetings.push({
      id: `mtg_${k}_${n}`, learnerId: s.id, staffId: 'csl_heena_qureshi', date, kind: 'academic', tier: 'T1',
      summary: gapsThen.length
        ? `Reviewed ${first(s.name)}'s ${gapsThen.length} open gap${gapsThen.length > 1 ? 's' : ''}${top ? `, biggest ${top.code} on ${nameOf(top.subtopicId)}` : ''}. Agreed to keep the timetable's gap blocks and re-test on Saturday.`
        : `${first(s.name)} has no open gaps this month. Kept the study windows and added one stretch block a week.`,
      decisions: gapsThen.length ? ['Keep current study windows', 'Re-test open gaps in the weekly test'] : ['Keep current study windows', 'One stretch block a week'],
      actionItems: [{ id: `ai_${k}_${n}`, title: top ? `Finish the practice blocks for ${nameOf(top.subtopicId)}` : 'Try one stretch problem set', dueOn: addDaysLocal(date, 7), done: true }],
    });
  }
  x.sessions.push({ id: `ses_${k}_csl_next`, code: `C-${n + 1}`, learnerId: s.id, learnerIds: [s.id], hostId: 'csl_heena_qureshi', hostRole: 'counsellor', kind: 'counselling', title: 'Check-in with Heena', startUtc: istUtc(addDaysLocal(TODAY, 6), '16:30'), minutes: 30, status: 'scheduled', mode: 'online', joinUrl: 'https://meet.learnibility.demo/heena' });
}

function wellbeing(x: Extra, s: Student, date: string, summary: string, decisions: string[], parentNote: string, parentId: string) {
  const k = s.id.slice(4);
  x.meetings.push({ id: `mtg_${k}_wellbeing_1`, learnerId: s.id, staffId: 'csl_heena_qureshi', date, kind: 'wellbeing', tier: 'T3', summary, decisions, actionItems: [{ id: `ai_${k}_wb_1`, title: 'Weekly 10-minute check-in with Heena', dueOn: addDaysLocal(date, 14) }] });
  x.sessions.push({ id: `ses_${k}_csl_wb`, code: 'C-W', learnerId: s.id, learnerIds: [s.id], hostId: 'csl_heena_qureshi', hostRole: 'counsellor', kind: 'counselling', title: 'Wellbeing check-in', startUtc: istUtc(date, '15:00'), minutes: 20, status: 'completed', mode: 'online', meetingNoteId: `mtg_${k}_wellbeing_1` });
  x.events.push({ eventId: `evt_${s.id}_wellbeing_1`, learnerId: s.id, timestampUtc: istUtc(date, '15:20'), sourceMethod: 'M11', type: 'wellbeing_checkin', payload: { flag: true, parameterIds: ['p149'], tier: 'T3', by: 'csl_heena_qureshi', meetingNoteId: `mtg_${k}_wellbeing_1` } });
  // parents get a summary only, never the screened values
  x.messages.push({ id: `msg_${k}_wb_parent`, threadId: `${s.id}:${parentId}:csl_heena_qureshi`, learnerId: s.id, from: 'csl_heena_qureshi', toIds: [parentId], text: parentNote, sentUtc: istUtc(addDaysLocal(date, 1), '18:00'), readBy: [parentId] });
}

interface TutorSpec {
  tutorId: string; tutorName: string; subjectId: string; demo: string; start: string; days: number[]; time: string; minutes: number; rate: number;
  format?: 'one_to_one' | 'group'; parentId: string; homeworkEvery?: number;
}
/** A full tutor track: demo, regular booking, sessions with reports, homework tasks, notes, invoices, approval. */
function tutorTrack(x: Extra, s: Student, o: SimOutput, t: TutorSpec) {
  const k = s.id.slice(4);
  const tk = t.tutorId.slice(4);
  const gapsAtStart = o.gaps.filter((g) => g.subjectId === t.subjectId && g.detectedUtc <= istUtc(t.start, '00:00')).sort((a, b) => b.size - a.size).slice(0, 4);
  const snapshot = {
    sharedUtc: istUtc(addDaysLocal(t.demo, -2), '20:00'), subjectId: t.subjectId,
    score: Math.round((100 * o.attempts.filter((a) => a.subjectId === t.subjectId && a.submittedUtc < istUtc(t.demo, '00:00')).slice(-3).reduce((a, x) => a + x.score / Math.max(1, x.maxScore), 0)) / 3),
    gaps: gapsAtStart.map((g) => ({ gapId: g.id, subtopicId: g.subtopicId, name: nameOf(g.subtopicId), code: g.code, level: g.level, hoursToClose: g.hoursToClose })),
  };
  x.bookings.push({ id: `bkg_${k}_${tk}_demo`, learnerId: s.id, tutorId: t.tutorId, kind: 'demo', status: 'completed', format: 'one_to_one', mode: 'online', subjectId: t.subjectId, priceInr: 0, requestedAt: istUtc(addDaysLocal(t.demo, -2), '20:00'), slotStartUtc: istUtc(t.demo, t.time), minutes: 30, topic: snapshot.gaps.map((g) => g.name).slice(0, 2).join(' and '), respondedUtc: istUtc(addDaysLocal(t.demo, -1), '09:30'), sharedGapSnapshot: snapshot, sharedParamIds: ['p8', 'p31'] });
  x.bookings.push({ id: `bkg_${k}_${tk}`, learnerId: s.id, tutorId: t.tutorId, kind: 'regular', status: 'active', format: t.format ?? 'one_to_one', mode: 'online', subjectId: t.subjectId, priceInr: t.rate, requestedAt: istUtc(addDaysLocal(t.demo, 1), '19:00'), slotStartUtc: istUtc(t.start, t.time), minutes: t.minutes, sessionsPerWeek: t.days.length, respondedUtc: istUtc(addDaysLocal(t.demo, 2), '10:00'), sharedGapSnapshot: snapshot, sharedParamIds: ['p8', 'p31'], parentApproval: { parentId: t.parentId, status: 'approved', utc: istUtc(addDaysLocal(t.demo, 2), '08:30') }, matchReason: `Teaches ${subjectName(t.subjectId)}, free demo, ₹${t.rate.toLocaleString('en-IN')} an hour, evenings that overlap ${first(s.name)}'s study windows.` });
  x.approvals.push({ id: `apr_${k}_${tk}`, learnerId: s.id, kind: 'paid_tutor', targetId: `bkg_${k}_${tk}`, byId: t.parentId, decision: 'approved', utc: istUtc(addDaysLocal(t.demo, 2), '08:30') });
  x.sessions.push({ id: `ses_${k}_${tk}_demo`, code: 'D-1', learnerId: s.id, learnerIds: [s.id], hostId: t.tutorId, hostRole: 'tutor', kind: 'demo', title: `Demo: ${subjectName(t.subjectId)}`, subjectId: t.subjectId, startUtc: istUtc(t.demo, t.time), minutes: 30, status: 'completed', mode: 'online', bookingId: `bkg_${k}_${tk}_demo`, rateInr: 0, report: null });
  let n = 0;
  const monthly = new Map<string, number>();
  for (let d = t.start; d <= addDaysLocal(TODAY, 13); d = addDaysLocal(d, 1)) {
    if (!t.days.includes(dow(d))) continue;
    n++;
    const startUtc = istUtc(d, t.time);
    const past = startUtc < NOW;
    // the session works on the biggest gap open on that day
    const live = o.gaps.filter((g) => g.subjectId === t.subjectId && g.detectedUtc <= startUtc && (!g.closedUtc || g.closedUtc > startUtc)).sort((a, b) => b.size - a.size || a.subtopicId.localeCompare(b.subtopicId));
    const focus = live[n % Math.max(1, Math.min(2, live.length))] ?? live[0];
    const topic = focus ? nameOf(focus.subtopicId) : `${subjectName(t.subjectId)} revision`;
    const id = `ses_${k}_${tk}_${String(n).padStart(2, '0')}`;
    let report: SessionReport | null = null;
    if (past) {
      const hw = `task_${k}_${tk}_hw_${n}`;
      const perf: SessionReport['performance'] = !focus ? 'confident' : focus.level <= 1 ? 'struggled' : focus.level <= 3 ? 'getting_there' : 'confident';
      report = { topics: [topic], performance: perf, engagement: perf === 'struggled' ? 'medium' : 'high', notes: perf === 'struggled' ? `Rebuilt ${topic.toLowerCase()} from the definition; needs another pass.` : perf === 'getting_there' ? `Method is right on ${topic.toLowerCase()}; slips on the last step under time.` : `Comfortable with ${topic.toLowerCase()}; moved to mixed questions.`, homeworkTaskIds: [hw], nextFocus: live[1] ? nameOf(live[1].subtopicId) : 'Mixed revision', submittedUtc: new Date(Date.parse(startUtc) + (t.minutes + 20) * 60_000).toISOString(), gapIds: focus ? [focus.id] : [] };
      x.tasks.push({ id: hw, learnerId: s.id, title: `Homework: ${topic}`, kind: 'homework', dueDate: addDaysLocal(d, 3), status: addDaysLocal(d, 3) < TODAY ? (n % 5 === 0 ? 'skipped' : 'done') : 'todo', source: 'tutor', createdBy: t.tutorId, createdUtc: report.submittedUtc, minutes: 30, subjectId: t.subjectId, refId: id, ...(addDaysLocal(d, 3) < TODAY && n % 5 ? { completedUtc: istUtc(addDaysLocal(d, 2), '19:30') } : {}) });
      if (n % 3 === 1) x.tutorNotes.push({ id: `note_${k}_${tk}_${n}`, learnerId: s.id, tutorId: t.tutorId, text: report.notes, createdUtc: report.submittedUtc, source: 'session_report' });
      const m = d.slice(0, 7);
      monthly.set(m, (monthly.get(m) ?? 0) + 1);
    }
    x.sessions.push({ id, code: `S-${n}`, learnerId: s.id, learnerIds: [s.id], hostId: t.tutorId, hostRole: 'tutor', kind: t.format === 'group' ? 'group' : 'one_to_one', title: topic, subjectId: t.subjectId, focus: topic, startUtc, minutes: t.minutes, status: past ? 'completed' : 'scheduled', mode: 'online', joinUrl: `https://meet.learnibility.demo/${id}`, bookingId: `bkg_${k}_${tk}`, rateInr: t.rate, report, ...(past ? {} : { prepNotes: focus ? `Focus: ${topic} (${focus.code}, level ${focus.level}). Start with one C2 explanation, then two C3 problems.` : 'Mixed revision.' }) });
  }
  for (const [m, count] of monthly) {
    const issued = `${m}-28`;
    const amount = Math.round((count * t.rate * t.minutes) / 60);
    const paid = issued < addDaysLocal(TODAY, -5);
    x.invoices.push({ id: `inv_${k}_${tk}_${m.replace('-', '')}`, learnerId: s.id, payerId: t.parentId, issuedUtc: istUtc(issued, '09:00'), dueDate: addDaysLocal(issued, 7), status: paid ? 'paid' : 'due', ...(paid ? { paidUtc: istUtc(addDaysLocal(issued, 2), '20:00') } : {}), lines: [{ title: `${t.tutorName}: ${count} × ${t.minutes} min ${subjectName(t.subjectId)} (${m})`, amountInr: amount, bookingId: `bkg_${k}_${tk}` }], amountInr: amount });
  }
  x.messages.push({ id: `msg_${k}_${tk}_1`, threadId: `${s.id}:${t.tutorId}`, learnerId: s.id, from: t.tutorId, toIds: [s.id], text: `Hi ${first(s.name)}, see you ${['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][t.days[0]]} at ${t.time}. I've read the gaps you shared; we'll start with ${snapshot.gaps[0]?.name ?? 'the basics'}.`, sentUtc: istUtc(addDaysLocal(t.demo, 2), '11:00'), readBy: [s.id], tutorId: t.tutorId });
  x.messages.push({ id: `msg_${k}_${tk}_2`, threadId: `${s.id}:${t.tutorId}`, learnerId: s.id, from: s.id, toIds: [t.tutorId], text: 'Thank you! I uploaded last week’s homework.', sentUtc: istUtc(addDaysLocal(TODAY, -3), '20:40'), readBy: [t.tutorId], tutorId: t.tutorId });
  x.assignments.push({ id: `asg_${k}_${tk}_1`, learnerId: s.id, tutorId: t.tutorId, title: `${subjectName(t.subjectId)} practice set`, subtopicIds: gapsAtStart.slice(0, 2).map((g) => g.subtopicId), questionIds: [], status: 'assigned', dueOn: addDaysLocal(TODAY, 3) });
}

/** Copy W2-T's hand-built tutor content (Rahul Verma) for a persona learner. */
function w2tFor(x: Extra, id: string) {
  x.bookings.push(...fromCollections<Booking>(W2T, 'bookings', id));
  x.sessions.push(...((W2T.sessions ?? []) as unknown as Session[]).filter((r) => r.learnerId === id));
  x.assignments.push(...fromCollections<Assignment>(W2T, 'assignments', id));
  x.messages.push(...fromCollections<Message>(W2T, 'messages', id));
  x.tutorNotes.push(...fromCollections<TutorNote>(W2T, 'tutorNotes', id));
  x.tasks.push(...fromCollections<Task>(W2T, 'tasks', id));
}
function appsFrom(x: Extra, src: Record<string, Record<string, unknown>[]>, id: string) {
  x.applications.push(...fromCollections<Application>(src, 'applications', id));
  x.meetings.push(...fromCollections<MeetingNote>(src, 'meetings', id));
  x.finance.push(...fromCollections<FinanceVisa>(src, 'finance', id));
  x.shortlist.push(...fromCollections<ShortlistEntry>(src, 'shortlist', id));
  x.documents.push(...fromCollections<DocumentRecord>(src, 'documents', id));
}
const parentMsg = (x: Extra, s: Student, parentId: string, parentName: string, date: string, text: string, from = 'csl_heena_qureshi', n = 1) =>
  x.messages.push({ id: `msg_${s.id.slice(4)}_${n}`, threadId: `${s.id}:${parentId}:csl_heena_qureshi`, learnerId: s.id, from, toIds: from === parentId ? ['csl_heena_qureshi'] : [parentId], text: text.replace('{p}', first(parentName)).replace('{s}', first(s.name)), sentUtc: istUtc(date, from === parentId ? '21:10' : '18:00'), readBy: from === parentId ? ['csl_heena_qureshi'] : [parentId] });
const supInvoice = (x: Extra, s: Student, payer: string, months: string[]) => months.forEach((d, i) => x.invoices.push({ id: `inv_${s.id.slice(4)}_sup_${i + 1}`, learnerId: s.id, payerId: payer, issuedUtc: istUtc(d, '09:00'), dueDate: addDaysLocal(d, 7), status: 'paid', paidUtc: istUtc(addDaysLocal(d, 2), '12:00'), lines: [{ title: 'Application Support, monthly', amountInr: 4999, planId: 'application_support' }], amountInr: 4999 }));
const task = (x: Extra, s: Student, id: string, title: string, kind: Task['kind'], dueDate: string, source: Task['source'], createdBy: string | undefined, created: string, more: Partial<Task> = {}) =>
  x.tasks.push({ id: `task_${s.id.slice(4)}_${id}`, learnerId: s.id, title, kind, dueDate, status: 'todo', source, ...(createdBy ? { createdBy } : {}), createdUtc: istUtc(created, '19:00'), ...more });
const mentorTrack = (x: Extra, s: Student, sessions: [string, string, string, string[], [string, string][]][], next: [string, string]) => {
  const k = s.id.slice(4);
  sessions.forEach(([date, title, summary, decisions, actions], i) => {
    const mid = `mtg_${k}_career_${i + 1}`;
    x.sessions.push({ id: `ses_${k}_mnt_${i + 1}`, code: `M-${i + 1}`, learnerId: s.id, learnerIds: [s.id], hostId: 'mnt_kelvin_thomas', hostRole: 'mentor', kind: 'career', title, startUtc: istUtc(date, '18:00'), minutes: 45, status: 'completed', mode: 'online', meetingNoteId: mid });
    x.meetings.push({ id: mid, learnerId: s.id, staffId: 'mnt_kelvin_thomas', date, kind: 'career', tier: 'T1', summary, decisions, actionItems: actions.map(([t, due], j) => ({ id: `ai_${k}_c${i + 1}_${j + 1}`, title: t, dueOn: due, taskId: `task_${k}_mnt_${i + 1}_${j + 1}`, ...(due < TODAY ? { done: true } : {}) })) });
    actions.forEach(([t, due], j) => task(x, s, `mnt_${i + 1}_${j + 1}`, t, 'action_item', due, 'mentor', 'mnt_kelvin_thomas', date, { refId: mid, ...(due < TODAY ? { status: 'done', completedUtc: istUtc(addDaysLocal(due, -1), '20:00') } : {}) }));
  });
  x.sessions.push({ id: `ses_${k}_mnt_next`, code: `M-${sessions.length + 1}`, learnerId: s.id, learnerIds: [s.id], hostId: 'mnt_kelvin_thomas', hostRole: 'mentor', kind: 'career', title: next[1], startUtc: istUtc(next[0], '18:00'), minutes: 45, status: 'scheduled', mode: 'online', joinUrl: 'https://meet.learnibility.demo/kelvin' });
};

// ------------------------------------------------------------------ per student

export function contentFor(c: Cast, o: SimOutput, built: Built): Extra {
  const x = empty();
  const s = c.student;
  const k = s.id.slice(4);
  const P = c.parent;
  void built;
  heenaTrack(x, s, o, c.start);
  parentMsg(x, s, P.id, P.name, '2026-11-15', 'Hello {p}, {s}’s weekly summary is ready on your Home page. Happy to talk if anything looks off.', 'csl_heena_qureshi', 1);
  if (s.grade >= 12) x.documents.push({ id: `doc_${k}_passport`, learnerId: s.id, folder: 'application_documents', title: 'Passport (bio page)', fileName: 'passport.pdf', kind: 'id_proof', uploadedUtc: istUtc('2026-09-02', '18:00'), source: 'M5', sizeKb: 640, requiresPlan: 'application_support' });
  const cert = (title: string, date: string, folder: DocumentRecord['folder'] = 'activities', kind: DocumentRecord['kind'] = 'certificate') => x.documents.push({ id: `doc_${k}_${x.documents.length + 1}`, learnerId: s.id, folder, title, fileName: `${title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.pdf`, kind, uploadedUtc: istUtc(date, '18:00'), source: 'M6', sizeKb: 220 });

  switch (s.id) {
    case 'lrn_aarav_kapoor': {
      cert('IMO Level 1, school topper', '2026-09-20');
      cert('National Science Olympiad, gold medal', '2026-10-30');
      x.careerShortlist = ['career-research-scientist', 'career-ai-ml-engineer'];
      const adv = getSubject('cbse-g8-maths')!.chapters.slice(8, 11);
      adv.forEach((ch, i) => task(x, s, `adv_${i + 1}`, `Advanced readiness: preview ${ch.name}`, 'learn', addDaysLocal(TODAY, 2 + 3 * i), 'system', undefined, '2026-11-16', { subjectId: 'cbse-g8-maths', refId: ch.id, minutes: 30, detail: 'Ahead of class: you have mastered every chapter so far.' }));
      task(x, s, 'olympiad_1', 'Olympiad enrichment: IMO Level 2 past paper (2025), Section A', 'practise', '2026-11-22', 'counsellor', 'csl_heena_qureshi', '2026-11-12', { minutes: 60, subjectId: 'cbse-g8-maths', detail: 'Timed, 60 minutes. Bring questions to Saturday.' });
      task(x, s, 'olympiad_2', 'Olympiad enrichment: NSO Level 2 practice set, Light and Sound', 'practise', '2026-11-25', 'counsellor', 'csl_heena_qureshi', '2026-11-12', { minutes: 45, subjectId: 'cbse-g8-science' });
      x.requests.push({ id: `req_${k}_1`, learnerId: s.id, createdUtc: istUtc('2026-11-09', '19:30'), weekStart: '2026-11-09', blockIds: [], kind: 'less_time', reason: 'I already know this week’s chapter; can I swap two chapter blocks for olympiad practice?', proposed: 'Compress the chapter blocks to one; add a 60-minute olympiad block on Saturday', status: 'approved', counsellorId: 'csl_heena_qureshi', decidedBy: 'csl_heena_qureshi', decidedUtc: istUtc('2026-11-10', '11:00'), decisionNote: 'Approved: compressed timetable, olympiad block on Saturdays.' });
      const sci = openGaps(o, 'cbse-g8-science')[0];
      if (sci) x.validations[sci.subtopicId] = { byId: 'tch_anjali_bose', utc: istUtc('2026-11-13', '13:10'), verdict: 'confirmed', note: 'Matches his lab write-up: knows the idea, skipped a step.' };
      parentMsg(x, s, P.id, P.name, '2026-11-12', 'Hi {p}, {s} is ahead in every chapter. I have added olympiad enrichment and compressed his timetable so he isn’t bored.', 'csl_heena_qureshi', 2);
      break;
    }
    case 'lrn_ishita_rao': {
      cert('Inter-school debate, best speaker (English)', '2026-09-26');
      cert('Cambridge Checkpoint English mock: 92%', '2026-10-31', 'academics', 'test_result');
      x.careerShortlist = ['career-journalist'];
      const fw = o.plans[o.plans.length - 1];
      parentMsg(x, s, P.id, P.name, '2026-11-14', `Hi {p}, {s}’s free plan has run ${fw?.freePlanWeeks ?? 3} weeks and her fractions and integers gaps are still open, so the plan now suggests a Maths tutor. Rahul Verma matches her gaps; she can book a free demo from Sessions.`, 'csl_heena_qureshi', 2);
      parentMsg(x, s, P.id, P.name, '2026-11-14', 'Thank you Heena. Yes, please let her book the demo. We are fine with a paid tutor for a couple of months.', P.id, 3);
      x.approvals.push({ id: `apr_${k}_tutor_ok`, learnerId: s.id, kind: 'plan_upgrade', targetId: fw?.id ?? 'plan', byId: P.id, decision: 'approved', utc: istUtc('2026-11-14', '21:15'), note: 'Agreed to paid Maths tutoring in principle.' });
      break;
    }
    case 'lrn_kabir_singh': {
      w2tFor(x, s.id);
      cert('Inter-school cricket, U-15 runners-up', '2026-09-12');
      x.careerShortlist = [];
      const st = 'cbse-g9-maths-ch05-st3';
      const qids = o.attempts.flatMap((a) => a.questionIds).filter((q, i, a) => q.startsWith(st + '-') && a.indexOf(q) === i).slice(0, 6);
      task(x, s, 'tch_1', `Re-teach set: ${nameOf(st)}`, 'test', '2026-11-20', 'teacher', 'tch_suresh_pillai', '2026-11-16', { minutes: 20, subjectId: 'cbse-g9-maths', refId: st, questionIds: qids, href: `/student/assessments/task.task_${k}_tch_1` });
      x.tasks[x.tasks.length - 1].createdUtc = istUtc('2026-11-16', '13:00');
      x.validations[st] = { byId: 'tch_suresh_pillai', utc: istUtc('2026-11-16', '12:40'), verdict: 'confirmed', note: 'Seven others in 9A show the same pattern; re-teaching on Friday.' };
      const cur = o.timetable[o.timetable.length - 1];
      const thuBlock = cur.blocks.find((b) => b.date === '2026-11-19' && b.kind !== 'buffer');
      x.requests.push({ id: 'req_kabir_singh_1', learnerId: s.id, createdUtc: istUtc('2026-10-27', '20:10'), weekStart: '2026-10-26', blockIds: [], kind: 'move', reason: 'Cricket practice on Wednesdays this month.', proposed: 'Move Wednesday study to Sunday 17:00', status: 'approved', counsellorId: 'csl_heena_qureshi', decidedBy: 'csl_heena_qureshi', decidedUtc: istUtc('2026-10-28', '11:00'), decisionNote: 'Approved; Sunday window added.' });
      x.requests.push({ id: 'req_kabir_singh_2', learnerId: s.id, createdUtc: istUtc('2026-11-17', '21:05'), weekStart: '2026-11-16', blockIds: thuBlock ? [thuBlock.id] : [], kind: 'move', reason: 'School science exhibition runs late on Thursday.', proposed: { date: '2026-11-22', start: '17:00', end: '18:00' }, status: 'pending', counsellorId: 'csl_heena_qureshi' });
      x.meetings.push({ id: 'mtg_kabir_singh_estimate', learnerId: s.id, staffId: 'csl_heena_qureshi', date: '2026-10-07', kind: 'academic', tier: 'T1', summary: 'Kabir rates himself 5/5 on answers he gets wrong (G9) and drops easy marks (G4). Agreed estimate-first: before each answer, write how sure he is, then check the two lowest-confidence answers.', decisions: ['Estimate-first on every test for six weeks', 'Two-minute checking pass at the end'], actionItems: [{ id: 'ai_kabir_est_1', title: 'Write a confidence estimate before every answer this week', dueOn: '2026-10-14', done: true }] });
      parentMsg(x, s, P.id, P.name, '2026-11-13', 'Hi {p}, good news: six weeks of estimate-first are working. {s}’s calibration (MCI) has gone from about 0.55 to about 0.7.', 'csl_heena_qureshi', 2);
      break;
    }
    case 'lrn_meera_iyer': {
      cert('MYP Science fair, first place (untimed project)', '2026-10-10');
      x.careerShortlist = ['career-doctor', 'career-biotechnologist'];
      wellbeing(x, s, '2026-11-04', 'Meera described a racing heart and blanking in timed tests, and rates her own correct answers low. Screened stress and exam anxiety are elevated. Agreed a breathing routine before tests, untimed-then-timed practice, and a weekly check-in. No referral needed now.',
        ['Box breathing for 2 minutes before each test', 'Practise untimed first, then timed with 25% extra time, then normal time', 'Weekly 10-minute check-in'],
        'Hi Radhika, I had a check-in with Meera this week. She is doing well in Science; we agreed some techniques for timed tests. Nothing for you to do, and I will keep you posted.', P.id);
      x.requests.push({ id: `req_${k}_1`, learnerId: s.id, createdUtc: istUtc('2026-11-05', '19:00'), weekStart: '2026-11-09', blockIds: [], kind: 'more_time', reason: 'Heena suggested timed practice in steps; can the weekly test be untimed for two weeks?', proposed: 'Weekly test untimed for 2 weeks, then 25% extra time', status: 'approved', counsellorId: 'csl_heena_qureshi', decidedBy: 'csl_heena_qureshi', decidedUtc: istUtc('2026-11-06', '10:00'), decisionNote: 'Approved for two weeks; review on 20 Nov.' });
      task(x, s, 'timed_1', 'Timed practice: 10 Science questions in 12 minutes', 'practise', '2026-11-21', 'counsellor', 'csl_heena_qureshi', '2026-11-14', { minutes: 15, subjectId: 'ib-g9-science' });
      break;
    }
    case 'lrn_ananya_kapoor': {
      appsFrom(x, W2A, s.id);
      cert('Model UN, Outstanding Delegate', '2026-09-27');
      cert('Cambridge IGCSE Maths mock: A*', '2026-11-01', 'academics', 'test_result');
      x.careerShortlist = ['career-economist'];
      x.meetings.push({ id: 'mtg_ananya_fit_1', learnerId: s.id, staffId: 'csl_farah_siddiqui', date: '2026-11-10', kind: 'applications', tier: 'T1', summary: 'Walked Ananya through her free University Fit: three reaches (Yale, Berkeley EECS), Purdue as a target. Explained what Application Support adds (essay reviews, deadlines board, document vault). She will decide with her mother.', decisions: ['Keep exploring on the free plan for now'], actionItems: [{ id: 'ai_ananya_fit_1', title: 'Talk to Mum about Application Support', dueOn: '2026-11-24' }] });
      parentMsg(x, s, P.id, P.name, '2026-11-11', 'Hi {p}, Farah ran Ananya’s free University Fit. If you want essay reviews and a deadline board for the US round, Application Support is available from Plan and spend.', 'csl_farah_siddiqui', 2);
      break;
    }
    case 'lrn_rohan_das': {
      w2tFor(x, s.id);
      cert('School football team', '2026-09-05');
      const firstPaid = o.plans.find((p) => p.plan.paidTuition.recommended);
      const fpDate = firstPaid ? localDateOf(firstPaid.createdUtc) : '2026-09-19';
      wellbeing(x, s, '2026-11-06', 'Rohan reports exam stress and pressure at home about the boards. Agreed shorter study blocks and a weekly 10-minute check-in.', ['Shorter 25-minute blocks', 'Weekly check-in'],
        'Hi Anita, I checked in with Rohan this week. We agreed shorter study blocks; please keep encouraging him, the tutor sessions are helping.', P.id);
      parentMsg(x, s, P.id, P.name, addDaysLocal(fpDate, 1), 'Hello {p}, {s}’s free plan has run three weeks and his Maths gaps now span three chapters, so the plan suggests a paid Maths tutor. You can see the reason under Plan and spend.', 'csl_heena_qureshi', 2);
      parentMsg(x, s, P.id, P.name, addDaysLocal(fpDate, 2), 'Thank you. Let us try a demo first, after his unit test.', P.id, 3);
      parentMsg(x, s, P.id, P.name, '2026-11-15', 'Hi {p}, {s} closed two Maths gaps since Rahul started. He has asked for a Science tutor too; it is waiting for your approval under Plan and spend.', 'csl_heena_qureshi', 4);
      x.approvals.push({ id: 'apr_rohan_das_rahul', learnerId: s.id, kind: 'paid_tutor', targetId: 'bkg_w2t_rohan', byId: P.id, decision: 'approved', utc: istUtc('2026-10-17', '21:00') });
      const sci = openGaps(o, 'cbse-g10-science').slice(0, 2);
      x.bookings.push({
        id: 'bkg_rohan_das_science', learnerId: s.id, tutorId: 'tut_sunita_gupta', kind: 'regular', status: 'requested', format: 'one_to_one', mode: 'online', subjectId: 'cbse-g10-science', priceInr: 500, requestedAt: istUtc('2026-11-16', '20:30'), slotStartUtc: istUtc('2026-11-21', '11:00'), minutes: 60, sessionsPerWeek: 2,
        topic: sci.map((g) => nameOf(g.subtopicId)).join(' and ') || 'Chemical reactions', note: 'Rohan asked for help before the pre-boards.',
        sharedGapSnapshot: { sharedUtc: istUtc('2026-11-16', '20:30'), subjectId: 'cbse-g10-science', score: 48, gaps: sci.map((g) => ({ gapId: g.id, subtopicId: g.subtopicId, name: nameOf(g.subtopicId), code: g.code, level: g.level, hoursToClose: g.hoursToClose })) },
        parentApproval: { parentId: P.id, status: 'pending', reason: 'Paid sessions for a minor need a parent’s approval.' },
        matchReason: 'Teaches CBSE Class 10 Science, concept-first, free 30-minute demo, ₹500 an hour, evenings that overlap Rohan’s study windows.',
      });
      const rahul = x.sessions.filter((z) => z.hostId === 'tut_rahul_verma' && z.status === 'completed' && z.kind !== 'demo');
      for (const m of ['2026-10', '2026-11']) {
        const n = rahul.filter((z) => z.startUtc.slice(0, 7) === m).length;
        if (!n) continue;
        const paid = m === '2026-10';
        x.invoices.push({ id: `inv_rohan_das_rahul_${m.replace('-', '')}`, learnerId: s.id, payerId: P.id, issuedUtc: istUtc(paid ? '2026-10-31' : '2026-11-15', '09:00'), dueDate: paid ? '2026-11-07' : '2026-11-22', status: paid ? 'paid' : 'due', ...(paid ? { paidUtc: istUtc('2026-11-02', '19:30') } : {}), lines: [{ title: `Rahul Verma: ${n} × 60 min Maths (${m})`, amountInr: n * 800, bookingId: 'bkg_w2t_rohan' }], amountInr: n * 800 });
      }
      x.invoices.push({ id: 'inv_rohan_das_mock', learnerId: s.id, payerId: P.id, issuedUtc: istUtc('2026-11-12', '09:00'), dueDate: '2026-11-19', status: 'paid', paidUtc: istUtc('2026-11-12', '20:00'), lines: [{ title: 'Mock test series, Class 10 Maths', amountInr: 600 }], amountInr: 600 });
      const g = openGaps(o, 'cbse-g10-maths')[0];
      if (g) x.validations[g.subtopicId] = { byId: 'tch_suresh_pillai', utc: istUtc('2026-11-11', '14:00'), verdict: 'confirmed', note: 'Same mistakes in his class test.' };
      break;
    }
    case 'lrn_vihaan_joshi': {
      cert('JEE Main mock 1: 168/300', '2026-10-12', 'academics', 'test_result');
      cert('Robotics club, regional finalist', '2026-08-30');
      x.careerShortlist = ['career-software-engineer', 'career-aerospace-engineer'];
      tutorTrack(x, s, o, { tutorId: 'tut_meenakshi_rao', tutorName: 'Meenakshi Rao', subjectId: 'cbse-g11-chemistry', demo: '2026-09-17', start: '2026-09-22', days: [1, 4], time: '19:00', minutes: 60, rate: 900, parentId: P.id });
      x.requests.push({ id: `req_${k}_1`, learnerId: s.id, createdUtc: istUtc('2026-10-12', '21:00'), weekStart: '2026-10-12', blockIds: [], kind: 'add', reason: 'Chemistry fades after a week. Can I get short spaced reviews on top of the tutor sessions?', proposed: '15-minute Chemistry reviews on day 1, 3 and 7 after each chapter', status: 'approved', counsellorId: 'csl_heena_qureshi', decidedBy: 'csl_heena_qureshi', decidedUtc: istUtc('2026-10-13', '10:30'), decisionNote: 'Approved; the timetable now spaces Chemistry reviews.' });
      parentMsg(x, s, P.id, P.name, '2026-10-14', 'Hi {p}, {s}’s Maths is excellent. His Chemistry is the issue: he learns it well but retains under 70% after a week, so his timetable now has spaced reviews alongside Mrs Rao’s sessions.', 'csl_heena_qureshi', 2);
      break;
    }
    case 'lrn_sara_khan': {
      cert('Commerce quiz, 2nd place', '2026-09-12');
      x.careerShortlist = ['career-chartered-accountant', 'career-data-analyst'];
      mentorTrack(x, s, [
        ['2026-10-15', 'Career session: what CAs and data analysts do', 'Mapped Sara’s strengths (Accountancy, logic, Excel) onto both careers. Both fit; she wants to know more about day-to-day work.', ['Shortlist Chartered Accountant and Data Analyst'], [['Shadow an article assistant at an audit firm for a day', '2026-11-01']]],
        ['2026-11-12', 'Career session: CA vs Data Analyst', 'Compared Chartered Accountant (ICAI route, 4.5 to 5 years) with Data Analyst (BSc + SQL/Python skills). Sara enjoys accounting logic but wants more variety; both stay open.', ['Keep both careers shortlisted', 'Try a free SQL course before deciding'], [['Finish the first 3 modules of a free SQL course', '2026-11-25'], ['Read the ICAI Foundation syllabus', '2026-11-22']]],
      ], ['2026-11-26', 'Career session: skill plan review']);
      x.messages.push({ id: 'msg_sara_khan_kelvin', threadId: `${s.id}:mnt_kelvin_thomas`, learnerId: s.id, from: 'mnt_kelvin_thomas', toIds: [s.id], text: 'Great session today, Sara. Start the SQL modules and tell me how they feel next time.', sentUtc: istUtc('2026-11-12', '19:05'), readBy: [s.id] });
      break;
    }
    case 'lrn_arjun_nair': {
      cert('Kerala MUN, Best Position Paper', '2026-09-19');
      cert('School debate captain', '2026-08-20');
      x.careerShortlist = ['career-corporate-lawyer', 'career-policy-analyst'];
      mentorTrack(x, s, [
        ['2026-10-08', 'Career session: is Law the right fit?', 'Arjun writes and argues well; marks are uneven because evaluation questions (C4) cost him. Law fits his strengths; we looked at corporate law and policy work.', ['Shortlist corporate lawyer and policy analyst'], [['Sit in on a moot court at school', '2026-10-30']]],
        ['2026-11-11', 'Career session: CLAT in India or an LLB in the UK', 'CLAT route: NLSIU, NALSAR, NLU Delhi; 5-year BA LLB, about ₹2.5 to 3.5 lakh a year. UK LLB: 3 years, then the SQE to practise in England, or conversion to practise in India; much higher cost. Decided to prepare for CLAT 2028 and keep two UK options on the list.', ['Prepare for CLAT 2028', 'Keep KCL and Leeds on the shortlist'], [['Take one CLAT sample paper, untimed', '2026-11-29'], ['Ask Farah about UK LLB recognition in India', '2026-11-20']]],
      ], ['2026-12-09', 'Career session: CLAT plan and reasoning skills']);
      const sl: [string, string, 'reach' | 'target' | 'safe'][] = [['uni-in-nlsiu-bengaluru', 'uni-in-nlsiu-bengaluru-ba-llb', 'reach'], ['uni-in-nalsar-hyderabad', 'uni-in-nalsar-hyderabad-ba-llb', 'reach'], ['uni-in-nlu-delhi', 'uni-in-nlu-delhi-ba-llb', 'target'], ['uni-uk-kcl', 'uni-uk-kcl-llb-law', 'reach'], ['uni-uk-leeds', 'uni-uk-leeds-llb-law', 'target']];
      sl.forEach(([u, p, f], i) => x.shortlist.push({ learnerId: s.id, universityId: u, programmeId: p, fitGroup: f, savedUtc: istUtc(addDaysLocal('2026-11-11', i % 3), '20:00') }));
      x.meetings.push({ id: 'mtg_arjun_fit_1', learnerId: s.id, staffId: 'csl_farah_siddiqui', date: '2026-11-13', kind: 'applications', tier: 'T1', summary: 'Exploring only: ran University Fit for Law. NLU Delhi is a target if his CLAT mocks reach the 90th percentile; KCL and Leeds LLB are possible with IB 36+. No applications this year.', decisions: ['Explore on the free plan until DP2'], actionItems: [{ id: 'ai_arjun_fit_1', title: 'Save two more UK LLB options to compare', dueOn: '2026-11-27' }] });
      const g = openGaps(o, 'ib-g11-economics')[0];
      if (g) x.validations[g.subtopicId] = { byId: 'tch_tom_hayes', utc: istUtc('2026-11-12', '15:00'), verdict: 'confirmed', note: 'His essays describe well but do not evaluate; working on it in class.' };
      break;
    }
    case 'lrn_diya_sharma': {
      cert('NEET mock 3: 541/720', '2026-10-18', 'academics', 'test_result');
      x.careerShortlist = ['career-doctor', 'career-pharmacist'];
      tutorTrack(x, s, o, { tutorId: 'tut_fatima_sheikh', tutorName: 'Fatima Sheikh', subjectId: 'cbse-g12-physics', demo: '2026-08-29', start: '2026-09-05', days: [5, 6], time: '16:00', minutes: 90, rate: 900, parentId: P.id });
      wellbeing(x, s, '2026-10-21', 'Diya sleeps about 5 hours on school nights and under 5 before mocks; daytime sleepiness most days. Her worst mock followed her shortest night. Agreed a fixed bedtime, no revision after 23:00, and moving the Sunday morning block later. Support only; no referral.',
        ['Fixed 23:00 bedtime on school nights', 'No new material the night before a mock', 'Weekly check-in for a month'],
        'Hi Kavita, I checked in with Diya about her mock routine. We agreed a few changes to her week before mocks; she is working hard and doing fine.', P.id);
      x.requests.push({ id: `req_${k}_1`, learnerId: s.id, createdUtc: istUtc('2026-11-16', '22:10'), weekStart: '2026-11-16', blockIds: [], kind: 'move', reason: 'Mock 5 is on 29 Nov. Can Sunday’s 9 AM block move to the afternoon so I can sleep in?', proposed: 'Move Sunday 09:00 blocks to 14:00 until the mock', status: 'pending', counsellorId: 'csl_heena_qureshi' });
      task(x, s, 'mock5', 'NEET mock 5 (full syllabus, 200 minutes)', 'test', '2026-11-29', 'system', undefined, '2026-11-10', { minutes: 200, href: '/student/assessments', detail: 'Mock 5 of 6. Mock 6 is on 20 December.' });
      parentMsg(x, s, P.id, P.name, '2026-11-08', 'Hi {p}, Diya has finished 4 of her 6 NEET mocks. Scores swing between mocks; Physics is the main lever and Mrs Sheikh’s weekend sessions are focused on it.', 'csl_heena_qureshi', 2);
      break;
    }
    case 'lrn_nikhil_reddy': {
      appsFrom(x, W2A, s.id);
      x.careerShortlist = ['career-management-consultant', 'career-business-analyst'];
      supInvoice(x, s, P.id, ['2026-09-01', '2026-10-01', '2026-11-01']);
      break;
    }
    case 'lrn_tara_menon': {
      appsFrom(x, TARA, s.id);
      cert('Malayalam flashcards app: 2,000 downloads (Play Store)', '2026-08-28', 'job_ready', 'portfolio');
      cert('School bus-tracker app, used by 600 students', '2026-09-15', 'job_ready', 'portfolio');
      cert('Robotics club lead', '2026-08-24');
      x.careerShortlist = ['career-software-engineer', 'career-product-manager'];
      supInvoice(x, s, P.id, ['2026-08-20', '2026-09-20', '2026-10-20']);
      parentMsg(x, s, P.id, P.name, '2026-11-02', 'Hi {p}, Tara’s Georgia Tech and Purdue Early Action applications are in. UT Austin is next (1 December); her essays are the part we are polishing.', 'csl_farah_siddiqui', 2);
      break;
    }
    case 'lrn_kunal_verma': {
      cert('Inter-school parliamentary debate, winner', '2026-08-22');
      cert('Head boy, student council', '2026-07-01');
      x.careerShortlist = ['career-civil-services-officer', 'career-corporate-lawyer', 'career-journalist'];
      tutorTrack(x, s, o, { tutorId: 'tut_farhan_ali', tutorName: 'Farhan Ali', subjectId: 'cbse-g12-english', demo: '2026-09-26', start: '2026-10-01', days: [2, 5], time: '18:30', minutes: 60, rate: 600, parentId: P.id });
      mentorTrack(x, s, [
        ['2026-09-24', 'Career session: careers that use debating', 'Kunal’s marks are weak but he leads and argues brilliantly. His written English (moved from Hindi medium) is what costs marks, not understanding. Looked at civil services, law and journalism.', ['Shortlist civil services, corporate law and journalism', 'Work on written English with a tutor'], [['Book an English writing tutor demo', '2026-09-30']]],
        ['2026-11-05', 'Career session: CLAT or a BA first?', 'Compared CLAT (law) with a BA in Political Science then UPSC. Both use his strengths. Agreed to keep both open and build a portfolio of debates and speeches.', ['Keep law and civil services open', 'Start a debate portfolio'], [['Upload three debate certificates to Inventory', '2026-11-15'], ['Write a 300-word op-ed in English and share it with Farhan', '2026-11-26']]],
      ], ['2026-12-03', 'Career session: portfolio review']);
      parentMsg(x, s, P.id, P.name, '2026-11-14', 'Hi {p}, {s} understands his subjects well; long written answers in English are costing him marks. Farhan’s sessions are focused on exactly that.', 'csl_heena_qureshi', 2);
      x.extraConsents = ['share_with_tutor'];
      break;
    }
  }
  if (s.tutorIds.length || x.bookings.length) if (!x.extraConsents.includes('share_with_tutor')) x.extraConsents.push('share_with_tutor');
  // unused export guard
  void (null as unknown as GapCode);
  return x;
}
