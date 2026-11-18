'use client';

import { useEffect, useRef, useState, useTransition } from 'react';
import { CalendarClock, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { requestTimetableChange, withdrawTimetableRequest, type RequestChangeInput } from '@/lib/actions/timetable';
import { cn } from '@/lib/utils';

const DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'] as const;
const field = 'h-10 w-full rounded-lg border border-line bg-surface px-3 text-sm text-ink placeholder:text-subtle focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-100';

/** PDF 3b: request a schedule change from the counsellor, as a modal over the timetable. */
export function RequestChangeButton({ counsellorName, tasks, defaultDate, autoOpen = false }: {
  counsellorName: string; tasks: { title: string; blockIds: string[] }[]; defaultDate: string; autoOpen?: boolean;
}) {
  const [open, setOpen] = useState(autoOpen);
  const [error, setError] = useState<string | null>(null);
  const [pending, start] = useTransition();
  const [repeat, setRepeat] = useState<RequestChangeInput['repeat']>('none');
  const [days, setDays] = useState<string[]>([]);
  const dialog = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const d = dialog.current;
    if (!d) return;
    if (open && !d.open) d.showModal();
    if (!open && d.open) d.close();
  }, [open]);

  const submit = (fd: FormData) => start(async () => {
    setError(null);
    const task = String(fd.get('task') ?? '');
    const res = await requestTimetableChange({
      task,
      blockIds: tasks.find((t) => t.title === task)?.blockIds ?? [],
      fromDate: String(fd.get('fromDate') ?? ''),
      toDate: String(fd.get('toDate') ?? ''),
      fromTime: String(fd.get('fromTime') ?? ''),
      toTime: String(fd.get('toTime') ?? ''),
      repeat,
      days: repeat === 'weekly' || repeat === 'custom' ? days : [],
      reason: String(fd.get('reason') ?? ''),
    });
    if (res.ok) { setOpen(false); setRepeat('none'); setDays([]); } else setError(res.error);
  });

  return (
    <>
      <Button variant="secondary" size="sm" onClick={() => setOpen(true)} className="border-brand-300 text-brand-700"><CalendarClock />Request change</Button>
      <dialog
        ref={dialog}
        onClose={() => setOpen(false)}
        className="m-auto w-[min(92vw,520px)] rounded-2xl border border-line bg-surface p-0 text-ink shadow-xl backdrop:bg-ink/40"
        aria-labelledby="req-title"
      >
        <form action={submit} className="flex flex-col gap-3 p-5">
          <div className="flex items-center justify-between">
            <h2 id="req-title" className="text-base font-semibold">Request a change from {counsellorName.split(' ')[0]}</h2>
            <button type="button" onClick={() => setOpen(false)} className="rounded-lg p-1 text-muted hover:bg-surface-muted" aria-label="Close"><X className="size-4" /></button>
          </div>
          <label className="text-xs font-medium text-muted">Task
            <select name="task" className={cn(field, 'mt-1')} defaultValue={tasks[0]?.title} required>
              {tasks.map((t) => <option key={t.title}>{t.title}</option>)}
            </select>
          </label>
          <div className="grid grid-cols-2 gap-3">
            <label className="text-xs font-medium text-muted">From date<input type="date" name="fromDate" defaultValue={defaultDate} className={cn(field, 'mt-1')} required /></label>
            <label className="text-xs font-medium text-muted">To date<input type="date" name="toDate" defaultValue={defaultDate} className={cn(field, 'mt-1')} /></label>
            <label className="text-xs font-medium text-muted">From time<input type="time" name="fromTime" defaultValue="20:00" className={cn(field, 'mt-1')} required /></label>
            <label className="text-xs font-medium text-muted">To time<input type="time" name="toTime" defaultValue="21:00" className={cn(field, 'mt-1')} required /></label>
          </div>
          <fieldset>
            <legend className="text-xs font-medium text-muted">Repeat</legend>
            <div className="mt-1 flex flex-wrap gap-2">
              {(['none', 'daily', 'weekly', 'custom'] as const).map((r) => (
                <button key={r} type="button" onClick={() => setRepeat(r)} aria-pressed={repeat === r}
                  className={cn('rounded-full px-3 py-1 text-sm ring-1 ring-inset', repeat === r ? 'bg-ink text-white ring-ink' : 'text-muted ring-line hover:text-ink')}>
                  {r === 'none' ? 'Once' : r[0]!.toUpperCase() + r.slice(1)}
                </button>
              ))}
            </div>
            {(repeat === 'weekly' || repeat === 'custom') && (
              <div className="mt-2 flex flex-wrap gap-1.5">
                {DAYS.map((d) => (
                  <button key={d} type="button" aria-pressed={days.includes(d)}
                    onClick={() => setDays((s) => (s.includes(d) ? s.filter((x) => x !== d) : [...s, d]))}
                    className={cn('w-11 rounded-md py-1 text-xs ring-1 ring-inset', days.includes(d) ? 'bg-brand-600 text-white ring-brand-600' : 'text-muted ring-line')}>
                    {d[0]!.toUpperCase() + d.slice(1)}
                  </button>
                ))}
              </div>
            )}
          </fieldset>
          <label className="text-xs font-medium text-muted">Why? (optional)
            <textarea name="reason" rows={3} className={cn(field, 'mt-1 h-auto py-2')} placeholder="For example: football practice moved to 5 pm on weekdays" />
          </label>
          {error && <p role="alert" className="text-sm text-danger-700">{error}</p>}
          <div className="flex justify-end gap-2 pt-1">
            <Button type="button" variant="secondary" onClick={() => setOpen(false)}>Cancel</Button>
            <Button type="submit" disabled={pending}>{pending ? 'Sending…' : 'Send request'}</Button>
          </div>
        </form>
      </dialog>
    </>
  );
}

export function UndoRequestButton({ requestId }: { requestId: string }) {
  const [pending, start] = useTransition();
  return (
    <Button variant="secondary" size="sm" disabled={pending} onClick={() => start(() => withdrawTimetableRequest(requestId))}>
      {pending ? 'Undoing…' : 'Undo'}
    </Button>
  );
}
