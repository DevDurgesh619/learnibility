import Link from 'next/link';
import { AlertTriangle, CalendarClock, ChevronRight } from 'lucide-react';
import { Avatar, Badge, BandBadge, Card } from '@/components/ui';
import type { CaseloadEntry, RiskFlag } from '@/lib/data/types';
import { formatDay, formatTime } from './format';

const SEV_TONE = { high: 'danger', medium: 'warning', low: 'neutral' } as const;
const PLAN_LABEL = { free: 'Free', application_support: 'Application Support', full_package: 'Full package' } as const;

export function FlagChip({ flag }: { flag: RiskFlag }) {
  return <Badge tone={SEV_TONE[flag.severity]} title={flag.text}>{flag.severity === 'high' && <AlertTriangle className="size-3" />}{flag.text}</Badge>;
}

/** One row per student: desktop table, stacked cards on mobile. */
export function CaseloadList({ entries }: { entries: CaseloadEntry[] }) {
  return (
    <Card className="overflow-hidden">
      <div className="hidden overflow-x-auto lg:block">
        <table className="w-full text-sm">
          <thead className="bg-surface-muted/60 text-left text-xs font-medium uppercase tracking-wide text-subtle">
            <tr><th className="h-10 px-4">Student</th><th className="px-4">Programme</th><th className="px-4">Band</th><th className="px-4">Open gaps</th><th className="px-4">Flags</th><th className="px-4">Next session</th><th className="px-4" /></tr>
          </thead>
          <tbody className="divide-y divide-line">
            {entries.map((e) => (
              <tr key={e.student.id} className="hover:bg-surface-muted/50">
                <td className="px-4 py-3">
                  <Link href={`/counsellor/student-360?student=${e.student.id}`} className="flex items-center gap-3">
                    <Avatar name={e.student.name} src={e.student.avatar} size="sm" />
                    <div className="min-w-0">
                      <div className="flex items-center gap-2 font-medium text-ink">{e.student.name}{e.needsYouToday && <Badge tone="danger">Today</Badge>}</div>
                      <div className="truncate text-xs text-muted">{e.focus}</div>
                    </div>
                  </Link>
                </td>
                <td className="px-4 py-3 text-muted"><div>{e.student.programme}</div><div className="text-xs text-subtle">{PLAN_LABEL[e.student.plan]}</div></td>
                <td className="px-4 py-3"><BandBadge band={e.student.band} /></td>
                <td className="px-4 py-3 text-ink">{e.openGaps}</td>
                <td className="max-w-xs px-4 py-3">
                  <div className="flex flex-wrap gap-1">
                    {e.flags.slice(0, 2).map((f, i) => <FlagChip key={i} flag={f} />)}
                    {e.flags.length > 2 && <Badge>+{e.flags.length - 2}</Badge>}
                    {e.pendingRequests > 0 && <Badge tone="info">{e.pendingRequests} request{e.pendingRequests > 1 ? 's' : ''}</Badge>}
                    {e.flags.length === 0 && e.pendingRequests === 0 && <span className="text-xs text-subtle">None</span>}
                  </div>
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-muted">{e.nextSession ? <>{formatDay(e.nextSession.startUtc)}, {formatTime(e.nextSession.startUtc)}</> : '—'}</td>
                <td className="px-4 py-3 text-right"><Link href={`/counsellor/student-360?student=${e.student.id}`} className="text-subtle hover:text-ink" aria-label={`Open ${e.student.name}`}><ChevronRight className="size-4" /></Link></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <ul className="divide-y divide-line lg:hidden">
        {entries.map((e) => (
          <li key={e.student.id}>
            <Link href={`/counsellor/student-360?student=${e.student.id}`} className="flex gap-3 p-4">
              <Avatar name={e.student.name} src={e.student.avatar} size="sm" />
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2"><span className="font-medium text-ink">{e.student.name}</span>{e.needsYouToday && <Badge tone="danger">Today</Badge>}<BandBadge band={e.student.band} /></div>
                <div className="text-xs text-muted">{e.student.programme} · {e.openGaps} open gaps</div>
                <div className="mt-2 flex flex-wrap gap-1">
                  {e.flags.slice(0, 3).map((f, i) => <FlagChip key={i} flag={f} />)}
                  {e.pendingRequests > 0 && <Badge tone="info">{e.pendingRequests} request{e.pendingRequests > 1 ? 's' : ''}</Badge>}
                </div>
                {e.nextSession && <div className="mt-2 inline-flex items-center gap-1 text-xs text-muted"><CalendarClock className="size-3.5" />{formatDay(e.nextSession.startUtc)}, {formatTime(e.nextSession.startUtc)}</div>}
              </div>
              <ChevronRight className="mt-1 size-4 shrink-0 text-subtle" />
            </Link>
          </li>
        ))}
      </ul>
    </Card>
  );
}
