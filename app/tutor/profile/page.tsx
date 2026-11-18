import type { Metadata } from 'next';
import { BadgeCheck, MapPin } from 'lucide-react';
import { Tag } from '@/components/marketplace/chip';
import { BOARD_LABEL, DAY_LABEL, FORMAT_LABEL, STYLE_LABEL, WEEKDAYS, clockLabel, subjectLabel, tagLabel } from '@/components/marketplace/labels';
import { getTutor } from '@/components/marketplace/queries';
import { Rating, Stars } from '@/components/marketplace/rating';
import { formatDate } from '@/components/marketplace/dates';
import { Saved, fieldClass } from '@/components/tutor/form-bits';
import { readPrefs, withPrefs } from '@/components/tutor/prefs';
import { SectionTitle } from '@/components/tutor/bits';
import { Avatar } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { saveTutorPrefs } from '@/lib/actions/tutor';
import { formatInr } from '@/lib/format';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Profile · Tutor' };

/** Tutor HTML 8a: the public profile as students see it, with the intro and headline editable in place. */
export default async function PublicProfilePage({ searchParams }: { searchParams: Promise<{ saved?: string; edit?: string }> }) {
  const sp = await searchParams;
  const persona = (await currentPersona())!;
  const prefs = await readPrefs(persona.id);
  const t = withPrefs(getTutor(persona.id)!, prefs);
  const p = t.pricing;
  const grades = [...new Set(t.subjects.flatMap((s) => s.grades))].sort((a, b) => Number(a) - Number(b));
  const days = WEEKDAYS.filter((d) => t.availability.some((a) => a.day === d));
  return (
    <div className="space-y-4">
      <Saved show={sp.saved}>Profile updated.</Saved>
      <Card><CardBody className="space-y-4">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start">
          <Avatar name={t.displayName} size="lg" />
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2"><h2 className="text-xl font-semibold text-ink">{t.displayName}</h2>{t.verified && <span className="inline-flex items-center gap-1 text-sm text-brand-700"><BadgeCheck className="size-4" />Verified</span>}<Rating value={t.rating} count={t.reviewsCount} /></div>
            <p className="mt-1 text-sm text-muted">{t.subjects.map((s) => subjectLabel(s.subjectSlug)).join(', ')} · Class {grades[0]}–{grades.at(-1)} · {[...new Set(t.subjects.flatMap((s) => s.boards))].map((b) => BOARD_LABEL[b as keyof typeof BOARD_LABEL]).join(', ')} · {t.yearsExperience} yrs · <MapPin className="inline size-3.5" /> {t.city} · {t.languages.join(', ')}</p>
            <p className="mt-2 text-sm text-ink">{t.headline}</p>
          </div>
        </div>
        <div className="flex flex-wrap gap-1.5">
          {t.subjects.flatMap((s) => s.topicStrengths.slice(0, 3)).slice(0, 6).map((x) => <Tag key={x}>{tagLabel(x)}</Tag>)}
          {t.teachingStyles.map((x) => <Tag key={x} tone="brand">{STYLE_LABEL[x]}</Tag>)}
        </div>
        <p className="text-sm text-muted">{formatInr(p.oneToOnePerHourInr)} / hr · {p.demoInr === 0 ? 'Free demo' : `Demo ${formatInr(p.demoInr)}`} · {t.formats.map((f) => FORMAT_LABEL[f]).join(' & ')} · {days.map((d) => DAY_LABEL[d]).join(', ')} ({[...new Set(t.availability.map((a) => `${clockLabel(a.start)}–${clockLabel(a.end)}`))].slice(0, 3).join(', ')})</p>
      </CardBody></Card>

      <Card><CardBody>
        <form action={saveTutorPrefs} className="space-y-3">
          <input type="hidden" name="back" value="/tutor/profile" />
          <SectionTitle>Intro {!prefs.bio && <span className="text-sm font-normal text-brand-700">· write your own 2-line intro (+10%)</span>}</SectionTitle>
          <label className="block text-sm text-muted">Headline<input name="f.headline" defaultValue={t.headline} className={`${fieldClass} mt-1`} /></label>
          <label className="block text-sm text-muted">Bio<textarea name="f.bio" rows={3} defaultValue={t.bio} className={`${fieldClass} mt-1`} /></label>
          <div className="flex justify-end"><Button type="submit">Save</Button></div>
        </form>
      </CardBody></Card>

      <Card><CardBody>
        <SectionTitle>Reviews · {t.reviewsCount}</SectionTitle>
        {t.reviews.length ? (
          <ul className="space-y-3">{t.reviews.map((r, i) => <li key={i} className="text-sm"><Stars value={r.rating} /><p className="mt-1 text-ink">“{r.text}”</p><p className="text-xs text-subtle">{r.author} · {formatDate(r.date)}</p></li>)}</ul>
        ) : <p className="text-sm text-muted">No reviews yet. Reviews come from students after 3 sessions.</p>}
        <p className="mt-3 text-xs text-subtle">Reviews come from students after 3+ sessions.</p>
      </CardBody></Card>
    </div>
  );
}
