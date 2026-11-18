import Link from 'next/link';
import { redirect } from 'next/navigation';
import { applicationsBundle, fitInputs, isPaid, listUniversities, studentCtx } from '@/components/applications/data';
import { fieldLabel } from '@/components/applications/fields';
import { fitAll, readiness, type FitBand } from '@/components/applications/fit';
import { FitHeader } from '@/components/applications/fit-header';
import { FitResults, type FitCard } from '@/components/applications/fit-results';
import { Upsell } from '@/components/applications/upsell';
import { currentPersona } from '@/lib/session';
import { cn } from '@/lib/utils';

export const metadata = { title: 'Your chances · University Fit · Learnibility' };

const STREAM_FIELDS: Record<string, string[]> = {
  commerce: ['business', 'accounting', 'commerce', 'economics', 'finance', 'management'],
  science: ['computer-science', 'mechanical-engineering', 'electrical-engineering', 'medicine', 'data-science'],
  humanities: ['law', 'politics', 'psychology', 'economics', 'liberal-arts', 'international-relations'],
};

export default async function Page({ searchParams }: { searchParams: Promise<{ field?: string; country?: string; again?: string }> }) {
  const persona = (await currentPersona())!;
  const ctx = studentCtx(persona.id);
  if (isPaid(ctx.plan)) redirect('/student/applications');
  const sp = await searchParams;
  const { profile, countries, sources } = fitInputs(persona.id);
  const r = readiness(profile, sources);
  if (r.pct === 0) redirect('/student/universities/best-fit');

  const unis = listUniversities();
  const bundle = applicationsBundle(persona.id);
  const savedFields = bundle.shortlist.map((s) => unis.find((u) => u.id === s.universityId)?.programmes.find((p) => p.id === s.programmeId)?.field).filter((x): x is string => !!x);
  const defaultFields = savedFields.length ? [...new Set(savedFields)] : STREAM_FIELDS[ctx.student?.stream ?? ''] ?? ['computer-science', 'economics', 'business'];
  const fields = sp.field ? [sp.field] : defaultFields;
  const country = sp.country ? [sp.country] : countries;
  const res = fitAll(unis, profile, { fields, countries: country });
  const card = (x: (typeof res)['reach'][number]): FitCard => ({ universityId: x.universityId, shortName: x.university.shortName, programme: x.programme.name, country: x.university.country, band: x.band, chancePct: x.chancePct, reason: x.reason });
  const groups = { reach: res.reach.map(card), target: res.target.map(card), safe: res.safe.map(card) } as Record<FitBand, FitCard[]>;
  const fieldChoices = [...new Set([...defaultFields, 'computer-science', 'economics', 'business', 'law', 'medicine'])];

  return (
    <>
      <FitHeader active="best-fit" title="Your chances" description="Reach, Target and Safe for your course, with the reason behind each." />
      <div className="mb-4 flex flex-wrap gap-2 text-xs">
        <span className="py-1 text-muted">Course:</span>
        {fieldChoices.map((f) => (
          <Link key={f} href={`?field=${f}${sp.country ? `&country=${sp.country}` : ''}&again=1`} className={cn('rounded-full border px-2.5 py-1', fields.length === 1 && fields[0] === f ? 'border-brand-600 bg-brand-50 text-brand-700' : 'border-line bg-surface text-muted hover:text-ink')}>{fieldLabel(f)}</Link>
        ))}
        {fields.length > 1 && <span className="rounded-full border border-brand-600 bg-brand-50 px-2.5 py-1 text-brand-700">{fields.map(fieldLabel).join(', ')}</span>}
      </div>
      <FitResults groups={groups} readinessPct={r.pct} instant={!!sp.again} footer={<Upsell variant="funnel" />} />
      <p className="mt-4 text-xs text-subtle">How this works: your results are compared with each programme&apos;s typical offer and test range, then scaled by its published admit rate. Universities admitting under 10% are always a reach. Sources and dates are on each university page.</p>
    </>
  );
}
