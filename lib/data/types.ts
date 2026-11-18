/**
 * Record types for the W2-0 data layer. These are also the FILE CONTRACT for
 * data/personas/students/{learnerId}/*.json (Wave 3 personas) and data/fixtures/students/{learnerId}/*.json:
 * every file is a DataFile<T> ({ schemaVersion: 1, generatedBy, items: T[] }) of the type named below.
 * See docs/data-layer.md for the file list.
 *
 * Shared contract types (Gap, MasteryState, AlrSnapshot, ProfileValue, EvidenceEvent, ItemResponse, Question...)
 * come from @/lib/types; this file only adds what the screens need on top.
 */
import type {
  AlrSnapshot,
  ApplicationType,
  Band,
  Board,
  CareerFit,
  CareerGapResult,
  Gap,
  GapCode,
  Grade,
  Inr,
  IsoUtc,
  ItemResponse,
  Level,
  MasteryState,
  NextAction,
  Role,
  SessionFormat,
  SessionMode,
  Stream,
  StudyWindow,
  Timetable,
  TimetableBlock,
  InterventionPlan,
} from './engine-types';
import type { Tutor } from '@/lib/types';

/** Local date, YYYY-MM-DD (Asia/Kolkata unless the person says otherwise). */
export type LocalDate = string;

export type PlanId = 'free' | 'application_support' | 'full_package';

// ------------------------------------------------------------------ people

/** students/{id}/student.json (one item). */
export interface Student {
  id: string; // lrn_
  role: 'student';
  firstName: string;
  lastName: string;
  name: string;
  board: Board;
  grade: Grade;
  stream: Stream;
  /** "CBSE Class 9", "Cambridge A Level (Commerce)". */
  programme: string;
  school: string;
  city: string;
  /** Medium of instruction, e.g. "English". */
  medium?: string;
  /** Planning band (latest measured ALR band, else onboarding band). */
  band: Band;
  plan: PlanId;
  /** Subjects the student takes; depth 'full' has history, 'light' only a few marks. */
  subjects: { subjectId: string; depth: 'full' | 'light' }[];
  /** Weekly study windows outside school, local time. */
  availability: StudyWindow[];
  /** Hours a week outside class across all subjects. */
  weeklyHours: number;
  tzOffsetMinutes: number;
  onboardedUtc?: IsoUtc;
  joinedUtc: IsoUtc;
  parentIds: string[];
  counsellorIds: string[];
  mentorIds: string[];
  tutorIds: string[];
  sectionIds: string[];
  /** Chapters the school is teaching now (first one drives the timetable's chapter block). */
  currentChapterIds?: string[];
  /** One-line goal, e.g. "JEE 2028", "BSc Business, UK". */
  goal?: string;
  /** Profile completion 0-100 (Home and NBA use it). */
  profileCompletionPct: number;
  /** Short story from the persona picker. */
  story?: string;
  avatar?: string;
}

/** adults/{parents,teachers,counsellors,mentors}.json. Tutors live in data/catalogues/tutors.json. */
export interface Adult {
  id: string; // par_ tch_ csl_ mnt_
  role: Exclude<Role, 'student' | 'tutor'>;
  firstName: string;
  lastName: string;
  name: string;
  city?: string;
  email?: string;
  phone?: string;
  headline?: string;
  /** Children (parent), caseload (counsellor, mentor), taught learners (teacher). */
  learnerIds: string[];
  /** Teachers: their section ids. */
  sectionIds?: string[];
  /** Counsellors: 'academic_wellbeing' | 'applications'; mentors: 'careers'. */
  focus?: string;
  /** Parents: relation per learner. */
  relation?: Record<string, 'mother' | 'father' | 'guardian'>;
  subjectIds?: string[];
  school?: string;
}

export type Person = Student | Adult | { id: string; role: 'tutor'; name: string };

// ------------------------------------------------------------------ assessment history

export type AttemptKind = 'onboarding' | 'chapter_check' | 'weekly' | 'mock' | 'retention_probe' | 'practice_form' | 'assigned';

/** students/{id}/attempts.json */
export interface Attempt {
  id: string; // att_{learner}_{n} or any unique string
  learnerId: string;
  kind: AttemptKind;
  title: string;
  subjectId: string;
  chapterId?: string;
  /** Who assigned it (tch_, tut_, csl_) or undefined for self/system. */
  assignedBy?: string;
  /** Task this attempt fulfils, if any. */
  taskId?: string;
  questionIds: string[];
  responses: ItemResponse[];
  startedUtc: IsoUtc;
  submittedUtc: IsoUtc;
  minutesAllotted: number;
  /** Marks scored / max marks. */
  score: number;
  maxScore: number;
  status: 'submitted' | 'abandoned';
}

/** students/{id}/gaps.json. Contract Gap plus what the Gap Log and screens show. */
export interface GapRecord extends Gap {
  chapterId: string;
  subjectId: string;
  /** Attempt that produced the current diagnosis. */
  attemptId?: string;
  detectedUtc: IsoUtc;
  updatedUtc: IsoUtc;
  closedUtc?: IsoUtc;
  /** Planning band used for hours. */
  band: Band;
  /** Weeks to close at the student's weekly hours; null when unknown. */
  weeks: number | null;
  scorePct: number;
  confirmingProbe: string | null;
  likelyCauses: string | null;
  prerequisiteToProbe: string | null;
  /** Teacher validation of the diagnosis (parameter #430, Gap Log). */
  validation?: { byId: string; utc: IsoUtc; verdict: 'confirmed' | 'corrected' | 'rejected'; correctedCode?: GapCode; note?: string };
}

/** students/{id}/mastery.json: contract MasteryState plus where it sits. */
export interface MasteryRecord extends MasteryState {
  chapterId: string;
  subjectId: string;
}

/** students/{id}/alr.json: one snapshot per chapter per date. */
export interface AlrRecord extends AlrSnapshot {
  subjectId: string;
  asOfUtc: IsoUtc;
  /** Indices left out of the LRS because evidence was missing. */
  missing?: string[];
  action?: string | null;
}

export interface AlrSummary {
  /** Latest snapshot per chapter. */
  chapters: AlrRecord[];
  /** Every snapshot, oldest first (for trend charts). */
  history: AlrRecord[];
  /** Year to date across chapters (mean of latest per chapter); null indices when no data. */
  overall: { dK: number | null; R: number | null; TQ: number | null; CE: number | null; ECV: number | null; MCI: number | null; LRS: number | null; band: Band | null };
}

/** students/{id}/plans.json: one intervention plan per diagnosis round. */
export interface PlanRecord {
  id: string;
  learnerId: string;
  createdUtc: IsoUtc;
  status: 'proposed' | 'active' | 'succeeded' | 'failed' | 'replaced';
  /** Weeks this plan has run without closing its gaps (feeds the 3-week paid rule). */
  freePlanWeeks: number;
  gapIds: string[];
  plan: InterventionPlan;
  paidTrigger?: 'any1_rule' | 'parent_request';
}

// ------------------------------------------------------------------ daily loop

/** students/{id}/timetable.json: one item per week. */
export interface TimetableWeek extends Timetable {
  generatedUtc: IsoUtc;
  /** Why it was (re)built: 'initial', 'test_result', 'request_approved', 'missed', 'session_booked'. */
  reason?: string;
}

export type TaskKind = 'learn' | 'practise' | 'retrieve' | 'test' | 'homework' | 'application' | 'profile' | 'action_item';
export type TaskSource = 'timetable' | 'teacher' | 'tutor' | 'counsellor' | 'mentor' | 'meeting' | 'parent' | 'system';

/** students/{id}/tasks.json */
export interface Task {
  id: string;
  learnerId: string;
  title: string;
  kind: TaskKind;
  dueDate: LocalDate;
  status: 'todo' | 'done' | 'skipped';
  source: TaskSource;
  /** Person who created it (tch_, tut_, csl_, mnt_). */
  createdBy?: string;
  createdUtc: IsoUtc;
  completedUtc?: IsoUtc;
  minutes?: number;
  subjectId?: string;
  /** Subtopic, gap, chapter, session, application or assessment the task points at. */
  refId?: string;
  /** For test tasks: the questions to take. */
  questionIds?: string[];
  href?: string;
  /** Free-form detail line. */
  detail?: string;
}

/** students/{id}/requests.json: timetable change requests (PDF 3b). S2 creates, counsellor decides. */
export interface TimetableRequest {
  id: string;
  learnerId: string;
  createdUtc: IsoUtc;
  weekStart: LocalDate;
  blockIds: string[];
  kind: 'move' | 'drop' | 'add' | 'swap' | 'more_time' | 'less_time' | 'other';
  reason: string;
  /** What the student asked for, in words or as a slot. */
  proposed?: { date: LocalDate; start: string; end: string } | string;
  status: 'pending' | 'approved' | 'edited' | 'declined';
  counsellorId?: string;
  decidedBy?: string;
  decidedUtc?: IsoUtc;
  decisionNote?: string;
}

// ------------------------------------------------------------------ sessions and marketplace

/** What a student chose to share with a tutor when booking (W2-T shape). */
export interface GapSnapshot {
  sharedUtc: IsoUtc;
  subjectId: string;
  /** Latest test score percent in that subject, if shared. */
  score?: number;
  gaps: { gapId?: string; subtopicId: string; name: string; code: GapCode; level: Level; hoursToClose: number }[];
}

/** students/{id}/bookings.json (or contrib). */
export interface Booking {
  id: string;
  learnerId: string;
  tutorId: string;
  kind: 'demo' | 'regular';
  status: 'requested' | 'accepted' | 'declined' | 'active' | 'completed' | 'cancelled';
  format: SessionFormat;
  mode?: SessionMode;
  subjectId?: string;
  /** Rupees per hour (0 for a free demo). */
  priceInr: Inr;
  requestedAt: IsoUtc;
  /** First (or demo) slot. */
  slotStartUtc?: IsoUtc;
  minutes: number;
  sessionsPerWeek?: number;
  topic?: string;
  note?: string;
  respondedUtc?: IsoUtc;
  /** Only what the student chose to share; null when sharing was off. */
  sharedGapSnapshot: GapSnapshot | null;
  sharedParamIds?: string[];
  /** Paid bookings for minors need a parent's approval (W2-P writes it). */
  parentApproval?: { parentId: string; status: 'pending' | 'approved' | 'declined'; utc?: IsoUtc; reason?: string };
  /** matchTutors reason line at booking time. */
  matchReason?: string;
}

/** Tutor post-session report (W2-T shape). Homework becomes Tasks (homeworkTaskIds). */
export interface SessionReport {
  topics: string[];
  performance: 'struggled' | 'getting_there' | 'confident';
  engagement: 'high' | 'medium' | 'low';
  notes: string;
  homeworkTaskIds: string[];
  nextFocus: string;
  submittedUtc: IsoUtc;
  gapIds?: string[];
}

/** students/{id}/sessions.json (or contrib): every live session, any host. */
export interface Session {
  id: string;
  /** Short display code, e.g. "S-10". */
  code?: string;
  /** Primary learner (first of learnerIds). */
  learnerId: string;
  /** All learners (group sessions have several). */
  learnerIds: string[];
  /** tut_, csl_, mnt_, tch_ */
  hostId: string;
  hostRole: 'tutor' | 'counsellor' | 'mentor' | 'teacher';
  kind: 'demo' | 'one_to_one' | 'group' | 'counselling' | 'career' | 'applications' | 'parent_meeting';
  title: string;
  subjectId?: string;
  focus?: string;
  startUtc: IsoUtc;
  minutes: number;
  status: 'scheduled' | 'completed' | 'cancelled' | 'no_show';
  mode: SessionMode;
  joinUrl?: string;
  bookingId?: string;
  /** Tutor rate for this session (earnings). */
  rateInr?: Inr;
  /** Tutor prep (AI focus list) before the session. */
  prepNotes?: string;
  report?: SessionReport | null;
  /** Counsellor/mentor notes. */
  meetingNoteId?: string;
}

/** Tutor assignment with per-question AI and tutor scores (W2-T shape). */
export interface Assignment {
  id: string;
  learnerId: string;
  tutorId: string;
  title: string;
  subtopicIds: string[];
  questionIds: string[];
  status: 'draft' | 'assigned' | 'in_progress' | 'submitted' | 'ai_evaluated' | 'reviewed' | 'completed' | 'overdue';
  dueOn: LocalDate;
  taskId?: string;
  score?: number;
  maxScore?: number;
  perQuestion?: { questionId: string; correct?: boolean; answer?: string; aiScore?: number; aiFeedback?: string; tutorScore?: number; tutorFeedback?: string; needsReview?: boolean }[];
}

/** Tutor's private notes on a student. */
export interface TutorNote {
  id: string;
  learnerId: string;
  tutorId: string;
  text: string;
  createdUtc: IsoUtc;
  source: 'manual' | 'session_report';
}

export interface Payout {
  id: string;
  tutorId: string;
  amountInr: Inr;
  paidOn: LocalDate;
  sessionIds: string[];
}

/** students/{id}/meetings.json: counsellor, mentor and application meeting notes. */
export interface MeetingNote {
  id: string;
  learnerId: string;
  staffId: string;
  date: LocalDate;
  kind: 'academic' | 'wellbeing' | 'career' | 'applications';
  summary: string;
  decisions: string[];
  actionItems: { id: string; title: string; dueOn: LocalDate; taskId?: string; done?: boolean }[];
  /** Wellbeing notes are T3: only the counsellor and the student see the summary. */
  tier: 'T1' | 'T2' | 'T3';
}

// ------------------------------------------------------------------ careers

/** students/{id}/careers.json (one item). */
export interface CareerMatches {
  learnerId: string;
  computedUtc: IsoUtc;
  fits: CareerFit[];
  shortlist: string[];
  /** careerGap output for shortlisted careers. */
  gaps: Record<string, CareerGapResult>;
}

// ------------------------------------------------------------------ applications (agreed with W2-A)

export type ApplicationStatus = 'shortlisted' | 'collecting_documents' | 'in_review' | 'submitted' | 'decision';
export type FitGroup = 'reach' | 'target' | 'safe';

export interface EssayComment {
  id: string;
  version: number;
  authorId: string | null;
  kind: 'ai' | 'human';
  anchor?: { start: number; end: number; quote: string };
  text: string;
  resolved: boolean;
  createdAt: IsoUtc;
  parentId?: string;
}

export interface Essay {
  id: string;
  prompt: string;
  wordLimit: number;
  status: 'drafting' | 'in_review' | 'final';
  versions: { version: number; text: string; createdAt: IsoUtc }[];
  comments: EssayComment[];
}

/** students/{id}/applications.json */
export interface Application {
  id: string;
  learnerId: string;
  universityId: string;
  programmeId: string;
  routeType: ApplicationType;
  status: ApplicationStatus;
  fitGroup: FitGroup;
  deadline: LocalDate;
  decision?: 'offer' | 'conditional_offer' | 'rejected' | 'waitlisted';
  counsellorId: string;
  checklist: { id: string; title: string; kind: 'document' | 'test_score' | 'recommendation' | 'essay' | 'form' | 'fee'; done: boolean; dueOn?: LocalDate }[];
  recommenders: { id: string; name: string; role: string; status: 'requested' | 'drafting' | 'submitted'; requestedOn: LocalDate; dueOn: LocalDate }[];
  essays: Essay[];
  /** Computed on read: e.g. "Deadline in 9 days with 3 open items". */
  riskFlags?: string[];
  updatedUtc: IsoUtc;
}

/** students/{id}/shortlist.json: universities saved while exploring (free and paid). */
export interface ShortlistEntry {
  learnerId: string;
  universityId: string;
  programmeId?: string;
  fitGroup?: FitGroup;
  savedUtc: IsoUtc;
}

/** students/{id}/finance.json: finance and visa block for an accepted offer. */
export interface FinanceVisa {
  learnerId: string;
  universityId: string;
  aid: { title: string; done: boolean; status?: string }[];
  visa: { title: string; done: boolean; date?: LocalDate }[];
  appointments: { title: string; date: LocalDate; place?: string }[];
  visaDocs: { title: string; done: boolean; documentId?: string }[];
}

export interface ApplicationsBundle {
  applications: Application[];
  shortlist: ShortlistEntry[];
  meetings: MeetingNote[];
  finance: FinanceVisa[];
}

// ------------------------------------------------------------------ documents, payments, consent

/** students/{id}/documents.json */
export interface DocumentRecord {
  id: string;
  learnerId: string;
  folder: 'academics' | 'activities' | 'application_documents' | 'job_ready';
  title: string;
  fileName: string;
  kind: 'report_card' | 'certificate' | 'test_result' | 'essay' | 'transcript' | 'portfolio' | 'recommendation' | 'id_proof' | 'other';
  uploadedUtc: IsoUtc;
  source: 'M5' | 'M6' | 'M7' | 'M8' | 'auto';
  sizeKb: number;
  /** Locked for free-plan users (application documents). */
  requiresPlan?: PlanId;
  refId?: string;
}

/** students/{id}/invoices.json */
export interface Invoice {
  id: string;
  learnerId: string;
  payerId: string;
  issuedUtc: IsoUtc;
  dueDate: LocalDate;
  status: 'due' | 'paid' | 'overdue';
  paidUtc?: IsoUtc;
  lines: { title: string; amountInr: Inr; bookingId?: string; planId?: PlanId }[];
  amountInr: Inr;
}

/** students/{id}/consents.json */
export interface Consent {
  id: string;
  learnerId: string;
  grantedById: string;
  scope: 'edu_personalisation' | 'share_with_tutor' | 'share_with_school' | 'wellbeing_screening' | 'marketing' | 'data_research';
  version: string;
  grantedUtc: IsoUtc;
  revokedUtc?: IsoUtc;
}

/** students/{id}/messages.json: messages between the student (or parent) and their people. */
export interface Message {
  id: string;
  /** Conversation key, e.g. "lrn_kabir_singh:tut_rahul_verma". */
  threadId: string;
  learnerId: string;
  /** Person id or 'system'. */
  from: string;
  toIds: string[];
  text: string;
  sentUtc: IsoUtc;
  readBy?: string[];
  /** Set for tutor messages so getTutorWorkspace can filter. */
  tutorId?: string;
}

/** Generic comment (on a gap, task, application) written through the store. */
export interface Comment {
  id: string;
  learnerId: string;
  targetType: 'gap' | 'task' | 'application' | 'essay' | 'session' | 'request';
  targetId: string;
  authorId: string;
  text: string;
  createdUtc: IsoUtc;
}

/** Generic approval (parent approves a paid tutor, counsellor approves a request...). */
export interface Approval {
  id: string;
  learnerId: string;
  kind: 'paid_tutor' | 'timetable_request' | 'plan_upgrade' | 'essay_final' | 'other';
  targetId: string;
  byId: string;
  decision: 'approved' | 'declined';
  utc: IsoUtc;
  note?: string;
}

// ------------------------------------------------------------------ classes, caseloads, tutor workspace

/** A background (non-persona) student inside a class file: light data only. */
export interface BackgroundStudent {
  id: string; // lrn_ (never a persona id)
  name: string;
  mastery: Record<string, { level: Level; pMastery: number; lastTestedUtc: IsoUtc }>;
  gaps: { subtopicId: string; code: GapCode; level: Level; hoursToClose: number; status: Gap['status'] }[];
  testScores: { title: string; date: LocalDate; pct: number }[];
}

/** classes/{sectionId}.json (one item). */
export interface Section {
  id: string; // sec-{subjectId}-{letter}
  name: string; // "9A Maths"
  teacherId: string;
  subjectId: string;
  board: Board;
  grade: Grade;
  school: string;
  /** Persona learners plus background learners. */
  learnerIds: string[];
  background: BackgroundStudent[];
}

export interface HeatmapCell {
  level: Level;
  pMastery: number;
  lastTestedUtc: IsoUtc;
}

export interface SectionHeatmap {
  section: Omit<Section, 'background'>;
  subtopics: { id: string; name: string; chapterId: string; chapterName: string; order: number }[];
  rows: { learnerId: string; name: string; isPersona: boolean; cells: Record<string, HeatmapCell | null> }[];
  /** Gap clusters: subtopic × code with the learners in it, biggest first. */
  clusters: { subtopicId: string; code: GapCode; learnerIds: string[] }[];
}

export interface RiskFlag {
  kind: 'deadline' | 'wellbeing' | 'data_sparsity' | 'engagement' | 'request_pending' | 'paid_rule';
  severity: 'high' | 'medium' | 'low';
  text: string;
  refId?: string;
}

export interface CaseloadEntry {
  student: Student;
  focus: string;
  flags: RiskFlag[];
  needsYouToday: boolean;
  pendingRequests: number;
  nextSession?: Session;
  lastMeeting?: MeetingNote;
  openGaps: number;
}

export interface TutorWorkspace {
  tutor: Tutor;
  students: { learnerId: string; name: string; grade: Grade; board: Board; goal: string; subjectIds: string[]; sinceUtc: IsoUtc; lastActivityUtc: IsoUtc; openGaps: number; student?: Student }[];
  bookings: Booking[];
  sessions: Session[];
  assignments: Assignment[];
  messages: Message[];
  notes: TutorNote[];
  payouts: Payout[];
  /** Per month, from completed sessions; platform fee is tutor.platformFeeRate (15%). */
  earnings: { month: string; sessions: number; grossInr: Inr; platformFeeInr: Inr; netInr: Inr }[];
}

export interface ChildSummary {
  student: Student;
  band: Band;
  lrs: number | null;
  openGaps: number;
  hoursToClose: number;
  nextSession?: Session;
  tasksThisWeek: { done: number; total: number };
}

export type { NextAction };
