import Link from 'next/link';
import { redirect } from 'next/navigation';
import { ChevronLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { fitInputs } from '@/components/applications/data';
import { saveFitProfile } from '@/lib/actions/applications';
import { getDocuments } from '@/lib/data';
import { currentPersona } from '@/lib/session';

export const metadata = { title: 'Complete your profile · University Fit · Learnibility' };

const field = 'mt-1 w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm text-ink placeholder:text-subtle';

export default async function Page() {
  const persona = (await currentPersona())!;
  const { profile, countries } = fitInputs(persona.id);
  const activityDocs = getDocuments(persona.id, 'activities').length;
  const academic = profile.aLevelGrades ?? (profile.ibPoints !== undefined ? `IB ${profile.ibPoints}` : profile.boardPercent !== undefined ? `${profile.boardPercent}%` : '');

  async function save(form: FormData) {
    'use server';
    await saveFitProfile(form);
    redirect('/student/universities/best-fit');
  }

  return (
    <>
      <Link href="/student/universities/best-fit" className="mb-3 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" />Best fit</Link>
      <h1 className="mb-1 text-2xl font-semibold tracking-tight text-ink">Complete your profile</h1>
      <p className="mb-6 text-sm text-muted">Pre-filled from onboarding and your Inventory. Add only what&apos;s missing.</p>
      <Card>
        <CardBody>
          <form action={save} className="grid gap-5 sm:grid-cols-2">
            <label className="text-sm font-medium text-ink">Academic results
              <input name="academic" defaultValue={academic} placeholder="e.g. 92%, AAB predicted, or IB 38" className={field} />
              <span className="mt-1 block text-xs font-normal text-subtle">Latest board percentage or predicted grades.</span>
            </label>
            <label className="text-sm font-medium text-ink">Activities
              <select name="activities" defaultValue={profile.activities ?? ''} className={field}>
                <option value="">Choose how deep your activities go</option>
                <option value="weak">A few, mostly participation</option>
                <option value="average">Regular, with some responsibility</option>
                <option value="strong">Leadership, awards or real impact</option>
              </select>
              <span className="mt-1 block text-xs font-normal text-subtle">{activityDocs ? `${activityDocs} from Inventory · ` : ''}<Link href="/student/inventory" className="underline">add more</Link></span>
            </label>
            <label className="text-sm font-medium text-ink">SAT score
              <input name="sat" inputMode="numeric" defaultValue={profile.sat ?? ''} placeholder='e.g. 1480, or leave blank if planned' className={field} />
            </label>
            <label className="text-sm font-medium text-ink">IELTS overall
              <input name="ielts" inputMode="decimal" defaultValue={profile.ielts ?? ''} placeholder="e.g. 7.0" className={field} />
            </label>
            <label className="text-sm font-medium text-ink sm:col-span-2">Essay
              <textarea name="essay" rows={5} placeholder="Paste a draft. We only use it to rate essay quality." className={field} />
            </label>
            <fieldset className="text-sm font-medium text-ink sm:col-span-2">
              <legend>Preferred countries (optional)</legend>
              <div className="mt-2 flex flex-wrap gap-3">
                {[['us', 'USA'], ['uk', 'UK'], ['ca', 'Canada'], ['au', 'Australia'], ['in', 'India']].map(([v, l]) => (
                  <label key={v} className="inline-flex items-center gap-2 rounded-full border border-line px-3 py-1.5 font-normal">
                    <input type="checkbox" name="countries" value={l} defaultChecked={countries.includes(v!)} />{l}
                  </label>
                ))}
              </div>
            </fieldset>
            <div className="sm:col-span-2 flex justify-end"><Button type="submit">Save</Button></div>
          </form>
        </CardBody>
      </Card>
    </>
  );
}
