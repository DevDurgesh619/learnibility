/**
 * Writes docs/demo-script.md from components/demo/scenarios.ts, so the printed script and the in-app
 * /demo page never drift. Run: npx tsx scripts/e2e/build-demo-script.ts
 */
import fs from 'node:fs';
import path from 'node:path';
import { SCENARIOS, type PersonaRef } from '../../components/demo/scenarios';

const who = (r: PersonaRef) => r.name ?? r.id ?? `parent of ${r.parentOf}`;

const out: string[] = [
  '# Learnibility demo script',
  '',
  '_Generated from `components/demo/scenarios.ts` by `npx tsx scripts/e2e/build-demo-script.ts`. Edit the scenarios file, not this one._',
  '',
  '## Before you start',
  '',
  '- Run the app (`npm run dev`) and open **http://localhost:3000/demo**.',
  '- Each scenario card has **Reset and start**: it clears every demo write (tests taken, bookings, approvals, conversions), logs you in as the right person and opens that scenario\'s first screen.',
  '- A **Demo guide** panel follows you around the app with the numbered steps. Each step\'s link switches to the right person and screen; **Next step** moves on. Close it with the X. On a phone it starts collapsed; tap its title to open it.',
  '- **Reset demo** at the top of `/demo` (or the circular-arrow icon in any app header) clears demo writes without starting a scenario.',
  '- The demo clock is fixed at Wednesday 18 November 2026, 9:00 AM India time. All people, schools, prices and data are fictional; prices are sample values.',
  '- `/login` lets you log in as anyone directly, outside a scenario.',
  '',
  '## Scenarios at a glance',
  '',
  '| # | Scenario | Log in as | Start at | Roles |',
  '| --- | --- | --- | --- | --- |',
  ...SCENARIOS.map((s) => `| ${s.n} | ${s.title} | ${who(s.start.as)} | \`${s.start.href}\` | ${s.roles.join(', ')} |`),
  '',
];

for (const s of SCENARIOS) {
  out.push(`## ${s.n}. ${s.title}`, '', s.summary, '', `**Log in as:** ${who(s.start.as)}  `, `**Start at:** \`${s.start.href}\``, '');
  s.steps.forEach((st, i) => {
    const bits = [`${i + 1}. **${st.title}**`];
    if (st.as) bits.push(`(switch to ${who(st.as)})`);
    if (st.href) bits.push(`at \`${st.href}\``);
    out.push(`${bits.join(' ')}${st.detail ? `. ${st.detail}` : ''}`);
  });
  out.push('', '**Point out**', '', ...s.pointOut.map((p) => `- ${p}`), '');
}

const file = path.join(process.cwd(), 'docs', 'demo-script.md');
fs.writeFileSync(file, out.join('\n'));
console.log(`wrote ${path.relative(process.cwd(), file)} (${SCENARIOS.length} scenarios)`);
