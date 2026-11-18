import Link from 'next/link';
import { ChevronLeft } from 'lucide-react';
import { TrendChart } from '@/components/charts';
import { Badge, Card, CardBody, CardHeader, Progress } from '@/components/ui';
import {
  ApplicationCards, ApplicationUpsell, AssessmentHero, MetricCards, NextActionCard, SectionTitle, SessionsCard, TextLink,
} from '@/components/student/home-cards';
import {
  applicationCards, isSubscriber, joinState, metricSeries, metricSummaries, nextActions, sessionsOf, starterTasks, studentCtx, tasksFor, todayLocal,
  weekTimetable, whenLabel, type MetricRange,
} from '@/components/student/load';
import { METRICS, PLAN_LABEL, type MetricKey } from '@/components/student/model';
import { TaskList } from '@/components/student/task-list';
import { Avatar } from '@/components/ui/avatar';
import { DEMO_NOW, DEMO_TIMEZONE } from '@/lib/demo-clock';
import { cn } from '@/lib/utils';

export const metadata = { title: 'Home · Learnibility' };

const TODAY_LABEL = new Intl.DateTimeFormat('en-IN', { weekday: 'long', day: 'numeric', month: 'long', timeZone: DEMO_TIMEZONE }).format(DEMO_NOW);

/** Time-of-day greeting on the demo clock, so every screen tells the same story. */
function greeting() {
  const hour = Number(new Intl.DateTimeFormat('en-GB', { hour: 'numeric', hour12: false, timeZone: DEMO_TIMEZONE }).format(DEMO_NOW));
  return hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';
}

export default async function StudentHome({ searchParams }: { searchParams: Promise<{ metric?: string; range?: string }> }) {
  const sp = await searchParams;
  const ctx = await studentCtx();
  const metric = METRICS.find((m) => m.key === sp.metric);
  if (metric) return <MetricDetail metricKey={metric.key} range={(['week', 'month', 'year'].includes(sp.range ?? '') ? sp.range : 'week') as MetricRange} />;

  const tt = weekTimetable(ctx);
  const tasks = ctx.firstVisit ? starterTasks() : tasksFor(ctx, todayLocal(), tt);
  const done = tasks.filter((t) => t.done).length;
  const actions = nextActions(ctx);
  const upcoming = sessionsOf(ctx).filter((s) => s.status === 'scheduled').slice(0, 3);
  const joins = Object.fromEntries(upcoming.map((s) => [s.id, joinState(s)]));
  const whens = Object.fromEntries(upcoming.map((s) => [s.id, whenLabel(s.startUtc)]));
  const subscriber = isSubscriber(ctx);
  const apps = applicationCards(ctx);
  const profilePct = ctx.student?.profileCompletionPct ?? 30;

  return (
    <>
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-4">
          <Avatar name={ctx.name} personId={ctx.learnerId} photo size="lg" className="hidden ring-4 ring-white shadow-sm sm:block" />
          <div>
            <p className="text-xs font-medium text-subtle">{TODAY_LABEL}{ctx.student?.programme ? ` · ${ctx.student.programme}` : ''}{ctx.student?.school ? ` · ${ctx.student.school}` : ''}</p>
            <h1 className="mt-0.5 text-2xl font-semibold tracking-tight text-ink">{greeting()}, {ctx.firstName}{ctx.firstVisit ? ' 👋' : ''}</h1>
            <p className="mt-1 text-sm text-muted">{ctx.firstVisit ? 'Welcome to Learnibility. Start with a short assessment so we can plan around you.' : 'Here is what to do today, then how you are doing.'}</p>
          </div>
        </div>
        {subscriber ? (
          <Badge tone="success" className="self-start sm:self-auto">{PLAN_LABEL[ctx.plan]}</Badge>
        ) : (
          <Link href="/student/inventory" className="flex items-center gap-2 self-start text-xs text-muted sm:self-auto" title="Profile completion">
            Profile {profilePct}%<Progress value={profilePct / 100} className="w-24" />
          </Link>
        )}
      </div>

      {ctx.firstVisit ? <AssessmentHero /> : <NextActionCard actions={actions} />}

      <div className="grid gap-4 lg:grid-cols-[1.6fr_1fr] [&>*]:min-w-0">
        <Card>
          <CardHeader
            title={ctx.firstVisit ? 'Today' : `Today's tasks · ${done}/${tasks.length}`}
            action={<TextLink href="/student/timetable">Timetable</TextLink>}
          />
          <CardBody className="pt-2">
            {tasks.length ? <TaskList tasks={tasks} /> : <p className="py-6 text-center text-sm text-muted">Nothing planned for today. Enjoy the break, or pull a task forward from the timetable.</p>}
            {ctx.firstVisit && <p className="mt-2 text-xs text-subtle">Draft plan from your targets · <Link className="underline" href="/student/timetable">Edit in Timetable</Link></p>}
          </CardBody>
        </Card>
        <SessionsCard sessions={upcoming} joinStates={joins} whenLabels={whens} />
      </div>

      {subscriber && apps.length > 0 && (
        <>
          <SectionTitle title="Applications" action={<TextLink href="/student/applications">Application Support</TextLink>} />
          <ApplicationCards apps={apps} deadlineLabels={Object.fromEntries(apps.map((a) => [a.id, a.deadlineUtc ? `Deadline ${whenLabel(a.deadlineUtc).replace(/ \d+:\d+ [ap]m$/, '')}` : 'No deadline']))} />
        </>
      )}

      <SectionTitle title="Your progress · this week" action={!ctx.firstVisit && <span className="text-xs text-subtle">Tap a card for the graph</span>} />
      <MetricCards metrics={metricSummaries(ctx)} sparks={Object.fromEntries(METRICS.map((m) => [m.key, metricSeries(ctx, m.key, 'month').map((p) => p.value)]))} />
      {ctx.firstVisit && <p className="mt-2 text-xs text-subtle">Metrics appear after your first assessment and a week of tasks.</p>}

      {!subscriber && <ApplicationUpsell />}
    </>
  );
}

async function MetricDetail({ metricKey, range }: { metricKey: MetricKey; range: MetricRange }) {
  const ctx = await studentCtx();
  const def = METRICS.find((m) => m.key === metricKey)!;
  const summary = metricSummaries(ctx).find((m) => m.key === metricKey)!;
  const series = metricSeries(ctx, metricKey, range);
  const chip = (active: boolean) => cn('rounded-full px-3 py-1 text-sm ring-1 ring-inset transition-colors', active ? 'bg-ink text-white ring-ink' : 'bg-surface text-muted ring-line hover:text-ink');

  return (
    <>
      <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-2">
          <Link href="/student" className="inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" />Home</Link>
          <h1 className="text-2xl font-semibold tracking-tight text-ink">{def.label}</h1>
        </div>
        <div className="flex gap-2">
          {(['week', 'month', 'year'] as const).map((r) => (
            <Link key={r} href={`/student?metric=${metricKey}&range=${r}`} className={chip(r === range)}>{r[0]!.toUpperCase() + r.slice(1)}</Link>
          ))}
        </div>
      </div>
      <div className="mb-4 flex flex-wrap gap-2">
        {METRICS.map((m) => <Link key={m.key} href={`/student?metric=${m.key}&range=${range}`} className={chip(m.key === metricKey)}>{m.label}</Link>)}
      </div>
      <Card>
        <CardBody>
          {series.some((p) => p.value !== null) ? (
            <TrendChart
              data={series.map((p) => ({ x: p.x, value: p.value }))}
              series={[{ key: 'value', label: def.label }]}
              format="percent" domain={[0, 1]} height={300}
              target={metricKey === 'retention' ? { value: 0.7, label: 'Retention target 70%' } : undefined}
            />
          ) : (
            <p className="py-16 text-center text-sm text-muted">No data yet. {summary.emptyReason ?? ''}</p>
          )}
        </CardBody>
      </Card>
      <div className="mt-4 grid gap-3 sm:grid-cols-3">
        <Card className="p-4"><p className="text-2xl font-semibold text-ink">{summary.value === null ? '—' : `${Math.round(summary.value * 100)}%`}</p><p className="text-sm text-muted">this week</p></Card>
        <Card className="p-4"><p className="text-2xl font-semibold text-ink">{summary.delta === null ? '—' : `${summary.delta >= 0 ? '+' : '−'}${Math.abs(Math.round(summary.delta * 100))}`}</p><p className="text-sm text-muted">vs last week, in points</p></Card>
        <Card className="bg-surface-muted/60 p-4"><p className="text-sm font-semibold text-ink">How it’s calculated</p><p className="mt-1 text-sm text-muted">{def.how}</p></Card>
      </div>
    </>
  );
}
