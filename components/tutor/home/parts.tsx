import Link from 'next/link';
import { AlertTriangle, ClipboardCheck, Plus, Send, Share2, Sparkles, Video } from 'lucide-react';
import { Avatar } from '@/components/ui/avatar';
import { Badge, GapBadge } from '@/components/ui/badge';
import { Button, buttonVariants } from '@/components/ui/button';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { formatDay, formatTime, relative } from '@/components/marketplace/dates';
import { BOARD_LABEL } from '@/components/marketplace/labels';
import { acceptBooking, declineBooking } from '@/lib/actions/booking';
import type { Booking, Session, TutorWorkspace } from '@/lib/data/types';
import { aiFocus, firstName, nameOf, sessionWho, type StudentRow, type TodayItem } from '../model';
import { SessionKind } from '../bits';
import { cn } from '@/lib/utils';

export function NextSessionCard({ ws, s, now, compact }: { ws: TutorWorkspace; s?: Session; now: Date; compact?: boolean }) {
  if (!s) {
    return (
      <Card className="p-5">
        <p className="text-sm text-muted">Next session</p>
        <p className="mt-1 font-medium text-ink">Nothing booked yet</p>
        <p className="text-sm text-muted">Open slots in your calendar are what students can book.</p>
      </Card>
    );
  }
  const f = aiFocus(ws, s);
  const lid = s.learnerIds?.[0] ?? s.learnerId;
  return (
    <Card className="border-brand-200 bg-gradient-to-br from-brand-50/70 to-surface p-5">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <p className="text-sm font-medium text-brand-700">Next session · {relative(s.startUtc, now)}</p>
        <SessionKind s={s} />
      </div>
      <p className="mt-1 text-lg font-semibold text-ink">{formatTime(s.startUtc)} · {sessionWho(ws, s)}</p>
      <p className="text-sm text-muted">{s.title}{s.focus && !compact ? ` · ${s.focus}` : ''} · {s.minutes} min</p>
      <p className="mt-3 flex gap-1.5 text-sm text-ink"><Sparkles className="mt-0.5 size-4 shrink-0 text-brand-600" /><span><span className="font-medium">AI focus:</span> {f.line} <span className="text-xs text-muted">({f.source})</span></span></p>
      <div className="mt-4 flex flex-wrap gap-2">
        <Link href={`/tutor/sessions/${s.id}/prep`} className={buttonVariants({ size: 'sm' })}>Prepare session</Link>
        {!compact && <Link href={`/tutor/students/${lid}`} className={buttonVariants({ size: 'sm', variant: 'secondary' })}>View student</Link>}
      </div>
    </Card>
  );
}

export function NeedsAttention({ rows, compact }: { rows: StudentRow[]; compact?: boolean }) {
  return (
    <Card>
      <CardHeader title={`Needs attention${rows.length ? ` · ${rows.length}` : ''}`} action={<Link href="/tutor/students" className="text-sm text-brand-700 hover:underline">Students</Link>} />
      <CardBody className="pt-3">
        {rows.length === 0 ? <p className="text-sm text-muted">Everyone is on track. Nice.</p> : compact ? (
          <p className="text-sm text-ink">{rows.slice(0, 4).map((r) => `${firstName(r.name)} ${r.issue!.label.replace(/^.*?(↓)/, '$1')}`).join(' · ')}</p>
        ) : (
          <ul className="divide-y divide-line">
            {rows.slice(0, 5).map((r) => (
              <li key={r.learnerId} className="flex items-center gap-3 py-2.5">
                <AlertTriangle className={cn('size-4 shrink-0', r.issue!.kind === 'drop' ? 'text-danger-600' : 'text-warning-600')} />
                <span className="min-w-0 flex-1 text-sm"><span className="font-medium text-ink">{firstName(r.name)}</span> <span className="text-muted">{r.issue!.label}</span></span>
                <Link href={r.issue!.href} className={buttonVariants({ size: 'sm', variant: 'secondary' })}>{r.issue!.action}</Link>
              </li>
            ))}
          </ul>
        )}
      </CardBody>
    </Card>
  );
}

export function ReviewQueue({ ws, queue }: { ws: TutorWorkspace; queue: { a: TutorWorkspace['assignments'][number]; waiting: number }[] }) {
  return (
    <Card>
      <CardHeader title={`Review queue${queue.length ? ` · ${queue.length}` : ''}`} />
      <CardBody className="pt-3">
        {queue.length === 0 ? <p className="text-sm text-muted">Nothing waiting for review.</p> : (
          <ul className="divide-y divide-line">
            {queue.map(({ a, waiting }) => (
              <li key={a.id} className="flex items-center gap-3 py-2.5">
                <ClipboardCheck className="size-4 shrink-0 text-brand-600" />
                <span className="min-w-0 flex-1 text-sm"><span className="font-medium text-ink">{firstName(nameOf(ws, a.learnerId))}</span> <span className="text-muted">· {a.title} · {waiting ? `AI graded, ${waiting} to check` : 'ready to publish'}</span></span>
                <Link href={`/tutor/students/${a.learnerId}/assignments/${a.id}`} className={buttonVariants({ size: 'sm', variant: 'secondary' })}>Evaluate</Link>
              </li>
            ))}
          </ul>
        )}
      </CardBody>
    </Card>
  );
}

export function RestOfToday({ items }: { items: TodayItem[] }) {
  const sessions = items.filter((i) => i.kind === 'session');
  return (
    <Card>
      <CardHeader title="Rest of today" action={<Link href="/tutor/today" className="text-sm text-brand-700 hover:underline">Today</Link>} />
      <CardBody className="pt-3">
        {sessions.length === 0 ? <p className="text-sm text-muted">No more sessions today.</p> : (
          <ul className="space-y-2">
            {sessions.map((i) => (
              <li key={i.id} className={cn('flex items-center gap-3 text-sm', i.done && 'opacity-60')}>
                <span className="w-20 shrink-0 font-medium text-ink">{formatTime(i.at!)}</span>
                <span className="min-w-0 flex-1 truncate text-muted">{i.title}</span>
              </li>
            ))}
          </ul>
        )}
      </CardBody>
    </Card>
  );
}

export function QuickActions({ share }: { share?: boolean }) {
  return (
    <div className="flex flex-wrap gap-2">
      <Link href="/tutor/sessions?view=calendar" className={buttonVariants({ variant: 'secondary', size: 'sm' })}><Plus /> Create session</Link>
      <Link href="/tutor/students?pick=assign" className={buttonVariants({ variant: 'secondary', size: 'sm' })}><Send /> Assign test</Link>
      {share ? <Link href="/tutor/profile" className={buttonVariants({ variant: 'secondary', size: 'sm' })}><Share2 /> Share profile link</Link>
        : <Link href="/tutor/sessions" className={buttonVariants({ variant: 'secondary', size: 'sm' })}><Video /> All sessions</Link>}
    </div>
  );
}

/** One request row with Accept / View / Decline (2b). */
export function RequestRow({ ws, b }: { ws: TutorWorkspace; b: Booking }) {
  const st = ws.students.find((s) => s.learnerId === b.learnerId);
  const g = b.sharedGapSnapshot?.gaps[0];
  return (
    <li className="flex flex-col gap-3 py-3 sm:flex-row sm:items-center">
      <div className="flex min-w-0 flex-1 items-center gap-3">
        <Avatar name={nameOf(ws, b.learnerId)} size="sm" />
        <div className="min-w-0">
          <p className="truncate text-sm font-medium text-ink">{nameOf(ws, b.learnerId)} · Class {st?.grade} {st ? BOARD_LABEL[st.board] : ''}</p>
          <p className="truncate text-xs text-muted">{b.kind === 'demo' ? 'Demo request' : 'Request'}{b.slotStartUtc ? ` · ${formatDay(b.slotStartUtc)} ${formatTime(b.slotStartUtc)}` : ''}{g ? ` · gap: ${g.name}` : b.topic ? ` · ${b.topic}` : ''}</p>
        </div>
      </div>
      <div className="flex shrink-0 gap-2">
        <form action={acceptBooking}><input type="hidden" name="bookingId" value={b.id} /><Button size="sm">Accept</Button></form>
        <Link href={`/tutor/requests/${b.id}`} className={buttonVariants({ size: 'sm', variant: 'secondary' })}>View</Link>
        <form action={declineBooking}><input type="hidden" name="bookingId" value={b.id} /><Button size="sm" variant="ghost">Decline</Button></form>
      </div>
    </li>
  );
}

export function GapChips({ b }: { b: Booking }) {
  return <div className="flex flex-wrap gap-1.5">{(b.sharedGapSnapshot?.gaps ?? []).slice(0, 4).map((g) => <GapBadge key={g.subtopicId} code={g.code} />)}{b.status === 'requested' && <Badge tone="warning">New</Badge>}</div>;
}
