import { CalendarClock, CheckCircle2, ClipboardList, NotebookPen } from 'lucide-react';
import { saveCareerSession } from '@/lib/actions/mentor';
import { mentorContext } from '@/components/mentor/context';
import { MenteeSwitcher } from '@/components/mentor/mentee-switcher';
import { fmtDateTime, fmtDateYear } from '@/components/parent/format';
import { Notice } from '@/components/parent/notice';
import { Badge, Button, Card, CardBody, CardHeader, EmptyState, PageHeader } from '@/components/ui';
import { addDaysLocal, demoNow, demoToday, getMeetingNotes, getSessions, getTasks } from '@/lib/data';
import { careersToPlan } from '@/components/mentor/skill-plan';

const input = 'mt-1 block w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm text-ink outline-none focus:border-brand-400';

export default async function CareerSessions({ searchParams }: { searchParams: Promise<Record<string, string | string[] | undefined>> }) {
  const sp = await searchParams;
  const { mentor, mentees, mentee } = await mentorContext(searchParams);
  if (!mentee) return (<><PageHeader eyebrow="Mentor" title="Career sessions" /><EmptyState title="No mentees yet" /></>);
  const id = mentee.student.id;
  const now = demoNow();
  const sessions = getSessions(id).filter((s) => s.hostId === mentor.id);
  const upcoming = sessions.filter((s) => s.status === 'scheduled' && s.startUtc >= now);
  const toLog = sessions.filter((s) => !s.meetingNoteId && s.startUtc.slice(0, 10) <= demoToday() && s.status !== 'cancelled');
  const notes = getMeetingNotes(id, { staffId: mentor.id }).filter((n) => n.tier !== 'T3');
  const tasks = new Map(getTasks(id).map((t) => [t.id, t]));
  const careers = careersToPlan(id);
  const saved = typeof sp.saved === 'string' ? sp.saved : undefined;
  const due = addDaysLocal(demoToday(), 7);

  return (
    <>
      <PageHeader eyebrow="Mentor" title="Career sessions" description="Session notes and action items. Each action item becomes a task in your mentee's timetable." />
      <MenteeSwitcher mentees={mentees} selectedId={id} basePath="/mentor/career-sessions" />
      {saved && <Notice>Session saved. The action items are now in {mentee.student.firstName}&apos;s tasks.</Notice>}

      <div className="grid gap-6 lg:grid-cols-5">
        <div className="space-y-6 lg:col-span-3">
          <Card>
            <CardHeader title={`Upcoming with ${mentee.student.firstName}`} />
            <CardBody className="pt-3">
              {upcoming.length ? (
                <ul className="divide-y divide-line">{upcoming.map((s) => (
                  <li key={s.id} className="flex items-center gap-3 py-3 first:pt-0"><CalendarClock className="size-4 text-brand-600" /><div className="min-w-0 flex-1"><p className="text-sm font-medium text-ink">{s.title}</p><p className="text-xs text-muted">{fmtDateTime(s.startUtc)} · {s.minutes} min · {s.mode}</p></div>{s.focus && <Badge tone="brand">{s.focus}</Badge>}</li>
                ))}</ul>
              ) : <p className="text-sm text-muted">No session booked. Book one from Messages.</p>}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Session history" description="Newest first" />
            <CardBody className="space-y-4 pt-3">
              {notes.length ? notes.map((n) => (
                <article key={n.id} className={`rounded-lg border p-4 ${n.id === saved ? 'border-success-600/30 bg-success-50' : 'border-line'}`}>
                  <div className="mb-2 flex flex-wrap items-center gap-2"><NotebookPen className="size-4 text-subtle" /><p className="text-sm font-semibold text-ink">{fmtDateYear(n.date)}</p><Badge>{n.kind}</Badge></div>
                  <p className="text-sm text-ink">{n.summary}</p>
                  {n.decisions.length > 0 && <ul className="mt-2 list-disc space-y-0.5 pl-5 text-sm text-muted">{n.decisions.map((d, i) => <li key={i}>{d}</li>)}</ul>}
                  {n.actionItems.length > 0 && (
                    <ul className="mt-3 space-y-1.5">{n.actionItems.map((a) => {
                      const t = a.taskId ? tasks.get(a.taskId) : undefined;
                      const isDone = t ? t.status === 'done' : a.done;
                      return (
                        <li key={a.id} className="flex items-center gap-2 text-sm">
                          {isDone ? <CheckCircle2 className="size-4 text-success-600" /> : <ClipboardList className="size-4 text-subtle" />}
                          <span className={isDone ? 'text-muted line-through' : 'text-ink'}>{a.title}</span>
                          <span className="text-xs text-subtle">due {fmtDateYear(a.dueOn)}</span>
                        </li>
                      );
                    })}</ul>
                  )}
                </article>
              )) : <EmptyState className="border-0" icon={<NotebookPen />} title="No sessions logged yet" description="Log your first career session on the right." />}
            </CardBody>
          </Card>
        </div>

        <Card className="h-fit lg:col-span-2">
          <CardHeader title="Log a session" description={careers.length ? `Careers in play: ${careers.map((c) => c.title).join(', ')}` : undefined} />
          <CardBody>
            <form action={saveCareerSession} className="space-y-4">
              <input type="hidden" name="learnerId" value={id} />
              {toLog.length > 0 && (
                <label className="block text-sm font-medium text-ink">Session
                  <select name="sessionId" className={input}><option value="">Not linked to a booked session</option>{toLog.map((s) => <option key={s.id} value={s.id}>{s.title}, {fmtDateYear(s.startUtc)}</option>)}</select>
                </label>
              )}
              <label className="block text-sm font-medium text-ink">Date<input type="date" name="date" defaultValue={demoToday()} className={input} /></label>
              <label className="block text-sm font-medium text-ink">Summary<textarea name="summary" required rows={3} className={input} placeholder="What you discussed and where they are now" /></label>
              <label className="block text-sm font-medium text-ink">Decisions <span className="font-normal text-subtle">(one per line)</span><textarea name="decisions" rows={2} className={input} /></label>
              <fieldset className="space-y-2">
                <legend className="text-sm font-medium text-ink">Action items</legend>
                {[0, 1, 2].map((i) => (
                  <div key={i} className="grid grid-cols-[1fr_9rem] gap-2">
                    <input name={`item${i}`} aria-label={`Action item ${i + 1}`} placeholder={i === 0 ? 'e.g. Finish the Excel basics course' : 'Another action item'} className={input.replace('mt-1 ', '')} />
                    <input type="date" name={`due${i}`} aria-label={`Due date ${i + 1}`} defaultValue={due} className={input.replace('mt-1 ', '')} />
                  </div>
                ))}
              </fieldset>
              <Button type="submit" className="w-full"><NotebookPen />Save session and send tasks</Button>
            </form>
          </CardBody>
        </Card>
      </div>
    </>
  );
}
