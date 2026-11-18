import { NextResponse } from 'next/server';
import { resetDemo } from '@/lib/actions/core';
import { SESSION_COOKIE } from '@/lib/session';
import { resolvePersona } from '@/components/demo/resolve';
import { DEMO_COOKIE, findScenario, hrefForStep, personaForStep } from '@/components/demo/scenarios';

/**
 * Demo navigation. GET /demo/go?scenario=kabir&step=2 logs in as that step's persona, remembers the
 * scenario and step for the Demo guide panel, and opens the step's route.
 * POST (the "Start" button on /demo) does the same for step 0 after resetting every demo write.
 */
function go(req: Request, scenarioId: string | null, stepParam: string | null) {
  const scenario = findScenario(scenarioId);
  if (!scenario) return NextResponse.redirect(new URL('/demo', req.url), 303);
  const step = Math.max(0, Math.min(scenario.steps.length - 1, Number(stepParam) || 0));
  const persona = resolvePersona(personaForStep(scenario, step));
  if (!persona) return NextResponse.redirect(new URL(`/demo?missing=${scenario.id}`, req.url), 303);
  const res = NextResponse.redirect(new URL(hrefForStep(scenario, step), req.url), 303);
  const opts = { path: '/', sameSite: 'lax' as const, maxAge: 60 * 60 * 24 };
  res.cookies.set(SESSION_COOKIE, persona.id, { ...opts, httpOnly: true, maxAge: 60 * 60 * 24 * 30 });
  res.cookies.set(DEMO_COOKIE, `${scenario.id}:${step}`, opts);
  return res;
}

export async function GET(req: Request) {
  const url = new URL(req.url);
  return go(req, url.searchParams.get('scenario'), url.searchParams.get('step'));
}

export async function POST(req: Request) {
  const form = await req.formData();
  resetDemo();
  return go(req, String(form.get('scenario') ?? ''), '0');
}
