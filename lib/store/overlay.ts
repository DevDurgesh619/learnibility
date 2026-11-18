/**
 * Demo write overlay. Every demo write (attempt, task done, booking, request, comment, approval, recomputed
 * gaps and timetable) is one row; reads merge rows over the JSON files. "Reset demo" deletes all rows.
 *
 * Backend: SQLite file via better-sqlite3 (already installed for Prisma's adapter) at
 * LEARNIBILITY_OVERLAY_DB (default .data/overlay.sqlite). Falls back to memory when SQLite cannot open
 * (read-only hosting) or when LEARNIBILITY_OVERLAY=memory (tests).
 *
 * On Vercel (VERCEL=1) the default is memory: the filesystem is read-only apart from /tmp, which is per
 * instance anyway, so SQLite would add a native module without making writes more durable. Demo writes
 * last while the server instance stays warm; a cold start begins from the seeded data, same as Reset.
 * Set LEARNIBILITY_OVERLAY=sqlite with LEARNIBILITY_OVERLAY_DB=/tmp/overlay.sqlite to force SQLite there.
 */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

export interface OverlayRow {
  seq: number;
  collection: string;
  key: string;
  learnerId: string | null;
  deleted: boolean;
  data: unknown;
}

export interface OverlayBackend {
  kind: 'sqlite' | 'memory';
  put(collection: string, key: string, learnerId: string | null, data: unknown, deleted?: boolean): number;
  rows(collection: string): OverlayRow[];
  /** Highest seq written; changes on every write (cache key). */
  version(): number;
  clear(): void;
  count(): number;
}

class MemoryBackend implements OverlayBackend {
  kind = 'memory' as const;
  private all: OverlayRow[] = [];
  private seq = 0;
  put(collection: string, key: string, learnerId: string | null, data: unknown, deleted = false) {
    this.seq += 1;
    this.all.push({ seq: this.seq, collection, key, learnerId, deleted, data: structuredClone(data) });
    return this.seq;
  }
  rows(collection: string) {
    return this.all.filter((r) => r.collection === collection);
  }
  version() {
    return this.seq;
  }
  clear() {
    this.all = [];
    // keep seq increasing so caches keyed on version never see a stale value
    this.seq += 1;
  }
  count() {
    return this.all.length;
  }
}

type Db = {
  prepare(sql: string): { run(...a: unknown[]): { lastInsertRowid: number | bigint }; all(...a: unknown[]): unknown[]; get(...a: unknown[]): unknown };
  exec(sql: string): void;
  pragma(s: string): unknown;
};

class SqliteBackend implements OverlayBackend {
  kind = 'sqlite' as const;
  constructor(private db: Db) {
    db.pragma('journal_mode = WAL');
    db.exec(`CREATE TABLE IF NOT EXISTS overlay (
      seq INTEGER PRIMARY KEY AUTOINCREMENT,
      collection TEXT NOT NULL,
      key TEXT NOT NULL,
      learner_id TEXT,
      deleted INTEGER NOT NULL DEFAULT 0,
      data TEXT NOT NULL,
      written_at TEXT NOT NULL DEFAULT (datetime('now'))
    );
    CREATE INDEX IF NOT EXISTS overlay_collection ON overlay(collection, seq);
    CREATE TABLE IF NOT EXISTS overlay_meta (k TEXT PRIMARY KEY, v INTEGER NOT NULL);
    INSERT OR IGNORE INTO overlay_meta (k, v) VALUES ('epoch', 0);`);
  }
  put(collection: string, key: string, learnerId: string | null, data: unknown, deleted = false) {
    const r = this.db
      .prepare('INSERT INTO overlay (collection, key, learner_id, deleted, data) VALUES (?, ?, ?, ?, ?)')
      .run(collection, key, learnerId, deleted ? 1 : 0, JSON.stringify(data ?? null));
    return Number(r.lastInsertRowid);
  }
  rows(collection: string) {
    const rs = this.db.prepare('SELECT seq, collection, key, learner_id, deleted, data FROM overlay WHERE collection = ? ORDER BY seq').all(collection) as {
      seq: number; collection: string; key: string; learner_id: string | null; deleted: number; data: string;
    }[];
    return rs.map((r) => ({ seq: r.seq, collection: r.collection, key: r.key, learnerId: r.learner_id, deleted: !!r.deleted, data: JSON.parse(r.data) }));
  }
  version() {
    const a = this.db.prepare('SELECT COALESCE(MAX(seq), 0) AS m FROM overlay').get() as { m: number };
    const b = this.db.prepare("SELECT v FROM overlay_meta WHERE k = 'epoch'").get() as { v: number };
    return a.m * 1000 + b.v;
  }
  clear() {
    this.db.exec("DELETE FROM overlay; UPDATE overlay_meta SET v = v + 1 WHERE k = 'epoch';");
  }
  count() {
    return (this.db.prepare('SELECT COUNT(*) AS n FROM overlay').get() as { n: number }).n;
  }
}

const g = globalThis as unknown as { __learnibilityOverlay?: OverlayBackend; __learnibilityResetEpoch?: number };

/**
 * Reset across server instances. On Vercel, route handlers (/demo/reset, /demo/go, /api/demo-reset) run in a
 * different function from the pages, each with its own memory, so clearing in the handler alone would not
 * reach the pages. Each reset therefore also stamps this cookie with its time; currentPersona() hands the
 * cookie to syncResetEpoch(), and any instance that has not yet seen that reset clears its overlay.
 */
export const RESET_COOKIE = 'learnibility_reset';

/** Clear this instance's overlay once for each newer reset stamp. Returns true when it cleared. */
export function syncResetEpoch(epoch: number | undefined): boolean {
  if (!epoch || !Number.isFinite(epoch)) return false;
  if ((g.__learnibilityResetEpoch ?? 0) >= epoch) return false;
  g.__learnibilityResetEpoch = epoch;
  overlay().clear();
  return true;
}

/** Record a reset done here; returns its stamp for RESET_COOKIE. */
export function markReset(): number {
  const epoch = Math.max(Date.now(), (g.__learnibilityResetEpoch ?? 0) + 1);
  g.__learnibilityResetEpoch = epoch;
  return epoch;
}

function open(): OverlayBackend {
  const mode = process.env.LEARNIBILITY_OVERLAY ?? (process.env.VERCEL ? 'memory' : 'sqlite');
  if (mode === 'memory') return new MemoryBackend();
  try {
    const file = process.env.LEARNIBILITY_OVERLAY_DB ?? path.join(process.cwd(), '.data', 'overlay.sqlite');
    fs.mkdirSync(path.dirname(file), { recursive: true });
    const ignore = path.join(path.dirname(file), '.gitignore');
    if (!fs.existsSync(ignore)) fs.writeFileSync(ignore, '*\n');
    const require = createRequire(import.meta.url);
    const Database = require('better-sqlite3') as new (f: string) => Db;
    return new SqliteBackend(new Database(file));
  } catch (err) {
    console.warn('[learnibility] overlay: SQLite unavailable, using memory:', (err as Error).message);
    return new MemoryBackend();
  }
}

export function overlay(): OverlayBackend {
  if (!g.__learnibilityOverlay) g.__learnibilityOverlay = open();
  return g.__learnibilityOverlay;
}

/** Tests: swap in a fresh memory backend. */
export function useMemoryOverlay(): OverlayBackend {
  g.__learnibilityOverlay = new MemoryBackend();
  return g.__learnibilityOverlay;
}
