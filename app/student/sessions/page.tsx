import Link from 'next/link';
import { Video } from 'lucide-react';
import { Avatar, Badge, Card, CardBody, EmptyState } from '@/components/ui';
import { joinState, people as peopleOf, sessionsOf, studentCtx, whenLabel } from '@/components/student/load';
import { LinkButton } from '@/components/student/link-button';
import { SectionTitle } from '@/components/student/home-cards';
import { cn } from '@/lib/utils';

export const metadata = { title: 'Sessions · Learnibility' };

export default async function SessionsPage({ searchParams }: { searchParams: Promise<{ tab?: string }> }) {
  const { tab: t } = await searchParams;
  const tab = t === 'past' ? 'past' : 'upcoming';
  const ctx = await studentCtx();
  const all = sessionsOf(ctx);
  const people = peopleOf(ctx);
  const list = tab === 'upcoming'
    ? all.filter((s) => s.status === 'scheduled' && joinState(s) !== 'ended')
    : all.filter((s) => s.status !== 'scheduled' || joinState(s) === 'ended').reverse();
  const chip = (active: boolean) => cn('rounded-full px-3 py-1 text-sm ring-1 ring-inset', active ? 'bg-ink text-white ring-ink' : 'bg-surface text-muted ring-line hover:text-ink');

  if (all.length === 0 && people.length === 0) {
    return (
      <>
        <h1 className="mb-6 text-2xl font-semibold tracking-tight text-ink">Sessions</h1>
        <EmptyState icon={<Video />} title="No sessions yet" description="Book a free demo with a tutor, or talk to a counsellor about your plan."
          action={<div className="flex flex-wrap justify-center gap-2"><LinkButton href="/student/tutors">Find a tutor</LinkButton><LinkButton href="/student/tutors?counsellor=1" variant="secondary">Book a free counsellor call</LinkButton></div>} />
      </>
    );
  }

  return (
    <>
      <div className="mb-4 flex items-center justify-between gap-3">
        <h1 className="text-2xl font-semibold tracking-tight text-ink">Sessions</h1>
        <div className="flex gap-2">
          <Link href="/student/sessions" className={chip(tab === 'upcoming')}>Upcoming</Link>
          <Link href="/student/sessions?tab=past" className={chip(tab === 'past')}>Past</Link>
        </div>
      </div>

      <Card>
        {list.length === 0 ? (
          <p className="p-8 text-center text-sm text-muted">{tab === 'upcoming' ? 'Nothing booked. Ask your counsellor for a slot or book a tutor demo.' : 'No past sessions yet.'}</p>
        ) : (
          <ul className="divide-y divide-line">
            {list.map((s) => {
              const js = joinState(s);
              return (
                <li key={s.id} className="flex flex-col gap-3 p-4 sm:flex-row sm:items-center">
                  <Avatar name={s.personName} />
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-semibold text-ink">{s.personName} · {s.roleLabel} <span className="font-normal text-subtle">{s.label}</span></p>
                    <p className="text-sm text-muted">{whenLabel(s.startUtc)} · {s.platform}{s.topic ? ` · Topic: ${s.topic}` : ''}</p>
                    {tab === 'past' && s.summary && <p className="mt-1 text-sm text-ink">{s.summary}</p>}
                  </div>
                  {tab === 'upcoming' ? (
                    js === 'open'
                      ? <LinkButton href={`/student/sessions/${s.personId}?join=${s.id}`} size="sm">Join</LinkButton>
                      : <span className="rounded-lg border border-dashed border-line px-3 py-1.5 text-xs text-subtle">Join opens 10 min before</span>
                  ) : (
                    <Badge tone={s.status === 'completed' ? 'success' : 'neutral'}>{s.status === 'completed' ? 'Summary ready' : s.status}</Badge>
                  )}
                </li>
              );
            })}
          </ul>
        )}
      </Card>

      <SectionTitle title="Your people" />
      {people.length === 0 ? (
        <EmptyState title="No counsellor, tutor or mentor yet" description="Book a demo to start working with someone." action={<LinkButton href="/student/tutors">Find a tutor</LinkButton>} />
      ) : (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {people.map((p) => (
            <Link key={p.id} href={`/student/sessions/${p.id}`} className="group">
              <Card className="h-full transition-colors group-hover:border-brand-300">
                <CardBody>
                  <p className="text-xs font-medium uppercase tracking-wide text-subtle">{p.role}</p>
                  <div className="mt-2 flex items-center gap-3">
                    <Avatar name={p.name} />
                    <div>
                      <p className="text-sm font-semibold text-ink">{p.name}</p>
                      <p className="text-xs text-muted">{p.focus} · {p.sessionCount} sessions</p>
                    </div>
                  </div>
                  <p className="mt-3 text-sm font-medium text-brand-700">See more →</p>
                </CardBody>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </>
  );
}
