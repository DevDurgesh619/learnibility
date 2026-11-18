import { cookies } from 'next/headers';
import { DEMO_COOKIE, parseDemoCookie } from './scenarios';
import { refLabel } from './resolve';
import { DemoGuidePanel } from './demo-guide-panel';

/** Root-layout hook: shows the Demo guide panel while a scenario from /demo is running. */
export async function DemoGuide() {
  const jar = await cookies();
  const current = parseDemoCookie(jar.get(DEMO_COOKIE)?.value);
  if (!current) return null;
  const { scenario, step } = current;
  return (
    <DemoGuidePanel
      scenarioId={scenario.id}
      n={scenario.n}
      title={scenario.title}
      step={step}
      steps={scenario.steps.map((s) => ({ title: s.title, detail: s.detail, as: s.as ? refLabel(s.as) : undefined }))}
      startAs={refLabel(scenario.start.as)}
      pointOut={scenario.pointOut}
    />
  );
}
