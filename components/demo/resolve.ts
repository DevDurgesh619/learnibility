import 'server-only';
import { listPersonas } from '@/lib/data/personas';
import type { PersonaSummary } from '@/lib/types';
import type { PersonaRef } from './scenarios';

/** Finds the persona a scenario names: by id, then parent-of-learner, then by name (last name for `parentOf`). */
export function resolvePersona(ref: PersonaRef): PersonaSummary | undefined {
  const all = listPersonas();
  if (ref.id) {
    const hit = all.find((p) => p.id === ref.id);
    if (hit) return hit;
  }
  if (ref.parentOf) {
    const hit = all.find((p) => p.role === 'parent' && p.linkedLearnerIds?.includes(ref.parentOf!));
    if (hit) return hit;
  }
  if (ref.name) {
    const name = ref.name.toLowerCase();
    const exact = all.find((p) => p.name.toLowerCase() === name);
    if (exact) return exact;
    if (ref.parentOf) return all.find((p) => p.role === 'parent' && p.name.toLowerCase().includes(name));
  }
  return undefined;
}

export function refLabel(ref: PersonaRef): string {
  return resolvePersona(ref)?.name ?? ref.name ?? ref.id ?? 'Unknown persona';
}
