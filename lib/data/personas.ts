import personasFile from '@/data/personas/index.json';
import fixturePersonasFile from '@/data/fixtures/personas.json';
import type { DataFile, PersonaSummary, Role } from '@/lib/types';
import { records } from '@/lib/store/collections';
import { getTutor } from './catalogue';
import type { Adult, Student } from './types';

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
  if (!id) return undefined;
  return all().find((p) => p.id === id) ?? fromStore(id);
}

/**
 * Fallback for people created at runtime (e.g. a learner converted from a CRM lead) who are in the
 * store but not in any persona list, and any catalogue tutor, so they can still sign in. They do not appear on the picker.
 */
function fromStore(id: string): PersonaSummary | undefined {
  if (id.startsWith('lrn_')) {
    const s = records<Student>('student').find((r) => r.id === id);
    if (!s) return undefined;
    return {
      id: s.id, role: 'student', name: s.name, story: s.goal ?? 'New family from sales',
      grade: s.grade, board: s.board, stream: s.stream, programme: s.programme, linkedLearnerIds: [],
    };
  }
  if (id.startsWith('tut_')) {
    const t = getTutor(id);
    return t ? { id: t.id, role: 'tutor', name: t.displayName, story: t.headline, linkedLearnerIds: [] } : undefined;
  }
  const a = records<Adult>('adults').find((r) => r.id === id);
  if (!a) return undefined;
  return { id: a.id, role: a.role, name: a.name, story: a.headline ?? '', linkedLearnerIds: a.learnerIds };
}

export function personasByRole(): Map<Role, PersonaSummary[]> {
  const out = new Map<Role, PersonaSummary[]>();
  for (const p of listPersonas()) out.set(p.role, [...(out.get(p.role) ?? []), p]);
  return out;
}
