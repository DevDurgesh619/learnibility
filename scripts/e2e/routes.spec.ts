/**
 * Route health (W3-QA). For every persona on the picker: every sidebar link at 1440 and 390 px must return 200,
 * stay in the persona's area, show no "This screen is on its way" placeholder, log no console or page errors and
 * not overflow horizontally. Reports the slowest pages; fails any page slower than MAX_MS (default 2000) to load.
 *   BASE_URL=http://localhost:3000 [MAX_MS=2000] npx tsx scripts/e2e/routes.spec.ts
 */
import { BASE, SIZES, as, chromium, report } from './lib';

const MAX_MS = Number(process.env.MAX_MS ?? 2000);

async function main() {
  const people = (await (await fetch(`${BASE}/demo/personas.json`)).json()) as { id: string; role: string; name: string }[];
  const browser = await chromium.launch();
  const failures: string[] = [];
  const timings: { ms: number; where: string }[] = [];
  const seenRole = new Set<string>();
  for (const p of people) {
    for (const size of SIZES) {
      const { ctx, page, errors } = await as(browser, p.id, size);
      await page.goto(`${BASE}/${p.role}`, { waitUntil: 'networkidle' });
      const nav: string[] = await page.$$eval(`a[href^="/${p.role}"]`, (as: HTMLAnchorElement[]) =>
        [...new Set(as.map((a) => a.getAttribute('href') ?? '').filter((h) => h && !h.includes('#')))]);
      for (const r of nav) {
        const where = `${p.name} (${p.role}) ${r} ${size.name}`;
        const t = Date.now();
        const res = await page.goto(`${BASE}${r}`, { waitUntil: 'load' }).catch((e: Error) => { failures.push(`${where}: ${e.message.split('\n')[0]}`); return undefined; });
        const ms = Date.now() - t;
        await page.waitForLoadState('networkidle').catch(() => undefined);
        if (!res) continue;
        if (size.name === 'desktop') timings.push({ ms, where: `${p.role} ${r}` });
        if (res.status() >= 400) failures.push(`${where}: HTTP ${res.status()}`);
        const path = new URL(page.url()).pathname;
        if (!path.startsWith(`/${p.role}`)) failures.push(`${where}: landed on ${path}`);
        if (await page.getByText('This screen is on its way').count()) failures.push(`${where}: placeholder page`);
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
        if (overflow > 1) failures.push(`${where}: horizontal overflow ${overflow}px`);
        if (errors.length) failures.push(`${where}: ${errors.splice(0).join(' | ').slice(0, 300)}`);
        if (ms > MAX_MS && !seenRole.has(`${p.role}${r}`)) failures.push(`${where}: ${ms} ms to load (limit ${MAX_MS})`);
        seenRole.add(`${p.role}${r}`);
      }
      await ctx.close();
    }
  }
  await browser.close();
  timings.sort((a, b) => b.ms - a.ms);
  console.log('slowest pages (desktop):');
  for (const t of timings.slice(0, 8)) console.log(`  ${t.ms} ms  ${t.where}`);
  report('routes', failures, `${people.length} personas, ${timings.length * 2} page loads`);
}

main().catch((e) => { console.error(e); process.exit(1); });
