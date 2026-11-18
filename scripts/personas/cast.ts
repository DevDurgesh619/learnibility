/**
 * W3-P: the 14 student personas. Stories are fixed (build/personas-brief.md); traits are chosen so the real
 * engines produce them. The six W2-0 fixture students keep their identities, schools and traits.
 */
import type { PersonaSummary } from '@/lib/types';
import type { Student } from '@/lib/data/types';
import type { SubjectSim, Traits } from './lib';

export interface Cast {
  student: Student;
  start: string;
  subjects: SubjectSim[];
  traits: Traits;
  parent: { id: string; name: string; relation: 'mother' | 'father' };
  persona: Pick<PersonaSummary, 'story' | 'order' | 'programme'>;
  /** Profile values fixed by the story (budgets are integer rupees: p178 annual, p180 India UG ceiling, p181 abroad total). */
  profile: Record<string, unknown>;
  /** T3 values the student shared in screening (student and counsellor only). */
  t3?: Record<string, unknown>;
  /** Seed variant (see lib.ts SimInput.seed). */
  seed?: string;
}

const weekdays = (start: string, end: string) => (['mon', 'tue', 'wed', 'thu', 'fri'] as const).map((day) => ({ day, start, end }));
const avail = (wk: [string, string], sat: [string, string], sun?: [string, string]) => [
  ...weekdays(wk[0], wk[1]),
  { day: 'sat' as const, start: sat[0], end: sat[1] },
  ...(sun ? [{ day: 'sun' as const, start: sun[0], end: sun[1] }] : []),
];
const CBSE_START = '2026-04-06';
const TERM_START = '2026-08-17'; // Cambridge and IB
const T = (p: Partial<Traits>): Traits => ({ base: 0.82, spread: 0.05, slip: 0.05, blank: 0.01, overconf: 0, growth: 0.05, speed: 0.9, doneRate: 0.8, forget: 0.04, prior: 0.5, ...p });

function student(p: Partial<Student> & Pick<Student, 'id' | 'firstName' | 'lastName' | 'board' | 'grade' | 'stream' | 'programme' | 'school' | 'city' | 'band' | 'plan'>, subjects: SubjectSim[]): Student {
  return {
    role: 'student', name: `${p.firstName} ${p.lastName}`, availability: avail(['17:00', '19:00'], ['10:00', '12:30']), weeklyHours: 8,
    tzOffsetMinutes: 330, joinedUtc: (p.board === 'cbse' ? `${CBSE_START}T04:30:00.000Z` : `${TERM_START}T04:30:00.000Z`), parentIds: [], counsellorIds: ['csl_heena_qureshi'], mentorIds: [], tutorIds: [], sectionIds: [],
    profileCompletionPct: 62, medium: 'English', subjects: subjects.map((s) => ({ subjectId: s.subjectId, depth: s.depth })), ...p,
  } as Student;
}

const S = (subjectId: string, depth: 'full' | 'light', chapters: number, more: Partial<SubjectSim> = {}): SubjectSim => ({ subjectId, depth, chapters, ...more });

function make(c: Omit<Cast, 'student'> & { s: Parameters<typeof student>[0] }): Cast {
  const { s, ...rest } = c;
  return { ...rest, student: student({ ...s, story: s.story ?? c.persona.story, parentIds: [c.parent.id, ...(s.parentIds ?? [])].filter((x, i, a) => a.indexOf(x) === i) }, c.subjects) };
}

export const CAST: Cast[] = [
  // ------------------------------------------------------------ grade 8
  make({
    s: { id: 'lrn_aarav_kapoor', firstName: 'Aarav', lastName: 'Kapoor', board: 'cbse', grade: 8, stream: 'none', programme: 'CBSE Class 8', school: 'Delhi Public School, Sector 45', city: 'Gurugram', band: 'excellent', plan: 'free',
      weeklyHours: 7, goal: 'Maths and Science olympiads, then IIT', currentChapterIds: ['cbse-g8-maths-ch09'], profileCompletionPct: 79, counsellorIds: ['csl_heena_qureshi'], sectionIds: ['sec-cbse-g8-science-a'],
      availability: avail(['17:30', '19:00'], ['09:30', '12:00']) },
    start: CBSE_START,
    subjects: [S('cbse-g8-maths', 'full', 8), S('cbse-g8-science', 'full', 7), S('cbse-g8-english', 'light', 2)],
    traits: T({ base: 0.97, spread: 0.02, slip: 0.015, growth: 0.1, speed: 0.6, doneRate: 0.95, prior: 0.8, forget: 0.01, overconf: 0.02 }),
    parent: { id: 'par_neha_kapoor', name: 'Neha Kapoor', relation: 'mother' },
    persona: { story: 'Class 8 topper; ready for advanced topics and olympiad enrichment.', order: 1, programme: 'CBSE Class 8' },
    profile: { p31: 2, p178: 400000, p181: 12000000, p193: 'Laptop + broadband', p212: 'C1', p230: 3, p163: 5, p150: 4, p268: 4, p200: 'IRA' },
  }),
  make({
    s: { id: 'lrn_ishita_rao', firstName: 'Ishita', lastName: 'Rao', board: 'cambridge', grade: 8, stream: 'none', programme: 'Cambridge Lower Secondary Stage 9', school: 'Indus International School', city: 'Bengaluru', band: 'average', plan: 'free',
      weeklyHours: 8, goal: 'Get comfortable with Maths before IGCSE', currentChapterIds: ['cambridge-g8-maths-ch07'], profileCompletionPct: 66, sectionIds: ['sec-cambridge-g8-english-a'] },
    start: TERM_START,
    subjects: [S('cambridge-g8-maths', 'full', 6), S('cambridge-g8-english', 'full', 4, { traits: { base: 0.93, weak: {} } }), S('cambridge-g8-social-science', 'light', 3, { traits: { base: 0.9, weak: {} } })],
    traits: T({ base: 0.8, spread: 0.06, slip: 0.05, overconf: -0.1, growth: 0.03, speed: 0.9, doneRate: 0.85, prior: 0.75,
      weak: { 'cambridge-g8-maths-ch01-st1': -0.25, 'cambridge-g8-maths-ch01-st2': -0.25, 'cambridge-g8-maths-ch03-st1': -0.2 } }),
    parent: { id: 'par_sunita_rao', name: 'Sunita Rao', relation: 'mother' },
    persona: { story: 'Strong in English and History; Maths gaps from grade 7 fractions and integers. Free plan ran 3 weeks; a tutor is next.', order: 3, programme: 'Cambridge Lower Secondary' },
    profile: { p31: 1.5, p178: 180000, p193: 'Laptop + broadband', p212: 'C1', p163: 4, p150: 3 },
  }),
  // ------------------------------------------------------------ grade 9
  make({
    s: { id: 'lrn_kabir_singh', firstName: 'Kabir', lastName: 'Singh', board: 'cbse', grade: 9, stream: 'none', programme: 'CBSE Class 9', school: 'Delhi Public School, Dwarka', city: 'New Delhi', band: 'average', plan: 'free',
      sectionIds: ['sec-cbse-g9-maths-a'], weeklyHours: 7, goal: 'Score 90% in Class 10 boards', currentChapterIds: ['cbse-g9-maths-ch07'], profileCompletionPct: 58, tutorIds: ['tut_rahul_verma'],
      availability: avail(['17:30', '19:30'], ['10:00', '12:30'], ['17:00', '18:00']) },
    seed: 'v4',
    start: CBSE_START,
    subjects: [S('cbse-g9-maths', 'full', 6, { checkDates: ['2026-05-14', '2026-07-09', '2026-08-13', '2026-09-24', '2026-10-29', '2026-11-12'] }), S('cbse-g9-science', 'light', 3)],
    // estimate-first starts 2026-10-07: over-confidence falls over six weeks (MCI rises)
    traits: T({ base: 0.86, spread: 0.03, slip: 0.12, overconf: [['2026-10-07', 0.15], ['2026-11-14', 0.05]], calib: [['2026-10-07', 0], ['2026-11-14', 0.85]], growth: 0.04, speed: 0.75, doneRate: 0.8, prior: 0.92, forget: 0.12, cgPenalty: { C4: 0.08 },
      weak: { 'cbse-g9-maths-ch05-st3': 0.33, 'cbse-g9-maths-ch06-st2': 0.45 } }),
    parent: { id: 'par_harpreet_singh', name: 'Harpreet Singh', relation: 'father' },
    persona: { story: 'Quick but careless, and more confident than his marks. Six weeks of estimate-first are working.', order: 4, programme: 'CBSE Class 9' },
    profile: { p31: 1.5, p178: 120000, p193: 'Laptop + broadband', p212: 'B2', p230: 2, p163: 3, p150: 4 },
  }),
  make({
    s: { id: 'lrn_meera_iyer', firstName: 'Meera', lastName: 'Iyer', board: 'ib', grade: 9, stream: 'none', programme: 'IB MYP Year 4', school: 'Kodai International Academy', city: 'Chennai', band: 'above_avg', plan: 'free',
      weeklyHours: 8, goal: 'Biology in DP; maybe medicine', currentChapterIds: ['ib-g9-science-ch06'], profileCompletionPct: 70,
      availability: avail(['16:30', '18:30'], ['10:00', '12:00'], ['16:00', '17:30']) },
    seed: 'v1',
    start: TERM_START,
    subjects: [S('ib-g9-science', 'full', 5), S('ib-g9-maths', 'full', 5, { traits: { base: 0.8 } }), S('ib-g9-english', 'light', 2)],
    // knows the work untimed; runs out of time and doubts correct answers
    traits: T({ base: 0.9, spread: 0.04, slip: 0.03, overconf: -0.68, growth: 0.05, speed: 1.6, doneRate: 0.9, prior: 0.55, typePenalty: { case: 0.12 } }),
    parent: { id: 'par_radhika_iyer', name: 'Radhika Iyer', relation: 'mother' },
    persona: { story: 'Strong in Science untimed, runs out of time in tests and doubts herself; counsellor wellbeing check.', order: 5, programme: 'IB MYP 4' },
    profile: { p31: 2, p178: 250000, p193: 'Laptop + broadband', p212: 'C1', p230: 3, p163: 4, p150: 2 },
    t3: { p109: 'Elevated before tests', p111: 'High (screened 7/10)', p84: 3, p142: 'Low-moderate' },
  }),
  // ------------------------------------------------------------ grade 10
  make({
    s: { id: 'lrn_ananya_kapoor', firstName: 'Ananya', lastName: 'Kapoor', board: 'cambridge', grade: 10, stream: 'none', programme: 'Cambridge IGCSE', school: 'The Shri Ram School, Moulsari', city: 'Gurugram', band: 'excellent', plan: 'free',
      counsellorIds: ['csl_heena_qureshi', 'csl_farah_siddiqui'], weeklyHours: 10, goal: 'Economics or Engineering at a top US university', currentChapterIds: ['cambridge-g10-maths-ch04'], profileCompletionPct: 77, sectionIds: ['sec-cambridge-g10-english-a'] },
    start: TERM_START,
    subjects: [S('cambridge-g10-maths', 'full', 3), S('cambridge-g10-physics', 'full', 3), S('cambridge-g10-chemistry', 'light', 2), S('cambridge-g10-english', 'light', 2)],
    traits: T({ base: 0.94, spread: 0.03, slip: 0.025, growth: 0.08, speed: 0.7, doneRate: 0.95, prior: 0.7, forget: 0.015 }),
    parent: { id: 'par_neha_kapoor', name: 'Neha Kapoor', relation: 'mother' },
    persona: { story: 'IGCSE topper aiming at US universities; used the free University Fit, upgrade offered.', order: 6, programme: 'Cambridge IGCSE' },
    profile: { p16: '8 A* predicted', p25: 'SAT 1520 (practice)', p212: 'C2', p268: 4, p178: 400000, p181: 12000000, p230: 5, p31: 2.5, p200: 'IAE' },
  }),
  make({
    s: { id: 'lrn_rohan_das', firstName: 'Rohan', lastName: 'Das', board: 'cbse', grade: 10, stream: 'none', programme: 'CBSE Class 10', school: 'Kendriya Vidyalaya, Salt Lake', city: 'Kolkata', band: 'below_avg', plan: 'free',
      sectionIds: ['sec-cbse-g10-maths-b', 'sec-cbse-g10-science-b'], weeklyHours: 6, goal: 'Pass Class 10 boards with 75%', joinedUtc: '2026-08-17T04:30:00.000Z', currentChapterIds: ['cbse-g10-maths-ch07'], profileCompletionPct: 44, tutorIds: ['tut_rahul_verma'] },
    seed: 'v10',
    start: '2026-08-17',
    subjects: [
      S('cbse-g10-maths', 'full', 6, { checkDates: ['2026-08-27', '2026-09-03', '2026-09-10', '2026-09-24', '2026-10-15', '2026-11-12'], mocks: [['2026-11-14', 1]] }),
      S('cbse-g10-science', 'light', 3, { checkDates: ['2026-09-03', '2026-09-24', '2026-10-08'], traits: { base: 0.72, weak: { 'cbse-g10-science-ch01-st2': 0.4, 'cbse-g10-science-ch02-st1': 0.35 } } }),
      S('cbse-g10-social-science', 'light', 3, { checkDates: ['2026-09-10', '2026-10-01', '2026-10-29'], traits: { base: 0.76 } }),
    ],
    // free plan barely moves the gaps; the paid Maths tutor (from 20 Oct) gives a small recovery
    traits: T({ base: 0.7, spread: 0.06, slip: 0.08, blank: [['2026-10-15', 0.07], ['2026-11-10', 0.04]], growth: [['2026-10-19', 0.012], ['2026-10-20', 0.07]], speed: 1.1, doneRate: [['2026-10-15', 0.5], ['2026-11-10', 0.65]], prior: 0.85, forget: 0.2, cgPenalty: { C4: 0.2 },
      weak: { 'cbse-g10-maths-ch02-st2': 0.3, 'cbse-g10-maths-ch03-st2': 0.35, 'cbse-g10-maths-ch03-st3': 0.4, 'cbse-g10-maths-ch04-st1': 0.32, 'cbse-g10-maths-ch04-st3': 0.38 } }),
    parent: { id: 'par_anita_das', name: 'Anita Das', relation: 'mother' },
    persona: { story: 'Struggling in Maths; the free plan ran 3 weeks without closing his gaps, so a paid tutor started 4 weeks ago.', order: 7, programme: 'CBSE Class 10' },
    profile: { p31: 1, p178: 72000, p193: 'Shared phone + broadband', p212: 'B1', p163: 2, p150: 2 },
    t3: { p109: 'High (exam pressure at home)', p111: 'Moderate-high' },
  }),
  // ------------------------------------------------------------ grade 11
  make({
    s: { id: 'lrn_vihaan_joshi', firstName: 'Vihaan', lastName: 'Joshi', board: 'cbse', grade: 11, stream: 'science', programme: 'CBSE Class 11 Science (PCM)', school: 'The Bishop’s School, Camp', city: 'Pune', band: 'above_avg', plan: 'free',
      weeklyHours: 14, goal: 'JEE Advanced 2028', currentChapterIds: ['cbse-g11-chemistry-ch05'], profileCompletionPct: 72, tutorIds: ['tut_meenakshi_rao'],
      availability: avail(['18:00', '21:00'], ['09:00', '13:00'], ['10:00', '12:00']) },
    start: CBSE_START,
    subjects: [
      S('cbse-g11-chemistry', 'full', 4, { checkDates: ['2026-06-04', '2026-08-06', '2026-09-24', '2026-10-29'], traits: { base: 0.84, forget: 0.42, growth: 0.04 } }),
      S('cbse-g11-physics', 'full', 6, { traits: { base: 0.86 } }),
      S('cbse-g11-maths', 'full', 7, { traits: { base: 0.95, slip: 0.02 } }),
    ],
    traits: T({ base: 0.86, spread: 0.04, slip: 0.04, growth: 0.06, speed: 0.85, doneRate: 0.85, forget: 0.05, prior: 0.55 }),
    parent: { id: 'par_sanjay_joshi', name: 'Sanjay Joshi', relation: 'father' },
    persona: { story: 'JEE aspirant: strong Maths, but Chemistry fades in a week; spaced reviews and a Chemistry tutor.', order: 8, programme: 'CBSE Science (PCM)' },
    profile: { p31: 3.5, p178: 240000, p180: 1500000, p193: 'Laptop + broadband', p212: 'B2', p230: 2, p163: 4, p150: 3, p200: 'IRC', p25: 'JEE Main mock 1: 168/300' },
  }),
  make({
    s: { id: 'lrn_sara_khan', firstName: 'Sara', lastName: 'Khan', board: 'cbse', grade: 11, stream: 'commerce', programme: 'CBSE Class 11 Commerce', school: 'St. Xavier’s Senior Secondary', city: 'Mumbai', band: 'above_avg', plan: 'free',
      mentorIds: ['mnt_kelvin_thomas'], weeklyHours: 9, goal: 'Chartered Accountant or Data Analyst?', currentChapterIds: ['cbse-g11-economics-ch07'], profileCompletionPct: 74 },
    seed: 'v12',
    start: CBSE_START,
    subjects: [
      S('cbse-g11-economics', 'full', 6, { checkDates: ['2026-05-21', '2026-07-16', '2026-08-27', '2026-09-24', '2026-10-22', '2026-11-05'] }),
      S('cbse-g11-accountancy', 'full', 5, { traits: { base: 0.95, cgPenalty: {}, weak: {}, slip: 0.02 } }),
      S('cbse-g11-business', 'light', 3, { traits: { base: 0.85, cgPenalty: { C2: 0.08 }, weak: {} } }),
    ],
    traits: T({ base: 0.84, spread: 0.05, slip: 0.04, blank: 0, overconf: 0.05, growth: 0.07, speed: 0.85, doneRate: 0.9, cgPenalty: { C2: 0.24 },
      weak: { 'cbse-g11-economics-ch05-st2': 0.42, 'cbse-g11-economics-ch05-st3': 0.45, 'cbse-g11-economics-ch06-st1': 0.42 } }),
    parent: { id: 'par_farida_khan', name: 'Farida Khan', relation: 'mother' },
    persona: { story: 'Strong in Accountancy; learns Economics by rote. Choosing between CA and Data Analyst.', order: 9, programme: 'CBSE Commerce' },
    profile: { p31: 2, p178: 150000, p180: 600000, p193: 'Laptop + broadband', p200: 'CEI', p212: 'C1', p230: 2, p163: 4, p268: 3 },
  }),
  make({
    s: { id: 'lrn_arjun_nair', firstName: 'Arjun', lastName: 'Nair', board: 'ib', grade: 11, stream: 'humanities', programme: 'IB Diploma Year 1 (Humanities)', school: 'Choice International School', city: 'Kochi', band: 'average', plan: 'free',
      counsellorIds: ['csl_heena_qureshi', 'csl_farah_siddiqui'], mentorIds: ['mnt_kelvin_thomas'], weeklyHours: 10, goal: 'Law: CLAT in India or an LLB in the UK', currentChapterIds: ['ib-g11-political-science-ch05'], profileCompletionPct: 68, sectionIds: ['sec-ib-g11-economics-a'] },
    seed: 'v1',
    start: TERM_START,
    subjects: [
      S('ib-g11-political-science', 'full', 4),
      S('ib-g11-history', 'full', 4, { traits: { base: 0.86 } }),
      S('ib-g11-economics', 'full', 4, { traits: { base: 0.66, cgPenalty: { C3: 0.06, C4: 0.2 } } }),
      S('ib-g11-english', 'light', 3, { traits: { base: 0.93, cgPenalty: {} } }),
    ],
    // writes well, argues less well: transfer / evaluation items (C4) are the gap
    traits: T({ base: 0.84, spread: 0.08, slip: 0.04, overconf: 0.1, growth: 0.04, speed: 0.95, doneRate: 0.75, cgPenalty: { C4: 0.24 } }),
    parent: { id: 'par_rajesh_nair', name: 'Rajesh Nair', relation: 'father' },
    persona: { story: 'Uneven marks, strong writer; wants Law (CLAT in India vs a UK LLB); reasoning gaps in evaluation questions.', order: 10, programme: 'IB DP 1 Humanities' },
    profile: { p31: 2, p178: 300000, p180: 800000, p181: 6000000, p193: 'Laptop + broadband', p212: 'C2', p230: 4, p163: 3, p268: 4, p200: 'SEA' },
  }),
  // ------------------------------------------------------------ grade 12
  make({
    s: { id: 'lrn_diya_sharma', firstName: 'Diya', lastName: 'Sharma', board: 'cbse', grade: 12, stream: 'science', programme: 'CBSE Class 12 Science (PCB)', school: 'Maharaja Sawai Man Singh Vidyalaya', city: 'Jaipur', band: 'average', plan: 'free',
      weeklyHours: 16, goal: 'NEET 2027: MBBS at a government college', currentChapterIds: ['cbse-g12-biology-ch08'], profileCompletionPct: 75, tutorIds: ['tut_fatima_sheikh'],
      availability: avail(['17:00', '21:30'], ['09:00', '13:00'], ['09:00', '12:00']) },
    start: CBSE_START,
    subjects: [
      S('cbse-g12-biology', 'full', 7, { traits: { base: 0.86 }, mocks: [['2026-09-05', 1], ['2026-09-26', 2], ['2026-10-17', 3], ['2026-11-07', 4]] }),
      S('cbse-g12-chemistry', 'full', 5, { traits: { base: 0.8, forget: 0.28 }, mocks: [['2026-09-05', 1], ['2026-09-26', 2], ['2026-10-17', 3], ['2026-11-07', 4]] }),
      S('cbse-g12-physics', 'full', 6, { traits: { base: 0.74, spread: 0.1 }, mocks: [['2026-09-05', 1], ['2026-09-26', 2], ['2026-10-17', 3], ['2026-11-07', 4]] }),
    ],
    // inconsistent: wide spread and slips that grow when she sleeps badly before tests
    traits: T({ base: 0.8, spread: 0.09, slip: [['2026-09-01', 0.05], ['2026-10-20', 0.12], ['2026-11-17', 0.09]], overconf: 0, growth: 0.05, speed: 1.05, doneRate: 0.8, forget: 0.1, prior: 0.45 }),
    parent: { id: 'par_kavita_sharma', name: 'Kavita Sharma', relation: 'mother' },
    persona: { story: 'NEET aspirant: 4 of 6 mocks done, scores swing; retention dips. Low sleep flagged privately, support only.', order: 11, programme: 'CBSE Science (PCB)' },
    profile: { p31: 5, p178: 200000, p180: 1200000, p193: 'Laptop + broadband', p212: 'B2', p230: 1, p163: 4, p150: 3, p25: 'NEET mocks: 512, 468, 541, 497 /720', p200: 'ISR' },
    t3: { p83: 5.2, p84: 2, p87: 'Most days', p88: 'Sleeps under 5 hours before tests', p111: 'Moderate' },
  }),
  make({
    s: { id: 'lrn_nikhil_reddy', firstName: 'Nikhil', lastName: 'Reddy', board: 'cambridge', grade: 12, stream: 'commerce', programme: 'Cambridge A Level (Commerce)', school: 'Oakridge International School', city: 'Hyderabad', band: 'average', plan: 'application_support',
      counsellorIds: ['csl_farah_siddiqui', 'csl_heena_qureshi'], weeklyHours: 10, goal: 'BSc Business in the UK or Canada', currentChapterIds: ['cambridge-g12-business-ch04'], profileCompletionPct: 81 },
    start: TERM_START,
    subjects: [S('cambridge-g12-business', 'full', 3), S('cambridge-g12-accountancy', 'light', 3, { traits: { base: 0.84 } }), S('cambridge-g12-economics', 'light', 3)],
    traits: T({ base: 0.8, spread: 0.06, slip: 0.06, overconf: 0.05, growth: 0.06, speed: 0.95, doneRate: 0.8 }),
    parent: { id: 'par_lakshmi_reddy', name: 'Lakshmi Reddy', relation: 'mother' },
    persona: { story: 'Average student, full Application Support subscriber applying to UK and Canada business programmes.', order: 12, programme: 'Cambridge A Level' },
    profile: { p16: 'AAB predicted', p25: 'SAT not taken', p212: 'IELTS 7.0', p268: 3, p178: 900000, p181: 9000000, p230: 5, p31: 2 },
  }),
  make({
    s: { id: 'lrn_tara_menon', firstName: 'Tara', lastName: 'Menon', board: 'ib', grade: 12, stream: 'science', programme: 'IB Diploma Year 2 (Sciences)', school: 'Canadian International School', city: 'Bengaluru', band: 'above_avg', plan: 'application_support',
      counsellorIds: ['csl_heena_qureshi', 'csl_farah_siddiqui'], weeklyHours: 10, goal: 'Computer Science in the US or Canada', currentChapterIds: ['ib-g12-computer-science-ch05'], profileCompletionPct: 86 },
    start: TERM_START,
    subjects: [
      S('ib-g12-computer-science', 'full', 4, { traits: { base: 0.95, slip: 0.02 } }),
      S('ib-g12-maths', 'full', 4, { traits: { base: 0.86 } }),
      S('ib-g12-english', 'full', 3, { traits: { base: 0.78, cgPenalty: { C4: 0.22 }, typePenalty: { long: 0.15 } } }),
      S('ib-g12-physics', 'light', 3),
    ],
    traits: T({ base: 0.86, spread: 0.04, slip: 0.03, growth: 0.06, speed: 0.8, doneRate: 0.85, prior: 0.6 }),
    parent: { id: 'par_lata_menon', name: 'Lata Menon', relation: 'mother' },
    persona: { story: 'Builds apps; applying to Computer Science in the US and Canada with code projects as her portfolio; essays need work.', order: 13, programme: 'IB DP 2 Sciences' },
    profile: { p16: 'IB 41/45 predicted', p25: 'SAT 1490 (superscore)', p212: 'Duolingo 140', p268: 5, p178: 800000, p181: 15000000, p230: 5, p31: 2.5, p200: 'IRE' },
  }),
  make({
    s: { id: 'lrn_kunal_verma', firstName: 'Kunal', lastName: 'Verma', board: 'cbse', grade: 12, stream: 'humanities', programme: 'CBSE Class 12 Humanities', school: 'City Montessori School, Gomti Nagar', city: 'Lucknow', band: 'below_avg', plan: 'free',
      mentorIds: ['mnt_kelvin_thomas'], weeklyHours: 9, goal: 'Law or civil services, using debating', currentChapterIds: ['cbse-g12-history-ch07'], profileCompletionPct: 64, medium: 'English (moved from Hindi medium in Class 11)', tutorIds: ['tut_farhan_ali'] },
    seed: 'v2',
    start: CBSE_START,
    subjects: [
      S('cbse-g12-history', 'full', 6),
      S('cbse-g12-political-science', 'full', 6, { traits: { base: 0.76 } }),
      S('cbse-g12-english', 'full', 4, { traits: { base: 0.66 } }),
      S('cbse-g12-geography', 'light', 3),
    ],
    // understands the ideas (MCQ fine) but long written answers in English lose marks: G7 language
    traits: T({ base: 0.74, spread: 0.06, slip: 0.05, overconf: 0.05, growth: [['2026-09-30', 0.02], ['2026-10-01', 0.045]], speed: 1.1, doneRate: 0.7, prior: 0.8,
      typePenalty: { long: 0.4, case: 0.38, multi_step: 0.38, explain: 0.25 } }),
    parent: { id: 'par_alok_verma', name: 'Alok Verma', relation: 'father' },
    persona: { story: 'Weak marks but a strong debater and leader; moved from Hindi medium, so written English costs him (G7). Careers from his strengths.', order: 14, programme: 'CBSE Humanities' },
    profile: { p31: 2, p178: 90000, p180: 300000, p193: 'Phone + broadband', p212: 'B1', p157: ['Hindi', 'English'], p230: 1, p163: 3, p150: 4, p268: 5, p200: 'ESA' },
  }),
];

/** Zoya signed up today: account, parent and consent only (the live demo fills the rest). */
export const ZOYA = {
  student: student({ id: 'lrn_zoya_fernandes', firstName: 'Zoya', lastName: 'Fernandes', board: 'cbse', grade: 9, stream: 'none', programme: 'CBSE Class 9', school: 'Carmel Convent School', city: 'Mumbai', band: 'average', plan: 'free',
    joinedUtc: '2026-11-18T03:10:00.000Z', profileCompletionPct: 8, story: 'Signed up today; onboarding test not taken yet (live demo).', parentIds: ['par_maria_fernandes'], weeklyHours: 6, availability: [] }, []),
  parent: { id: 'par_maria_fernandes', name: 'Maria Fernandes', relation: 'mother' as const },
  persona: { story: 'Signed up today; onboarding test not taken yet (live demo).', order: 2, programme: 'CBSE Class 9' },
};
