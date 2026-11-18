import Link from 'next/link';
import { buttonVariants } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { formatDay, formatTime } from '@/components/marketplace/dates';
import { demoNow } from '@/lib/data';
import type { Session, TutorWorkspace } from '@/lib/data/types';
import { aiFocus, isUpcoming, reportMissing, sessionWho } from './model';
import { SessionKind } from './bits';

/** One session line with the right action for its state: Join/Prep, Write report, or View summary. */
export function SectionKindRow({ ws, s, showWho }: { ws: TutorWorkspace; s: Session; showWho?: boolean }) {
  const up = isUpcoming(s);
  const missing = reportMissing(s);
  const joinable = up && Date.parse(s.startUtc) - Date.parse(demoNow()) <= 10 * 60_000;
  const focus = up ? aiFocus(ws, s).line : s.report?.topics.join(', ') || s.focus;
  return (
    <li className="flex flex-col gap-2 px-4 py-3 sm:flex-row sm:items-center">
      <div className="w-36 shrink-0 text-sm"><p className="font-medium text-ink">{formatDay(s.startUtc)}</p><p className="text-xs text-muted">{formatTime(s.startUtc)} · {s.minutes} min</p></div>
      <div className="min-w-0 flex-1">
        <p className="flex items-center gap-2 truncate text-sm font-medium text-ink">{s.code} {showWho && `· ${sessionWho(ws, s)}`} · {s.title} <SessionKind s={s} /></p>
        <p className="truncate text-xs text-muted">{up ? 'Focus: ' : ''}{focus}</p>
      </div>
      <div className="flex shrink-0 gap-2">
        {s.status === 'no_show' && <Badge tone="danger">Missed</Badge>}
        {up && <Link href={`/tutor/sessions/${s.id}/prep`} className={buttonVariants({ size: 'sm', variant: 'secondary' })}>{s.prepNotes ? 'Prep ✓' : 'Prep'}</Link>}
        {up && <Link href={`/tutor/sessions/${s.id}/live`} aria-disabled={!joinable} className={buttonVariants({ size: 'sm', className: joinable ? '' : 'pointer-events-none opacity-50' })} title={joinable ? 'Join' : 'Join opens 10 minutes before'}>Join</Link>}
        {missing && s.kind !== 'demo' && <Link href={`/tutor/sessions/${s.id}/report`} className={buttonVariants({ size: 'sm' })}>Write report</Link>}
        {s.report && <Link href={`/tutor/sessions/${s.id}`} className={buttonVariants({ size: 'sm', variant: 'secondary' })}>View summary</Link>}
      </div>
    </li>
  );
}
