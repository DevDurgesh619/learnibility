import { Check } from 'lucide-react';
import { cn } from '@/lib/utils';
import { STEPS } from './draft';

/** "1 About you — 2 What you need — 3 Your profile — 4 Starting test" from PDF 1e-1g. */
export function Stepper({ current }: { current: number }) {
  return (
    <ol className="mb-8 flex items-center gap-2 text-xs" aria-label="Onboarding steps">
      {STEPS.map((s, i) => {
        const done = i < current;
        const active = i === current;
        return (
          <li key={s.href} className="flex flex-1 items-center gap-2" aria-current={active ? 'step' : undefined}>
            <span
              className={cn(
                'flex size-6 shrink-0 items-center justify-center rounded-full text-[11px] font-semibold',
                done ? 'bg-brand-600 text-white' : active ? 'bg-ink text-white' : 'bg-surface-muted text-subtle',
              )}
            >
              {done ? <Check className="size-3.5" /> : i + 1}
            </span>
            <span className={cn('hidden whitespace-nowrap sm:inline', active ? 'font-medium text-ink' : 'text-muted')}>{s.label}</span>
            {i < STEPS.length - 1 && <span className={cn('h-px flex-1', done ? 'bg-brand-600' : 'bg-line')} />}
          </li>
        );
      })}
    </ol>
  );
}
