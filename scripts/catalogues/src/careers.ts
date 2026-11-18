import type { Career, CareerPathway, DemandLevel, Riasec } from '../../../lib/types/catalogue';
import type { Stream } from '../../../lib/types/enums';

type S = Exclude<Stream, 'none'>;
type Country = CareerPathway['country'];
const L = 100_000; // one lakh rupees

function p(
  careerSlug: string,
  suffix: string,
  label: string,
  country: Country,
  stream: S,
  examIds: string[],
  degree: string,
  steps: [string, number][],
  yearsToEntry: number,
  costLakh: [number, number, number],
  costNote: string,
  universityIds: string[],
): CareerPathway {
  return {
    id: `${careerSlug}-${suffix}`,
    label,
    region: country === 'in' ? 'india' : 'abroad',
    country,
    stream,
    examIds,
    degree,
    steps: steps.map(([stage, years]) => ({ stage, years })),
    yearsToEntry,
    costInr: { low: Math.round(costLakh[0] * L), typical: Math.round(costLakh[1] * L), high: Math.round(costLakh[2] * L) },
    costNote,
    universityIds,
  };
}

interface C {
  slug: string;
  title: string;
  cluster: string;
  streams: S[];
  riasec: Riasec[];
  apt: number[]; // 430-profile parameter numbers
  summary: string;
  day: string;
  subjects: [string, number, boolean][];
  skills: [string, 1 | 2 | 3 | 4 | 5, 'core' | 'helpful'][];
  pathways: (slug: string) => CareerPathway[];
  salLakh: [number, number, number, number]; // entry low, entry high, mid, senior (lakh per year)
  abroad?: ['us' | 'uk' | 'ca' | 'au', number, number]; // entry, mid in lakh per year
  demand: DemandLevel;
  growth: number;
  cities: [string, number][];
  recruiters: string[];
  style: string[];
  related: string[];
  sources: [string, string][];
}

const AS_OF = '2026-11-18';

function c(x: C): Career {
  return {
    id: `career-${x.slug}`,
    title: x.title,
    cluster: x.cluster,
    summary: x.summary,
    dayInLife: x.day,
    streams: x.streams,
    riasec: x.riasec,
    aptitudeParamIds: x.apt.map((n) => `p${n}`),
    subjects: x.subjects.map(([subjectSlug, minPercent, required]) => ({ subjectSlug, minPercent, required })),
    skills: x.skills.map(([s, targetLevel, importance]) => ({ skillId: `skill-${s}`, targetLevel, importance })),
    pathways: x.pathways(x.slug),
    salaryInr: { entryLow: x.salLakh[0] * L, entryHigh: x.salLakh[1] * L, mid: x.salLakh[2] * L, senior: x.salLakh[3] * L },
    ...(x.abroad ? { abroadSalaryInr: { country: x.abroad[0], entry: x.abroad[1] * L, mid: x.abroad[2] * L } } : {}),
    demand: x.demand,
    growthPct: x.growth,
    topCities: x.cities.map(([city, sharePct]) => ({ city, sharePct })),
    topRecruiters: x.recruiters,
    workStyle: x.style,
    relatedCareerIds: x.related.map((r) => `career-${r}`),
    sources: x.sources.map(([label, url]) => ({ label, url, asOf: AS_OF })),
  };
}

// Common source pages
const NCS = ['National Career Service: career guide', 'https://www.ncs.gov.in'] as [string, string];
const BLS = (path: string): [string, string] => ['US BLS Occupational Outlook Handbook', `https://www.bls.gov/ooh/${path}`];
const AMB = (slug: string): [string, string] => ['AmbitionBox salary data (India)', `https://www.ambitionbox.com/profile/${slug}-salary`];

// Common pathway costs (lakh rupees, class 12 to entry, incl. coaching, living, fees). Abroad uses FX in docs/catalogue-ids.md.
const IIT_BTECH: [number, number, number] = [9, 14, 22];
const PVT_BTECH: [number, number, number] = [14, 22, 35];
const US_4YR: [number, number, number] = [180, 290, 380];
const UK_3YR: [number, number, number] = [95, 125, 160];
const CA_4YR: [number, number, number] = [110, 150, 210];
const AU_3YR: [number, number, number] = [95, 120, 150];

const TECH_IN = ['uni-in-iit-bombay', 'uni-in-iit-delhi', 'uni-in-iit-madras', 'uni-in-iit-kanpur', 'uni-in-bits-pilani', 'uni-in-iiit-hyderabad', 'uni-in-vit-vellore', 'uni-in-manipal'];
const TECH_US = ['uni-us-mit', 'uni-us-stanford', 'uni-us-carnegie-mellon', 'uni-us-uc-berkeley', 'uni-us-georgia-tech', 'uni-us-uiuc', 'uni-us-purdue', 'uni-us-ut-austin', 'uni-us-arizona-state'];
const TECH_CA = ['uni-ca-waterloo', 'uni-ca-toronto', 'uni-ca-ubc', 'uni-ca-mcgill', 'uni-ca-mcmaster'];
const TECH_UK = ['uni-uk-imperial', 'uni-uk-cambridge', 'uni-uk-oxford', 'uni-uk-ucl', 'uni-uk-edinburgh', 'uni-uk-manchester'];
const BIZ_IN = ['uni-in-srcc-delhi', 'uni-in-iim-indore', 'uni-in-ashoka', 'uni-in-flame-pune', 'uni-in-christ-bengaluru', 'uni-in-lsr-delhi'];
const BIZ_UK = ['uni-uk-lse', 'uni-uk-warwick', 'uni-uk-ucl', 'uni-uk-manchester', 'uni-uk-leeds', 'uni-uk-nottingham', 'uni-uk-durham'];
const BIZ_CA = ['uni-ca-toronto', 'uni-ca-western', 'uni-ca-queens', 'uni-ca-york', 'uni-ca-ubc', 'uni-ca-mcgill'];
const BIZ_US = ['uni-us-nyu', 'uni-us-umich', 'uni-us-uc-berkeley', 'uni-us-boston-university', 'uni-us-northeastern', 'uni-us-ut-austin'];
const MED_IN = ['uni-in-aiims-delhi', 'uni-in-cmc-vellore', 'uni-in-manipal'];
const LAW_IN = ['uni-in-nlsiu-bengaluru', 'uni-in-nalsar-hyderabad', 'uni-in-nlu-delhi'];
const LAW_UK = ['uni-uk-oxford', 'uni-uk-cambridge', 'uni-uk-lse', 'uni-uk-kcl', 'uni-uk-ucl', 'uni-uk-durham'];
const LIB_IN = ['uni-in-ashoka', 'uni-in-flame-pune', 'uni-in-lsr-delhi', 'uni-in-christ-bengaluru'];
const DESIGN_IN = ['uni-in-nid-ahmedabad', 'uni-in-iit-bombay', 'uni-in-flame-pune'];

const ENGG_STEPS: [string, number][] = [['JEE preparation alongside class 11-12', 2], ['B.Tech', 4]];
const PCM: [string, number, boolean][] = [['maths', 75, true], ['physics', 75, true], ['chemistry', 70, true]];

export const CAREERS: Career[] = [
  // ======================================================= Technology
  c({
    slug: 'software-engineer', title: 'Software Engineer', cluster: 'Technology', streams: ['science'], riasec: ['I', 'R', 'C'], apt: [62, 65, 63],
    summary: 'Designs, builds and maintains the software behind apps, websites and enterprise systems.',
    day: 'Stand-up with the team, two focused coding blocks, a code review, and a bug fix shipped before evening.',
    subjects: [['maths', 75, true], ['physics', 70, false], ['computer-science', 70, false]],
    skills: [['python-programming', 4, 'core'], ['data-structures-algorithms', 4, 'core'], ['web-development', 3, 'core'], ['sql-databases', 3, 'core'], ['problem-solving', 4, 'core'], ['teamwork', 3, 'helpful'], ['ai-tool-fluency', 3, 'helpful'], ['written-communication', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'B.Tech Computer Science via JEE', 'in', 'science', ['jee-main', 'jee-advanced', 'bitsat'], 'B.Tech Computer Science and Engineering (4 yrs)', ENGG_STEPS, 4, IIT_BTECH, 'IIT/NIT fees about ₹2.2 lakh a year plus hostel; private colleges cost more.', TECH_IN),
      p(s, 'us', 'BS Computer Science in the US', 'us', 'science', ['sat', 'toefl'], 'BS Computer Science (4 yrs)', [['SAT and applications in class 11-12', 1], ['BS', 4]], 4, US_4YR, 'Before aid; MIT, Stanford and CMU meet need for some internationals.', TECH_US),
      p(s, 'canada', 'BCS / BASc in Canada with co-op', 'ca', 'science', ['ielts'], 'Bachelor of Computer Science, co-op (4-5 yrs)', [['Applications in class 12', 1], ['Co-op degree', 5]], 5, CA_4YR, 'Waterloo co-op terms pay roughly ₹15-25 lakh in total over the degree.', TECH_CA),
    ],
    salLakh: [6, 18, 30, 60], abroad: ['us', 105, 150], demand: 'very_high', growth: 14,
    cities: [['Bengaluru', 34], ['Hyderabad', 18], ['Pune', 12], ['Delhi NCR', 12], ['Chennai', 9]],
    recruiters: ['TCS', 'Infosys', 'Microsoft', 'Google', 'Flipkart', 'Zoho'], style: ['Desk-based', 'Hybrid or remote', 'Team-based'],
    related: ['ai-ml-engineer', 'game-developer', 'cybersecurity-analyst', 'product-manager'],
    sources: [NCS, AMB('software-engineer'), BLS('computer-and-information-technology/software-developers.htm')],
  }),
  c({
    slug: 'data-analyst', title: 'Data Analyst', cluster: 'Technology', streams: ['science', 'commerce'], riasec: ['I', 'C', 'E'], apt: [62, 319, 318],
    summary: 'Turns raw business data into dashboards and answers that help teams decide.',
    day: 'Pull numbers with SQL, clean them in Python or Excel, build a dashboard, and walk a manager through what changed this week.',
    subjects: [['maths', 70, true], ['applied-maths', 70, false], ['economics', 65, false], ['informatics', 65, false]],
    skills: [['sql-databases', 3, 'core'], ['spreadsheets', 4, 'core'], ['statistics', 3, 'core'], ['python-programming', 3, 'core'], ['data-visualisation', 3, 'core'], ['written-communication', 3, 'core'], ['commercial-awareness', 2, 'helpful']],
    pathways: (s) => [
      p(s, 'india-btech', 'B.Tech CSE or Data Science via JEE', 'in', 'science', ['jee-main', 'bitsat'], 'B.Tech CSE / Data Science (4 yrs)', ENGG_STEPS, 4, IIT_BTECH, 'Engineering route; strongest placements.', ['uni-in-iit-bombay', 'uni-in-iiit-hyderabad', 'uni-in-bits-pilani', 'uni-in-vit-vellore']),
      p(s, 'india-bsc', 'BSc Statistics / Economics or BCom + certificate', 'in', 'commerce', ['cuet-ug'], 'BSc / BCom (3 yrs) + analytics certificate', [['CUET in class 12', 1], ['Degree', 3], ['Analytics certificate', 0.5]], 3.5, [3, 6, 12], 'Delhi University fees are low; a ₹30,000-80,000 certificate closes the tools gap.', ['uni-in-srcc-delhi', 'uni-in-christ-bengaluru', 'uni-in-ashoka', 'uni-in-flame-pune']),
      p(s, 'uk', 'BSc Data Science / Economics in the UK', 'uk', 'science', ['ielts'], 'BSc Data Science (3 yrs)', [['UCAS application in class 12', 1], ['BSc', 3]], 3, UK_3YR, 'Graduate Route visa allows 18 months of UK work after study.', ['uni-uk-warwick', 'uni-uk-lse', 'uni-uk-manchester', 'uni-uk-edinburgh']),
    ],
    salLakh: [6, 12, 18, 35], abroad: ['uk', 35, 55], demand: 'high', growth: 18,
    cities: [['Bengaluru', 31], ['Hyderabad', 17], ['Pune', 13], ['Delhi NCR', 14], ['Mumbai', 11]],
    recruiters: ['Mu Sigma', 'Fractal', 'Deloitte', 'Swiggy', 'Amazon', 'HDFC Bank'], style: ['Desk-based', 'Hybrid', 'Works with business teams'],
    related: ['business-analyst', 'ai-ml-engineer', 'financial-analyst', 'economist'],
    sources: [NCS, AMB('data-analyst'), BLS('math/data-scientists.htm')],
  }),
  c({
    slug: 'ai-ml-engineer', title: 'AI / Machine Learning Engineer', cluster: 'Technology', streams: ['science'], riasec: ['I', 'R'], apt: [62, 63, 318],
    summary: 'Builds and deploys machine-learning models, from recommendation systems to language models.',
    day: 'Review overnight training runs, debug a data pipeline, read a new paper, and ship an improved model behind a feature flag.',
    subjects: PCM.concat([['computer-science', 75, false]]),
    skills: [['python-programming', 4, 'core'], ['machine-learning', 4, 'core'], ['calculus', 4, 'core'], ['statistics', 4, 'core'], ['algebra', 4, 'core'], ['data-structures-algorithms', 3, 'core'], ['research', 3, 'helpful'], ['ai-tool-fluency', 4, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'B.Tech CSE / AI via JEE, then M.Tech or industry', 'in', 'science', ['jee-main', 'jee-advanced'], 'B.Tech CSE or AI and Data Science (4 yrs)', ENGG_STEPS, 4, IIT_BTECH, 'Many roles prefer an M.Tech or MS; add ₹2-40 lakh if you do one.', ['uni-in-iit-bombay', 'uni-in-iit-madras', 'uni-in-iit-delhi', 'uni-in-iiit-hyderabad', 'uni-in-iisc-bengaluru']),
      p(s, 'us', 'BS CS with ML focus in the US', 'us', 'science', ['sat', 'toefl'], 'BS Computer Science (4 yrs)', [['SAT and applications', 1], ['BS', 4]], 4, US_4YR, 'OPT/STEM OPT gives up to 3 years of US work after graduation.', ['uni-us-carnegie-mellon', 'uni-us-stanford', 'uni-us-mit', 'uni-us-uc-berkeley', 'uni-us-uiuc']),
      p(s, 'canada', 'BCS in Canada (Toronto/Waterloo AI cluster)', 'ca', 'science', ['ielts'], 'BSc / BCS Computer Science (4 yrs)', [['Applications', 1], ['Degree', 4]], 4, CA_4YR, 'Toronto-Waterloo is a major AI research hub (Vector Institute).', ['uni-ca-toronto', 'uni-ca-waterloo', 'uni-ca-mcgill', 'uni-ca-ubc']),
    ],
    salLakh: [10, 30, 45, 90], abroad: ['us', 120, 180], demand: 'very_high', growth: 26,
    cities: [['Bengaluru', 41], ['Hyderabad', 16], ['Delhi NCR', 12], ['Pune', 9], ['Chennai', 7]],
    recruiters: ['Google DeepMind', 'Microsoft Research', 'Sarvam AI', 'Flipkart', 'Nvidia', 'Ola Krutrim'], style: ['Desk-based', 'Research-heavy', 'Hybrid'],
    related: ['software-engineer', 'data-analyst', 'research-scientist'],
    sources: [NCS, AMB('machine-learning-engineer'), BLS('computer-and-information-technology/computer-and-information-research-scientists.htm')],
  }),
  c({
    slug: 'cybersecurity-analyst', title: 'Cybersecurity Analyst', cluster: 'Technology', streams: ['science'], riasec: ['I', 'C', 'R'], apt: [65, 63],
    summary: 'Protects networks and data by monitoring threats, testing defences and responding to attacks.',
    day: 'Triage alerts in the security operations centre, investigate a phishing attempt, patch a vulnerable server and write the incident report.',
    subjects: [['maths', 65, true], ['computer-science', 65, false], ['physics', 60, false]],
    skills: [['cybersecurity', 4, 'core'], ['python-programming', 3, 'core'], ['sql-databases', 2, 'helpful'], ['problem-solving', 4, 'core'], ['written-communication', 3, 'helpful'], ['ethical-reasoning', 3, 'core']],
    pathways: (s) => [
      p(s, 'india', 'B.Tech CSE (cybersecurity) + certifications', 'in', 'science', ['jee-main', 'viteee', 'met-manipal'], 'B.Tech CSE with Cyber Security (4 yrs)', ENGG_STEPS, 4, PVT_BTECH, 'Add ₹40,000-1.5 lakh for CompTIA Security+ / CEH certifications.', ['uni-in-vit-vellore', 'uni-in-manipal', 'uni-in-iiit-hyderabad', 'uni-in-iit-kanpur']),
      p(s, 'us', 'BS Computer Science / Cybersecurity in the US', 'us', 'science', ['sat', 'toefl'], 'BS Cybersecurity or CS (4 yrs)', [['Applications', 1], ['BS', 4]], 4, US_4YR, 'Government security roles in the US usually need citizenship.', ['uni-us-carnegie-mellon', 'uni-us-purdue', 'uni-us-georgia-tech', 'uni-us-northeastern', 'uni-us-arizona-state']),
    ],
    salLakh: [5, 10, 20, 45], abroad: ['us', 85, 115], demand: 'very_high', growth: 22,
    cities: [['Bengaluru', 28], ['Delhi NCR', 18], ['Hyderabad', 15], ['Mumbai', 13], ['Pune', 10]],
    recruiters: ['Wipro', 'Palo Alto Networks', 'Quick Heal', 'Deloitte', 'CERT-In', 'HDFC Bank'], style: ['Shift work in SOCs', 'Desk-based', 'On-call'],
    related: ['software-engineer', 'ai-ml-engineer'],
    sources: [NCS, AMB('cyber-security-analyst'), BLS('computer-and-information-technology/information-security-analysts.htm')],
  }),
  c({
    slug: 'game-developer', title: 'Game Developer', cluster: 'Technology', streams: ['science'], riasec: ['A', 'I', 'R'], apt: [64, 63, 81],
    summary: 'Programs gameplay, physics and tools for mobile, PC and console games.',
    day: 'Prototype a new mechanic in Unity, fix frame-rate issues, playtest with designers and polish a level.',
    subjects: [['maths', 70, true], ['physics', 65, false], ['computer-science', 65, false]],
    skills: [['game-engines', 4, 'core'], ['python-programming', 3, 'helpful'], ['data-structures-algorithms', 3, 'core'], ['geometry', 4, 'core'], ['mechanics', 3, 'helpful'], ['creative-design', 3, 'helpful'], ['teamwork', 3, 'core']],
    pathways: (s) => [
      p(s, 'india', 'B.Tech CSE + game portfolio', 'in', 'science', ['jee-main', 'viteee'], 'B.Tech CSE (4 yrs)', ENGG_STEPS, 4, PVT_BTECH, 'Portfolio of shipped games matters more than college name.', ['uni-in-iiit-hyderabad', 'uni-in-vit-vellore', 'uni-in-manipal', 'uni-in-iit-bombay']),
      p(s, 'canada', 'Computer Science / Game Design in Canada', 'ca', 'science', ['ielts'], 'BSc Computer Science (4 yrs)', [['Applications', 1], ['Degree', 4]], 4, CA_4YR, 'Montreal and Vancouver are big game-studio cities (Ubisoft, EA).', ['uni-ca-mcgill', 'uni-ca-ubc', 'uni-ca-waterloo', 'uni-ca-york']),
    ],
    salLakh: [4.5, 9, 16, 35], abroad: ['ca', 45, 65], demand: 'medium', growth: 12,
    cities: [['Bengaluru', 30], ['Hyderabad', 20], ['Pune', 18], ['Mumbai', 12], ['Delhi NCR', 10]],
    recruiters: ['Ubisoft India', 'Nazara', 'Rockstar India', 'EA', 'Zynga', 'SuperGaming'], style: ['Studio-based', 'Crunch periods near launches', 'Creative teams'],
    related: ['software-engineer', 'ux-designer', 'communication-designer'],
    sources: [NCS, AMB('game-developer'), BLS('computer-and-information-technology/software-developers.htm')],
  }),
  // ======================================================= Engineering
  c({
    slug: 'mechanical-engineer', title: 'Mechanical Engineer', cluster: 'Engineering', streams: ['science'], riasec: ['R', 'I'], apt: [64, 62],
    summary: 'Designs machines and thermal systems, from car engines to HVAC and robotics.',
    day: 'Model a part in SolidWorks, run a stress simulation, visit the shop floor to check a prototype and update the bill of materials.',
    subjects: PCM,
    skills: [['mechanics', 4, 'core'], ['calculus', 3, 'core'], ['cad-modelling', 4, 'core'], ['physical-chemistry', 2, 'helpful'], ['problem-solving', 4, 'core'], ['teamwork', 3, 'helpful'], ['spreadsheets', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'B.Tech Mechanical via JEE', 'in', 'science', ['jee-main', 'jee-advanced', 'bitsat'], 'B.Tech Mechanical Engineering (4 yrs)', ENGG_STEPS, 4, IIT_BTECH, 'Core PSU jobs via GATE are a common next step.', ['uni-in-iit-madras', 'uni-in-iit-bombay', 'uni-in-iit-kanpur', 'uni-in-bits-pilani', 'uni-in-vit-vellore']),
      p(s, 'germany-alt-uk', 'MEng Mechanical in the UK', 'uk', 'science', ['ielts', 'esat'], 'MEng Mechanical Engineering (4 yrs)', [['UCAS + ESAT', 1], ['MEng', 4]], 4, [125, 165, 210], 'Integrated master\'s is 4 years; ESAT needed for Imperial and Cambridge.', ['uni-uk-imperial', 'uni-uk-cambridge', 'uni-uk-manchester', 'uni-uk-edinburgh']),
    ],
    salLakh: [4, 9, 15, 30], abroad: ['uk', 36, 50], demand: 'medium', growth: 7,
    cities: [['Pune', 20], ['Chennai', 19], ['Bengaluru', 15], ['Delhi NCR', 14], ['Ahmedabad', 9]],
    recruiters: ['Tata Motors', 'Mahindra', 'L&T', 'Bosch', 'Ather Energy', 'BHEL'], style: ['Office and shop floor', 'Site visits', 'Team-based'],
    related: ['aerospace-engineer', 'civil-engineer', 'electronics-engineer'],
    sources: [NCS, AMB('mechanical-engineer'), BLS('architecture-and-engineering/mechanical-engineers.htm')],
  }),
  c({
    slug: 'civil-engineer', title: 'Civil Engineer', cluster: 'Engineering', streams: ['science'], riasec: ['R', 'I', 'C'], apt: [64, 62],
    summary: 'Plans and builds roads, bridges, metros, water systems and buildings.',
    day: 'Check site progress against drawings, review a structural calculation, meet contractors and sign off a concrete pour.',
    subjects: PCM,
    skills: [['mechanics', 4, 'core'], ['geometry', 3, 'core'], ['cad-modelling', 3, 'core'], ['geography-environment', 2, 'helpful'], ['problem-solving', 3, 'core'], ['leadership', 3, 'helpful'], ['spreadsheets', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'B.Tech Civil via JEE', 'in', 'science', ['jee-main', 'jee-advanced'], 'B.Tech Civil Engineering (4 yrs)', ENGG_STEPS, 4, IIT_BTECH, 'Government routes via GATE and ESE (UPSC) are common.', ['uni-in-iit-delhi', 'uni-in-iit-madras', 'uni-in-iit-kanpur', 'uni-in-vit-vellore']),
      p(s, 'canada', 'BASc Civil Engineering in Canada', 'ca', 'science', ['ielts'], 'BASc Civil Engineering (4 yrs)', [['OUAC application', 1], ['BASc', 4]], 4, CA_4YR, 'Licensing as a P.Eng needs 4 years of supervised work.', ['uni-ca-toronto', 'uni-ca-waterloo', 'uni-ca-ubc', 'uni-ca-mcmaster']),
    ],
    salLakh: [3.5, 7, 12, 28], abroad: ['ca', 42, 60], demand: 'medium', growth: 8,
    cities: [['Delhi NCR', 18], ['Mumbai', 17], ['Bengaluru', 12], ['Hyderabad', 11], ['Chennai', 9]],
    recruiters: ['L&T Construction', 'Tata Projects', 'Afcons', 'DMRC', 'NHAI', 'Shapoorji Pallonji'], style: ['Site-based', 'Fieldwork', 'Travel'],
    related: ['architect', 'mechanical-engineer', 'environmental-scientist'],
    sources: [NCS, AMB('civil-engineer'), BLS('architecture-and-engineering/civil-engineers.htm')],
  }),
  c({
    slug: 'electronics-engineer', title: 'Electronics and Electrical Engineer', cluster: 'Engineering', streams: ['science'], riasec: ['R', 'I'], apt: [62, 63],
    summary: 'Designs chips, circuits, embedded systems and power networks.',
    day: 'Simulate a circuit, debug firmware on a dev board, review a PCB layout with the team and test a batch of prototypes.',
    subjects: PCM,
    skills: [['electromagnetism', 4, 'core'], ['calculus', 4, 'core'], ['electronics-prototyping', 4, 'core'], ['python-programming', 2, 'helpful'], ['problem-solving', 4, 'core'], ['lab-techniques', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'B.Tech ECE / EE via JEE', 'in', 'science', ['jee-main', 'jee-advanced', 'bitsat'], 'B.Tech Electronics and Communication (4 yrs)', ENGG_STEPS, 4, IIT_BTECH, 'India\'s semiconductor push (ISM fabs) is creating VLSI roles.', ['uni-in-iit-bombay', 'uni-in-iit-madras', 'uni-in-iit-delhi', 'uni-in-bits-pilani', 'uni-in-iiit-hyderabad']),
      p(s, 'us', 'BS Electrical Engineering in the US', 'us', 'science', ['sat', 'toefl'], 'BS Electrical and Computer Engineering (4 yrs)', [['Applications', 1], ['BS', 4]], 4, US_4YR, 'STEM OPT allows 3 years of work.', ['uni-us-purdue', 'uni-us-georgia-tech', 'uni-us-uiuc', 'uni-us-umich', 'uni-us-ut-austin']),
    ],
    salLakh: [5, 14, 22, 45], abroad: ['us', 80, 120], demand: 'high', growth: 11,
    cities: [['Bengaluru', 35], ['Hyderabad', 17], ['Noida', 12], ['Chennai', 11], ['Pune', 8]],
    recruiters: ['Texas Instruments', 'Qualcomm', 'Intel', 'Tata Electronics', 'Siemens', 'Power Grid'], style: ['Lab and office', 'Team-based'],
    related: ['mechanical-engineer', 'aerospace-engineer', 'software-engineer'],
    sources: [NCS, AMB('electronics-engineer'), BLS('architecture-and-engineering/electrical-and-electronics-engineers.htm')],
  }),
  c({
    slug: 'aerospace-engineer', title: 'Aerospace Engineer', cluster: 'Engineering', streams: ['science'], riasec: ['I', 'R'], apt: [62, 64],
    summary: 'Designs and tests aircraft, satellites, rockets and drones.',
    day: 'Run aerodynamic simulations, review test data from a wind tunnel or engine run, and document design changes for certification.',
    subjects: PCM,
    skills: [['mechanics', 5, 'core'], ['calculus', 4, 'core'], ['cad-modelling', 4, 'core'], ['python-programming', 3, 'helpful'], ['electromagnetism', 3, 'helpful'], ['problem-solving', 4, 'core'], ['research', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'B.Tech Aerospace via JEE Advanced', 'in', 'science', ['jee-main', 'jee-advanced'], 'B.Tech Aerospace Engineering (4 yrs)', ENGG_STEPS, 4, IIT_BTECH, 'ISRO hires through its own ICRB exam; IIST is another route.', ['uni-in-iit-bombay', 'uni-in-iit-madras', 'uni-in-iit-kanpur']),
      p(s, 'us', 'BS Aerospace Engineering in the US', 'us', 'science', ['sat', 'toefl'], 'BS Aerospace Engineering (4 yrs)', [['Applications', 1], ['BS', 4]], 4, US_4YR, 'Defence roles need US citizenship; commercial space is more open.', ['uni-us-mit', 'uni-us-georgia-tech', 'uni-us-purdue', 'uni-us-umich', 'uni-us-ut-austin']),
      p(s, 'uk', 'MEng Aeronautical Engineering in the UK', 'uk', 'science', ['ielts', 'esat'], 'MEng Aeronautical Engineering (4 yrs)', [['UCAS + ESAT', 1], ['MEng', 4]], 4, [125, 165, 210], 'Rolls-Royce and Airbus UK recruit graduates.', ['uni-uk-imperial', 'uni-uk-cambridge', 'uni-uk-manchester']),
    ],
    salLakh: [5, 12, 20, 40], abroad: ['us', 85, 125], demand: 'medium', growth: 9,
    cities: [['Bengaluru', 45], ['Hyderabad', 18], ['Thiruvananthapuram', 9], ['Chennai', 8], ['Nagpur', 5]],
    recruiters: ['ISRO', 'HAL', 'Airbus India', 'Skyroot Aerospace', 'Agnikul', 'Boeing India'], style: ['Lab and test sites', 'Documentation-heavy'],
    related: ['mechanical-engineer', 'electronics-engineer', 'research-scientist'],
    sources: [NCS, AMB('aerospace-engineer'), BLS('architecture-and-engineering/aerospace-engineers.htm')],
  }),
  c({
    slug: 'architect', title: 'Architect', cluster: 'Design and built environment', streams: ['science'], riasec: ['A', 'R', 'I'], apt: [64, 81],
    summary: 'Designs buildings and spaces that are safe, useful and beautiful.',
    day: 'Sketch concepts for a client, develop drawings in AutoCAD and Revit, coordinate with structural engineers and visit a site.',
    subjects: [['maths', 60, true], ['physics', 55, true], ['chemistry', 50, false]],
    skills: [['drawing-sketching', 4, 'core'], ['cad-modelling', 4, 'core'], ['geometry', 4, 'core'], ['creative-design', 4, 'core'], ['mechanics', 2, 'helpful'], ['presentation', 3, 'core'], ['empathy', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'B.Arch via NATA or JEE Main Paper 2', 'in', 'science', ['nata', 'jee-main'], 'B.Arch (5 yrs)', [['NATA / JEE Paper 2 prep', 1], ['B.Arch incl. internship', 5]], 5, [8, 15, 28], 'Registration with the Council of Architecture after B.Arch.', ['uni-in-iit-kanpur', 'uni-in-manipal']),
      p(s, 'uk', 'BA Architecture (RIBA Part 1) in the UK', 'uk', 'science', ['ielts'], 'BA/BSc Architecture (3 yrs) + Part 2', [['UCAS + portfolio', 1], ['Part 1 degree', 3], ['Year out', 1], ['Part 2', 2]], 4, [130, 170, 220], 'Full UK qualification takes about 7 years; most return after Part 1 or 2.', ['uni-uk-ucl', 'uni-uk-cambridge', 'uni-uk-manchester', 'uni-uk-edinburgh']),
    ],
    salLakh: [3.5, 7, 12, 30], abroad: ['uk', 32, 45], demand: 'medium', growth: 6,
    cities: [['Mumbai', 20], ['Delhi NCR', 20], ['Bengaluru', 16], ['Ahmedabad', 10], ['Pune', 9]],
    recruiters: ['Morphogenesis', 'Studio Lotus', 'Hafeez Contractor', 'CP Kukreja', 'Jacobs', 'DLF'], style: ['Studio-based', 'Site visits', 'Client-facing'],
    related: ['civil-engineer', 'ux-designer', 'communication-designer'],
    sources: [NCS, AMB('architect'), ['Council of Architecture', 'https://www.coa.gov.in']],
  }),
  // ======================================================= Healthcare and life sciences
  c({
    slug: 'doctor', title: 'Doctor (MBBS)', cluster: 'Healthcare', streams: ['science'], riasec: ['I', 'S'], apt: [70, 72, 61],
    summary: 'Diagnoses and treats patients; most go on to specialise after MBBS.',
    day: 'Ward rounds, an outpatient clinic of 40 patients, reviewing test results and handing over to the night team.',
    subjects: [['biology', 80, true], ['chemistry', 75, true], ['physics', 70, true], ['english', 60, false]],
    skills: [['human-physiology', 5, 'core'], ['genetics', 4, 'core'], ['organic-chemistry', 3, 'core'], ['clinical-knowledge', 4, 'core'], ['empathy', 4, 'core'], ['spoken-communication', 4, 'core'], ['ethical-reasoning', 4, 'core'], ['time-management', 4, 'helpful']],
    pathways: (s) => [
      p(s, 'india-govt', 'MBBS at a government college via NEET', 'in', 'science', ['neet-ug'], 'MBBS (5.5 yrs incl. internship)', [['NEET preparation (often 1 drop year)', 2], ['MBBS + internship', 5.5]], 5.5, [4, 9, 16], 'Government seats cost little; coaching ₹1.5-4 lakh; NEET PG for specialisation.', MED_IN),
      p(s, 'india-pvt', 'MBBS at a private / deemed college via NEET', 'in', 'science', ['neet-ug'], 'MBBS (5.5 yrs)', [['NEET preparation', 2], ['MBBS + internship', 5.5]], 5.5, [60, 110, 160], 'Deemed-university MBBS fees run ₹15-30 lakh a year.', ['uni-in-manipal']),
      p(s, 'uk', 'MBBS / MBChB in the UK with UCAT', 'uk', 'science', ['ucat', 'ielts'], 'MBBS (5-6 yrs)', [['UCAS by 15 Oct + UCAT', 1], ['Medical degree', 5]], 5, [280, 360, 450], 'International places are very limited (about 7.5%); NHS foundation training after.', ['uni-uk-oxford', 'uni-uk-cambridge', 'uni-uk-imperial', 'uni-uk-kcl', 'uni-uk-edinburgh', 'uni-uk-manchester']),
    ],
    salLakh: [8, 14, 25, 60], abroad: ['uk', 42, 90], demand: 'very_high', growth: 9,
    cities: [['Delhi NCR', 16], ['Mumbai', 12], ['Bengaluru', 11], ['Chennai', 10], ['Hyderabad', 9]],
    recruiters: ['AIIMS', 'Apollo Hospitals', 'Fortis', 'Max Healthcare', 'Narayana Health', 'State health services'], style: ['Hospital-based', 'Shift and on-call', 'Patient-facing'],
    related: ['dentist', 'nurse', 'physiotherapist', 'pharmacist'],
    sources: [NCS, ['National Medical Commission', 'https://www.nmc.org.in'], ['Medical Counselling Committee', 'https://mcc.nic.in']],
  }),
  c({
    slug: 'dentist', title: 'Dentist (BDS)', cluster: 'Healthcare', streams: ['science'], riasec: ['I', 'R', 'S'], apt: [64, 72],
    summary: 'Diagnoses and treats problems of the teeth, gums and mouth.',
    day: 'Fillings, a root canal and two consultations in the morning; orthodontic reviews and lab-work checks after lunch.',
    subjects: [['biology', 70, true], ['chemistry', 65, true], ['physics', 60, true]],
    skills: [['human-physiology', 4, 'core'], ['clinical-knowledge', 4, 'core'], ['empathy', 4, 'core'], ['organic-chemistry', 3, 'helpful'], ['entrepreneurship', 3, 'helpful'], ['spoken-communication', 3, 'core']],
    pathways: (s) => [
      p(s, 'india', 'BDS via NEET', 'in', 'science', ['neet-ug'], 'BDS (5 yrs incl. internship)', [['NEET preparation', 2], ['BDS', 5]], 5, [6, 25, 60], 'Many dentists open their own clinic; setup costs ₹15-30 lakh.', ['uni-in-manipal', 'uni-in-aiims-delhi']),
    ],
    salLakh: [3, 6, 12, 30], demand: 'medium', growth: 6,
    cities: [['Delhi NCR', 15], ['Mumbai', 14], ['Bengaluru', 12], ['Chennai', 10], ['Pune', 8]],
    recruiters: ['Clove Dental', 'Sabka Dentist', 'Apollo White', 'Own clinic', 'Government hospitals'], style: ['Clinic-based', 'Patient-facing', 'Often self-employed'],
    related: ['doctor', 'pharmacist'],
    sources: [NCS, ['Dental Council of India', 'https://dciindia.gov.in'], AMB('dentist')],
  }),
  c({
    slug: 'pharmacist', title: 'Pharmacist', cluster: 'Healthcare', streams: ['science'], riasec: ['I', 'C', 'S'], apt: [72, 62],
    summary: 'Ensures medicines are safe and effective, in hospitals, pharma companies and regulatory roles.',
    day: 'Check prescriptions for interactions, counsel patients, or in industry run quality tests on a new batch.',
    subjects: [['chemistry', 65, true], ['biology', 60, false], ['maths', 60, false], ['physics', 55, true]],
    skills: [['organic-chemistry', 4, 'core'], ['physical-chemistry', 3, 'core'], ['human-physiology', 3, 'core'], ['lab-techniques', 4, 'core'], ['ethical-reasoning', 3, 'helpful'], ['written-communication', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'B.Pharm via state CETs / NEET-based admission', 'in', 'science', ['neet-ug', 'met-manipal'], 'B.Pharm (4 yrs)', [['Entrance', 1], ['B.Pharm', 4]], 4, [5, 9, 18], 'Pharm.D (6 yrs) suits hospital clinical roles.', ['uni-in-manipal', 'uni-in-bits-pilani']),
      p(s, 'canada', 'BSc Pharmacy in Canada', 'ca', 'science', ['ielts'], 'BSc Pharmacy / PharmD (4 yrs)', [['Applications', 1], ['Pre-pharmacy + PharmD', 6]], 6, [150, 200, 260], 'Long but leads to licensed practice.', ['uni-ca-toronto', 'uni-ca-ubc']),
    ],
    salLakh: [3, 6, 10, 22], abroad: ['ca', 70, 85], demand: 'medium', growth: 7,
    cities: [['Hyderabad', 20], ['Ahmedabad', 15], ['Mumbai', 15], ['Bengaluru', 10], ['Baddi', 6]],
    recruiters: ['Sun Pharma', "Dr. Reddy's", 'Cipla', 'Apollo Pharmacy', 'Biocon', 'CDSCO'], style: ['Lab or pharmacy-based', 'Regulated'],
    related: ['biotechnologist', 'doctor', 'research-scientist'],
    sources: [NCS, ['Pharmacy Council of India', 'https://www.pci.nic.in'], AMB('pharmacist')],
  }),
  c({
    slug: 'nurse', title: 'Registered Nurse', cluster: 'Healthcare', streams: ['science'], riasec: ['S', 'I'], apt: [61, 70],
    summary: 'Provides and coordinates patient care in hospitals, communities and abroad.',
    day: 'Hand-over, medication rounds for eight patients, wound care, updating charts and supporting a doctor during a procedure.',
    subjects: [['biology', 55, true], ['chemistry', 50, true], ['english', 55, true]],
    skills: [['human-physiology', 4, 'core'], ['clinical-knowledge', 3, 'core'], ['empathy', 5, 'core'], ['spoken-communication', 3, 'core'], ['teamwork', 4, 'core'], ['english-proficiency', 4, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'BSc Nursing (state or institutional entrance)', 'in', 'science', ['neet-ug'], 'BSc Nursing (4 yrs)', [['Entrance', 1], ['BSc Nursing', 4]], 4, [3, 7, 15], 'Indian-trained nurses are in demand in the UK, Gulf and Australia.', ['uni-in-cmc-vellore', 'uni-in-aiims-delhi', 'uni-in-manipal']),
      p(s, 'australia', 'Bachelor of Nursing in Australia', 'au', 'science', ['ielts'], 'Bachelor of Nursing (3 yrs)', [['Applications', 1], ['Degree', 3]], 3, AU_3YR, 'Registered nurse is on Australia\'s skilled occupation list.', ['uni-au-sydney', 'uni-au-monash', 'uni-au-uq']),
    ],
    salLakh: [2.5, 5, 8, 15], abroad: ['au', 45, 58], demand: 'very_high', growth: 10,
    cities: [['Delhi NCR', 14], ['Bengaluru', 12], ['Chennai', 12], ['Kochi', 10], ['Mumbai', 10]],
    recruiters: ['AIIMS', 'Apollo Hospitals', 'NHS (UK)', 'Manipal Hospitals', 'Aster DM', 'Fortis'], style: ['Hospital-based', 'Shift work', 'Patient-facing'],
    related: ['doctor', 'physiotherapist'],
    sources: [NCS, ['Indian Nursing Council', 'https://www.indiannursingcouncil.org'], AMB('staff-nurse')],
  }),
  c({
    slug: 'physiotherapist', title: 'Physiotherapist', cluster: 'Healthcare', streams: ['science'], riasec: ['S', 'R', 'I'], apt: [64, 70],
    summary: 'Helps people recover movement after injury, surgery or illness, including sports rehab.',
    day: 'Assess a post-surgery knee, run rehab sessions, plan exercises for a cricketer and update treatment notes.',
    subjects: [['biology', 60, true], ['physics', 55, true], ['chemistry', 50, true]],
    skills: [['human-physiology', 4, 'core'], ['mechanics', 3, 'helpful'], ['clinical-knowledge', 3, 'core'], ['empathy', 4, 'core'], ['spoken-communication', 3, 'core'], ['entrepreneurship', 2, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'BPT (Bachelor of Physiotherapy)', 'in', 'science', ['neet-ug', 'met-manipal'], 'BPT (4.5 yrs incl. internship)', [['Entrance', 1], ['BPT', 4.5]], 4.5, [4, 9, 18], 'Sports physio roles pay well with an MPT.', ['uni-in-manipal', 'uni-in-cmc-vellore']),
      p(s, 'australia', 'Physiotherapy in Australia', 'au', 'science', ['ielts'], 'Bachelor of Physiotherapy (4 yrs)', [['Applications', 1], ['Degree', 4]], 4, [120, 155, 190], 'Strong demand; on the skilled occupation list.', ['uni-au-sydney', 'uni-au-melbourne', 'uni-au-uq', 'uni-au-monash']),
    ],
    salLakh: [2.5, 5, 9, 20], abroad: ['au', 45, 60], demand: 'high', growth: 11,
    cities: [['Delhi NCR', 16], ['Mumbai', 14], ['Bengaluru', 13], ['Chennai', 9], ['Pune', 8]],
    recruiters: ['Fortis', 'Apollo', 'Sports teams and academies', 'Physio clinics', 'Own practice'], style: ['Clinic or hospital', 'Patient-facing', 'Active'],
    related: ['doctor', 'nurse'],
    sources: [NCS, AMB('physiotherapist')],
  }),
  c({
    slug: 'biotechnologist', title: 'Biotechnologist', cluster: 'Life sciences', streams: ['science'], riasec: ['I', 'R'], apt: [62, 72],
    summary: 'Uses living cells and molecules to make vaccines, drugs, enzymes and crops.',
    day: 'Run PCR and cell-culture experiments, analyse data, troubleshoot a protocol and present results at the lab meeting.',
    subjects: [['biology', 70, true], ['chemistry', 70, true], ['maths', 60, false], ['physics', 60, true]],
    skills: [['genetics', 5, 'core'], ['organic-chemistry', 4, 'core'], ['lab-techniques', 4, 'core'], ['statistics', 3, 'core'], ['research', 4, 'core'], ['python-programming', 2, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'B.Tech / BSc Biotechnology, then MSc or PhD', 'in', 'science', ['jee-main', 'iiser-iat', 'cuet-ug'], 'B.Tech or BS Biotechnology (4 yrs)', [['Entrance', 1], ['Degree', 4], ['MSc (most roles)', 2]], 6, [8, 14, 25], 'Research roles usually need a master\'s; PhD funded in India.', ['uni-in-iit-madras', 'uni-in-iisc-bengaluru', 'uni-in-vit-vellore', 'uni-in-manipal']),
      p(s, 'uk', 'BSc Biochemistry / Biomedical Sciences in the UK', 'uk', 'science', ['ielts'], 'BSc Biomedical Sciences (3 yrs)', [['UCAS', 1], ['BSc', 3]], 3, UK_3YR, 'Oxford-Cambridge-London golden triangle has many biotech start-ups.', ['uni-uk-imperial', 'uni-uk-ucl', 'uni-uk-kcl', 'uni-uk-edinburgh']),
    ],
    salLakh: [3.5, 7, 12, 28], abroad: ['uk', 30, 45], demand: 'medium', growth: 10,
    cities: [['Bengaluru', 26], ['Hyderabad', 24], ['Pune', 14], ['Ahmedabad', 9], ['Delhi NCR', 8]],
    recruiters: ['Biocon', 'Serum Institute', 'Bharat Biotech', 'Syngene', 'Strand Life Sciences', 'CSIR labs'], style: ['Lab-based', 'Research teams'],
    related: ['research-scientist', 'pharmacist', 'doctor'],
    sources: [NCS, AMB('biotechnologist'), ['Department of Biotechnology', 'https://dbtindia.gov.in']],
  }),
  c({
    slug: 'research-scientist', title: 'Research Scientist (Physical Sciences)', cluster: 'Life sciences', streams: ['science'], riasec: ['I'], apt: [62, 63, 316],
    summary: 'Discovers new knowledge in physics, chemistry or maths at universities, ISRO, DRDO or industry labs.',
    day: 'Design an experiment or simulation, read papers, analyse results, mentor a junior student and draft a paper.',
    subjects: PCM.map(([a, b, r]) => [a, Math.max(b, 80), r] as [string, number, boolean]),
    skills: [['calculus', 5, 'core'], ['mechanics', 4, 'core'], ['research', 5, 'core'], ['statistics', 4, 'core'], ['python-programming', 3, 'core'], ['written-communication', 4, 'core'], ['lab-techniques', 4, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'BS-MS at IISc / IISER, then PhD', 'in', 'science', ['iiser-iat', 'jee-advanced'], 'BS-MS (5 yrs) + PhD (5 yrs)', [['Entrance', 1], ['BS-MS', 5], ['PhD (stipend)', 5]], 10, [6, 10, 16], 'PhD stipends (₹37,000-42,000 a month) cover living costs.', ['uni-in-iisc-bengaluru', 'uni-in-iit-bombay', 'uni-in-iit-kanpur']),
      p(s, 'us', 'BS in the US, then funded PhD', 'us', 'science', ['sat', 'toefl'], 'BS (4 yrs) + funded PhD (5-6 yrs)', [['Applications', 1], ['BS', 4], ['PhD', 5]], 9, [180, 290, 380], 'US PhDs are fully funded; the cost is the undergraduate degree.', ['uni-us-mit', 'uni-us-stanford', 'uni-us-harvard', 'uni-us-uc-berkeley']),
    ],
    salLakh: [8, 14, 22, 45], abroad: ['us', 80, 120], demand: 'medium', growth: 6,
    cities: [['Bengaluru', 30], ['Delhi NCR', 15], ['Mumbai', 12], ['Pune', 10], ['Hyderabad', 10]],
    recruiters: ['ISRO', 'DRDO', 'BARC', 'TIFR', 'IISc', 'Shell Technology Centre'], style: ['Lab and desk', 'Self-directed', 'Long horizons'],
    related: ['aerospace-engineer', 'biotechnologist', 'ai-ml-engineer'],
    sources: [NCS, ['DST INSPIRE scheme', 'https://online-inspire.gov.in'], BLS('life-physical-and-social-science/physicists-and-astronomers.htm')],
  }),
  c({
    slug: 'environmental-scientist', title: 'Environmental Scientist', cluster: 'Life sciences', streams: ['science', 'humanities'], riasec: ['I', 'R', 'S'], apt: [62, 317],
    summary: 'Studies pollution, climate and ecosystems and advises on sustainability and compliance.',
    day: 'Collect water samples at a site, model emissions data, and write an environmental impact report for a client.',
    subjects: [['biology', 60, false], ['chemistry', 60, false], ['geography', 60, false], ['environmental', 60, false]],
    skills: [['geography-environment', 4, 'core'], ['statistics', 3, 'core'], ['lab-techniques', 3, 'core'], ['research', 4, 'core'], ['data-literacy', 3, 'core'], ['policy-analysis', 3, 'helpful'], ['written-communication', 3, 'core']],
    pathways: (s) => [
      p(s, 'india', 'BSc Environmental Science, then MSc', 'in', 'science', ['cuet-ug'], 'BSc (3 yrs) + MSc (2 yrs)', [['CUET', 1], ['BSc', 3], ['MSc', 2]], 5, [3, 6, 12], 'ESG and climate-finance roles are growing fast.', ['uni-in-ashoka', 'uni-in-christ-bengaluru', 'uni-in-iit-kanpur']),
      p(s, 'australia', 'Bachelor of Environmental Science in Australia', 'au', 'science', ['ielts'], 'Bachelor of Environmental Science (3 yrs)', [['Applications', 1], ['Degree', 3]], 3, AU_3YR, 'Australia has strong climate and water research.', ['uni-au-anu', 'uni-au-uq', 'uni-au-melbourne', 'uni-au-unsw']),
    ],
    salLakh: [3.5, 7, 12, 25], abroad: ['au', 42, 55], demand: 'high', growth: 13,
    cities: [['Delhi NCR', 22], ['Mumbai', 16], ['Bengaluru', 14], ['Pune', 9], ['Chennai', 8]],
    recruiters: ['ERM', 'WRI India', 'Tata Power', 'CEEW', 'KPMG ESG', 'Central Pollution Control Board'], style: ['Fieldwork and desk', 'Consulting'],
    related: ['policy-analyst', 'civil-engineer', 'research-scientist'],
    sources: [NCS, BLS('life-physical-and-social-science/environmental-scientists-and-specialists.htm')],
  }),
  // ======================================================= Finance and business
  c({
    slug: 'chartered-accountant', title: 'Chartered Accountant', cluster: 'Finance', streams: ['commerce'], riasec: ['C', 'E'], apt: [62, 68],
    summary: 'Audits companies, advises on tax and prepares the financial statements investors rely on.',
    day: 'Audit fieldwork at a client, reconcile ledgers, review GST filings and draft an audit observation for the partner.',
    subjects: [['accountancy', 75, true], ['economics', 60, false], ['maths', 60, false], ['business', 60, false]],
    skills: [['accounting', 5, 'core'], ['taxation-audit', 4, 'core'], ['spreadsheets', 4, 'core'], ['financial-literacy', 4, 'core'], ['ethical-reasoning', 4, 'core'], ['written-communication', 3, 'helpful'], ['commercial-awareness', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'CA via ICAI: Foundation, Intermediate, articleship, Final', 'in', 'commerce', ['ca-foundation'], 'CA (ICAI), often with a BCom alongside', [['CA Foundation after class 12', 0.6], ['CA Intermediate', 1], ['Articleship (paid stipend)', 2], ['CA Final', 1]], 5, [1.5, 3, 6], 'ICAI fees are about ₹1 lakh in total; coaching adds ₹1-3 lakh. Pass rates are low, so 5-6 years is typical.', ['uni-in-srcc-delhi', 'uni-in-christ-bengaluru']),
      p(s, 'uk', 'BSc Accounting and Finance + ACCA/ACA in the UK', 'uk', 'commerce', ['ielts'], 'BSc Accounting and Finance (3 yrs) + ACA', [['UCAS', 1], ['BSc', 3], ['ACA training contract', 3]], 3, UK_3YR, 'Big Four graduate schemes pay while you qualify.', ['uni-uk-lse', 'uni-uk-warwick', 'uni-uk-manchester', 'uni-uk-leeds']),
    ],
    salLakh: [7, 12, 22, 50], abroad: ['uk', 33, 60], demand: 'high', growth: 9,
    cities: [['Mumbai', 26], ['Delhi NCR', 22], ['Bengaluru', 14], ['Chennai', 8], ['Kolkata', 7]],
    recruiters: ['Deloitte', 'EY', 'KPMG', 'PwC', 'Grant Thornton Bharat', 'Reliance'], style: ['Office and client sites', 'Busy seasons', 'Detail-heavy'],
    related: ['financial-analyst', 'investment-banker', 'business-analyst'],
    sources: [['ICAI: CA course', 'https://www.icai.org'], AMB('chartered-accountant'), NCS],
  }),
  c({
    slug: 'investment-banker', title: 'Investment Banker', cluster: 'Finance', streams: ['commerce', 'science'], riasec: ['E', 'C', 'I'], apt: [62, 319],
    summary: 'Advises companies on mergers, acquisitions and raising capital through IPOs and debt.',
    day: 'Update a valuation model, build a pitch deck for a client, join diligence calls and work late on a live deal.',
    subjects: [['maths', 80, true], ['economics', 75, false], ['accountancy', 70, false]],
    skills: [['financial-modelling', 5, 'core'], ['accounting', 4, 'core'], ['spreadsheets', 5, 'core'], ['commercial-awareness', 4, 'core'], ['presentation', 4, 'core'], ['quantitative-reasoning', 4, 'core'], ['time-management', 4, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'BCom / Economics at a top college, then MBA', 'in', 'commerce', ['cuet-ug', 'ipmat-indore'], 'BCom/BA Economics (3 yrs) or IPM (5 yrs) + MBA', [['CUET / IPMAT', 1], ['UG', 3], ['Work', 2], ['MBA', 2]], 7, [12, 28, 45], 'IIM MBA fees are about ₹25 lakh; IPM Indore integrates UG and MBA.', ['uni-in-srcc-delhi', 'uni-in-iim-indore', 'uni-in-lsr-delhi', 'uni-in-ashoka']),
      p(s, 'uk', 'BSc Economics / Finance in London', 'uk', 'commerce', ['ielts', 'tmua'], 'BSc Economics or Finance (3 yrs)', [['UCAS + TMUA', 1], ['BSc', 3]], 3, [110, 140, 175], 'London summer internships convert to analyst offers.', ['uni-uk-lse', 'uni-uk-warwick', 'uni-uk-ucl', 'uni-uk-cambridge', 'uni-uk-oxford']),
      p(s, 'us', 'BS/BA Finance or Economics in the US', 'us', 'commerce', ['sat', 'toefl'], 'BS Finance / BA Economics (4 yrs)', [['Applications', 1], ['Degree', 4]], 4, US_4YR, 'Wall Street recruits heavily from target schools.', ['uni-us-nyu', 'uni-us-harvard', 'uni-us-umich', 'uni-us-uc-berkeley']),
    ],
    salLakh: [14, 30, 60, 150], abroad: ['uk', 75, 140], demand: 'medium', growth: 7,
    cities: [['Mumbai', 62], ['Delhi NCR', 16], ['Bengaluru', 12], ['Gurugram', 5], ['Chennai', 2]],
    recruiters: ['Kotak Investment Banking', 'JM Financial', 'Goldman Sachs', 'Morgan Stanley', 'Avendus', 'J.P. Morgan'], style: ['Long hours', 'Deal-driven', 'Client-facing'],
    related: ['financial-analyst', 'management-consultant', 'chartered-accountant'],
    sources: [NCS, AMB('investment-banking-analyst'), BLS('business-and-financial/financial-analysts.htm')],
  }),
  c({
    slug: 'financial-analyst', title: 'Financial Analyst', cluster: 'Finance', streams: ['commerce', 'science'], riasec: ['C', 'I', 'E'], apt: [62, 319],
    summary: 'Analyses companies, budgets and investments to guide business or investor decisions.',
    day: 'Update the monthly forecast, explain a cost overrun to a manager, and research a listed company for the investment committee.',
    subjects: [['maths', 70, true], ['accountancy', 65, false], ['economics', 65, false]],
    skills: [['financial-modelling', 4, 'core'], ['accounting', 4, 'core'], ['spreadsheets', 4, 'core'], ['statistics', 3, 'core'], ['commercial-awareness', 3, 'core'], ['written-communication', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'BCom / BBA + CFA Level 1-2', 'in', 'commerce', ['cuet-ug'], 'BCom (Hons) (3 yrs) + CFA', [['CUET', 1], ['BCom', 3], ['CFA levels', 1.5]], 3.5, [4, 8, 15], 'CFA exam fees are about ₹1.2-1.5 lakh per level.', ['uni-in-srcc-delhi', 'uni-in-christ-bengaluru', 'uni-in-flame-pune', 'uni-in-ashoka']),
      p(s, 'canada', 'BCom / BBA in Canada', 'ca', 'commerce', ['ielts'], 'Bachelor of Commerce (4 yrs)', [['Applications', 1], ['BCom', 4]], 4, CA_4YR, 'Toronto\'s Bay Street banks hire co-op students.', BIZ_CA),
    ],
    salLakh: [5, 9, 16, 35], abroad: ['ca', 45, 65], demand: 'high', growth: 10,
    cities: [['Mumbai', 30], ['Bengaluru', 20], ['Delhi NCR', 18], ['Hyderabad', 9], ['Pune', 8]],
    recruiters: ['HDFC Bank', 'Goldman Sachs (Bengaluru)', 'Morgan Stanley', 'ICICI Securities', 'Deloitte', 'American Express'], style: ['Desk-based', 'Deadline-driven'],
    related: ['investment-banker', 'chartered-accountant', 'actuary', 'data-analyst'],
    sources: [NCS, AMB('financial-analyst'), BLS('business-and-financial/financial-analysts.htm')],
  }),
  c({
    slug: 'actuary', title: 'Actuary', cluster: 'Finance', streams: ['commerce', 'science'], riasec: ['C', 'I'], apt: [62, 318, 68],
    summary: 'Uses maths and statistics to price insurance, pensions and financial risk.',
    day: 'Build a pricing model for a health product, test assumptions against claims data and present results to the risk committee.',
    subjects: [['maths', 85, true], ['applied-maths', 80, false], ['economics', 65, false]],
    skills: [['actuarial-maths', 4, 'core'], ['statistics', 5, 'core'], ['calculus', 4, 'core'], ['spreadsheets', 4, 'core'], ['python-programming', 3, 'helpful'], ['written-communication', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'BSc Statistics / Maths + IAI actuarial exams', 'in', 'commerce', ['cuet-ug'], 'BSc (3 yrs) + Institute of Actuaries of India exams', [['ACET (IAI entrance)', 0.5], ['BSc', 3], ['Actuarial papers while working', 4]], 3.5, [3, 6, 10], 'Pay rises with each paper passed; full fellowship takes 6-8 years.', ['uni-in-srcc-delhi', 'uni-in-christ-bengaluru', 'uni-in-ashoka']),
      p(s, 'uk', 'BSc Actuarial Science in the UK', 'uk', 'commerce', ['ielts', 'tmua'], 'BSc Actuarial Science (3 yrs)', [['UCAS', 1], ['BSc', 3]], 3, UK_3YR, 'Accredited degrees give exemptions from IFoA papers.', ['uni-uk-lse', 'uni-uk-warwick', 'uni-uk-leeds', 'uni-uk-kcl']),
    ],
    salLakh: [7, 12, 30, 70], abroad: ['uk', 40, 80], demand: 'medium', growth: 15,
    cities: [['Gurugram', 30], ['Mumbai', 26], ['Bengaluru', 22], ['Hyderabad', 8], ['Pune', 6]],
    recruiters: ['Swiss Re', 'LIC', 'Milliman', 'WTW', 'Aon', 'ICICI Lombard'], style: ['Desk-based', 'Exam-heavy early career'],
    related: ['financial-analyst', 'data-analyst', 'economist'],
    sources: [['Institute of Actuaries of India', 'https://www.actuariesindia.org'], AMB('actuary'), BLS('math/actuaries.htm')],
  }),
  c({
    slug: 'management-consultant', title: 'Management Consultant', cluster: 'Business', streams: ['commerce', 'science', 'humanities'], riasec: ['E', 'I', 'S'], apt: [61, 62, 316],
    summary: 'Helps companies solve their biggest problems: growth, cost, strategy and change.',
    day: 'Client workshop in the morning, analyse survey data, build slides with the team and pressure-test the storyline with the partner.',
    subjects: [['maths', 70, false], ['economics', 70, false], ['english', 70, true]],
    skills: [['problem-solving', 5, 'core'], ['commercial-awareness', 4, 'core'], ['presentation', 4, 'core'], ['spreadsheets', 4, 'core'], ['written-communication', 4, 'core'], ['teamwork', 4, 'core'], ['quantitative-reasoning', 4, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'Top UG (IIT / SRCC / IPM) then IIM MBA', 'in', 'commerce', ['ipmat-indore', 'cuet-ug', 'jee-main'], 'UG (3-4 yrs) + MBA (2 yrs)', [['Entrance', 1], ['UG', 3], ['Work', 2], ['MBA', 2]], 7, [10, 28, 40], 'MBB firms hire mainly from IIM A/B/C and IIT campuses.', ['uni-in-iim-indore', 'uni-in-srcc-delhi', 'uni-in-iit-bombay', 'uni-in-ashoka']),
      p(s, 'uk', 'BSc Management / Economics in the UK', 'uk', 'commerce', ['ielts'], 'BSc Management (3 yrs)', [['UCAS', 1], ['BSc', 3]], 3, UK_3YR, 'Big Four and boutique consultancies run graduate schemes.', BIZ_UK),
      p(s, 'canada', 'BBA / HBA in Canada', 'ca', 'commerce', ['ielts'], 'Honours Business Administration (4 yrs)', [['Applications', 1], ['Degree', 4]], 4, CA_4YR, 'Ivey (Western) and Rotman (Toronto) place into consulting.', BIZ_CA),
    ],
    salLakh: [12, 25, 45, 120], abroad: ['uk', 50, 90], demand: 'high', growth: 11,
    cities: [['Mumbai', 30], ['Gurugram', 28], ['Bengaluru', 22], ['Chennai', 6], ['Hyderabad', 6]],
    recruiters: ['McKinsey', 'BCG', 'Bain', 'Accenture Strategy', 'Deloitte', 'Kearney'], style: ['Travel', 'Client-facing', 'Long hours'],
    related: ['business-analyst', 'investment-banker', 'product-manager', 'economist'],
    sources: [NCS, AMB('management-consultant'), BLS('business-and-financial/management-analysts.htm')],
  }),
  c({
    slug: 'business-analyst', title: 'Business Analyst', cluster: 'Business', streams: ['commerce', 'science'], riasec: ['C', 'E', 'I'], apt: [62, 362],
    summary: 'Bridges business teams and tech teams: defines what to build and measures if it worked.',
    day: 'Interview users about a process, write requirements, check a dashboard and agree priorities with product and engineering.',
    subjects: [['maths', 65, true], ['economics', 60, false], ['business', 60, false], ['informatics', 60, false]],
    skills: [['spreadsheets', 4, 'core'], ['sql-databases', 3, 'core'], ['data-visualisation', 3, 'core'], ['written-communication', 4, 'core'], ['problem-solving', 4, 'core'], ['commercial-awareness', 3, 'core'], ['empathy', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'BBA / BCom / B.Tech + analytics', 'in', 'commerce', ['cuet-ug', 'christ-entrance'], 'BBA / BCom (3 yrs)', [['Entrance', 1], ['Degree', 3]], 3, [3, 8, 18], 'Fast entry; an MBA later boosts pay.', ['uni-in-christ-bengaluru', 'uni-in-flame-pune', 'uni-in-srcc-delhi', 'uni-in-manipal']),
      p(s, 'canada', 'BCom / BBA in Canada with co-op', 'ca', 'commerce', ['ielts'], 'BCom / BBA (4 yrs)', [['Applications', 1], ['Degree', 4]], 4, CA_4YR, 'Co-op terms build a local CV.', BIZ_CA),
      p(s, 'uk', 'BSc Business Management in the UK', 'uk', 'commerce', ['ielts'], 'BSc Business Management (3 yrs)', [['UCAS', 1], ['BSc', 3]], 3, UK_3YR, 'Graduate Route visa: 18 months to find work.', BIZ_UK),
    ],
    salLakh: [5, 10, 16, 32], abroad: ['ca', 42, 60], demand: 'high', growth: 14,
    cities: [['Bengaluru', 30], ['Hyderabad', 15], ['Pune', 14], ['Delhi NCR', 15], ['Mumbai', 12]],
    recruiters: ['Accenture', 'TCS', 'Amazon', 'Paytm', 'Capgemini', 'ZS Associates'], style: ['Desk-based', 'Meetings-heavy', 'Hybrid'],
    related: ['data-analyst', 'product-manager', 'management-consultant'],
    sources: [NCS, AMB('business-analyst')],
  }),
  c({
    slug: 'product-manager', title: 'Product Manager', cluster: 'Technology', streams: ['science', 'commerce'], riasec: ['E', 'I', 'A'], apt: [362, 61, 62],
    summary: 'Decides what a tech product should do next and leads designers and engineers to ship it.',
    day: 'Review user metrics, run a design review, prioritise the backlog with engineering and talk to three customers.',
    subjects: [['maths', 70, false], ['computer-science', 60, false], ['english', 65, true]],
    skills: [['problem-solving', 4, 'core'], ['empathy', 4, 'core'], ['data-literacy', 4, 'core'], ['written-communication', 4, 'core'], ['leadership', 4, 'core'], ['sql-databases', 2, 'helpful'], ['ui-ux-tools', 2, 'helpful'], ['commercial-awareness', 4, 'core']],
    pathways: (s) => [
      p(s, 'india', 'B.Tech, a few years as engineer/analyst, then APM or MBA', 'in', 'science', ['jee-main', 'bitsat'], 'B.Tech (4 yrs) + 2-3 yrs work', [['Entrance', 1], ['B.Tech', 4], ['Engineer or analyst', 2]], 6, IIT_BTECH, 'Some companies hire APMs straight from IIT/BITS campuses.', ['uni-in-iit-bombay', 'uni-in-iit-delhi', 'uni-in-bits-pilani', 'uni-in-iim-indore']),
      p(s, 'us', 'CS or Economics in the US, then APM programme', 'us', 'science', ['sat', 'toefl'], 'BS (4 yrs)', [['Applications', 1], ['BS', 4]], 4, US_4YR, 'Google and Meta APM programmes hire new grads.', ['uni-us-stanford', 'uni-us-uc-berkeley', 'uni-us-carnegie-mellon', 'uni-us-umich']),
    ],
    salLakh: [15, 30, 50, 100], abroad: ['us', 110, 160], demand: 'high', growth: 13,
    cities: [['Bengaluru', 48], ['Delhi NCR', 18], ['Mumbai', 12], ['Hyderabad', 10], ['Pune', 6]],
    recruiters: ['Flipkart', 'Razorpay', 'Swiggy', 'Google', 'Microsoft', 'Zomato'], style: ['Hybrid', 'Meetings-heavy', 'Cross-functional'],
    related: ['software-engineer', 'business-analyst', 'ux-designer', 'entrepreneur'],
    sources: [NCS, AMB('product-manager')],
  }),
  c({
    slug: 'marketing-manager', title: 'Marketing Manager', cluster: 'Business', streams: ['commerce', 'humanities'], riasec: ['E', 'A', 'S'], apt: [61, 81],
    summary: 'Plans how a brand reaches and persuades customers, across digital, retail and media.',
    day: 'Review campaign performance, brief an agency on a new ad, plan the festive-season budget and check social sentiment.',
    subjects: [['business', 65, false], ['economics', 60, false], ['english', 65, true]],
    skills: [['digital-marketing', 4, 'core'], ['commercial-awareness', 4, 'core'], ['creative-design', 2, 'helpful'], ['data-literacy', 3, 'core'], ['presentation', 4, 'core'], ['written-communication', 4, 'core'], ['empathy', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'BBA / BMS then MBA Marketing', 'in', 'commerce', ['cuet-ug', 'ipmat-indore', 'christ-entrance'], 'BBA (3 yrs) + MBA (2 yrs)', [['Entrance', 1], ['BBA', 3], ['Work', 1], ['MBA', 2]], 6, [8, 20, 35], 'FMCG management-trainee roles after an MBA pay best.', ['uni-in-iim-indore', 'uni-in-flame-pune', 'uni-in-christ-bengaluru', 'uni-in-srcc-delhi']),
      p(s, 'uk', 'BSc Marketing / Management in the UK', 'uk', 'commerce', ['ielts'], 'BSc Marketing (3 yrs)', [['UCAS', 1], ['BSc', 3]], 3, UK_3YR, 'Graduate schemes at Unilever UK, P&G, Diageo.', ['uni-uk-leeds', 'uni-uk-nottingham', 'uni-uk-manchester', 'uni-uk-warwick']),
    ],
    salLakh: [5, 10, 20, 45], abroad: ['uk', 32, 50], demand: 'high', growth: 10,
    cities: [['Mumbai', 30], ['Delhi NCR', 22], ['Bengaluru', 22], ['Hyderabad', 7], ['Chennai', 6]],
    recruiters: ['Hindustan Unilever', 'ITC', 'Nestlé', 'Asian Paints', 'Nykaa', 'Ogilvy'], style: ['Office-based', 'Agency collaboration', 'Creative and analytical'],
    related: ['public-relations-manager', 'entrepreneur', 'communication-designer', 'product-manager'],
    sources: [NCS, AMB('marketing-manager'), BLS('management/advertising-promotions-and-marketing-managers.htm')],
  }),
  c({
    slug: 'entrepreneur', title: 'Entrepreneur / Startup Founder', cluster: 'Business', streams: ['commerce', 'science', 'humanities'], riasec: ['E', 'A', 'I'], apt: [362, 366],
    summary: 'Starts and grows a new business, from first customer to a funded team.',
    day: 'Talk to customers, fix a sales problem, interview a hire, review cash in the bank and pitch an investor.',
    subjects: [['business', 60, false], ['english', 60, false], ['maths', 60, false]],
    skills: [['entrepreneurship', 5, 'core'], ['leadership', 4, 'core'], ['commercial-awareness', 4, 'core'], ['spoken-communication', 4, 'core'], ['financial-literacy', 4, 'core'], ['problem-solving', 4, 'core'], ['digital-marketing', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'Any strong UG + build while studying (incubators, Startup India)', 'in', 'commerce', ['cuet-ug', 'ipmat-indore', 'jee-main'], 'BBA / BTech / BA + incubator', [['UG with projects', 3], ['First venture or startup job', 2]], 3, [4, 12, 30], 'Most founders first work 2-3 years at a startup; cost depends on the college.', ['uni-in-ashoka', 'uni-in-flame-pune', 'uni-in-iit-bombay', 'uni-in-iim-indore', 'uni-in-bits-pilani']),
      p(s, 'us', 'US degree + startup ecosystem', 'us', 'commerce', ['sat', 'toefl'], 'BS / BA (4 yrs)', [['Applications', 1], ['Degree', 4]], 4, US_4YR, 'Visa rules make founding in the US hard right after graduation.', ['uni-us-stanford', 'uni-us-mit', 'uni-us-harvard', 'uni-us-northeastern']),
    ],
    salLakh: [0, 8, 25, 100], demand: 'medium', growth: 12,
    cities: [['Bengaluru', 35], ['Delhi NCR', 25], ['Mumbai', 20], ['Pune', 6], ['Hyderabad', 6]],
    recruiters: ['Self', 'Startup India', 'Y Combinator', 'Sequoia (Peak XV)', 'Accel', 'Blume Ventures'], style: ['High risk', 'Long hours', 'Varied'],
    related: ['product-manager', 'marketing-manager', 'management-consultant'],
    sources: [['Startup India', 'https://www.startupindia.gov.in'], NCS],
  }),
  c({
    slug: 'economist', title: 'Economist', cluster: 'Finance', streams: ['commerce', 'humanities'], riasec: ['I', 'C', 'E'], apt: [62, 317, 318],
    summary: 'Studies data on markets, prices and policy to forecast and advise governments, banks and companies.',
    day: 'Update an inflation model, read RBI and IMF releases, write a research note and brief a client on what it means.',
    subjects: [['economics', 80, true], ['maths', 75, true], ['applied-maths', 70, false]],
    skills: [['macroeconomics', 5, 'core'], ['microeconomics', 5, 'core'], ['statistics', 4, 'core'], ['calculus', 3, 'core'], ['python-programming', 3, 'helpful'], ['written-communication', 4, 'core'], ['research', 4, 'core']],
    pathways: (s) => [
      p(s, 'india', 'BA Economics (Hons) then MA (DSE / JNU / ISI)', 'in', 'commerce', ['cuet-ug'], 'BA Economics (3-4 yrs) + MA (2 yrs)', [['CUET', 1], ['BA', 3], ['MA', 2]], 5, [3, 7, 15], 'Indian Economic Service (UPSC) and RBI Grade B are government routes.', ['uni-in-srcc-delhi', 'uni-in-lsr-delhi', 'uni-in-ashoka', 'uni-in-flame-pune']),
      p(s, 'uk', 'BSc Economics in the UK', 'uk', 'commerce', ['ielts', 'tmua'], 'BSc Economics (3 yrs)', [['UCAS + TMUA', 1], ['BSc', 3]], 3, UK_3YR, 'Government Economic Service and consultancies hire graduates.', ['uni-uk-lse', 'uni-uk-ucl', 'uni-uk-warwick', 'uni-uk-oxford', 'uni-uk-cambridge']),
    ],
    salLakh: [6, 12, 20, 45], abroad: ['uk', 38, 60], demand: 'medium', growth: 8,
    cities: [['Delhi NCR', 34], ['Mumbai', 30], ['Bengaluru', 14], ['Chennai', 5], ['Hyderabad', 5]],
    recruiters: ['RBI', 'NITI Aayog', 'CRISIL', 'ICRIER', 'World Bank', 'Goldman Sachs'], style: ['Desk-based', 'Research and writing'],
    related: ['policy-analyst', 'financial-analyst', 'data-analyst', 'actuary'],
    sources: [NCS, BLS('life-physical-and-social-science/economists.htm'), ['UPSC Indian Economic Service', 'https://upsc.gov.in']],
  }),
  c({
    slug: 'supply-chain-manager', title: 'Supply Chain Manager', cluster: 'Business', streams: ['commerce', 'science'], riasec: ['E', 'C', 'R'], apt: [62, 366],
    summary: 'Gets products from suppliers to customers on time and at the right cost.',
    day: 'Check warehouse stock, re-route a delayed shipment, negotiate with a transporter and review delivery metrics.',
    subjects: [['maths', 65, false], ['business', 60, false], ['economics', 60, false]],
    skills: [['spreadsheets', 4, 'core'], ['data-literacy', 3, 'core'], ['problem-solving', 4, 'core'], ['leadership', 3, 'core'], ['commercial-awareness', 3, 'core'], ['spoken-communication', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'BBA / B.Tech, then MBA Operations', 'in', 'commerce', ['cuet-ug', 'jee-main'], 'UG (3-4 yrs) + MBA', [['Entrance', 1], ['UG', 3], ['MBA', 2]], 5, [8, 18, 30], 'Quick-commerce has created many entry roles.', ['uni-in-iim-indore', 'uni-in-christ-bengaluru', 'uni-in-vit-vellore']),
      p(s, 'canada', 'BCom Supply Chain in Canada', 'ca', 'commerce', ['ielts'], 'BCom (4 yrs)', [['Applications', 1], ['BCom', 4]], 4, CA_4YR, 'Logistics roles are in demand in Toronto and Vancouver.', ['uni-ca-york', 'uni-ca-ubc', 'uni-ca-mcmaster']),
    ],
    salLakh: [4, 8, 15, 35], abroad: ['ca', 40, 58], demand: 'high', growth: 12,
    cities: [['Mumbai', 20], ['Delhi NCR', 22], ['Bengaluru', 18], ['Chennai', 10], ['Pune', 8]],
    recruiters: ['Amazon', 'Flipkart', 'Delhivery', 'Blinkit', 'Maersk', 'Tata Steel'], style: ['Warehouse and office', 'Problem-solving on the fly'],
    related: ['business-analyst', 'management-consultant'],
    sources: [NCS, AMB('supply-chain-manager')],
  }),
  // ======================================================= Law, policy and public life
  c({
    slug: 'corporate-lawyer', title: 'Lawyer (Corporate and Litigation)', cluster: 'Law', streams: ['humanities', 'commerce'], riasec: ['E', 'I', 'S'], apt: [61, 65, 66],
    summary: 'Advises clients on deals and disputes, drafts contracts and argues cases in court.',
    day: 'Draft a share-purchase agreement, research case law for a dispute, join a client call and review a junior\'s memo.',
    subjects: [['english', 75, true], ['legal-studies', 70, false], ['political-science', 65, false], ['history', 60, false]],
    skills: [['legal-concepts', 4, 'core'], ['legal-drafting', 4, 'core'], ['logical-reasoning', 4, 'core'], ['critical-thinking', 4, 'core'], ['written-communication', 5, 'core'], ['debate-advocacy', 3, 'helpful'], ['commercial-awareness', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'Five-year BA LLB at a National Law University via CLAT', 'in', 'humanities', ['clat', 'ailet'], 'BA LLB (Hons) (5 yrs)', [['CLAT prep in class 11-12', 1.5], ['BA LLB', 5]], 5, [10, 18, 28], 'NLU fees are ₹2.5-3.5 lakh a year incl. hostel; CLAT coaching ₹60,000-1.5 lakh.', LAW_IN),
      p(s, 'uk', 'LLB in the UK, then SQE (or return to India via Bar Council)', 'uk', 'humanities', ['lnat', 'ielts'], 'LLB (3 yrs)', [['UCAS + LNAT', 1], ['LLB', 3], ['SQE / Indian enrolment', 1]], 4, [110, 140, 175], 'Practising in India after a UK LLB needs Bar Council of India recognition steps.', LAW_UK),
    ],
    salLakh: [12, 18, 40, 150], abroad: ['uk', 50, 120], demand: 'high', growth: 9,
    cities: [['Mumbai', 34], ['Delhi NCR', 34], ['Bengaluru', 14], ['Chennai', 6], ['Hyderabad', 5]],
    recruiters: ['Cyril Amarchand Mangaldas', 'Shardul Amarchand Mangaldas', 'AZB & Partners', 'Khaitan & Co', 'Trilegal', 'Supreme Court chambers'], style: ['Long hours', 'Research and writing', 'Client-facing'],
    related: ['policy-analyst', 'civil-services-officer', 'journalist'],
    sources: [['Consortium of NLUs (CLAT)', 'https://consortiumofnlus.ac.in'], ['Bar Council of India', 'https://www.barcouncilofindia.org'], AMB('associate-lawyer')],
  }),
  c({
    slug: 'civil-services-officer', title: 'Civil Services Officer (IAS / IPS / IFS)', cluster: 'Public service', streams: ['humanities', 'science', 'commerce'], riasec: ['S', 'E', 'I'], apt: [61, 66, 366],
    summary: 'Runs districts, ministries and embassies; selected through the UPSC Civil Services Examination.',
    day: 'As a district collector: review a flood-relief plan, hold a public hearing, inspect a hospital and chair a meeting on schemes.',
    subjects: [['history', 60, false], ['political-science', 60, false], ['geography', 60, false], ['economics', 60, false]],
    skills: [['polity-governance', 5, 'core'], ['history-analysis', 4, 'core'], ['geography-environment', 4, 'core'], ['written-communication', 5, 'core'], ['leadership', 4, 'core'], ['ethical-reasoning', 5, 'core'], ['spoken-communication', 4, 'core'], ['policy-analysis', 4, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'Any graduation, then UPSC Prelims, Mains and Interview', 'in', 'humanities', ['cuet-ug'], 'Any bachelor\'s degree (3 yrs) + UPSC', [['Bachelor\'s degree', 3], ['UPSC preparation (avg 2-3 attempts)', 2.5]], 5.5, [4, 8, 15], 'Coaching ₹1.5-3 lakh plus Delhi living costs; salary starts at Level 10 (₹56,100 basic).', ['uni-in-srcc-delhi', 'uni-in-lsr-delhi', 'uni-in-ashoka', 'uni-in-iit-delhi']),
    ],
    salLakh: [10, 12, 22, 32], demand: 'low', growth: 2,
    cities: [['All of India (cadre-based)', 100]],
    recruiters: ['Union Public Service Commission', 'Government of India', 'State governments'], style: ['Field postings', 'Transfers every 2-3 years', 'High responsibility'],
    related: ['policy-analyst', 'corporate-lawyer', 'economist'],
    sources: [['UPSC Civil Services Examination', 'https://upsc.gov.in'], ['7th Pay Commission pay matrix', 'https://doe.gov.in']],
  }),
  c({
    slug: 'policy-analyst', title: 'Public Policy Analyst', cluster: 'Public service', streams: ['humanities', 'commerce'], riasec: ['I', 'S', 'E'], apt: [61, 317, 320],
    summary: 'Researches social problems and recommends policies to governments, think tanks and NGOs.',
    day: 'Analyse survey data on a welfare scheme, interview officials, write a policy brief and present it to a ministry team.',
    subjects: [['political-science', 65, false], ['economics', 65, false], ['english', 65, true], ['sociology', 60, false]],
    skills: [['policy-analysis', 4, 'core'], ['research', 4, 'core'], ['polity-governance', 4, 'core'], ['statistics', 3, 'core'], ['written-communication', 4, 'core'], ['critical-thinking', 4, 'core'], ['data-literacy', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'BA Political Science / Economics, then MPP', 'in', 'humanities', ['cuet-ug', 'ashoka-aptitude'], 'BA (3-4 yrs) + Master of Public Policy (2 yrs)', [['Entrance', 1], ['BA', 3], ['MPP or fellowship', 2]], 5, [5, 12, 25], 'Fellowships like LAMP and CM fellowships are common entry points.', LIB_IN),
      p(s, 'uk', 'BSc Politics / PPE in the UK', 'uk', 'humanities', ['ielts', 'tsa'], 'BSc Politics and Economics (3 yrs)', [['UCAS', 1], ['BSc', 3]], 3, UK_3YR, 'Think tanks in London hire graduates as researchers.', ['uni-uk-lse', 'uni-uk-oxford', 'uni-uk-ucl', 'uni-uk-kcl', 'uni-uk-warwick']),
    ],
    salLakh: [4, 8, 15, 30], abroad: ['uk', 30, 45], demand: 'medium', growth: 9,
    cities: [['Delhi NCR', 55], ['Mumbai', 12], ['Bengaluru', 12], ['Chennai', 5], ['Pune', 5]],
    recruiters: ['NITI Aayog', 'J-PAL South Asia', 'CPR', 'PRS Legislative Research', 'Dalberg', 'UNDP India'], style: ['Research and writing', 'Field visits'],
    related: ['civil-services-officer', 'economist', 'journalist', 'corporate-lawyer'],
    sources: [NCS, ['PRS Legislative Research', 'https://prsindia.org']],
  }),
  c({
    slug: 'journalist', title: 'Journalist', cluster: 'Media', streams: ['humanities'], riasec: ['A', 'S', 'I'], apt: [61, 66, 67],
    summary: 'Finds, verifies and tells stories for newspapers, TV, digital and podcasts.',
    day: 'Pitch a story, call sources, attend a press conference, write and fact-check the piece and record a short video version.',
    subjects: [['english', 75, true], ['political-science', 60, false], ['history', 60, false]],
    skills: [['journalism-reporting', 4, 'core'], ['written-communication', 5, 'core'], ['research', 4, 'core'], ['critical-thinking', 4, 'core'], ['spoken-communication', 4, 'core'], ['ethical-reasoning', 4, 'core'], ['data-literacy', 2, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'BA Journalism / English, then PG diploma (IIMC / ACJ)', 'in', 'humanities', ['cuet-ug', 'christ-entrance'], 'BA (3 yrs) + PG Diploma (1 yr)', [['Entrance', 1], ['BA', 3], ['PG Diploma', 1]], 4, [3, 7, 14], 'A strong clip portfolio matters more than the degree.', ['uni-in-lsr-delhi', 'uni-in-christ-bengaluru', 'uni-in-ashoka', 'uni-in-flame-pune']),
      p(s, 'uk', 'BA Journalism / English in the UK', 'uk', 'humanities', ['ielts'], 'BA Journalism (3 yrs)', [['UCAS', 1], ['BA', 3]], 3, UK_3YR, 'Competitive; many work freelance at first.', ['uni-uk-leeds', 'uni-uk-kcl', 'uni-uk-edinburgh']),
    ],
    salLakh: [3, 6, 12, 30], abroad: ['uk', 28, 40], demand: 'low', growth: 3,
    cities: [['Delhi NCR', 40], ['Mumbai', 25], ['Bengaluru', 12], ['Chennai', 8], ['Kolkata', 6]],
    recruiters: ['The Hindu', 'Indian Express', 'NDTV', 'The Print', 'Scroll', 'Reuters'], style: ['Deadline-driven', 'Fieldwork', 'Irregular hours'],
    related: ['public-relations-manager', 'policy-analyst', 'communication-designer'],
    sources: [NCS, BLS('media-and-communication/reporters-correspondents-and-broadcast-news-analysts.htm')],
  }),
  c({
    slug: 'public-relations-manager', title: 'Public Relations and Communications Manager', cluster: 'Media', streams: ['humanities', 'commerce'], riasec: ['E', 'S', 'A'], apt: [61, 66],
    summary: 'Shapes how the public sees a company, leader or cause through media, events and crisis communication.',
    day: 'Pitch a founder interview to journalists, draft a press release, prep a spokesperson and track media coverage.',
    subjects: [['english', 70, true], ['business', 55, false], ['political-science', 55, false]],
    skills: [['spoken-communication', 5, 'core'], ['written-communication', 4, 'core'], ['debate-advocacy', 3, 'helpful'], ['leadership', 3, 'core'], ['commercial-awareness', 3, 'core'], ['digital-marketing', 3, 'helpful'], ['empathy', 3, 'core']],
    pathways: (s) => [
      p(s, 'india', 'BA Mass Communication / BMS', 'in', 'humanities', ['cuet-ug', 'christ-entrance'], 'BA / BMS (3 yrs)', [['Entrance', 1], ['Degree', 3]], 3, [3, 7, 14], 'Agencies hire interns; a strong network matters.', ['uni-in-christ-bengaluru', 'uni-in-flame-pune', 'uni-in-lsr-delhi']),
    ],
    salLakh: [3.5, 6, 14, 35], demand: 'medium', growth: 8,
    cities: [['Mumbai', 32], ['Delhi NCR', 34], ['Bengaluru', 18], ['Hyderabad', 5], ['Chennai', 4]],
    recruiters: ['Adfactors PR', 'Edelman India', 'Ogilvy PR', 'Avian WE', 'Corporate communications teams'], style: ['Client-facing', 'Events', 'Crisis on-call'],
    related: ['journalist', 'marketing-manager'],
    sources: [NCS, BLS('media-and-communication/public-relations-specialists.htm')],
  }),
  c({
    slug: 'psychologist', title: 'Psychologist (Clinical / Counselling)', cluster: 'Healthcare', streams: ['humanities', 'science'], riasec: ['S', 'I', 'A'], apt: [61, 66],
    summary: 'Assesses and supports mental health through therapy, testing and counselling.',
    day: 'Four therapy sessions, a psychometric assessment, case notes and supervision with a senior clinician.',
    subjects: [['psychology', 70, false], ['biology', 60, false], ['english', 65, true]],
    skills: [['psychology-foundations', 5, 'core'], ['empathy', 5, 'core'], ['spoken-communication', 4, 'core'], ['ethical-reasoning', 5, 'core'], ['research', 3, 'helpful'], ['statistics', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'BA/BSc Psychology, MA/MSc, then M.Phil Clinical (RCI)', 'in', 'humanities', ['cuet-ug', 'christ-entrance'], 'BA (3 yrs) + MA (2 yrs) + M.Phil (2 yrs) for clinical', [['Entrance', 1], ['BA', 3], ['MA', 2], ['M.Phil (RCI) for clinical', 2]], 7, [5, 10, 20], 'Counselling roles open after MA; RCI licence needed to practise clinically.', ['uni-in-christ-bengaluru', 'uni-in-lsr-delhi', 'uni-in-ashoka', 'uni-in-flame-pune']),
      p(s, 'australia', 'Psychology in Australia (APAC-accredited)', 'au', 'humanities', ['ielts'], 'BPsych (Hons) (4 yrs) + Masters', [['Applications', 1], ['BPsych Hons', 4], ['Masters', 2]], 6, [150, 190, 240], 'Registration needs a 6-year sequence.', ['uni-au-melbourne', 'uni-au-unsw', 'uni-au-uq', 'uni-au-monash']),
    ],
    salLakh: [3, 6, 12, 30], abroad: ['au', 50, 70], demand: 'high', growth: 14,
    cities: [['Delhi NCR', 22], ['Mumbai', 20], ['Bengaluru', 20], ['Chennai', 9], ['Pune', 8]],
    recruiters: ['NIMHANS', 'Fortis Mental Health', 'Schools and colleges', 'Amaha', 'Private practice'], style: ['Clinic or school', 'Client-facing', 'Emotionally demanding'],
    related: ['teacher', 'doctor', 'ux-designer'],
    sources: [['Rehabilitation Council of India', 'https://rehabcouncil.nic.in'], NCS, BLS('life-physical-and-social-science/psychologists.htm')],
  }),
  c({
    slug: 'teacher', title: 'Teacher / Educator', cluster: 'Education', streams: ['humanities', 'science', 'commerce'], riasec: ['S', 'A', 'I'], apt: [61, 66],
    summary: 'Teaches and mentors students in schools, coaching centres or online.',
    day: 'Teach four periods, run a lab or discussion, mark assignments, meet a parent and plan next week\'s lessons.',
    subjects: [['english', 60, true]],
    skills: [['spoken-communication', 4, 'core'], ['empathy', 4, 'core'], ['presentation', 4, 'core'], ['time-management', 3, 'core'], ['written-communication', 3, 'core'], ['ai-tool-fluency', 3, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'Subject degree + B.Ed, then CTET / school hiring', 'in', 'humanities', ['cuet-ug'], 'BA/BSc (3 yrs) + B.Ed (2 yrs), or 4-yr ITEP', [['Entrance', 1], ['Degree', 3], ['B.Ed', 2]], 5, [3, 6, 12], 'International-board schools (IB/Cambridge) pay 1.5-2x CBSE schools.', ['uni-in-lsr-delhi', 'uni-in-christ-bengaluru', 'uni-in-ashoka']),
    ],
    salLakh: [3, 5, 9, 18], demand: 'high', growth: 6,
    cities: [['Delhi NCR', 18], ['Bengaluru', 14], ['Mumbai', 14], ['Hyderabad', 9], ['Chennai', 9]],
    recruiters: ['Kendriya Vidyalaya', 'DPS schools', 'International schools', 'PhysicsWallah', 'Unacademy', 'Teach For India'], style: ['School hours', 'People-heavy'],
    related: ['psychologist', 'research-scientist'],
    sources: [['CTET', 'https://ctet.nic.in'], NCS],
  }),
  // ======================================================= Design and creative
  c({
    slug: 'ux-designer', title: 'UX / Product Designer', cluster: 'Design', streams: ['science', 'humanities', 'commerce'], riasec: ['A', 'I', 'S'], apt: [64, 81, 368],
    summary: 'Designs how apps and websites work and feel, grounded in user research.',
    day: 'Run two user interviews, turn findings into Figma wireframes, review prototypes with engineers and test a new flow.',
    subjects: [['english', 60, false], ['computer-science', 55, false]],
    skills: [['ui-ux-tools', 4, 'core'], ['empathy', 4, 'core'], ['creative-design', 4, 'core'], ['research', 3, 'core'], ['presentation', 3, 'core'], ['web-development', 2, 'helpful'], ['problem-solving', 4, 'core']],
    pathways: (s) => [
      p(s, 'india', 'B.Des via NID DAT or UCEED', 'in', 'humanities', ['nid-dat', 'uceed'], 'B.Des Interaction / Communication Design (4 yrs)', [['Design entrance prep', 1], ['B.Des', 4]], 4, [8, 16, 28], 'NID and IIT Bombay (IDC) are the top routes; portfolio matters most.', DESIGN_IN),
      p(s, 'us', 'BS Human-Computer Interaction / Design in the US', 'us', 'humanities', ['sat', 'toefl'], 'BS HCI or Design (4 yrs)', [['Applications + portfolio', 1], ['Degree', 4]], 4, US_4YR, 'CMU is the best-known HCI programme.', ['uni-us-carnegie-mellon', 'uni-us-umich', 'uni-us-northeastern', 'uni-us-georgia-tech']),
    ],
    salLakh: [6, 12, 25, 50], abroad: ['us', 85, 120], demand: 'high', growth: 15,
    cities: [['Bengaluru', 44], ['Delhi NCR', 18], ['Mumbai', 14], ['Pune', 9], ['Hyderabad', 9]],
    recruiters: ['Flipkart', 'Swiggy', 'CRED', 'Microsoft', 'Adobe', 'Lollypop Design'], style: ['Studio and hybrid', 'Collaborative'],
    related: ['product-manager', 'communication-designer', 'game-developer', 'architect'],
    sources: [NCS, AMB('ux-designer')],
  }),
  c({
    slug: 'communication-designer', title: 'Communication / Graphic Designer', cluster: 'Design', streams: ['humanities', 'commerce'], riasec: ['A', 'E'], apt: [64, 81],
    summary: 'Creates brand identities, illustrations, packaging, motion graphics and campaigns.',
    day: 'Sketch logo directions, build social creatives, present concepts to a client and finalise print files.',
    subjects: [['english', 55, false]],
    skills: [['creative-design', 5, 'core'], ['drawing-sketching', 4, 'core'], ['ui-ux-tools', 2, 'helpful'], ['presentation', 3, 'core'], ['digital-marketing', 2, 'helpful'], ['time-management', 3, 'core']],
    pathways: (s) => [
      p(s, 'india', 'B.Des Communication Design via NID DAT / UCEED', 'in', 'humanities', ['nid-dat', 'uceed'], 'B.Des (4 yrs)', [['Design entrance prep', 1], ['B.Des', 4]], 4, [6, 14, 25], 'Freelancing alongside a job is common.', DESIGN_IN),
      p(s, 'uk', 'BA Graphic Communication in the UK', 'uk', 'humanities', ['ielts'], 'BA Graphic Design (3 yrs)', [['UCAS + portfolio', 1], ['BA', 3]], 3, UK_3YR, 'London agencies are competitive; portfolio is key.', ['uni-uk-leeds', 'uni-uk-edinburgh']),
    ],
    salLakh: [3, 6, 12, 25], abroad: ['uk', 27, 38], demand: 'medium', growth: 8,
    cities: [['Mumbai', 28], ['Bengaluru', 24], ['Delhi NCR', 24], ['Pune', 8], ['Ahmedabad', 6]],
    recruiters: ['Ogilvy', 'Lowe Lintas', 'Landor', 'Elephant Design', 'In-house brand teams', 'Freelance'], style: ['Studio-based', 'Deadlines', 'Creative'],
    related: ['ux-designer', 'marketing-manager', 'fashion-designer'],
    sources: [NCS, BLS('arts-and-design/graphic-designers.htm')],
  }),
  c({
    slug: 'fashion-designer', title: 'Fashion Designer', cluster: 'Design', streams: ['humanities', 'commerce'], riasec: ['A', 'E', 'R'], apt: [64, 81],
    summary: 'Designs clothing and accessories, from sketches to production-ready collections.',
    day: 'Research trends, sketch a capsule collection, fit samples on a model and visit the production unit.',
    subjects: [['english', 55, false]],
    skills: [['creative-design', 5, 'core'], ['drawing-sketching', 4, 'core'], ['garment-construction', 4, 'core'], ['commercial-awareness', 3, 'helpful'], ['entrepreneurship', 3, 'helpful'], ['presentation', 3, 'core']],
    pathways: (s) => [
      p(s, 'india', 'B.Des Fashion via NIFT / NID entrance', 'in', 'humanities', ['nid-dat'], 'B.Des Fashion Design (4 yrs)', [['Entrance prep', 1], ['B.Des', 4]], 4, [8, 16, 28], 'NIFT runs its own entrance; NID has textile and apparel design.', ['uni-in-nid-ahmedabad', 'uni-in-flame-pune']),
    ],
    salLakh: [3, 5, 10, 30], demand: 'medium', growth: 7,
    cities: [['Mumbai', 26], ['Delhi NCR', 30], ['Bengaluru', 16], ['Tiruppur', 8], ['Jaipur', 6]],
    recruiters: ['Fabindia', 'Sabyasachi', 'Aditya Birla Fashion', 'Reliance Trends', 'H&M India', 'Own label'], style: ['Studio and factory', 'Seasonal deadlines'],
    related: ['communication-designer', 'entrepreneur'],
    sources: [['NIFT', 'https://www.nift.ac.in'], NCS],
  }),
  c({
    slug: 'hotel-manager', title: 'Hotel and Hospitality Manager', cluster: 'Hospitality', streams: ['commerce', 'humanities'], riasec: ['E', 'S', 'C'], apt: [366, 368],
    summary: 'Runs hotel operations so guests are looked after and the property makes money.',
    day: 'Morning briefing, check occupancy and complaints, walk the property, handle a VIP arrival and review the food cost report.',
    subjects: [['english', 60, true], ['business', 55, false]],
    skills: [['hospitality-operations', 4, 'core'], ['empathy', 4, 'core'], ['leadership', 4, 'core'], ['spoken-communication', 4, 'core'], ['spreadsheets', 3, 'helpful'], ['english-proficiency', 4, 'helpful']],
    pathways: (s) => [
      p(s, 'india', 'BHM via NCHM JEE or Manipal WGSHA', 'in', 'commerce', ['met-manipal'], 'Bachelor of Hotel Management (4 yrs)', [['Entrance', 1], ['BHM incl. industrial training', 4]], 4, [6, 12, 22], 'Management-trainee programmes at Taj (IHCL) and Oberoi (STEP) are the fast track.', ['uni-in-manipal', 'uni-in-christ-bengaluru']),
      p(s, 'australia', 'Bachelor of Hospitality / Business in Australia', 'au', 'commerce', ['ielts'], 'Bachelor of Business (Hospitality) (3 yrs)', [['Applications', 1], ['Degree', 3]], 3, AU_3YR, 'Post-study work rights help start a career abroad.', ['uni-au-uq', 'uni-au-monash']),
    ],
    salLakh: [3, 5, 10, 30], abroad: ['au', 38, 52], demand: 'medium', growth: 9,
    cities: [['Mumbai', 18], ['Delhi NCR', 18], ['Goa', 12], ['Bengaluru', 12], ['Jaipur', 8]],
    recruiters: ['IHCL (Taj)', 'Oberoi Group', 'Marriott', 'ITC Hotels', 'Hyatt', 'Accor'], style: ['Shift work', 'Guest-facing', 'On your feet'],
    related: ['marketing-manager', 'entrepreneur'],
    sources: [NCS, ['NCHMCT', 'https://nchm.gov.in'], AMB('hotel-manager')],
  }),
];
