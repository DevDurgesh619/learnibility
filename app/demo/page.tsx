import type { Metadata } from 'next';
import Link from 'next/link';
import { cookies } from 'next/headers';
import { Play, RotateCcw, Users } from 'lucide-react';
import { Logo } from '@/components/shell/logo';
import { Badge } from '@/components/ui/badge';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardBody, CardFooter } from '@/components/ui/card';
import { DEMO_COOKIE, SCENARIOS, parseDemoCookie } from '@/components/demo/scenarios';
import { refLabel, resolvePersona } from '@/components/demo/resolve';
import { DEMO_NOW, DEMO_TIMEZONE } from '@/lib/demo-clock';

export const metadata: Metadata = { title: 'Guided demo · Learnibility' };

const demoDate = new Intl.DateTimeFormat('en-IN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', timeZone: DEMO_TIMEZONE }).format(DEMO_NOW);

/** /demo: the 12 guided scenarios. Start resets the demo, logs in as the scenario's persona and opens the Demo guide. */
export default async function DemoPage({ searchParams }: { searchParams: Promise<{ missing?: string; reset?: string }> }) {
  const { missing, reset } = await searchParams;
  const running = parseDemoCookie((await cookies()).get(DEMO_COOKIE)?.value);
  const missingScenario = SCENARIOS.find((s) => s.id === missing);

  return (
    <div className="min-h-screen bg-surface-muted">
      <header className="border-b border-line bg-surface">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center gap-3 px-4 py-4 sm:px-6">
          <Logo href="/demo" />
          <Badge tone="brand">Guided demo</Badge>
          <div className="ml-auto flex flex-wrap items-center gap-2">
            <Link href="/login" className={buttonVariants({ variant: 'secondary', size: 'sm' })}>
              <Users /> Log in as anyone
            </Link>
            <form action="/demo/reset" method="post">
              <button className={buttonVariants({ variant: 'secondary', size: 'sm' })} data-testid="demo-reset">
                <RotateCcw /> Reset demo
              </button>
            </form>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6">
        <h1 className="text-2xl font-semibold tracking-tight text-ink sm:text-3xl">Walk through Learnibility</h1>
        <p className="mt-2 max-w-3xl text-muted">
          Twelve short stories, each told from the screens of the people involved. Start a scenario to reset the demo data, log in as
          the right person and open a guide that follows you around the app. The demo date is fixed at {demoDate}, India time; all
          people and data are fictional.
        </p>

        {reset && <p className="mt-4 rounded-lg bg-success-50 px-3 py-2 text-sm text-success-700">Demo reset. Every test taken, booking and approval from earlier runs is cleared.</p>}
        {missingScenario && (
          <p className="mt-4 rounded-lg bg-warning-50 px-3 py-2 text-sm text-warning-700">
            &ldquo;{missingScenario.title}&rdquo; needs a persona that is not in this build yet. Try another scenario.
          </p>
        )}
        {running && (
          <p className="mt-4 rounded-lg bg-brand-50 px-3 py-2 text-sm text-brand-700">
            Running: Demo {running.scenario.n}, {running.scenario.title} (step {running.step + 1} of {running.scenario.steps.length}).{' '}
            <a className="font-medium underline" href={`/demo/go?scenario=${running.scenario.id}&step=${running.step}`}>Continue</a>
          </p>
        )}

        <div className="mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {SCENARIOS.map((s) => {
            const ready = Boolean(resolvePersona(s.start.as));
            return (
              <Card key={s.id} className="flex flex-col" data-testid={`scenario-${s.id}`}>
                <CardBody className="flex flex-1 flex-col gap-3">
                  <div className="flex items-start gap-3">
                    <span className="flex size-8 shrink-0 items-center justify-center rounded-full bg-brand-600 text-sm font-semibold text-white">{s.n}</span>
                    <div className="min-w-0">
                      <h2 className="font-semibold text-ink">{s.title}</h2>
                      <p className="mt-0.5 text-sm text-muted">{s.summary}</p>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {s.roles.map((r) => <Badge key={r}>{r}</Badge>)}
                  </div>
                  <p className="text-xs text-subtle">
                    Log in as <span className="font-medium text-ink">{refLabel(s.start.as)}</span>, start at <code className="text-ink">{s.start.href}</code>
                  </p>
                  <ol className="flex list-decimal flex-col gap-1 pl-5 text-sm text-ink">
                    {s.steps.map((st, i) => (
                      <li key={i}>
                        {st.title}
                        {st.as && <span className="text-xs text-subtle"> (as {refLabel(st.as)})</span>}
                      </li>
                    ))}
                  </ol>
                  <div className="mt-auto rounded-lg bg-surface-muted p-3 text-xs text-muted">
                    <p className="mb-1 font-medium text-ink">Point out</p>
                    <ul className="list-disc pl-4">{s.pointOut.map((p) => <li key={p}>{p}</li>)}</ul>
                  </div>
                </CardBody>
                <CardFooter>
                  <form action="/demo/go" method="post" className="w-full">
                    <input type="hidden" name="scenario" value={s.id} />
                    <button className={buttonVariants({ className: 'w-full' })} disabled={!ready} data-testid={`start-${s.id}`}>
                      <Play /> {ready ? 'Reset and start' : 'Persona not in this build yet'}
                    </button>
                  </form>
                </CardFooter>
              </Card>
            );
          })}
        </div>
      </main>
    </div>
  );
}
