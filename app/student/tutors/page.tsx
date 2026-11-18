import type { Metadata } from 'next';
import Link from 'next/link';
import { ClipboardList, SearchX, Users } from 'lucide-react';
import { ExploreSearch } from '@/components/marketplace/explore-search';
import { RemovableChip } from '@/components/marketplace/chip';
import { BOARD_LABEL, FORMAT_LABEL, MODE_LABEL, subjectLabel } from '@/components/marketplace/labels';
import { loadMarketplaceLearner, listTutors, getTutor } from '@/components/marketplace/queries';
import { activeFilterCount, filterTutors, filtersToParams, moreLikeThese, parseFilters, type TutorFilters } from '@/components/marketplace/search';
import { TutorCard } from '@/components/marketplace/tutor-card';
import { BookingStatusBadge } from '@/components/marketplace/booking-status';
import { Avatar } from '@/components/ui/avatar';
import { buttonVariants } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import { PageHeader } from '@/components/ui/page-header';
import { formatDateTime } from '@/components/marketplace/dates';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Explore Tutors · Learnibility' };

const BASE = '/student/tutors';

export default async function ExploreTutorsPage({ searchParams }: { searchParams: Promise<Record<string, string | string[] | undefined>> }) {
  const sp = await searchParams;
  const persona = await currentPersona();
  const learner = persona ? await loadMarketplaceLearner(persona.id) : undefined;
  const filters = parseFilters(sp);
  const searching = !!filters.q || activeFilterCount(filters) > 0;
  const all = listTutors();
  const subjects = [...new Set(all.flatMap((t) => t.subjects.map((s) => s.subjectSlug)))].sort();
  const languages = [...new Set(all.flatMap((t) => t.languages))].sort((a, b) => (a === 'English' ? -1 : b === 'English' ? 1 : a.localeCompare(b))).slice(0, 8);
  const matchById = new Map((learner?.matches ?? []).map((m) => [m.tutorId, m]));

  return (
    <>
      <PageHeader title="Explore Tutors" description="Tutors matched to your gaps, the way you learn, your budget and your free time." />
      <ExploreSearch base={BASE} initial={filters} subjects={subjects} languages={languages} openByDefault={sp.filters === '1'} />
      {searching ? <Results filters={filters} all={all} matchById={matchById} /> : <Home learner={learner} matchById={matchById} />}
    </>
  );
}

async function Home({ learner, matchById }: { learner: Awaited<ReturnType<typeof loadMarketplaceLearner>>; matchById: Map<string, { reason: string; score: number }> }) {
  const bookings = (learner?.bookings ?? []).filter((b) => b.status !== 'declined' && b.status !== 'cancelled');
  const current = bookings.filter((b) => b.status === 'active' || b.status === 'accepted' || b.status === 'completed');
  const pending = bookings.filter((b) => b.status === 'requested');
  const currentTutors = [...new Set(current.map((b) => b.tutorId))].map((id) => getTutor(id)).filter((t) => !!t);
  const recommended = (learner?.matches ?? []).slice(0, 6).map((m) => ({ m, t: getTutor(m.tutorId) })).filter((x) => !!x.t);

  return (
    <div className="mt-8 space-y-10">
      {pending.length > 0 && (
        <section>
          <SectionTitle title="Your demo requests" />
          <div className="grid gap-3 md:grid-cols-2">
            {pending.map((b) => {
              const t = getTutor(b.tutorId);
              return (
                <Link key={b.id} href={`${BASE}/booked/${b.id}`}>
                  <Card className="flex items-center gap-3 p-4 hover:border-brand-300">
                    <Avatar name={t?.displayName ?? b.tutorId} personId={b.tutorId} size="sm" photo />
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-sm font-medium text-ink">{t?.displayName} · demo</p>
                      <p className="text-xs text-muted">{b.slotStartUtc ? formatDateTime(b.slotStartUtc) : 'Time to be agreed'}</p>
                    </div>
                    <BookingStatusBadge status={b.status} />
                  </Card>
                </Link>
              );
            })}
          </div>
        </section>
      )}

      <section>
        <SectionTitle title="Currently studying with" />
        {currentTutors.length === 0 ? (
          <p className="rounded-lg border border-dashed border-line p-4 text-sm text-muted">No tutors yet. Book a free demo with one of the tutors below; nothing is charged until you continue after the demo.</p>
        ) : (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {currentTutors.map((t) => (
              <Link key={t.id} href={`${BASE}/${t.id}`}>
                <Card className="flex items-center gap-3 p-4 hover:border-brand-300">
                  <Avatar name={t.displayName} personId={t.id} photo />
                  <div className="min-w-0">
                    <p className="truncate font-medium text-ink">{t.displayName}</p>
                    <p className="truncate text-xs text-muted">{t.subjects.map((s) => subjectLabel(s.subjectSlug)).join(', ')} tutor</p>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        )}
      </section>

      <section>
        <SectionTitle title="Recommended for you" hint="based on your gap analysis" />
        {recommended.length === 0 ? (
          <EmptyState
            icon={<ClipboardList />}
            title="Take a test to get matched"
            description="We match tutors to your open gaps. Once a chapter check or the onboarding test shows where you need help, your best-fit tutors appear here."
            action={<Link href="/student/assessments" className={buttonVariants()}>Go to Assessments</Link>}
          />
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {recommended.map(({ m, t }) => <TutorCard key={t!.id} tutor={t!} reason={m.reason} score={m.score} href={`${BASE}/${t!.id}`} />)}
          </div>
        )}
      </section>
    </div>
  );
}

function Results({ filters, all, matchById }: { filters: TutorFilters; all: ReturnType<typeof listTutors>; matchById: Map<string, { reason: string; score: number }> }) {
  const found = filterTutors(all, filters).sort((a, b) => (matchById.get(b.id)?.score ?? 0) - (matchById.get(a.id)?.score ?? 0) || b.rating - a.rating || b.reviewsCount - a.reviewsCount);
  const more = moreLikeThese(all, found.length ? found.slice(0, 6) : [], 3);
  const chips = chipList(filters);
  return (
    <div className="mt-4 space-y-8">
      <div className="flex flex-wrap items-center gap-2">
        {chips.map((c) => <RemovableChip key={c.key} href={c.href}>{c.label}</RemovableChip>)}
        <span className="text-sm text-muted">{found.length} {found.length === 1 ? 'tutor' : 'tutors'}</span>
      </div>
      {found.length === 0 ? (
        <EmptyState icon={<SearchX />} title="No tutors match all of that" description="Try removing a filter or searching a broader subject." action={<Link href={BASE} className={buttonVariants({ variant: 'secondary' })}>Clear search</Link>} />
      ) : (
        <section>
          <SectionTitle title="Best match for your preferences" />
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {found.slice(0, 12).map((t) => <TutorCard key={t.id} tutor={t} reason={matchById.get(t.id)?.reason} href={`${BASE}/${t.id}`} />)}
          </div>
          {found.length > 12 && <p className="mt-3 text-sm text-muted">Showing 12 of {found.length}. Add a filter to narrow it down.</p>}
        </section>
      )}
      {more.length > 0 && (
        <section>
          <SectionTitle title="More like these" />
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {more.map((t) => <TutorCard key={t.id} tutor={t} href={`${BASE}/${t.id}`} compact />)}
          </div>
        </section>
      )}
      {all.length === 0 && <EmptyState icon={<Users />} title="No tutors listed yet" />}
    </div>
  );
}

function chipList(f: TutorFilters) {
  const without = (k: keyof TutorFilters) => {
    const p = filtersToParams({ ...f, [k]: undefined });
    return p.size ? `${BASE}?${p}` : BASE;
  };
  const out: { key: string; label: string; href: string }[] = [];
  if (f.subject) out.push({ key: 'subject', label: subjectLabel(f.subject), href: without('subject') });
  if (f.board) out.push({ key: 'board', label: BOARD_LABEL[f.board], href: without('board') });
  if (f.minRating) out.push({ key: 'rating', label: `★ ${f.minRating}+`, href: without('minRating') });
  if (f.maxPrice) out.push({ key: 'price', label: `< ₹${f.maxPrice.toLocaleString('en-IN')}/hr`, href: without('maxPrice') });
  if (f.format) out.push({ key: 'format', label: FORMAT_LABEL[f.format], href: without('format') });
  if (f.mode) out.push({ key: 'mode', label: MODE_LABEL[f.mode], href: without('mode') });
  if (f.language) out.push({ key: 'lang', label: f.language, href: without('language') });
  if (f.verified) out.push({ key: 'verified', label: 'Verified', href: without('verified') });
  return out;
}

function SectionTitle({ title, hint }: { title: string; hint?: string }) {
  return (
    <h2 className="mb-3 border-b border-line pb-2 text-base font-semibold text-ink">
      {title}{hint && <span className="ml-2 text-sm font-normal text-muted">· {hint}</span>}
    </h2>
  );
}
