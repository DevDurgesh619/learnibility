/**
 * W3-CRM smoke test. Plain Playwright (pre-installed `playwright`), no test runner needed:
 *   BASE_URL=http://localhost:3000 node scripts/smoke/w3-crm.spec.ts
 * 1. Visits every sales route (plus a lead page and an invoice) as Priya and Aman at 1440 and 390 px; fails on HTTP
 *    errors, console or page errors and horizontal page overflow; screenshots go to docs/screens/w3-crm/.
 * 2. Acceptance flow at both sizes (demo reset before each): Aman opens Zoya's lead, records the payment, converts to
 *    the platform, checks the dashboard revenue and won count went up, then "Open Zoya in platform" lands on onboarding.
 * Calls POST /api/demo-reset before and after.
 */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { chromium } = require('playwright') as { chromium: any };

const BASE = process.env.BASE_URL ?? 'http://localhost:3000';
const OUT = path.join(process.cwd(), 'docs', 'screens', 'w3-crm');
const ZOYA_LEAD = 'lead_0013';
const ROUTES = ['', '/leads', '/leads?status=all&q=Kapoor', `/leads/${ZOYA_LEAD}`, '/leads/lead_0003', '/pipeline', '/follow-ups', '/follow-ups?tab=overdue', '/payments', '/payments/pay_0003_1', '/conversions', '/settings'];
const RUNS = [{ persona: 'sal_priya_malhotra' }, { persona: 'sal_aman_gupta' }];
const SIZES = [{ name: 'desktop', width: 1440, height: 900 }, { name: 'mobile', width: 390, height: 844 }];

async function reset() {
  await fetch(`${BASE}/api/demo-reset`, { method: 'POST', redirect: 'manual' }).catch(() => undefined);
}
const slug = (r: string) => (r || '/dashboard').slice(1).replace(/[/?&=]+/g, '-');

// eslint-disable-next-line @typescript-eslint/no-explicit-any
async function stat(page: any, label: string): Promise<string> {
  return page.evaluate((l: string) => {
    const tile = [...document.querySelectorAll('span')].find((s) => s.textContent?.trim() === l)?.closest('div')?.parentElement;
    return tile?.querySelector('.text-2xl')?.textContent?.trim() ?? '';
  }, label);
}
const rupees = (s: string) => Number(s.replace(/[^\d]/g, ''));

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
      for (const r of ROUTES) {
        const res = await page.goto(`${BASE}/sales${r}`, { waitUntil: 'networkidle' });
        visited++;
        if (!page.url().includes('/sales')) { failures.push(`${run.persona} ${r}: landed on ${page.url()}`); continue; }
        await page.waitForTimeout(400);
        if (!res || res.status() >= 400) failures.push(`${run.persona} ${r || '/'} ${size.name}: HTTP ${res?.status()}`);
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
        if (overflow > 1) failures.push(`${run.persona} ${r || '/'} ${size.name}: horizontal overflow ${overflow}px`);
        if (errors.length) failures.push(`${run.persona} ${r || '/'} ${size.name}: ${errors.splice(0).join(' | ')}`);
        if (run.persona === 'sal_aman_gupta') await page.screenshot({ path: path.join(OUT, `${slug(r)}-${size.name}.png`), fullPage: true });
      }
      await ctx.close();
    }
  }

  // ---------------------------------------------------------------- acceptance flow
  for (const size of SIZES) {
    await reset();
    const ctx = await browser.newContext({ viewport: { width: size.width, height: size.height }, deviceScaleFactor: 1 });
    await ctx.addCookies([{ name: 'learnibility_persona', value: 'sal_aman_gupta', url: BASE }]);
    const page = await ctx.newPage();
    const errors: string[] = [];
    page.on('pageerror', (e: Error) => errors.push(String(e)));
    const fail = (m: string) => failures.push(`flow ${size.name}: ${m}`);
    try {
      await page.goto(`${BASE}/sales`, { waitUntil: 'networkidle' });
      const revBefore = rupees(await stat(page, 'Revenue this month'));
      const wonBefore = Number(await stat(page, 'Deals won this month'));

      await page.goto(`${BASE}/sales/leads?q=Zoya&status=all`, { waitUntil: 'networkidle' });
      await page.getByRole('link', { name: /Fernandes/ }).first().click();
      await page.waitForURL(`**/sales/leads/${ZOYA_LEAD}`);
      if (!(await page.getByText('Proposal sent').first().isVisible())) fail('Zoya lead is not at Proposal sent');

      await page.getByTestId('record-payment').getByRole('button', { name: /Record payment/ }).click();
      await page.getByTestId('convert').waitFor({ timeout: 15000 });
      await page.getByTestId('convert').getByRole('button', { name: /Convert to platform/ }).click();
      await page.getByTestId('converted').waitFor({ timeout: 15000 });
      const timeline = (await page.getByTestId('timeline').innerText()) as string;
      for (const t of ['Payment received', 'Converted to platform', 'Closed won']) if (!timeline.includes(t)) fail(`timeline is missing "${t}"`);
      await page.screenshot({ path: path.join(OUT, `flow-converted-${size.name}.png`), fullPage: true });

      await page.goto(`${BASE}/sales`, { waitUntil: 'networkidle' });
      const revAfter = rupees(await stat(page, 'Revenue this month'));
      const wonAfter = Number(await stat(page, 'Deals won this month'));
      if (revAfter - revBefore !== 22797) fail(`revenue moved ${revBefore} → ${revAfter}, expected +22,797`);
      if (wonAfter !== wonBefore + 1) fail(`won this month ${wonBefore} → ${wonAfter}`);

      await page.goto(`${BASE}/sales/conversions`, { waitUntil: 'networkidle' });
      await page.goto(`${BASE}/sales/leads/${ZOYA_LEAD}`, { waitUntil: 'networkidle' });
      await page.getByRole('button', { name: /Open Zoya in platform/ }).click();
      await page.waitForURL('**/onboarding/**', { timeout: 15000 });
      if (!page.url().includes('/onboarding/about')) fail(`Open in platform landed on ${page.url()}`);
      await page.screenshot({ path: path.join(OUT, `flow-onboarding-${size.name}.png`), fullPage: true });
    } catch (e) {
      fail(String(e));
      await page.screenshot({ path: path.join(OUT, `flow-error-${size.name}.png`), fullPage: true }).catch(() => undefined);
    }
    if (errors.length) fail(errors.join(' | '));
    await ctx.close();
  }

  await browser.close();
  await reset();
  console.log(`visited ${visited} pages, ${failures.length} failures`);
  for (const f of failures) console.log(' -', f);
  process.exit(failures.length ? 1 : 0);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
