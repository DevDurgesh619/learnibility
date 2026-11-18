import Link from 'next/link';
import { notFound } from 'next/navigation';
import { ChevronLeft, MessageSquare, Video } from 'lucide-react';
import { Avatar, Button, Card, CardBody, CardHeader } from '@/components/ui';
import { fmtDay, joinState, people, mainCounsellor, sessionsOf, studentCtx, todosFrom, whenLabel } from '@/components/student/load';
import { LinkButton } from '@/components/student/link-button';
import { TodoList } from '@/components/student/todo-list';

export const metadata = { title: 'Sessions · Learnibility' };

/** PDF 10b: one counsellor, tutor or mentor: history with Join / View summary, and their to-dos. */
export default async function PersonPage({ params, searchParams }: { params: Promise<{ personId: string }>; searchParams: Promise<{ join?: string; summary?: string }> }) {
  const { personId } = await params;
  const sp = await searchParams;
  const ctx = await studentCtx();
  const person = people(ctx).find((p) => p.id === personId);
  if (!person) notFound();
  const history = sessionsOf(ctx).filter((s) => s.personId === personId).reverse();
  const first = person.name.split(' ')[0]!;
  const since = new Intl.DateTimeFormat('en-IN', { month: 'short', year: 'numeric', timeZone: 'UTC' }).format(new Date(person.sinceUtc));
  const joining = history.find((s) => s.id === sp.join && joinState(s) === 'open');
  const isCounsellor = person.role === 'counsellor' && mainCounsellor(ctx)?.id === person.id && ctx.hasCounsellor;

  return (
    <>
      <Link href="/student/sessions" className="mb-3 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" />Sessions</Link>
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center">
        <Avatar name={person.name} size="lg" />
        <div className="min-w-0 flex-1">
          <h1 className="text-2xl font-semibold tracking-tight text-ink">{person.name}</h1>
          <p className="text-sm text-muted">Your {person.focus.toLowerCase()} · since {since} · {person.sessionCount} sessions</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button variant="secondary" size="sm" disabled title="Messages open from your parent and counsellor apps"><MessageSquare />Message</Button>
          {isCounsellor && <LinkButton href="/student/timetable?request=1" variant="secondary" size="sm" className="border-brand-300 text-brand-700">Request schedule change</LinkButton>}
        </div>
      </div>

      {joining && (
        <Card className="mb-4 border-success-600/40 bg-success-50/50">
          <CardBody className="flex items-center gap-3 text-sm">
            <Video className="size-5 text-success-700" />
            <p className="flex-1 text-ink">Demo: this would open {joining.platform} for <span className="font-medium">{joining.title}</span>. The session starts {whenLabel(joining.startUtc).toLowerCase()}.</p>
          </CardBody>
        </Card>
      )}

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title="History" />
          <CardBody className="pt-2">
            {history.length === 0 ? <p className="py-6 text-center text-sm text-muted">No sessions with {first} yet.</p> : (
              <ul className="divide-y divide-line">
                {history.map((s) => {
                  const js = joinState(s);
                  const open = sp.summary === s.id;
                  return (
                    <li key={s.id} className="py-2.5">
                      <div className="flex items-center gap-3">
                        <p className="min-w-0 flex-1 text-sm text-ink">{s.label} · {whenLabel(s.startUtc)}{s.topic ? <span className="text-muted"> · {s.topic}</span> : null}</p>
                        {s.status === 'scheduled' && js !== 'ended'
                          ? (js === 'open' ? <LinkButton href={`?join=${s.id}`} size="sm">Join</LinkButton> : <span className="text-xs text-subtle">Join opens 10 min before</span>)
                          : s.summary ? <LinkButton href={open ? '?' : `?summary=${s.id}`} variant="secondary" size="sm">{open ? 'Hide summary' : 'View summary'}</LinkButton> : <span className="text-xs text-subtle">{s.status}</span>}
                      </div>
                      {open && s.summary && <p className="mt-2 rounded-lg bg-surface-muted p-3 text-sm text-ink">{s.summary}</p>}
                    </li>
                  );
                })}
              </ul>
            )}
          </CardBody>
        </Card>
        <Card>
          <CardHeader title={`To-dos from ${first}`} />
          <CardBody className="pt-2">
            <TodoList personFirstName={first} todos={todosFrom(ctx, person.id).map((t) => ({ ...t, dueLabel: t.dueOn ? fmtDay(t.dueOn) : undefined }))} />
          </CardBody>
        </Card>
      </div>
    </>
  );
}
