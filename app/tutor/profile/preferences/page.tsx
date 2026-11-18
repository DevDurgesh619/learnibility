import type { Metadata } from 'next';
import { AUDIENCE_LABEL, FORMAT_LABEL, HELP_LABEL, HOMEWORK_LABEL, MODE_LABEL, STYLE_LABEL, subjectLabel } from '@/components/marketplace/labels';
import { getTutor } from '@/components/marketplace/queries';
import { CheckChips, Saved, fieldClass } from '@/components/tutor/form-bits';
import { readPrefs, withPrefs } from '@/components/tutor/prefs';
import { SectionTitle } from '@/components/tutor/bits';
import { Tag } from '@/components/marketplace/chip';
import { Button } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { saveTutorPrefs } from '@/lib/actions/tutor';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Teaching preferences · Tutor' };

const opts = <K extends string>(r: Record<K, string>) => Object.entries(r) as [string, string][];

/** Tutor HTML 8b: subjects and levels, who and what, style and format, ideal student. Same controls as onboarding 1d. */
export default async function PreferencesPage({ searchParams }: { searchParams: Promise<{ saved?: string }> }) {
  const sp = await searchParams;
  const persona = (await currentPersona())!;
  const t = withPrefs(getTutor(persona.id)!, await readPrefs(persona.id));
  return (
    <form action={saveTutorPrefs}>
      <input type="hidden" name="back" value="/tutor/profile/preferences" />
      <Saved show={sp.saved}>Preferences saved.</Saved>
      <Card><CardBody className="space-y-6">
        <section>
          <SectionTitle>Subjects and levels</SectionTitle>
          <div className="space-y-2">{t.subjects.map((s) => <p key={s.subjectSlug} className="flex flex-wrap items-center gap-2 text-sm"><span className="font-medium text-ink">{subjectLabel(s.subjectSlug)}</span>{s.grades.map((g) => <Tag key={g}>Class {g}</Tag>)}</p>)}</div>
          <p className="mt-2 text-xs text-subtle">Adding a subject goes through a short check by the Learnibility team.</p>
        </section>
        <section className="space-y-3">
          <SectionTitle>Who and what</SectionTitle>
          <CheckChips name="audiences" options={opts(AUDIENCE_LABEL)} selected={t.audiences} />
          <CheckChips name="helpTypes" options={opts(HELP_LABEL)} selected={t.helpTypes} />
        </section>
        <section className="space-y-3">
          <SectionTitle>Style and format</SectionTitle>
          <CheckChips name="teachingStyles" options={opts(STYLE_LABEL)} selected={t.teachingStyles} />
          <div className="flex flex-wrap gap-6">
            <div><p className="mb-1 text-sm text-muted">Format</p><CheckChips name="formats" options={opts(FORMAT_LABEL)} selected={t.formats} /></div>
            <div><p className="mb-1 text-sm text-muted">Mode</p><CheckChips name="modes" options={opts(MODE_LABEL)} selected={t.modes} /></div>
            <div><p className="mb-1 text-sm text-muted">Homework</p><CheckChips type="radio" name="homework" options={opts(HOMEWORK_LABEL)} selected={[t.homework]} /></div>
          </div>
        </section>
        <section>
          <label htmlFor="ideal" className="mb-1 block text-base font-semibold text-ink">Your ideal student</label>
          <textarea id="ideal" name="f.idealStudent" rows={3} defaultValue={t.idealStudent} className={fieldClass} />
          <p className="mt-1 text-xs text-subtle">Used to match you in Explore Tutors and gap-analysis recommendations.</p>
        </section>
        <div className="flex justify-end"><Button type="submit">Save</Button></div>
      </CardBody></Card>
    </form>
  );
}
