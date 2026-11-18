import type { Metadata } from 'next';
import { BadgeCheck, ShieldCheck } from 'lucide-react';
import { getTutor } from '@/components/marketplace/queries';
import { formatDate } from '@/components/marketplace/dates';
import { Pill } from '@/components/tutor/bits';
import { Button } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Verification · Tutor' };

/** Tutor HTML 8e: each document's status and what it unlocks. Document names are sample data. */
export default async function VerificationPage() {
  const persona = (await currentPersona())!;
  const t = getTutor(persona.id)!;
  const v = t.verification;
  const items = [
    { name: 'Identity', doc: 'Aadhaar', ok: v.identity, unlocks: 'Required to publish' },
    { name: 'Qualification', doc: t.qualifications[0] ?? 'Degree certificate', ok: v.qualification, unlocks: 'Verified badge' },
    { name: 'Experience proof', doc: 'Optional', ok: v.experience, unlocks: `Unlocks "${t.yearsExperience}+ yrs experience" badge` },
    { name: 'Background check', doc: 'Required for offline sessions with minors', ok: false, unlocks: 'In-person sessions' },
  ];
  return (
    <div className="space-y-4">
      <Card><CardBody className="flex items-start gap-3">
        {t.verified ? <BadgeCheck className="size-6 shrink-0 text-brand-600" /> : <ShieldCheck className="size-6 shrink-0 text-muted" />}
        <div><p className="font-semibold text-ink">{t.verified ? 'Verified tutor' : 'Verification in progress'}</p><p className="text-sm text-muted">{t.verified ? `Badge shown on your public profile since ${formatDate(t.joinedOn)}` : 'Upload identity and one qualification to get the badge.'}</p></div>
      </CardBody></Card>
      <Card><ul className="divide-y divide-line">
        {items.map((i) => (
          <li key={i.name} className="flex flex-col gap-2 px-5 py-4 sm:flex-row sm:items-center">
            <div className="min-w-0 flex-1"><p className="text-sm font-medium text-ink">{i.name}</p><p className="text-xs text-muted">{i.doc}{i.ok ? ` · uploaded ${formatDate(t.joinedOn)}` : ''} · {i.unlocks}</p></div>
            {i.ok ? <Pill tone="success">Approved</Pill> : <Button type="button" variant="secondary" size="sm">{i.name === 'Background check' ? 'Start' : 'Upload'}</Button>}
          </li>
        ))}
      </ul></Card>
      <p className="text-xs text-subtle">Documents are stored encrypted and never shown to students.</p>
    </div>
  );
}
