/**
 * Named record collections: JSON base (personas > fixtures > contrib) merged with the demo overlay.
 * Screens never call this directly; they use lib/data reads and lib/actions writes.
 */
import { contribRecords, itemsOf, jsonFilesIn, learnerFile, learnerSources, personaLearnerIds, sharedDir } from '@/lib/data/source';
import { overlay } from './overlay';

type Rec = Record<string, unknown>;

interface CollectionDef {
  /** Unique key of a record within the collection. */
  key: (r: Rec) => string;
  /** Learners a record belongs to (for persona/fixture switching and per-learner reads). */
  learners: (r: Rec) => string[];
  /** 'learner': read from students/{id}/{file}.json; 'shared': from adults/ or classes/. */
  scope: 'learner' | 'shared';
  file?: string;
}

const byId = (r: Rec) => String(r.id);
const one = (r: Rec) => (r.learnerId ? [String(r.learnerId)] : []);
const many = (r: Rec) => (Array.isArray(r.learnerIds) ? (r.learnerIds as string[]) : one(r));

export const COLLECTIONS = {
  student: { scope: 'learner', key: byId, learners: (r: Rec) => [String(r.id)] },
  profile: { scope: 'learner', key: (r: Rec) => `${r.learnerId}:${r.paramId}`, learners: one },
  events: { scope: 'learner', key: (r: Rec) => String(r.eventId), learners: one },
  attempts: { scope: 'learner', key: byId, learners: one },
  mastery: { scope: 'learner', key: (r: Rec) => `${r.learnerId}:${r.subtopicId}`, learners: one },
  alr: { scope: 'learner', key: (r: Rec) => `${r.learnerId}:${r.chapterId}:${r.asOfUtc}`, learners: one },
  gaps: { scope: 'learner', key: byId, learners: one },
  plans: { scope: 'learner', key: byId, learners: one },
  timetable: { scope: 'learner', key: (r: Rec) => `${r.learnerId}:${r.weekStart}`, learners: one },
  tasks: { scope: 'learner', key: byId, learners: one },
  requests: { scope: 'learner', key: byId, learners: one },
  bookings: { scope: 'learner', key: byId, learners: one },
  sessions: { scope: 'learner', key: byId, learners: many },
  meetings: { scope: 'learner', key: byId, learners: one },
  careers: { scope: 'learner', key: (r: Rec) => String(r.learnerId), learners: one },
  applications: { scope: 'learner', key: byId, learners: one },
  shortlist: { scope: 'learner', key: (r: Rec) => `${r.learnerId}:${r.universityId}:${r.programmeId ?? ''}`, learners: one },
  finance: { scope: 'learner', key: (r: Rec) => `${r.learnerId}:${r.universityId}`, learners: one },
  documents: { scope: 'learner', key: byId, learners: one },
  invoices: { scope: 'learner', key: byId, learners: one },
  consents: { scope: 'learner', key: byId, learners: one },
  messages: { scope: 'learner', key: byId, learners: one },
  comments: { scope: 'learner', key: byId, learners: one },
  approvals: { scope: 'learner', key: byId, learners: one },
  assignments: { scope: 'learner', key: byId, learners: one },
  tutorNotes: { scope: 'learner', key: byId, learners: one },
  payouts: { scope: 'shared', key: byId, learners: () => [] },
  adults: { scope: 'shared', key: byId, learners: () => [] },
  sections: { scope: 'shared', key: byId, learners: () => [] },
} satisfies Record<string, CollectionDef>;

export type CollectionName = keyof typeof COLLECTIONS;

function def(name: CollectionName): CollectionDef {
  return COLLECTIONS[name] as CollectionDef;
}

/** JSON base records, before the overlay. */
export function baseRecords<T>(name: CollectionName): T[] {
  const d = def(name);
  const personaIds = personaLearnerIds();
  const out: Rec[] = [];
  if (d.scope === 'learner') {
    for (const id of learnerSources().keys()) out.push(...learnerFile<Rec>(id, d.file ?? name));
  } else if (name === 'adults') {
    for (const dir of sharedDir('adults').slice(0, 1)) for (const f of jsonFilesIn(dir)) out.push(...itemsOf<Rec>(f));
  } else if (name === 'sections') {
    for (const dir of sharedDir('classes').slice(0, 1)) for (const f of jsonFilesIn(dir)) out.push(...itemsOf<Rec>(f));
  }
  // Contributions never override persona-backed learners.
  for (const r of contribRecords<Rec>(name)) {
    const ls = d.learners(r);
    if (ls.length && ls.every((l) => personaIds.has(l))) continue;
    out.push(r);
  }
  return out as T[];
}

// Merged cache, keyed on the overlay version so every write invalidates it.
const merged = new Map<string, { version: number; items: Rec[] }>();

/** Base records merged with overlay writes (later writes win; deletes remove). */
export function records<T>(name: CollectionName): T[] {
  const ov = overlay();
  const version = ov.version();
  const hit = merged.get(name);
  if (hit && hit.version === version && process.env.NODE_ENV === 'production') return hit.items as T[];
  const d = def(name);
  const map = new Map<string, Rec>();
  for (const r of baseRecords<Rec>(name)) map.set(d.key(r), r);
  for (const row of ov.rows(name)) {
    if (row.deleted) map.delete(row.key);
    else map.set(row.key, row.data as Rec);
  }
  const items = [...map.values()];
  merged.set(name, { version, items });
  return items as T[];
}

/** Records belonging to one learner. */
export function learnerRecords<T>(name: CollectionName, learnerId: string): T[] {
  const d = def(name);
  return records<Rec>(name).filter((r) => d.learners(r).includes(learnerId)) as T[];
}

/** Upsert a record into the overlay. Returns its key. */
export function writeRecord<T extends object>(name: CollectionName, record: T): string {
  const d = def(name);
  const r = record as unknown as Rec;
  const key = d.key(r);
  overlay().put(name, key, d.learners(r)[0] ?? null, record);
  return key;
}

export function deleteRecord(name: CollectionName, key: string, learnerId?: string): void {
  overlay().put(name, key, learnerId ?? null, null, true);
}

/** Keys of records that exist only because of overlay writes (not in JSON). */
export function overlayKeys(name: CollectionName): Set<string> {
  return new Set(overlay().rows(name).filter((r) => !r.deleted).map((r) => r.key));
}

export function isOverlayEmpty(): boolean {
  return overlay().count() === 0;
}
