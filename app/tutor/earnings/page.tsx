import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { AlertTriangle } from 'lucide-react';
import { BarChart } from '@/components/charts';
import { Delta, SectionTitle, Stat } from '@/components/tutor/bits';
import { earningRows, loadWorkspace, money, nextPayoutDate } from '@/components/tutor/model';
import { formatDay } from '@/components/marketplace/dates';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { addDaysLocal, demoToday, localDateOf, weekStartOf } from '@/lib/data';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Earnings · Tutor' };

const monthLabel = (m: string) => new Intl.DateTimeFormat('en-IN', { month: 'long', year: 'numeric', timeZone: 'UTC' }).format(new Date(`${m}-01T00:00:00Z`));
const prevMonth = (m: string) => { const d = new Date(`${m}-01T00:00:00Z`); d.setUTCMonth(d.getUTCMonth() - 1); return d.toISOString().slice(0, 7); };

/** Tutor HTML 7a: this month, pending, paid, next payout, activity, weekly chart, and the held-earnings line. */
export default async function EarningsPage({ searchParams }: { searchParams: Promise<{ month?: string }> }) {
  const sp = await searchParams;
  const persona = (await currentPersona())!;
  const ws = loadWorkspace(persona.id);
  if (!ws) notFound();
  const rows = earningRows(ws);
  const months = [...new Set(rows.map((r) => localDateOf(r.session.startUtc).slice(0, 7)))].sort().reverse();
  const month = sp.month && months.includes(sp.month) ? sp.month : demoToday().slice(0, 7);
  const inMonth = (m: string) => rows.filter((r) => localDateOf(r.session.startUtc).startsWith(m));
  const cur = inMonth(month);
  const sum = (xs: typeof rows) => xs.reduce((a, r) => a + r.netInr, 0);
  const total = sum(cur);
  // Mid-month, compare with the same days of the previous month so the change is fair.
  const isCurrent = month === demoToday().slice(0, 7);
  const cutDay = demoToday().slice(8);
  const last = sum(inMonth(prevMonth(month)).filter((r) => !isCurrent || localDateOf(r.session.startUtc).slice(8) <= cutDay));
  const change = last ? Math.round(((total - last) / last) * 100) : null;
  const pending = rows.filter((r) => r.status === 'pending');
  const held = rows.filter((r) => r.status === 'report_missing');
  const taught = cur.filter((r) => r.status !== 'free');
  const hours = taught.reduce((a, r) => a + r.session.minutes, 0) / 60;
  const gross = taught.reduce((a, r) => a + r.grossInr, 0);
  const demos = ws.bookings.filter((b) => b.kind === 'demo' && ['accepted', 'active', 'completed'].includes(b.status));
  const converted = demos.filter((b) => ws.sessions.some((s) => s.kind !== 'demo' && (s.learnerIds ?? [s.learnerId]).includes(b.learnerId))).length;

  const thisWeek = weekStartOf(demoToday());
  const weeks = Array.from({ length: 8 }, (_, i) => addDaysLocal(thisWeek, -7 * (7 - i)));
  const chart = weeks.map((w) => ({ x: formatDay(w).split(', ')[1] ?? w, earned: rows.filter((r) => { const d = localDateOf(r.session.startUtc); return d >= w && d < addDaysLocal(w, 7); }).reduce((a, r) => a + r.netInr, 0) }));

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center gap-2">
        {months.slice(0, 4).map((m) => <Link key={m} href={m === demoToday().slice(0, 7) ? '/tutor/earnings' : `/tutor/earnings?month=${m}`} aria-current={m === month ? 'page' : undefined} className={buttonVariants({ size: 'sm', variant: m === month ? 'primary' : 'secondary' })}>{monthLabel(m)}</Link>)}
      </div>

      {held.length > 0 && (
        <div className="flex flex-col gap-3 rounded-lg border border-warning-600/20 bg-warning-50 p-4 sm:flex-row sm:items-center">
          <AlertTriangle className="size-5 shrink-0 text-warning-600" />
          <p className="flex-1 text-sm text-warning-700">{held.length} session {held.length === 1 ? 'report' : 'reports'} missing · {held.map((r) => `${r.who} ${r.session.code ?? ''}`.trim()).join(', ')} · {money(sum(held))} held until filed</p>
          <Link href={`/tutor/sessions/${held[0]!.session.id}/report`} className={buttonVariants({ size: 'sm' })}>Write report</Link>
        </div>
      )}

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <Stat label={monthLabel(month)} value={money(total)} hint={<span className="inline-flex items-center gap-1"><Delta value={change} /> vs {isCurrent ? `1–${Number(cutDay)} ` : ''}{monthLabel(prevMonth(month)).split(' ')[0]}</span>} />
        <Stat label="Pending" value={money(sum(pending))} hint="clears after reports" href="/tutor/earnings/transactions?pending=1" />
        <Stat label="Paid this month" value={money(sum(cur.filter((r) => r.status === 'paid')))} />
        <Stat label="Next payout" value={money(sum(pending))} hint={formatDay(nextPayoutDate())} />
        <Stat label="Sessions completed" value={taught.length} />
        <Stat label="Hours taught" value={hours.toFixed(1)} />
        <Stat label="Avg rate" value={hours ? `${money(gross / hours)} / hr` : '—'} hint="before the 15% fee" />
        <Stat label="Demos → paid" value={`${converted} / ${demos.length}`} />
      </div>

      <Card><CardBody>
        <SectionTitle>Weekly earnings · last 8 weeks</SectionTitle>
        {chart.some((c) => c.earned > 0) ? <BarChart data={chart} series={[{ key: 'earned', label: 'You get' }]} format="inr" height={240} /> : <p className="py-10 text-center text-sm text-muted">No paid sessions in the last 8 weeks.</p>}
        <p className="mt-2 text-xs text-subtle">After the platform fee ({Math.round((ws.tutor.platformFeeRate ?? 0.15) * 100)}%). Payouts every Monday for sessions with a filed report.</p>
      </CardBody></Card>
    </div>
  );
}
