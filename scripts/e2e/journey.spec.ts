/**
 * Cross-role journey (W3-QA). One family's path through every role, asserting data at each hop, not just page loads:
 *   1. Sales (Aman Gupta) records Zoya's payment, converts her lead (lead_0013) and opens her in the platform → onboarding
 *   2. Zoya completes onboarding and the starting test                   → /student shows gaps and a plan
 *   3. Gaps and timetable appear                                          → timetable has study blocks
 *   4. Zoya books a tutor demo                                            → booking confirmation with tutor name
 *   5. The tutor accepts and files a session report with homework         → report saved
 *   6. Homework lands in Zoya's tasks                                     → task visible on /student/assessments
 *   7. Zoya's parent sees the booking and the spend                       → tutor name and ₹ amount on /parent/payments
 *   8. Heena sees Zoya in her caseload with her flags                     → Zoya row on /counsellor
 *   9. The sales dashboard counts the conversion                          → deals won +1, revenue up, Zoya on Conversions
 * Resets the demo first and last.  BASE_URL=http://localhost:3000 npx tsx scripts/e2e/journey.spec.ts
 * HOPS=2,3 runs only some hops (for debugging); later hops depend on earlier ones. KEEP=1 skips the final reset.
 */
import { BASE, as, chromium, report, resetDemo } from './lib';

const ZOYA = 'lrn_zoya_fernandes';
const ZOYA_LEAD = 'lead_0013';
const HOMEWORK = 'Journey check: practise sequence of tenses';
const P = {
  sales: 'sal_aman_gupta',
  counsellor: 'csl_heena_qureshi',
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Page = any;
interface Ctx { browser: Page; failures: string[]; facts: Record<string, string | number> }

const text = async (page: Page) => (await page.locator('main').innerText().catch(() => page.locator('body').innerText())) as string;
const num = (s: string | null | undefined) => Number(String(s ?? '').replace(/[^\d]/g, '')) || 0;
/** A StatTile's value by its label (same lookup as scripts/smoke/w3-crm.spec.ts). */
async function stat(page: Page, label: string): Promise<string> {
  return page.evaluate((l: string) => {
    const tile = [...document.querySelectorAll('span')].find((s) => s.textContent?.trim() === l)?.closest('div')?.parentElement;
    return tile?.querySelector('.text-2xl')?.textContent?.trim() ?? '';
  }, label);
}

async function hop(c: Ctx, n: number, name: string, fn: () => Promise<void>) {
  const only = process.env.HOPS?.split(',').map(Number);
  if (only && !only.includes(n)) return;
  const t = Date.now();
  try {
    await fn();
    console.log(`  hop ${n} ${name}: ok (${Date.now() - t} ms)`);
  } catch (e) {
    c.failures.push(`hop ${n} ${name}: ${(e as Error).message.split('\n')[0]}`);
    console.log(`  hop ${n} ${name}: FAILED`);
  }
}

function expect(cond: unknown, msg: string) {
  if (!cond) throw new Error(msg);
}

async function main() {
  await resetDemo();
  const browser = await chromium.launch();
  const c: Ctx = { browser, failures: [], facts: {} };

  await hop(c, 1, 'sales converts Zoya', async () => {
    const { ctx, page, errors } = await as(browser, P.sales);
    await page.goto(`${BASE}/sales`, { waitUntil: 'networkidle' });
    expect(new URL(page.url()).pathname === '/sales', `sales persona did not reach /sales (landed on ${page.url()})`);
    c.facts.revenueBefore = num(await stat(page, 'Revenue this month'));
    c.facts.wonBefore = num(await stat(page, 'Deals won this month'));
    await page.goto(`${BASE}/sales/leads/${ZOYA_LEAD}`, { waitUntil: 'networkidle' });
    expect(/Fernandes/.test(await text(page)), 'lead_0013 is not the Fernandes family');
    expect(await page.getByText('Proposal sent').first().isVisible(), "Zoya's lead is not at Proposal sent");
    await page.getByTestId('record-payment').getByRole('button', { name: /Record payment/ }).click();
    await page.getByTestId('convert').waitFor({ timeout: 15000 });
    await page.getByTestId('convert').getByRole('button', { name: /Convert to platform/ }).click();
    await page.getByTestId('converted').waitFor({ timeout: 15000 });
    expect(/payment received/i.test(await page.getByTestId('timeline').innerText()), 'timeline has no payment-received message');
    await page.getByRole('button', { name: /Open Zoya in platform/ }).click();
    await page.waitForURL(/\/onboarding\/about/, { timeout: 15000 });
    expect(!errors.length, errors.join(' | '));
    await ctx.close();
  });

  await hop(c, 2, 'Zoya onboarding and starting test', async () => {
    const { ctx, page, errors } = await as(browser, ZOYA);
    await page.goto(`${BASE}/onboarding/about`, { waitUntil: 'networkidle' });
    const demo = page.getByRole('button', { name: /Demo details/ });
    if (await demo.count()) await demo.click();
    await page.getByRole('button', { name: 'Continue' }).click(); await page.waitForURL(/needs/);
    await page.getByRole('button', { name: 'Continue' }).click(); await page.waitForURL(/profile/);
    await page.getByRole('button', { name: 'Save and continue' }).click(); await page.waitForURL(/onboarding\/test/);
    await page.getByRole('button', { name: 'Start' }).first().waitFor({ timeout: 30_000 });
    for (let i = 0; i < 8; i++) {
      const start = page.getByRole('button', { name: 'Start' }).first();
      if (!(await start.count())) break;
      await start.click();
      await page.getByRole('button', { name: /for me \(demo\)/ }).click();
      await page.waitForTimeout(300);
    }
    await page.getByRole('button', { name: 'See my results and plan' }).click();
    await page.waitForURL(/\/student$/, { timeout: 60_000 });
    await page.waitForLoadState('networkidle');
    const home = await text(page);
    expect(/gap/i.test(home), 'Zoya home shows no gaps after the starting test');
    expect(!/take (your|the) (starting|onboarding) test/i.test(home), 'Zoya home still asks for the starting test');
    expect(!errors.length, errors.join(' | '));
    await ctx.close();
  });

  await hop(c, 3, 'gaps and timetable appear', async () => {
    const { ctx, page } = await as(browser, ZOYA);
    await page.goto(`${BASE}/student/timetable`, { waitUntil: 'networkidle' });
    const tt = await text(page);
    expect(!/no timetable yet|take .* test first/i.test(tt), 'timetable is empty after onboarding');
    expect(/Maths|Science/i.test(tt), 'timetable has no subject blocks');
    await ctx.close();
  });

  await hop(c, 4, 'Zoya books a tutor demo', async () => {
    const { ctx, page, errors } = await as(browser, ZOYA);
    await page.goto(`${BASE}/student/tutors`, { waitUntil: 'networkidle' });
    const hrefs: string[] = await page.$$eval('main a[href^="/student/tutors/tut_"]', (as: HTMLAnchorElement[]) => as.map((a) => a.getAttribute('href') ?? ''));
    expect(hrefs.length, 'no recommended tutor for Zoya (are her onboarding gaps open?)');
    // Book a recommended tutor who can log in (a tutor persona); else Rahul Verma, the demo's lead tutor persona.
    const tutorPersonas = (await personas()).filter((p) => p.role === 'tutor').map((p) => p.id);
    c.facts.tutorId = hrefs.map((h) => h.split('/')[3]).find((id) => tutorPersonas.includes(id)) ?? 'tut_rahul_verma';
    await page.goto(`${BASE}/student/tutors/${c.facts.tutorId}/book`, { waitUntil: 'networkidle' });
    c.facts.tutorName = (await page.locator('main h1, main h2').first().innerText()).trim();
    c.facts.sharedGaps = /G\d (Prerequisite|Conceptual|Procedural|Careless|Language|Retention|Time|Over|Engagement)/.test(await text(page)) ? 1 : 0;
    await page.locator('main button[aria-pressed]').first().click();
    await page.getByRole('button', { name: /Confirm booking/ }).click();
    await page.waitForURL(/booked\//, { timeout: 30_000 });
    c.facts.bookingId = page.url().split('/booked/')[1]?.split(/[?#]/)[0] ?? '';
    expect(c.facts.bookingId, 'no booking id after confirming');
    expect(!errors.length, errors.join(' | '));
    await ctx.close();
  });

  await hop(c, 5, 'tutor accepts and files a report', async () => {
    const { ctx, page, errors } = await as(browser, String(c.facts.tutorId));
    await page.goto(`${BASE}/tutor`, { waitUntil: 'networkidle' });
    if (!/Zoya/.test(await text(page))) c.failures.push("hop 5: Zoya's new demo request is not on the tutor's Home (/tutor)");
    await page.goto(`${BASE}/tutor/requests/${c.facts.bookingId}`, { waitUntil: 'networkidle' });
    const req = await text(page);
    expect(/Zoya/.test(req), 'tutor request does not name Zoya');
    if (c.facts.sharedGaps) expect(/G\d/.test(req), 'Zoya shared her gap snapshot but the tutor request does not show it');
    await page.getByRole('button', { name: /^Accept/ }).first().click();
    await page.waitForURL(/\/tutor\/students\//, { timeout: 30_000 });
    await page.goto(`${BASE}/tutor/students/${ZOYA}/sessions`, { waitUntil: 'networkidle' });
    const sessionHref: string | undefined = await page.$$eval('main a[href^="/tutor/sessions/"]', (as: HTMLAnchorElement[]) => as[0]?.getAttribute('href') ?? undefined);
    expect(sessionHref, 'no session for Zoya after accepting');
    const sessionId = sessionHref!.split('/')[3];
    await page.goto(`${BASE}/tutor/sessions/${sessionId}/report`, { waitUntil: 'networkidle' });
    await page.locator('input[name="homework"]').first().fill(HOMEWORK);
    await page.locator('textarea[name="notes"]').fill('Demo went well; started on her first gaps.');
    await page.getByRole('button', { name: /Submit report|Update report/ }).click();
    await page.waitForLoadState('networkidle');
    expect(!errors.length, errors.join(' | '));
    await ctx.close();
  });

  await hop(c, 6, "homework in Zoya's tasks", async () => {
    const { ctx, page } = await as(browser, ZOYA);
    await page.goto(`${BASE}/student/assessments`, { waitUntil: 'networkidle' });
    let found = new RegExp(HOMEWORK).test(await text(page));
    if (!found) {
      await page.goto(`${BASE}/student`, { waitUntil: 'networkidle' });
      found = new RegExp(HOMEWORK).test(await text(page));
    }
    expect(found, `homework "${HOMEWORK}" is not in Zoya's tasks (Assessments or Home)`);
    await ctx.close();
  });

  await hop(c, 7, 'parent sees the booking and spend', async () => {
    const parent = await findParentOf(ZOYA);
    expect(parent, "no parent persona linked to Zoya");
    const p = await as(browser, parent!);
    await p.page.goto(`${BASE}/parent/payments`, { waitUntil: 'networkidle' });
    const t = await text(p.page);
    expect(t.includes(String(c.facts.tutorName).split(' ')[0]), `parent payments do not show ${c.facts.tutorName}`);
    expect(/₹\s?\d/.test(t), 'parent payments show no rupee amount');
    await p.ctx.close();
  });

  await hop(c, 8, "counsellor sees Zoya in the caseload", async () => {
    const { ctx, page } = await as(browser, P.counsellor);
    await page.goto(`${BASE}/counsellor`, { waitUntil: 'networkidle' });
    expect(/Zoya/.test(await text(page)), 'Zoya is not in the counsellor caseload');
    await ctx.close();
  });

  await hop(c, 9, 'sales dashboard shows the conversion', async () => {
    const { ctx, page } = await as(browser, P.sales);
    await page.goto(`${BASE}/sales`, { waitUntil: 'networkidle' });
    const won = num(await stat(page, 'Deals won this month'));
    const revenue = num(await stat(page, 'Revenue this month'));
    expect(won === Number(c.facts.wonBefore) + 1, `deals won this month ${c.facts.wonBefore} → ${won}, expected +1`);
    expect(revenue > Number(c.facts.revenueBefore), `revenue this month did not go up (${c.facts.revenueBefore} → ${revenue})`);
    await page.goto(`${BASE}/sales/conversions`, { waitUntil: 'networkidle' });
    expect(/Zoya/.test(await text(page)), 'Zoya is not on the Conversions page');
    await ctx.close();
  });

  await browser.close();
  if (!process.env.KEEP) await resetDemo();
  report('journey', c.failures);
}

async function personas() {
  const res = await fetch(`${BASE}/demo/personas.json`);
  return res.ok ? ((await res.json()) as { id: string; role: string; linkedLearnerIds?: string[] }[]) : [];
}

/** The parent account linked to a learner, from the persona picker list. */
async function findParentOf(learnerId: string): Promise<string | undefined> {
  const items = await personas();
  return items.find((p) => p.role === 'parent' && p.linkedLearnerIds?.includes(learnerId))?.id;
}

main().catch((e) => { console.error(e); process.exit(1); });
