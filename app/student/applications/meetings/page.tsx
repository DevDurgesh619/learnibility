import { applicationsBundle } from '@/components/applications/data';
import { requireSubscriber } from '@/components/applications/guard';
import { MeetingList } from '@/components/applications/meetings';
import { SupportHeader } from '@/components/applications/support-header';

export const metadata = { title: 'Meetings · Application Support · Learnibility' };

export default async function Page() {
  const { persona, counsellorName } = await requireSubscriber();
  const b = applicationsBundle(persona.id);
  return (
    <>
      <SupportHeader active="meetings" counsellorName={counsellorName} />
      <MeetingList meetings={b.meetings} viewer="student" />
    </>
  );
}
