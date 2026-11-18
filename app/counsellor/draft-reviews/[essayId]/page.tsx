import Link from 'next/link';
import { notFound } from 'next/navigation';
import { ChevronLeft } from 'lucide-react';
import { caseloadApplications, findEssay, firstName, getUniversity, nameOf } from '@/components/applications/data';
import { EssayEditor } from '@/components/applications/essay-editor';
import { shortPrompt } from '@/components/applications/logic';
import { currentPersona } from '@/lib/session';

export const metadata = { title: 'Review essay · Learnibility' };

export default async function Page({ params }: { params: Promise<{ essayId: string }> }) {
  const { essayId } = await params;
  const me = (await currentPersona())!;
  const hit = findEssay(essayId, caseloadApplications(me.id));
  if (!hit) notFound();
  const ids = new Set([me.id, hit.app.learnerId, ...hit.essay.comments.map((c) => c.authorId).filter((x): x is string => !!x)]);
  const names = Object.fromEntries([...ids].map((id) => [id, nameOf(id)]));
  const uni = getUniversity(hit.app.universityId);
  return (
    <>
      <Link href="/counsellor/draft-reviews" className="mb-3 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" />Draft reviews</Link>
      <p className="mb-4 text-sm text-muted">{nameOf(hit.app.learnerId)} · <Link href={`/counsellor/applications/${hit.app.id}`} className="underline">{uni?.shortName} application</Link></p>
      <EssayEditor essay={hit.essay} title={`${shortPrompt(hit.essay.prompt)} · ${uni?.shortName}`} viewer="counsellor" names={names} counsellorFirst={firstName(me.id)} studentFirst={firstName(hit.app.learnerId)} />
    </>
  );
}
