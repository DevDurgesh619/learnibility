/**
 * W2-A application support smoke test. Plain Playwright (pre-installed `playwright`), no test runner needed:
 *   BASE_URL=http://localhost:3000 node scripts/smoke/w2-a.spec.ts          routes only
 *   BASE_URL=http://localhost:3000 FLOW=1 node scripts/smoke/w2-a.spec.ts   routes, then the acceptance flow
 * Routes: logs in as Nikhil (paid), Ananya (free), Farah (counsellor) and two parents, visits every W2-A route
 * at 1440 and 390 px, fails on HTTP errors, console errors and horizontal overflow, saves screenshots to
 * docs/screens/w2-a/.
 * Flow (writes to the demo overlay, then resets it): Ananya sees fit results and the upgrade prompt; Farah
 * comments on Nikhil's personal statement; Nikhil replies, revises and resolves; Farah approves it as final and
 * marks the reference received; Nikhil ticks the last items, passes the QA check and submits Leeds.
 */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { chromium } = require('playwright') as { chromium: any };

const BASE = process.env.BASE_URL ?? 'http://localhost:3000';
const OUT = path.join(process.cwd(), 'docs', 'screens', 'w2-a');
const SIZES = [{ name: 'desktop', width: 1440, height: 900 }, { name: 'mobile', width: 390, height: 844 }];

const ROUTES: Record<string, string[]> = {
  lrn_nikhil_reddy: [
    '/student/applications', '/student/applications/universities', '/student/applications/universities?view=recommended',
    '/student/applications/universities?view=milestones', '/student/applications/board', '/student/applications/app_nikhil_leeds',
    '/student/applications/essays', '/student/applications/essays/ess_nikhil_ucas_ps', '/student/applications/finance',
    '/student/applications/meetings', '/student/universities/uni-uk-leeds',
  ],
  lrn_ananya_kapoor: [
    '/student/universities', '/student/universities?q=computer%20science', '/student/universities/uni-us-yale',
    '/student/universities/uni-us-yale?tab=admissions', '/student/universities/uni-us-yale?tab=costs', '/student/universities/best-fit',
    '/student/universities/best-fit/profile', '/student/universities/best-fit/results?again=1', '/student/applications/upgrade',
  ],
  csl_farah_siddiqui: [
    '/counsellor/applications', '/counsellor/applications?student=lrn_nikhil_reddy', '/counsellor/applications/app_nikhil_leeds',
    '/counsellor/draft-reviews', '/counsellor/draft-reviews/ess_nikhil_ucas_ps',
  ],
  csl_heena_qureshi: ['/counsellor/applications', '/counsellor/draft-reviews'],
  par_lakshmi_reddy: ['/parent/applications'],
  par_neha_kapoor: ['/parent/applications', '/parent/applications?child=lrn_ananya_kapoor'],
};

type Page = any; // eslint-disable-line @typescript-eslint/no-explicit-any

async function login(browser: any, persona: string, width = 1440, height = 900) { // eslint-disable-line @typescript-eslint/no-explicit-any
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: 1 });
  await ctx.addCookies([{ name: 'learnibility_persona', value: persona, url: BASE }]);
  const page: Page = await ctx.newPage();
  const errors: string[] = [];
  page.on('console', (m: { type(): string; text(): string }) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', (e: Error) => errors.push(String(e)));
  return { ctx, page, errors };
}

async function routes(browser: any, failures: string[]) { // eslint-disable-line @typescript-eslint/no-explicit-any
  let visited = 0;
  for (const [persona, list] of Object.entries(ROUTES)) {
    for (const size of SIZES) {
      const { ctx, page, errors } = await login(browser, persona, size.width, size.height);
      for (const r of list) {
        const res = await page.goto(`${BASE}${r}`, { waitUntil: 'networkidle' });
        await page.waitForTimeout(r.includes('results') ? 2500 : 200);
        visited++;
        if (!res || res.status() >= 400) failures.push(`${persona} ${r} ${size.name}: HTTP ${res?.status()}`);
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
        if (overflow > 1) failures.push(`${persona} ${r} ${size.name}: horizontal overflow ${overflow}px`);
        const slug = r.replace(/^\/(student|counsellor|parent)\//, '').replace(/[^a-z0-9]+/gi, '-').replace(/-$/, '') || 'home';
        await page.screenshot({ path: path.join(OUT, `${persona.split('_')[1]}-${slug}-${size.name}.png`), fullPage: true });
      }
      if (errors.length) failures.push(`${persona} ${size.name}: console errors\n  ${errors.join('\n  ')}`);
      await ctx.close();
    }
  }
  return visited;
}

async function flow(browser: any, failures: string[]) { // eslint-disable-line @typescript-eslint/no-explicit-any
  const step = (s: string) => console.log(`  flow: ${s}`);
  const expect = async (page: Page, text: string | RegExp, what: string) => {
    try { await page.getByText(text).first().waitFor({ timeout: 15000 }); } catch { failures.push(`flow: ${what} (missing "${text}")`); throw new Error(what); }
  };
  await fetch(`${BASE}/api/demo-reset`, { method: 'POST' }).catch(() => undefined);

  // Ananya: free fit results and the upgrade prompt.
  {
    const { ctx, page } = await login(browser, 'lrn_ananya_kapoor');
    await page.goto(`${BASE}/student/universities/best-fit/results`);
    await expect(page, 'Calculating your fit', 'calculating state');
    await expect(page, 'Turn this into applications.', 'upgrade prompt on fit results');
    await expect(page, /^Reach \d+$/, 'reach group');
    step('Ananya sees Reach, Target and Safe and the upgrade prompt');
    await ctx.close();
  }

  // Farah comments on Nikhil's personal statement.
  {
    const { ctx, page } = await login(browser, 'csl_farah_siddiqui');
    await page.goto(`${BASE}/counsellor/draft-reviews/ess_nikhil_ucas_ps`);
    const mark = page.locator('div.whitespace-pre-wrap').first();
    await mark.waitFor();
    await page.evaluate(() => {
      const box = document.querySelector('div.whitespace-pre-wrap')!;
      const walker = document.createTreeWalker(box, NodeFilter.SHOW_TEXT);
      let n: Node | null;
      while ((n = walker.nextNode())) {
        const i = (n.textContent ?? '').indexOf('Outside the classroom');
        if (i >= 0) {
          const r = document.createRange();
          r.setStart(n, i);
          r.setEnd(n, i + 'Outside the classroom I was treasurer of our commerce club'.length);
          const s = window.getSelection()!;
          s.removeAllRanges();
          s.addRange(r);
          box.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
          return;
        }
      }
    });
    await page.getByPlaceholder('Suggestion for Nikhil').fill('Good. Say what the audited accounts showed in one clause.');
    await page.getByRole('button', { name: 'Comment' }).click();
    await expect(page, 'Say what the audited accounts showed', 'counsellor comment saved');
    step('Farah adds an anchored comment');
    await ctx.close();
  }

  // Nikhil replies, revises (v3) and resolves Farah's comments, then sends it back.
  {
    const { ctx, page } = await login(browser, 'lrn_nikhil_reddy');
    await page.goto(`${BASE}/student/applications/essays/ess_nikhil_ucas_ps`);
    await expect(page, 'Say what the audited accounts showed', 'student sees the comment');
    await page.getByPlaceholder('Reply…').first().fill('Done in v3, thanks.');
    await page.getByRole('button', { name: 'Reply', exact: true }).first().click();
    await expect(page, 'Done in v3, thanks.', 'student reply saved');
    await page.getByRole('button', { name: 'Edit' }).click();
    const ta = page.getByLabel('Essay text');
    const text: string = await ta.inputValue();
    await ta.fill(text
      .replace(', a line my teacher repeats and I now repeat to my friends', '')
      .replace('presenting audited accounts to the principal', 'presenting audited accounts to the principal that showed a surplus for the first time in three years')
      .replace('I am drawn to a degree that is accredited by professional bodies and that teaches financial reporting alongside data analysis', 'I want a degree accredited by professional bodies, with modules in financial data analytics, so I can build better versions of that receivables schedule'));
    await page.getByRole('button', { name: 'Save' }).click();
    await expect(page, 'v3 · current', 'v3 saved');
    // Comments stay on v2; resolve them there.
    await page.getByRole('button', { name: /^v2 / }).click();
    for (let i = 0; i < 4; i++) {
      const btn = page.getByRole('button', { name: 'Resolve' }).first();
      if (!(await btn.count())) break;
      await btn.click();
      await page.waitForTimeout(800);
    }
    step('Nikhil replies, saves v3 and resolves the comments');
    await ctx.close();
  }

  // Farah approves as final and marks the reference received.
  {
    const { ctx, page } = await login(browser, 'csl_farah_siddiqui');
    await page.goto(`${BASE}/counsellor/draft-reviews/ess_nikhil_ucas_ps`);
    await page.getByRole('button', { name: 'Approve as final' }).click();
    await expect(page, 'Approved as final.', 'essay approved');
    await page.goto(`${BASE}/counsellor/applications/app_nikhil_leeds`);
    await page.getByRole('button', { name: 'Mark received' }).click();
    await expect(page, 'Received', 'reference received');
    step('Farah approves the statement and marks the reference received');
    await ctx.close();
  }

  // Nikhil ticks the remaining items, passes QA and submits.
  {
    const { ctx, page } = await login(browser, 'lrn_nikhil_reddy');
    await page.goto(`${BASE}/student/applications/app_nikhil_leeds`);
    for (const title of ['UCAS form: education, employment and choices completed', 'UCAS application fee (£28.95)']) {
      await page.getByRole('button', { name: `Tick ${title}` }).click();
      await page.waitForTimeout(800);
    }
    await expect(page, 'Everything checks out.', 'QA passes');
    await page.getByRole('button', { name: 'Mark as submitted' }).click();
    await page.waitForTimeout(1500);
    await page.goto(`${BASE}/student/applications/board`);
    const col = page.locator('section[aria-label="Submitted"]');
    if (!(await col.getByText('Leeds').count())) failures.push('flow: Leeds is not in the Submitted column');
    await page.screenshot({ path: path.join(OUT, 'flow-nikhil-board-after-submit.png'), fullPage: true });
    step('Nikhil submits Leeds; it moves to Submitted');
    await ctx.close();
  }
  await fetch(`${BASE}/api/demo-reset`, { method: 'POST' }).catch(() => undefined);
}

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const failures: string[] = [];
  const visited = process.env.ROUTES === '0' ? 0 : await routes(browser, failures);
  if (process.env.FLOW) await flow(browser, failures).catch((e) => failures.push(`flow stopped: ${e.message}`));
  await browser.close();
  if (failures.length) { console.error(failures.join('\n')); process.exit(1); }
  console.log(`W2-A smoke: ${visited} page views OK${process.env.FLOW ? ', acceptance flow OK' : ''}, screenshots in ${path.relative(process.cwd(), OUT)}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
