import Link from 'next/link';
import { CheckCircle2, Sparkles } from 'lucide-react';
import { Delta, SectionTitle } from '@/components/tutor/bits';
import { aiFocus, openGapsFor, scoreSeries, sessionsFor, studentContext, topicCards } from '@/components/tutor/model';
import { formatDay, formatTime } from '@/components/marketplace/dates';
import { GapBadge } from '@/components/ui/badge';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { getGaps, getSubject, namesFor } from '@/lib/data';
import { currentPersona } from '@/lib/session';

/** 4a Overview: the student snapshot a tutor reads in 10 seconds. */
export default async function Overview({ params }: { params: Promise<{ learnerId: string }> }) {
  const { learnerId } = await params;
  const { ws, row } = studentContext((await currentPersona())!.id, learnerId)!;
  const subjectId = row.subjectIds[0];
  const names = namesFor(row.subjectIds);
  const open = openGapsFor(learnerId, row.subjectIds).sort((a, b) => b.hoursToClose - a.hoursToClose);
  const closed = getGaps(learnerId, { status: 'closed' }).filter((g) => row.subjectIds.includes(g.subjectId)).slice(0, 3);
  const booking = ws.bookings.filter((b) => b.learnerId === learnerId).sort((a, b) => a.requestedAt.localeCompare(b.requestedAt))[0];
  const ref = row.nextSession ?? sessionsFor(ws, learnerId).at(-1);
  const focus = ref ? aiFocus(ws, ref) : undefined;
  const last = sessionsFor(ws, learnerId).filter((s) => s.report).at(-1);
  const cards = subjectId ? topicCards(learnerId, subjectId) : [];
  const tested = cards.filter((c) => c.pct !== null);
  const mastery = tested.length ? Math.round(tested.reduce((s, c) => s + c.pct!, 0) / tested.length) : null;
  const scores = scoreSeries(ws, learnerId);
  const asg = ws.assignments.filter((a) => a.learnerId === learnerId);
  const pending = asg.filter((a) => ['assigned', 'in_progress', 'overdue', 'submitted', 'ai_evaluated'].includes(a.status)).length;
  const closedHours = closed.reduce((s, g) => s + g.hoursToClose, 0);
  const totalGaps = open.length + getGaps(learnerId, { status: 'closed' }).filter((g) => row.subjectIds.includes(g.subjectId)).length;
  const planPct = totalGaps && totalGaps > open.length ? Math.round(((totalGaps - open.length) / totalGaps) * 100) : cards.length ? Math.round((cards.filter((c) => c.state === 'strong' || c.state === 'medium').length / cards.length) * 100) : 0;

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1.3fr_1fr]">
      <div className="space-y-6">
        <Card>
          <CardHeader title={`Why ${row.name.split(' ')[0]} is here`} />
          <CardBody className="space-y-3 pt-3 text-sm">
            <p className="text-ink">{booking?.topic ?? `Improve ${subjectId ? getSubject(subjectId)?.subject.name : 'their subject'}${row.goal ? ` and prepare for ${row.goal}` : ''}.`}</p>
            <div>
              <p className="mb-1.5 text-xs font-medium uppercase tracking-wide text-muted">Gaps in your subjects</p>
              {open.length === 0 && closed.length === 0 ? <p className="text-muted">No diagnosed gaps yet. Assign a test to find them.</p> : (
                <ul className="flex flex-wrap gap-2">
                  {open.slice(0, 5).map((g) => <li key={g.id} className="flex items-center gap-1.5 rounded-lg border border-line px-2 py-1"><span className="text-ink">{names[g.subtopicId]?.split(/[:;,]/)[0]}</span><GapBadge code={g.code} /></li>)}
                  {closed.map((g) => <li key={g.id} className="flex items-center gap-1 rounded-lg border border-success-600/20 bg-success-50 px-2 py-1 text-success-700"><CheckCircle2 className="size-3.5" />{names[g.subtopicId]?.split(/[:;,]/)[0]}</li>)}
                </ul>
              )}
            </div>
          </CardBody>
        </Card>
        <Card className="border-brand-200 bg-brand-50/40">
          <CardHeader title={<span className="flex items-center gap-1.5"><Sparkles className="size-4 text-brand-600" />AI recommendation</span>} />
          <CardBody className="pt-2 text-sm text-ink">
            {focus ? <p>Focus on <span className="font-medium">{focus.line}</span> next ({focus.source}).{last?.report && last.report.performance !== 'confident' ? ` Last session (${last.code}) they were ${last.report.performance === 'struggled' ? 'struggling' : 'getting there'}: “${last.report.notes}”` : ''}</p> : <p>Run a first session to build a plan.</p>}
            {row.nextSession && <Link href={`/tutor/sessions/${row.nextSession.id}/prep`} className={buttonVariants({ size: 'sm', className: 'mt-3' })}>Prepare next session</Link>}
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Topic mastery" description={subjectId ? getSubject(subjectId)?.subject.name : undefined} action={<Link href={`/tutor/students/${learnerId}/learning`} className="text-sm text-brand-700 hover:underline">All topics</Link>} />
          <CardBody className="space-y-2.5 pt-3">
            {tested.length === 0 && <p className="text-sm text-muted">No platform tests in your subject yet.</p>}
            {tested.slice(-6).map((c) => (
              <div key={c.chapterId} className="flex items-center gap-3 text-sm">
                <span className="w-48 truncate text-ink" title={c.name}>{c.name}</span>
                <Progress value={(c.pct ?? 0) / 100} tone={c.state === 'strong' ? 'success' : c.state === 'medium' ? 'warning' : 'danger'} />
                <span className="w-10 text-right text-muted">{c.pct}%</span>
              </div>
            ))}
          </CardBody>
        </Card>
      </div>
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-3">
          <Tile label="Avg test score" value={row.avgScorePct !== null ? `${row.avgScorePct}%` : '—'} extra={<Delta value={row.progressDelta} />} />
          <Tile label="Subject mastery" value={mastery !== null ? `${mastery}%` : '—'} />
          <Tile label="Sessions done" value={row.sessionsDone} extra={<span className="text-xs text-muted">{row.attendancePct ?? 100}% attended</span>} />
          <Tile label="Assignments" value={asg.length} extra={<span className="text-xs text-muted">{pending} pending</span>} />
        </div>
        <Card className="p-4">
          <p className="text-sm text-muted">Overall progress</p>
          <p className="mt-1 text-lg font-semibold text-ink">{planPct}% of plan</p>
          <Progress value={planPct / 100} className="mt-2" />
          <p className="mt-2 text-xs text-muted">{open.length} open {open.length === 1 ? 'gap' : 'gaps'} in your subjects{closedHours ? ` · ${closed.length} closed recently` : ''}</p>
          <p className="mt-3 text-sm text-ink">Next session: {row.nextSession ? `${formatDay(row.nextSession.startUtc)}, ${formatTime(row.nextSession.startUtc)}` : 'not scheduled'}</p>
        </Card>
        <Card className="p-4">
          <SectionTitle className="mb-2">Recent scores</SectionTitle>
          {scores.length === 0 ? <p className="text-sm text-muted">No scores yet.</p> : (
            <ul className="space-y-1.5 text-sm">
              {scores.slice(-5).reverse().map((s) => <li key={s.id} className="flex justify-between gap-3"><span className="truncate text-ink">{s.title}</span><span className="text-muted">{s.pct}%</span></li>)}
            </ul>
          )}
        </Card>
      </div>
    </div>
  );
}

function Tile({ label, value, extra }: { label: string; value: React.ReactNode; extra?: React.ReactNode }) {
  return <Card className="p-4"><p className="text-sm text-muted">{label}</p><p className="mt-1 text-2xl font-semibold text-ink">{value}</p>{extra}</Card>;
}
