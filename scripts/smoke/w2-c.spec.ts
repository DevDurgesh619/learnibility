/**
 * W2-C counsellor smoke test. Plain Playwright (pre-installed `playwright`), no test runner needed:
 *   BASE_URL=http://localhost:3000 node scripts/smoke/w2-c.spec.ts
 * Logs in as each counsellor persona (cookie, same as the /login picker), visits every W2-C route at
 * 1440 and 390 px, fails on console errors or page errors, and saves screenshots to docs/screens/w2-c/.
 */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { chromium } = require('playwright') as { chromium: any };

const BASE = process.env.BASE_URL ?? 'http://localhost:3000';
const OUT = path.join(process.cwd(), 'docs', 'screens', 'w2-c');
const PERSONAS = (process.env.PERSONAS ?? 'csl_heena_qureshi,csl_farah_siddiqui').split(',');
const ROUTES = ['', '/student-360', '/timetable-requests', '/career-sessions', '/risk-flags'];
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
      for (const r of ROUTES) {
        const res = await page.goto(`${BASE}/counsellor${r}`, { waitUntil: 'networkidle' });
        if (!page.url().includes('/counsellor')) { console.log(`skip ${persona}: not a counsellor persona (landed on ${page.url()})`); break; }
        visited++;
        if (!res || res.status() >= 400) failures.push(`${persona} ${r || '/'} ${size.name}: HTTP ${res?.status()}`);
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
        if (overflow > 1) failures.push(`${persona} ${r || '/'} ${size.name}: horizontal overflow ${overflow}px`);
        const name = `${persona.replace(/^csl_/, '')}-${(r || '/caseload').slice(1)}-${size.name}.png`;
        await page.screenshot({ path: path.join(OUT, name), fullPage: true });
      }
      if (errors.length) failures.push(`${persona} ${size.name}: console errors\n  ${errors.join('\n  ')}`);
      await ctx.close();
    }
  }
  await browser.close();
  if (!visited) failures.push('no routes visited');
  if (failures.length) { console.error(failures.join('\n')); process.exit(1); }
  console.log(`W2-C smoke: ${visited} page views OK, screenshots in ${path.relative(process.cwd(), OUT)}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
