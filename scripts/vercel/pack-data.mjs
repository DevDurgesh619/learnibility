#!/usr/bin/env node
/**
 * Hosted build step (Vercel): pack the question banks so the server bundle fits serverless size limits.
 * data/questions/** is ~185 MB of pretty JSON; each file becomes minified `*.json.gz` (~22 MB total) and
 * the original is removed from the build copy only. lib/data/source.ts reads both forms transparently.
 * index.json files stay as they are because they are imported at build time.
 * Run only on a disposable checkout: `node scripts/vercel/pack-data.mjs` (the vercel-build script does this).
 */
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';

const root = path.join(process.cwd(), 'data', 'questions');
if (!process.env.VERCEL && !process.argv.includes('--force')) {
  console.log('pack-data: not on Vercel, nothing to do (pass --force to run anyway)');
  process.exit(0);
}
let n = 0, before = 0, after = 0;
function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p);
    else if (e.name.endsWith('.json') && e.name !== 'index.json') {
      const raw = fs.readFileSync(p);
      const gz = zlib.gzipSync(JSON.stringify(JSON.parse(raw.toString('utf8'))), { level: 9 });
      fs.writeFileSync(`${p}.gz`, gz);
      fs.unlinkSync(p);
      n += 1; before += raw.length; after += gz.length;
    }
  }
}
walk(root);
console.log(`pack-data: ${n} files, ${(before / 1e6).toFixed(1)} MB -> ${(after / 1e6).toFixed(1)} MB`);
