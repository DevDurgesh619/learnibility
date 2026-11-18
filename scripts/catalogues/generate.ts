/**
 * Builds /data/catalogues/*.json from the source modules in scripts/catalogues/src.
 * Run: npx tsx scripts/catalogues/generate.ts
 */
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import type { Career, FxTable, Resource, Skill, University } from '../../lib/types/catalogue';
import { CAREERS } from './src/careers';
import { EXAMS } from './src/exams';
import { RESOURCES } from './src/resources';
import { SKILLS } from './src/skills';
import { TUTORS } from './src/tutors';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..', '..');
const outDir = join(root, 'data', 'catalogues');
const GENERATED_BY = 'scripts/catalogues/generate.ts';

export const FX: FxTable = {
  asOf: '2026-11-18',
  sourceUrl: 'https://www.rbi.org.in/scripts/ReferenceRateArchive.aspx',
  inrPer: { USD: 88.5, GBP: 117.0, CAD: 63.5, AUD: 58.0 },
};

function write<T>(name: string, items: T[]): void {
  mkdirSync(outDir, { recursive: true });
  const file = join(outDir, `${name}.json`);
  writeFileSync(file, JSON.stringify({ schemaVersion: 1, generatedBy: GENERATED_BY, items }, null, 2) + '\n');
  console.log(`${name}.json: ${items.length} items`);
}

// Skills: fill resourceIds from Resource.skillOutcomes.
const resources: Resource[] = RESOURCES;
const skills: Skill[] = SKILLS.map((s) => ({
  ...s,
  resourceIds: resources.filter((r) => r.skillOutcomes.some((o) => o.skillId === s.id)).map((r) => r.id),
}));

// Universities: merged from the researched source files, sorted by country then name.
const COUNTRY_ORDER = ['in', 'us', 'uk', 'ca', 'au'];
const uniFiles = ['universities-in-au.json', 'universities-us-uk-ca.json'].map((f) => join(here, 'src', f));
const universities: University[] = uniFiles
  .filter((f) => existsSync(f))
  .flatMap((f) => JSON.parse(readFileSync(f, 'utf8')) as University[])
  .sort((a, b) => COUNTRY_ORDER.indexOf(a.country) - COUNTRY_ORDER.indexOf(b.country) || a.name.localeCompare(b.name));

const careers: Career[] = CAREERS;

write('exams', EXAMS);
write('skills', skills);
write('careers', careers);
write('tutors', TUTORS);
write('resources', resources);
write('universities', universities);
write('fx', [FX]);
