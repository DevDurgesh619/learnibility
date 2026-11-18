import type {
  AvailabilitySlot,
  HelpType,
  SessionFormat,
  SessionMode,
  TeachingStyle,
  Tutor,
  TutorAudience,
  TutorReview,
  TutorSubject,
  Weekday,
} from '../../../lib/types/catalogue';
import type { Board, Grade } from '../../../lib/types/enums';

// ------------------------------------------------------------ availability presets (IST)
const WEEKDAYS: Weekday[] = ['mon', 'tue', 'wed', 'thu', 'fri'];
const slot = (day: Weekday, start: string, end: string): AvailabilitySlot => ({ day, start, end });
const each = (days: Weekday[], start: string, end: string) => days.map((d) => slot(d, start, end));

const AVAIL = {
  /** Rahul Verma, as drawn in the tutor wireframes 1e/8c. */
  rahul: [...each(WEEKDAYS, '16:00', '19:00'), ...each(['mon', 'wed', 'fri'], '19:00', '22:00'), slot('sat', '07:00', '10:00'), slot('sat', '10:00', '13:00')],
  evenings: [...each(WEEKDAYS, '17:00', '21:00'), slot('sat', '10:00', '13:00')],
  lateEvenings: [...each(WEEKDAYS, '19:00', '22:00'), slot('sun', '10:00', '13:00')],
  afternoons: [...each(WEEKDAYS, '14:00', '18:00'), slot('sat', '14:00', '17:00')],
  weekends: [slot('sat', '09:00', '13:00'), slot('sat', '15:00', '19:00'), slot('sun', '09:00', '13:00'), slot('sun', '15:00', '18:00'), slot('wed', '19:00', '21:00')],
  mornings: [...each(WEEKDAYS, '06:30', '08:30'), ...each(['tue', 'thu'], '18:00', '21:00'), slot('sun', '08:00', '12:00')],
  fullDay: [...each(WEEKDAYS, '10:00', '13:00'), ...each(WEEKDAYS, '16:00', '20:00'), slot('sat', '10:00', '18:00')],
  /** Abroad-based tutors teaching Indian evenings from the UK / Dubai morning-afternoon. */
  gulf: [...each(WEEKDAYS, '18:30', '21:30'), slot('sat', '11:00', '15:00'), slot('sun', '11:00', '15:00')],
} satisfies Record<string, AvailabilitySlot[]>;

// ------------------------------------------------------------ helpers
const G8_10: Grade[] = [8, 9, 10];
const G9_12: Grade[] = [9, 10, 11, 12];
const G11_12: Grade[] = [11, 12];
const ALL_G: Grade[] = [8, 9, 10, 11, 12];
const ALL_B: Board[] = ['cbse', 'cambridge', 'ib'];

const sub = (subjectSlug: string, boards: Board[], grades: Grade[], topicStrengths: string[]): TutorSubject => ({ subjectSlug, boards, grades, topicStrengths });
const rv = (author: string, rating: TutorReview['rating'], text: string, date: string): TutorReview => ({ author, rating, text, date });

interface T {
  first: string;
  last: string;
  gender: 'female' | 'male';
  city: string;
  tz?: string;
  headline: string;
  bio: string;
  quals: string[];
  years: number;
  subjects: TutorSubject[];
  exams?: string[];
  audiences: TutorAudience[];
  help: HelpType[];
  styles: TeachingStyle[];
  formats: SessionFormat[];
  modes: SessionMode[];
  offlineArea?: string;
  langs: string[];
  homework?: Tutor['homework'];
  ideal: string;
  avail: AvailabilitySlot[];
  minutes?: Tutor['sessionMinutes'];
  maxPerDay?: number;
  price: number;
  group?: number | null;
  groupSize?: [number, number];
  demo?: number;
  packages?: { label: string; sessions: number; priceInr: number }[];
  rating: number;
  reviewsCount: number;
  rebook: number;
  sessions: number;
  response: number;
  verified?: boolean | 'pending';
  joined: string;
  strength: number;
  reviews: TutorReview[];
}

function t(x: T): Tutor {
  const verified = x.verified === undefined ? true : x.verified === true;
  const pending = x.verified === 'pending';
  const group = x.group === undefined ? null : x.group;
  const formats = x.formats;
  // Default monthly package: 8 sessions at about 6% off, rounded to ₹100.
  const packages = x.packages ?? [{ label: '8 sessions / month', sessions: 8, priceInr: Math.round((x.price * 8 * 0.94) / 100) * 100 }];
  return {
    id: `tut_${x.first.toLowerCase()}_${x.last.toLowerCase().replace(/[^a-z]/g, '')}`,
    firstName: x.first,
    lastName: x.last,
    displayName: `${x.first} ${x.last}`,
    gender: x.gender,
    city: x.city,
    timeZone: x.tz ?? 'Asia/Kolkata',
    headline: x.headline,
    bio: x.bio,
    qualifications: x.quals,
    yearsExperience: x.years,
    subjects: x.subjects,
    examPrep: x.exams ?? [],
    audiences: x.audiences,
    helpTypes: x.help,
    teachingStyles: x.styles,
    formats,
    modes: x.modes,
    ...(x.offlineArea ? { offlineArea: x.offlineArea } : {}),
    languages: x.langs,
    homework: x.homework ?? 'every_session',
    idealStudent: x.ideal,
    availability: x.avail,
    sessionMinutes: x.minutes ?? 60,
    maxSessionsPerDay: x.maxPerDay ?? 4,
    pricing: {
      oneToOnePerHourInr: x.price,
      groupPerStudentPerHourInr: formats.includes('group') ? group : null,
      groupSize: formats.includes('group') ? (x.groupSize ?? [3, 6]) : null,
      demoInr: x.demo ?? 0,
      demoMinutes: 30,
      packages,
    },
    platformFeeRate: 0.15,
    rating: x.rating,
    reviewsCount: x.reviewsCount,
    rebookPct: x.rebook,
    sessionsCompleted: x.sessions,
    responseTimeHours: x.response,
    verified,
    verification: { identity: true, qualification: verified, experience: verified && x.years >= 3 && !pending },
    joinedOn: x.joined,
    profileStrengthPct: x.strength,
    reviews: x.reviews,
  };
}

export const TUTORS: Tutor[] = [
  // ============================================================ Maths and Physics
  t({
    first: 'Rahul', last: 'Verma', gender: 'male', city: 'Delhi',
    headline: 'Maths and Physics · Class 9-12 · JEE · concept-first',
    bio: 'I have taught mathematics and physics for 6 years, mostly Class 9-12 students preparing for JEE. I start every topic from first principles, then move to exam problems once the idea clicks.',
    quals: ['B.Tech, Delhi Technological University', 'M.Sc Mathematics (IGNOU)'], years: 6,
    subjects: [
      sub('maths', ['cbse', 'cambridge'], G9_12, ['algebra', 'calculus', 'quadratic-equations', 'trigonometry', 'coordinate-geometry', 'probability']),
      sub('physics', ['cbse'], G9_12, ['laws-of-motion', 'rotational-motion', 'work-energy-power', 'gravitation', 'force-diagrams', 'kinematics']),
    ],
    exams: ['jee-main', 'jee-advanced'], audiences: ['school', 'competitive_exam'], help: ['concept_learning', 'exam_prep', 'homework'],
    styles: ['concept_first', 'exam_focused'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Hindi'],
    ideal: 'Class 11-12 students preparing for JEE who need concept-first help with Algebra, Calculus and Mechanics.',
    avail: AVAIL.rahul, price: 800, group: 350, demo: 0,
    packages: [{ label: '8 sessions / month', sessions: 8, priceInr: 6000 }],
    rating: 4.8, reviewsCount: 31, rebook: 92, sessions: 412, response: 3, joined: '2025-06-14', strength: 85,
    reviews: [
      rv("Aarav's parent", 5, 'Explains from basics, very patient.', '2026-09-02'),
      rv('Kabir, Class 9', 4, 'Great for JEE problem practice.', '2026-08-21'),
      rv("Sana's parent", 5, 'Rotational motion finally made sense to her after two sessions. Very organised.', '2026-10-11'),
    ],
  }),
  t({
    first: 'Neha', last: 'Kulkarni', gender: 'female', city: 'Pune',
    headline: 'Maths for Class 8-10 · fixes foundation gaps · CBSE and Cambridge',
    bio: 'Former maths teacher at a Pune CBSE school. I specialise in students who are scared of maths because of gaps from earlier classes: fractions, negative numbers and basic algebra.',
    quals: ['M.Sc Mathematics, Savitribai Phule Pune University', 'B.Ed'], years: 11,
    subjects: [sub('maths', ['cbse', 'cambridge'], G8_10, ['fractions', 'rational-numbers', 'linear-equations', 'exponents-and-powers', 'factorisation', 'mensuration', 'percentages', 'ratio'])],
    audiences: ['school'], help: ['concept_learning', 'homework'],
    styles: ['concept_first', 'socratic'], formats: ['one_to_one', 'group'], modes: ['online', 'offline'], offlineArea: 'Kothrud and Baner, Pune', langs: ['English', 'Hindi', 'Marathi'],
    ideal: 'Class 8-9 students who lost confidence in maths and need fraction and algebra basics rebuilt slowly.',
    avail: AVAIL.afternoons, price: 600, group: 250, demo: 0,
    rating: 4.9, reviewsCount: 58, rebook: 94, sessions: 960, response: 2, joined: '2024-11-03', strength: 100,
    reviews: [
      rv("Ishita's parent", 5, 'She went from avoiding maths homework to explaining fractions to her cousin. Neha is calm and never rushes.', '2026-10-28'),
      rv('Parent of a Class 8 student', 5, 'Diagnosed exactly where my son was stuck in the first demo.', '2026-07-15'),
    ],
  }),
  t({
    first: 'Arvind', last: 'Raghavan', gender: 'male', city: 'Chennai',
    headline: 'JEE Advanced Maths · ex-IIT Madras · problem-solving bootcamps',
    bio: 'IIT Madras alumnus who has coached JEE aspirants for 14 years. My sessions are dense problem-solving with timed sets and post-test analysis.',
    quals: ['B.Tech, IIT Madras'], years: 14,
    subjects: [sub('maths', ['cbse'], G11_12, ['calculus', 'complex-numbers', 'vectors-3d', 'permutations-combinations', 'probability', 'matrices', 'conic-sections'])],
    exams: ['jee-main', 'jee-advanced', 'bitsat'], audiences: ['competitive_exam'], help: ['exam_prep'],
    styles: ['practice_first', 'exam_focused'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Tamil'],
    ideal: 'Strong Class 11-12 students targeting a top-1,000 JEE Advanced rank who need speed and harder problems.',
    avail: AVAIL.lateEvenings, price: 1500, group: 600, demo: 300, groupSize: [4, 8],
    rating: 4.7, reviewsCount: 112, rebook: 81, sessions: 2100, response: 6, joined: '2024-08-20', strength: 95,
    reviews: [
      rv("Vihaan's parent", 5, 'Tough but worth it. Vihaan\'s mock percentile in maths went from 94 to 99.', '2026-10-05'),
      rv('JEE 2026 student', 4, 'Very fast pace. Not for beginners, but the problem sets are gold.', '2026-05-30'),
    ],
  }),
  t({
    first: 'Fatima', last: 'Sheikh', gender: 'female', city: 'Hyderabad',
    headline: 'Physics Class 9-12 · makes mechanics visual · CBSE and IGCSE',
    bio: 'I use simulations and sketches so students see physics before they calculate it. I taught IGCSE and CBSE physics at an international school for 8 years.',
    quals: ['M.Sc Physics, University of Hyderabad', 'Cambridge CIDTT'], years: 9,
    subjects: [sub('physics', ['cbse', 'cambridge'], G9_12, ['laws-of-motion', 'rotational-motion', 'electricity', 'magnetism', 'waves', 'thermal-physics', 'kinematics'])],
    exams: ['jee-main'], audiences: ['school', 'competitive_exam'], help: ['concept_learning', 'exam_prep'],
    styles: ['concept_first', 'socratic'], formats: ['one_to_one'], modes: ['online'], langs: ['English', 'Hindi', 'Urdu'],
    ideal: 'Students who can do the maths but cannot picture what is happening in mechanics and electricity.',
    avail: AVAIL.evenings, price: 900, demo: 0,
    rating: 4.9, reviewsCount: 44, rebook: 90, sessions: 620, response: 4, joined: '2025-01-09', strength: 100,
    reviews: [
      rv("Ananya's parent", 5, 'Excellent IGCSE preparation, very structured past-paper practice.', '2026-06-18'),
      rv('Class 11 student', 5, 'The simulations made torque click for me.', '2026-09-12'),
    ],
  }),
  t({
    first: 'Sandeep', last: 'Yadav', gender: 'male', city: 'Kota',
    headline: 'Physics for JEE and NEET · 10 years in Kota · daily practice sheets',
    bio: 'Ten years teaching physics at Kota coaching institutes. I focus on the question types that repeat every year and drill them until students are fast and accurate.',
    quals: ['M.Sc Physics, University of Rajasthan'], years: 10,
    subjects: [sub('physics', ['cbse'], G11_12, ['electrostatics', 'current-electricity', 'modern-physics', 'optics', 'laws-of-motion', 'rotational-motion'])],
    exams: ['jee-main', 'neet-ug'], audiences: ['competitive_exam'], help: ['exam_prep', 'homework'],
    styles: ['practice_first', 'exam_focused'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['Hindi', 'English'],
    ideal: 'NEET and JEE Main aspirants who understand the theory but lose marks on speed and silly errors.',
    avail: AVAIL.mornings, price: 700, group: 250, demo: 0, groupSize: [5, 10],
    rating: 4.6, reviewsCount: 87, rebook: 84, sessions: 1850, response: 5, joined: '2024-09-01', strength: 90,
    reviews: [
      rv("Diya's parent", 5, 'His daily sheets helped Diya get physics from 120 to 150 in mocks.', '2026-10-20'),
      rv('NEET 2026 aspirant', 4, 'Explains in Hindi which helped me a lot. Strict about homework.', '2026-04-14'),
    ],
  }),
  t({
    first: 'Priya', last: 'Menon', gender: 'female', city: 'Bengaluru',
    headline: 'IB Maths AA / AI and MYP · IA guidance · ex-international school',
    bio: 'IB maths teacher for 12 years at international schools in Bengaluru and Dubai. I help students with both exam technique and their maths Internal Assessment.',
    quals: ['M.Sc Mathematics, Christ University', 'IB Category 2 Maths workshops'], years: 12,
    subjects: [sub('maths', ['ib', 'cambridge'], ALL_G, ['functions', 'calculus', 'statistics', 'probability', 'algebra', 'trigonometry', 'internal-assessment'])],
    audiences: ['school'], help: ['concept_learning', 'exam_prep', 'homework'],
    styles: ['concept_first', 'exam_focused'], formats: ['one_to_one'], modes: ['online', 'offline'], offlineArea: 'Whitefield and Indiranagar, Bengaluru', langs: ['English', 'Malayalam'],
    ideal: 'IB MYP 4-5 and DP students in Maths AA SL/HL who want a 6 or 7 and a strong IA.',
    avail: AVAIL.evenings, price: 1400, demo: 0,
    rating: 4.9, reviewsCount: 39, rebook: 93, sessions: 540, response: 3, joined: '2025-03-22', strength: 100,
    reviews: [
      rv("Meera's parent", 5, 'Priya noticed Meera freezes in timed papers and built practice around that. Huge confidence boost.', '2026-10-02'),
      rv('IB DP2 student', 5, 'Helped me pick and structure my Maths IA topic.', '2026-08-30'),
    ],
  }),
  t({
    first: 'Rohit', last: 'Malhotra', gender: 'male', city: 'Chandigarh',
    headline: 'Class 9-10 Maths and Science · board exam specialist',
    bio: 'I run small online batches for CBSE Class 9-10 with weekly tests modelled on the board paper. Many of my students move from 60s to 80s in a year.',
    quals: ['B.Sc (Non-Medical), Panjab University', 'B.Ed'], years: 8,
    subjects: [
      sub('maths', ['cbse'], [9, 10], ['polynomials', 'linear-equations', 'quadratic-equations', 'triangles', 'statistics', 'surface-areas-and-volumes']),
      sub('science', ['cbse'], [9, 10], ['motion', 'force-and-laws-of-motion', 'chemical-reactions', 'electricity', 'life-processes']),
    ],
    audiences: ['school'], help: ['exam_prep', 'homework'],
    styles: ['exam_focused', 'practice_first'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['Hindi', 'English', 'Punjabi'],
    ideal: 'Class 10 board students scoring 50-70% who need structured weekly practice and accountability.',
    avail: AVAIL.evenings, price: 500, group: 200, demo: 0, groupSize: [5, 10],
    rating: 4.6, reviewsCount: 73, rebook: 86, sessions: 1320, response: 4, joined: '2024-10-15', strength: 90,
    reviews: [
      rv("Rohan's parent", 4, 'Regular tests and WhatsApp updates on attendance. Rohan is more regular now.', '2026-10-25'),
      rv('Class 10 student', 5, 'The board pattern tests made the real exam feel easy.', '2026-04-02'),
    ],
  }),
  t({
    first: 'Kavya', last: 'Iyer', gender: 'female', city: 'Mumbai',
    headline: 'Cambridge Lower Secondary and IGCSE Maths · patient with weak foundations',
    bio: 'Cambridge-trained maths teacher. I help Stage 8-9 and IGCSE students who find word problems and fractions confusing by building number sense first.',
    quals: ['B.Sc Mathematics, St Xavier\'s College Mumbai', 'Cambridge PDQ Teaching and Learning'], years: 7,
    subjects: [sub('maths', ['cambridge', 'ib'], [8, 9, 10], ['fractions', 'decimals', 'ratio-and-proportion', 'algebraic-expressions', 'number', 'word-problems'])],
    audiences: ['school'], help: ['concept_learning', 'homework'],
    styles: ['concept_first', 'socratic'], formats: ['one_to_one'], modes: ['online', 'offline'], offlineArea: 'Bandra to Andheri West, Mumbai', langs: ['English', 'Hindi', 'Tamil'],
    ideal: 'Cambridge Lower Secondary students who are strong readers but get lost in multi-step number problems.',
    avail: AVAIL.afternoons, price: 1000, demo: 0,
    rating: 4.8, reviewsCount: 26, rebook: 91, sessions: 310, response: 3, joined: '2025-07-01', strength: 95,
    reviews: [
      rv('Parent of a Stage 8 student', 5, 'Kavya uses fraction strips and drawings. My daughter finally understands why the rules work.', '2026-09-19'),
      rv('IGCSE student', 5, 'Very kind and very clear.', '2026-07-08'),
    ],
  }),
  t({
    first: 'Amit', last: 'Saxena', gender: 'male', city: 'Lucknow',
    headline: 'Maths Class 8-12 · Hindi and English medium · affordable small batches',
    bio: 'I teach maths bilingually, which helps students moving from Hindi-medium to English-medium schools. Small batches keep the fee low.',
    quals: ['M.Sc Mathematics, University of Lucknow', 'B.Ed'], years: 9,
    subjects: [sub('maths', ['cbse'], ALL_G, ['linear-equations', 'algebra', 'trigonometry', 'mensuration', 'statistics', 'number-systems'])],
    audiences: ['school'], help: ['concept_learning', 'homework', 'exam_prep'],
    styles: ['practice_first', 'concept_first'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['Hindi', 'English'],
    ideal: 'Students switching from Hindi to English medium who know the maths but stumble on the language of questions.',
    avail: AVAIL.evenings, price: 350, group: 150, demo: 0, groupSize: [4, 8],
    rating: 4.5, reviewsCount: 48, rebook: 82, sessions: 870, response: 5, joined: '2025-02-11', strength: 80,
    reviews: [
      rv('Class 12 student', 5, 'Bilingual explanations are a big help. Very affordable.', '2026-08-04'),
      rv('Parent', 4, 'Good teacher, the group is sometimes noisy.', '2026-06-22'),
    ],
  }),
  // ============================================================ Chemistry and Biology
  t({
    first: 'Meenakshi', last: 'Rao', gender: 'female', city: 'Bengaluru',
    headline: 'Chemistry for JEE and boards · retention-first revision plans',
    bio: 'Chemistry is mostly forgotten, not misunderstood. I use spaced revision, reaction maps and weekly recall quizzes so organic and inorganic stick until the exam.',
    quals: ['M.Sc Chemistry, Bangalore University', 'PhD (Organic Chemistry), IISc'], years: 13,
    subjects: [sub('chemistry', ['cbse', 'cambridge'], G11_12, ['organic-chemistry', 'reaction-mechanisms', 'chemical-bonding', 'p-block', 'thermodynamics', 'equilibrium', 'mole-concept'])],
    exams: ['jee-main', 'jee-advanced', 'neet-ug'], audiences: ['school', 'competitive_exam'], help: ['concept_learning', 'exam_prep'],
    styles: ['concept_first', 'practice_first'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Kannada', 'Hindi'],
    ideal: 'JEE aspirants strong in maths and physics who keep forgetting chemistry reactions and inorganic facts.',
    avail: AVAIL.evenings, price: 1200, group: 450, demo: 0,
    rating: 4.9, reviewsCount: 67, rebook: 95, sessions: 1100, response: 3, joined: '2024-08-28', strength: 100,
    reviews: [
      rv("Vihaan's parent", 5, 'Her revision schedule is exactly what Vihaan needed. Chemistry retention tests went from 55% to 85%.', '2026-10-30'),
      rv('JEE 2026 student', 5, 'Reaction maps are brilliant. Best organic teacher I have had.', '2026-05-12'),
    ],
  }),
  t({
    first: 'Deepak', last: 'Chauhan', gender: 'male', city: 'Jaipur',
    headline: 'Chemistry Class 9-12 · NCERT line-by-line for NEET and boards',
    bio: 'NEET chemistry is NCERT chemistry. I teach line by line from the textbook and test with previous-year NEET questions every week.',
    quals: ['M.Sc Chemistry, University of Rajasthan', 'B.Ed'], years: 10,
    subjects: [sub('chemistry', ['cbse'], G9_12, ['ncert-inorganic', 'organic-chemistry', 'biomolecules', 'coordination-compounds', 'solutions', 'chemical-kinetics'])],
    exams: ['neet-ug'], audiences: ['school', 'competitive_exam'], help: ['exam_prep', 'homework'],
    styles: ['exam_focused', 'practice_first'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['Hindi', 'English'],
    ideal: 'NEET aspirants who need a disciplined NCERT-first chemistry plan.',
    avail: AVAIL.mornings, price: 600, group: 220, demo: 0, groupSize: [5, 10],
    rating: 4.6, reviewsCount: 55, rebook: 83, sessions: 1050, response: 6, joined: '2024-12-02', strength: 85,
    reviews: [
      rv('NEET 2026 student', 5, 'NCERT-focused method works. Scored 165 in chemistry.', '2026-07-01'),
      rv("Diya's parent", 4, 'Good discipline. Sessions start early which suits Diya.', '2026-09-27'),
    ],
  }),
  t({
    first: 'Ananya', last: 'Bhattacharya', gender: 'female', city: 'Kolkata',
    headline: 'Biology for NEET and boards · diagrams, mnemonics and PYQs',
    bio: 'Biology needs memory plus understanding. I teach with hand-drawn diagrams, stories and mnemonics, then test with NEET previous-year questions.',
    quals: ['M.Sc Zoology, University of Calcutta', 'B.Ed'], years: 9,
    subjects: [sub('biology', ['cbse', 'cambridge'], G9_12, ['human-physiology', 'genetics', 'plant-physiology', 'cell-biology', 'ecology', 'reproduction', 'biotechnology'])],
    exams: ['neet-ug'], audiences: ['school', 'competitive_exam'], help: ['concept_learning', 'exam_prep'],
    styles: ['concept_first', 'exam_focused'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Bengali', 'Hindi'],
    ideal: 'NEET aspirants whose biology scores swing between mocks because of weak recall in physiology and genetics.',
    avail: AVAIL.evenings, price: 800, group: 300, demo: 0,
    rating: 4.8, reviewsCount: 61, rebook: 90, sessions: 980, response: 4, joined: '2024-10-01', strength: 95,
    reviews: [
      rv("Diya's parent", 5, 'Genetics was Diya\'s weak spot; three weeks with Ananya and her mock scores steadied.', '2026-10-14'),
      rv('Class 11 student', 5, 'Her diagrams are amazing. I remember them in the exam.', '2026-08-19'),
    ],
  }),
  t({
    first: 'Joseph', last: 'Mathew', gender: 'male', city: 'Kochi',
    headline: 'IB and IGCSE Biology and Chemistry · IA and EE supervisor',
    bio: 'I have supervised IB Biology Internal Assessments and Extended Essays for 10 years. I help students plan experiments and write like scientists.',
    quals: ['M.Sc Biotechnology, Cochin University', 'IB Biology examiner training'], years: 10,
    subjects: [
      sub('biology', ['ib', 'cambridge'], G9_12, ['cell-biology', 'genetics', 'ecology', 'human-physiology', 'internal-assessment', 'extended-essay']),
      sub('chemistry', ['ib', 'cambridge'], G9_12, ['stoichiometry', 'organic-chemistry', 'energetics', 'internal-assessment']),
    ],
    audiences: ['school'], help: ['concept_learning', 'exam_prep', 'skill_development'],
    styles: ['socratic', 'project_based'], formats: ['one_to_one'], modes: ['online'], langs: ['English', 'Malayalam'],
    ideal: 'IB DP students who need help designing and writing a strong Biology or Chemistry IA.',
    avail: AVAIL.lateEvenings, price: 1300, demo: 0,
    rating: 4.8, reviewsCount: 22, rebook: 88, sessions: 290, response: 5, joined: '2025-05-17', strength: 95,
    reviews: [
      rv('IB DP2 student', 5, 'My Bio IA went from a vague idea to a proper investigation. Got a 7.', '2026-07-21'),
      rv('IGCSE parent', 5, 'Very knowledgeable and calm.', '2026-03-09'),
    ],
  }),
  t({
    first: 'Sunita', last: 'Gupta', gender: 'female', city: 'Delhi',
    headline: 'Science Class 8-10 · CBSE · experiments at home',
    bio: 'I make science practical with kitchen experiments and short videos. Students learn the NCERT concepts and then explain them back to me.',
    quals: ['M.Sc Chemistry, Delhi University', 'B.Ed'], years: 15,
    subjects: [sub('science', ['cbse'], G8_10, ['chemical-reactions', 'acids-bases-salts', 'light', 'electricity', 'life-processes', 'force-and-pressure', 'cell'])],
    audiences: ['school'], help: ['concept_learning', 'homework'],
    styles: ['project_based', 'concept_first'], formats: ['one_to_one', 'group'], modes: ['online', 'offline'], offlineArea: 'South Delhi', langs: ['Hindi', 'English'],
    ideal: 'Curious Class 8-9 students who learn better by doing than by reading.',
    avail: AVAIL.afternoons, price: 500, group: 200, demo: 0,
    rating: 4.7, reviewsCount: 49, rebook: 87, sessions: 860, response: 3, joined: '2024-11-20', strength: 90,
    reviews: [
      rv("Aarav's parent", 5, 'Aarav loved the olympiad-style extension experiments.', '2026-08-10'),
      rv('Class 9 parent', 4, 'Very engaging, sometimes runs over time.', '2026-07-03'),
    ],
  }),
  // ============================================================ English and languages
  t({
    first: 'Grace', last: 'Fernandes', gender: 'female', city: 'Goa',
    headline: 'English writing and literature · essays that sound like you',
    bio: 'Twelve years teaching English at ICSE and IB schools in Goa. I coach students to write clear, honest essays, from board answers to college personal statements.',
    quals: ['MA English, Goa University', 'CELTA'], years: 12,
    subjects: [sub('english', ALL_B, ALL_G, ['essay-writing', 'literature', 'comprehension', 'creative-writing', 'grammar', 'personal-statement'])],
    exams: ['ielts', 'sat'], audiences: ['school', 'english_learners'], help: ['concept_learning', 'skill_development'],
    styles: ['socratic', 'concept_first'], formats: ['one_to_one'], modes: ['online'], langs: ['English', 'Konkani', 'Hindi'],
    ideal: 'Students who have ideas but whose writing is vague or too long, including college essay applicants.',
    avail: AVAIL.evenings, price: 1100, demo: 0,
    rating: 4.9, reviewsCount: 37, rebook: 92, sessions: 470, response: 3, joined: '2025-02-02', strength: 100,
    reviews: [
      rv("Tara's parent", 5, 'Tara\'s essays became sharper and more personal in a month.', '2026-10-21'),
      rv('IB DP1 student', 5, 'She asks questions until you find your own argument.', '2026-08-02'),
    ],
  }),
  t({
    first: 'Imran', last: 'Qureshi', gender: 'male', city: 'Bhopal',
    headline: 'Spoken English and English-medium transition · Hindi explanations',
    bio: 'I help students coming from Hindi-medium schools speak and write English with confidence. We practise board answers, presentations and everyday conversation.',
    quals: ['MA English, Barkatullah University', 'TESOL certificate'], years: 8,
    subjects: [sub('english', ['cbse'], ALL_G, ['grammar', 'spoken-english', 'answer-writing', 'vocabulary', 'reading-comprehension'])],
    exams: ['ielts'], audiences: ['school', 'english_learners'], help: ['skill_development', 'homework'],
    styles: ['practice_first', 'socratic'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['Hindi', 'English', 'Urdu'],
    ideal: 'Class 11-12 students moving from Hindi to English medium who understand the subject but freeze when writing in English.',
    avail: AVAIL.lateEvenings, price: 450, group: 180, demo: 0,
    rating: 4.7, reviewsCount: 52, rebook: 89, sessions: 900, response: 4, joined: '2025-01-25', strength: 90,
    reviews: [
      rv("Kunal's parent", 5, 'Kunal now writes his History answers in English without translating in his head.', '2026-10-17'),
      rv('Class 12 student', 5, 'Very encouraging, explains grammar in Hindi.', '2026-06-11'),
    ],
  }),
  t({
    first: 'Rebecca', last: 'Thomas', gender: 'female', city: 'London', tz: 'Europe/London',
    headline: 'IELTS 7.5+ and UK applications · ex-British Council examiner',
    bio: 'Former IELTS examiner now based in London. I prepare students for IELTS Academic and help with UCAS personal statements.',
    quals: ['BA English Language, University of Leeds', 'DELTA', 'Former IELTS examiner'], years: 11,
    subjects: [sub('english', ALL_B, G11_12, ['ielts-writing', 'ielts-speaking', 'academic-writing', 'personal-statement'])],
    exams: ['ielts', 'toefl', 'pte'], audiences: ['english_learners', 'college'], help: ['exam_prep', 'skill_development'],
    styles: ['exam_focused', 'practice_first'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English'],
    ideal: 'Class 12 students applying to the UK, Canada or Australia who need IELTS 7.0+ in writing and speaking.',
    avail: AVAIL.gulf, price: 1500, group: 600, demo: 300,
    rating: 4.8, reviewsCount: 29, rebook: 85, sessions: 380, response: 8, joined: '2025-04-04', strength: 95,
    reviews: [
      rv("Nikhil's parent", 5, 'Nikhil moved from 6.5 to 7.5 overall in five weeks.', '2026-09-30'),
      rv('Class 12 student', 4, 'Expensive but very precise feedback on writing.', '2026-08-14'),
    ],
  }),
  t({
    first: 'Pooja', last: 'Tiwari', gender: 'female', city: 'Varanasi',
    headline: 'Hindi Class 8-12 · CBSE Hindi A and B · grammar and lekhan',
    bio: 'I teach CBSE Hindi with a focus on vyakaran and lekhan, using previous board papers and simple formats for letters, essays and notices.',
    quals: ['MA Hindi, Banaras Hindu University', 'B.Ed'], years: 10,
    subjects: [sub('hindi', ['cbse'], ALL_G, ['vyakaran', 'lekhan', 'kavya', 'gadya', 'patra-lekhan'])],
    audiences: ['school'], help: ['exam_prep', 'homework'],
    styles: ['exam_focused', 'practice_first'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['Hindi', 'English'],
    ideal: 'CBSE students who lose easy marks in Hindi grammar and writing sections.',
    avail: AVAIL.evenings, price: 400, group: 150, demo: 0,
    rating: 4.7, reviewsCount: 33, rebook: 86, sessions: 610, response: 4, joined: '2025-03-01', strength: 85,
    reviews: [
      rv('Class 10 parent', 5, 'My daughter scored 94 in Hindi. Very good formats for letter and essay.', '2026-05-28'),
      rv('Class 9 student', 4, 'Explains kavya meanings nicely.', '2026-08-25'),
    ],
  }),
  // ============================================================ Commerce
  t({
    first: 'Harish', last: 'Agarwal', gender: 'male', city: 'Kolkata',
    headline: 'Accountancy Class 11-12 and CA Foundation · Chartered Accountant',
    bio: 'Practising CA who has taught accountancy for 9 years. I teach the logic behind every entry so students stop memorising formats.',
    quals: ['Chartered Accountant (ICAI)', 'B.Com (Hons), St Xavier\'s College Kolkata'], years: 9,
    subjects: [
      sub('accountancy', ['cbse', 'cambridge'], G11_12, ['partnership-accounts', 'company-accounts', 'financial-statements', 'ratio-analysis', 'cash-flow-statement', 'journal-and-ledger']),
      sub('business', ['cbse'], G11_12, ['financial-management', 'business-finance']),
    ],
    exams: ['ca-foundation'], audiences: ['school', 'competitive_exam'], help: ['concept_learning', 'exam_prep'],
    styles: ['concept_first', 'practice_first'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Hindi', 'Bengali'],
    ideal: 'Commerce students aiming for CA who want accountancy to make sense, not just be memorised.',
    avail: AVAIL.lateEvenings, price: 900, group: 350, demo: 0,
    rating: 4.8, reviewsCount: 46, rebook: 91, sessions: 720, response: 4, joined: '2024-12-10', strength: 95,
    reviews: [
      rv("Sara's parent", 5, 'Sara already liked accountancy; Harish sir gave her a clear plan for CA Foundation.', '2026-09-08'),
      rv('Class 12 student', 5, 'Partnership accounts finally make sense.', '2026-02-16'),
    ],
  }),
  t({
    first: 'Nandini', last: 'Bose', gender: 'female', city: 'Delhi',
    headline: 'Economics Class 11-12 and A Level · understand, don\'t memorise',
    bio: 'Delhi School of Economics graduate. I teach economics through real Indian examples, diagrams and why-questions so students can handle any case-based question.',
    quals: ['MA Economics, Delhi School of Economics'], years: 7,
    subjects: [sub('economics', ['cbse', 'cambridge', 'ib'], G11_12, ['microeconomics', 'macroeconomics', 'national-income', 'money-and-banking', 'elasticity', 'market-structures', 'indian-economy'])],
    exams: ['cuet-ug'], audiences: ['school'], help: ['concept_learning', 'exam_prep'],
    styles: ['concept_first', 'socratic'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Hindi', 'Bengali'],
    ideal: 'Commerce students who memorise economics definitions but cannot apply them to case questions.',
    avail: AVAIL.evenings, price: 850, group: 320, demo: 0,
    rating: 4.9, reviewsCount: 34, rebook: 93, sessions: 450, response: 3, joined: '2025-02-19', strength: 100,
    reviews: [
      rv("Sara's parent", 5, 'Exactly what Sara needed: she now explains macro with diagrams instead of reciting notes.', '2026-10-26'),
      rv('A Level student', 5, 'Great evaluation practice for 12-mark questions.', '2026-06-05'),
    ],
  }),
  t({
    first: 'Vikram', last: 'Singhania', gender: 'male', city: 'Mumbai',
    headline: 'Business Studies and A Level Business · case-study method · ex-consultant',
    bio: 'Former management consultant who now teaches Business at A Level, IB and CBSE using real Indian company cases.',
    quals: ['MBA, IIM Ahmedabad', 'B.Com, Narsee Monjee College'], years: 6,
    subjects: [
      sub('business', ['cambridge', 'ib', 'cbse'], G11_12, ['marketing', 'finance-and-accounts', 'operations', 'strategy', 'case-study', 'human-resources']),
      sub('economics', ['cambridge'], G11_12, ['microeconomics', 'market-failure']),
    ],
    audiences: ['school', 'career_learners'], help: ['concept_learning', 'exam_prep', 'skill_development'],
    styles: ['project_based', 'socratic'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Hindi', 'Gujarati'],
    ideal: 'A Level and IB Business students who want top marks on evaluation and a head start on business-school interviews.',
    avail: AVAIL.weekends, price: 1400, group: 500, demo: 0,
    rating: 4.7, reviewsCount: 19, rebook: 84, sessions: 240, response: 6, joined: '2025-06-30', strength: 90,
    reviews: [
      rv("Nikhil's parent", 5, 'Helped Nikhil link his A Level Business to his UK applications.', '2026-10-09'),
      rv('IB DP1 student', 4, 'Real cases make it interesting.', '2026-08-28'),
    ],
  }),
  t({
    first: 'Sneha', last: 'Joshi', gender: 'female', city: 'Ahmedabad',
    headline: 'Applied Maths and Statistics for Commerce · CUET and IPMAT quant',
    bio: 'I teach applied maths and statistics to commerce students and prepare them for CUET and IPMAT quantitative sections.',
    quals: ['M.Sc Statistics, Gujarat University'], years: 6,
    subjects: [
      sub('applied-maths', ['cbse'], G11_12, ['statistics', 'probability', 'financial-mathematics', 'linear-programming', 'index-numbers']),
      sub('maths', ['cbse'], G11_12, ['statistics', 'probability']),
    ],
    exams: ['cuet-ug', 'ipmat-indore'], audiences: ['school', 'competitive_exam'], help: ['exam_prep', 'concept_learning'],
    styles: ['practice_first', 'exam_focused'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Gujarati', 'Hindi'],
    ideal: 'Commerce students targeting IPM or top DU colleges who need quant speed.',
    avail: AVAIL.evenings, price: 700, group: 280, demo: 0,
    rating: 4.6, reviewsCount: 24, rebook: 85, sessions: 350, response: 5, joined: '2025-05-05', strength: 85,
    reviews: [
      rv('IPMAT aspirant', 5, 'Shortcuts plus proper understanding. Got an IIM Indore interview call.', '2026-06-20'),
      rv('Class 11 parent', 4, 'Good structure and mock tests.', '2026-09-02'),
    ],
  }),
  // ============================================================ Humanities
  t({
    first: 'Ritu', last: 'Saxena', gender: 'female', city: 'Delhi',
    headline: 'History and Political Science · CBSE and IB · source-based answers',
    bio: 'I teach history as argument, not dates. Students learn to read sources, build answers and connect events to today.',
    quals: ['MA History, Jawaharlal Nehru University', 'B.Ed'], years: 12,
    subjects: [
      sub('history', ['cbse', 'ib'], G9_12, ['modern-india', 'world-wars', 'colonialism', 'source-analysis', 'nationalism']),
      sub('political-science', ['cbse'], G11_12, ['indian-constitution', 'federalism', 'international-relations', 'cold-war']),
      sub('social-science', ['cbse'], [9, 10], ['nationalism-in-india', 'democratic-politics', 'french-revolution']),
    ],
    exams: ['cuet-ug'], audiences: ['school', 'competitive_exam'], help: ['concept_learning', 'exam_prep'],
    styles: ['socratic', 'concept_first'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Hindi'],
    ideal: 'Humanities students who know the content but write descriptive, unstructured answers.',
    avail: AVAIL.evenings, price: 700, group: 260, demo: 0,
    rating: 4.8, reviewsCount: 41, rebook: 90, sessions: 690, response: 4, joined: '2024-12-18', strength: 95,
    reviews: [
      rv("Kunal's parent", 5, 'Ma\'am turned Kunal\'s debating skill into structured written answers.', '2026-09-24'),
      rv('IB History student', 5, 'Source analysis practice was excellent.', '2026-05-15'),
    ],
  }),
  t({
    first: 'Aditya', last: 'Narayan', gender: 'male', city: 'Bengaluru',
    headline: 'CLAT and LNAT coaching · legal and logical reasoning · NLSIU alumnus',
    bio: 'NLSIU graduate and former associate at a Mumbai law firm. I coach CLAT, AILET and LNAT with daily reading, reasoning drills and full mocks.',
    quals: ['BA LLB (Hons), NLSIU Bengaluru'], years: 5,
    subjects: [
      sub('legal-studies', ['cbse', 'ib'], G11_12, ['legal-reasoning', 'constitutional-law', 'contracts', 'torts']),
      sub('english', ['cbse', 'ib'], G11_12, ['reading-comprehension', 'critical-reasoning', 'argument-essay']),
    ],
    exams: ['clat', 'ailet', 'lnat'], audiences: ['competitive_exam'], help: ['exam_prep', 'skill_development'],
    styles: ['practice_first', 'socratic'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Hindi', 'Kannada'],
    ideal: 'Class 11-12 students aiming for a top-5 NLU or a UK law school who read well but reason slowly.',
    avail: AVAIL.lateEvenings, price: 1200, group: 450, demo: 0,
    rating: 4.8, reviewsCount: 36, rebook: 89, sessions: 520, response: 4, joined: '2025-01-15', strength: 95,
    reviews: [
      rv("Arjun's parent", 5, 'Arjun writes beautifully but rushed reasoning. Aditya fixed his approach to logical reasoning in a month.', '2026-10-12'),
      rv('CLAT 2026 student', 5, 'Mocks with detailed analysis. Got NALSAR.', '2026-01-20'),
    ],
  }),
  t({
    first: 'Shalini', last: 'Pillai', gender: 'female', city: 'Thiruvananthapuram',
    headline: 'Geography and Environmental Systems · maps, data and fieldwork',
    bio: 'Geography teacher who loves maps and data. I teach CBSE and IB geography with real datasets and map practice.',
    quals: ['MA Geography, University of Kerala', 'B.Ed'], years: 10,
    subjects: [
      sub('geography', ['cbse', 'ib'], G9_12, ['climate', 'resources-and-development', 'population', 'map-work', 'landforms']),
      sub('environmental', ['ib', 'cambridge'], G11_12, ['ecosystems', 'climate-change', 'sustainability']),
    ],
    audiences: ['school'], help: ['concept_learning', 'exam_prep'],
    styles: ['project_based', 'concept_first'], formats: ['one_to_one'], modes: ['online'], langs: ['English', 'Malayalam'],
    ideal: 'Students who find geography dry and would enjoy data and map-based learning.',
    avail: AVAIL.afternoons, price: 600, demo: 0,
    rating: 4.7, reviewsCount: 18, rebook: 87, sessions: 260, response: 5, joined: '2025-07-12', strength: 90,
    reviews: [
      rv('Class 9 parent', 5, 'Map work marks went up immediately.', '2026-09-10'),
      rv('IB ESS student', 4, 'Good case studies.', '2026-04-03'),
    ],
  }),
  t({
    first: 'Rachel', last: 'Dsouza', gender: 'female', city: 'Mumbai',
    headline: 'Psychology Class 11-12 and IB · research methods made easy',
    bio: 'Counselling psychologist who teaches CBSE and IB Psychology part-time. I connect theories to real life and teach research methods step by step.',
    quals: ['MA Clinical Psychology, Mumbai University', 'RCI registered'], years: 6,
    subjects: [sub('psychology', ['cbse', 'ib'], G11_12, ['research-methods', 'biological-approach', 'cognitive-approach', 'developmental-psychology', 'abnormal-psychology'])],
    audiences: ['school'], help: ['concept_learning', 'exam_prep'],
    styles: ['socratic', 'concept_first'], formats: ['one_to_one'], modes: ['online'], langs: ['English', 'Hindi', 'Konkani'],
    ideal: 'Students curious about psychology as a career who want strong board or IB results.',
    avail: AVAIL.weekends, price: 800, demo: 0,
    rating: 4.9, reviewsCount: 15, rebook: 92, sessions: 180, response: 6, joined: '2025-08-01', strength: 95,
    reviews: [
      rv('IB DP2 student', 5, 'Research methods finally make sense.', '2026-05-22'),
      rv('Class 12 parent', 5, 'Kind and knowledgeable.', '2026-09-15'),
    ],
  }),
  t({
    first: 'Manish', last: 'Pandey', gender: 'male', city: 'Patna',
    headline: 'Social Science Class 8-10 · Hindi and English · board answer writing',
    bio: 'I help CBSE Class 8-10 students master history, geography, civics and economics with maps, timelines and answer-writing practice.',
    quals: ['MA Political Science, Patna University', 'B.Ed'], years: 8,
    subjects: [sub('social-science', ['cbse'], G8_10, ['nationalism-in-india', 'resources-and-development', 'democratic-politics', 'money-and-credit', 'map-work'])],
    audiences: ['school'], help: ['exam_prep', 'homework'],
    styles: ['exam_focused', 'practice_first'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['Hindi', 'English'],
    ideal: 'Class 10 board students who find social science too long to revise.',
    avail: AVAIL.evenings, price: 300, group: 120, demo: 0, groupSize: [5, 12],
    rating: 4.5, reviewsCount: 40, rebook: 80, sessions: 760, response: 5, joined: '2025-04-20', strength: 80,
    reviews: [
      rv("Rohan's parent", 4, 'Affordable and regular. Rohan likes the short timeline notes.', '2026-10-01'),
      rv('Class 10 student', 5, 'Map practice helped a lot.', '2026-03-28'),
    ],
  }),
  // ============================================================ Computer science and skills
  t({
    first: 'Karthik', last: 'Subramanian', gender: 'male', city: 'Bengaluru',
    headline: 'Computer Science and Python · IB CS HL · app projects and portfolios',
    bio: 'Software engineer at a Bengaluru product company who teaches CS on weekends. I help students build real apps and portfolios for university applications.',
    quals: ['B.Tech Computer Science, NIT Trichy'], years: 7,
    subjects: [
      sub('computer-science', ['ib', 'cambridge', 'cbse'], G9_12, ['python', 'object-oriented-programming', 'algorithms', 'data-structures', 'internal-assessment', 'databases']),
      sub('informatics', ['cbse'], G11_12, ['python', 'pandas', 'sql']),
    ],
    audiences: ['school', 'career_learners'], help: ['skill_development', 'concept_learning'],
    styles: ['project_based', 'socratic'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Tamil', 'Kannada'],
    ideal: 'Students who code for fun and want projects strong enough for a CS application abroad.',
    avail: AVAIL.weekends, price: 1300, group: 500, demo: 0,
    rating: 4.9, reviewsCount: 27, rebook: 91, sessions: 330, response: 5, joined: '2025-03-08', strength: 100,
    reviews: [
      rv("Tara's parent", 5, 'Karthik helped Tara turn her app into a portfolio piece with a proper README and demo.', '2026-10-18'),
      rv('IB CS student', 5, 'My CS IA was the best in my class.', '2026-06-27'),
    ],
  }),
  t({
    first: 'Divya', last: 'Reddy', gender: 'female', city: 'Hyderabad',
    headline: 'Data analytics for teens · Excel, SQL, Python and Tableau',
    bio: 'Data analyst at a Hyderabad fintech. I run a 12-week analytics track for Class 11-12 students exploring data careers, built around real datasets.',
    quals: ['B.Tech, JNTU Hyderabad', 'Google Data Analytics certificate'], years: 4,
    subjects: [
      sub('informatics', ['cbse'], G11_12, ['sql', 'pandas', 'data-visualisation', 'spreadsheets']),
      sub('computer-science', ['cbse', 'cambridge'], G11_12, ['python', 'databases']),
    ],
    audiences: ['career_learners', 'school'], help: ['skill_development'],
    styles: ['project_based', 'practice_first'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Telugu', 'Hindi'],
    ideal: 'Commerce or science students curious about data analyst roles who want hands-on skills before college.',
    avail: AVAIL.weekends, price: 900, group: 350, demo: 0,
    packages: [{ label: '12-week analytics track (24 sessions)', sessions: 24, priceInr: 19500 }],
    rating: 4.8, reviewsCount: 21, rebook: 88, sessions: 260, response: 4, joined: '2025-06-05', strength: 95,
    reviews: [
      rv("Sara's parent", 5, 'Sara built a sales dashboard in Tableau in six weeks. Great for comparing CA with data careers.', '2026-10-07'),
      rv('Class 12 student', 5, 'Real datasets, not boring exercises.', '2026-07-30'),
    ],
  }),
  t({
    first: 'Farhan', last: 'Ali', gender: 'male', city: 'Lucknow',
    headline: 'Debate, public speaking and MUN coaching',
    bio: 'National-level debater and MUN trainer. I coach structured argument, rebuttal and confident delivery for debates, interviews and group discussions.',
    quals: ['BA (Hons) Political Science, Hindu College, Delhi University'], years: 5,
    subjects: [sub('english', ['cbse', 'ib', 'cambridge'], ALL_G, ['debate', 'public-speaking', 'mun', 'argument-essay'])],
    audiences: ['school', 'career_learners'], help: ['skill_development'],
    styles: ['practice_first', 'socratic'], formats: ['one_to_one', 'group'], modes: ['online', 'offline'], offlineArea: 'Gomti Nagar, Lucknow', langs: ['English', 'Hindi', 'Urdu'],
    ideal: 'Confident talkers who need structure, and shy students who want to find their voice.',
    avail: AVAIL.weekends, price: 700, group: 250, demo: 0,
    rating: 4.8, reviewsCount: 30, rebook: 87, sessions: 410, response: 4, joined: '2025-02-28', strength: 90,
    reviews: [
      rv("Kunal's parent", 5, 'Kunal won his first inter-school debate after joining.', '2026-08-23'),
      rv('Class 11 student', 5, 'MUN prep was excellent.', '2026-07-11'),
    ],
  }),
  t({
    first: 'Lakshmi', last: 'Narasimhan', gender: 'female', city: 'Chennai',
    headline: 'SAT Math and Reading · 1500+ strategy · US applications',
    bio: 'SAT coach for 9 years with students placed at Ivy League and top public universities. I diagnose each student\'s pattern of errors and build a plan around it.',
    quals: ['M.Sc Mathematics, IIT Madras', 'SAT 1580'], years: 9,
    subjects: [
      sub('maths', ALL_B, G9_12, ['sat-math', 'algebra', 'data-analysis', 'advanced-math']),
      sub('english', ALL_B, G9_12, ['sat-reading-writing', 'grammar', 'reading-comprehension']),
    ],
    exams: ['sat', 'act'], audiences: ['competitive_exam'], help: ['exam_prep'],
    styles: ['exam_focused', 'practice_first'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Tamil'],
    ideal: 'Class 10-11 students targeting SAT 1450+ for US universities.',
    avail: AVAIL.weekends, price: 1500, group: 650, demo: 0,
    packages: [{ label: 'SAT 10-week plan (20 sessions)', sessions: 20, priceInr: 27000 }],
    rating: 4.8, reviewsCount: 64, rebook: 86, sessions: 1150, response: 5, joined: '2024-09-12', strength: 100,
    reviews: [
      rv("Ananya's parent", 5, 'Ananya went from 1410 to 1530. The error log method works.', '2026-10-03'),
      rv('SAT student', 5, 'Very clear strategy for the digital SAT.', '2026-06-14'),
    ],
  }),
  t({
    first: 'Arun', last: 'Prakash', gender: 'male', city: 'Coimbatore',
    headline: 'Physics and Maths for IGCSE and A Level · Cambridge examiner experience',
    bio: 'Taught Cambridge physics and maths for 15 years in Coimbatore and Muscat. I know exactly how Cambridge mark schemes reward answers.',
    quals: ['M.Sc Physics, Bharathiar University', 'Cambridge examiner training (Physics 9702)'], years: 15,
    subjects: [
      sub('physics', ['cambridge'], G9_12, ['kinematics', 'dynamics', 'electricity', 'waves', 'quantum-physics', 'practical-skills']),
      sub('maths', ['cambridge'], G9_12, ['pure-mathematics', 'mechanics', 'statistics']),
    ],
    audiences: ['school'], help: ['exam_prep', 'concept_learning'],
    styles: ['exam_focused', 'concept_first'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Tamil'],
    ideal: 'IGCSE and A Level students aiming for A* who need mark-scheme precision.',
    avail: AVAIL.evenings, price: 1100, group: 400, demo: 0,
    rating: 4.7, reviewsCount: 38, rebook: 88, sessions: 600, response: 5, joined: '2024-11-11', strength: 95,
    reviews: [
      rv('A Level student', 5, 'Mark-scheme tips were game-changing.', '2026-08-26'),
      rv('IGCSE parent', 4, 'Very experienced, strict about homework.', '2026-05-07'),
    ],
  }),
  t({
    first: 'Swati', last: 'Mishra', gender: 'female', city: 'Indore',
    headline: 'Study skills, exam anxiety and time management coach',
    bio: 'Educational psychologist who helps students plan, revise and stay calm in exams. Works alongside subject tutors and school counsellors.',
    quals: ['MA Psychology, Devi Ahilya Vishwavidyalaya', 'Certified study-skills coach'], years: 7,
    subjects: [
      sub('english', ALL_B, ALL_G, ['study-skills', 'time-management', 'exam-anxiety', 'note-making']),
      sub('psychology', ['cbse', 'ib'], G11_12, ['stress-and-coping']),
    ],
    audiences: ['school'], help: ['skill_development'],
    styles: ['socratic', 'concept_first'], formats: ['one_to_one'], modes: ['online'], langs: ['English', 'Hindi'],
    homework: 'weekly',
    ideal: 'Capable students whose marks do not match their ability because of panic, procrastination or poor planning.',
    avail: AVAIL.afternoons, price: 900, demo: 0, minutes: 45,
    rating: 4.9, reviewsCount: 25, rebook: 90, sessions: 300, response: 4, joined: '2025-04-11', strength: 95,
    reviews: [
      rv("Meera's parent", 5, 'Breathing and pacing routines really helped Meera in timed tests.', '2026-10-15'),
      rv("Kabir's parent", 4, 'Helped Kabir slow down and check his work.', '2026-09-06'),
    ],
  }),
  t({
    first: 'Gaurav', last: 'Bhatia', gender: 'male', city: 'Gurugram',
    headline: 'IB Economics and TOK · essays and IA commentaries',
    bio: 'IB Economics teacher and TOK coordinator. I help students with evaluation, IA commentaries and the TOK essay.',
    quals: ['MA Economics, Ashoka University', 'IB Economics and TOK workshops'], years: 8,
    subjects: [
      sub('economics', ['ib', 'cambridge'], G11_12, ['microeconomics', 'macroeconomics', 'global-economy', 'ia-commentary', 'evaluation']),
      sub('english', ['ib'], G11_12, ['theory-of-knowledge', 'tok-essay']),
    ],
    audiences: ['school'], help: ['exam_prep', 'concept_learning'],
    styles: ['socratic', 'exam_focused'], formats: ['one_to_one'], modes: ['online'], langs: ['English', 'Hindi', 'Punjabi'],
    ideal: 'IB DP students who understand economics but lose marks on evaluation and commentary structure.',
    avail: AVAIL.lateEvenings, price: 1400, demo: 0,
    rating: 4.8, reviewsCount: 20, rebook: 89, sessions: 260, response: 5, joined: '2025-05-28', strength: 95,
    reviews: [
      rv("Arjun's parent", 5, 'Arjun\'s TOK essay improved a lot.', '2026-09-29'),
      rv('IB DP2 student', 5, 'IA commentaries got a 7.', '2026-04-18'),
    ],
  }),
  t({
    first: 'Tanvi', last: 'Desai', gender: 'female', city: 'Vadodara',
    headline: 'Design portfolio and NID / UCEED preparation',
    bio: 'NID graduate and practising designer. I prepare students for NID DAT and UCEED with sketching drills, design thinking and portfolio reviews.',
    quals: ['B.Des Communication Design, NID Ahmedabad'], years: 5,
    subjects: [sub('entrepreneurship', ['cbse'], G11_12, ['design-thinking', 'creative-problem-solving'])],
    exams: ['nid-dat', 'uceed', 'nata'], audiences: ['competitive_exam', 'career_learners'], help: ['exam_prep', 'skill_development'],
    styles: ['project_based', 'practice_first'], formats: ['one_to_one', 'group'], modes: ['online', 'offline'], offlineArea: 'Alkapuri, Vadodara', langs: ['English', 'Gujarati', 'Hindi'],
    ideal: 'Creative Class 11-12 students who want a design career but have never built a portfolio.',
    avail: AVAIL.weekends, price: 1000, group: 400, demo: 0,
    rating: 4.7, reviewsCount: 23, rebook: 85, sessions: 280, response: 6, joined: '2025-03-30', strength: 90,
    reviews: [
      rv('UCEED 2026 student', 5, 'Got AIR 212. Sketching drills were key.', '2026-03-20'),
      rv('Class 11 parent', 4, 'Good mentoring for portfolio.', '2026-08-12'),
    ],
  }),
  t({
    first: 'Rohan', last: 'Kapadia', gender: 'male', city: 'Ahmedabad',
    headline: 'Entrepreneurship and Business for teens · build a real venture',
    bio: 'Two-time founder who teaches CBSE Entrepreneurship and runs a venture-building programme for school students.',
    quals: ['BBA, Nirma University', 'Founder, two D2C brands'], years: 4,
    subjects: [
      sub('entrepreneurship', ['cbse'], G11_12, ['business-plan', 'idea-validation', 'marketing', 'financial-planning']),
      sub('business', ['cbse', 'ib'], G11_12, ['marketing', 'entrepreneurship']),
    ],
    audiences: ['school', 'career_learners'], help: ['skill_development', 'concept_learning'],
    styles: ['project_based'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Gujarati', 'Hindi'],
    ideal: 'Students who already sell something or run a club and want to turn it into a real venture.',
    avail: AVAIL.weekends, price: 800, group: 300, demo: 0, verified: 'pending',
    rating: 4.6, reviewsCount: 12, rebook: 80, sessions: 140, response: 8, joined: '2026-07-20', strength: 75,
    reviews: [
      rv('Class 12 student', 5, 'We launched our tote-bag store in four weeks.', '2026-10-04'),
      rv('Class 11 parent', 4, 'Practical and motivating.', '2026-09-18'),
    ],
  }),
  t({
    first: 'Mehul', last: 'Shah', gender: 'male', city: 'Surat',
    headline: 'Accountancy and Economics Class 11-12 · CBSE · budget-friendly batches',
    bio: 'I run small online batches for commerce students with chapter tests and quick doubt sessions. Clear notes and lots of practice.',
    quals: ['M.Com, Veer Narmad South Gujarat University'], years: 7,
    subjects: [
      sub('accountancy', ['cbse'], G11_12, ['journal-and-ledger', 'partnership-accounts', 'financial-statements', 'depreciation']),
      sub('economics', ['cbse'], G11_12, ['national-income', 'money-and-banking', 'demand-and-supply']),
    ],
    audiences: ['school'], help: ['exam_prep', 'homework'],
    styles: ['practice_first', 'exam_focused'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['Gujarati', 'Hindi', 'English'],
    ideal: 'Commerce students who need regular practice and fast doubt-solving at a low fee.',
    avail: AVAIL.evenings, price: 400, group: 160, demo: 0,
    rating: 4.5, reviewsCount: 35, rebook: 81, sessions: 640, response: 3, joined: '2025-01-05', strength: 80,
    reviews: [
      rv('Class 12 student', 5, 'Doubts solved the same day.', '2026-02-27'),
      rv('Class 11 parent', 4, 'Good value.', '2026-08-08'),
    ],
  }),
  t({
    first: 'Elizabeth', last: 'George', gender: 'female', city: 'Dubai', tz: 'Asia/Dubai',
    headline: 'IB English A Language and Literature · IO and Paper 1',
    bio: 'IB English teacher at a Dubai international school. I coach the Individual Oral, Paper 1 analysis and the HL essay.',
    quals: ['MA English Literature, University of Kerala', 'PGCE (International)'], years: 13,
    subjects: [sub('english', ['ib', 'cambridge'], G9_12, ['literary-analysis', 'individual-oral', 'paper-1-analysis', 'hl-essay', 'global-issues'])],
    audiences: ['school'], help: ['exam_prep', 'concept_learning'],
    styles: ['socratic', 'exam_focused'], formats: ['one_to_one'], modes: ['online'], langs: ['English', 'Malayalam'],
    ideal: 'IB DP students who read well but struggle to structure analysis under time pressure.',
    avail: AVAIL.gulf, price: 1500, demo: 0,
    rating: 4.9, reviewsCount: 28, rebook: 92, sessions: 390, response: 6, joined: '2025-02-14', strength: 100,
    reviews: [
      rv("Tara's parent", 5, 'Helped Tara move from a 4 to a 6 in Paper 1.', '2026-09-21'),
      rv('IB DP2 student', 5, 'IO practice was brilliant.', '2026-03-12'),
    ],
  }),
  t({
    first: 'Nitin', last: 'Jain', gender: 'male', city: 'Indore',
    headline: 'IPMAT and CUET quant and verbal · IIM Indore IPM alumnus',
    bio: 'IPM graduate from IIM Indore. I coach IPMAT and CUET general test with sectional drills and personal interview prep.',
    quals: ['IPM (BA + MBA), IIM Indore'], years: 4,
    subjects: [
      sub('maths', ['cbse', 'cambridge', 'ib'], G11_12, ['quantitative-aptitude', 'arithmetic', 'algebra', 'data-interpretation']),
      sub('english', ['cbse', 'cambridge', 'ib'], G11_12, ['verbal-ability', 'reading-comprehension']),
    ],
    exams: ['ipmat-indore', 'cuet-ug'], audiences: ['competitive_exam'], help: ['exam_prep'],
    styles: ['practice_first', 'exam_focused'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Hindi'],
    ideal: 'Class 12 commerce or science students aiming for IPM programmes at IIMs.',
    avail: AVAIL.lateEvenings, price: 1000, group: 400, demo: 0,
    rating: 4.7, reviewsCount: 31, rebook: 84, sessions: 420, response: 4, joined: '2025-03-12', strength: 90,
    reviews: [
      rv('IPMAT 2026 student', 5, 'Converted IIM Rohtak and Indore calls.', '2026-07-09'),
      rv('Class 12 parent', 4, 'Good mock analysis.', '2026-09-03'),
    ],
  }),
  t({
    first: 'Ayesha', last: 'Khan', gender: 'female', city: 'Hyderabad',
    headline: 'Biology Class 8-10 and IGCSE Biology · visual learners welcome',
    bio: 'Biology teacher who uses colour-coded notes and models. Popular with Class 8-10 and IGCSE students who find biology terms overwhelming.',
    quals: ['M.Sc Botany, Osmania University', 'B.Ed'], years: 6,
    subjects: [
      sub('biology', ['cambridge'], [9, 10], ['cells', 'nutrition', 'transport-in-plants', 'human-physiology', 'inheritance']),
      sub('science', ['cbse', 'cambridge'], G8_10, ['cell', 'life-processes', 'reproduction', 'microorganisms']),
    ],
    audiences: ['school'], help: ['concept_learning', 'homework'],
    styles: ['concept_first', 'project_based'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Hindi', 'Urdu', 'Telugu'],
    ideal: 'Visual learners in Class 8-10 who get lost in biology vocabulary.',
    avail: AVAIL.afternoons, price: 550, group: 220, demo: 0,
    rating: 4.7, reviewsCount: 19, rebook: 86, sessions: 270, response: 4, joined: '2025-06-22', strength: 85,
    reviews: [
      rv('IGCSE parent', 5, 'Colour notes are lovely and effective.', '2026-08-29'),
      rv('Class 9 student', 4, 'Biology is easier now.', '2026-07-17'),
    ],
  }),
  t({
    first: 'Siddharth', last: 'Banerjee', gender: 'male', city: 'Kolkata',
    headline: 'Maths olympiad and enrichment · Class 8-10 · RMO / IOQM prep',
    bio: 'Former INMO participant who coaches olympiad maths. Ideal for strong students who are bored by school maths and want deeper problems.',
    quals: ['B.Math, Indian Statistical Institute'], years: 5,
    subjects: [sub('maths', ['cbse', 'cambridge', 'ib'], G8_10, ['number-theory', 'combinatorics', 'olympiad-geometry', 'inequalities', 'problem-solving'])],
    audiences: ['competitive_exam', 'school'], help: ['skill_development', 'exam_prep'],
    styles: ['socratic', 'practice_first'], formats: ['one_to_one', 'group'], modes: ['online'], langs: ['English', 'Bengali', 'Hindi'],
    ideal: 'Class 8-10 toppers ready for IOQM and RMO-level problems.',
    avail: AVAIL.weekends, price: 1200, group: 450, demo: 0,
    rating: 4.9, reviewsCount: 17, rebook: 94, sessions: 220, response: 5, joined: '2025-05-02', strength: 95,
    reviews: [
      rv("Aarav's parent", 5, 'Aarav is finally challenged. He qualified IOQM this year.', '2026-10-24'),
      rv('Class 9 student', 5, 'Problems are hard and fun.', '2026-08-18'),
    ],
  }),
];
