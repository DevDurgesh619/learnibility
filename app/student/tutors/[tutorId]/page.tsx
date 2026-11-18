import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { BadgeCheck, CalendarClock, ChevronLeft, Clock, GraduationCap, Languages, MapPin, Sparkles } from 'lucide-react';
import { Tag } from '@/components/marketplace/chip';
import { AUDIENCE_LABEL, BOARD_LABEL, DAY_LABEL, FORMAT_LABEL, HELP_LABEL, MODE_LABEL, STYLE_LABEL, clockLabel, subjectLabel, tagLabel } from '@/components/marketplace/labels';
import { getTutor, loadMarketplaceLearner } from '@/components/marketplace/queries';
import { Rating, Stars } from '@/components/marketplace/rating';
import { formatDate } from '@/components/marketplace/dates';
import { BookingStatusBadge } from '@/components/marketplace/booking-status';
import { Avatar } from '@/components/ui/avatar';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { formatInr } from '@/lib/format';
import { currentPersona } from '@/lib/session';
import { WEEKDAYS } from '@/components/marketplace/labels';

export async function generateMetadata({ params }: { params: Promise<{ tutorId: string }> }): Promise<Metadata> {
  const t = getTutor((await params).tutorId);
  return { title: `${t?.displayName ?? 'Tutor'} · Explore Tutors` };
}

export default async function TutorProfilePage({ params }: { params: Promise<{ tutorId: string }> }) {
  const { tutorId } = await params;
  const tutor = getTutor(tutorId);
  if (!tutor) notFound();
  const persona = await currentPersona();
  const learner = persona ? await loadMarketplaceLearner(persona.id) : undefined;
  const match = learner?.matches.find((m) => m.tutorId === tutor.id);
  const open = learner?.bookings.find((b) => b.tutorId === tutor.id && (b.status === 'requested' || b.status === 'accepted' || b.status === 'active'));
  const p = tutor.pricing;
  const byDay = WEEKDAYS.map((d) => ({ d, slots: tutor.availability.filter((a) => a.day === d) })).filter((x) => x.slots.length);

  return (
    <>
      <Link href="/student/tutors" className="mb-4 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" /> Explore Tutors</Link>

      <Card className="p-5 sm:p-6">
        <div className="flex flex-col gap-5 sm:flex-row sm:items-start">
          <Avatar name={tutor.displayName} size="lg" />
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <h1 className="text-2xl font-semibold tracking-tight text-ink">{tutor.displayName}</h1>
              {tutor.verified && <span className="inline-flex items-center gap-1 text-sm text-brand-700"><BadgeCheck className="size-4" /> Verified</span>}
            </div>
            <p className="mt-1 text-sm text-muted">{tutor.headline}</p>
            <div className="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-muted">
              <Rating value={tutor.rating} count={tutor.reviewsCount} />
              <span>{tutor.yearsExperience} yrs</span>
              <span className="inline-flex items-center gap-1"><MapPin className="size-3.5" />{tutor.city}</span>
              <span className="inline-flex items-center gap-1"><Languages className="size-3.5" />{tutor.languages.join(', ')}</span>
              <span>{tutor.rebookPct}% rebook · replies in ~{tutor.responseTimeHours} h</span>
            </div>
            <div className="mt-3 flex flex-wrap gap-1.5">
              {tutor.subjects.flatMap((s) => s.topicStrengths.slice(0, 4)).slice(0, 8).map((tg) => <Tag key={tg}>{tagLabel(tg)}</Tag>)}
              {tutor.teachingStyles.slice(0, 1).map((s) => <Tag key={s} tone="brand">{STYLE_LABEL[s]}</Tag>)}
            </div>
          </div>
          <div className="flex shrink-0 flex-col items-stretch gap-2 sm:items-end">
            {open ? (
              <>
                <BookingStatusBadge status={open.status} />
                <Link href={`/student/tutors/booked/${open.id}`} className={buttonVariants({ variant: 'secondary' })}>View booking</Link>
              </>
            ) : (
              <Link href={`/student/tutors/${tutor.id}/book`} className={buttonVariants()}>
                <CalendarClock /> {p.demoInr === 0 ? `Book a free ${p.demoMinutes}-min demo` : `Book a demo · ${formatInr(p.demoInr)}`}
              </Link>
            )}
          </div>
        </div>
        {match && (
          <p className="mt-5 flex gap-2 rounded-lg bg-brand-50/70 p-3 text-sm text-brand-800">
            <Sparkles className="mt-0.5 size-4 shrink-0" />
            <span><span className="font-medium">Why we suggest {tutor.firstName}:</span> {match.reason}</span>
          </p>
        )}
      </Card>

      <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_1fr]">
        <div className="space-y-6">
          <Card>
            <CardHeader title="Ways to learn" />
            <CardBody className="space-y-3">
              {tutor.formats.includes('one_to_one') && (
                <div className="rounded-lg border border-line p-3">
                  <p className="font-medium text-ink">1-on-1 · {formatInr(p.oneToOnePerHourInr)}/hr</p>
                  <p className="text-sm text-muted">{tutor.sessionMinutes}-min sessions, your topics, flexible slots</p>
                </div>
              )}
              {tutor.formats.includes('group') && p.groupPerStudentPerHourInr && (
                <div className="rounded-lg border border-line p-3">
                  <p className="font-medium text-ink">Group of {p.groupSize?.[0]}–{p.groupSize?.[1]} · {formatInr(p.groupPerStudentPerHourInr)}/hr per student</p>
                  <p className="text-sm text-muted">Small batches at fixed times</p>
                </div>
              )}
              {p.packages.map((pk) => (
                <div key={pk.label} className="rounded-lg border border-line p-3">
                  <p className="font-medium text-ink">{pk.label} · {formatInr(pk.priceInr)}</p>
                  <p className="text-sm text-muted">{pk.sessions} sessions · {formatInr(Math.round(pk.priceInr / pk.sessions))} a session</p>
                </div>
              ))}
              <p className="text-xs text-muted">{tutor.modes.map((m) => MODE_LABEL[m]).join(' or ')}{tutor.offlineArea ? ` (${tutor.offlineArea})` : ''} · demo {p.demoInr === 0 ? 'free' : formatInr(p.demoInr)}, {p.demoMinutes} min</p>
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="About" />
            <CardBody className="space-y-4 text-sm">
              <p className="text-ink">{tutor.bio}</p>
              <dl className="grid gap-3 sm:grid-cols-2">
                <Fact icon={<GraduationCap />} label="Qualifications" value={tutor.qualifications.join(' · ')} />
                <Fact label="Teaches" value={tutor.subjects.map((s) => `${subjectLabel(s.subjectSlug)} (${s.boards.map((b) => BOARD_LABEL[b]).join(', ')}, class ${Math.min(...s.grades)}–${Math.max(...s.grades)})`).join('; ')} />
                <Fact label="Best for" value={tutor.audiences.map((a) => AUDIENCE_LABEL[a]).join(', ')} />
                <Fact label="Help with" value={tutor.helpTypes.map((h) => HELP_LABEL[h]).join(', ')} />
                <Fact label="Style" value={tutor.teachingStyles.map((s) => STYLE_LABEL[s]).join(', ')} />
                <Fact label="Format" value={tutor.formats.map((f) => FORMAT_LABEL[f]).join(', ')} />
              </dl>
              <p className="rounded-lg bg-surface-muted p-3 text-muted"><span className="font-medium text-ink">Ideal student:</span> {tutor.idealStudent}</p>
            </CardBody>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader title="What students say" description={`${tutor.reviewsCount} reviews · ${tutor.sessionsCompleted} sessions taught`} />
            <CardBody className="space-y-3">
              {tutor.reviews.length === 0 && <p className="text-sm text-muted">No written reviews yet.</p>}
              {tutor.reviews.map((r, i) => (
                <figure key={i} className="rounded-lg border border-line p-3">
                  <div className="flex items-center justify-between"><Stars value={r.rating} /><span className="text-xs text-subtle">{formatDate(r.date)}</span></div>
                  <blockquote className="mt-1.5 text-sm text-ink">“{r.text}”</blockquote>
                  <figcaption className="mt-1 text-xs text-muted">— {r.author}</figcaption>
                </figure>
              ))}
            </CardBody>
          </Card>
          <Card>
            <CardHeader title="Weekly hours" description="Times are IST. Demo slots only show times you're both free." />
            <CardBody>
              <ul className="space-y-1.5 text-sm">
                {byDay.map(({ d, slots }) => (
                  <li key={d} className="flex gap-3"><span className="w-10 font-medium text-ink">{DAY_LABEL[d]}</span><span className="text-muted">{slots.map((s) => `${clockLabel(s.start)}–${clockLabel(s.end)}`).join(', ')}</span></li>
                ))}
              </ul>
              <p className="mt-3 flex items-center gap-1.5 text-xs text-muted"><Clock className="size-3.5" /> Up to {tutor.maxSessionsPerDay} sessions a day</p>
            </CardBody>
          </Card>
        </div>
      </div>
    </>
  );
}

function Fact({ label, value, icon }: { label: string; value: string; icon?: React.ReactNode }) {
  return (
    <div>
      <dt className="flex items-center gap-1 text-xs font-medium uppercase tracking-wide text-muted [&_svg]:size-3.5">{icon}{label}</dt>
      <dd className="mt-0.5 text-ink">{value}</dd>
    </div>
  );
}
