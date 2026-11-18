import { notFound } from 'next/navigation';
import { ApplicationDetail } from '@/components/applications/app-detail';
import { applicationDocuments, applicationsBundle, firstName, getApplication, getUniversity, nameOf } from '@/components/applications/data';
import { MeetingComposer } from '@/components/applications/meeting-composer';
import { MeetingList } from '@/components/applications/meetings';
import { DEMO_NOW_ISO } from '@/lib/demo-clock';
import { currentPersona } from '@/lib/session';

export const metadata = { title: 'Application · Counsellor · Learnibility' };

export default async function Page({ params }: { params: Promise<{ applicationId: string }> }) {
  const { applicationId } = await params;
  const me = (await currentPersona())!;
  const app = getApplication(applicationId);
  if (!app || app.counsellorId !== me.id) notFound();
  const uni = getUniversity(app.universityId);
  if (!uni) notFound();
  const docs = applicationDocuments(app.learnerId).filter((d) => !d.refId || d.refId === app.id);
  const meetings = applicationsBundle(app.learnerId).meetings;
  return (
    <>
      <ApplicationDetail app={app} uni={uni} viewer="counsellor" studentName={nameOf(app.learnerId)} counsellorFirst="you" documents={docs} essayHref={(id) => `/counsellor/draft-reviews/${id}`} backHref="/counsellor/applications" />
      <section className="mt-8 grid gap-6 lg:grid-cols-[minmax(0,1fr)_420px]">
        <div>
          <h2 className="mb-3 text-base font-semibold text-ink">Meetings with {firstName(app.learnerId)}</h2>
          <MeetingList meetings={meetings} viewer="counsellor" />
        </div>
        <MeetingComposer learnerId={app.learnerId} studentFirst={firstName(app.learnerId)} today={DEMO_NOW_ISO.slice(0, 10)} />
      </section>
    </>
  );
}
