import Link from 'next/link';
import { CheckCircle2, Compass, NotebookPen } from 'lucide-react';
import { ActionItemsField } from '@/components/counsellor/action-items-field';
import { CareerColumn } from '@/components/counsellor/career-compare';
import { formatDate } from '@/components/counsellor/format';
import { StudentPicker } from '@/components/counsellor/student-picker';
import { loadCareerSession } from '@/components/counsellor/load';
import { Badge, Button, Card, CardBody, CardHeader, EmptyState, PageHeader } from '@/components/ui';
import { saveCareerSession } from '@/lib/actions/counsellor';

export const dynamic = 'force-dynamic';

export default async function CareerSessionsPage({ searchParams }: { searchParams: Promise<{ student?: string; a?: string; b?: string; saved?: string }> }) {
  const sp = await searchParams;
  const data = await loadCareerSession(sp.student, sp.a, sp.b);
  if (!data) return <EmptyState title="No students in your caseload" description="Students appear here once they are assigned to you." />;
  const { student, students, fits, compare, notes, defaultDue, saved, careers } = data;
  const first = student.name.split(' ')[0];
  const href = (a?: string, b?: string) => `/counsellor/career-sessions?student=${student.id}${a ? `&a=${a}` : ''}${b ? `&b=${b}` : ''}`;

  return (
    <>
      <PageHeader eyebrow="Counsellor" title="Career sessions" description="Explore fits together, compare two careers, and save notes whose action items land in the student's tasks."
        actions={<StudentPicker students={students} value={student.id} />} />

      {saved && (
        <div className="mb-6 rounded-[var(--radius-card)] border border-success-600/20 bg-success-50 p-4 text-sm">
          <p className="flex items-center gap-2 font-medium text-success-700"><CheckCircle2 className="size-4" />Session saved. {saved.actionItems.length} action item{saved.actionItems.length === 1 ? '' : 's'} added to {first}&apos;s tasks.</p>
          <ul className="mt-2 list-disc pl-6 text-ink">{saved.actionItems.map((a) => <li key={a.id}>{a.title} <span className="text-muted">· due {formatDate(a.dueOn)}</span></li>)}</ul>
        </div>
      )}

      <div className="grid gap-6 xl:grid-cols-[320px_1fr]">
        <div className="space-y-6">
          <Card>
            <CardHeader title={`Top fits for ${first}`} description="mapCareers, T3 data left out" />
            <CardBody className="p-0">
              {fits.length === 0 ? <p className="p-5 text-sm text-muted">Not enough profile evidence yet. Add interests (p200) in Student 360.</p> : (
                <ul className="divide-y divide-line">
                  {fits.slice(0, 8).map((f) => {
                    const inCompare = compare.some((c) => c.career.id === f.careerId);
                    return (
                      <li key={f.careerId} className="flex items-center gap-3 px-5 py-3">
                        <div className="min-w-0 flex-1">
                          <div className="truncate text-sm font-medium text-ink">{f.title}</div>
                          <div className="text-xs text-muted">{f.confidence} confidence</div>
                        </div>
                        <span className="text-sm font-semibold text-ink">{f.score}</span>
                        {inCompare ? <Badge tone="brand">Comparing</Badge> : (
                          <Link href={href(compare[0]?.career.id, f.careerId)} className="text-xs font-medium text-brand-700 hover:underline">Compare</Link>
                        )}
                      </li>
                    );
                  })}
                </ul>
              )}
            </CardBody>
          </Card>
          <Card>
            <CardHeader title="Past sessions" description={`Career notes with ${first}`} />
            <CardBody className="space-y-4">
              {notes.length === 0 ? <p className="text-sm text-muted">No career sessions yet. This will be the first.</p> : notes.map((n) => (
                <div key={n.id} className="border-l-2 border-brand-200 pl-3">
                  <p className="text-xs text-subtle">{formatDate(n.date)}</p>
                  <p className="text-sm text-ink">{n.summary}</p>
                  {n.actionItems.length > 0 && <ul className="mt-1 space-y-0.5 text-xs text-muted">{n.actionItems.map((a) => <li key={a.id}>{a.done ? '✓' : '○'} {a.title}</li>)}</ul>}
                </div>
              ))}
            </CardBody>
          </Card>
        </div>

        <div className="min-w-0 space-y-6">
          {compare.length === 0 ? (
            <EmptyState icon={<Compass />} title="Pick careers to compare" description="Choose from the top fits to see fit, skill gap, routes and pathways side by side." />
          ) : (
            <div className="grid gap-4 lg:grid-cols-2">
              {compare.map((c) => <CareerColumn key={c.career.id} career={c.career} fit={c.fit} gap={c.gap} />)}
            </div>
          )}

          <Card>
            <CardHeader title="Session notes" description={`Saved to ${first}'s record. Action items become tasks on ${first}'s timetable.`} action={<NotebookPen className="size-5 text-subtle" />} />
            <CardBody>
              <form action={saveCareerSession} className="space-y-4">
                <input type="hidden" name="learnerId" value={student.id} />
                {compare.map((c) => <input key={c.career.id} type="hidden" name="careerId" value={c.career.id} />)}
                <label className="block text-sm text-muted">Summary
                  <textarea name="summary" required rows={3} className="mt-1 w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm text-ink"
                    defaultValue={compare.length === 2 ? `Compared ${compare[0]!.career.title} and ${compare[1]!.career.title}. ` : ''} placeholder="What you talked about and how the student felt about it" />
                </label>
                <label className="block text-sm text-muted">Decisions <span className="text-subtle">(one per line)</span>
                  <textarea name="decisions" rows={2} className="mt-1 w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm text-ink" placeholder="e.g. Keep both options open until the class 11 finals" />
                </label>
                <div>
                  <p className="mb-2 text-sm text-muted">Action items</p>
                  <ActionItemsField defaultDue={defaultDue} initial={compare.flatMap((c) => c.suggested).slice(0, 3)} />
                </div>
                <div className="flex flex-wrap items-center gap-3">
                  <Button type="submit"><CheckCircle2 />Save session and add tasks</Button>
                  <span className="text-xs text-subtle">{careers} careers in the catalogue</span>
                </div>
              </form>
            </CardBody>
          </Card>
        </div>
      </div>
    </>
  );
}
