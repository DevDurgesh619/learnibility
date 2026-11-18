/**
 * Risk flags for a counsellor's caseload. Pure rules over one learner's data; the page gathers inputs.
 *
 * Rules (W2-C, logged in docs/decisions.md):
 *  - deadline   an application deadline within 14 days with open checklist items (high under 7 days)
 *  - wellbeing  monthly check-in (p149) 2 or below, burnout flag (p114), screened stress or anxiety (p109, p110)
 *               in the high band, or no check-in for 35+ days. T3: counsellor eyes only, never ranking.
 *  - data       profile under 40% complete, a section under 25% that the plan relies on, or no assessment for 21+ days
 *  - learning   learning-rate band below average, an engagement gap (G10), or 3+ missed tasks in the last 7 days
 *  - request    a timetable request waiting more than 48 hours
 */
import type { Band, GapCode } from '@/lib/types';

export type RiskKind = 'deadline' | 'wellbeing' | 'data' | 'learning' | 'request';
export type Severity = 'high' | 'medium' | 'low';

export interface RiskFlag {
  id: string;
  learnerId: string;
  kind: RiskKind;
  severity: Severity;
  title: string;
  detail: string;
  href?: string;
  /** Sort key: when it matters. */
  dueUtc?: string;
}

export interface RiskInput {
  learnerId: string;
  now: Date;
  applications?: { id: string; title: string; deadlineUtc: string; openItems: number }[];
  /** Latest values of the wellbeing parameters, by param id (counsellor view, T3 included). */
  wellbeing?: Partial<Record<'p109' | 'p110' | 'p114' | 'p149', { value: unknown; asOfUtc: string }>>;
  completeness?: number;
  sparseSections?: string[];
  lastAssessmentUtc?: string;
  lrsBand?: Band;
  gapCodes?: GapCode[];
  missedTasks7d?: number;
  pendingRequests?: { id: string; createdUtc: string; summary: string }[];
}

const DAY = 86_400_000;
const days = (from: Date, iso: string) => (Date.parse(iso) - from.getTime()) / DAY;
const HIGH_BANDS = ['high', 'very_high', 'severe', 'elevated', 'above_threshold'];

function isHighBand(v: unknown): boolean {
  if (typeof v === 'number') return v >= 4;
  return typeof v === 'string' && HIGH_BANDS.includes(v.toLowerCase().replace(/[\s-]/g, '_'));
}

export function riskFlags(input: RiskInput): RiskFlag[] {
  const { learnerId, now } = input;
  const out: RiskFlag[] = [];
  const add = (f: Omit<RiskFlag, 'learnerId'>) => out.push({ ...f, learnerId });

  for (const a of input.applications ?? []) {
    const left = days(now, a.deadlineUtc);
    if (left >= 0 && left <= 14 && a.openItems > 0) {
      add({
        id: `${learnerId}-deadline-${a.id}`, kind: 'deadline', severity: left < 7 ? 'high' : 'medium',
        title: `${a.title}: ${Math.ceil(left)} days left`,
        detail: `${a.openItems} open item${a.openItems === 1 ? '' : 's'} before the deadline.`,
        href: '/counsellor/applications', dueUtc: a.deadlineUtc,
      });
    }
  }

  const w = input.wellbeing ?? {};
  const checkIn = w.p149;
  if (checkIn && typeof checkIn.value === 'number' && checkIn.value <= 2) {
    add({ id: `${learnerId}-wb-checkin`, kind: 'wellbeing', severity: 'high', title: `Wellbeing check-in scored ${checkIn.value} of 5`, detail: 'Book a human check-in this week. Screened data stays with you and the student.', dueUtc: checkIn.asOfUtc });
  }
  if (w.p114 && (w.p114.value === true || w.p114.value === 'yes' || w.p114.value === 'flagged')) {
    add({ id: `${learnerId}-wb-burnout`, kind: 'wellbeing', severity: 'high', title: 'Burnout signals flagged', detail: 'Treat as a wellbeing alert, not a score. Check in before changing the plan.', dueUtc: w.p114.asOfUtc });
  }
  for (const [pid, label] of [['p109', 'Stress'], ['p110', 'Anxiety']] as const) {
    const v = w[pid];
    if (v && isHighBand(v.value)) add({ id: `${learnerId}-wb-${pid}`, kind: 'wellbeing', severity: 'medium', title: `${label} screened in the high band`, detail: 'Screening, not diagnosis. A counsellor conversation decides next steps.', dueUtc: v.asOfUtc });
  }
  if (!checkIn || -days(now, checkIn.asOfUtc) > 35) {
    add({ id: `${learnerId}-wb-due`, kind: 'wellbeing', severity: 'low', title: 'Monthly wellbeing check-in due', detail: checkIn ? `Last check-in ${Math.floor(-days(now, checkIn.asOfUtc))} days ago.` : 'No check-in on record yet.' });
  }

  if (input.completeness != null && input.completeness < 0.4) {
    add({ id: `${learnerId}-data-profile`, kind: 'data', severity: 'medium', title: `Profile ${Math.round(input.completeness * 100)}% complete`, detail: 'Recommendations rest on thin evidence. Fill the gaps in Student 360.', href: `/counsellor/student-360?student=${learnerId}` });
  }
  if (input.sparseSections?.length) {
    add({ id: `${learnerId}-data-sections`, kind: 'data', severity: 'low', title: `${input.sparseSections.length} sparse profile section${input.sparseSections.length === 1 ? '' : 's'}`, detail: input.sparseSections.join(', '), href: `/counsellor/student-360?student=${learnerId}` });
  }
  const sinceTest = input.lastAssessmentUtc ? -days(now, input.lastAssessmentUtc) : Infinity;
  if (sinceTest > 21) {
    add({ id: `${learnerId}-data-assessment`, kind: 'data', severity: 'medium', title: input.lastAssessmentUtc ? `No assessment for ${Math.floor(sinceTest)} days` : 'No assessment yet', detail: 'Gaps and the timetable are going stale without fresh evidence.' });
  }

  if (input.lrsBand === 'below_avg') add({ id: `${learnerId}-learn-lrs`, kind: 'learning', severity: 'medium', title: 'Learning rate below average', detail: 'Check method fit before adding hours.' });
  if (input.gapCodes?.includes('G10')) add({ id: `${learnerId}-learn-g10`, kind: 'learning', severity: 'medium', title: 'Engagement gap (G10)', detail: 'Blank answers on recent tests. Talk about motivation before content.' });
  if ((input.missedTasks7d ?? 0) >= 3) add({ id: `${learnerId}-learn-missed`, kind: 'learning', severity: 'medium', title: `${input.missedTasks7d} tasks missed this week`, detail: 'The plan may be too heavy. Consider a timetable change.', href: '/counsellor/timetable-requests' });

  for (const r of input.pendingRequests ?? []) {
    const age = -days(now, r.createdUtc);
    if (age > 2) add({ id: `${learnerId}-req-${r.id}`, kind: 'request', severity: 'medium', title: `Timetable request waiting ${Math.floor(age)} days`, detail: r.summary, href: '/counsellor/timetable-requests' });
  }
  return sortFlags(out);
}

const SEV: Record<Severity, number> = { high: 0, medium: 1, low: 2 };
export function sortFlags(flags: RiskFlag[]): RiskFlag[] {
  return [...flags].sort((a, b) => SEV[a.severity] - SEV[b.severity] || (a.dueUtc ?? '9').localeCompare(b.dueUtc ?? '9') || a.id.localeCompare(b.id));
}

export const RISK_KIND_LABEL: Record<RiskKind, string> = {
  deadline: 'Deadline', wellbeing: 'Wellbeing', data: 'Data sparsity', learning: 'Learning', request: 'Request',
};
