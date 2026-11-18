/**
 * W2-T tutor marketplace + tutor app smoke test. Plain Playwright (pre-installed `playwright`), no runner needed:
 *   BASE_URL=http://localhost:3000 node scripts/smoke/w2-t.spec.ts
 * Visits every W2-T route as a student (Ishita) and a tutor (Rahul Verma) at 1440 and 390 px, failing on HTTP
 * errors, console or page errors and horizontal overflow. Then runs the "done when" loop: Ishita books a free demo
 * with Rahul sharing her gap snapshot, Rahul accepts, files a session report with homework, and the homework shows
 * on Ishita's Today. The loop writes to the overlay; use LEARNIBILITY_OVERLAY=memory or reset the demo afterwards.
 * Screenshots go to docs/screens/w2-t/.
 */
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { chromium } = require('playwright') as { chromium: any };

const BASE = process.env.BASE_URL ?? 'http://localhost:3000';
const OUT = path.join(process.cwd(), 'docs', 'screens', 'w2-t');
const STUDENT = process.env.STUDENT ?? 'lrn_ishita_rao';
const TUTOR = process.env.TUTOR ?? 'tut_rahul_verma';
const LEARNER = 'lrn_tanvi_bhatia';
const STUDENT_ROUTES = ['/student/tutors', '/student/tutors?q=algebra&rating=4.5&format=one_to_one', `/student/tutors/${TUTOR}`, `/student/tutors/${TUTOR}/book`];
const TUTOR_ROUTES = [
  '/tutor', '/tutor/requests/bkg_w2t_req_sana', '/tutor/students', `/tutor/students/${LEARNER}`, `/tutor/students/${LEARNER}/learning`,
  `/tutor/students/${LEARNER}/sessions`, `/tutor/students/${LEARNER}/assignments`, `/tutor/students/${LEARNER}/assignments/asg_w2t_tanvi_hw3`,
  `/tutor/students/${LEARNER}/assignments/new`, `/tutor/students/${LEARNER}/tasks`, `/tutor/students/${LEARNER}/messages`, `/tutor/students/${LEARNER}/notes`,
  '/tutor/sessions', '/tutor/sessions?tab=requests', '/tutor/sessions?tab=past', '/tutor/sessions?view=calendar',
  '/tutor/sessions/ses_w2t_032', '/tutor/sessions/ses_w2t_032/prep', '/tutor/sessions/ses_w2t_032/live', '/tutor/sessions/ses_w2t_032/reschedule',
  '/tutor/sessions/ses_w2t_043/report', '/tutor/sessions/ses_w2t_015',
  '/tutor/today', '/tutor/today?day=2026-11-16', '/tutor/earnings', '/tutor/earnings/transactions', '/tutor/earnings/transactions?tab=payouts', '/tutor/earnings/settings',
  '/tutor/profile', '/tutor/profile/preferences', '/tutor/profile/availability', '/tutor/profile/pricing', '/tutor/profile/verification', '/tutor/onboarding',
];
const SIZES = [{ name: 'desktop', width: 1440, height: 900 }, { name: 'mobile', width: 390, height: 844 }];
const fileName = (who: string, r: string, size: string) => `${who}-${r.replace(/^\/(student|tutor)\/?/, '').replace(/[/?=&.]+/g, '-').replace(/^-|-$/g, '').slice(0, 70) || 'home'}-${size}.png`;

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const failures: string[] = [];
  let visited = 0;
  for (const [who, persona, routes] of [['student', STUDENT, STUDENT_ROUTES], ['tutor', TUTOR, TUTOR_ROUTES]] as const) {
    for (const size of SIZES) {
      const ctx = await browser.newContext({ viewport: { width: size.width, height: size.height }, deviceScaleFactor: 1 });
      await ctx.addCookies([{ name: 'learnibility_persona', value: persona, url: BASE }]);
      const page = await ctx.newPage();
      const errors: string[] = [];
      page.on('console', (m: { type(): string; text(): string }) => { if (m.type() === 'error') errors.push(m.text()); });
      page.on('pageerror', (e: Error) => errors.push(String(e)));
      for (const r of routes) {
        const res = await page.goto(`${BASE}${r}`, { waitUntil: 'networkidle' });
        visited++;
        if (!res || res.status() >= 400) failures.push(`${who} ${r} ${size.name}: HTTP ${res?.status()}`);
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
        if (overflow > 1) failures.push(`${who} ${r} ${size.name}: horizontal overflow ${overflow}px`);
        await page.screenshot({ path: path.join(OUT, fileName(who, r, size.name)), fullPage: true });
      }
      if (errors.length) failures.push(`${who} ${size.name}: console errors\n  ${errors.join('\n  ')}`);
      await ctx.close();
    }
  }

  // Done when: Ishita books Rahul → Rahul sees the request with her snapshot, accepts, files a report → homework on Ishita's Today.
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  const errors: string[] = [];
  page.on('pageerror', (e: Error) => errors.push(String(e)));
  const as = async (id: string) => { await ctx.clearCookies(); await ctx.addCookies([{ name: 'learnibility_persona', value: id, url: BASE }]); };
  try {
    await as(STUDENT);
    await page.goto(`${BASE}/student/tutors/${TUTOR}/book`, { waitUntil: 'networkidle' });
    if (await page.getByRole('button', { name: /Confirm booking/ }).count() === 0) throw new Error('booking form missing (already booked? reset the demo)');
    await page.locator('button[aria-pressed]').first().click();
    await page.getByRole('button', { name: /Confirm booking/ }).click();
    await page.waitForURL(/\/student\/tutors\/booked\//);
    const bookingId = page.url().split('/').pop()!;
    await page.screenshot({ path: path.join(OUT, 'flow-1-student-booked-desktop.png'), fullPage: true });

    await as(TUTOR);
    await page.goto(`${BASE}/tutor/requests/${bookingId}`, { waitUntil: 'networkidle' });
    if (!(await page.getByText('shared by', { exact: false }).count())) throw new Error('tutor request has no shared gap snapshot');
    await page.screenshot({ path: path.join(OUT, 'flow-2-tutor-request-desktop.png'), fullPage: true });
    await page.getByRole('button', { name: 'Accept demo' }).click();
    await page.waitForLoadState('networkidle');
    await page.goto(`${BASE}/tutor/sessions`, { waitUntil: 'networkidle' });
    const sid = await page.evaluate(() => [...document.querySelectorAll('a[href$="/prep"]')].find((a) => a.closest('li')?.textContent?.includes('Ishita'))?.getAttribute('href')?.split('/')[3]);
    if (!sid) throw new Error('accepted demo not in Sessions');
    await page.goto(`${BASE}/tutor/sessions/${sid}/live`, { waitUntil: 'networkidle' });
    await page.fill('#notes', 'Warmed up quickly; build on surds next time.');
    await page.getByRole('button', { name: 'End session' }).click();
    await page.waitForURL(/\/report/);
    await page.fill('input[name="dueDate"]', '2026-11-18');
    await page.getByRole('button', { name: /Submit report/ }).click();
    await page.waitForURL(/filed=1/);
    await page.screenshot({ path: path.join(OUT, 'flow-3-tutor-report-filed-desktop.png'), fullPage: true });

    await as(STUDENT);
    await page.goto(`${BASE}/student`, { waitUntil: 'networkidle' });
    if (!(await page.getByText('Practice set:', { exact: false }).count())) throw new Error("homework not on the student's Today");
    await page.screenshot({ path: path.join(OUT, 'flow-4-student-today-homework-desktop.png'), fullPage: true });
    console.log('flow ok: booked, snapshot shared, accepted, report filed, homework on Today');
  } catch (e) {
    failures.push(`flow: ${(e as Error).message}`);
  }
  if (errors.length) failures.push(`flow: page errors\n  ${errors.join('\n  ')}`);
  await ctx.close();

  await browser.close();
  if (!visited) failures.push('no routes visited');
  if (failures.length) { console.error(failures.join('\n')); process.exit(1); }
  console.log(`ok: ${visited} page visits, no errors`);
}

main().catch((e) => { console.error(e); process.exit(1); });
