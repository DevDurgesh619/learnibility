import personasFile from '@/data/personas/index.json';
import fixturePersonasFile from '@/data/fixtures/personas.json';
import type { DataFile, PersonaSummary, Role } from '@/lib/types';

const file = personasFile as DataFile<PersonaSummary>;
const fixtures = fixturePersonasFile as DataFile<PersonaSummary>;

/**
 * Persona picker list: data/personas/index.json, plus fixture people (data/fixtures/personas.json)
 * that the index does not list yet, so fixture-backed demo flows can be logged into before Wave 3.
 * Entries from the index win when both have the same id.
 */
function all(): PersonaSummary[] {
  const ids = new Set(file.items.map((p) => p.id));
  const fromIndex = file.items.map((p) => {
    const fx = fixtures.items.find((f) => f.id === p.id);
    return fx && !p.linkedLearnerIds?.length && fx.linkedLearnerIds?.length ? { ...p, linkedLearnerIds: fx.linkedLearnerIds } : p;
  });
  return [...fromIndex, ...fixtures.items.filter((p) => !ids.has(p.id))];
}

export function listPersonas(): PersonaSummary[] {
  return all().sort((a, b) => (a.order ?? 99) - (b.order ?? 99) || a.name.localeCompare(b.name));
}

export function getPersona(id: string | undefined | null): PersonaSummary | undefined {
  return id ? all().find((p) => p.id === id) : undefined;
}

export function personasByRole(): Map<Role, PersonaSummary[]> {
  const out = new Map<Role, PersonaSummary[]>();
  for (const p of listPersonas()) out.set(p.role, [...(out.get(p.role) ?? []), p]);
  return out;
}
