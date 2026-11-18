import { applicationsBundle, firstName, uniMap } from '@/components/applications/data';
import { EssayList } from '@/components/applications/essay-list';
import { requireSubscriber } from '@/components/applications/guard';
import { SupportHeader } from '@/components/applications/support-header';

export const metadata = { title: 'Essays · Learnibility' };

export default async function Page() {
  const { persona, ctx, counsellorName } = await requireSubscriber();
  const b = applicationsBundle(persona.id);
  return (
    <>
      <SupportHeader active="essays" counsellorName={counsellorName} />
      <EssayList apps={b.applications} unis={uniMap()} hrefFor={(id) => `/student/applications/essays/${id}`} counsellorFirst={firstName(ctx.counsellorId)} />
    </>
  );
}
