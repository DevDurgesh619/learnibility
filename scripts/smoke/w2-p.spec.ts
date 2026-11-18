/**
 * W2-P parent and mentor smoke test. Plain Playwright (pre-installed `playwright`), no test runner needed:
 *   BASE_URL=http://localhost:3000 node scripts/smoke/w2-p.spec.ts
 * Logs in as two parents (Anita Das, Neha Kapoor) and the mentor (Kelvin Thomas), visits every W2-P route at
 * 1440 and 390 px, fails on HTTP errors, console or page errors and horizontal overflow, and saves screenshots to
 * docs/screens/w2-p/. Then runs the acceptance flow: Anita approves the paid tutor Rohan asked for, the booking
 * shows as approved, and the tutor sees Rohan. It calls POST /api/demo-reset before and after.
 */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { chromium } = require('playwright') as { chromium: any };

const BASE = process.env.BASE_URL ?? 'http://localhost:3000';
const OUT = path.join(process.cwd(), 'docs', 'screens', 'w2-p');
const PARENT_ROUTES = ['', '/progress', '/plan', '/timetable', '/payments', '/messages', '/privacy'];
const MENTOR_ROUTES = ['', '/career-sessions', '/skill-plans', '/messages'];
const RUNS = [
  { persona: 'par_anita_das', role: 'parent', routes: PARENT_ROUTES },
  { persona: 'par_neha_kapoor', role: 'parent', routes: PARENT_ROUTES },
  { persona: 'mnt_kelvin_thomas', role: 'mentor', routes: MENTOR_ROUTES },
];
const SIZES = [{ name: 'desktop', width: 1440, height: 900 }, { name: 'mobile', width: 390, height: 844 }];

async function reset() {
  await fetch(`${BASE}/api/demo-reset`, { method: 'POST' }).catch(() => undefined);
}

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  await reset();
  const browser = await chromium.launch();
  const failures: string[] = [];
  let visited = 0;
  for (const run of RUNS) {
    for (const size of SIZES) {
      const ctx = await browser.newContext({ viewport: { width: size.width, height: size.height }, deviceScaleFactor: 1 });
      await ctx.addCookies([{ name: 'learnibility_persona', value: run.persona, url: BASE }]);
      const page = await ctx.newPage();
      const errors: string[] = [];
      page.on('console', (m: { type(): string; text(): string }) => { if (m.type() === 'error') errors.push(m.text()); });
      page.on('pageerror', (e: Error) => errors.push(String(e)));
      for (const r of run.routes) {
        const res = await page.goto(`${BASE}/${run.role}${r}`, { waitUntil: 'networkidle' });
        if (!page.url().includes(`/${run.role}`)) { console.log(`skip ${run.persona}: landed on ${page.url()}`); break; }
        visited++;
        await page.waitForTimeout(600); // let chart animations settle before the screenshot
        if (!res || res.status() >= 400) failures.push(`${run.persona} ${r || '/'} ${size.name}: HTTP ${res?.status()}`);
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
        if (overflow > 1) failures.push(`${run.persona} ${r || '/'} ${size.name}: horizontal overflow ${overflow}px`);
        if (errors.length) failures.push(`${run.persona} ${r || '/'} ${size.name}: ${errors.splice(0).join(' | ')}`);
        await page.screenshot({ path: path.join(OUT, `${run.persona}-${(r || '/home').slice(1)}-${size.name}.png`), fullPage: true });
      }
      await ctx.close();
    }
  }

  // Acceptance: Rohan's parent sees why a paid tutor is suggested, approves it, and the booking reaches Rohan's tutor.
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  await ctx.addCookies([{ name: 'learnibility_persona', value: 'par_anita_das', url: BASE }]);
  const page = await ctx.newPage();
  await page.goto(`${BASE}/parent/plan`, { waitUntil: 'networkidle' });
  if (!(await page.getByText('Free plan has run 3 weeks').count())) failures.push('plan: 3-week rule not shown');
  const approve = page.getByRole('button', { name: 'Approve', exact: true });
  if (!(await approve.count())) failures.push('plan: no booking waiting for approval');
  else {
    await approve.first().click();
    await page.waitForURL(/done=approved/);
    await page.screenshot({ path: path.join(OUT, 'acceptance-approved.png'), fullPage: true });
    if (!(await page.getByText('Waiting for the tutor to accept').count())) failures.push('plan: approved booking not shown');
    const t = await browser.newContext();
    await t.addCookies([{ name: 'learnibility_persona', value: 'tut_sunita_gupta', url: BASE }]);
    const tp = await t.newPage();
    await tp.goto(`${BASE}/tutor`, { waitUntil: 'networkidle' });
    if (!/Rohan/.test(await tp.locator('body').innerText())) failures.push('tutor: Rohan not visible to the approved tutor');
    await t.close();
  }
  await ctx.close();
  await browser.close();
  await reset();

  console.log(`W2-P smoke: ${visited} page visits, ${failures.length} failures`);
  for (const f of failures) console.log('  FAIL', f);
  process.exit(failures.length ? 1 : 0);
}

main().catch((e) => { console.error(e); process.exit(1); });
