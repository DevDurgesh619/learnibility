/**
 * Guided demo walk: for every scenario on /demo, "Reset and start", then open every step through the
 * Demo guide's links (the same /demo/go route a presenter clicks), at 1440 and 390 px. Fails on HTTP errors,
 * console or page errors, landing on /login (persona missing), a missing guide panel and horizontal overflow.
 * Scenarios whose start persona is not in the build are reported as skipped, not failed, unless STRICT=1.
 *   BASE_URL=http://localhost:3000 [STRICT=1] npx tsx scripts/e2e/demo.spec.ts
 */
import { SCENARIOS } from '../../components/demo/scenarios';
import { BASE, SIZES, chromium, report, resetDemo } from './lib';

async function main() {
  const browser = await chromium.launch();
  const failures: string[] = [];
  const skipped: string[] = [];
  let steps = 0;
  for (const size of SIZES) {
    for (const s of SCENARIOS) {
      const ctx = await browser.newContext({ viewport: { width: size.width, height: size.height }, deviceScaleFactor: 1 });
      const page = await ctx.newPage();
      const errors: string[] = [];
      page.on('console', (m: { type(): string; text(): string }) => { if (m.type() === 'error') errors.push(m.text()); });
      page.on('pageerror', (e: Error) => errors.push(String(e)));
      await page.goto(`${BASE}/demo`, { waitUntil: 'networkidle' });
      const start = page.getByTestId(`start-${s.id}`);
      if (await start.isDisabled()) {
        if (size.name === 'desktop') skipped.push(`${s.n} ${s.title}`);
        await ctx.close();
        continue;
      }
      await start.click();
      await page.waitForLoadState('networkidle');
      for (let i = 0; i < s.steps.length; i++) {
        const where = `[${size.name}] ${s.n}.${i + 1} ${s.steps[i].title}`;
        const res = await page.goto(`${BASE}/demo/go?scenario=${s.id}&step=${i}`, { waitUntil: 'networkidle' });
        steps++;
        const url = new URL(page.url());
        if (!res || res.status() >= 400) failures.push(`${where}: HTTP ${res?.status()} at ${url.pathname}`);
        if (url.pathname === '/login' || url.pathname === '/demo') failures.push(`${where}: landed on ${url.pathname}${url.search}`);
        if (!(await page.getByTestId('demo-guide').count())) failures.push(`${where}: Demo guide panel missing`);
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
        if (overflow > 1) failures.push(`${where}: horizontal overflow ${overflow}px at ${url.pathname}`);
        if (errors.length) failures.push(`${where}: ${errors.splice(0).join(' | ')}`);
      }
      await ctx.close();
    }
  }
  await browser.close();
  await resetDemo();
  if (skipped.length && process.env.STRICT) failures.push(...skipped.map((s) => `scenario not runnable: ${s}`));
  report('demo walk', failures, `${steps} steps${skipped.length ? `; skipped: ${skipped.join(', ')}` : ''}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
