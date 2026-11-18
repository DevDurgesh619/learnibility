import { notFound } from 'next/navigation';
import { Share2 } from 'lucide-react';
import { LinkTabs } from '@/components/tutor/tabs';
import { profileStrength, readPrefs } from '@/components/tutor/prefs';
import { Progress } from '@/components/ui/progress';
import { getTutor } from '@/components/marketplace/queries';
import { currentPersona } from '@/lib/session';

/** Tutor HTML 8a-8e: profile strength on top, the doc §15 list as sub-nav. */
export default async function ProfileLayout({ children }: { children: React.ReactNode }) {
  const persona = (await currentPersona())!;
  const t = getTutor(persona.id);
  if (!t) notFound();
  const pct = profileStrength(t.profileStrengthPct, await readPrefs(persona.id));
  return (
    <div className="mx-auto max-w-4xl">
      <div className="mb-4 flex flex-wrap items-end justify-between gap-4">
        <h1 className="text-2xl font-semibold text-ink">Profile</h1>
        <div className="flex items-center gap-4">
          <div className="w-44"><p className="mb-1 text-sm text-muted">Profile strength <span className="font-medium text-ink">{pct}%</span></p><Progress value={pct} tone={pct >= 90 ? 'success' : 'brand'} /></div>
          <a href="/tutor/onboarding" className="text-sm font-medium text-muted hover:text-ink">Guided setup</a>
          <a href={`/student/tutors/${t.id}`} className="inline-flex items-center gap-1 text-sm font-medium text-brand-700 hover:underline"><Share2 className="size-4" />Share link</a>
        </div>
      </div>
      <LinkTabs className="mb-6" tabs={[
        { href: '/tutor/profile', label: 'Public profile' }, { href: '/tutor/profile/preferences', label: 'Teaching preferences' },
        { href: '/tutor/profile/availability', label: 'Availability' }, { href: '/tutor/profile/pricing', label: 'Pricing' }, { href: '/tutor/profile/verification', label: 'Verification' },
      ]} />
      {children}
    </div>
  );
}
