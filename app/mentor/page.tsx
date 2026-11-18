import Link from 'next/link';
import { CalendarClock, ClipboardList, Compass, Users } from 'lucide-react';
import { mentorContext } from '@/components/mentor/context';
import { careersToPlan } from '@/components/mentor/skill-plan';
import { firstName, fmtDateTime, fmtDateYear, plural } from '@/components/parent/format';
import { Avatar, Badge, Card, CardBody, CardFooter, EmptyState, PageHeader, Progress, StatTile } from '@/components/ui';
import { demoNow, getCareerMatches, getMeetingNotes, getSessions, getTasks } from '@/lib/data';

export default async function MentorHome() {
  const { mentor, mentorName, mentees } = await mentorContext();
  const now = demoNow();
  const rows = mentees.map((m) => {
    const id = m.student.id;
    const open = getTasks(id, undefined, { source: 'mentor' }).filter((t) => t.status === 'todo');
    const next = getSessions(id).find((s) => s.hostId === mentor.id && s.status === 'scheduled' && s.startUtc >= now);
    const last = getMeetingNotes(id, { staffId: mentor.id })[0];
    return { m, open, next, last, careers: careersToPlan(id), fits: getCareerMatches(id)?.fits.slice(0, 3) ?? [] };
  });
  const sessionsThisMonth = getSessions(mentor.id).filter((s) => s.startUtc.slice(0, 7) === now.slice(0, 7)).length;
  const openItems = rows.reduce((a, r) => a + r.open.length, 0);

  return (
    <>
      <PageHeader eyebrow="Mentor" title={`Hi ${firstName(mentorName)}`} description="Your mentees, their career goals and what they owe you next." />
      <section className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatTile label="Mentees" value={mentees.length} icon={<Users />} />
        <StatTile label="Sessions this month" value={sessionsThisMonth} icon={<CalendarClock />} />
        <StatTile label="Open action items" value={openItems} icon={<ClipboardList />} />
        <StatTile label="Careers being planned" value={rows.reduce((a, r) => a + r.careers.length, 0)} icon={<Compass />} />
      </section>
      {!rows.length ? <EmptyState icon={<Users />} title="No mentees yet" description="Students matched to you for career mentoring appear here." /> : (
        <div className="grid gap-4 lg:grid-cols-2">
          {rows.map(({ m, open, next, last, fits }) => (
            <Card key={m.student.id} className="flex flex-col">
              <CardBody className="flex-1 space-y-4">
                <div className="flex items-start gap-3">
                  <Avatar name={m.student.name} size="lg" />
                  <div className="min-w-0">
                    <p className="font-semibold text-ink">{m.student.name}</p>
                    <p className="text-sm text-muted">{m.student.programme}{m.student.city ? ` · ${m.student.city}` : ''}</p>
                    {m.student.goal && <p className="mt-1 text-sm text-ink">Goal: {m.student.goal}</p>}
                  </div>
                </div>
                <div>
                  <p className="mb-2 text-xs font-medium uppercase tracking-wide text-subtle">Top career fits</p>
                  {fits.length ? (
                    <ul className="space-y-2">{fits.map((f) => (
                      <li key={f.careerId} className="flex items-center gap-3 text-sm">
                        <span className="w-40 truncate text-ink">{f.title}</span><Progress value={f.score / 100} className="flex-1" /><span className="w-10 text-right text-xs text-muted">{Math.round(f.score)}</span>
                      </li>
                    ))}</ul>
                  ) : <p className="text-sm text-muted">No career fit run yet.</p>}
                </div>
                <div className="grid gap-2 text-sm sm:grid-cols-2">
                  <p className="text-muted"><span className="font-medium text-ink">Next session: </span>{next ? fmtDateTime(next.startUtc) : 'none booked'}</p>
                  <p className="text-muted"><span className="font-medium text-ink">Last met: </span>{last ? fmtDateYear(last.date) : 'not yet'}</p>
                </div>
                {open.length > 0 && <div className="flex flex-wrap gap-2">{open.slice(0, 3).map((t) => <Badge key={t.id} tone={t.dueDate < now.slice(0, 10) ? 'danger' : 'neutral'}>{t.title}</Badge>)}</div>}
              </CardBody>
              <CardFooter className="flex-wrap">
                <span className="text-muted">{plural(open.length, 'open item')}</span>
                <span className="flex-1" />
                <Link className="font-medium text-brand-600 hover:underline" href={`/mentor/career-sessions?mentee=${m.student.id}`}>Log session</Link>
                <Link className="font-medium text-brand-600 hover:underline" href={`/mentor/skill-plans?mentee=${m.student.id}`}>Skill plan</Link>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </>
  );
}
