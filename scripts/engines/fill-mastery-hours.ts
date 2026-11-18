/**
 * Fill Subtopic.learnHours / masterHours in data/curriculum/{subjectId}.json from engine 1 (masteryTime).
 * W2 owns the curriculum files; this script only touches those two fields.
 *
 *   npx tsx scripts/engines/fill-mastery-hours.ts            # dry run: report what would change
 *   npx tsx scripts/engines/fill-mastery-hours.ts --write    # write the files
 *   npx tsx scripts/engines/fill-mastery-hours.ts --write cbse-g8-maths   # one subject
 */
import { readdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { masteryTimeAllBands } from '../../lib/engines/masteryTime';
import type { Subtopic } from '../../lib/types';

const dir = path.resolve(process.cwd(), 'data/curriculum');
const args = process.argv.slice(2);
const write = args.includes('--write');
const only = args.filter((a) => !a.startsWith('--'));
const skip = new Set(['subjects.json', 'streams.json', 'sheet-reference.json']);

let files = 0, subs = 0, changed = 0;
for (const f of readdirSync(dir).filter((x) => x.endsWith('.json') && !skip.has(x))) {
  if (only.length && !only.includes(f.replace(/\.json$/, ''))) continue;
  const file = path.join(dir, f);
  const data = JSON.parse(readFileSync(file, 'utf8')) as { subtopics?: Subtopic[] };
  if (!Array.isArray(data.subtopics)) continue;
  files++;
  let fileChanged = false;
  for (const s of data.subtopics) {
    subs++;
    const { learnHours, masterHours } = masteryTimeAllBands(s);
    if (JSON.stringify(s.learnHours) !== JSON.stringify(learnHours) || JSON.stringify(s.masterHours) !== JSON.stringify(masterHours)) {
      s.learnHours = learnHours;
      s.masterHours = masterHours;
      changed++;
      fileChanged = true;
    }
  }
  if (write && fileChanged) writeFileSync(file, JSON.stringify(data, null, 1) + '\n');
}
console.log(`${files} subject files, ${subs} subtopics, ${changed} ${write ? 'updated' : 'would change'}`);
