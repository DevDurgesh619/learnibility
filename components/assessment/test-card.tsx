import Link from 'next/link';
import { ArrowRight, CheckCircle2, Lock } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { buttonVariants } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import type { Attempt } from '@/lib/data';
import { resultHref, testHref, type AssessmentDef } from './catalog';

/** One test card on 8a: start, locked (paid) or completed with "See gap analysis" (PDF f.5 folded in). */
export function TestCard({ test, last, done = false, locked = false, highlight = false }: { test: AssessmentDef; last?: Attempt; done?: boolean; locked?: boolean; highlight?: boolean }) {
  const pct = last && last.maxScore ? Math.round((100 * last.score) / last.maxScore) : null;
  return (
    <div className={cn('flex h-full flex-col gap-3 rounded-xl border bg-surface p-4 shadow-[var(--shadow-card)]', highlight ? 'border-brand-300 ring-1 ring-brand-200' : 'border-line', locked && 'opacity-80')}>
      <div className="min-w-0">
        <div className="flex items-start justify-between gap-2">
          <p className="font-medium leading-snug text-ink">{test.title}</p>
          {locked && <Lock className="mt-0.5 size-4 shrink-0 text-subtle" aria-label="Paid" />}
        </div>
        <p className="mt-0.5 text-xs text-muted">
          {test.questions} Q · {test.minutes} min{test.questionTypes.length === 1 ? ` · ${test.questionTypes[0].toLowerCase()}` : ''}
        </p>
      </div>
      <div className="mt-auto flex flex-wrap items-center gap-2">
        {last ? (
          <>
            <Badge tone="success"><CheckCircle2 className="size-3" /> Completed{pct !== null ? ` · ${pct}%` : ''}</Badge>
            <Link href={`${resultHref(last.id)}/gaps`} className="text-xs font-medium text-brand-700 hover:underline">See gap analysis</Link>
            {!locked && <Link href={testHref(test.id)} className="ml-auto text-xs text-muted hover:text-ink">Retake</Link>}
          </>
        ) : done ? (
          <>
            <Badge tone="success"><CheckCircle2 className="size-3" /> Completed</Badge>
            <Link href={testHref(test.id)} className="ml-auto text-xs text-muted hover:text-ink">Retake</Link>
          </>
        ) : locked ? (
          <span className="text-xs text-subtle">In-depth set</span>
        ) : (
          <Link href={testHref(test.id)} className={buttonVariants({ size: 'sm', variant: highlight ? 'primary' : 'secondary' })}>
            Start <ArrowRight />
          </Link>
        )}
      </div>
    </div>
  );
}
