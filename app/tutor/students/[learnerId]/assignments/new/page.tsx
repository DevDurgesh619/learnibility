import { BackLink } from '@/components/tutor/bits';
import { AddTestWizard } from '@/components/tutor/add-test-wizard';
import { openGapsFor, studentContext } from '@/components/tutor/model';
import { Card, CardBody } from '@/components/ui/card';
import { addDaysLocal, demoToday, getMastery, getSubject } from '@/lib/data';
import { assignTest, draftTest } from '@/lib/actions/tutor';
import { currentPersona } from '@/lib/session';

/** 4i-4k: add a test for this student. */
export default async function NewTest({ params, searchParams }: { params: Promise<{ learnerId: string }>; searchParams: Promise<{ subtopic?: string }> }) {
  const { learnerId } = await params;
  const sp = await searchParams;
  const { row } = studentContext((await currentPersona())!.id, learnerId)!;
  const topics = row.subjectIds.flatMap((sid) => {
    const b = getSubject(sid);
    return (b?.subtopics ?? []).map((s) => ({ id: s.id, label: s.name.split(/[;:]/)[0]!, chapter: b!.chapters.find((c) => c.id === s.chapterId)?.name ?? '' }));
  });
  const gaps = openGapsFor(learnerId, row.subjectIds).sort((a, b) => a.level - b.level);
  const label = (id: string) => topics.find((t) => t.id === id)?.label ?? id;
  const ids = sp.subtopic ? [sp.subtopic] : gaps.slice(0, 2).map((g) => g.subtopicId);
  const text = ids.map((id) => { const g = gaps.find((x) => x.subtopicId === id); return `${label(id).toLowerCase()}${g ? ` (${g.code}, level L${g.level})` : ''}`; }).join(', ');
  const retention = getMastery(learnerId).filter((m) => row.subjectIds.includes(m.subjectId) && m.level >= 4 && !ids.includes(m.subtopicId)).slice(0, 2).map((m) => m.subtopicId);
  return (
    <>
      <BackLink href={`/tutor/students/${learnerId}/assignments`}>Assignments</BackLink>
      <Card><CardBody>
        <AddTestWizard learnerId={learnerId} firstName={row.name.split(' ')[0]!} topics={topics} suggested={{ ids, text: text ? `suggested ${text}` : '' }} retention={retention}
          defaultDue={addDaysLocal(demoToday(), 2)} draft={draftTest} assign={assignTest} />
      </CardBody></Card>
    </>
  );
}
