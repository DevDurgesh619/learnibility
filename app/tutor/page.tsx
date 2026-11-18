import type { Metadata } from 'next';
import { cookies } from 'next/headers';
import Link from 'next/link';
import { CheckCircle2, Eye, Inbox, Share2, Star } from 'lucide-react';
import { TUTOR_HOME_COOKIE } from '@/components/tutor/constants';
import { NeedsAttention, NextSessionCard, QuickActions, RequestRow, RestOfToday, ReviewQueue } from '@/components/tutor/home/parts';
import { earningRows, money, needsAttention, isUpcoming, loadWorkspace, requests, reviewQueue, sessionsOn, studentRows, todayItems } from '@/components/tutor/model';
import { formatDay } from '@/components/marketplace/dates';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { demoNow, demoToday, getTasks, localDateOf } from '@/lib/data';
import { setHomeLayout } from '@/lib/actions/tutor';
import { currentPersona } from '@/lib/session';
import { cn } from '@/lib/utils';

export const metadata: Metadata = { title: 'Home · Tutor · Learnibility' };

export default async function TutorHome({ searchParams }: { searchParams: Promise<{ home?: string }> }) {
  const persona = (await currentPersona())!;
  const ws = loadWorkspace(persona.id);
  const sp = await searchParams;
  const layout = sp.home === 'a' || sp.home === 'b' ? sp.home : (await cookies()).get(TUTOR_HOME_COOKIE)?.value === 'b' ? 'b' : 'a';
  const now = new Date(demoNow());
  const first = persona.name.split(' ')[0];
  const hour = Number(new Intl.DateTimeFormat('en-IN', { hour: 'numeric', hour12: false, timeZone: 'Asia/Kolkata' }).format(now));
  const greet = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';

  if (!ws || (ws.students.length === 0 && ws.bookings.length === 0)) return <FirstDay name={first} verified={ws?.tutor.verified ?? false} profilePct={ws?.tutor.profileStrengthPct ?? 60} />;

  const rows = studentRows(ws);
  const attention = needsAttention(rows);
  const queue = reviewQueue(ws);
  const reqs = requests(ws);
  const today = todayItems(ws);
  const todaySessions = sessionsOn(ws, demoToday());
  const next = ws.sessions.filter((s) => isUpcoming(s)).sort((a, b) => a.startUtc.localeCompare(b.startUtc))[0];
  const tasksDue = ws.students.reduce((n, s) => n + getTasks(s.learnerId, demoToday(), { createdBy: ws.tutor.id, status: 'todo' }).length, 0);
  const month = demoToday().slice(0, 7);
  const thisMonth = { netInr: earningRows(ws).filter((r) => localDateOf(r.session.startUtc).startsWith(month)).reduce((a, r) => a + r.netInr, 0) };

  return (
    <>
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-ink">{greet}, {first}</h1>
          <p className="mt-1 text-sm text-muted">
            {formatDay(demoNow())} · {todaySessions.length} {todaySessions.length === 1 ? 'session' : 'sessions'}
            {layout === 'a' ? ` · ${queue.length} ${queue.length === 1 ? 'review' : 'reviews'} · ${tasksDue} student ${tasksDue === 1 ? 'task' : 'tasks'} due` : ` · ${money(thisMonth?.netInr ?? 0)} this month`}
          </p>
        </div>
        <LayoutToggle layout={layout} />
      </div>

      {layout === 'a' ? (
        <div className="space-y-6">
          {reqs.length > 0 && (
            <Link href={`/tutor/requests/${reqs[0]!.id}`} className="flex items-center gap-3 rounded-[var(--radius-card)] border border-warning-600/30 bg-warning-50 px-4 py-3 text-sm text-warning-700 hover:border-warning-600/60">
              <Inbox className="size-4 shrink-0" />
              <span className="flex-1"><span className="font-medium">{reqs.length} new student {reqs.length === 1 ? 'request' : 'requests'}.</span> Respond within 24 h to keep your response badge.</span>
              <span className="font-medium">Open</span>
            </Link>
          )}
          <div className="grid gap-6 lg:grid-cols-[1.2fr_1fr]">
            <NextSessionCard ws={ws} s={next} now={now} />
            <NeedsAttention rows={attention} />
          </div>
          <div className="grid gap-6 lg:grid-cols-2">
            <ReviewQueue ws={ws} queue={queue} />
            <RestOfToday items={today} />
          </div>
          <div><p className="mb-2 text-sm font-medium text-muted">Quick actions</p><QuickActions /></div>
        </div>
      ) : (
        <div className="space-y-6">
          <Card>
            <CardHeader title={reqs.length ? `${reqs.length} new student ${reqs.length === 1 ? 'request' : 'requests'}` : 'Student requests'} description="Respond within 24 h to keep your response badge" />
            <CardBody className="pt-2">
              {reqs.length === 0 ? <p className="text-sm text-muted">No open requests. Share your profile link to get more.</p> : (
                <ul className="divide-y divide-line">{reqs.map((b) => <RequestRow key={b.id} ws={ws} b={b} />)}</ul>
              )}
            </CardBody>
          </Card>
          <div className="grid gap-6 lg:grid-cols-3">
            <NextSessionCard ws={ws} s={next} now={now} compact />
            <NeedsAttention rows={attention} compact />
            <Card className="p-5">
              <p className="text-sm text-muted">Rating</p>
              <p className="mt-1 flex items-center gap-1.5 text-2xl font-semibold text-ink"><Star className="size-5 fill-amber-400 text-amber-400" />{ws.tutor.rating.toFixed(1)}</p>
              <p className="text-sm text-muted">{ws.tutor.reviewsCount} reviews · {ws.tutor.rebookPct}% rebook</p>
              <p className="mt-3 text-sm text-muted">This month <span className="font-medium text-ink">{money(thisMonth?.netInr ?? 0)}</span> after fees</p>
            </Card>
          </div>
          <div><p className="mb-2 text-sm font-medium text-muted">Quick actions</p><QuickActions share /></div>
        </div>
      )}
    </>
  );
}

function LayoutToggle({ layout }: { layout: 'a' | 'b' }) {
  return (
    <form action={setHomeLayout} className="flex items-center gap-2 self-start sm:self-auto">
      <span className="text-xs text-muted">Home layout</span>
      <div className="inline-flex rounded-lg border border-line bg-surface p-0.5" role="group" aria-label="Home layout">
        {(['a', 'b'] as const).map((v) => (
          <button key={v} name="layout" value={v} aria-pressed={layout === v}
            className={cn('rounded-md px-2.5 py-1 text-xs font-medium', layout === v ? 'bg-brand-600 text-white' : 'text-muted hover:text-ink')}>
            {v === 'a' ? 'Teaching first' : 'Requests first'}
          </button>
        ))}
      </div>
    </form>
  );
}

/** 2d: a fresh tutor with no students yet. */
function FirstDay({ name, verified, profilePct }: { name: string; verified: boolean; profilePct: number }) {
  return (
    <>
      <h1 className="text-2xl font-semibold tracking-tight text-ink">Welcome, {name}</h1>
      <div className={cn('mt-4 flex items-center gap-3 rounded-[var(--radius-card)] border px-4 py-3 text-sm', verified ? 'border-success-600/30 bg-success-50 text-success-700' : 'border-warning-600/30 bg-warning-50 text-warning-700')}>
        <CheckCircle2 className="size-4" />
        {verified ? 'Your profile is verified and live in Explore Tutors.' : 'Verification in progress, usually within 24 hours. Students can already book a demo.'}
      </div>
      <Card className="mt-6">
        <CardHeader title="While you wait, finish these" description={`Your profile is ${profilePct}% complete. Complete profiles get 3× more requests.`} />
        <CardBody className="space-y-2">
          {['Add a photo', 'Write a 2-line intro', 'Set availability'].map((t, i) => (
            <div key={t} className="flex items-center justify-between rounded-lg border border-line px-3 py-2 text-sm">
              <span className="text-ink">{t}</span>
              <Link href={i === 2 ? '/tutor/profile/availability' : '/tutor/profile'} className="text-brand-700 hover:underline">{i === 2 ? 'Set' : 'Add'}</Link>
            </div>
          ))}
        </CardBody>
      </Card>
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <Card className="border-dashed p-6 text-center text-sm text-muted">No sessions yet. Requests from students will show here.</Card>
        <Card className="border-dashed p-6 text-center text-sm text-muted">Students you accept will appear in Students.</Card>
      </div>
      <div className="mt-6 flex flex-wrap gap-2">
        <Link href="/tutor/profile" className={buttonVariants({ variant: 'secondary' })}><Eye /> Preview my public profile</Link>
        <Link href="/tutor/profile" className={buttonVariants({ variant: 'secondary' })}><Share2 /> Share profile link</Link>
      </div>
    </>
  );
}
