import { sendMentorMessage } from '@/lib/actions/mentor';
import { mentorContext } from '@/components/mentor/context';
import { MessageView, threadsFor } from '@/components/parent/message-view';
import { PageHeader } from '@/components/ui';
import { getMessages } from '@/lib/data';

export default async function MentorMessages({ searchParams }: { searchParams: Promise<Record<string, string | string[] | undefined>> }) {
  const sp = await searchParams;
  const { mentor, mentees } = await mentorContext(searchParams);
  const mine = new Set(mentees.map((m) => m.student.id));
  const messages = getMessages(mentor.id).filter((m) => mine.has(m.learnerId) && (m.from === mentor.id || m.toIds.includes(mentor.id)));
  const threads = threadsFor(mentor.id, messages).map((t) => {
    // For a mentor, the other party is the mentee (learner ids are skipped by default for parents).
    const people = new Set(messages.filter((m) => m.threadId === t.threadId).flatMap((m) => [m.from, ...m.toIds]));
    people.delete(mentor.id);
    const other = [...people].find((p) => p.startsWith('lrn_')) ?? t.otherId;
    const name = mentees.find((m) => m.student.id === other)?.student.name ?? t.otherName;
    return { ...t, otherId: other, otherName: name, otherRole: other.startsWith('lrn_') ? 'mentee' : t.otherRole };
  });
  return (
    <>
      <PageHeader eyebrow="Mentor" title="Messages" description="Conversations with your mentees." />
      <MessageView
        viewerId={mentor.id} threads={threads} messages={messages} openThreadId={typeof sp.thread === 'string' ? sp.thread : undefined}
        hrefFor={(t) => `/mentor/messages?thread=${encodeURIComponent(t.threadId)}`}
        action={sendMentorMessage} hidden={(t) => ({ learnerId: t.learnerId })}
        emptyText="Messages from your mentees show up here."
      />
    </>
  );
}
