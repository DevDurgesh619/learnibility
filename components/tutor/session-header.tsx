import Link from 'next/link';
import { formatDay, formatRange } from '@/components/marketplace/dates';
import { getSubject } from '@/lib/data';
import type { Session, TutorWorkspace } from '@/lib/data/types';
import { BackLink, SessionKind } from './bits';
import { sessionWho } from './model';

/** Title block shared by the session screens (5c to 5g). */
export function SessionHeader({ ws, s, title, back = '/tutor/sessions', backLabel = 'Sessions', actions }: { ws: TutorWorkspace; s: Session; title: string; back?: string; backLabel?: string; actions?: React.ReactNode }) {
  const subject = s.subjectId ? getSubject(s.subjectId)?.subject.name : undefined;
  const lid = s.learnerIds?.[0] ?? s.learnerId;
  const st = ws.students.find((x) => x.learnerId === lid);
  return (
    <div className="mb-6">
      <BackLink href={back}>{backLabel}</BackLink>
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div className="min-w-0">
          <h1 className="flex flex-wrap items-center gap-2 text-2xl font-semibold text-ink">{title} · {sessionWho(ws, s)} <SessionKind s={s} /></h1>
          <p className="mt-1 text-sm text-muted">
            {formatDay(s.startUtc)} {formatRange(s.startUtc, s.minutes)} · {s.minutes} min{s.code ? ` · ${s.code}` : ''}{subject ? ` · ${subject}` : ''}{st?.goal ? ` · goal: ${st.goal}` : ''}
          </p>
          {st && <Link href={`/tutor/students/${lid}`} className="mt-1 inline-block text-sm font-medium text-brand-700 hover:underline">View student</Link>}
        </div>
        {actions && <div className="flex flex-wrap gap-2">{actions}</div>}
      </div>
    </div>
  );
}
