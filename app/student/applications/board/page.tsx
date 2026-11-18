import { ApplicationsBoard } from '@/components/applications/board';
import { applicationsBundle, firstName, uniMap } from '@/components/applications/data';
import { requireSubscriber } from '@/components/applications/guard';
import { qaCheck } from '@/components/applications/logic';
import { SupportHeader } from '@/components/applications/support-header';
import { DEMO_NOW } from '@/lib/demo-clock';

export const metadata = { title: 'Applications · Learnibility' };

export default async function Page() {
  const { persona, ctx, counsellorName } = await requireSubscriber();
  const b = applicationsBundle(persona.id);
  const unis = uniMap();
  const pending = b.applications.filter((a) => a.status === 'collecting_documents' || a.status === 'in_review');
  const closest = pending.sort((x, y) => qaCheck(y, DEMO_NOW).filter((i) => i.ok).length - qaCheck(x, DEMO_NOW).filter((i) => i.ok).length)[0];
  return (
    <>
      <SupportHeader active="board" counsellorName={counsellorName} />
      <ApplicationsBoard apps={b.applications} unis={unis} hrefFor={(a) => `/student/applications/${a.id}`} closest={closest ? unis.get(closest.universityId)?.shortName : undefined} counsellorFirst={firstName(ctx.counsellorId)} />
    </>
  );
}
