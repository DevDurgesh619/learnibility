'use client';

import { useActionState, useState } from 'react';
import { CalendarCheck2, Lock } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { DAY_LABEL, clockLabel } from './labels';
import type { DemoDay } from './slots';

export interface BookingFormState { error?: string }

/**
 * PDF 5e: pick a slot from the overlap of both calendars, choose whether to share the gap snapshot,
 * say what to cover, confirm. The action redirects to the confirmation (5f) on success.
 */
export function DemoBookingForm({ action, tutorId, tutorFirstName, days, defaultTopic, subjectId, snapshotPreview, minutes, bothCalendars }: {
  action: (state: BookingFormState, data: FormData) => Promise<BookingFormState>;
  tutorId: string;
  tutorFirstName: string;
  days: DemoDay[];
  defaultTopic: string;
  subjectId?: string;
  snapshotPreview: string[];
  minutes: number;
  bothCalendars: boolean;
}) {
  const [state, formAction, pending] = useActionState(action, {});
  const [slot, setSlot] = useState<string>('');
  const [share, setShare] = useState(true);
  const any = days.some((d) => d.slots.length);

  return (
    <form action={formAction} className="space-y-6">
      <input type="hidden" name="tutorId" value={tutorId} />
      <input type="hidden" name="slotStartUtc" value={slot} />
      <input type="hidden" name="share" value={share ? '1' : '0'} />
      {subjectId && <input type="hidden" name="subjectId" value={subjectId} />}

      <section>
        <h2 className="text-sm font-semibold text-ink">Pick a slot <span className="font-normal text-muted">· {bothCalendars ? "only times you're both free" : `${tutorFirstName}'s open times`} · {minutes} min</span></h2>
        {!any ? (
          <p className="mt-3 rounded-lg border border-dashed border-line p-4 text-sm text-muted">No shared free time in the next 7 days. Message {tutorFirstName} or widen your study hours in Timetable.</p>
        ) : (
          <div className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-4 lg:grid-cols-7">
            {days.map((d) => (
              <div key={d.date} className="rounded-lg border border-line bg-surface p-2">
                <p className="border-b border-line pb-1 text-xs font-semibold text-ink">{DAY_LABEL[d.day]} <span className="font-normal text-muted">{Number(d.date.slice(8))}</span></p>
                <div className="mt-2 flex flex-col gap-1.5">
                  {d.slots.length === 0 && <span className="text-xs text-subtle">{d.full ? 'Fully booked' : '—'}</span>}
                  {d.slots.map((s) => (
                    <button
                      key={s.startUtc} type="button" onClick={() => setSlot(s.startUtc)} aria-pressed={slot === s.startUtc}
                      className={cn('rounded-md px-2 py-1 text-left text-xs transition-colors', slot === s.startUtc ? 'bg-brand-600 text-white' : 'bg-surface-muted text-ink hover:bg-brand-50')}
                    >
                      {clockLabel(s.start)}–{clockLabel(s.end)}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="rounded-lg border border-line p-4">
        <label className="flex cursor-pointer items-start gap-3">
          <input type="checkbox" checked={share} onChange={(e) => setShare(e.target.checked)} className="mt-1 size-4 accent-[var(--color-brand-600)]" />
          <span>
            <span className="block text-sm font-medium text-ink">Share my gap snapshot with {tutorFirstName} before the call</span>
            <span className="block text-xs text-muted">Only this subject's latest score and open gaps. Nothing sensitive, and you can stop sharing any time.</span>
          </span>
        </label>
        {share && snapshotPreview.length > 0 && (
          <ul className="mt-3 space-y-1 border-t border-line pt-3 text-xs text-muted">
            {snapshotPreview.map((l) => <li key={l}>• {l}</li>)}
          </ul>
        )}
        {!share && <p className="mt-3 flex items-center gap-1.5 border-t border-line pt-3 text-xs text-muted"><Lock className="size-3.5" /> {tutorFirstName} will only see your name, class and the topic below.</p>}
      </section>

      <label className="block">
        <span className="text-sm font-medium text-ink">What do you want to cover?</span>
        <input name="topic" defaultValue={defaultTopic} maxLength={160} className="mt-1.5 h-10 w-full rounded-lg border border-line bg-surface px-3 text-sm outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100" />
      </label>

      <div className="flex flex-col-reverse gap-3 border-t border-line pt-4 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-xs text-muted">A video link is created automatically. {tutorFirstName} confirms within a day.</p>
        <Button type="submit" disabled={!slot || pending}><CalendarCheck2 /> {pending ? 'Booking…' : 'Confirm booking'}</Button>
      </div>
      {state.error && <p role="alert" className="text-sm text-danger-700">{state.error}</p>}
    </form>
  );
}
