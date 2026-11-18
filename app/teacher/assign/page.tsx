import type { Metadata } from 'next';
import { CheckCircle2, ClipboardList } from 'lucide-react';
import { AssignForm } from '@/components/teacher/assign-form';
import { NoSection } from '@/components/teacher/no-section';
import { SectionTabs } from '@/components/teacher/section-tabs';
import { chaptersOf, sectionAssignments, sectionClusters, sectionHref, teacherContext } from '@/components/teacher/data';
import { Badge, Card, CardBody, CardHeader, EmptyState, PageHeader, Progress, Table, TBody, TD, TH, THead, TR } from '@/components/ui';
import { assignWork } from '@/lib/actions/teacher';
import { addDaysLocal, demoToday, getStudent, getSubject } from '@/lib/data';

export const metadata: Metadata = { title: 'Assign · Learnibility' };

const fmtDate = (d: string) => new Date(`${d}T00:00:00Z`).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'UTC' });

export default async function AssignPage({ searchParams }: {
  searchParams: Promise<{ section?: string; chapter?: string; kind?: string; subtopic?: string; code?: string; learners?: string; done?: string }>;
}) {
  const sp = await searchParams;
  const ctx = await teacherContext(sp.section);
  const section = ctx.section;
  if (!section) return <NoSection title="Assign" description="Assign a chapter check or a re-teach set." />;

  const subject = getSubject(section.subjectId);
  const chapters = chaptersOf(section.subjectId).map((c) => ({
    id: c.id,
    label: `${c.order}. ${c.name}`,
    subtopics: (subject?.subtopics ?? []).filter((s) => s.chapterId === c.id).sort((a, b) => a.order - b.order).map((s) => ({ id: s.id, label: `${c.order}.${s.order} ${s.name}` })),
  }));
  const names = new Map(section.background.map((b) => [b.id, b.name]));
  const clusters = sectionClusters(section);
  for (const c of clusters) for (const l of c.learners) names.set(l.id, l.name);
  const students = section.learnerIds.map((id) => ({ id, name: names.get(id) ?? getStudent(id)?.name ?? id })).sort((a, b) => a.name.localeCompare(b.name));
  const groups = clusters.map((c) => ({ key: `${c.subtopicId}|${c.code}`, label: `${c.learners.length} at ${c.code} · ${c.subtopicName}`, learnerIds: c.learners.map((l) => l.id), subtopicId: c.subtopicId, code: c.code }));
  const assignments = sectionAssignments(section, ctx.teacherId);
  const done = sp.done ? assignments.find((a) => a.groupId === sp.done) : undefined;
  const today = demoToday();
  const learners = sp.learners?.split(',').filter((id) => section.learnerIds.includes(id));

  return (
    <>
      <PageHeader eyebrow={section.name} title="Assign" description="Send a chapter check or a re-teach set to the whole section or a group. It lands in each student's tasks." />
      <div className="mb-6">
        <SectionTabs sections={ctx.sections.map((s) => ({ id: s.id, name: s.name, count: s.learnerIds.length }))} activeId={section.id} hrefFor={(id) => sectionHref('/teacher/assign', id)} />
      </div>

      {done && (
        <div role="status" className="mb-6 flex items-start gap-3 rounded-xl border border-success-600/30 bg-success-50 p-4 text-sm text-success-700">
          <CheckCircle2 className="mt-0.5 size-5 shrink-0" />
          <div>
            <p className="font-semibold">Assigned to {done.learners.length} student{done.learners.length === 1 ? '' : 's'}</p>
            <p>{done.title}, due {fmtDate(done.dueDate)}. It is in their tasks now and their week has been re-planned around it.</p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,1fr)_420px]">
        <Card>
          <CardHeader title="New assignment" description={subject?.subject.programme ?? subject?.subject.name} />
          <CardBody>
            {chapters.length ? (
              <AssignForm
                key={`${section.id}|${sp.done ?? ''}`}
                action={assignWork}
                sectionId={section.id}
                chapters={chapters}
                students={students}
                groups={groups}
                today={today}
                defaults={{
                  kind: sp.kind === 'reteach' ? 'reteach' : 'chapter_check',
                  chapterId: chapters.some((c) => c.id === sp.chapter) ? sp.chapter : undefined,
                  subtopicId: sp.subtopic,
                  code: sp.code,
                  learnerIds: learners,
                  dueDate: addDaysLocal(today, 3),
                }}
              />
            ) : (
              <EmptyState title="Curriculum not loaded" description="This subject's chapters are not available yet." />
            )}
          </CardBody>
        </Card>

        <Card className="min-w-0">
          <CardHeader title="Assigned so far" description="Completion across the students who got it." />
          {assignments.length ? (
            <Table className="mt-3">
              <THead><TR><TH>Assignment</TH><TH>Due</TH><TH className="w-32">Done</TH></TR></THead>
              <TBody>
                {assignments.map((a) => {
                  const n = a.learners.filter((l) => l.status === 'done').length;
                  const overdue = a.dueDate < today && n < a.learners.length;
                  return (
                    <TR key={a.groupId}>
                      <TD>
                        <p className="font-medium text-ink">{a.title}</p>
                        <p className="text-xs text-subtle">{a.learners.length === section.learnerIds.length ? 'Whole section' : `${a.learners.length} students`}{a.refId?.includes('-st') ? ' · re-teach' : ' · chapter check'}</p>
                      </TD>
                      <TD className="whitespace-nowrap">{overdue ? <Badge tone="danger">{fmtDate(a.dueDate)}</Badge> : fmtDate(a.dueDate)}</TD>
                      <TD><div className="flex items-center gap-2"><Progress value={n / a.learners.length} tone="success" /><span className="text-xs text-muted tabular-nums">{n}/{a.learners.length}</span></div></TD>
                    </TR>
                  );
                })}
              </TBody>
            </Table>
          ) : (
            <CardBody><EmptyState icon={<ClipboardList />} title="Nothing assigned yet" description="Your chapter checks and re-teach sets show here with how many students finished them." /></CardBody>
          )}
        </Card>
      </div>
    </>
  );
}
