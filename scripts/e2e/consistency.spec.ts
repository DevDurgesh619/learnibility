/**
 * Cross-role consistency (W3-QA). For 5 students, the same gaps, hours, learning rate, band, timetable and spend must
 * read identically on the student, parent, teacher, counsellor and tutor screens. The expected values come from
 * GET /demo/facts.json?learner=… (the data layer, formatted the way screens format them).
 *   BASE_URL=http://localhost:3000 npx tsx scripts/e2e/consistency.spec.ts
 * LEARNERS=lrn_a,lrn_b overrides the student list.
 */
import { BASE, as, chromium, report, resetDemo } from './lib';

const LEARNERS = (process.env.LEARNERS ?? 'lrn_kabir_singh,lrn_rohan_das,lrn_ishita_rao,lrn_sara_khan,lrn_vihaan_joshi').split(',');
const FALLBACK = ['lrn_nikhil_reddy', 'lrn_ananya_kapoor'];

interface Facts {
  id: string; name: string; firstName: string; bandLabel: string; lrs: string | null; openGaps: number; hoursToClose: string;
  gaps: { name: string; code: string; hours: string }[]; timetableTitles: string[];
  spend: { paid: string; due: string; invoices: number };
  viewers: { parents: string[]; teachers: string[]; teacherSections: { teacherId: string; sectionId: string }[]; tutors: string[]; counsellors: string[] };
}

const esc = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const squash = (s: string) => s.replace(/\s+/g, ' ');

async function facts(id: string): Promise<Facts | undefined> {
  const res = await fetch(`${BASE}/demo/facts.json?learner=${id}`);
  return res.ok ? ((await res.json()) as Facts) : undefined;
}

async function main() {
  await resetDemo();
  const browser = await chromium.launch();
  const failures: string[] = [];
  let checks = 0;
  const learners: Facts[] = [];
  for (const id of [...LEARNERS, ...FALLBACK]) {
    if (learners.length >= 5) break;
    const f = await facts(id);
    if (f) learners.push(f);
  }
  if (learners.length < 5) failures.push(`only ${learners.length} of 5 learners exist`);

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  async function read(persona: string, route: string): Promise<string | undefined> {
    const { ctx, page, errors } = await as(browser, persona);
    const res = await page.goto(`${BASE}${route}`, { waitUntil: 'networkidle' });
    const body = squash(await page.locator('main').innerText().catch(() => ''));
    const landed = new URL(page.url()).pathname;
    await ctx.close();
    if (!res || res.status() >= 400) { failures.push(`${persona} ${route}: HTTP ${res?.status()}`); return undefined; }
    if (landed === '/login') { failures.push(`${persona} ${route}: sent to /login`); return undefined; }
    if (errors.length) failures.push(`${persona} ${route}: console ${errors.join(' | ')}`);
    return body;
  }
  function has(where: string, body: string | undefined, what: string, pattern: RegExp) {
    if (body === undefined) return;
    checks++;
    if (!pattern.test(body)) failures.push(`${where}: expected ${what}`);
  }

  for (const f of learners) {
    const who = f.firstName;
    const gapCount = new RegExp(`Open gaps ${f.openGaps}\\b`);

    // Student: timetable titles.
    const st = await read(f.id, '/student/timetable');
    for (const t of f.timetableTitles.slice(0, 6)) has(`${who} student timetable`, st, `block "${t}"`, new RegExp(esc(squash(t))));

    // Parent: home numbers, plan gaps, timetable, spend.
    for (const parent of f.viewers.parents) {
      const home = await read(parent, `/parent?child=${f.id}`);
      has(`${who} parent home`, home, `open gaps ${f.openGaps}`, gapCount);
      has(`${who} parent home`, home, `hours to close ${f.hoursToClose}`, new RegExp(`Hours to close ${esc(f.hoursToClose)}`));
      if (f.lrs) has(`${who} parent home`, home, `LRS ${f.lrs}`, new RegExp(`\\(LRS\\) ${esc(f.lrs)}`));
      const plan = await read(parent, `/parent/plan?child=${f.id}`);
      has(`${who} parent plan`, plan, `open gaps ${f.openGaps}`, gapCount);
      for (const g of f.gaps) has(`${who} parent plan`, plan, `gap "${g.name}" (${g.hours})`, new RegExp(esc(squash(g.name))));
      const tt = await read(parent, `/parent/timetable?child=${f.id}`);
      for (const t of f.timetableTitles.slice(0, 6)) has(`${who} parent timetable`, tt, `block "${t}"`, new RegExp(esc(squash(t))));
      if (f.spend.invoices) {
        const pay = await read(parent, `/parent/payments?child=${f.id}`);
        has(`${who} parent payments`, pay, `paid total ${f.spend.paid}`, new RegExp(esc(f.spend.paid)));
      }
    }

    // Counsellor: caseload row and Student 360.
    for (const csl of f.viewers.counsellors.slice(0, 1)) {
      const s360 = await read(csl, `/counsellor/student-360?student=${f.id}`);
      has(`${who} counsellor 360`, s360, `name`, new RegExp(esc(f.name)));
      has(`${who} counsellor 360`, s360, `open gaps ${f.openGaps}`, gapCount);
      if (f.lrs) has(`${who} counsellor 360`, s360, `LRS ${f.lrs}`, new RegExp(`\\(LRS\\) ${esc(f.lrs)}`));
      const { ctx, page } = await as(browser, csl);
      await page.goto(`${BASE}/counsellor`, { waitUntil: 'networkidle' });
      const row = page.locator('tr', { hasText: f.name });
      const rowText = (await row.count()) ? squash(await row.first().innerText()) : undefined;
      await ctx.close();
      if (rowText === undefined) failures.push(`${who} counsellor caseload: no row`);
      else {
        has(`${who} counsellor caseload`, rowText, `band ${f.bandLabel}`, new RegExp(esc(f.bandLabel)));
        has(`${who} counsellor caseload`, rowText, `${f.openGaps} open gaps`, new RegExp(`\\b${f.openGaps}\\b`));
      }
    }

    // Teacher: student detail (T1 only).
    for (const { teacherId: tch, sectionId } of f.viewers.teacherSections.slice(0, 1)) {
      const t = await read(tch, `/teacher/students?section=${sectionId}&id=${f.id}`);
      has(`${who} teacher`, t, `open gaps ${f.openGaps}`, gapCount);
      has(`${who} teacher`, t, `${f.hoursToClose} to close`, new RegExp(`${esc(f.hoursToClose)} to close`));
      if (f.lrs) has(`${who} teacher`, t, `LRS ${f.lrs}`, new RegExp(`\\(LRS\\) ${esc(f.lrs)}`));
      for (const g of f.gaps) has(`${who} teacher`, t, `gap "${g.name}"`, new RegExp(esc(squash(g.name))));
    }

    // Tutor: the student workspace shows the same gaps (the tutor may show only their subject; need at least one).
    for (const tut of f.viewers.tutors.slice(0, 1)) {
      const t = await read(tut, `/tutor/students/${f.id}`);
      if (t !== undefined && f.gaps.length) {
        checks++;
        if (!f.gaps.some((g) => t.includes(squash(g.name)))) failures.push(`${who} tutor ${tut}: none of the ${f.gaps.length} open gaps shown`);
      }
    }
  }

  await browser.close();
  report('consistency', failures, `${learners.map((l) => l.firstName).join(', ')}; ${checks} checks`);
}

main().catch((e) => { console.error(e); process.exit(1); });
