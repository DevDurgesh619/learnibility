import { BadgeCheck, CalendarClock, CircleDollarSign, Clock, Info, ShieldCheck, Star, Wallet } from 'lucide-react';
import { approvePaidTutor, declinePaidTutor } from '@/lib/actions/parent';
import { paidTutorDecision } from '@/components/parent/attention';
import { ChildSwitcher } from '@/components/parent/child-switcher';
import { param, parentContext, type SearchParams } from '@/components/parent/context';
import { fmtDateYear, plural } from '@/components/parent/format';
import { NoChild } from '@/components/parent/no-child';
import { Notice } from '@/components/parent/notice';
import { Avatar, Badge, Button, Card, CardBody, CardFooter, CardHeader, EmptyState, GapBadge, PageHeader, StatTile, Table, TBody, TD, TH, THead, TR } from '@/components/ui';
import { getCurrentPlan, getGaps, getSubject, getSubtopic, getTutor, getTutorMatches, type Booking } from '@/lib/data';
import { formatHours, formatInr } from '@/lib/format';

const inrRange = (r: { min: number; max: number }) => (r.max === 0 ? 'Free' : r.min === r.max ? formatInr(r.min) : `${formatInr(r.min)}–${formatInr(r.max)}`);

export default async function ParentPlan({ searchParams }: { searchParams: SearchParams }) {
  const sp = await searchParams;
  const { children, child } = await parentContext(searchParams);
  if (!child) return (<><PageHeader eyebrow="Parent" title="Plan and spend" /><NoChild /></>);
  const s = child.student;
  const record = getCurrentPlan(s.id);
  const gaps = getGaps(s.id, { status: 'open' });
  const gapById = new Map(gaps.map((g) => [g.id, g]));
  const decision = paidTutorDecision(s.id);
  const plan = record?.plan;
  const chapters = new Set(gaps.map((g) => g.chapterId)).size;
  const weeks = record?.freePlanWeeks ?? 0;
  // Subject the paid help is for: the one carrying the most open hours.
  const bySubject = new Map<string, number>();
  for (const g of gaps) bySubject.set(g.subjectId, (bySubject.get(g.subjectId) ?? 0) + g.hoursToClose);
  const mainSubject = [...bySubject.entries()].sort((a, b) => b[1] - a[1])[0]?.[0];
  const matches = decision.ruleFired && !decision.approved.length && !decision.pending.length ? getTutorMatches(s.id, { subjectId: mainSubject, limit: 3 }) : [];
  const done = param(sp, 'done');
  const freeHours = gaps.reduce((a, g) => a + g.hoursToClose, 0);

  return (
    <>
      <PageHeader eyebrow="Parent" title="Plan and spend" description={`What each of ${s.firstName}'s gaps costs in time and rupees, and any paid help waiting for you.`} />
      <ChildSwitcher children={children} selectedId={s.id} basePath="/parent/plan" />
      {done === 'approved' && <Notice>Approved. The tutor has the request now, and {s.firstName} can see the booking in their tutors. You&apos;ll get an invoice after the first session.</Notice>}
      {done === 'declined' && <Notice>Declined. {s.firstName} stays on the free plan, and the request is closed.</Notice>}

      <section className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatTile label="Open gaps" value={gaps.length} icon={<Info />} hint={`across ${plural(chapters, 'chapter')}`} />
        <StatTile label="Time to close" value={formatHours(freeHours)} icon={<Clock />} hint={`About ${s.weeklyHours} h a week`} />
        <StatTile label="Free plan running" value={plural(weeks, 'week')} icon={<CalendarClock />} hint={record ? `Since ${fmtDateYear(record.createdUtc)}` : 'No plan yet'} />
        <StatTile label="Monthly cost now" value={plan ? inrRange(plan.totalInrPerMonth) : '—'} icon={<Wallet />} hint="Free methods first" />
      </section>

      {(decision.ruleFired || decision.pending.length > 0 || decision.approved.length > 0) && (
        <Card className="mb-6 border-warning-600/30">
          <CardHeader title={decision.pending.length ? 'A paid tutor needs your approval' : decision.approved.length ? 'Paid tutor approved' : 'Why a paid tutor is suggested'} description="Learnibility suggests paid tuition only when free methods have had a fair try." />
          <CardBody className="space-y-5">
            <div className="grid gap-3 sm:grid-cols-2">
              <RuleCheck ok={chapters >= 2} title="Gaps span 2 or more chapters" detail={`${s.firstName} has open gaps in ${plural(chapters, 'chapter')}.`} />
              <RuleCheck ok={weeks >= 3} title="Free plan has run 3 weeks" detail={`The current free plan has run ${plural(weeks, 'week')} without closing them.`} />
            </div>
            {decision.reason && <p className="rounded-lg bg-surface-muted px-4 py-3 text-sm text-ink">{decision.reason}</p>}

            {plan && <p className="text-sm text-muted">Typical cost: {inrRange(plan.paidTuition.inrPerMonth)} a month. {plan.paidTuition.affordable ? 'This fits the budget you gave us.' : 'This is above the budget you gave us, so compare tutors carefully.'}</p>}
            {decision.pending.map((b) => <BookingDecision key={b.id} booking={b} learnerId={s.id} />)}
            {decision.approved.map((b) => <ApprovedBooking key={b.id} booking={b} highlight={param(sp, 'booking') === b.id} />)}

            {matches.length > 0 && (
              <div>
                <p className="mb-3 text-sm font-medium text-ink">Tutors matched to {s.firstName}&apos;s gaps</p>
                <div className="grid gap-4 lg:grid-cols-3">
                  {matches.map((m, i) => {
                    const t = getTutor(m.tutorId);
                    return (
                      <Card key={m.tutorId} className={i === 0 ? 'ring-2 ring-brand-200' : ''}>
                        <CardBody className="space-y-3">
                          <div className="flex items-center gap-3">
                            <Avatar name={m.name} />
                            <div className="min-w-0"><p className="font-medium text-ink">{m.name}</p><p className="flex items-center gap-1 text-xs text-muted"><Star className="size-3 fill-warning-500 text-warning-500" />{t?.rating ?? '—'} · {t?.reviewsCount ?? 0} reviews · {t?.yearsExperience ?? 0} yrs</p></div>
                          </div>
                          {i === 0 && <Badge tone="brand">Best match</Badge>}
                          <p className="text-sm text-muted">{m.reason}</p>
                          <p className="text-sm text-ink"><span className="font-semibold">{formatInr(m.pricePerHourInr)}</span> an hour · {t?.sessionMinutes ?? 60} min sessions</p>
                          <form action={approvePaidTutor} className="space-y-2">
                            <input type="hidden" name="learnerId" value={s.id} />
                            <input type="hidden" name="tutorId" value={m.tutorId} />
                            {mainSubject && <input type="hidden" name="subjectId" value={mainSubject} />}
                            <input type="hidden" name="matchReason" value={m.reason} />
                            <input type="hidden" name="topic" value={gaps.filter((g) => g.subjectId === mainSubject).slice(0, 3).map((g) => getSubtopic(g.subtopicId)?.name ?? '').filter(Boolean).join(', ')} />
                            <label className="block text-xs text-muted">Sessions a week
                              <select name="sessionsPerWeek" defaultValue="2" className="mt-1 block w-full rounded-lg border border-line bg-surface px-2 py-1.5 text-sm text-ink">
                                <option value="1">1 a week (~{formatInr(Math.round(m.pricePerHourInr * ((t?.sessionMinutes ?? 60) / 60) * 4))}/month)</option>
                                <option value="2">2 a week (~{formatInr(Math.round(m.pricePerHourInr * ((t?.sessionMinutes ?? 60) / 60) * 8))}/month)</option>
                              </select>
                            </label>
                            <Button type="submit" className="w-full" variant={i === 0 ? 'primary' : 'secondary'}><BadgeCheck />Approve and book</Button>
                          </form>
                        </CardBody>
                      </Card>
                    );
                  })}
                </div>
              </div>
            )}
          </CardBody>
        </Card>
      )}

      <Card>
        <CardHeader title={`${s.firstName}'s plan, gap by gap`} description={plan?.orderOfOperations ?? 'Prerequisite gaps first, then the biggest.'} />
        {plan && plan.gaps.length ? (
          <>
            <div className="hidden md:block">
              <Table className="mt-4">
                <THead><TR><TH>Gap</TH><TH>Method</TH><TH>Hours</TH><TH>Weeks</TH><TH>Cost a month</TH><TH>Re-test</TH></TR></THead>
                <TBody>
                  {plan.gaps.map((gp) => {
                    const g = gapById.get(gp.gapId);
                    const step = gp.steps[0];
                    return (
                      <TR key={gp.gapId}>
                        <TD><p className="font-medium text-ink">{getSubtopic(gp.subtopicId)?.name ?? gp.subtopicId}</p><div className="mt-1 flex items-center gap-2"><GapBadge code={gp.code} /><span className="text-xs text-subtle">{g ? getSubject(g.subjectId)?.subject.name : ''}</span></div></TD>
                        <TD className="max-w-xs"><p className="text-ink">{step?.name ?? '—'}</p><p className="text-xs text-muted">{step?.timeCost}{gp.addOns.length ? ` · plus ${gp.addOns.map((a) => a.name).join(', ')}` : ''}</p></TD>
                        <TD>{formatHours(gp.hours)}</TD>
                        <TD>{gp.weeks ?? '—'}</TD>
                        <TD>{inrRange(step?.inrPerMonth ?? { min: 0, max: 0 })}</TD>
                        <TD className="text-xs text-muted">{fmtDateYear(gp.retestDateUtc)}</TD>
                      </TR>
                    );
                  })}
                </TBody>
              </Table>
            </div>
            <ul className="divide-y divide-line md:hidden">
              {plan.gaps.map((gp) => (
                <li key={gp.gapId} className="space-y-1 px-5 py-4">
                  <div className="flex items-start justify-between gap-2"><p className="font-medium text-ink">{getSubtopic(gp.subtopicId)?.name ?? gp.subtopicId}</p><GapBadge code={gp.code} /></div>
                  <p className="text-sm text-ink">{gp.steps[0]?.name}</p>
                  <p className="text-xs text-muted">{formatHours(gp.hours)} · {gp.weeks ?? '—'} weeks · {inrRange(gp.steps[0]?.inrPerMonth ?? { min: 0, max: 0 })} · re-test {fmtDateYear(gp.retestDateUtc)}</p>
                </li>
              ))}
            </ul>
            <CardFooter className="flex-wrap text-muted"><CircleDollarSign className="size-4" />{plan.gaps[0]?.moneyCheck}</CardFooter>
          </>
        ) : <CardBody><EmptyState className="border-0" title="No plan yet" description={`A plan appears after ${s.firstName}'s first test finds a gap.`} /></CardBody>}
      </Card>
    </>
  );
}

function RuleCheck({ ok, title, detail }: { ok: boolean; title: string; detail: string }) {
  return (
    <div className={`flex items-start gap-3 rounded-lg border px-4 py-3 ${ok ? 'border-warning-600/30 bg-warning-50' : 'border-line bg-surface'}`}>
      <ShieldCheck className={`mt-0.5 size-4 shrink-0 ${ok ? 'text-warning-700' : 'text-subtle'}`} />
      <div><p className="text-sm font-medium text-ink">{title} {ok ? '· met' : '· not yet'}</p><p className="text-xs text-muted">{detail}</p></div>
    </div>
  );
}

function BookingDecision({ booking, learnerId }: { booking: Booking; learnerId: string }) {
  const t = getTutor(booking.tutorId);
  const monthly = Math.round(booking.priceInr * (booking.minutes / 60) * (booking.sessionsPerWeek ?? 1) * 4);
  return (
    <div className="rounded-lg border border-line p-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-3"><Avatar name={t?.displayName ?? booking.tutorId} /><div><p className="font-medium text-ink">{t?.displayName ?? booking.tutorId}</p><p className="text-sm text-muted">{formatInr(booking.priceInr)}/h · {booking.sessionsPerWeek ?? 1} a week · about {formatInr(monthly)} a month</p></div></div>
        <Badge tone="warning" className="w-fit">Waiting for you</Badge>
      </div>
      {booking.matchReason && <p className="mt-3 text-sm text-muted">{booking.matchReason}</p>}
      <div className="mt-4 flex flex-wrap gap-2">
        <form action={approvePaidTutor}><input type="hidden" name="learnerId" value={learnerId} /><input type="hidden" name="bookingId" value={booking.id} /><Button type="submit"><BadgeCheck />Approve</Button></form>
        <form action={declinePaidTutor}><input type="hidden" name="learnerId" value={learnerId} /><input type="hidden" name="bookingId" value={booking.id} /><Button type="submit" variant="secondary">Decline</Button></form>
      </div>
    </div>
  );
}

function ApprovedBooking({ booking, highlight }: { booking: Booking; highlight: boolean }) {
  const t = getTutor(booking.tutorId);
  const status = { requested: 'Waiting for the tutor to accept', accepted: 'Accepted', active: 'Sessions running', completed: 'Completed', declined: 'Tutor declined', cancelled: 'Cancelled' }[booking.status];
  return (
    <div className={`flex flex-col gap-3 rounded-lg border p-4 sm:flex-row sm:items-center sm:justify-between ${highlight ? 'border-success-600/30 bg-success-50' : 'border-line'}`}>
      <div className="flex items-center gap-3"><Avatar name={t?.displayName ?? booking.tutorId} /><div><p className="font-medium text-ink">{t?.displayName ?? booking.tutorId}</p><p className="text-sm text-muted">{formatInr(booking.priceInr)}/h · {booking.sessionsPerWeek ?? 1} a week{booking.parentApproval?.utc ? ` · approved ${fmtDateYear(booking.parentApproval.utc)}` : ''}</p></div></div>
      <Badge tone={booking.status === 'requested' ? 'info' : 'success'} className="w-fit">{status}</Badge>
    </div>
  );
}
