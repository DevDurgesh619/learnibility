/**
 * Student 360: the 430 parameters grouped by the 12 profile sections, each with the learner's value,
 * source method, date, confidence and tier, plus evidence density per section.
 * Pure: the page passes the parameter definitions, the values a counsellor may see and `now`.
 */
import type { Cadence, Confidence, ProfileParameter, ProfileSection, SourceMethod, Tier } from '@/lib/types';
import { PROFILE_SECTIONS } from '@/lib/types';

export interface Value360 {
  paramId: string;
  value?: unknown;
  source?: SourceMethod;
  asOfUtc?: string;
  confidence?: Confidence;
  tier: Tier;
  mode?: 'full' | 'summary';
}

export interface Row360 {
  param: Pick<ProfileParameter, 'id' | 'number' | 'name' | 'category' | 'dataType' | 'tier' | 'cadence' | 'methods' | 'phase1Default' | 'handlingNote'>;
  value?: Value360;
  /** Older than the parameter's cadence allows. */
  stale: boolean;
}

export interface Section360 {
  section: ProfileSection;
  rows: Row360[];
  total: number;
  filled: number;
  /** filled ÷ total, 0..1 */
  density: number;
  densityLabel: 'Sparse' | 'Thin' | 'Good' | 'Rich';
  highConfidence: number;
  lowConfidence: number;
  stale: number;
  tiers: Record<Tier, number>;
  /** Most common source method among filled values. */
  topSources: { source: SourceMethod; count: number }[];
}

/** Days a value stays fresh per cadence. "Once" and "As needed" never go stale. */
export const CADENCE_DAYS: Record<Cadence, number | null> = {
  Once: null, Annual: 400, Term: 140, Monthly: 45, Weekly: 10, Continuous: 10, 'As needed': null,
};

const DAY = 86_400_000;

export function isStale(cadence: Cadence, asOfUtc: string | undefined, now: Date): boolean {
  const days = CADENCE_DAYS[cadence];
  if (!asOfUtc || days == null) return false;
  return (now.getTime() - Date.parse(asOfUtc)) / DAY > days;
}

export function densityLabel(d: number): Section360['densityLabel'] {
  if (d >= 0.75) return 'Rich';
  if (d >= 0.5) return 'Good';
  if (d >= 0.25) return 'Thin';
  return 'Sparse';
}

/** Latest value per parameter. */
export function latestValues(values: Value360[]): Map<string, Value360> {
  const out = new Map<string, Value360>();
  for (const v of values) {
    const cur = out.get(v.paramId);
    if (!cur || (v.asOfUtc ?? '') > (cur.asOfUtc ?? '')) out.set(v.paramId, v);
  }
  return out;
}

export function buildStudent360(params: ProfileParameter[], values: Value360[], now: Date): Section360[] {
  const latest = latestValues(values);
  return PROFILE_SECTIONS.map((section) => {
    const rows: Row360[] = params
      .filter((p) => p.section === section)
      .sort((a, b) => a.number - b.number)
      .map((p) => {
        const value = latest.get(p.id);
        return {
          param: { id: p.id, number: p.number, name: p.name, category: p.category, dataType: p.dataType, tier: p.tier, cadence: p.cadence, methods: p.methods, phase1Default: p.phase1Default, handlingNote: p.handlingNote },
          value,
          stale: value ? isStale(p.cadence, value.asOfUtc, now) : false,
        };
      });
    const filledRows = rows.filter((r) => r.value);
    const sources = new Map<SourceMethod, number>();
    for (const r of filledRows) if (r.value?.source) sources.set(r.value.source, (sources.get(r.value.source) ?? 0) + 1);
    const tiers: Record<Tier, number> = { T1: 0, T2: 0, T3: 0, C: 0 };
    for (const r of rows) tiers[r.param.tier]++;
    const density = rows.length ? filledRows.length / rows.length : 0;
    return {
      section, rows, total: rows.length, filled: filledRows.length, density, densityLabel: densityLabel(density),
      highConfidence: filledRows.filter((r) => r.value?.confidence === 'high').length,
      lowConfidence: filledRows.filter((r) => r.value?.confidence === 'low').length,
      stale: rows.filter((r) => r.stale).length,
      tiers,
      topSources: [...sources].map(([source, count]) => ({ source, count })).sort((a, b) => b.count - a.count).slice(0, 3),
    };
  });
}

export function overallCompleteness(sections: Section360[]): number {
  const total = sections.reduce((s, x) => s + x.total, 0);
  return total ? sections.reduce((s, x) => s + x.filled, 0) / total : 0;
}

/** Display a profile value compactly. */
export function displayValue(v: unknown): string {
  if (v == null || v === '') return '—';
  if (Array.isArray(v)) return v.map(displayValue).join(', ');
  if (typeof v === 'boolean') return v ? 'Yes' : 'No';
  if (typeof v === 'number') return Number.isInteger(v) ? String(v) : v.toFixed(2);
  if (typeof v === 'object') {
    return Object.entries(v as Record<string, unknown>).map(([k, x]) => `${k}: ${displayValue(x)}`).join(' · ');
  }
  return String(v).replace(/_/g, ' ');
}
