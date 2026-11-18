/**
 * W2-S2 student daily-loop smoke test. Plain Playwright (pre-installed `playwright`), no test runner needed:
 *   BASE_URL=http://localhost:3000 node scripts/smoke/w2-s2.spec.ts
 * Logs in as student personas (cookie, same as the /login picker), visits every W2-S2 route at 1440 and 390 px,
 * fails on HTTP errors, console or page errors and horizontal overflow, then sends a timetable change request
 * through the modal (PDF 3b) and checks the pending state (3c). Screenshots go to docs/screens/w2-s2/.
 */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { chromium } = require('playwright') as { chromium: any };

const BASE = process.env.BASE_URL ?? 'http://localhost:3000';
const OUT = path.join(process.cwd(), 'docs', 'screens', 'w2-s2');
const PERSONAS = (process.env.PERSONAS ?? 'lrn_kabir_singh,lrn_nikhil_reddy,lrn_zoya_fernandes').split(',');
const ROUTES = [
  '', '?metric=learning-rate', '/timetable', '/timetable?view=month', '/inventory', '/inventory/class-9', '/inventory/essay-drafts',
  '/sessions', '/sessions?tab=past', '/career', '/career/search?q=data', '/career/career-data-analyst', '/career/career-data-analyst/gap',
  '/career?tab=insights&uni=uni-in-iit-bombay&role=career-data-analyst&city=Bengaluru',
];
const SIZES = [{ name: 'desktop', width: 1440, height: 900 }, { name: 'mobile', width: 390, height: 844 }];
const fileName = (persona: string, r: string, size: string) =>
  `${persona.replace(/^lrn_/, '').split('_')[0]}-${(r || 'home').replace(/^\//, '').replace(/[/?=&]+/g, '-').slice(0, 60)}-${size}.png`;

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
        const res = await page.goto(`${BASE}/student${r}`, { waitUntil: 'networkidle' });
        if (!page.url().includes('/student')) { console.log(`skip ${persona}: not a student persona (landed on ${page.url()})`); break; }
        visited++;
        if (!res || res.status() >= 400) failures.push(`${persona} ${r || '/'} ${size.name}: HTTP ${res?.status()}`);
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
        if (overflow > 1) failures.push(`${persona} ${r || '/'} ${size.name}: horizontal overflow ${overflow}px`);
        await page.screenshot({ path: path.join(OUT, fileName(persona, r, size.name)), fullPage: true });
      }
      if (errors.length) failures.push(`${persona} ${size.name}: console errors\n  ${errors.join('\n  ')}`);
      await ctx.close();
    }
  }

  // PDF 3b → 3c: request a change, see it pending, undo it.
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  await ctx.addCookies([{ name: 'learnibility_persona', value: PERSONAS[0], url: BASE }]);
  const page = await ctx.newPage();
  await page.goto(`${BASE}/student/timetable`, { waitUntil: 'networkidle' });
  const btn = page.getByRole('button', { name: 'Request change' });
  if (await btn.count()) {
    await btn.click();
    await page.getByRole('button', { name: 'Send request' }).click();
    await page.getByText('Request sent').waitFor({ timeout: 10_000 });
    await page.screenshot({ path: path.join(OUT, 'request-pending-desktop.png'), fullPage: true });
    await page.getByRole('button', { name: 'Undo' }).first().click();
    await page.getByText('Request sent').waitFor({ state: 'detached', timeout: 10_000 });
  } else {
    console.log(`skip request flow: ${PERSONAS[0]} has no counsellor`);
  }
  await ctx.close();

  await browser.close();
  if (!visited) failures.push('no routes visited');
  if (failures.length) { console.error(failures.join('\n')); process.exit(1); }
  console.log(`ok: ${visited} page visits, no errors`);
}

main().catch((e) => { console.error(e); process.exit(1); });
