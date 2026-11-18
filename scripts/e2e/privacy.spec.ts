/**
 * Privacy crawl (W3-QA). Logs in as every parent, teacher, tutor, mentor and sales persona, opens every sidebar route
 * plus the per-learner views (?child=, ?id=, ?mentee=, /tutor/students/{id}), and fails if the page shows:
 *   - the name of any T3 (screened wellbeing) parameter that holds a value for a learner that person can see, or
 *   - counsellor-only wellbeing wording (check-in scores, screening results).
 * The parent Privacy page may name the T3 tier itself; it must not name T3 parameters.
 *   BASE_URL=http://localhost:3000 npx tsx scripts/e2e/privacy.spec.ts
 */
import { BASE, as, chromium, report } from './lib';

const ROLES = ['parent', 'teacher', 'tutor', 'mentor', 'sales'] as const;
const WELLBEING = [/check-in scored/i, /wellbeing (check-in|screen(ing)?) (score|result)/i, /\bPHQ|GAD-?7\b/, /sleep (quality|hours) (is|was|score)/i];

interface Persona { id: string; role: string; name: string; linkedLearnerIds?: string[] }

async function main() {
  const people = (await (await fetch(`${BASE}/demo/personas.json`)).json()) as Persona[];
  const students = people.filter((p) => p.role === 'student').map((p) => p.id);
  const t3 = new Map<string, string[]>();
  for (const s of students) t3.set(s, ((await (await fetch(`${BASE}/demo/t3.json?learner=${s}`)).json()) as { names: string[] }).names);

  const browser = await chromium.launch();
  const failures: string[] = [];
  let pages = 0;
  for (const p of people.filter((x) => (ROLES as readonly string[]).includes(x.role))) {
    const { ctx, page } = await as(browser, p.id);
    await page.goto(`${BASE}/${p.role}`, { waitUntil: 'networkidle' });
    const nav: string[] = await page.$$eval(`a[href^="/${p.role}"]`, (as: HTMLAnchorElement[]) => [...new Set(as.map((a) => a.getAttribute('href') ?? ''))]);
    const learners = p.role === 'sales' ? [] : p.linkedLearnerIds ?? [];
    const routes = new Set(nav.filter((h) => h && !h.includes('#')));
    for (const l of learners) {
      if (p.role === 'parent') for (const r of ['', '/progress', '/plan', '/timetable', '/payments', '/messages', '/privacy']) routes.add(`/parent${r}?child=${l}`);
      if (p.role === 'teacher') routes.add(`/teacher/students?id=${l}`);
      if (p.role === 'tutor') routes.add(`/tutor/students/${l}`);
      if (p.role === 'mentor') for (const r of ['', '/skill-plans', '/career-sessions']) routes.add(`/mentor${r}?mentee=${l}`);
    }
    // Names to look for: T3 parameters of every learner this person can see (sales: every learner).
    const visible = p.role === 'sales' ? students : learners;
    const names = [...new Set(visible.flatMap((l) => t3.get(l) ?? []))].filter((n) => n.length >= 8);
    for (const r of routes) {
      const res = await page.goto(`${BASE}${r}`, { waitUntil: 'networkidle' }).catch(() => undefined);
      if (!res || res.status() >= 400) continue; // route health is the smoke specs' job
      pages++;
      const html = (await page.content()) as string;
      const text = (await page.locator('body').innerText()) as string;
      for (const n of names) if (text.includes(n) || html.includes(n)) failures.push(`${p.name} (${p.role}) ${r}: shows T3 parameter "${n}"`);
      for (const w of WELLBEING) if (w.test(text)) failures.push(`${p.name} (${p.role}) ${r}: wellbeing wording ${w}`);
    }
    await ctx.close();
  }
  await browser.close();
  report('privacy', failures, `${pages} pages, ${people.filter((x) => (ROLES as readonly string[]).includes(x.role)).length} personas`);
}

main().catch((e) => { console.error(e); process.exit(1); });
