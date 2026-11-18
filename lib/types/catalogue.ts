/**
 * Catalogue types (W4 Catalogues). Data lives in /data/catalogues/*.json, each file wrapped in DataFile<T>.
 *
 * Consumers:
 *  - W3 engine 5 (tutor matching) reads Tutor.
 *  - W3 engine 6 (career mapping) reads Career, Skill, CareerPathway, Resource (course hours and rupees).
 *  - Application support (Wave 2) reads University.
 *
 * Conventions: money is integer rupees (Inr); hours are decimals to 0.1; dates are ISO "YYYY-MM-DD"
 * (deadlines are local to the university); timestamps are ISO UTC.
 * Subjects are referenced by W2's subject slug (e.g. "maths", "physics") plus boards and grades, because a
 * tutor or career spans many subject IDs. Build a subject ID with subjectId(board, grade, slug) from lib/ids.
 */
import type { Board, Grade, Hours, Inr, Stream } from './enums';

// ---------------------------------------------------------------- shared

/** ISO calendar date, "YYYY-MM-DD". */
export type IsoDate = string;

/** A checkable fact. verified=true means it was taken from sourceUrl on asOf; false means realistic but unconfirmed. */
export interface Sourced<T> {
  value: T;
  sourceUrl: string;
  asOf: IsoDate;
  verified: boolean;
  note?: string;
}

/** 1 Beginner, 2 Developing, 3 Proficient, 4 Advanced, 5 Expert. */
export type SkillLevel = 1 | 2 | 3 | 4 | 5;

/** Holland RIASEC codes, matching the career-interest inventory in profile parameter p200. */
export type Riasec = 'R' | 'I' | 'A' | 'S' | 'E' | 'C';

export type Weekday = 'mon' | 'tue' | 'wed' | 'thu' | 'fri' | 'sat' | 'sun';

// ---------------------------------------------------------------- exams

export const EXAM_KINDS = ['india_entrance', 'abroad_admission', 'english', 'professional'] as const;
export type ExamKind = (typeof EXAM_KINDS)[number];

/** Entrance and admission exams referenced by careers and universities. id is a plain slug, e.g. "jee-main". */
export interface EntranceExam {
  id: string;
  name: string; // "JEE Main"
  fullName: string; // "Joint Entrance Examination (Main)"
  kind: ExamKind;
  conductedBy: string;
  /** Usual sitting months, e.g. ["Jan", "Apr"]. */
  sittings: string[];
  /** Grade in which students normally sit it. */
  typicalGrade: Grade | 'after_12';
  subjects: string[];
  feeInr: Inr;
  /** Typical serious-preparation hours. */
  prepHours: Hours;
  scoreFormat: string; // "Percentile (NTA score)", "400-1600"
  website: string;
}

// ---------------------------------------------------------------- tutors

export const TEACHING_STYLES = ['concept_first', 'practice_first', 'socratic', 'exam_focused', 'project_based'] as const;
export type TeachingStyle = (typeof TEACHING_STYLES)[number];

export const TUTOR_AUDIENCES = ['school', 'competitive_exam', 'college', 'english_learners', 'career_learners'] as const;
export type TutorAudience = (typeof TUTOR_AUDIENCES)[number];

export const HELP_TYPES = ['concept_learning', 'exam_prep', 'homework', 'skill_development'] as const;
export type HelpType = (typeof HELP_TYPES)[number];

export type SessionFormat = 'one_to_one' | 'group';
export type SessionMode = 'online' | 'offline';
export type HomeworkPolicy = 'every_session' | 'weekly' | 'on_request';

/** What a tutor teaches in one subject family. */
export interface TutorSubject {
  /** W2 subject slug, e.g. "maths", "physics", "accountancy". */
  subjectSlug: string;
  boards: Board[];
  grades: Grade[];
  /**
   * Kebab topic tags the tutor is strong in, e.g. "rotational-motion", "fractions", "organic-chemistry".
   * Tutor matching treats a gap as a topic match when a tag's words appear in the slugified chapter or subtopic name.
   */
  topicStrengths: string[];
}

/** A bookable weekly window in the tutor's time zone. Times "HH:MM" 24h. */
export interface AvailabilitySlot {
  day: Weekday;
  start: string;
  end: string;
}

export interface TutorReview {
  author: string; // "Aarav's parent", "Kabir, Class 9"
  rating: 1 | 2 | 3 | 4 | 5;
  text: string;
  date: IsoDate;
}

export interface Tutor {
  id: string; // tut_{first}_{last}
  firstName: string;
  lastName: string;
  displayName: string; // "Rahul Verma"
  gender: 'female' | 'male';
  city: string;
  timeZone: string; // "Asia/Kolkata"
  headline: string; // one line under the name in Explore Tutors
  bio: string; // 2-3 sentences
  qualifications: string[];
  yearsExperience: number;
  subjects: TutorSubject[];
  /** Exams the tutor prepares students for: EntranceExam ids, e.g. "jee-main", "sat". */
  examPrep: string[];
  audiences: TutorAudience[];
  helpTypes: HelpType[];
  /** First entry is the primary style. */
  teachingStyles: TeachingStyle[];
  formats: SessionFormat[];
  modes: SessionMode[];
  /** Only set when modes includes offline. */
  offlineArea?: string;
  languages: string[]; // "English", "Hindi", "Tamil" ...
  homework: HomeworkPolicy;
  idealStudent: string;
  availability: AvailabilitySlot[];
  sessionMinutes: 45 | 60 | 90;
  maxSessionsPerDay: number;
  pricing: {
    oneToOnePerHourInr: Inr;
    /** Per student per hour; null when the tutor does not take groups. */
    groupPerStudentPerHourInr: Inr | null;
    groupSize: [number, number] | null;
    /** 0 = free demo. */
    demoInr: Inr;
    demoMinutes: number;
    packages: { label: string; sessions: number; priceInr: Inr }[];
  };
  /** Platform fee share, 0.15 = 15%. */
  platformFeeRate: number;
  rating: number; // 0-5, one decimal
  reviewsCount: number;
  /** Share of students who booked again after the first paid session, 0-100. */
  rebookPct: number;
  sessionsCompleted: number;
  responseTimeHours: number;
  verified: boolean;
  verification: { identity: boolean; qualification: boolean; experience: boolean };
  joinedOn: IsoDate;
  profileStrengthPct: number;
  reviews: TutorReview[];
}

// ---------------------------------------------------------------- resources and courses

export const RESOURCE_FORMATS = ['textbook', 'video', 'practice', 'past_papers', 'interactive', 'course', 'test_series', 'mentorship'] as const;
export type ResourceFormat = (typeof RESOURCE_FORMATS)[number];

export interface Resource {
  /** res-{slug} for free resources, course-{slug} for paid courses. */
  id: string;
  kind: 'free_resource' | 'paid_course';
  title: string;
  provider: string; // "NCERT", "Khan Academy", "Coursera (Google)"
  format: ResourceFormat;
  url: string;
  description: string;
  /** W2 subject slugs this resource teaches; empty for pure skill courses. */
  subjectSlugs: string[];
  boards: Board[];
  grades: Grade[];
  /** Skills this resource builds (skill ids), with the level reached on completion. */
  skillOutcomes: { skillId: string; toLevel: SkillLevel }[];
  examIds: string[];
  topicTags: string[];
  /** Typical hours to complete. */
  hours: Hours;
  /** 0 for free resources. */
  priceInr: Inr;
  language: string[];
  certificate: boolean;
  rating?: number;
}

// ---------------------------------------------------------------- skills

export const SKILL_KINDS = ['academic', 'future', 'technical', 'domain'] as const;
export type SkillKind = (typeof SKILL_KINDS)[number];

export interface Skill {
  id: string; // skill-{slug}
  name: string;
  kind: SkillKind;
  category: string; // "Quantitative", "Communication", "Digital", "Business", "Science", "Law and society", "Creative", "Health"
  description: string;
  /** Exactly five descriptors, index 0 = level 1. */
  levelDescriptors: [string, string, string, string, string];
  /**
   * Typical hours to move up one level outside school (used when no mastery-model hours apply).
   * Index 0 = hours from 0 to level 1, index 4 = level 4 to level 5.
   */
  hoursPerLevel: [Hours, Hours, Hours, Hours, Hours];
  /** Academic skills: W2 subject slugs whose mastery evidences this skill. Hours then come from the mastery model. */
  subjectSlugs: string[];
  /** 430-profile parameters that hold evidence for this skill, e.g. ["p216"]. */
  profileParamIds: string[];
  /** Free and paid resources that build it (resource ids). */
  resourceIds: string[];
}

// ---------------------------------------------------------------- careers

export const DEMAND_LEVELS = ['very_high', 'high', 'medium', 'low'] as const;
export type DemandLevel = (typeof DEMAND_LEVELS)[number];

export interface CareerSkillRequirement {
  skillId: string;
  targetLevel: SkillLevel;
  importance: 'core' | 'helpful';
}

export interface CareerSubjectRequirement {
  subjectSlug: string;
  /** Grade 12 board percentage or equivalent the pathway expects. */
  minPercent: number;
  required: boolean;
}

/** One way into the career. Every career has at least one India pathway; most also have an abroad one. */
export interface CareerPathway {
  id: string; // "{careerSlug}-india", "{careerSlug}-uk"
  label: string; // "B.Tech CSE via JEE Main", "BSc Computer Science in the UK"
  region: 'india' | 'abroad';
  country: 'in' | 'us' | 'uk' | 'ca' | 'au';
  stream: Exclude<Stream, 'none'>;
  examIds: string[];
  degree: string; // "B.Tech Computer Science (4 yrs)"
  steps: { stage: string; years: number }[];
  /** Years from finishing class 12 to first paid job in the role. */
  yearsToEntry: number;
  /** Total cost from class 12 to entry: tuition + living + coaching/exams, rupees. */
  costInr: { low: Inr; typical: Inr; high: Inr };
  costNote: string;
  universityIds: string[];
}

export interface Career {
  id: string; // career-{slug}
  title: string;
  cluster: string; // "Technology", "Healthcare", "Finance", "Law", "Design", ...
  summary: string;
  dayInLife: string;
  /** Streams that lead in naturally. */
  streams: Exclude<Stream, 'none'>[];
  riasec: Riasec[]; // top 2-3 codes, strongest first
  /** Aptitude evidence the fit engine reads (430-profile parameter ids), e.g. numerical reasoning p62. */
  aptitudeParamIds: string[];
  subjects: CareerSubjectRequirement[];
  skills: CareerSkillRequirement[];
  pathways: CareerPathway[];
  /** Annual salary in India, rupees. */
  salaryInr: { entryLow: Inr; entryHigh: Inr; mid: Inr; senior: Inr };
  /** Abroad salary where an abroad pathway exists, converted to rupees per year at fxNote rate. */
  abroadSalaryInr?: { country: 'us' | 'uk' | 'ca' | 'au'; entry: Inr; mid: Inr };
  demand: DemandLevel;
  /** Expected annual growth in openings, percent. */
  growthPct: number;
  /** Share of Indian openings by city, percents summing to <= 100. */
  topCities: { city: string; sharePct: number }[];
  topRecruiters: string[];
  workStyle: string[]; // "Desk-based", "Shift work", "Fieldwork", "Client-facing"
  relatedCareerIds: string[];
  sources: { label: string; url: string; asOf: IsoDate }[];
}

// ---------------------------------------------------------------- universities

export type CountryCode = 'in' | 'us' | 'uk' | 'ca' | 'au';

export const APPLICATION_TYPES = [
  'early_decision',
  'early_decision_2',
  'early_action',
  'restrictive_early_action',
  'regular',
  'rolling',
  'ucas_oxbridge_medicine',
  'ucas_equal_consideration',
  'ouac',
  'direct',
  'josaa',
  'cuet',
  'institutional_exam',
  'merit',
] as const;
export type ApplicationType = (typeof APPLICATION_TYPES)[number];

export type ApplicationPlatform =
  | 'common_app'
  | 'uc_application'
  | 'coalition'
  | 'ucas'
  | 'ouac'
  | 'university_portal'
  | 'josaa'
  | 'cuet_samarth'
  | 'csab';

export interface ApplicationRequirements {
  /** Board percentage (CBSE) or equivalent the route expects for a competitive Indian applicant. */
  minBoardPercent?: number;
  /** A level / IB offer, e.g. "A*A*A", "IB 40 with 7,7,6 HL". */
  typicalOffer?: string;
  testPolicy: 'required' | 'optional' | 'blind' | 'not_applicable';
  /** Middle 50% SAT, when published. */
  satMid50?: [number, number];
  /** Exam ids that must or may be submitted. */
  examIds: string[];
  ielts?: number;
  toefl?: number;
  essays: { prompt: string; wordLimit: number }[];
  recommendations: number;
  /** Other items: "Mid-year report", "Personal statement (4,000 chars)", "Interview", "Portfolio", "ESAT" ... */
  otherItems: string[];
  applicationFeeInr: Inr;
}

export interface ApplicationRoute {
  type: ApplicationType;
  platform: ApplicationPlatform;
  /** Deadline for the 2027 intake. */
  deadline: Sourced<IsoDate>;
  decisionBy?: IsoDate;
  binding: boolean;
  requirements: ApplicationRequirements;
}

export interface Programme {
  id: string; // "{uniId}-{slug}"
  name: string; // "BSc Computer Science"
  degree: string; // "BSc", "B.Tech", "BA LLB (Hons)"
  field: string; // "computer-science", "business", "law", "medicine" ...
  durationYears: number;
  careerIds: string[];
  /** Overrides the route requirements for this programme, e.g. a higher offer. */
  typicalOffer?: string;
  entryExamIds: string[];
  /** Indian institutes: closing rank or percentile for the general category, last round. */
  cutoff?: Sourced<string>;
}

export interface Scholarship {
  name: string;
  amount: Sourced<string>; // "Up to 100% of demonstrated need", "₹50,000 a year"
  /** Rupee value per year for the cost engine; 0 when need-based and unknown. */
  valueInrPerYear: Inr;
  eligibility: string;
  deadline?: IsoDate;
  needBased: boolean;
}

export interface University {
  id: string; // uni-{country}-{slug}
  name: string;
  shortName: string;
  country: CountryCode;
  city: string;
  region: string; // state / province
  type: 'public' | 'private';
  website: string;
  founded: number;
  qsWorldRank: Sourced<number | null>;
  nirfRank?: Sourced<number | null>;
  acceptanceRatePct: Sourced<number | null>;
  intlStudentPct: Sourced<number | null>;
  /** Selectivity tier used for Reach / Target / Safe grouping before personal data is applied. */
  selectivity: 'most_selective' | 'highly_selective' | 'selective' | 'moderate' | 'accessible';
  /** Tuition for an international (or Indian, for India) undergraduate, per year. */
  tuition: Sourced<{ amount: number; currency: 'INR' | 'USD' | 'GBP' | 'CAD' | 'AUD' }>;
  tuitionInrPerYear: Inr;
  livingInrPerYear: Inr;
  /** Typical total cost of the full UG degree in rupees (tuition + living, before aid). */
  totalCostInr: Inr;
  programmes: Programme[];
  applicationRoutes: ApplicationRoute[];
  scholarships: Scholarship[];
  strengths: string[]; // "Computer science", "Economics"
  /** Graduate outcome headline numbers for Job Insights (PDF 9e). */
  outcomes?: { employmentRatePct: Sourced<number>; medianStartingSalaryInr: Sourced<Inr>; topRecruiters: string[] };
  /** Admit-trend points for the detail page chart. */
  admitTrend?: { year: number; ratePct: number }[];
}

/** Exchange rates used to convert foreign money to rupees across the catalogues. */
export interface FxTable {
  asOf: IsoDate;
  sourceUrl: string;
  inrPer: { USD: number; GBP: number; CAD: number; AUD: number };
}
