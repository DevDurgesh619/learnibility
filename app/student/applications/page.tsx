import Link from 'next/link';
import { AlertTriangle, CalendarClock } from 'lucide-react';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import { Progress } from '@/components/ui/progress';
import { StatTile } from '@/components/ui/stat-tile';
import { ActionButton } from '@/components/applications/action-button';
import { applicationsBundle, firstName, getUniversity, programmeOf } from '@/components/applications/data';
import { requireSubscriber } from '@/components/applications/guard';
import { daysUntil, fmtDate, nextStep, progress, riskFlags } from '@/components/applications/logic';
import { SupportHeader } from '@/components/applications/support-header';
import { DaysLeft, FitBadge, StatusBadge, UniMark } from '@/components/applications/ui';
import { actionItemsToTasks, toggleActionItem } from '@/lib/actions/applications';
import { getSessions } from '@/lib/data';
import { DEMO_NOW } from '@/lib/demo-clock';

export const metadata = { title: 'Application Support · Learnibility' };

export default async function Page() {
  const { persona, ctx, counsellorName } = await requireSubscriber();
  const b = applicationsBundle(persona.id);
  const active = b.applications.filter((a) => a.status !== 'submitted' && a.status !== 'decision');
  const offers = b.applications.filter((a) => a.status === 'decision' && (a.decision === 'offer' || a.decision === 'conditional_offer'));
  const openItems = active.reduce((n, a) => n + a.checklist.filter((c) => !c.done).length, 0);
  const flags = b.applications.flatMap((a) => riskFlags(a, DEMO_NOW).map((f) => ({ ...f, app: a })));
  const cFirst = firstName(ctx.counsellorId);
  const nextMeeting = getSessions(persona.id, { from: DEMO_NOW.toISOString(), status: 'scheduled' })
    .filter((s) => s.hostRole === 'counsellor')
    .sort((x, y) => x.startUtc.localeCompare(y.startUtc))[0];
  const meeting = b.meetings[0];
  const todos = meeting?.actionItems ?? [];
  const untasked = todos.filter((t) => !t.taskId && !t.done).length;

  if (!b.applications.length) {
    return (
      <>
        <SupportHeader active="overview" counsellorName={counsellorName} />
        <EmptyState icon={<CalendarClock />} title="Your board is empty" description={`Shortlist universities and ${cFirst} will help you plan each application.`} action={<Link href="/student/applications/universities" className={buttonVariants()}>Find universities</Link>} />
      </>
    );
  }

  return (
    <>
      <SupportHeader active="overview" counsellorName={counsellorName} />
      <div className="mb-6 grid grid-cols-2 gap-3 lg:grid-cols-4">
        <StatTile label="Applications" value={b.applications.length} hint={`${active.length} in progress`} />
        <StatTile label="Submitted" value={b.applications.filter((a) => a.status === 'submitted' || a.status === 'decision').length} />
        <StatTile label="Offers" value={offers.length} hint={offers.map((o) => getUniversity(o.universityId)?.shortName).join(', ') || 'None yet'} />
        <StatTile label="Open items" value={openItems} hint={flags.length ? `${flags.length} risk flag${flags.length === 1 ? '' : 's'}` : 'No risk flags'} />
      </div>

      <div className="grid grid-cols-[minmax(0,1fr)] gap-6 lg:grid-cols-[minmax(0,1fr)_340px]">
        <div className="space-y-6">
          {flags.length > 0 && (
            <Card className="border-danger-600/30 bg-danger-50/40">
              <CardBody className="space-y-2">
                {flags.map((f, i) => (
                  <Link key={i} href={`/student/applications/${f.app.id}`} className="flex items-start gap-2 text-sm hover:underline">
                    <AlertTriangle className={f.severity === 'high' ? 'mt-0.5 size-4 text-danger-600' : 'mt-0.5 size-4 text-warning-600'} />
                    <span><span className="font-medium text-ink">{getUniversity(f.app.universityId)?.shortName}:</span> <span className="text-muted">{f.text}</span></span>
                  </Link>
                ))}
              </CardBody>
            </Card>
          )}
          <section>
            <h2 className="mb-3 text-base font-semibold text-ink">Application progress</h2>
            <div className="space-y-3">
              {active.slice(0, 3).map((a) => {
                const u = getUniversity(a.universityId);
                const days = daysUntil(a.deadline, DEMO_NOW);
                const pct = progress(a);
                return (
                  <Link key={a.id} href={`/student/applications/${a.id}`} className="block">
                    <Card className="p-4 transition-colors hover:border-brand-300">
                      <div className="flex items-start justify-between gap-3">
                        <div className="flex min-w-0 items-center gap-3">
                          {u && <UniMark uni={u} size="sm" />}
                          <div className="min-w-0">
                            <p className="truncate font-semibold text-ink">{u?.shortName} · {programmeOf(u, a.programmeId)?.name}</p>
                            <p className="text-xs text-subtle">Deadline {fmtDate(a.deadline)}</p>
                          </div>
                        </div>
                        <DaysLeft days={days} />
                      </div>
                      <div className="mt-3 flex items-center gap-3">
                        <Progress value={pct} tone={days < 14 && pct < 1 ? 'danger' : 'brand'} />
                        <span className="w-10 text-right text-xs font-medium text-muted">{Math.round(pct * 100)}%</span>
                      </div>
                      <div className="mt-2 flex flex-wrap items-center gap-2 text-xs">
                        <StatusBadge status={a.status} /><FitBadge band={a.fitGroup} />
                        <span className="text-muted">Next: {nextStep(a, cFirst)}</span>
                      </div>
                    </Card>
                  </Link>
                );
              })}
            </div>
            <Link href="/student/applications/board" className="mt-3 inline-block text-sm font-medium text-brand-700 hover:underline">All {b.applications.length} applications ›</Link>
          </section>
        </div>

        <div className="space-y-6">
          <Card className="border-success-600/30 bg-success-50/50">
            <CardHeader title="Next meeting" />
            <CardBody className="pt-2 text-sm">
              {nextMeeting ? (
                <>
                  <p className="text-ink">{new Intl.DateTimeFormat('en-IN', { weekday: 'short', day: 'numeric', month: 'short', hour: 'numeric', minute: '2-digit', timeZone: 'Asia/Kolkata' }).format(new Date(nextMeeting.startUtc))} · {firstName(nextMeeting.hostId)}</p>
                  <p className="text-muted">Topic: {nextMeeting.focus ?? nextMeeting.title}</p>
                  <Link href="/student/sessions" className={buttonVariants({ size: 'sm', className: 'mt-3' })}>Open in Sessions</Link>
                </>
              ) : (
                <>
                  <p className="text-muted">Nothing booked with {cFirst} yet.</p>
                  <Link href="/student/sessions" className={buttonVariants({ size: 'sm', variant: 'secondary', className: 'mt-3' })}>Book a session</Link>
                </>
              )}
            </CardBody>
          </Card>
          <Card>
            <CardHeader title={<>To-do <span className="text-sm font-normal text-muted">from {cFirst}</span></>} description={meeting ? `From your meeting on ${fmtDate(meeting.date)}` : undefined} />
            <CardBody className="pt-2">
              {todos.length === 0 ? <p className="text-sm text-muted">No open to-dos.</p> : (
                <ul className="divide-y divide-line">
                  {todos.map((t) => (
                    <li key={t.id} className="flex items-start gap-3 py-2.5 text-sm">
                      <form action={toggleActionItem.bind(null, meeting!.id, t.id)}>
                        <button aria-label={t.done ? 'Mark not done' : 'Mark done'} className={`mt-0.5 flex size-4 items-center justify-center rounded border ${t.done ? 'border-brand-600 bg-brand-600 text-white' : 'border-line bg-surface'}`}>{t.done ? '✓' : ''}</button>
                      </form>
                      <div className="min-w-0 flex-1">
                        <p className={t.done ? 'text-subtle line-through' : 'text-ink'}>{t.title}</p>
                        <p className="text-xs text-subtle">Due {fmtDate(t.dueOn)}{t.taskId ? ' · in your timetable' : ''}</p>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
              {meeting && untasked > 0 && (
                <div className="mt-3"><ActionButton size="sm" variant="secondary" action={actionItemsToTasks.bind(null, meeting.id)} done="Added to timetable ✓">Add {untasked} to my timetable</ActionButton></div>
              )}
            </CardBody>
          </Card>
        </div>
      </div>
    </>
  );
}
