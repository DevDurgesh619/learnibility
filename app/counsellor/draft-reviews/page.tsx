import { PageHeader } from '@/components/ui/page-header';
import { caseloadApplications, caseloadLearners, nameOf, uniMap } from '@/components/applications/data';
import { EssayList } from '@/components/applications/essay-list';
import { currentPersona } from '@/lib/session';

export const metadata = { title: 'Draft reviews · Learnibility' };

export default async function Page() {
  const me = (await currentPersona())!;
  const apps = caseloadApplications(me.id);
  const names = Object.fromEntries(caseloadLearners(me.id).map((id) => [id, nameOf(id)]));
  const waiting = apps.map((a) => ({ ...a, essays: a.essays.filter((e) => e.status === 'in_review') })).filter((a) => a.essays.length);
  const rest = apps.map((a) => ({ ...a, essays: a.essays.filter((e) => e.status !== 'in_review') })).filter((a) => a.essays.length);
  const unis = uniMap();
  return (
    <>
      <PageHeader eyebrow="Counsellor" title="Draft reviews" description="Essays waiting for your comments, oldest deadline first." />
      <h2 className="mb-2 text-sm font-semibold tracking-wide text-muted uppercase">Waiting for you · {waiting.reduce((n, a) => n + a.essays.length, 0)}</h2>
      <EssayList apps={waiting} unis={unis} hrefFor={(id) => `/counsellor/draft-reviews/${id}`} studentNames={names} />
      {rest.length > 0 && (
        <>
          <h2 className="mt-8 mb-2 text-sm font-semibold tracking-wide text-muted uppercase">Drafting or final</h2>
          <EssayList apps={rest} unis={unis} hrefFor={(id) => `/counsellor/draft-reviews/${id}`} studentNames={names} />
        </>
      )}
    </>
  );
}
