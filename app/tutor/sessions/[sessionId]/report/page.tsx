import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { Eye, Sparkles } from 'lucide-react';
import { SessionHeader } from '@/components/tutor/session-header';
import { SectionTitle } from '@/components/tutor/bits';
import { aiFocus, firstName, nameOf, sessionContext, suggestNextFocus } from '@/components/tutor/model';
import { formatDay, formatTime } from '@/components/marketplace/dates';
import { Button } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { submitSessionReport } from '@/lib/actions/tutor';
import { addDaysLocal, demoToday } from '@/lib/data';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Session report · Tutor' };

const field = 'w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm text-ink focus:border-brand-400 focus:outline-none';

function Segmented({ name, options, value }: { name: string; options: [string, string][]; value: string }) {
  return (
    <div className="inline-flex flex-wrap gap-1 rounded-lg border border-line bg-surface-muted p-1">
      {options.map(([v, label]) => (
        <label key={v} className="cursor-pointer">
          <input type="radio" name={name} value={v} defaultChecked={v === value} className="peer sr-only" />
          <span className="block rounded-md px-3 py-1.5 text-sm text-muted peer-checked:bg-surface peer-checked:font-medium peer-checked:text-ink peer-checked:shadow-sm peer-focus-visible:ring-2 peer-focus-visible:ring-brand-400">{label}</span>
        </label>
      ))}
    </div>
  );
}

/**
 * Tutor HTML 5e: post-session report, pre-filled from the plan and live notes. Submit puts homework into each
 * student's tasks (4m and their Today), files private notes, moves the next focus to the next session.
 */
export default async function ReportPage({ params, searchParams }: { params: Promise<{ sessionId: string }>; searchParams: Promise<{ notes?: string; done?: string | string[] }> }) {
  const [{ sessionId }, sp] = await Promise.all([params, searchParams]);
  const persona = (await currentPersona())!;
  const ctx = sessionContext(persona.id, sessionId);
  if (!ctx) notFound();
  const { ws, s, learners, ownHomework, next } = ctx;
  const r = s.report;
  const who = learners.length > 1 ? 'the group' : firstName(nameOf(ws, s.learnerId));
  const focus = aiFocus(ws, s).line.split(':')[0]!;
  const done = ([] as string[]).concat(sp.done ?? []);
  const topics = r?.topics ?? [focus];
  const liveNotes = [sp.notes?.trim(), done.length ? `Plan steps done: ${done.join('; ')}` : ''].filter(Boolean).join('\n');
  const homeworkDefault = r ? [...new Set(ownHomework.filter((t) => t.status !== 'skipped').map((t) => t.title))] : [`Practice set: ${focus}`, 'Re-attempt the problems you got wrong today'];
  const due = ownHomework[0]?.dueDate ?? addDaysLocal(demoToday(), 2);
  const nextFocus = r?.nextFocus ?? suggestNextFocus(ws, s);
  const pad = <T,>(xs: T[], n: number, fill: T) => [...xs, ...Array(Math.max(0, n - xs.length)).fill(fill)] as T[];

  return (
    <div className="mx-auto max-w-3xl">
      <SessionHeader ws={ws} s={s} title={r ? 'Edit report' : 'Session report'} back={`/tutor/sessions/${s.id}`} backLabel="Session" />
      <form action={submitSessionReport}>
        <input type="hidden" name="sessionId" value={s.id} />
        <Card><CardBody className="space-y-6">
          <p className="text-sm text-muted">Takes about 2 minutes · Attended ✓</p>

          <section>
            <SectionTitle>Topics covered</SectionTitle>
            <div className="grid gap-2 sm:grid-cols-2">
              {pad(topics, 4, '').map((t, i) => <input key={i} name="topic" defaultValue={t} placeholder={i === 0 ? 'Topic' : '+ add topic'} aria-label={`Topic ${i + 1}`} className={field} />)}
            </div>
          </section>

          <section className="space-y-3">
            <SectionTitle>How did {who} do?</SectionTitle>
            <Segmented name="performance" value={r?.performance ?? 'getting_there'} options={[['struggled', 'Struggled'], ['getting_there', 'Getting there'], ['confident', 'Confident']]} />
            <div className="flex flex-wrap items-center gap-3"><span className="text-sm text-muted">Engagement</span><Segmented name="engagement" value={r?.engagement ?? 'high'} options={[['high', 'High'], ['medium', 'Medium'], ['low', 'Low']]} /></div>
          </section>

          <section>
            <label htmlFor="notes" className="mb-2 block text-base font-semibold text-ink">Notes <span className="text-sm font-normal text-muted">(private)</span></label>
            <textarea id="notes" name="notes" rows={3} defaultValue={r?.notes ?? liveNotes} placeholder="What worked, what to watch next time" className={field} />
          </section>

          <section>
            <SectionTitle>Homework for {who}</SectionTitle>
            <div className="space-y-2">
              {pad(homeworkDefault, 3, '').map((h, i) => <input key={i} name="homework" defaultValue={h} placeholder="+ add task" aria-label={`Homework ${i + 1}`} className={field} />)}
            </div>
            <label className="mt-2 flex items-center gap-2 text-sm text-muted">Due <input type="date" name="dueDate" defaultValue={due} className="rounded-lg border border-line bg-surface px-2 py-1 text-sm text-ink" /></label>
          </section>

          <section>
            <SectionTitle>Next session{next ? ` · ${formatDay(next.startUtc)} ${formatTime(next.startUtc)}` : ''}</SectionTitle>
            <p className="mb-2 flex items-start gap-2 text-sm text-muted"><Sparkles className="mt-0.5 size-4 shrink-0 text-brand-600" />AI suggests: {suggestNextFocus(ws, s)}</p>
            <input name="nextFocus" defaultValue={nextFocus} aria-label="Next focus" className={field} />
          </section>

          <p className="flex items-start gap-2 rounded-lg bg-surface-muted p-3 text-sm text-muted"><Eye className="mt-0.5 size-4 shrink-0" />{who === 'the group' ? 'Students' : who} will see topics, homework and next focus, not your notes or the performance rating.</p>
          <div className="flex justify-end gap-2"><Button type="submit">{r ? 'Update report' : 'Submit report'}</Button></div>
        </CardBody></Card>
      </form>
    </div>
  );
}
