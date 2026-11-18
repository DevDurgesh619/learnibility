import Link from 'next/link';
import { MessageSquare, Send } from 'lucide-react';
import { Avatar, Button, Card, CardBody, EmptyState } from '@/components/ui';
import { getPersonName, type Message } from '@/lib/data';
import { cn } from '@/lib/utils';
import { fmtDateTime } from './format';

export interface ThreadSummary { threadId: string; otherId: string; otherName: string; otherRole: string; learnerId: string; last: Message; count: number }

/** Group a viewer's messages into threads (newest first). */
export function threadsFor(viewerId: string, messages: Message[]): ThreadSummary[] {
  const by = new Map<string, Message[]>();
  for (const m of messages) by.set(m.threadId, [...(by.get(m.threadId) ?? []), m]);
  return [...by.entries()].map(([threadId, ms]) => {
    const last = ms[ms.length - 1]!;
    const people = new Set(ms.flatMap((m) => [m.from, ...m.toIds]));
    people.delete(viewerId);
    people.delete('system');
    const otherId = [...people].find((p) => !p.startsWith('lrn_')) ?? [...people][0] ?? 'system';
    const p = getPersonName(otherId);
    return { threadId, otherId, otherName: p?.name ?? 'Learnibility', otherRole: p?.role ?? 'system', learnerId: last.learnerId, last, count: ms.length };
  }).sort((a, b) => b.last.sentUtc.localeCompare(a.last.sentUtc));
}

/** Two-pane inbox: thread list and the open conversation with a reply box. */
export function MessageView({
  viewerId, threads, messages, openThreadId, hrefFor, action, hidden, emptyText,
}: {
  viewerId: string; threads: ThreadSummary[]; messages: Message[]; openThreadId?: string;
  hrefFor: (t: ThreadSummary) => string; action: (f: FormData) => Promise<void>; hidden: (t: ThreadSummary) => Record<string, string>; emptyText: string;
}) {
  if (!threads.length) return <EmptyState icon={<MessageSquare />} title="No messages yet" description={emptyText} />;
  const open = threads.find((t) => t.threadId === openThreadId) ?? threads[0]!;
  const conv = messages.filter((m) => m.threadId === open.threadId);
  return (
    <div className="grid gap-4 lg:grid-cols-[20rem_1fr]">
      <Card className="overflow-hidden">
        <ul className="divide-y divide-line">
          {threads.map((t) => (
            <li key={t.threadId}>
              <Link href={hrefFor(t)} className={cn('flex items-start gap-3 px-4 py-3 hover:bg-surface-muted', t.threadId === open.threadId && 'bg-brand-50')}>
                <Avatar name={t.otherName} size="sm" />
                <div className="min-w-0 flex-1">
                  <div className="flex items-baseline justify-between gap-2"><p className="truncate text-sm font-medium text-ink">{t.otherName}</p><span className="shrink-0 text-[11px] text-subtle">{fmtDateTime(t.last.sentUtc).split(',')[0]}</span></div>
                  <p className="text-[11px] capitalize text-subtle">{t.otherRole}</p>
                  <p className="truncate text-xs text-muted">{t.last.text}</p>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      </Card>
      <Card className="flex min-h-[28rem] flex-col">
        <div className="flex items-center gap-3 border-b border-line px-5 py-3"><Avatar name={open.otherName} size="sm" /><div><p className="text-sm font-semibold text-ink">{open.otherName}</p><p className="text-xs capitalize text-muted">{open.otherRole}</p></div></div>
        <CardBody className="flex-1 space-y-3 overflow-y-auto">
          {conv.map((m) => {
            const mine = m.from === viewerId;
            return (
              <div key={m.id} className={cn('flex', mine ? 'justify-end' : 'justify-start')}>
                <div className={cn('max-w-[85%] rounded-2xl px-4 py-2 text-sm', mine ? 'bg-brand-600 text-white' : 'bg-surface-muted text-ink')}>
                  {!mine && <p className="mb-0.5 text-[11px] font-medium text-muted">{getPersonName(m.from)?.name ?? 'Learnibility'}</p>}
                  <p className="whitespace-pre-line">{m.text}</p>
                  <p className={cn('mt-1 text-[10px]', mine ? 'text-white/70' : 'text-subtle')}>{fmtDateTime(m.sentUtc)}</p>
                </div>
              </div>
            );
          })}
        </CardBody>
        {open.otherId !== 'system' && (
          <form action={action} className="flex items-end gap-2 border-t border-line p-3">
            {Object.entries({ ...hidden(open), threadId: open.threadId, to: open.otherId }).map(([k, v]) => <input key={k} type="hidden" name={k} value={v} />)}
            <label className="sr-only" htmlFor="msg-text">Message</label>
            <textarea id="msg-text" name="text" required rows={2} placeholder={`Write to ${open.otherName.split(' ')[0]}…`} className="min-h-10 flex-1 resize-none rounded-lg border border-line bg-surface px-3 py-2 text-sm text-ink outline-none focus:border-brand-400" />
            <Button type="submit" size="icon" aria-label="Send"><Send /></Button>
          </form>
        )}
      </Card>
    </div>
  );
}
