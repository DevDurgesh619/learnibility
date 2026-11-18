import Link from 'next/link';
import { CalendarDays, Download, RefreshCw, Sparkles } from 'lucide-react';
import { Badge, Button, Card, CardBody, CardHeader, EmptyState } from '@/components/ui';
import {
  addDaysStr, describeRequest, nowUtc, requestTitle, mainCounsellor, mondayOf, pendingRequests, requestDates, starterTasks, studentCtx,
  tasksFor, todayLocal, weekTimetable, fmtDay,
} from '@/components/student/load';
import { LinkButton } from '@/components/student/link-button';
import { TaskList } from '@/components/student/task-list';
import { RequestChangeButton, UndoRequestButton } from '@/components/timetable/request-change';
import { BlockLegend, WeekGrid, type GridDay } from '@/components/timetable/week-grid';
import { regenerateTimetable } from '@/lib/actions/timetable';
import { cn } from '@/lib/utils';

export const metadata = { title: 'Timetable · Learnibility' };

const DAY = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
type View = 'today' | 'week' | 'month';

export default async function TimetablePage({ searchParams }: { searchParams: Promise<{ view?: string; request?: string }> }) {
  const sp = await searchParams;
  const view: View = sp.view === 'today' || sp.view === 'month' ? sp.view : 'week';
  const ctx = await studentCtx();
  const today = todayLocal();
  const weekStart = mondayOf(today);
  const tt = weekTimetable(ctx, weekStart);
  const counsellor = mainCounsellor(ctx);
  const requests = pendingRequests(ctx.learnerId);
  const canRequest = ctx.hasCounsellor && !!counsellor && !!tt;

  const chip = (active: boolean) => cn('rounded-full px-3 py-1 text-sm ring-1 ring-inset', active ? 'bg-ink text-white ring-ink' : 'bg-surface text-muted ring-line hover:text-ink');

  const header = (
    <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-ink">Timetable</h1>
        <p className="mt-1 text-sm text-muted">Re-planned after every test and missed task. Tick blocks off as you go.</p>
      </div>
      <div className="flex items-center gap-2">
        {requests.length > 0 && counsellor && <Badge tone="success">{requests.length} change{requests.length > 1 ? 's' : ''} pending with {counsellor.name.split(' ')[0]}</Badge>}
        {(['today', 'week', 'month'] as const).map((v) => <Link key={v} href={`/student/timetable?view=${v}`} className={chip(view === v)}>{v[0]!.toUpperCase() + v.slice(1)}</Link>)}
      </div>
    </div>
  );

  if (!tt) {
    return (
      <>
        {header}
        <Card className="mb-4">
          <CardHeader title="Draft plan" description="From the targets you gave at sign-up. Your real plan arrives after the first assessment." />
          <CardBody className="pt-2"><TaskList tasks={starterTasks()} /></CardBody>
        </Card>
        <EmptyState icon={<CalendarDays />} title="Your timetable is waiting for your first assessment"
          description="The assessment finds your gaps; the planner then fits practice, reviews and tests into your free time."
          action={<LinkButton href="/student/assessments">Take the free assessment</LinkButton>} />
      </>
    );
  }

  const byTitle = new Map<string, string[]>();
  for (const b of tt.blocks) {
    if (b.kind === 'buffer' || b.kind === 'session' || b.endUtc <= nowUtc()) continue;
    const t = b.title.replace(/^Review \d\/\d: /, 'Review: ');
    byTitle.set(t, [...(byTitle.get(t) ?? []), b.id]);
  }
  const taskOptions = [...byTitle].map(([title, blockIds]) => ({ title, blockIds }));
  const grid = (start: string): GridDay[] => {
    const t = start === weekStart ? tt : weekTimetable(ctx, start)!;
    return DAY.map((label, i) => {
      const date = addDaysStr(start, i);
      const blocks = t.blocks.filter((b) => b.date === date && b.kind !== 'buffer').sort((a, b) => a.start.localeCompare(b.start))
        .map((b) => ({ ...b, title: shortBlock(b.title) }));
      const ghosts = requests.flatMap((r) => requestDates(r, start).includes(date)
        ? [{ id: `${r.id}_${date}`, kind: 'chapter' as const, title: shortBlock(requestTitle(r)), start: typeof r.proposed === 'object' ? r.proposed.start : '', minutes: 0, status: 'planned' as const, pending: true }] : []);
      return { date, label, dayNum: fmtDay(date), isToday: date === today, blocks: [...blocks, ...ghosts] };
    });
  };

  return (
    <>
      {header}
      <div className="mb-4 flex flex-wrap items-center gap-2">
        <Badge tone="brand"><Sparkles className="size-3" />AI generated · updated Sun</Badge>
        <span className="text-xs text-subtle">{Math.round(tt.plannedMinutes / 6) / 10} h planned · {Math.round(tt.bufferMinutes / 6) / 10} h buffer</span>
        <div className="ml-auto flex flex-wrap gap-2">
          <form action={regenerateTimetable}><Button variant="secondary" size="sm"><RefreshCw />Regenerate</Button></form>
          <a href="/student/timetable/ics" download className="inline-flex h-8 items-center gap-2 rounded-lg border border-line bg-surface px-3 text-sm font-medium text-ink shadow-sm hover:bg-surface-muted"><Download className="size-4" />Export .ics</a>
          {canRequest && <RequestChangeButton counsellorName={counsellor!.name} tasks={taskOptions} defaultDate={addDaysStr(today, 1)} autoOpen={sp.request === '1'} />}
        </div>
      </div>

      {requests.map((r) => (
        <Card key={r.id} className="mb-4 border-success-600/40">
          <CardBody className="flex flex-col gap-3 sm:flex-row sm:items-center">
            <div className="min-w-0 flex-1">
              <p className="text-sm font-semibold text-ink">Request sent</p>
              <p className="text-sm text-muted">{describeRequest(r)}. {counsellor?.name.split(' ')[0]} usually replies within a day; the block updates automatically once approved.</p>
            </div>
            <UndoRequestButton requestId={r.id} />
          </CardBody>
        </Card>
      ))}

      {view !== 'month' && (
        <Card className="mb-4">
          <CardHeader title={`Today's tasks · ${DAY[(new Date(today + 'T00:00:00Z').getUTCDay() + 6) % 7]}`} description="Tap a box when you finish; missed blocks move to your next free slot." />
          <CardBody className="pt-2">
            {(() => { const tasks = tasksFor(ctx, today, tt); return tasks.length ? <TaskList tasks={tasks} columns={2} /> : <p className="py-6 text-center text-sm text-muted">Nothing planned today.</p>; })()}
          </CardBody>
        </Card>
      )}

      {view === 'week' && (
        <>
          <WeekGrid days={grid(weekStart)} />
          <div className="mt-3"><BlockLegend /></div>
        </>
      )}

      {view === 'month' && (
        <div className="flex flex-col gap-3">
          {[-7, 0, 7, 14].map((off) => {
            const start = addDaysStr(weekStart, off);
            return (
              <div key={start}>
                <p className="mb-1 text-xs font-medium text-muted">Week of {fmtDay(start)}{off < 0 ? ' · done' : off === 0 ? ' · this week' : ' · draft, re-planned after each test'}</p>
                <WeekGrid days={grid(start)} />
              </div>
            );
          })}
        </div>
      )}

      {tt.unscheduled.length > 0 && (
        <Card className="mt-4">
          <CardHeader title="Didn't fit this week" description="These move to next week unless you free up time." />
          <CardBody className="pt-2">
            <ul className="divide-y divide-line text-sm">
              {tt.unscheduled.map((u) => <li key={`${u.kind}-${u.refId ?? u.title}`} className="flex justify-between py-2"><span className="text-ink">{u.title}</span><span className="text-muted">{u.minutes} min · {u.reason}</span></li>)}
            </ul>
          </CardBody>
        </Card>
      )}
    </>
  );
}

/** "Mathematics: Irrational numbers" → "Maths: Irrational numbers" for the compact grid. */
function shortBlock(title: string) {
  return title.replace(/^Review \d\/\d: /, 'Review: ').replace('Mathematics', 'Maths').replace(/^Practice: /, '');
}
