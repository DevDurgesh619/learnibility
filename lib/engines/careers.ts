/**
 * Engine 7: career fit and career gap.
 * Source: W3 brief (weights), blueprint "The engines behind the daily loop" (career mapping),
 * Design Edu Tech PDF area 9 (career detail), catalogue types Career / Skill / Resource / EntranceExam,
 * 430-profile file sheet "Sensitivity Tiers" (T3 excluded from career fit).
 *
 * mapCareers: fit score out of 100
 *   interests 35            RIASEC from p200; career codes weighted 1, 0.6, 0.3
 *   aptitude & academics 35 half from the career's aptitude params (0-100 scores), half from class
 *                           percentages against the pathway's minimum per subject (required ones count double)
 *   skill evidence 15       current level ÷ target level per required skill (core ×2), capped at 1
 *   feasibility 15          stream fit (grades 8-10 always fit) and cheapest pathway cost vs budget
 *   Missing evidence counts as neutral 0.5 and lowers the confidence label. T3 values are dropped
 *   before anything is read, whatever parameter they sit on.
 *
 * careerGap: per required skill, levels to climb and hours (Skill.hoursPerLevel, or mastery-model hours
 *   for academic skills when given), the free route (free resources, ₹0) and the paid route (cheapest
 *   paid course reaching the target level), months at the learner's weekly hours, plus each pathway's
 *   cost, years to entry and exam preparation hours.
 */
import type { Grade, Hours, Inr, Stream } from '../types';
import type { Career, CareerPathway, EntranceExam, Resource, Riasec, Skill, SkillLevel } from '../types/catalogue';
import { ProfileLike, round } from './util';

const WEEKS_PER_MONTH = 4.345;

/** Drop T3 values; return a plain map of the latest value per parameter. */
export function nonSensitive(profile: ProfileLike | undefined): Record<string, unknown> {
  if (!profile) return {};
  if (!Array.isArray(profile)) return { ...profile };
  const out: Record<string, { v: unknown; at: string }> = {};
  for (const p of profile) {
    if (p.tier === 'T3') continue;
    if (!out[p.paramId] || out[p.paramId].at < p.asOfUtc) out[p.paramId] = { v: p.value, at: p.asOfUtc };
  }
  return Object.fromEntries(Object.entries(out).map(([k, x]) => [k, x.v]));
}

export interface CareerContext {
  grade?: Grade;
  stream?: Stream;
  /** Latest class percentage per W2 subject slug. */
  subjectPercents?: Record<string, number>;
  /** Current level per skill id (0 = none). Falls back to skill.profileParamIds values in the profile. */
  skillLevels?: Record<string, number>;
  /** Total rupees the family can put toward the degree path; falls back to p178 annual budget × years. */
  budgetTotalInr?: Inr;
  /** Learner's hours a week for skill building (default 5). */
  weeklyHours?: number;
  skills?: Skill[];
  resources?: Resource[];
  exams?: EntranceExam[];
  /** Mastery-model hours to reach a level for academic skills, keyed by skill id. */
  academicHours?: Record<string, Hours>;
  limit?: number;
}

export interface CareerFit {
  careerId: string;
  title: string;
  score: number;
  parts: { interests: number; aptitudeAcademics: number; skills: number; feasibility: number };
  confidence: 'low' | 'medium' | 'high';
  reasons: string[];
}

/** RIASEC scores 0-1 from p200 ("IAS" ordered string, array, or { R: 0-100 ... }). */
export function riasecScores(v: unknown): Partial<Record<Riasec, number>> | null {
  if (!v) return null;
  if (typeof v === 'string' || Array.isArray(v)) {
    const codes = (typeof v === 'string' ? v.toUpperCase().replace(/[^RIASEC]/g, '').split('') : v) as Riasec[];
    const w = [1, 0.7, 0.4, 0.2, 0.1, 0];
    return Object.fromEntries(codes.map((c, i) => [c, w[i] ?? 0]));
  }
  if (typeof v === 'object') {
    const o = v as Record<string, number>;
    const max = Math.max(...Object.values(o), 1);
    return Object.fromEntries(Object.entries(o).map(([k, x]) => [k.toUpperCase(), x / (max > 1 ? 100 : 1)]));
  }
  return null;
}

const BAND_LEVEL: Record<string, number> = { none: 0, beginner: 1, basic: 1, developing: 2, intermediate: 3, proficient: 3, advanced: 4, expert: 5 };
function levelFromValue(v: unknown): number | undefined {
  if (typeof v === 'number') return v > 5 ? Math.round(v / 20) : v;
  if (typeof v === 'string') return BAND_LEVEL[v.toLowerCase()];
  return undefined;
}

function currentLevel(skillId: string, p: Record<string, unknown>, ctx: CareerContext): number {
  if (ctx.skillLevels?.[skillId] !== undefined) return ctx.skillLevels[skillId];
  const sk = ctx.skills?.find((s) => s.id === skillId);
  for (const pid of sk?.profileParamIds ?? []) {
    const l = levelFromValue(p[pid]);
    if (l !== undefined) return l;
  }
  return 0;
}

const BUDGET_BANDS: Record<string, number> = { none: 0, low: 100_000, medium: 300_000, high: 800_000, very_high: 2_000_000 };

function budgetTotal(p: Record<string, unknown>, ctx: CareerContext, years: number): number | undefined {
  if (ctx.budgetTotalInr !== undefined) return ctx.budgetTotalInr;
  const v = p['p178'];
  const annual = typeof v === 'number' ? v : typeof v === 'string' ? BUDGET_BANDS[v.toLowerCase()] ?? (Number(v.replace(/[^\d]/g, '')) || undefined) : undefined;
  return annual === undefined ? undefined : annual * years;
}

export function cheapestPathway(c: Career): CareerPathway | undefined {
  return [...c.pathways].sort((a, b) => a.costInr.typical - b.costInr.typical)[0];
}

export function mapCareers(profile: ProfileLike | undefined, careers: Career[], ctx: CareerContext = {}): CareerFit[] {
  const p = nonSensitive(profile);
  const ri = riasecScores(p['p200']);
  const out: CareerFit[] = [];
  for (const c of careers) {
    let known = 0;
    const reasons: string[] = [];

    // interests
    let interests = 0.5;
    if (ri) {
      known++;
      const w = [1, 0.6, 0.3];
      const codes = c.riasec.slice(0, 3);
      interests = codes.reduce((s, code, i) => s + w[i] * (ri[code] ?? 0), 0) / codes.reduce((s, _, i) => s + w[i], 0);
      const top = codes.filter((code) => (ri[code] ?? 0) >= 0.7);
      if (top.length) reasons.push(`Matches your ${top.join('')} interests`);
    }

    // aptitude and academics
    const apt = c.aptitudeParamIds.map((id) => p[id]).filter((v): v is number => typeof v === 'number');
    const aptScore = apt.length ? apt.reduce((s, v) => s + v, 0) / apt.length / 100 : undefined;
    let acad: number | undefined;
    if (ctx.subjectPercents) {
      let num = 0, den = 0;
      for (const s of c.subjects) {
        const pct = ctx.subjectPercents[s.subjectSlug];
        if (pct === undefined) continue;
        const wt = s.required ? 2 : 1;
        num += wt * Math.min(1, pct / Math.max(1, s.minPercent));
        den += wt;
      }
      if (den) acad = num / den;
    }
    const aa = aptScore !== undefined && acad !== undefined ? (aptScore + acad) / 2 : aptScore ?? acad ?? 0.5;
    if (aptScore !== undefined || acad !== undefined) known++;
    if (aa >= 0.8) reasons.push('Strong aptitude and marks for it');
    else if (aa < 0.5 && (aptScore !== undefined || acad !== undefined)) reasons.push('Marks or aptitude below what the pathway expects');

    // skills
    let skills = 0;
    let wsum = 0;
    let anySkill = false;
    for (const r of c.skills) {
      const cur = currentLevel(r.skillId, p, ctx);
      if (cur > 0) anySkill = true;
      const wt = r.importance === 'core' ? 2 : 1;
      skills += wt * Math.min(1, cur / r.targetLevel);
      wsum += wt;
    }
    skills = wsum ? skills / wsum : 0.5;
    if (anySkill) known++;

    // feasibility
    const streamFit = !ctx.stream || ctx.stream === 'none' || (ctx.grade !== undefined && ctx.grade <= 10) || c.streams.includes(ctx.stream as Exclude<Stream, 'none'>) ? 1 : 0.3;
    if (streamFit < 1) reasons.push(`Usually entered from ${c.streams.join(' or ')}`);
    const cheap = cheapestPathway(c);
    const budget = cheap ? budgetTotal(p, ctx, Math.max(1, cheap.yearsToEntry)) : undefined;
    const costFit = cheap && budget !== undefined ? Math.min(1, budget / Math.max(1, cheap.costInr.typical)) : 0.5;
    if (cheap && budget !== undefined) {
      known++;
      reasons.push(costFit >= 1 ? `Affordable route: ${cheap.label}` : `Cheapest route (${cheap.label}) costs more than the budget`);
    }
    const feasibility = (streamFit + costFit) / 2;

    const parts = { interests: round(interests * 35, 1), aptitudeAcademics: round(aa * 35, 1), skills: round(skills * 15, 1), feasibility: round(feasibility * 15, 1) };
    out.push({
      careerId: c.id, title: c.title,
      score: round(parts.interests + parts.aptitudeAcademics + parts.skills + parts.feasibility, 1),
      parts, confidence: known >= 3 ? 'high' : known >= 2 ? 'medium' : 'low', reasons,
    });
  }
  return out.sort((a, b) => b.score - a.score || a.careerId.localeCompare(b.careerId)).slice(0, ctx.limit ?? careers.length);
}

export interface SkillGapLine {
  skillId: string;
  name: string;
  importance: 'core' | 'helpful';
  currentLevel: number;
  targetLevel: SkillLevel;
  levelsToClimb: number;
  hours: Hours;
  freeRoute: { resourceIds: string[]; hours: Hours; inr: 0 };
  paidRoute: { resourceId: string | null; hours: Hours; inr: Inr };
}

export interface CareerGapResult {
  careerId: string;
  skills: SkillGapLine[];
  totalHours: Hours;
  free: { hours: Hours; inr: 0; months: number };
  paid: { hours: Hours; inr: Inr; months: number };
  pathways: { id: string; label: string; region: CareerPathway['region']; yearsToEntry: number; costInr: CareerPathway['costInr']; examIds: string[]; examPrepHours: Hours; examFeesInr: Inr }[];
}

export function careerGap(profile: ProfileLike | undefined, career: Career, ctx: CareerContext = {}): CareerGapResult {
  const p = nonSensitive(profile);
  const weekly = ctx.weeklyHours ?? 5;
  const lines: SkillGapLine[] = [];
  for (const r of career.skills) {
    const sk = ctx.skills?.find((s) => s.id === r.skillId);
    const cur = Math.min(5, Math.max(0, Math.floor(currentLevel(r.skillId, p, ctx))));
    const climb = Math.max(0, r.targetLevel - cur);
    const ladder = sk ? sk.hoursPerLevel.slice(cur, r.targetLevel).reduce((s, h) => s + h, 0) : climb * 20;
    const hours = round(climb === 0 ? 0 : ctx.academicHours?.[r.skillId] ?? ladder, 1);
    const res = (ctx.resources ?? []).filter((x) => (sk?.resourceIds.includes(x.id) ?? false) || x.skillOutcomes.some((o) => o.skillId === r.skillId));
    const reaches = (x: Resource) => x.skillOutcomes.some((o) => o.skillId === r.skillId && o.toLevel >= r.targetLevel);
    const free = res.filter((x) => x.kind === 'free_resource');
    const paid = res.filter((x) => x.kind === 'paid_course').sort((a, b) => Number(reaches(b)) - Number(reaches(a)) || a.priceInr - b.priceInr)[0];
    lines.push({
      skillId: r.skillId, name: sk?.name ?? r.skillId, importance: r.importance, currentLevel: cur, targetLevel: r.targetLevel, levelsToClimb: climb, hours,
      freeRoute: { resourceIds: climb ? free.map((x) => x.id) : [], hours, inr: 0 },
      // a structured course replaces self-assembly; use its own hours when longer
      paidRoute: climb && paid ? { resourceId: paid.id, hours: round(Math.max(paid.hours, hours * 0.8), 1), inr: paid.priceInr } : { resourceId: null, hours, inr: 0 },
    });
  }
  const totalHours = round(lines.reduce((s, l) => s + l.hours, 0), 1);
  const paidHours = round(lines.reduce((s, l) => s + l.paidRoute.hours, 0), 1);
  const months = (h: number) => round(h / weekly / WEEKS_PER_MONTH, 1);
  const exams = new Map((ctx.exams ?? []).map((e) => [e.id, e]));
  return {
    careerId: career.id,
    skills: lines,
    totalHours,
    free: { hours: totalHours, inr: 0, months: months(totalHours) },
    paid: { hours: paidHours, inr: lines.reduce((s, l) => s + l.paidRoute.inr, 0), months: months(paidHours) },
    pathways: career.pathways.map((pw) => ({
      id: pw.id, label: pw.label, region: pw.region, yearsToEntry: pw.yearsToEntry, costInr: pw.costInr, examIds: pw.examIds,
      examPrepHours: pw.examIds.reduce((s, id) => s + (exams.get(id)?.prepHours ?? 0), 0),
      examFeesInr: pw.examIds.reduce((s, id) => s + (exams.get(id)?.feeInr ?? 0), 0),
    })),
  };
}
