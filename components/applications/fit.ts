/**
 * University fit: a simple, documented rule that sorts programmes into Reach, Target and Safe.
 *
 * Inputs are only academic and test evidence (T1). Wellbeing, family and other T2/T3 values never feed fit
 * (lib/visibility.ts model-use rule); budget is a filter, not a score.
 *
 * The rule, in four steps:
 *  1. Academic margin. The student's results and the programme's typical offer are both put on one
 *     percent-equivalent scale (A level grades A* 97, A 90, B 80, C 70, D 60, E 50, averaged over the three;
 *     IB points 40 + 1.3 × points; CBSE and other board percentages as they are). Where the offer is a range
 *     (e.g. "AAB-A*AA") the midpoint is used. Margin in steps = (student − required) / 5.
 *  2. Test margin (US routes that publish a SAT middle 50%): t = (SAT − midpoint) / (high − low), so the
 *     middle 50% spans −0.5 to +0.5. Missing SAT on a test-optional route counts as 0; on a required route, −0.5.
 *  3. Chance = published admit rate × 2^(0.8 × academic steps + 1.5 × t + profile bonus), clamped to 1–95%.
 *     Profile bonus: +0.25 each for a strong activity record and a strong essay, −0.25 for a weak one.
 *     When no admit rate is published, the selectivity tier's default rate is used.
 *  4. Band: anything with an admit rate under 10% or tier "most selective" is always Reach (nobody is "safe"
 *     there). Otherwise chance under 30% is Reach, under 65% Target, and 65% or more Safe.
 */
import type { ApplicationRoute, Programme, University } from '@/lib/types';

export type FitBand = 'reach' | 'target' | 'safe';

export const FIT_BAND_LABEL: Record<FitBand, string> = { reach: 'Reach', target: 'Target', safe: 'Safe' };

export type Strength = 'weak' | 'average' | 'strong';

export interface FitProfile {
  /** Predicted or achieved results. Any one of these is enough. */
  aLevelGrades?: string; // "ABB", "A*AA"
  ibPoints?: number; // 24-45
  boardPercent?: number; // CBSE / Cambridge / other board percentage, 0-100
  sat?: number;
  ielts?: number;
  activities?: Strength;
  essay?: Strength;
}

export interface FitResult {
  universityId: string;
  programmeId: string;
  band: FitBand;
  /** 1-95, whole percent. */
  chancePct: number;
  /** One line shown on the card, e.g. "SAT 1480 vs 1500-1560 middle 50%". */
  reason: string;
  /** Details for the "why" popover. */
  factors: { label: string; effect: 'helps' | 'neutral' | 'hurts' }[];
}

const SELECTIVITY_DEFAULT_RATE: Record<University['selectivity'], number> = {
  most_selective: 5, highly_selective: 15, selective: 40, moderate: 65, accessible: 85,
};

const GRADE_PCT: Record<string, number> = { 'A*': 97, A: 90, B: 80, C: 70, D: 60, E: 50 };

/** "A*AB" -> [A*, A, B]. */
export function splitGrades(s: string): string[] {
  return s.match(/A\*|[A-E]/g) ?? [];
}

export function aLevelToPct(grades: string): number | undefined {
  const g = splitGrades(grades);
  if (!g.length) return undefined;
  return g.reduce((sum, x) => sum + (GRADE_PCT[x] ?? 50), 0) / g.length;
}

export const ibToPct = (points: number) => Math.min(100, 40 + 1.3 * points);

const mid = (xs: number[]) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : undefined);

/** Parse an offer string into percent-equivalent requirements per system. */
export function parseOffer(offer: string | undefined): { aLevel?: number; ib?: number; percent?: number } {
  if (!offer) return {};
  const triples = offer.match(/(?:A\*|[A-E]){3}/g) ?? [];
  const aLevel = mid(triples.map((t) => aLevelToPct(t)!).filter((x) => x !== undefined));
  const ibm = offer.match(/IB\s*(\d{2})(?:\s*[-–]\s*(\d{2}))?/);
  const ib = ibm ? ibToPct(mid([Number(ibm[1]), ...(ibm[2] ? [Number(ibm[2])] : [])])!) : undefined;
  const pm = offer.match(/(?:CBSE|board)\s*(\d{2})(?:\s*[-–]\s*(\d{2}))?\s*%/i);
  const percent = pm ? mid([Number(pm[1]), ...(pm[2] ? [Number(pm[2])] : [])]) : undefined;
  return { aLevel, ib, percent };
}

export function offerFor(programme: Programme, route: ApplicationRoute): string | undefined {
  // Programme offer is more specific, but Canadian routes keep their CBSE / IB ranges on the route.
  return [programme.typicalOffer, route.requirements.typicalOffer].filter(Boolean).join(' / ') || undefined;
}

/** The route a student would normally use: regular / UCAS equal consideration / OUAC first, else the latest deadline. */
export function mainRoute(uni: University): ApplicationRoute | undefined {
  const pref = ['ucas_equal_consideration', 'regular', 'ouac', 'direct', 'rolling', 'ucas_oxbridge_medicine'];
  for (const t of pref) {
    const r = uni.applicationRoutes.find((x) => x.type === t);
    if (r) return r;
  }
  return [...uni.applicationRoutes].sort((a, b) => b.deadline.value.localeCompare(a.deadline.value))[0];
}

function studentPct(p: FitProfile, req: ReturnType<typeof parseOffer>): { student?: number; required?: number; label?: string } {
  if (p.aLevelGrades && req.aLevel !== undefined) {
    return { student: aLevelToPct(p.aLevelGrades), required: req.aLevel, label: `Predicted ${p.aLevelGrades}` };
  }
  if (p.ibPoints !== undefined && req.ib !== undefined) {
    return { student: ibToPct(p.ibPoints), required: req.ib, label: `IB ${p.ibPoints}` };
  }
  // Fall back to percentages: convert whatever the student has.
  const s = p.boardPercent ?? (p.aLevelGrades ? aLevelToPct(p.aLevelGrades) : p.ibPoints !== undefined ? ibToPct(p.ibPoints) : undefined);
  const r = req.percent ?? req.aLevel ?? req.ib;
  const label = p.boardPercent !== undefined ? `${Math.round(p.boardPercent)}%` : p.aLevelGrades ? `Predicted ${p.aLevelGrades}` : p.ibPoints !== undefined ? `IB ${p.ibPoints}` : undefined;
  return { student: s, required: r, label };
}

const round = (x: number) => Math.round(x);

export function computeFit(uni: University, programme: Programme, profile: FitProfile, route = mainRoute(uni)): FitResult {
  const factors: FitResult['factors'] = [];
  const reasons: { text: string; weight: number }[] = [];
  let exponent = 0;

  // 1. Academic margin.
  const offer = route ? offerFor(programme, route) : programme.typicalOffer;
  const req = parseOffer(offer);
  if (req.percent === undefined && route?.requirements.minBoardPercent) req.percent = route.requirements.minBoardPercent;
  const ac = studentPct(profile, req);
  if (ac.student !== undefined && ac.required !== undefined) {
    const steps = (ac.student - ac.required) / 5;
    exponent += 0.8 * steps;
    const offerText = req.aLevel !== undefined && profile.aLevelGrades ? (offer?.match(/(?:A\*|[A-E]){3}(?:\s*(?:-|–|to)\s*(?:A\*|[A-E]){3})?/)?.[0] ?? '') : `${round(ac.required)}%`;
    const effect = steps >= 0.2 ? 'helps' : steps <= -0.2 ? 'hurts' : 'neutral';
    factors.push({ label: `${ac.label} vs typical ${offerText}`, effect });
    reasons.push({ text: steps >= 0 ? `${ac.label} meets ${offerText}` : `${ac.label} vs ${offerText}`, weight: Math.abs(steps) * 0.8 });
  } else {
    factors.push({ label: 'No grades on file yet', effect: 'neutral' });
  }

  // 2. Test margin.
  const satBand = route?.requirements.satMid50;
  const policy = route?.requirements.testPolicy;
  if (satBand && policy !== 'blind' && policy !== 'not_applicable') {
    const [lo, hi] = satBand;
    if (profile.sat !== undefined) {
      const t = (profile.sat - (lo + hi) / 2) / (hi - lo);
      exponent += 1.5 * t;
      factors.push({ label: `SAT ${profile.sat} vs ${lo}-${hi} middle 50%`, effect: t > 0.1 ? 'helps' : t < -0.1 ? 'hurts' : 'neutral' });
      reasons.push({ text: `SAT ${profile.sat} vs ${lo}-${hi}`, weight: Math.abs(t) * 1.5 + 0.01 });
    } else if (policy === 'required') {
      exponent -= 0.75;
      factors.push({ label: 'SAT required and not on file', effect: 'hurts' });
      reasons.push({ text: 'SAT required, add your score', weight: 0.75 });
    } else {
      factors.push({ label: 'Test-optional: no SAT needed', effect: 'neutral' });
      reasons.push({ text: 'Test-optional', weight: 0.05 });
    }
  }

  // 3. Profile bonus.
  for (const [key, label] of [['activities', 'Activities'], ['essay', 'Essay']] as const) {
    const v = profile[key];
    if (!v) continue;
    const b = v === 'strong' ? 0.25 : v === 'weak' ? -0.25 : 0;
    exponent += b;
    factors.push({ label: `${label}: ${v}`, effect: b > 0 ? 'helps' : b < 0 ? 'hurts' : 'neutral' });
    if (b > 0) reasons.push({ text: `${label.toLowerCase()} help`, weight: 0.02 });
  }

  // 4. Chance and band. The multiplier is capped at 2x the admit rate: grades above the bar help, but never guarantee.
  exponent = Math.min(exponent, 1);
  const rate = uni.acceptanceRatePct.value ?? SELECTIVITY_DEFAULT_RATE[uni.selectivity];
  const chance = Math.max(1, Math.min(95, rate * 2 ** exponent));
  const chancePct = chance < 10 ? Math.max(1, Math.round(chance)) : Math.round(chance);
  let band: FitBand;
  if (rate < 10 || uni.selectivity === 'most_selective') band = 'reach';
  else band = chancePct < 30 ? 'reach' : chancePct < 65 ? 'target' : 'safe';

  const allMet = factors.every((f) => f.effect !== 'hurts') && factors.some((f) => f.effect === 'helps');
  let reason: string;
  if (band !== 'reach' && allMet) reason = 'Meets all score bands';
  else {
    const top = reasons.sort((a, b) => b.weight - a.weight).slice(0, 2).map((r) => r.text);
    reason = top.length ? top.join(' · ') : 'Based on published admit rate';
  }
  if (band === 'reach' && (rate < 10 || uni.selectivity === 'most_selective')) {
    reason = `${reason} · ${rate < 1 ? 'under 1' : round(rate)}% admitted`;
  }
  return { universityId: uni.id, programmeId: programme.id, band, chancePct, reason: capitalise(reason), factors };
}

function capitalise(s: string) {
  return s ? s[0]!.toUpperCase() + s.slice(1) : s;
}

/** Readiness of the four fit signals (PDF 6d). */
export interface ReadinessSignal {
  key: 'academic' | 'essay' | 'activities' | 'tests';
  label: string;
  rating?: string;
  source?: string;
  missing: boolean;
}

export function readiness(p: FitProfile, sources: Partial<Record<ReadinessSignal['key'], string>> = {}): { pct: number; signals: ReadinessSignal[] } {
  const academic = p.aLevelGrades ?? (p.ibPoints !== undefined ? `IB ${p.ibPoints}` : p.boardPercent !== undefined ? `${Math.round(p.boardPercent)}%` : undefined);
  const academicRating = academicStrength(p);
  const signals: ReadinessSignal[] = [
    { key: 'academic', label: 'Academic strength', rating: academic ? `${academicRating} (${academic})` : undefined, source: sources.academic, missing: !academic },
    { key: 'essay', label: 'Essay quality', rating: p.essay ? STRENGTH_LABEL[p.essay] : undefined, source: sources.essay, missing: !p.essay },
    { key: 'activities', label: 'Activity impact', rating: p.activities ? ACTIVITY_LABEL[p.activities] : undefined, source: sources.activities, missing: !p.activities },
    { key: 'tests', label: 'Test scores', rating: p.sat !== undefined ? `SAT ${p.sat}${p.ielts ? ` · IELTS ${p.ielts}` : ''}` : p.ielts ? `IELTS ${p.ielts}` : undefined, source: sources.tests, missing: p.sat === undefined && !p.ielts },
  ];
  const pct = Math.round((signals.filter((s) => !s.missing).length / signals.length) * 100);
  return { pct, signals };
}

const STRENGTH_LABEL: Record<Strength, string> = { weak: 'Developing', average: 'Good', strong: 'Strong' };
const ACTIVITY_LABEL: Record<Strength, string> = { weak: 'Low', average: 'Medium', strong: 'High' };

export function academicStrength(p: FitProfile): string {
  const pct = p.aLevelGrades ? aLevelToPct(p.aLevelGrades) : p.ibPoints !== undefined ? ibToPct(p.ibPoints) : p.boardPercent;
  if (pct === undefined) return 'Unknown';
  return pct >= 92 ? 'Excellent' : pct >= 85 ? 'Strong' : pct >= 75 ? 'Good' : 'Developing';
}

/** Fit for every programme in a field (or every programme), grouped and sorted for PDF 6g. */
export function fitAll(unis: University[], profile: FitProfile, opts: { fields?: string[]; countries?: string[] } = {}) {
  const out: (FitResult & { university: University; programme: Programme })[] = [];
  for (const u of unis) {
    if (opts.countries?.length && !opts.countries.includes(u.country)) continue;
    const progs = u.programmes.filter((p) => !opts.fields?.length || opts.fields.includes(p.field));
    // One card per university: its best-matching programme.
    const best = progs.map((p) => ({ ...computeFit(u, p, profile), university: u, programme: p })).sort((a, b) => b.chancePct - a.chancePct)[0];
    if (best) out.push(best);
  }
  const by = (b: FitBand) => out.filter((r) => r.band === b).sort((x, y) => x.chancePct - y.chancePct);
  return { reach: by('reach'), target: by('target'), safe: by('safe') };
}
