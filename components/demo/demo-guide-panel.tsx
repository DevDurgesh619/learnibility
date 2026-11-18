'use client';

import { useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';
import { ChevronDown, ChevronUp, Lightbulb, ListChecks, X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Props {
  scenarioId: string;
  n: number;
  title: string;
  step: number;
  steps: { title: string; detail?: string; as?: string }[];
  startAs: string;
  pointOut: string[];
}

const goHref = (id: string, step: number) => `/demo/go?scenario=${encodeURIComponent(id)}&step=${step}`;

/**
 * Floating "Demo guide": the running scenario's numbered steps, the current one highlighted, with Go links
 * that switch persona and route. Collapses to a pill; the X ends the scenario. Hidden on /demo itself.
 */
export function DemoGuidePanel({ scenarioId, n, title, step, steps, startAs, pointOut }: Props) {
  const pathname = usePathname();
  const [open, setOpen] = useState(true);
  useEffect(() => {
    const saved = window.sessionStorage.getItem('demo-guide-open');
    // Phones start collapsed so the guide never hides the screen being shown.
    setOpen(saved ? saved === '1' : window.innerWidth >= 640);
  }, []);
  const toggle = () => {
    window.sessionStorage.setItem('demo-guide-open', open ? '0' : '1');
    setOpen(!open);
  };
  if (pathname === '/demo') return null;
  const last = steps.length - 1;

  return (
    <div
      data-testid="demo-guide"
      className="fixed bottom-3 right-3 z-50 w-[min(360px,calc(100vw-24px))] print:hidden"
      role="complementary"
      aria-label="Demo guide"
    >
      <div className="overflow-hidden rounded-xl border border-brand-200 bg-surface shadow-lg">
        <div className="flex items-center gap-2 bg-brand-700 px-3 py-2 text-white">
          <ListChecks className="size-4 shrink-0" />
          <button type="button" onClick={toggle} className="min-w-0 flex-1 text-left" aria-expanded={open}>
            <p className="truncate text-sm font-medium">Demo {n}: {title}</p>
            <p className="text-xs text-brand-100">Step {step + 1} of {steps.length}</p>
          </button>
          <button type="button" onClick={toggle} className="rounded p-1 hover:bg-brand-600" aria-label={open ? 'Collapse demo guide' : 'Expand demo guide'}>
            {open ? <ChevronDown className="size-4" /> : <ChevronUp className="size-4" />}
          </button>
          <form action="/demo/exit" method="post">
            <button className="rounded p-1 hover:bg-brand-600" aria-label="Close demo guide" title="End this scenario">
              <X className="size-4" />
            </button>
          </form>
        </div>
        {open && (
          <div className="max-h-[55vh] overflow-y-auto p-3">
            <ol className="flex flex-col gap-1">
              {steps.map((s, i) => (
                <li key={i}>
                  <a
                    href={goHref(scenarioId, i)}
                    className={cn(
                      'flex gap-2 rounded-lg px-2 py-1.5 text-sm',
                      i === step ? 'bg-brand-50 ring-1 ring-brand-200' : 'hover:bg-surface-muted',
                      i < step && 'text-muted',
                    )}
                    aria-current={i === step ? 'step' : undefined}
                  >
                    <span className={cn('mt-0.5 flex size-5 shrink-0 items-center justify-center rounded-full text-xs font-semibold', i === step ? 'bg-brand-600 text-white' : 'bg-surface-muted text-muted')}>
                      {i + 1}
                    </span>
                    <span className="min-w-0">
                      <span className="font-medium text-ink">{s.title}</span>
                      {s.as && <span className="ml-1 text-xs text-subtle">as {s.as}</span>}
                      {i === step && s.detail && <span className="mt-0.5 block text-xs text-muted">{s.detail}</span>}
                    </span>
                  </a>
                </li>
              ))}
            </ol>
            {step === last && pointOut.length > 0 && (
              <div className="mt-3 rounded-lg bg-surface-muted p-2 text-xs text-muted">
                <p className="mb-1 flex items-center gap-1 font-medium text-ink"><Lightbulb className="size-3.5" /> Point out</p>
                <ul className="list-disc pl-4">{pointOut.map((p) => <li key={p}>{p}</li>)}</ul>
              </div>
            )}
            <div className="mt-3 flex items-center gap-2 text-xs">
              <a href="/demo" className="text-brand-600 hover:underline">All scenarios</a>
              <span className="text-subtle">· started as {startAs}</span>
              <span className="ml-auto flex gap-1">
                {step > 0 && <a href={goHref(scenarioId, step - 1)} className="rounded-md border border-line px-2 py-1 hover:bg-surface-muted">Back</a>}
                {step < last && <a href={goHref(scenarioId, step + 1)} className="rounded-md bg-brand-600 px-2 py-1 font-medium text-white hover:bg-brand-700">Next step</a>}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
