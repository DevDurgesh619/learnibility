/**
 * Shared helpers for the W3-QA end-to-end specs. Plain Playwright (the pre-installed `playwright` package),
 * no test runner: each spec is `BASE_URL=http://localhost:3000 npx tsx scripts/e2e/<name>.spec.ts` and exits 1 on failure.
 */
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const { chromium } = require('playwright') as { chromium: any };

export const BASE = process.env.BASE_URL ?? 'http://localhost:3000';
export const SESSION_COOKIE = 'learnibility_persona';
export const SIZES = [
  { name: 'desktop', width: 1440, height: 900 },
  { name: 'mobile', width: 390, height: 844 },
] as const;

export async function resetDemo() {
  const res = await fetch(`${BASE}/api/demo-reset`, { method: 'POST' });
  if (!res.ok) throw new Error(`demo reset failed: HTTP ${res.status}`);
}

/** A browser context logged in as `personaId`, collecting console and page errors. */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export async function as(browser: any, personaId: string, size: { width: number; height: number } = SIZES[0]) {
  const ctx = await browser.newContext({ viewport: { width: size.width, height: size.height }, deviceScaleFactor: 1 });
  await ctx.addCookies([{ name: SESSION_COOKIE, value: personaId, url: BASE }]);
  const page = await ctx.newPage();
  const errors: string[] = [];
  page.on('console', (m: { type(): string; text(): string }) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', (e: Error) => errors.push(String(e)));
  return { ctx, page, errors };
}

export function report(name: string, failures: string[], extra = '') {
  if (failures.length) {
    console.error(`${name}: ${failures.length} failure(s)${extra ? ` (${extra})` : ''}`);
    for (const f of failures) console.error(`  - ${f}`);
    process.exit(1);
  }
  console.log(`${name}: pass${extra ? ` (${extra})` : ''}`);
}
