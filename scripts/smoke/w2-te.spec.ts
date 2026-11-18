/**
 * W2-TE teacher smoke test. Plain Playwright (pre-installed `playwright`), no test runner needed:
 *   BASE_URL=http://localhost:3000 node scripts/smoke/w2-te.spec.ts
 * Logs in as each teacher persona (cookie, same as the /login picker), visits every W2-TE route at
 * 1440 and 390 px, fails on console errors or page errors, and saves screenshots to docs/screens/w2-te/.
 */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { chromium } = require('playwright') as { chromium: any };

const BASE = process.env.BASE_URL ?? 'http://localhost:3000';
const OUT = path.join(process.cwd(), 'docs', 'screens', 'w2-te');
/** Every teacher persona on the login picker (index + fixture people), or PERSONAS=a,b. */
function teacherIds(): string[] {
  const ids = new Set<string>();
  for (const f of ['data/personas/index.json', 'data/fixtures/personas.json']) {
    try { for (const p of JSON.parse(fs.readFileSync(f, 'utf8')).items ?? []) if (p.role === 'teacher') ids.add(p.id); } catch { /* missing file */ }
  }
  return [...ids].slice(0, 2);
}
const PERSONAS = process.env.PERSONAS ? process.env.PERSONAS.split(',') : teacherIds();
const ROUTES = ['', '?chapter=FIRST', '/assign', '/class-gaps', '/students', '/students?id=FIRST_STUDENT', '/gap-log', '/gap-log?show=all'];
const SIZES = [{ name: 'desktop', width: 1440, height: 900 }, { name: 'mobile', width: 390, height: 844 }];

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const failures: string[] = [];
  let visited = 0;
  for (const persona of PERSONAS) {
    for (const size of SIZES) {
      const ctx = await browser.newContext({ viewport: { width: size.width, height: size.height }, deviceScaleFactor: 1 });
      await ctx.addCookies([{ name: 'learnibility_persona', value: persona, url: BASE }]);
      const page = await ctx.newPage();
      const errors: string[] = [];
      page.on('console', (m: { type(): string; text(): string }) => { if (m.type() === 'error') errors.push(m.text()); });
      page.on('pageerror', (e: Error) => errors.push(String(e)));
      let firstStudent = '';
      let firstChapter = '';
      for (const r0 of ROUTES) {
        if (r0.includes('FIRST_STUDENT') && !firstStudent) continue;
        const r = r0.replace('FIRST_STUDENT', firstStudent).replace('FIRST', firstChapter);
        if (r0.includes('chapter=FIRST') && !firstChapter) {
          // Pick the first chapter from the filter on the Classes page.
          await page.goto(`${BASE}/teacher`, { waitUntil: 'networkidle' });
          firstChapter = await page.evaluate(() => (document.querySelector('select option:nth-child(2)') as HTMLOptionElement | null)?.value ?? '');
          if (!firstChapter) continue;
        }
        const res = await page.goto(`${BASE}/teacher${r.replace('FIRST', firstChapter)}`, { waitUntil: 'networkidle' });
        if (!page.url().includes('/teacher')) { console.log(`skip ${persona}: not a teacher persona (landed on ${page.url()})`); break; }
        if (r0 === '/students' && !firstStudent) {
          firstStudent = await page.evaluate(() => new URL((document.querySelector('a[href*="/teacher/students?"][href*="id="]') as HTMLAnchorElement | null)?.href ?? 'http://x/').searchParams.get('id') ?? '');
        }
        visited++;
        if (!res || res.status() >= 400) failures.push(`${persona} ${r || '/'} ${size.name}: HTTP ${res?.status()}`);
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
        if (overflow > 1) failures.push(`${persona} ${r || '/'} ${size.name}: horizontal overflow ${overflow}px`);
        const name = `${persona.replace(/^tch_/, '')}-${(r0 || '/classes').replace(/^[/?]/, '').replace(/[^a-z0-9]+/gi, '-').toLowerCase()}-${size.name}.png`;
        await page.screenshot({ path: path.join(OUT, name), fullPage: true, caret: 'initial' });
      }
      if (errors.length) failures.push(`${persona} ${size.name}: console errors\n  ${errors.join('\n  ')}`);
      await ctx.close();
    }
  }
  await browser.close();
  if (!visited) failures.push('no routes visited');
  if (failures.length) { console.error(failures.join('\n')); process.exit(1); }
  console.log(`W2-TE smoke: ${visited} page views OK, screenshots in ${path.relative(process.cwd(), OUT)}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
