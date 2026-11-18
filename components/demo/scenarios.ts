/**
 * The guided demo: 12 scenarios, each a short walk through one story with the persona to log in as,
 * where to start, numbered steps and what to point out. Shared by the /demo page, the Demo guide panel
 * and docs/demo-script.md (keep the three in step).
 *
 * A persona is named by id, with the person's name as a fallback so a scenario still resolves if a
 * Wave 3 persona lands under a different id. `parentOf` picks the parent account linked to a learner.
 * A step's `as` switches persona from that step on; a step's `href` is where its "Go" link lands.
 */

export interface PersonaRef {
  id?: string;
  name?: string;
  /** Resolve to the parent account linked to this learner. */
  parentOf?: string;
}

export interface DemoStep {
  title: string;
  detail?: string;
  /** Log in as this persona when this step is opened (sticks for later steps). */
  as?: PersonaRef;
  /** Route to open for this step. Omitted: stay on the current page and act there. */
  href?: string;
}

export interface DemoScenario {
  id: string;
  n: number;
  title: string;
  summary: string;
  /** Roles this scenario passes through, for the card's badges. */
  roles: string[];
  start: { as: PersonaRef; href: string };
  steps: DemoStep[];
  pointOut: string[];
}

const zoya: PersonaRef = { id: 'lrn_zoya_fernandes', name: 'Zoya Fernandes' };
const aman: PersonaRef = { id: 'sal_aman_gupta', name: 'Aman Gupta' };
const priya: PersonaRef = { id: 'sal_priya_malhotra', name: 'Priya Malhotra' };
const heena: PersonaRef = { id: 'csl_heena_qureshi', name: 'Heena Qureshi' };
const farah: PersonaRef = { id: 'csl_farah_siddiqui', name: 'Farah Siddiqui' };
const rahul: PersonaRef = { id: 'tut_rahul_verma', name: 'Rahul Verma' };

export const SCENARIOS: DemoScenario[] = [
  {
    id: 'lead-to-student',
    n: 1,
    title: 'Lead to student',
    summary: "A sales rep closes Zoya's family, converts the lead, and Zoya onboards and gets a personal plan.",
    roles: ['Sales', 'Student'],
    start: { as: aman, href: '/crm' },
    steps: [
      { title: 'Sales dashboard', detail: 'Funnel by stage, leads by source, revenue this month and follow-ups due today.', href: '/crm' },
      { title: "Open Zoya Fernandes' lead", detail: 'Leads, search "Fernandes". The timeline shows every call, WhatsApp and the proposal sent.', href: '/crm/leads' },
      { title: 'Record the payment', detail: 'On the lead, Record payment, mark it paid. An invoice with the GST line is created.' },
      { title: 'Convert to platform', detail: 'Convert to platform assigns the counsellor and creates the subscription. Then Open in platform.' },
      { title: 'Zoya onboards', detail: 'About, needs and profile, then the starting test.', as: zoya, href: '/onboarding/about' },
      { title: 'Take the starting test', detail: 'Answer a few items, then "Answer the rest for me (demo)" on each part.', href: '/onboarding/test' },
      { title: 'Home fills in', detail: 'Gaps, plan, timetable and the next best action, all from her test.', href: '/student' },
      { title: 'Back in sales', detail: 'The funnel and revenue now count Zoya as converted.', as: aman, href: '/crm' },
    ],
    pointOut: [
      'One record from first enquiry to first lesson: nothing is typed twice.',
      'Follow-up rules (48 h nudge, demo reminders, payment chase) are shown and simulated, not sent.',
      "Zoya's starting profile comes from one 40-minute test, at low confidence until evidence builds.",
    ],
  },
  {
    id: 'kabir',
    n: 2,
    title: 'Kabir: careless and over-confident',
    summary: 'A chapter check finds G4 careless and G9 over-confidence; the plan uses estimate-first practice and the week re-plans.',
    roles: ['Student'],
    start: { as: { id: 'lrn_kabir_singh', name: 'Kabir Singh' }, href: '/student' },
    steps: [
      { title: 'Home', detail: 'Mastery, MCI (confidence calibration) trending up, and the next best action.', href: '/student' },
      { title: 'Take the in-class chapter check', detail: 'Assessments, the chapter his class is on now. Answer quickly and confidently.', href: '/student/assessments' },
      { title: 'Gap analysis', detail: 'After submit, open Gap analysis: G4 (careless) and G9 (over-confident) with the evidence for each.' },
      { title: 'Topic detail', detail: 'Open a topic: "why you chose this", free plan steps with estimate-first practice, a matched tutor.' },
      { title: 'Timetable re-plans', detail: 'The week now holds the new practice blocks; the change log says why.', href: '/student/timetable' },
    ],
    pointOut: [
      'Every gap code comes with the answer pattern that triggered it, not a guess.',
      'Estimate-first means he predicts the answer before solving, which trains calibration.',
      'The timetable is rebuilt by the engine after every test, inside his free slots.',
    ],
  },
  {
    id: 'rohan',
    n: 3,
    title: 'Rohan: free plan fails, paid tutor suggested',
    summary: 'Three weeks of free plan without recovery triggers a paid tutor suggestion; his parent approves and sees the spend.',
    roles: ['Student', 'Parent', 'Tutor'],
    start: { as: { id: 'lrn_rohan_das', name: 'Rohan Das' }, href: '/student' },
    steps: [
      { title: "Rohan's home", detail: 'Open gaps across chapters and the "paid tutor recommended" next action.', href: '/student' },
      { title: 'His tutor request', detail: 'Explore Tutors shows the matched tutors and the request waiting for his parent.', href: '/student/tutors' },
      { title: 'Parent: Plan and spend', detail: '"Free plan has run 3 weeks" with the hours and rupees each gap costs.', as: { parentOf: 'lrn_rohan_das', id: 'par_anita_das', name: 'Anita Das' }, href: '/parent/plan' },
      { title: 'Approve the tutor', detail: 'Approve. The booking now waits for the tutor to accept.' },
      { title: 'Spend shows', detail: 'Sessions and payments lists the booking and what it will cost.', href: '/parent/payments' },
    ],
    pointOut: [
      'The 3-week rule is an engine rule, not a sales nudge: free help first, paid only when it has not worked.',
      'The parent sees cost and progress, never wellbeing check-ins (T3).',
    ],
  },
  {
    id: 'ishita-rahul',
    n: 4,
    title: 'Ishita books Rahul Verma',
    summary: 'Ishita books a tutor, Rahul accepts with her gap snapshot, files a session report, and homework lands in her tasks.',
    roles: ['Student', 'Tutor'],
    start: { as: { id: 'lrn_ishita_rao', name: 'Ishita Rao' }, href: '/student/tutors' },
    steps: [
      { title: 'Explore tutors', detail: 'Matched on her G1 gaps (fractions, integers), style, budget and free slots.', href: '/student/tutors' },
      { title: 'Book Rahul Verma', detail: "Open Rahul's profile, Book, choose a slot, share the gap snapshot." },
      { title: 'Rahul sees the request', detail: 'Home lists the request with her gap snapshot. Accept it.', as: rahul, href: '/tutor' },
      { title: 'Run the session report', detail: "Sessions, open Ishita's session, Report: what was covered, and set homework.", href: '/tutor/sessions' },
      { title: 'Homework in her tasks', detail: 'Back as Ishita: the homework is in her tasks and her timetable.', as: { id: 'lrn_ishita_rao', name: 'Ishita Rao' }, href: '/student/assessments' },
    ],
    pointOut: [
      'The tutor gets the diagnosis, not just a name: they start the first session knowing the gaps.',
      "The report and homework write back into the same record the student's plan reads.",
    ],
  },
  {
    id: 'vihaan',
    n: 5,
    title: 'Vihaan: Chemistry retention',
    summary: 'A JEE aspirant whose Chemistry fades between tests gets spaced reviews built into his timetable.',
    roles: ['Student'],
    start: { as: { id: 'lrn_vihaan_joshi', name: 'Vihaan Joshi' }, href: '/student' },
    steps: [
      { title: 'Home', detail: 'Strong Maths, Chemistry flagged for retention (R under 0.7).', href: '/student' },
      { title: 'Retention gaps', detail: 'Assessments, the latest Chemistry result, Gap analysis: G6 retention.', href: '/student/assessments' },
      { title: 'Spaced reviews', detail: 'Timetable: short review blocks spaced 1, 3 and 7 days after each Chemistry topic.', href: '/student/timetable' },
      { title: 'His tutor', detail: 'Sessions shows his Chemistry tutor and the last report.', href: '/student/sessions' },
    ],
    pointOut: [
      'Retention is measured by 7-day probes, so "forgot it" is evidence, not a feeling.',
      'Reviews are short and placed by the forgetting curve, not added as extra hours.',
    ],
  },
  {
    id: 'suresh',
    n: 6,
    title: 'Teacher finds a G3 cluster',
    summary: 'Suresh Pillai spots several students with the same procedural gap and assigns one re-teach set.',
    roles: ['Teacher', 'Student'],
    start: { as: { id: 'tch_suresh_pillai', name: 'Suresh Pillai' }, href: '/teacher' },
    steps: [
      { title: 'Class heatmap', detail: '9A Maths: students by subtopics, coloured by mastery.', href: '/teacher' },
      { title: 'Class gaps', detail: 'A G3 cluster on one subtopic, with the students in it.', href: '/teacher/class-gaps' },
      { title: 'Assign a re-teach set', detail: 'Assign the re-teach set to the cluster.', href: '/teacher/assign' },
      { title: 'Validate a gap', detail: 'Gap log: confirm or correct a diagnosis. It is written to the record as teacher-validated.', href: '/teacher/gap-log' },
      { title: 'Kabir sees it', detail: 'As Kabir, the re-teach set is in his tasks.', as: { id: 'lrn_kabir_singh', name: 'Kabir Singh' }, href: '/student/assessments' },
    ],
    pointOut: [
      'Teachers see T1 data only: mastery and gaps, never wellbeing or family details.',
      'One click turns a class pattern into individual tasks.',
    ],
  },
  {
    id: 'heena-sara',
    n: 7,
    title: 'Counsellor approves a change and runs a career session',
    summary: "Heena approves a timetable change request, then runs Sara's career session: CA vs Data Analyst with time and cost.",
    roles: ['Counsellor', 'Student'],
    start: { as: heena, href: '/counsellor' },
    steps: [
      { title: 'Caseload', detail: 'All students with flags and what needs Heena today.', href: '/counsellor' },
      { title: 'Approve a timetable request', detail: "Kabir's pending request; approve it and the week re-plans.", href: '/counsellor/timetable-requests' },
      { title: "Sara's career session", detail: 'Career sessions, Sara: CA vs Data Analyst, skill gaps, years and rupees for each route.', href: '/counsellor/career-sessions' },
      { title: 'Save action items', detail: 'Save notes; action items become tasks for Sara.' },
      { title: "Sara's view", detail: 'Career: the comparison and her new tasks.', as: { id: 'lrn_sara_khan', name: 'Sara Khan' }, href: '/student/career' },
    ],
    pointOut: [
      'The comparison uses her real strengths (Accountancy) and gaps (Economics G2), not a generic quiz.',
      'Approving a request calls the same timetable engine the student uses.',
    ],
  },
  {
    id: 'nikhil',
    n: 8,
    title: "Nikhil's application",
    summary: 'A full Application Support subscriber: QA check, an essay comment round trip with Farah, then submit.',
    roles: ['Student', 'Counsellor'],
    start: { as: { id: 'lrn_nikhil_reddy', name: 'Nikhil Reddy' }, href: '/student/applications' },
    steps: [
      { title: 'Command center', detail: 'Universities, board and deadlines. Leeds is due 28 Nov with open items.', href: '/student/applications' },
      { title: 'QA check', detail: 'Open the Leeds application and run the QA check: what is missing before submit.' },
      { title: 'Essay', detail: 'Essays: versions, the AI pre-pass and anchored comments.', href: '/student/applications/essays' },
      { title: 'Farah reviews', detail: 'Draft reviews: add a comment on the essay.', as: farah, href: '/counsellor/draft-reviews' },
      { title: 'Nikhil replies and submits', detail: 'Resolve the comment, then submit the application once QA is clear.', as: { id: 'lrn_nikhil_reddy', name: 'Nikhil Reddy' }, href: '/student/applications' },
    ],
    pointOut: [
      'The deadline risk flag fires because the due date is under 14 days with open items.',
      'Comments are anchored to the exact sentence, across versions.',
    ],
  },
  {
    id: 'ananya',
    n: 9,
    title: 'Ananya: University Fit to Application Support',
    summary: 'A topper uses the free University Fit, sees reach, target and safe options, and is offered the paid upgrade.',
    roles: ['Student'],
    start: { as: { id: 'lrn_ananya_kapoor', name: 'Ananya Kapoor' }, href: '/student/universities' },
    steps: [
      { title: 'University Fit', detail: 'The free explorer with saved universities.', href: '/student/universities' },
      { title: 'Best Fit', detail: 'Run Best Fit: reach, target and safe with the reason for each.', href: '/student/universities/best-fit' },
      { title: 'A university', detail: 'Open one: requirements, deadlines and what she is missing.' },
      { title: 'Upgrade', detail: 'Application Support: what the paid plan adds and its price (sample pricing).', href: '/student/applications/upgrade' },
    ],
    pointOut: ['Free tools are genuinely useful; the upgrade is offered, not forced.', 'Prices are sample values kept in one config file.'],
  },
  {
    id: 'meera',
    n: 10,
    title: 'Meera: wellbeing, seen by the right people',
    summary: "Meera's wellbeing check is visible to her counsellor in full and to her parent only as a summary.",
    roles: ['Counsellor', 'Parent'],
    start: { as: heena, href: '/counsellor/risk-flags' },
    steps: [
      { title: 'Risk flags', detail: "Meera's wellbeing flag (time pressure, under-confidence).", href: '/counsellor/risk-flags' },
      { title: 'Student 360', detail: "Meera's full profile: each value with its source, confidence and tier.", href: '/counsellor/student-360' },
      { title: "Parent's view", detail: 'Home and Privacy: a summary only, no T3 values.', as: { parentOf: 'lrn_meera_iyer', name: 'Iyer' }, href: '/parent' },
      { title: 'Privacy and consent', detail: 'What is collected, who sees it, dated consents.', href: '/parent/privacy' },
    ],
    pointOut: [
      'T3 (screened wellbeing) data is visible only to the counsellor. Parents, teachers and tutors never get it.',
      'Consent is per purpose and can be withdrawn from the parent screen.',
    ],
  },
  {
    id: 'aarav',
    n: 11,
    title: 'Aarav: topper, stretched',
    summary: 'A strong learner gets advanced readiness, a compressed timetable and olympiad enrichment instead of more of the same.',
    roles: ['Student', 'Parent'],
    start: { as: { id: 'lrn_aarav_kapoor', name: 'Aarav Kapoor' }, href: '/student' },
    steps: [
      { title: 'Home', detail: 'Excellent band, LRS about 0.84, advanced-topic readiness high.', href: '/student' },
      { title: 'Timetable', detail: 'Compressed: fewer hours for mastered work, enrichment blocks added.', href: '/student/timetable' },
      { title: 'Enrichment', detail: 'Inventory and career: olympiad preparation and resources.', href: '/student/inventory' },
      { title: 'One parent, two children', detail: 'Neha Kapoor switches between Aarav and Ananya.', as: { id: 'par_neha_kapoor', name: 'Neha Kapoor' }, href: '/parent' },
    ],
    pointOut: ['Personalisation works both ways: stretch for toppers, support for strugglers.', 'Siblings share one parent account.'],
  },
  {
    id: 'tara-kunal',
    n: 12,
    title: 'Tara and Kunal: careers from strengths',
    summary: "Tara's app projects become her portfolio; Kunal's debating and leadership point to careers, with language support for his G7 gap.",
    roles: ['Student', 'Mentor'],
    start: { as: { id: 'lrn_tara_menon', name: 'Tara Menon' }, href: '/student/career' },
    steps: [
      { title: "Tara's careers", detail: 'Software and CS careers ranked from her strengths.', href: '/student/career' },
      { title: 'Portfolio', detail: 'Inventory: code projects filed as application documents.', href: '/student/inventory' },
      { title: 'Applications', detail: 'CS applications to the US and Canada; essay gaps flagged.', href: '/student/applications' },
      { title: "Kunal's careers", detail: 'Law, policy, public speaking: careers that use debating and leadership.', as: { id: 'lrn_kunal_verma', name: 'Kunal Verma' }, href: '/student/career' },
      { title: 'Language support', detail: 'His G7 language gap and the support plan (moved from Hindi medium).', href: '/student' },
      { title: 'Mentor view', detail: "Kelvin's skill plans for Kunal.", as: { id: 'mnt_kelvin_thomas', name: 'Kelvin Thomas' }, href: '/mentor/skill-plans' },
    ],
    pointOut: [
      'Weak marks do not mean weak prospects: careers come from strengths, not only scores.',
      'G7 language gaps get language support, not more subject drills.',
    ],
  },
];

export const DEMO_COOKIE = 'learnibility_demo';

export function findScenario(id: string | undefined | null) {
  return id ? SCENARIOS.find((s) => s.id === id) : undefined;
}

/** The persona a step runs as: the latest `as` at or before the step, else the scenario's start persona. */
export function personaForStep(s: DemoScenario, step: number): PersonaRef {
  for (let i = Math.min(step, s.steps.length - 1); i >= 0; i--) if (s.steps[i]?.as) return s.steps[i].as!;
  return s.start.as;
}

/** Where a step's Go link lands: its own href, else the latest earlier href, else the start route. */
export function hrefForStep(s: DemoScenario, step: number): string {
  for (let i = Math.min(step, s.steps.length - 1); i >= 0; i--) if (s.steps[i]?.href) return s.steps[i].href!;
  return s.start.href;
}

export function parseDemoCookie(v: string | undefined) {
  if (!v) return undefined;
  const [id, n] = v.split(':');
  const scenario = findScenario(id);
  if (!scenario) return undefined;
  const step = Math.max(0, Math.min(scenario.steps.length - 1, Number(n) || 0));
  return { scenario, step };
}
