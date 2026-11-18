/**
 * The only place application-support screens read data. It wraps the W2-0 data layer (lib/data) so the
 * screens never touch JSON or the store, and computes risk flags with logic.ts.
 */
import 'server-only';
import { DEMO_NOW } from '@/lib/demo-clock';
import {
  getAdult, getApplication as getApp, getApplications, getApplicationsPipeline, getApprovals, getDocuments, getPersonName, getProfileValues,
  getStudent, getUniversity, listUniversities,
} from '@/lib/data';
import type { Application, ApplicationsBundle, DocumentRecord, PlanId, Student } from '@/lib/data/types';
import type { ProfileValue, University } from '@/lib/types';
import type { FitProfile, Strength } from './fit';
import { riskFlags } from './logic';

export { getUniversity, listUniversities };

/** Risk flags from logic.ts (adds over-limit essays to the data layer's deadline and recommender flags). */
const withFlags = <T extends Application>(a: T): T => ({ ...a, riskFlags: riskFlags(a, DEMO_NOW).map((f) => f.text) });

export function nameOf(id: string | null | undefined): string {
  if (!id) return 'AI pre-pass';
  const n = getPersonName(id)?.name;
  if (n) return n;
  return id.replace(/^[a-z]+_/, '').split('_').map((w) => w[0]!.toUpperCase() + w.slice(1)).join(' ');
}

export const firstName = (id: string | null | undefined) => nameOf(id).split(' ')[0]!;

export interface StudentCtx {
  id: string;
  name: string;
  student?: Student;
  plan: PlanId;
  counsellorId?: string;
}

export function studentCtx(learnerId: string): StudentCtx {
  const student = getStudent(learnerId);
  const apps = getApplications(learnerId).applications;
  const upgraded = getApprovals({ learnerId, kind: 'plan_upgrade' }).some((a) => a.decision === 'approved');
  const base: PlanId = student?.plan ?? (apps.length ? 'application_support' : 'free');
  const plan: PlanId = upgraded && base === 'free' ? 'application_support' : base;
  const counsellorId = apps[0]?.counsellorId
    ?? student?.counsellorIds?.find((c) => getAdult(c)?.focus === 'applications')
    ?? student?.counsellorIds?.[0];
  return { id: learnerId, name: student?.name ?? nameOf(learnerId), student, plan, counsellorId };
}

export const isPaid = (plan: PlanId) => plan !== 'free';

export function applicationsBundle(learnerId: string): ApplicationsBundle {
  const b = getApplications(learnerId);
  return {
    ...b,
    applications: b.applications.map(withFlags),
    // Only application meetings here; wellbeing notes (T3) never reach these screens.
    meetings: b.meetings.filter((m) => m.kind === 'applications' && m.tier !== 'T3'),
  };
}

export function getApplication(applicationId: string): Application | undefined {
  const a = getApp(applicationId);
  return a && withFlags(a);
}

export function findEssay(essayId: string, apps: Application[]) {
  for (const app of apps) {
    const essay = app.essays.find((e) => e.id === essayId);
    if (essay) return { app, essay };
  }
  return undefined;
}

/** Applications of every learner whose application counsellor is `counsellorId`. */
export function caseloadApplications(counsellorId: string) {
  return getApplicationsPipeline(counsellorId).map(withFlags);
}

export function caseloadLearners(counsellorId: string): string[] {
  const ids = new Set<string>(getAdult(counsellorId)?.learnerIds ?? []);
  for (const a of caseloadApplications(counsellorId)) ids.add(a.learnerId);
  return [...ids];
}

export function applicationDocuments(learnerId: string): DocumentRecord[] {
  return getDocuments(learnerId, 'application_documents');
}

export function uniMap(): Map<string, University> {
  return new Map(listUniversities().map((u) => [u.id, u]));
}

export function programmeOf(uni: University | undefined, programmeId: string) {
  return uni?.programmes.find((p) => p.id === programmeId);
}

// ------------------------------------------------------------------ fit inputs

/** Profile parameters the fit uses. T1 only; see fit.ts. */
export const FIT_PARAMS = {
  predicted: 'p16', // Class XII board target / predicted grades
  latestPercent: 'p8',
  testScores: 'p25', // competitive and admission test scores (SAT)
  english: 'p212',
  activities: 'p268', // extracurricular depth score
  essay: 'p267', // personal-statement material bank
  countries: 'p231',
} as const;

/** Raw values feed the fit engine only (never rendered); fit reads T1 parameters only. */
function profileValues(learnerId: string): ProfileValue[] {
  return getProfileValues(learnerId).filter((v) => v.tier === 'T1');
}

function num(v: unknown): number | undefined {
  if (typeof v === 'number') return v;
  if (typeof v === 'string') {
    const m = v.match(/\d+(\.\d+)?/);
    return m ? Number(m[0]) : undefined;
  }
  if (v && typeof v === 'object' && 'value' in v) return num((v as { value: unknown }).value);
  return undefined;
}

function strength(v: unknown): Strength | undefined {
  if (v === undefined || v === null || v === '') return undefined;
  const s = String(typeof v === 'object' && v && 'value' in v ? (v as { value: unknown }).value : v).toLowerCase();
  if (/strong|high|excellent/.test(s)) return 'strong';
  if (/weak|low|developing/.test(s)) return 'weak';
  const n = num(v);
  if (n !== undefined && n <= 5) return n >= 4 ? 'strong' : n >= 3 ? 'average' : 'weak'; // 1-5 scale
  if (n !== undefined) return n >= 70 ? 'strong' : n >= 40 ? 'average' : 'weak'; // 0-100 score
  return 'average';
}

export interface FitInputs {
  profile: FitProfile;
  countries: string[];
  sources: Partial<Record<'academic' | 'essay' | 'activities' | 'tests', string>>;
}

const SOURCE_LABEL: Record<string, string> = {
  M1: 'from onboarding', M2: 'from onboarding', M5: 'from report card upload', M6: 'from document upload', M9: 'from onboarding',
  M14: 'from platform tests', M16: 'from platform tests',
};

const sourceLabel = (v: ProfileValue, fallback = 'from your profile') => SOURCE_LABEL[v.source] ?? fallback;

export function fitInputs(learnerId: string): FitInputs {
  const vals = profileValues(learnerId);
  const get = (id: string) => vals.find((v) => v.paramId === id);
  const pred = get(FIT_PARAMS.predicted);
  const latest = get(FIT_PARAMS.latestPercent);
  const profile: FitProfile = {};
  const src: FitInputs['sources'] = {};
  const rawOf = (v: ProfileValue | undefined) => (v && typeof v.value === 'object' && v.value && 'value' in v.value ? (v.value as { value: unknown }).value : v?.value);
  const p = String(rawOf(pred) ?? '').trim();
  const aLevel = p.match(/^((?:A\*|[A-E]){2,4})\b/);
  const ib = p.match(/^IB\s*(\d{2})/i);
  const pct = p.match(/(\d{2}(?:\.\d)?)\s*%/);
  if (aLevel) { profile.aLevelGrades = aLevel[1]; src.academic = sourceLabel(pred!); }
  else if (ib) { profile.ibPoints = Number(ib[1]); src.academic = sourceLabel(pred!); }
  else if (pct) { profile.boardPercent = Number(pct[1]); src.academic = sourceLabel(pred!); }
  else if (latest && num(rawOf(latest)) !== undefined) { profile.boardPercent = num(rawOf(latest)); src.academic = sourceLabel(latest); }
  const tests = get(FIT_PARAMS.testScores);
  if (tests) {
    const t = tests.value;
    const sat = Array.isArray(t) ? t.map((x) => (x && typeof x === 'object' && /sat/i.test(String((x as { exam?: string; name?: string }).exam ?? (x as { name?: string }).name)) ? num((x as { score?: unknown }).score) : undefined)).find((x) => x !== undefined) : /sat/i.test(String(t)) || (num(t) ?? 0) > 400 ? num(t) : undefined;
    if (sat !== undefined) profile.sat = sat;
    if (sat !== undefined) src.tests = sourceLabel(tests);
  }
  const eng = get(FIT_PARAMS.english);
  if (eng) {
    const t = String(rawOf(eng) ?? '');
    const n = /ielts/i.test(t) || typeof eng.value === 'number' ? num(t) : undefined;
    if (n !== undefined && n <= 9) { profile.ielts = n; src.tests ??= sourceLabel(eng); }
  }
  const act = get(FIT_PARAMS.activities);
  if (act) {
    profile.activities = strength(act.value);
    src.activities = sourceLabel(act, 'from Inventory');
  }
  const ess = get(FIT_PARAMS.essay);
  if (ess) {
    profile.essay = strength(ess.value);
    src.essay = sourceLabel(ess, 'from uploaded essay');
  }
  const c = get(FIT_PARAMS.countries)?.value;
  const countries = Array.isArray(c) ? c.map((x) => countryCode(String(x))).filter((x): x is string => !!x) : [];
  return { profile, countries, sources: src };
}

const COUNTRY_CODES: Record<string, string> = { usa: 'us', us: 'us', 'united states': 'us', uk: 'uk', 'united kingdom': 'uk', canada: 'ca', ca: 'ca', australia: 'au', au: 'au', india: 'in', in: 'in' };
export const countryCode = (s: string) => COUNTRY_CODES[s.trim().toLowerCase()];
