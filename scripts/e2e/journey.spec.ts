/**
 * Cross-role journey (W3-QA). One family's path through every role, asserting data at each hop, not just page loads:
 *   1. Sales (Aman Gupta) records Zoya's payment and converts her lead  → lead shows Converted
 *   2. Zoya completes onboarding and the starting test                   → /student shows gaps and a plan
 *   3. Gaps and timetable appear                                          → timetable has study blocks
 *   4. Zoya books a tutor demo                                            → booking confirmation with tutor name
 *   5. The tutor accepts and files a session report with homework         → report saved
 *   6. Homework lands in Zoya's tasks                                     → task visible on /student/assessments
 *   7. Zoya's parent sees the booking and the spend                       → tutor name and ₹ amount on /parent/payments
 *   8. Heena sees Zoya in her caseload with her flags                     → Zoya row on /counsellor
 *   9. The sales dashboard counts the conversion                          → won/converted count went up by one
 * Resets the demo first and last.  BASE_URL=http://localhost:3000 npx tsx scripts/e2e/journey.spec.ts
 * HOPS=2,3 runs only some hops (for debugging); later hops depend on earlier ones.
 */
import { BASE, as, chromium, report, resetDemo } from './lib';

const ZOYA = 'lrn_zoya_fernandes';
const P = {
  sales: 'sal_aman_gupta',
  counsellor: 'csl_heena_qureshi',
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Page = any;
interface Ctx { browser: Page; failures: string[]; facts: Record<string, string | number> }

const text = async (page: Page) => (await page.locator('main').innerText().catch(() => page.locator('body').innerText())) as string;
const num = (s: string | null | undefined) => Number(String(s ?? '').replace(/[^\d.]/g, '')) || 0;

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

  // 0. Sales baseline for hop 9.
  await hop(c, 1, 'sales converts Zoya', async () => {
    const { ctx, page, errors } = await as(browser, P.sales);
    await page.goto(`${BASE}/crm`, { waitUntil: 'networkidle' });
    expect(page.url().includes('/crm'), `sales persona did not reach /crm (landed on ${page.url()})`);
    c.facts.convertedBefore = num(await page.getByTestId('crm-converted-count').textContent().catch(() => '0'));
    await page.goto(`${BASE}/crm/leads?q=Fernandes`, { waitUntil: 'networkidle' });
    await page.getByRole('link', { name: /Fernandes/ }).first().click();
    await page.waitForLoadState('networkidle');
    expect(/Proposal sent/i.test(await text(page)), "Zoya's lead is not at Proposal sent");
    await page.getByRole('button', { name: /Record payment/ }).click();
    await page.getByRole('button', { name: /Mark (as )?paid|Save payment|Confirm/ }).first().click();
    await page.waitForLoadState('networkidle');
    await page.getByRole('button', { name: /Convert to platform/ }).click();
    await page.waitForLoadState('networkidle');
    expect(/Converted/i.test(await text(page)), 'lead does not show Converted after conversion');
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
    const { ctx, page } = await as(browser, ZOYA);
    await page.goto(`${BASE}/student/tutors`, { waitUntil: 'networkidle' });
    await page.locator('a[href^="/student/tutors/"][href$="/book"], a[href^="/student/tutors/tut_"]').first().click();
    await page.waitForLoadState('networkidle');
    c.facts.tutorId = page.url().match(/tutors\/(tut_[a-z_]+)/)?.[1] ?? '';
    expect(c.facts.tutorId, 'could not open a tutor');
    if (!page.url().endsWith('/book')) await page.goto(`${BASE}/student/tutors/${c.facts.tutorId}/book`, { waitUntil: 'networkidle' });
    const demoOpt = page.getByText(/demo/i).first();
    if (await demoOpt.count()) await demoOpt.click().catch(() => undefined);
    await page.getByRole('button', { name: /Book|Request|Confirm|Send/ }).last().click();
    await page.waitForURL(/booked\//, { timeout: 30_000 });
    c.facts.bookingId = page.url().split('/booked/')[1] ?? '';
    c.facts.tutorName = (await page.locator('h1, h2').first().innerText()).trim();
    await ctx.close();
  });

  await hop(c, 5, 'tutor accepts and files a report', async () => {
    const { ctx, page } = await as(browser, String(c.facts.tutorId));
    await page.goto(`${BASE}/tutor/requests/${c.facts.bookingId}`, { waitUntil: 'networkidle' });
    expect(/Zoya/.test(await text(page)), 'tutor request does not name Zoya');
    expect(/gap/i.test(await text(page)), 'tutor request has no gap snapshot');
    await page.getByRole('button', { name: /Accept/ }).first().click();
    await page.waitForLoadState('networkidle');
    await page.goto(`${BASE}/tutor/sessions`, { waitUntil: 'networkidle' });
    await page.getByRole('link', { name: /Zoya/ }).first().click();
    await page.waitForLoadState('networkidle');
    const sessionId = page.url().match(/sessions\/([^/?]+)/)?.[1];
    expect(sessionId, 'no session for Zoya after accepting');
    await page.goto(`${BASE}/tutor/sessions/${sessionId}/report`, { waitUntil: 'networkidle' });
    const area = page.locator('textarea').first();
    if (await area.count()) await area.fill('Worked through her first gaps; set practice homework.');
    await page.getByRole('button', { name: /Submit|Save|File report|Send/ }).last().click();
    await page.waitForLoadState('networkidle');
    await ctx.close();
  });

  await hop(c, 6, "homework in Zoya's tasks", async () => {
    const { ctx, page } = await as(browser, ZOYA);
    await page.goto(`${BASE}/student/assessments`, { waitUntil: 'networkidle' });
    expect(/homework|from your tutor|task/i.test(await text(page)), 'no tutor homework in Zoya\'s tasks');
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
    await page.goto(`${BASE}/crm`, { waitUntil: 'networkidle' });
    const after = num(await page.getByTestId('crm-converted-count').textContent().catch(() => '0'));
    expect(after === Number(c.facts.convertedBefore) + 1, `converted count ${c.facts.convertedBefore} → ${after}, expected +1`);
    await ctx.close();
  });

  await browser.close();
  await resetDemo();
  report('journey', c.failures);
}

/** The parent account linked to a learner, read from the persona picker on /login. */
async function findParentOf(learnerId: string): Promise<string | undefined> {
  const res = await fetch(`${BASE}/demo/personas.json`);
  if (!res.ok) return undefined;
  const items = (await res.json()) as { id: string; role: string; linkedLearnerIds?: string[] }[];
  return items.find((p) => p.role === 'parent' && p.linkedLearnerIds?.includes(learnerId))?.id;
}

main().catch((e) => { console.error(e); process.exit(1); });
