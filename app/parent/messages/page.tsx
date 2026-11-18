import { sendParentMessage } from '@/lib/actions/parent';
import { ChildSwitcher } from '@/components/parent/child-switcher';
import { param, parentContext, type SearchParams } from '@/components/parent/context';
import { MessageView, threadsFor } from '@/components/parent/message-view';
import { NoChild } from '@/components/parent/no-child';
import { PageHeader } from '@/components/ui';
import { getMessages } from '@/lib/data';

export default async function ParentMessages({ searchParams }: { searchParams: SearchParams }) {
  const sp = await searchParams;
  const { parent, children, child } = await parentContext(searchParams);
  if (!child) return (<><PageHeader eyebrow="Parent" title="Messages" /><NoChild /></>);
  const s = child.student;
  const messages = getMessages(parent.id, { learnerId: s.id }).filter((m) => m.from === parent.id || m.toIds.includes(parent.id));
  const threads = threadsFor(parent.id, messages);
  return (
    <>
      <PageHeader eyebrow="Parent" title="Messages" description={`Notes from ${s.firstName}'s counsellor, teachers and tutors.`} />
      <ChildSwitcher children={children} selectedId={s.id} basePath="/parent/messages" />
      <MessageView
        viewerId={parent.id} threads={threads} messages={messages} openThreadId={param(sp, 'thread')}
        hrefFor={(t) => `/parent/messages?${new URLSearchParams({ child: s.id, thread: t.threadId })}`}
        action={sendParentMessage} hidden={() => ({ learnerId: s.id })}
        emptyText={`When ${s.firstName}'s counsellor, teacher or tutor writes to you, it shows up here.`}
      />
    </>
  );
}
