import { notFound } from 'next/navigation';
import { ApplicationDetail } from '@/components/applications/app-detail';
import { applicationDocuments, firstName, getApplication, getUniversity } from '@/components/applications/data';
import { requireSubscriber } from '@/components/applications/guard';
import { SupportHeader } from '@/components/applications/support-header';

export const metadata = { title: 'Application · Learnibility' };

export default async function Page({ params }: { params: Promise<{ applicationId: string }> }) {
  const { applicationId } = await params;
  const { persona, ctx, counsellorName } = await requireSubscriber();
  const app = getApplication(applicationId);
  if (!app || app.learnerId !== persona.id) notFound();
  const uni = getUniversity(app.universityId);
  if (!uni) notFound();
  const docs = applicationDocuments(persona.id).filter((d) => !d.refId || d.refId === app.id || d.refId === app.universityId);
  return (
    <>
      <SupportHeader active="board" counsellorName={counsellorName} />
      <ApplicationDetail app={app} uni={uni} viewer="student" counsellorFirst={firstName(ctx.counsellorId)} documents={docs} essayHref={(id) => `/student/applications/essays/${id}`} backHref="/student/applications/board" />
    </>
  );
}
