/**
 * File sources for the data layer (server only: uses fs).
 *
 * Priority, per learner: data/personas/students/{id}/ when that folder exists, else data/fixtures/students/{id}/.
 * Shared files: data/personas/{adults,classes}/ else data/fixtures/{adults,classes}/.
 * Contributions: every data/fixtures/contrib/*.json file is { schemaVersion, generatedBy, collections: { name: T[] } }
 * and adds records to those collections (screen threads author their own demo content there).
 * Records of a persona-backed learner never come from fixtures.
 */
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';

export function dataRoot(): string {
  return process.env.LEARNIBILITY_DATA_DIR ?? path.join(process.cwd(), 'data');
}

const fileCache = new Map<string, { mtimeMs: number; value: unknown }>();

/**
 * Hosted builds (Vercel) ship data/ packed as minified `*.json.gz` to stay inside serverless size limits
 * (scripts/vercel/pack-data.mjs). Every read and directory listing here treats `x.json.gz` as `x.json`.
 */
function statData(file: string): { st: fs.Stats; real: string; gz: boolean } | undefined {
  try {
    return { st: fs.statSync(file), real: file, gz: false };
  } catch {
    try {
      return { st: fs.statSync(`${file}.gz`), real: `${file}.gz`, gz: true };
    } catch {
      return undefined;
    }
  }
}

/** Text of a data file, plain or packed. Returns undefined when missing. */
export function readDataText(file: string): string | undefined {
  const s = statData(file);
  if (!s) return undefined;
  const buf = fs.readFileSync(s.real);
  return s.gz ? zlib.gunzipSync(buf).toString('utf8') : buf.toString('utf8');
}

/** Parse a JSON file, cached by mtime. Returns undefined when missing. */
export function readJson<T = unknown>(file: string): T | undefined {
  const s = statData(file);
  if (!s) return undefined;
  const hit = fileCache.get(file);
  if (hit && hit.mtimeMs === s.st.mtimeMs) return hit.value as T;
  const buf = fs.readFileSync(s.real);
  const value = JSON.parse(s.gz ? zlib.gunzipSync(buf).toString('utf8') : buf.toString('utf8')) as T;
  fileCache.set(file, { mtimeMs: s.st.mtimeMs, value });
  return value;
}

/** Items of a DataFile, or the array itself, or [obj] for a single-object file. */
export function itemsOf<T>(file: string): T[] {
  const v = readJson<unknown>(file);
  if (v === undefined) return [];
  if (Array.isArray(v)) return v as T[];
  if (v && typeof v === 'object' && Array.isArray((v as { items?: unknown }).items)) return (v as { items: T[] }).items;
  return [v as T];
}

function listDir(dir: string): string[] {
  try {
    return fs.readdirSync(dir).map((f) => (f.endsWith('.json.gz') ? f.slice(0, -3) : f));
  } catch {
    return [];
  }
}

export type SourceKind = 'personas' | 'fixtures';

/** Learner ids that have a persona folder (these win over fixtures). */
export function personaLearnerIds(): Set<string> {
  return new Set(listDir(path.join(dataRoot(), 'personas', 'students')).filter((d) => d.startsWith('lrn_')));
}

export function fixtureLearnerIds(): Set<string> {
  return new Set(listDir(path.join(dataRoot(), 'fixtures', 'students')).filter((d) => d.startsWith('lrn_')));
}

/** Every learner with a data folder, and where it comes from. */
export function learnerSources(): Map<string, SourceKind> {
  const out = new Map<string, SourceKind>();
  for (const id of fixtureLearnerIds()) out.set(id, 'fixtures');
  for (const id of personaLearnerIds()) out.set(id, 'personas');
  return out;
}

export function learnerDir(learnerId: string): { dir: string; kind: SourceKind } | undefined {
  const kind = learnerSources().get(learnerId);
  if (!kind) return undefined;
  return { dir: path.join(dataRoot(), kind, 'students', learnerId), kind };
}

/** students/{id}/{collection}.json items for one learner. */
export function learnerFile<T>(learnerId: string, collection: string): T[] {
  const src = learnerDir(learnerId);
  return src ? itemsOf<T>(path.join(src.dir, `${collection}.json`)) : [];
}

/** Shared folder (adults, classes): personas when it has files, else fixtures. */
export function sharedDir(name: 'adults' | 'classes'): string[] {
  const p = path.join(dataRoot(), 'personas', name);
  const f = path.join(dataRoot(), 'fixtures', name);
  const dirs: string[] = [];
  if (listDir(p).some((x) => x.endsWith('.json'))) dirs.push(p);
  if (listDir(f).some((x) => x.endsWith('.json'))) dirs.push(f);
  return dirs;
}

export function jsonFilesIn(dir: string): string[] {
  return listDir(dir)
    .filter((f) => f.endsWith('.json') && !f.startsWith('_'))
    .sort()
    .map((f) => path.join(dir, f));
}

/** Records contributed to a collection by data/fixtures/contrib/*.json. */
export function contribRecords<T>(collection: string): T[] {
  const out: T[] = [];
  for (const f of jsonFilesIn(path.join(dataRoot(), 'fixtures', 'contrib'))) {
    const v = readJson<{ collections?: Record<string, T[]> }>(f);
    const items = v?.collections?.[collection];
    if (Array.isArray(items)) out.push(...items);
  }
  return out;
}
