'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Check, ChevronLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { saveProfile } from '@/lib/actions/onboarding';
import type { OnboardingDraft } from './draft';
import { Field, Select, TextInput } from './field';

export function ProfileForm({ draft, subjects }: { draft: OnboardingDraft; subjects: { id: string; name: string }[] }) {
  const [hard, setHard] = useState<string[]>(draft.hardSubjects ?? []);
  const [sat, setSat] = useState<string>(draft.satStatus ?? '');
  const toggle = (id: string) => setHard((h) => (h.includes(id) ? h.filter((x) => x !== id) : h.length >= 3 ? h : [...h, id]));
  const showSat = (draft.grade ?? 0) >= 10 || draft.target === 'sat_act' || draft.target === 'study_abroad';
  return (
    <form action={saveProfile} className="mt-6 flex flex-col gap-4">
      <div className="grid gap-4 sm:grid-cols-[1fr_180px]">
        <Field label="Current school">
          <TextInput name="school" defaultValue={draft.school} placeholder="e.g. Delhi Public School, Pune" />
        </Field>
        <Field label="Last exam %">
          <TextInput name="lastExamPercent" defaultValue={draft.lastExamPercent} inputMode="decimal" placeholder="e.g. 78" />
        </Field>
      </div>
      <fieldset className="flex flex-col gap-2 text-sm">
        <legend className="mb-1.5 font-medium text-ink">Subjects you find hard <span className="font-normal text-subtle">(pick up to 3)</span></legend>
        <div className="flex flex-wrap gap-2">
          {subjects.map((s) => {
            const on = hard.includes(s.id);
            return (
              <button key={s.id} type="button" aria-pressed={on} onClick={() => toggle(s.id)}
                className={cn('inline-flex items-center gap-1 rounded-full border px-3 py-1.5 text-sm transition', on ? 'border-brand-500 bg-brand-50 text-brand-700' : 'border-line bg-surface text-muted hover:border-brand-300')}>
                {on && <Check className="size-3.5" />} {s.name}
                {on && <input type="hidden" name="hardSubjects" value={s.id} />}
              </button>
            );
          })}
          {subjects.length === 0 && <span className="text-subtle">Pick your class and board first.</span>}
        </div>
      </fieldset>
      {showSat && (
        <div className="grid gap-4 sm:grid-cols-[1fr_180px]">
          <Field label="Have you taken the SAT or ACT?">
            <Select name="satStatus" value={sat} onChange={(e) => setSat(e.target.value)}>
              <option value="">Choose</option>
              <option value="taken">Yes</option>
              <option value="planned">Planned</option>
              <option value="no">No</option>
            </Select>
          </Field>
          {sat === 'taken' && (
            <Field label="Score">
              <TextInput name="satScore" defaultValue={draft.satScore} inputMode="numeric" placeholder="e.g. 1380" />
            </Field>
          )}
        </div>
      )}
      <Field label="Activities, projects, sports" hint="Anything you do outside class. It goes into your Inventory.">
        <textarea name="activities" defaultValue={draft.activities} rows={3} placeholder="e.g. School debate team, piano grade 4, district football"
          className="rounded-lg border border-line bg-surface p-3 text-sm outline-none placeholder:text-subtle focus:border-brand-500 focus:ring-2 focus:ring-brand-200" />
      </Field>
      <div className="mt-2 flex items-center justify-between gap-3">
        <Link href="/onboarding/needs" className="inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" /> Back</Link>
        <div className="flex items-center gap-2">
          <Button type="submit" name="skip" value="1" variant="ghost">Skip for now</Button>
          <Button type="submit">Save and continue</Button>
        </div>
      </div>
    </form>
  );
}
