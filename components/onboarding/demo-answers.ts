/**
 * Demo shortcut answers ("Answer the rest for me"). Deterministic per student and item, so a rerun of the demo
 * produces the same starting profile: right more often on easy items and prerequisites, a few slips on D3.
 */
import type { Difficulty } from '@/lib/types';

function hash(s: string): number {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return (h >>> 0) / 4294967295;
}

const P_RIGHT: Record<string, number> = { D1: 0.9, D2: 0.72, D3: 0.5, D4: 0.4, D5: 0.3 };

export function demoCorrect(seed: string, item: { id: string; difficulty?: Difficulty; half?: string }): boolean {
  const p = (P_RIGHT[item.difficulty ?? 'D2'] ?? 0.6) + (item.half === 'prerequisite' ? 0.05 : -0.05);
  return hash(`${seed}:${item.id}`) < p;
}

export function demoPick<T>(seed: string, id: string, options: T[], bias = 0.5): T {
  const r = hash(`${seed}:${id}`);
  const i = Math.min(options.length - 1, Math.floor(Math.pow(r, bias < 0.5 ? 2 : 0.7) * options.length));
  return options[i];
}

export function demoNumber(seed: string, id: string): number {
  return hash(`${seed}:${id}`);
}
