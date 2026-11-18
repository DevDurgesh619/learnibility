import Link from 'next/link';
import { ChevronRight } from 'lucide-react';
import { Delta, Pill, SectionTitle } from '@/components/tutor/bits';
import { scoreSeries, studentContext, topicCards } from '@/components/tutor/model';
import { formatDay } from '@/components/marketplace/dates';
import { Card } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import { getSubject } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import { cn } from '@/lib/utils';

const STATE = { strong: ['Strong', 'border-success-600/30 bg-success-50'], medium: ['Medium', 'border-warning-600/30 bg-warning-50'], weak: ['Weak', 'border-danger-600/30 bg-danger-50'], not_started: ['Not started', 'border-line bg-surface'] } as const;

/** 4b topic mastery + 4c assessments and assignments with gap analysis links. */
export default async function Learning({ params, searchParams }: { params: Promise<{ learnerId: string }>; searchParams: Promise<{ subject?: string; src?: string }> }) {
  const { learnerId } = await params;
  const sp = await searchParams;
  const { ws, row } = studentContext((await currentPersona())!.id, learnerId)!;
  const subjectId = sp.subject && row.subjectIds.includes(sp.subject) ? sp.subject : row.subjectIds[0];
  const cards = subjectId ? topicCards(learnerId, subjectId) : [];
  const series = scoreSeries(ws, learnerId).filter((s) => !s.subjectId || s.subjectId === subjectId);
  const src = sp.src === 'platform' || sp.src === 'assignment' ? sp.src : 'all';
  const list = series.map((s, i) => ({ ...s, delta: i > 0 ? s.pct - series[i - 1]!.pct : null })).filter((s) => src === 'all' || s.source === src).reverse();
  const base = `/tutor/students/${learnerId}/learning`;
  return (
    <div className="space-y-8">
      <section>
        <SectionTitle action={row.subjectIds.length > 1 ? <div className="flex gap-1">{row.subjectIds.map((s) => <Link key={s} href={`${base}?subject=${s}`} className="text-sm text-brand-700">{getSubject(s)?.subject.name}</Link>)}</div> : undefined}>
          Topics · {subjectId ? getSubject(subjectId)?.subject.name : '—'} <span className="text-sm font-normal text-muted">· from platform tests, assignments and sessions</span>
        </SectionTitle>
        {cards.length === 0 ? <EmptyState title="No topics yet" description="Topic mastery appears after the first test in your subject." /> : (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {cards.map((c) => (
              <div key={c.chapterId} className={cn('rounded-[var(--radius-card)] border p-3', STATE[c.state][1])}>
                <p className="line-clamp-2 text-sm font-medium text-ink" title={c.name}>{c.name}</p>
                <p className="mt-1 text-sm text-muted">{STATE[c.state][0]}{c.pct !== null ? ` · ${c.pct}%` : ''}</p>
                {c.delta !== null && <Delta value={c.delta} />}
              </div>
            ))}
          </div>
        )}
      </section>
      <section>
        <SectionTitle>Assessments and assignments · {series.length}</SectionTitle>
        <div className="mb-3 flex gap-2">
          {(['all', 'platform', 'assignment'] as const).map((k) => (
            <Link key={k} href={`${base}?${new URLSearchParams({ ...(subjectId ? { subject: subjectId } : {}), ...(k === 'all' ? {} : { src: k }) })}`}
              className={cn('rounded-full border px-3 py-1 text-sm', src === k ? 'border-brand-600 bg-brand-600 text-white' : 'border-line bg-surface hover:bg-surface-muted')}>
              {{ all: 'All', platform: 'Platform tests', assignment: 'My assignments' }[k]}
            </Link>
          ))}
        </div>
        {list.length === 0 ? <EmptyState title="Nothing scored yet" /> : (
          <Card>
            <ul className="divide-y divide-line">
              {list.map((s) => (
                <li key={s.id}>
                  <Link href={`${base}/${s.id}`} className="flex items-center gap-3 px-4 py-3 hover:bg-surface-muted/60">
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-sm font-medium text-ink">{s.title}</p>
                      <p className="text-xs text-muted">{formatDay(s.date)} · <Pill tone={s.source === 'platform' ? 'brand' : 'neutral'}>{s.source === 'platform' ? 'Platform test' : 'Your assignment'}</Pill></p>
                    </div>
                    <span className="w-12 text-right text-sm font-medium text-ink">{s.pct}%</span>
                    <span className="w-14 text-right">{s.delta === null ? <span className="text-xs text-muted">baseline</span> : <Delta value={s.delta} />}</span>
                    <span className="hidden text-xs text-brand-700 sm:inline">Gap analysis</span>
                    <ChevronRight className="size-4 text-subtle" />
                  </Link>
                </li>
              ))}
            </ul>
          </Card>
        )}
        <p className="mt-3 text-xs text-muted">Platform tests and your assignments feed the same topic mastery. Re-assessment on the platform shows whether teaching moved the needle.</p>
      </section>
    </div>
  );
}
