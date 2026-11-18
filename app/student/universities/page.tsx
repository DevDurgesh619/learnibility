import Link from 'next/link';
import { redirect } from 'next/navigation';
import { Bookmark } from 'lucide-react';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { applicationsBundle, fitInputs, isPaid, listUniversities, studentCtx } from '@/components/applications/data';
import { UniversityExplorer } from '@/components/applications/explorer';
import { FitHeader } from '@/components/applications/fit-header';
import { uniRow } from '@/components/applications/rows';
import { FitBadge, UniMark } from '@/components/applications/ui';
import { Upsell } from '@/components/applications/upsell';
import { currentPersona } from '@/lib/session';

export const metadata = { title: 'University Fit · Learnibility' };

export default async function Page({ searchParams }: { searchParams: Promise<{ q?: string }> }) {
  const persona = (await currentPersona())!;
  const ctx = studentCtx(persona.id);
  if (isPaid(ctx.plan)) redirect('/student/applications');
  const { q } = await searchParams;

  const unis = listUniversities();
  const bundle = applicationsBundle(persona.id);
  const saved = new Set(bundle.shortlist.map((s) => s.universityId));
  const rows = unis.map((u) => uniRow(u, saved));
  const fields = [...new Set(unis.flatMap((u) => u.programmes.map((p) => p.field)))].sort();
  const { countries } = fitInputs(persona.id);
  const target = countries.length ? countries : ['us', 'uk', 'ca'];
  const top = rows.filter((r) => target.includes(r.country) && r.qsRank).sort((a, b) => (a.qsRank ?? 999) - (b.qsRank ?? 999)).slice(0, 3);
  const savedUnis = bundle.shortlist.map((s) => ({ s, u: unis.find((u) => u.id === s.universityId) })).filter((x) => x.u);

  return (
    <>
      <FitHeader active="explore" />
      <UniversityExplorer
        rows={rows}
        fields={fields}
        initialQuery={q}
        detailBase="/student/universities"
        top={
          <div className="mt-6 space-y-6">
            <section>
              <h2 className="mb-3 text-base font-semibold text-ink">Top universities for your target</h2>
              <div className="grid gap-3 sm:grid-cols-3">
                {top.map((r) => (
                  <Link key={r.id} href={`/student/universities/${r.id}`} className="block">
                    <Card className="h-full p-4 transition-colors hover:border-brand-300">
                      <p className="font-semibold text-ink">{r.shortName}</p>
                      <p className="mt-1 text-xs text-muted">{r.countryName} · {r.satLabel} · {r.deadlineLabel}</p>
                      <p className="mt-2 text-xs text-subtle">QS #{r.qsRank} · {r.acceptancePct}% admitted</p>
                    </Card>
                  </Link>
                ))}
              </div>
            </section>
            <Card>
              <CardHeader title="Saved universities" description="Save from any university page. Your fit result groups them." />
              <CardBody className="pt-3">
                {savedUnis.length === 0 ? (
                  <p className="flex items-center gap-2 text-sm text-muted"><Bookmark className="size-4" />Nothing saved yet. Open a university and press Save.</p>
                ) : (
                  <ul className="divide-y divide-line">
                    {savedUnis.map(({ s, u }) => (
                      <li key={s.universityId} className="flex items-center gap-3 py-2.5">
                        <UniMark uni={u!} size="sm" />
                        <Link href={`/student/universities/${u!.id}`} className="min-w-0 flex-1 truncate text-sm font-medium text-ink hover:underline">{u!.name}</Link>
                        {s.fitGroup && <FitBadge band={s.fitGroup} />}
                      </li>
                    ))}
                  </ul>
                )}
              </CardBody>
            </Card>
          </div>
        }
        banner={<Upsell />}
      />
    </>
  );
}
