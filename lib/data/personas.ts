import personasFile from '@/data/personas/index.json';
import type { DataFile, PersonaSummary, Role } from '@/lib/types';

const file = personasFile as DataFile<PersonaSummary>;

export function listPersonas(): PersonaSummary[] {
  return [...file.items].sort((a, b) => (a.order ?? 99) - (b.order ?? 99) || a.name.localeCompare(b.name));
}

export function getPersona(id: string | undefined | null): PersonaSummary | undefined {
  return id ? file.items.find((p) => p.id === id) : undefined;
}

export function personasByRole(): Map<Role, PersonaSummary[]> {
  const out = new Map<Role, PersonaSummary[]>();
  for (const p of listPersonas()) out.set(p.role, [...(out.get(p.role) ?? []), p]);
  return out;
}
