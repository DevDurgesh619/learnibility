/**
 * W2-S1 smoke test (student onboarding and assessments). Plain Playwright, no runner needed:
 *   BASE_URL=http://localhost:3000 node scripts/smoke/w2-s1.spec.ts
 *
 * 1. Zoya signs up (landing → mobile → OTP with an error first → role → about → needs → profile → starting test
 *    with the demo shortcuts → setting up) and lands on /student.
 * 2. Kabir takes his current chapter check, submits, and sees result → gap analysis → topic detail; the result
 *    must say his week was re-planned.
 * 3. Every route this thread owns is visited at 1440 and 390 px; console errors, HTTP errors and horizontal
 *    overflow fail the run. Screenshots go to docs/screens/w2-s1/.
 */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { chromium } = require('playwright') as { chromium: any };
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Page = any;

const BASE = process.env.BASE_URL ?? 'http://localhost:3000';
const OUT = path.join(process.cwd(), 'docs', 'screens', 'w2-s1');
const SIZES = [{ name: 'desktop', width: 1440, height: 900 }, { name: 'mobile', width: 390, height: 844 }];
const failures: string[] = [];

function watch(page: Page, label: string) {
  const errors: string[] = [];
  page.on('console', (m: { type(): string; text(): string }) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', (e: Error) => errors.push(String(e)));
  return () => { if (errors.length) failures.push(`${label}: console errors\n  ${errors.join('\n  ')}`); };
}

async function snap(page: Page, name: string, size: string) {
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  if (overflow > 1) failures.push(`${name} ${size}: horizontal overflow ${overflow}px`);
  await page.screenshot({ path: path.join(OUT, `${name}-${size}.png`), fullPage: true });
}

async function signUpZoya(browser: Page) {
  const size = SIZES[0];
  const ctx = await browser.newContext({ viewport: { width: size.width, height: size.height } });
  const page = await ctx.newPage();
  const done = watch(page, 'zoya sign-up');
  await page.goto(`${BASE}/welcome`); await snap(page, '1a-landing', size.name);
  await page.getByRole('link', { name: /Get started/ }).first().click(); await page.waitForURL(/\/signup$/);
  await page.getByText('new student (Zoya)').click(); await snap(page, '1b-mobile', size.name);
  await page.getByRole('button', { name: 'Send OTP' }).click(); await page.waitForURL(/verify/);
  await page.locator('input[aria-label="Digit 1"]').fill('111111');
  await page.getByRole('button', { name: 'Verify' }).click(); await page.getByText("That code didn't match").waitFor();
  await snap(page, '1c-otp-error', size.name);
  await page.getByRole('button', { name: 'Fill' }).click(); await page.getByRole('button', { name: 'Verify' }).click();
  await page.waitForURL(/role/); await snap(page, '1d-role', size.name);
  await page.getByRole('button', { name: 'Continue as Student' }).click(); await page.waitForURL(/about/);
  await page.getByRole('button', { name: /Demo details/ }).click(); await snap(page, '1e-about', size.name);
  await page.getByRole('button', { name: 'Continue' }).click(); await page.waitForURL(/needs/); await snap(page, '1f-needs', size.name);
  await page.getByRole('button', { name: 'Continue' }).click(); await page.waitForURL(/profile/); await snap(page, '1g-profile', size.name);
  await page.getByRole('button', { name: 'Save and continue' }).click(); await page.waitForURL(/onboarding\/test/);
  await snap(page, 'onb-test-parts', size.name);
  for (let i = 0; i < 8; i++) {
    const start = page.getByRole('button', { name: 'Start' }).first();
    if (!(await start.count())) break;
    await start.click();
    if (i === 0) await snap(page, 'onb-test-adaptive', size.name);
    if (i === 4) await snap(page, 'onb-test-reasoning', size.name);
    if (i === 5) await snap(page, 'onb-test-about', size.name);
    await page.getByRole('button', { name: /for me \(demo\)/ }).click();
    await page.waitForTimeout(300);
  }
  await page.getByRole('button', { name: 'See my results and plan' }).click();
  await page.waitForURL(/setup/); await snap(page, '1i-setup', size.name);
  await page.waitForURL(/\/student$/, { timeout: 30_000 });
  await snap(page, 'zoya-home-after-onboarding', size.name);
  done();
  await ctx.close();
}

async function kabirChapterCheck(browser: Page) {
  const size = SIZES[0];
  const ctx = await browser.newContext({ viewport: { width: size.width, height: size.height } });
  await ctx.addCookies([{ name: 'learnibility_persona', value: 'lrn_kabir_singh', url: BASE }]);
  const page = await ctx.newPage();
  const done = watch(page, 'kabir chapter check');
  await page.goto(`${BASE}/student/assessments`);
  // His class is on the chapter marked "In class now"; fall back to any chapter check.
  const current = page.locator('tr:has-text("In class now")').getByRole('link', { name: /^(Chapter check|Check again)$/ });
  const check = (await current.count()) ? current.first() : page.getByRole('link', { name: /^(Chapter check|Check again)$/ }).first();
  if (!(await check.count())) { failures.push('kabir: no chapter check offered'); await ctx.close(); return; }
  await check.click(); await page.waitForURL(/chk\./);
  await page.getByRole('link', { name: /Continue/ }).click(); await page.waitForURL(/instructions/);
  await page.getByRole('checkbox').check();
  await page.getByRole('link', { name: 'Start test now' }).click(); await page.waitForURL(/take/);
  await page.getByText(/Question 1 of/).first().waitFor();
  const total = Number((await page.getByText(/Question 1 of \d+/).first().innerText()).match(/of (\d+)/)?.[1] ?? 0);
  for (let i = 0; i < total; i++) {
    const radio = page.locator('[role=radiogroup] [role=radio]');
    if (await radio.count()) await radio.nth(i % 4 === 3 ? 1 : 0).click();
    else await page.locator('textarea, input[inputmode=decimal]').first().fill(i % 3 ? 'I am not sure' : '12');
    await page.locator('fieldset button').nth(3).click();
    if (i === 1) await page.getByRole('button', { name: /^Flag/ }).click();
    if (i === 2) await snap(page, '8d-test-in-progress', size.name);
    if (i < total - 1) await page.getByRole('button', { name: /^(Next|Save & next)$/ }).click();
  }
  await page.getByRole('button', { name: 'Finish' }).click();
  await snap(page, '8e-submit-check', size.name);
  await page.getByRole('alertdialog').getByRole('button', { name: 'Submit' }).click();
  await page.waitForURL(/results\/[^/]+$/, { timeout: 30_000 });
  if (!(await page.getByText('Your week has been re-planned').count())) failures.push('kabir: result does not show a re-planned week');
  done();
  await ctx.close();
  return page.url().replace(BASE, '');
}

async function visitAll(browser: Page, persona: string, resultPath: string | undefined) {
  for (const size of SIZES) {
    const ctx = await browser.newContext({ viewport: { width: size.width, height: size.height } });
    await ctx.addCookies([{ name: 'learnibility_persona', value: persona, url: BASE }]);
    const page = await ctx.newPage();
    const done = watch(page, `${persona} ${size.name}`);
    const who = persona.replace(/^lrn_/, '').split('_')[0];
    const routes: [string, string][] = [['/student/assessments', '8a-assessments']];
    await page.goto(`${BASE}/student/assessments`);
    const chk = await page.getByRole('link', { name: /^(Chapter check|Check again)$/ }).first().getAttribute('href').catch(() => null);
    if (chk) routes.push([chk, '8b-overview'], [`${chk}/instructions`, '8c-instructions']);
    if (resultPath) {
      routes.push([resultPath, '8f-result'], [`${resultPath}/gaps`, '8g-gap-analysis']);
    }
    for (const [r, name] of routes) {
      const res = await page.goto(`${BASE}${r}`, { waitUntil: 'networkidle' });
      if (!res || res.status() >= 400) failures.push(`${persona} ${r} ${size.name}: HTTP ${res?.status()}`);
      await snap(page, `${who}-${name}`, size.name);
    }
    if (resultPath) {
      const topic = page.locator('tbody a').first();
      if (await topic.count()) {
        await topic.click(); await page.waitForURL(/topics/);
        await snap(page, `${who}-8h-topic-detail`, size.name);
      }
    }
    if (size.name === 'mobile') {
      for (const [r, name] of [['/welcome', '1a-landing'], ['/signup', '1b-mobile'], ['/signup/verify?phone=9876543210', '1c-otp'], ['/signup/role', '1d-role']] as const) {
        await page.goto(`${BASE}${r}`, { waitUntil: 'networkidle' });
        await snap(page, name, size.name);
      }
    }
    done();
    await ctx.close();
  }
}

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  await signUpZoya(browser);
  const kabirResult = await kabirChapterCheck(browser);
  await visitAll(browser, 'lrn_kabir_singh', kabirResult);
  await visitAll(browser, 'lrn_zoya_fernandes', undefined);
  await browser.close();
  if (failures.length) { console.error(failures.join('\n')); process.exit(1); }
  console.log(`W2-S1 smoke OK, screenshots in ${path.relative(process.cwd(), OUT)}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
