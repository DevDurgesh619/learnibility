import Link from 'next/link';
import { ChevronLeft, ChevronRight, Eye } from 'lucide-react';
import { ChildSwitcher } from '@/components/parent/child-switcher';
import { param, parentContext, type SearchParams } from '@/components/parent/context';
import { fmtDate, fmtDay } from '@/components/parent/format';
import { NoChild } from '@/components/parent/no-child';
import { Badge, Card, CardBody, CardHeader, EmptyState, PageHeader, StatTile } from '@/components/ui';
import { buttonVariants } from '@/components/ui/button';
import { addDaysLocal, demoToday, getTimetable, weekStartOf } from '@/lib/data';
import type { TimetableBlock } from '@/lib/engines';
import { formatHours } from '@/lib/format';
import { cn } from '@/lib/utils';

const KIND: Record<TimetableBlock['kind'], { label: string; cls: string }> = {
  session: { label: 'Session', cls: 'border-l-brand-600 bg-brand-50' },
  locked: { label: 'Fixed', cls: 'border-l-line bg-surface-muted' },
  weekly_test: { label: 'Weekly test', cls: 'border-l-danger-600 bg-danger-50' },
  carry_over: { label: 'Carried over', cls: 'border-l-warning-600 bg-warning-50' },
  review: { label: 'Review', cls: 'border-l-info-600 bg-info-50' },
  gap: { label: 'Gap work', cls: 'border-l-warning-600 bg-warning-50' },
  chapter: { label: 'Chapter practice', cls: 'border-l-success-600 bg-success-50' },
  buffer: { label: 'Buffer', cls: 'border-l-line bg-surface' },
};

export default async function ParentTimetable({ searchParams }: { searchParams: SearchParams }) {
  const sp = await searchParams;
  const { children, child } = await parentContext(searchParams);
  if (!child) return (<><PageHeader eyebrow="Parent" title="Timetable" /><NoChild /></>);
  const s = child.student;
  const ws = weekStartOf(param(sp, 'week') ?? demoToday());
  const week = getTimetable(s.id, ws);
  const days = Array.from({ length: 7 }, (_, i) => addDaysLocal(ws, i));
  const blocks = (week?.blocks ?? []).filter((b) => b.kind !== 'buffer');
  const today = demoToday();
  const link = (w: string) => `/parent/timetable?${new URLSearchParams({ child: s.id, week: w })}`;
  const done = blocks.filter((b) => b.status === 'done').length;
  const missed = blocks.filter((b) => b.status === 'missed').length;

  return (
    <>
      <PageHeader eyebrow="Parent" title={`${s.firstName}'s timetable`} description="Re-planned automatically after every test and missed task. Read only."
        actions={<div className="flex items-center gap-2">
          <Link className={buttonVariants({ variant: 'secondary', size: 'sm' })} href={link(addDaysLocal(ws, -7))} aria-label="Previous week"><ChevronLeft /></Link>
          <span className="min-w-36 text-center text-sm font-medium text-ink">{fmtDate(ws)} – {fmtDate(addDaysLocal(ws, 6))}</span>
          <Link className={buttonVariants({ variant: 'secondary', size: 'sm' })} href={link(addDaysLocal(ws, 7))} aria-label="Next week"><ChevronRight /></Link>
        </div>} />
      <ChildSwitcher children={children} selectedId={s.id} basePath="/parent/timetable" extra={{ week: ws }} />

      {!week || !blocks.length ? (
        <EmptyState icon={<Eye />} title="Nothing planned this week" description={`${s.firstName}'s timetable is built from their study hours and open gaps. It shows here once there is a plan.`} />
      ) : (
        <>
          <section className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
            <StatTile label="Planned" value={formatHours(week.plannedMinutes / 60)} hint={`of ${formatHours(week.capacityMinutes / 60)} free time`} />
            <StatTile label="Blocks" value={blocks.length} />
            <StatTile label="Done" value={done} />
            <StatTile label="Missed" value={missed} hint={missed ? 'Carried over to later days' : undefined} />
          </section>
          <div className="grid gap-3 md:grid-cols-7">
            {days.map((d) => {
              const list = blocks.filter((b) => b.date === d).sort((a, b) => a.start.localeCompare(b.start));
              return (
                <Card key={d} className={cn('min-w-0', d === today && 'ring-2 ring-brand-300')}>
                  <CardHeader className="px-3 pt-3" title={<span className="text-sm">{fmtDay(d)}</span>} action={d === today ? <Badge tone="brand">Today</Badge> : undefined} />
                  <CardBody className="space-y-2 p-3">
                    {list.length ? list.map((b) => (
                      <div key={b.id} className={cn('rounded-md border-l-4 px-2 py-1.5', KIND[b.kind].cls, b.status === 'missed' && 'opacity-60')}>
                        <p className="text-[11px] text-muted">{b.start}–{b.end} · {KIND[b.kind].label}</p>
                        <p className={cn('text-xs font-medium text-ink', b.status === 'done' && 'line-through decoration-success-600')}>{b.title}</p>
                        {b.status !== 'planned' && <p className="text-[10px] uppercase tracking-wide text-subtle">{b.status}</p>}
                      </div>
                    )) : <p className="text-xs text-subtle">Free</p>}
                  </CardBody>
                </Card>
              );
            })}
          </div>
          {week.unscheduled.length > 0 && (
            <Card className="mt-6"><CardHeader title="Didn't fit this week" description="Moved to next week automatically" />
              <CardBody><ul className="space-y-1 text-sm text-muted">{week.unscheduled.map((u, i) => <li key={i}>{u.title} · {u.minutes} min · {u.reason}</li>)}</ul></CardBody></Card>
          )}
        </>
      )}
    </>
  );
}
