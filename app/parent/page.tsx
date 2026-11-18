import Link from 'next/link';
import { AlertCircle, CalendarClock, CheckCircle2, ChevronRight, Clock, Sparkles, Target, TrendingUp } from 'lucide-react';
import { ChildSwitcher } from '@/components/parent/child-switcher';
import { attentionFor } from '@/components/parent/attention';
import { parentContext, type SearchParams } from '@/components/parent/context';
import { firstName, fmtDateTime, fmtDay, plural } from '@/components/parent/format';
import { NoChild } from '@/components/parent/no-child';
import { Avatar, Badge, BandBadge, Card, CardBody, CardHeader, EmptyState, GapBadge, PageHeader, Progress, StatTile } from '@/components/ui';
import {
  addDaysLocal, demoNow, demoToday, getAlr, getAttempts, getGaps, getNextBestActions, getPersonName, getSubject, getSubtopic,
} from '@/lib/data';
import { formatHours, formatPercent } from '@/lib/format';

export default async function ParentHome({ searchParams }: { searchParams: SearchParams }) {
  const { parent, parentName, children, child } = await parentContext(searchParams);
  const attention = attentionFor(parent.id, children);
  if (!child) {
    return (<><PageHeader eyebrow="Parent" title={`Hi ${firstName(parentName)}`} description="This week at a glance for each child." /><NoChild /></>);
  }
  const s = child.student;
  const id = s.id;
  const today = demoToday();
  const weekAgo = addDaysLocal(today, -7);
  const attempts = getAttempts(id).filter((a) => a.submittedUtc.slice(0, 10) >= weekAgo);
  const allGaps = getGaps(id);
  const closedThisWeek = allGaps.filter((g) => g.status === 'closed' && (g.closedUtc ?? '').slice(0, 10) >= weekAgo);
  const newThisWeek = allGaps.filter((g) => g.status !== 'closed' && g.detectedUtc.slice(0, 10) >= weekAgo);
  const open = allGaps.filter((g) => g.status !== 'closed');
  const alr = getAlr(id);
  const hist = alr.history;
  const prevLrs = (() => {
    const cutoff = addDaysLocal(today, -28);
    const older = hist.filter((h) => h.asOfUtc.slice(0, 10) <= cutoff);
    if (!older.length) return null;
    const latest = new Map<string, number>();
    for (const h of older) latest.set(h.chapterId, h.LRS);
    const xs = [...latest.values()];
    return Math.round((xs.reduce((a, b) => a + b, 0) / xs.length) * 100) / 100;
  })();
  const nba = getNextBestActions(id, 1)[0];
  const tasks = child.tasksThisWeek;
  const lrsDelta = child.lrs !== null && prevLrs !== null ? Math.round((child.lrs - prevLrs) * 100) / 100 : null;

  return (
    <>
      <PageHeader eyebrow="Parent" title={`Hi ${firstName(parentName)}`} description={`Here is ${s.firstName}'s week, up to ${fmtDay(today)}.`} />
      <ChildSwitcher children={children} selectedId={id} basePath="/parent" />

      {children.length > 1 && (
        <section className="mb-6 grid gap-4 md:grid-cols-2">
          {children.map((c) => (
            <Link key={c.student.id} href={`/parent?child=${c.student.id}`} className="group">
              <Card className={c.student.id === id ? 'ring-2 ring-brand-300' : 'transition-shadow group-hover:shadow-md'}>
                <CardBody className="flex items-center gap-4">
                  <Avatar name={c.student.name} size="lg" />
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2"><p className="font-semibold text-ink">{c.student.name}</p><BandBadge band={c.band} /></div>
                    <p className="text-sm text-muted">{c.student.programme}</p>
                    <p className="mt-1 text-sm text-muted">{plural(c.openGaps, 'open gap')} · {formatHours(c.hoursToClose)} to close · {c.tasksThisWeek.done}/{c.tasksThisWeek.total} tasks this week</p>
                  </div>
                  <ChevronRight className="size-5 text-subtle" />
                </CardBody>
              </Card>
            </Link>
          ))}
        </section>
      )}

      <section className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatTile label="Learning rate (LRS)" value={child.lrs !== null ? child.lrs.toFixed(2) : '—'} icon={<TrendingUp />}
          delta={lrsDelta !== null && lrsDelta !== 0 ? { value: `${lrsDelta > 0 ? '+' : ''}${lrsDelta.toFixed(2)}`, direction: lrsDelta > 0 ? 'up' : 'down' } : undefined}
          hint={prevLrs !== null ? `vs ${s.firstName}'s own level 4 weeks ago` : 'Builds up after a few tests'} />
        <StatTile label="Tasks this week" value={`${tasks.done}/${tasks.total}`} icon={<CheckCircle2 />} hint={tasks.total ? `${formatPercent(tasks.done / tasks.total)} done so far` : 'No tasks planned'} />
        <StatTile label="Open gaps" value={open.length} icon={<Target />}
          delta={closedThisWeek.length ? { value: `${closedThisWeek.length} closed`, direction: 'down', good: true } : undefined}
          hint={newThisWeek.length ? `${newThisWeek.length} new this week` : 'None new this week'} />
        <StatTile label="Hours to close" value={formatHours(child.hoursToClose)} icon={<Clock />} hint={`At about ${s.weeklyHours} h a week of study`} />
      </section>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="order-2 min-w-0 space-y-6 lg:order-none lg:col-span-2">
          <Card>
            <CardHeader title="This week's digest" description={`${fmtDay(weekAgo)} to ${fmtDay(today)}`} />
            <CardBody className="space-y-5">
              <DigestRow label="Tests taken">
                {attempts.length ? (
                  <ul className="space-y-2">
                    {attempts.slice(0, 4).map((a) => (
                      <li key={a.id} className="flex items-center justify-between gap-3 text-sm">
                        <span className="min-w-0 truncate text-ink">{a.title}<span className="text-subtle"> · {getSubject(a.subjectId)?.subject.name ?? ''}</span></span>
                        <span className="shrink-0 font-medium text-ink">{a.maxScore ? formatPercent(a.score / a.maxScore) : '—'}</span>
                      </li>
                    ))}
                  </ul>
                ) : <p className="text-sm text-muted">No tests this week.</p>}
              </DigestRow>
              <DigestRow label="Gaps closed">
                {closedThisWeek.length ? (
                  <ul className="flex flex-wrap gap-2">{closedThisWeek.map((g) => <Badge key={g.id} tone="success" className="max-w-full"><span className="truncate">{getSubtopic(g.subtopicId)?.name ?? g.subtopicId}</span></Badge>)}</ul>
                ) : <p className="text-sm text-muted">None closed yet this week. Gaps close after a re-test and a 7-day retention check.</p>}
              </DigestRow>
              <DigestRow label="New gaps found">
                {newThisWeek.length ? (
                  <ul className="space-y-2">{newThisWeek.slice(0, 4).map((g) => (
                    <li key={g.id} className="flex flex-wrap items-center gap-2 text-sm"><GapBadge code={g.code} /><span className="text-ink">{getSubtopic(g.subtopicId)?.name ?? g.subtopicId}</span><span className="text-subtle">{formatHours(g.hoursToClose)}</span></li>
                  ))}</ul>
                ) : <p className="text-sm text-muted">No new gaps this week.</p>}
              </DigestRow>
              <DigestRow label="Plan progress">
                <div className="flex items-center gap-3"><Progress value={tasks.total ? tasks.done / tasks.total : 0} tone={tasks.total && tasks.done / tasks.total < 0.5 ? 'warning' : 'success'} /><span className="shrink-0 text-sm text-muted">{tasks.done} of {tasks.total}</span></div>
              </DigestRow>
            </CardBody>
          </Card>

          {nba && (
            <Card>
              <CardHeader title={`What ${s.firstName} should do next`} description="The app's next best action, and why" />
              <CardBody className="flex items-start gap-3">
                <span className="flex size-9 shrink-0 items-center justify-center rounded-full bg-brand-50 text-brand-600"><Sparkles className="size-4" /></span>
                <div><p className="font-medium text-ink">{nba.title}</p><p className="mt-0.5 text-sm text-muted">{nba.reason}</p></div>
              </CardBody>
            </Card>
          )}
        </div>

        <div className="order-1 min-w-0 space-y-6 lg:order-none">
          <Card>
            <CardHeader title="Needs you" description={attention.length ? `${plural(attention.length, 'item')} across your family` : undefined} />
            <CardBody className="pt-3">
              {attention.length ? (
                <ul className="divide-y divide-line">
                  {attention.map((a) => (
                    <li key={a.id} className="py-3 first:pt-0 last:pb-0">
                      <Link href={a.href} className="group flex items-start gap-3">
                        <AlertCircle className={`mt-0.5 size-4 shrink-0 ${a.tone === 'danger' ? 'text-danger-600' : a.tone === 'warning' ? 'text-warning-600' : 'text-brand-600'}`} />
                        <div className="min-w-0 flex-1"><p className="text-sm font-medium text-ink group-hover:underline">{a.title}</p><p className="line-clamp-2 text-xs text-muted">{a.detail}</p></div>
                        <span className="shrink-0 text-xs font-medium text-brand-600">{a.cta}</span>
                      </Link>
                    </li>
                  ))}
                </ul>
              ) : <EmptyState className="border-0 py-6" icon={<CheckCircle2 />} title="All caught up" description="Nothing needs your decision right now." />}
            </CardBody>
          </Card>
          <Card>
            <CardHeader title="Next session" />
            <CardBody className="pt-3">
              {child.nextSession ? (
                <div className="flex items-start gap-3">
                  <CalendarClock className="mt-0.5 size-5 text-brand-600" />
                  <div>
                    <p className="font-medium text-ink">{child.nextSession.title}</p>
                    <p className="text-sm text-muted">{fmtDateTime(child.nextSession.startUtc)} · {child.nextSession.minutes} min</p>
                    <p className="text-sm text-muted">with {getPersonName(child.nextSession.hostId)?.name ?? 'their tutor'}</p>
                  </div>
                </div>
              ) : <p className="text-sm text-muted">No sessions booked. {s.firstName}&apos;s tutor and counsellor sessions show here.</p>}
            </CardBody>
          </Card>
          <p className="px-1 text-xs text-subtle">Progress is always compared with {s.firstName}&apos;s own past, never ranked against other children. Updated {fmtDateTime(demoNow())}.</p>
        </div>
      </div>
    </>
  );
}

function DigestRow({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="grid gap-2 sm:grid-cols-[9rem_1fr]">
      <p className="text-sm font-medium text-muted">{label}</p>
      <div className="min-w-0">{children}</div>
    </div>
  );
}
