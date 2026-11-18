import { notFound } from 'next/navigation';
import { applicationsBundle, findEssay, firstName, getUniversity, nameOf } from '@/components/applications/data';
import { EssayEditor } from '@/components/applications/essay-editor';
import { requireSubscriber } from '@/components/applications/guard';
import { shortPrompt } from '@/components/applications/logic';
import { SupportHeader } from '@/components/applications/support-header';

export const metadata = { title: 'Essay · Learnibility' };

export default async function Page({ params }: { params: Promise<{ essayId: string }> }) {
  const { essayId } = await params;
  const { persona, ctx, counsellorName } = await requireSubscriber();
  const b = applicationsBundle(persona.id);
  const hit = findEssay(essayId, b.applications);
  if (!hit) notFound();
  const authors = new Set(hit.essay.comments.map((c) => c.authorId).filter((x): x is string => !!x));
  const names = Object.fromEntries([...authors, persona.id].map((id) => [id, nameOf(id)]));
  const others = b.applications.flatMap((a) => a.essays.filter((e) => e.id !== essayId).map((e) => ({ id: e.id, label: `${shortPrompt(e.prompt)} (${getUniversity(a.universityId)?.shortName})`, href: `/student/applications/essays/${e.id}` })));
  return (
    <>
      <SupportHeader active="essays" counsellorName={counsellorName} />
      <EssayEditor
        essay={hit.essay}
        title={`${shortPrompt(hit.essay.prompt)} · ${getUniversity(hit.app.universityId)?.shortName}`}
        viewer="student"
        names={names}
        counsellorFirst={firstName(ctx.counsellorId)}
        studentFirst={firstName(persona.id)}
        others={others}
      />
    </>
  );
}
