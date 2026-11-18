import { ArrowRight, CalendarClock, Check, Pencil, X } from 'lucide-react';
import { Avatar, Badge, Button, Card } from '@/components/ui';
import type { TimetableRequest } from '@/lib/data/types';
import type { TimetableBlock } from '@/lib/engines';
import { decideTimetableRequest } from '@/lib/actions/counsellor';
import { formatDate, formatDay, formatHHMM, relativeDays } from './format';

export const REQUEST_KIND_LABEL: Record<TimetableRequest['kind'], string> = {
  move: 'Move a block', add: 'Add a block', drop: 'Drop a block', swap: 'Swap blocks', more_time: 'More time', less_time: 'Less time', other: 'Other change',
};
const STATUS_TONE = { pending: 'warning', approved: 'success', edited: 'info', declined: 'danger' } as const;
const STATUS_LABEL = { pending: 'Pending', approved: 'Approved', edited: 'Approved with edits', declined: 'Declined' } as const;

function proposedText(p: TimetableRequest['proposed']) {
  if (!p) return null;
  if (typeof p === 'string') return p;
  return `${formatDay(p.date)}, ${formatHHMM(p.start)} to ${formatHHMM(p.end)}`;
}

function BlockLine({ b }: { b: TimetableBlock }) {
  return (
    <li className="flex flex-wrap items-center gap-x-2 text-sm">
      <span className="font-medium text-ink">{b.title}</span>
      <span className="text-muted">{formatDay(b.date)}, {formatHHMM(b.start)} to {formatHHMM(b.end)} · {b.minutes} min</span>
    </li>
  );
}

export function RequestCard({ request, studentName, blocks, now, editable = true }: {
  request: TimetableRequest; studentName: string; blocks: TimetableBlock[]; now: Date; editable?: boolean;
}) {
  const proposed = proposedText(request.proposed);
  const slot = typeof request.proposed === 'object' && request.proposed ? request.proposed : undefined;
  const first = blocks[0];
  return (
    <Card className="overflow-hidden" id={request.id}>
      <div className="flex flex-col gap-4 p-5 lg:flex-row lg:items-start">
        <div className="flex min-w-0 flex-1 gap-3">
          <Avatar name={studentName} />
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <span className="font-semibold text-ink">{studentName}</span>
              <Badge tone="brand">{REQUEST_KIND_LABEL[request.kind]}</Badge>
              <Badge tone={STATUS_TONE[request.status]}>{STATUS_LABEL[request.status]}</Badge>
              <span className="text-xs text-subtle">Sent {relativeDays(request.createdUtc, now)}</span>
            </div>
            <p className="mt-2 text-sm text-ink">&ldquo;{request.reason}&rdquo;</p>
            {blocks.length > 0 && (
              <div className="mt-3">
                <p className="text-xs font-medium uppercase tracking-wide text-subtle">{request.status === 'pending' ? 'Affects' : 'Now planned'}</p>
                <ul className="mt-1 space-y-1">{blocks.map((b) => <BlockLine key={b.id} b={b} />)}</ul>
              </div>
            )}
            {proposed && (
              <p className="mt-3 inline-flex flex-wrap items-center gap-2 rounded-lg bg-surface-muted px-3 py-2 text-sm">
                <CalendarClock className="size-4 text-brand-600" />
                <span className="text-muted">Asks for</span>
                <ArrowRight className="size-3.5 text-subtle" />
                <span className="font-medium text-ink">{proposed}</span>
              </p>
            )}
            {request.status !== 'pending' && (
              <p className="mt-3 text-sm text-muted">
                Decided {request.decidedUtc ? formatDate(request.decidedUtc) : ''}{request.decisionNote ? `: ${request.decisionNote}` : ''}
              </p>
            )}
          </div>
        </div>
      </div>
      {editable && request.status === 'pending' && (
        <div className="border-t border-line bg-surface-muted/40 px-5 py-4">
          <form action={decideTimetableRequest} className="flex flex-col gap-3">
            <input type="hidden" name="requestId" value={request.id} />
            <input type="hidden" name="learnerId" value={request.learnerId} />
            <label className="text-sm text-muted">
              Note to {studentName.split(' ')[0]} <span className="text-subtle">(optional)</span>
              <input name="note" className="mt-1 h-10 w-full rounded-lg border border-line bg-surface px-3 text-sm text-ink" placeholder="e.g. Moved so it doesn't clash with football" />
            </label>
            <details className="group">
              <summary className="cursor-pointer list-none text-sm font-medium text-brand-700 [&::-webkit-details-marker]:hidden">
                <span className="inline-flex items-center gap-1"><Pencil className="size-3.5" />Edit the slot before approving</span>
              </summary>
              <div className="mt-3 grid gap-3 sm:grid-cols-3">
                <label className="text-sm text-muted">Date
                  <input type="date" name="date" defaultValue={slot?.date ?? first?.date} className="mt-1 h-10 w-full rounded-lg border border-line bg-surface px-3 text-sm text-ink" />
                </label>
                <label className="text-sm text-muted">Start
                  <input type="time" name="start" defaultValue={slot?.start ?? first?.start} className="mt-1 h-10 w-full rounded-lg border border-line bg-surface px-3 text-sm text-ink" />
                </label>
                <label className="text-sm text-muted">End
                  <input type="time" name="end" defaultValue={slot?.end ?? first?.end} className="mt-1 h-10 w-full rounded-lg border border-line bg-surface px-3 text-sm text-ink" />
                </label>
              </div>
              <Button type="submit" name="decision" value="edited" variant="secondary" className="mt-3"><Pencil />Approve with these times</Button>
            </details>
            <div className="flex flex-wrap gap-2">
              <Button type="submit" name="decision" value="approved"><Check />Approve and re-plan</Button>
              <Button type="submit" name="decision" value="declined" variant="secondary"><X />Decline</Button>
            </div>
          </form>
        </div>
      )}
    </Card>
  );
}
