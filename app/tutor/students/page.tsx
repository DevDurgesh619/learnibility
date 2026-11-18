import type { Metadata } from 'next';
import Link from 'next/link';
import { ChevronRight, Search, Trophy, Users } from 'lucide-react';
import { Delta, Pill, SectionTitle, Stat } from '@/components/tutor/bits';
import { firstName, loadWorkspace, needsAttention, scoreSeries, studentRows, type StudentRow } from '@/components/tutor/model';
import { formatDay, formatTime, relative } from '@/components/marketplace/dates';
import { BOARD_LABEL } from '@/components/marketplace/labels';
import { Avatar } from '@/components/ui/avatar';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import { Table, TBody, TD, TH, THead, TR } from '@/components/ui/table';
import { demoNow, demoToday, getTasks, addDaysLocal } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import { cn } from '@/lib/utils';

export const metadata: Metadata = { title: 'Students · Tutor' };

type SP = Record<string, string | undefined>;
const STATUS = ['all', 'active', 'attention', 'new', 'inactive'] as const;
const SORTS = { next: 'Next session', name: 'Name A–Z', grade: 'Grade', progress: 'Progress' } as const;

function href(sp: SP, patch: SP) {
  const p = new URLSearchParams(Object.entries({ ...sp, ...patch }).filter(([, v]) => v) as [string, string][]);
  return `/tutor/students${p.size ? `?${p}` : ''}#list`;
}

export default async function StudentsPage({ searchParams }: { searchParams: Promise<SP> }) {
  const sp = await searchParams;
  const persona = (await currentPersona())!;
  const ws = loadWorkspace(persona.id);
  if (!ws || ws.students.length === 0) {
    return (
      <>
        <h1 className="mb-6 text-2xl font-semibold tracking-tight text-ink">Students</h1>
        <EmptyState icon={<Users />} title="No students yet" description="Students appear here once you accept a demo request from Explore Tutors." action={<Link href="/tutor" className={buttonVariants()}>Back to Home</Link>} />
      </>
    );
  }
  const now = new Date(demoNow());
  const rows = studentRows(ws);
  const attention = needsAttention(rows);
  const activeWeek = rows.filter((r) => r.daysInactive < 7).length;
  const improving = rows.filter((r) => (r.progressDelta ?? 0) > 0).length;

  // filters (3c chips, 3d panel)
  const status = (STATUS as readonly string[]).includes(sp.status ?? '') ? sp.status! : 'all';
  const q = sp.q?.toLowerCase().trim();
  let list = rows.filter((r) => status === 'all' || (status === 'attention' ? !!r.issue : r.status === status));
  if (q) list = list.filter((r) => r.name.toLowerCase().includes(q) || `class ${r.grade}`.includes(q) || String(r.grade) === q || r.goal.toLowerCase().includes(q));
  if (sp.grade) list = list.filter((r) => String(r.grade) === sp.grade);
  if (sp.perf === 'weak') list = list.filter((r) => (r.avgScorePct ?? 100) < 60);
  if (sp.perf === 'strong') list = list.filter((r) => (r.avgScorePct ?? 0) >= 75);
  if (sp.format === 'group') list = list.filter((r) => ws.sessions.some((s) => s.kind === 'group' && s.learnerIds.includes(r.learnerId)));
  if (sp.format === 'one_to_one') list = list.filter((r) => ws.sessions.some((s) => s.kind === 'one_to_one' && s.learnerIds.includes(r.learnerId)));
  if (sp.upcoming === '1') list = list.filter((r) => !!r.nextSession);
  const sort = (sp.sort ?? 'next') as keyof typeof SORTS;
  list = [...list].sort((a, b) =>
    sort === 'name' ? a.name.localeCompare(b.name) : sort === 'grade' ? a.grade - b.grade : sort === 'progress' ? (b.progressDelta ?? -99) - (a.progressDelta ?? -99) : (a.nextSession?.startUtc ?? '9').localeCompare(b.nextSession?.startUtc ?? '9'));

  // leaderboard (3b): this month
  const monthStart = `${demoToday().slice(0, 7)}-01`;
  const top = rows.map((r) => {
    const s = scoreSeries(ws, r.learnerId).filter((x) => x.source === 'assignment' && x.date >= monthStart).at(-1);
    return { r, s };
  }).filter((x) => x.s).sort((a, b) => b.s!.pct - a.s!.pct).slice(0, 3);
  const disciplined = rows.map((r) => {
    const t = getTasks(r.learnerId, undefined, { createdBy: ws.tutor.id, range: [monthStart, addDaysLocal(demoToday(), -1)] });
    const done = t.filter((x) => x.status === 'done').length;
    return { r, done, total: t.length };
  }).filter((x) => x.total > 0).sort((a, b) => b.done / b.total - a.done / a.total || (b.r.attendancePct ?? 0) - (a.r.attendancePct ?? 0)).slice(0, 3);

  const pick = sp.pick === 'assign';

  return (
    <>
      <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-ink">Students</h1>
          {pick && <p className="mt-1 text-sm text-brand-700">Pick a student to assign a test to.</p>}
        </div>
      </div>

      <section className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <Stat label="Total students" value={rows.length} href={href(sp, { status: undefined })} />
        <Stat label="Active this week" value={activeWeek} href={href(sp, { status: 'active' })} />
        <Stat label="Improving" value={improving} hint="score up vs earlier tests" href={href(sp, { sort: 'progress' })} />
        <Stat label="Need attention" value={attention.length} href={href(sp, { status: 'attention' })} />
      </section>

      {attention.length > 0 && !pick && (
        <Card className="mt-6">
          <CardHeader title="Needs your attention" />
          <CardBody className="pt-3">
            <Table>
              <THead><TR><TH>Student</TH><TH>Issue</TH><TH className="hidden sm:table-cell">Last activity</TH><TH className="text-right">Action</TH></TR></THead>
              <TBody>
                {attention.map((r) => (
                  <TR key={r.learnerId}>
                    <TD><Link href={`/tutor/students/${r.learnerId}`} className="flex items-center gap-2 font-medium text-ink hover:text-brand-700"><Avatar name={r.name} size="sm" />{firstName(r.name)}</Link></TD>
                    <TD className="text-ink">{r.issue!.label}</TD>
                    <TD className="hidden text-muted sm:table-cell">{relative(r.lastActivityUtc, now)}</TD>
                    <TD className="text-right"><Link href={r.issue!.href} className={buttonVariants({ size: 'sm', variant: 'secondary' })}>{r.issue!.action}</Link></TD>
                  </TR>
                ))}
              </TBody>
            </Table>
          </CardBody>
        </Card>
      )}

      {!pick && (
        <section className="mt-6 grid gap-6 lg:grid-cols-2">
          <Board title="Top scorers in assignments" hint="this month" items={top.map(({ r, s }) => ({ id: r.learnerId, name: r.name, line: `${s!.pct}% · ${s!.title}` }))} empty="No marked assignments this month yet." />
          <Board title="Most disciplined" hint="tasks on time + sessions attended" items={disciplined.map(({ r, done, total }) => ({ id: r.learnerId, name: r.name, line: `${done} / ${total} tasks · ${r.attendancePct ?? 100}% attendance` }))} empty="No tasks set this month yet." />
        </section>
      )}

      <section id="list" className="mt-8 scroll-mt-20">
        <SectionTitle>All students · {rows.length}</SectionTitle>
        <form className="flex flex-col gap-2 sm:flex-row" action="/tutor/students">
          {Object.entries(sp).filter(([k, v]) => k !== 'q' && v).map(([k, v]) => <input key={k} type="hidden" name={k} value={v} />)}
          <label className="relative flex-1">
            <span className="sr-only">Search students</span>
            <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-subtle" />
            <input name="q" defaultValue={sp.q} placeholder="Type a name or grade…" className="h-10 w-full rounded-lg border border-line bg-surface pl-9 pr-3 text-sm outline-none focus:border-brand-400" />
          </label>
          <details className="relative">
            <summary className={cn(buttonVariants({ variant: 'secondary' }), 'cursor-pointer list-none')}>Filter & sort</summary>
            <div className="absolute right-0 z-20 mt-2 w-72 rounded-[var(--radius-card)] border border-line bg-surface p-4 shadow-lg">
              <Facet label="Sort by" items={Object.entries(SORTS).map(([k, l]) => [l, href(sp, { sort: k })] as const)} active={SORTS[sort]} />
              <Facet label="Performance" items={[['Weak', href(sp, { perf: 'weak' })], ['Strong', href(sp, { perf: 'strong' })], ['Inactive', href(sp, { status: 'inactive' })]]} active={sp.perf === 'weak' ? 'Weak' : sp.perf === 'strong' ? 'Strong' : status === 'inactive' ? 'Inactive' : ''} />
              <Facet label="Status" items={[['New', href(sp, { status: 'new' })], ['Upcoming session', href(sp, { upcoming: '1' })]]} active={status === 'new' ? 'New' : sp.upcoming ? 'Upcoming session' : ''} />
              <Facet label="Format" items={[['1:1', href(sp, { format: 'one_to_one' })], ['Group', href(sp, { format: 'group' })]]} active={sp.format === 'group' ? 'Group' : sp.format === 'one_to_one' ? '1:1' : ''} />
              <Facet label="Grade" items={['8', '9', '10', '11', '12'].map((g) => [g, href(sp, { grade: g })] as const)} active={sp.grade ?? ''} />
              <Link href="/tutor/students#list" className="mt-2 inline-block text-sm text-brand-700 hover:underline">Clear all</Link>
            </div>
          </details>
        </form>
        <div className="mt-3 flex flex-wrap gap-2">
          {STATUS.map((s) => (
            <Link key={s} href={href(sp, { status: s === 'all' ? undefined : s })} className={cn('rounded-full border px-3 py-1 text-sm', status === s ? 'border-brand-600 bg-brand-600 text-white' : 'border-line bg-surface text-ink hover:bg-surface-muted')}>
              {{ all: 'All', active: 'Active', attention: `Needs attention · ${attention.length}`, new: `New · ${rows.filter((r) => r.status === 'new').length}`, inactive: 'Inactive' }[s]}
            </Link>
          ))}
        </div>

        {list.length === 0 ? (
          <EmptyState className="mt-4" title="No students match" description="Clear a filter to see more." action={<Link href="/tutor/students#list" className={buttonVariants({ variant: 'secondary' })}>Clear filters</Link>} />
        ) : (
          <Card className="mt-4">
            <ul className="divide-y divide-line">
              {list.map((r) => <Row key={r.learnerId} r={r} pick={pick} />)}
            </ul>
          </Card>
        )}
      </section>
    </>
  );
}

function Row({ r, pick }: { r: StudentRow; pick: boolean }) {
  const next = r.pendingDemo?.slotStartUtc ? `${formatDay(r.pendingDemo.slotStartUtc)} ${formatTime(r.pendingDemo.slotStartUtc)} (demo)` : r.nextSession ? `${formatDay(r.nextSession.startUtc)} ${formatTime(r.nextSession.startUtc)}` : 'Not scheduled';
  return (
    <li>
      <Link href={pick ? `/tutor/students/${r.learnerId}/assignments/new` : `/tutor/students/${r.learnerId}`} className="flex items-center gap-3 px-4 py-3 hover:bg-surface-muted/60">
        <Avatar name={r.name} size="sm" />
        <div className="min-w-0 flex-1">
          <p className="flex items-center gap-2 truncate text-sm font-medium text-ink">{r.name} {r.status === 'new' && <Pill tone="brand">new</Pill>}{r.issue && <Pill tone="warning">attention</Pill>}</p>
          <p className="truncate text-xs text-muted">Class {r.grade} {BOARD_LABEL[r.board]}{r.goal ? ` · ${r.goal}` : ''}</p>
        </div>
        <div className="hidden w-28 text-sm sm:block">{r.pendingDemo ? <span className="text-xs text-muted">demo pending</span> : <Delta value={r.progressDelta} />}</div>
        <div className="hidden w-44 text-right text-sm text-muted md:block">{next}</div>
        <ChevronRight className="size-4 text-subtle" />
      </Link>
    </li>
  );
}

function Board({ title, hint, items, empty }: { title: string; hint: string; items: { id: string; name: string; line: string }[]; empty: string }) {
  return (
    <Card>
      <CardHeader title={title} description={hint} />
      <CardBody className="pt-3">
        {items.length === 0 ? <p className="text-sm text-muted">{empty}</p> : (
          <ol className="grid gap-3 sm:grid-cols-3">
            {items.map((x, i) => (
              <li key={x.id} className="rounded-lg border border-line p-3 text-center">
                <span className={cn('mx-auto mb-1 flex size-6 items-center justify-center rounded-full text-xs font-semibold', i === 0 ? 'bg-amber-100 text-amber-700' : 'bg-surface-muted text-muted')}>{i === 0 ? <Trophy className="size-3.5" /> : i + 1}</span>
                <Avatar name={x.name} size="sm" className="mx-auto" />
                <p className="mt-1 text-sm font-medium text-ink">{firstName(x.name)}</p>
                <p className="text-xs text-muted">{x.line}</p>
              </li>
            ))}
          </ol>
        )}
      </CardBody>
    </Card>
  );
}

function Facet({ label, items, active }: { label: string; items: readonly (readonly [string, string])[]; active: string }) {
  return (
    <div className="mb-3">
      <p className="mb-1.5 text-xs font-semibold uppercase tracking-wide text-muted">{label}</p>
      <div className="flex flex-wrap gap-1.5">
        {items.map(([l, h]) => <Link key={l} href={h} className={cn('rounded-full border px-2.5 py-0.5 text-xs', active === l ? 'border-brand-600 bg-brand-600 text-white' : 'border-line hover:bg-surface-muted')}>{l}</Link>)}
      </div>
    </div>
  );
}
