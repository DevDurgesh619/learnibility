import { notFound } from 'next/navigation';
import { applicationsBundle, fitInputs, getUniversity, isPaid, studentCtx } from '@/components/applications/data';
import { SHOW_COSTS } from '@/components/applications/config';
import { UniversityDetail } from '@/components/applications/university-detail';
import { currentPersona } from '@/lib/session';

type Tab = 'overview' | 'courses' | 'admissions' | 'costs';
const TABS: Tab[] = ['overview', 'courses', 'admissions', ...(SHOW_COSTS ? (['costs'] as Tab[]) : [])];

export async function generateMetadata({ params }: { params: Promise<{ universityId: string }> }) {
  const { universityId } = await params;
  return { title: `${getUniversity(universityId)?.shortName ?? 'University'} · Learnibility` };
}

export default async function Page({ params, searchParams }: { params: Promise<{ universityId: string }>; searchParams: Promise<{ tab?: string }> }) {
  const { universityId } = await params;
  const { tab } = await searchParams;
  const uni = getUniversity(universityId);
  if (!uni) notFound();
  const persona = (await currentPersona())!;
  const ctx = studentCtx(persona.id);
  const paid = isPaid(ctx.plan);
  const bundle = applicationsBundle(persona.id);
  const { profile } = fitInputs(persona.id);
  return (
    <UniversityDetail
      uni={uni}
      tab={TABS.includes(tab as Tab) ? (tab as Tab) : 'overview'}
      base={`/student/universities/${uni.id}`}
      mode={paid ? 'paid' : 'free'}
      saved={bundle.shortlist.some((s) => s.universityId === uni.id)}
      onBoard={new Set(bundle.applications.map((a) => a.universityId))}
      fitProfile={profile}
      backHref={paid ? '/student/applications/universities' : '/student/universities'}
      backLabel={paid ? 'Universities' : 'Results'}
    />
  );
}
