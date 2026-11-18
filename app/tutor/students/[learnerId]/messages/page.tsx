import { Send } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { formatDay, formatTime } from '@/components/marketplace/dates';
import { studentContext } from '@/components/tutor/model';
import { sendMessage } from '@/lib/actions/tutor';
import { localDateOf } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import { cn } from '@/lib/utils';

/** 4n 1:1 chat; system events (assignments, session changes) appear inline so the chat doubles as a log. */
export default async function Messages({ params }: { params: Promise<{ learnerId: string }> }) {
  const { learnerId } = await params;
  const { ws, row } = studentContext((await currentPersona())!.id, learnerId)!;
  const msgs = ws.messages.filter((m) => m.learnerId === learnerId);
  const first = row.name.split(' ')[0];
  let lastDay = '';
  const quick = [`Reminder: our session is ${row.nextSession ? `${formatDay(row.nextSession.startUtc)} at ${formatTime(row.nextSession.startUtc)}` : 'coming up'}.`, 'Sharing a resource for this week: check your tasks.', 'You have an overdue task. Can you finish it today?'];
  return (
    <Card className="flex flex-col">
      <div className="max-h-[60vh] min-h-64 space-y-3 overflow-y-auto p-4">
        {msgs.length === 0 && <p className="py-10 text-center text-sm text-muted">No messages yet. Say hello to {first}.</p>}
        {msgs.map((m) => {
          const day = localDateOf(m.sentUtc);
          const sep = day !== lastDay; lastDay = day;
          const mine = m.from === ws.tutor.id;
          return (
            <div key={m.id}>
              {sep && <p className="my-2 text-center text-xs text-subtle">{formatDay(m.sentUtc)}</p>}
              {m.from === 'system' ? (
                <p className="mx-auto w-fit rounded-full bg-surface-muted px-3 py-1 text-center text-xs text-muted">{m.text}</p>
              ) : (
                <div className={cn('flex', mine ? 'justify-end' : 'justify-start')}>
                  <div className={cn('max-w-[80%] rounded-2xl px-3 py-2 text-sm', mine ? 'rounded-br-sm bg-brand-600 text-white' : 'rounded-bl-sm bg-surface-muted text-ink')}>
                    {m.text}<span className={cn('ml-2 text-[10px]', mine ? 'text-brand-100' : 'text-subtle')}>{formatTime(m.sentUtc)}</span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
      <form action={sendMessage} className="space-y-2 border-t border-line p-3">
        <input type="hidden" name="learnerId" value={learnerId} />
        <div className="flex gap-2">
          <input name="text" required placeholder={`Message ${first}…`} className="h-10 flex-1 rounded-lg border border-line px-3 text-sm" />
          <Button><Send /> Send</Button>
        </div>
      </form>
      <div className="flex flex-wrap gap-2 border-t border-line px-3 py-2 text-xs">
        <span className="text-muted">Quick:</span>
        {quick.map((q) => (
          <form key={q} action={sendMessage}><input type="hidden" name="learnerId" value={learnerId} /><input type="hidden" name="text" value={q} /><button className="rounded-full border border-line px-2.5 py-0.5 hover:bg-surface-muted">{q.split(':')[0]}</button></form>
        ))}
      </div>
    </Card>
  );
}
