import type { Metadata } from 'next';
import Link from 'next/link';
import { redirect } from 'next/navigation';
import { ClipboardCheck, Sparkles } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { buttonVariants } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import { PageHeader } from '@/components/ui/page-header';
import { Table, TBody, TD, TH, THead, TR } from '@/components/ui/table';
import { getAttempts, getEvents, getStudent, getTasks, demoToday } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import { cn } from '@/lib/utils';
import { initialTests, resultHref, subjectTests, testHref } from '@/components/assessment/catalog';
import { TestCard } from '@/components/assessment/test-card';

export const metadata: Metadata = { title: 'Assessments · Learnibility' };

const KIND_LABEL: Record<string, string> = {
  onboarding: 'Starting test', chapter_check: 'Chapter check', weekly: 'Weekly test', mock: 'Mock', retention_probe: 'Review check', practice_form: 'Practice test', assigned: 'Assigned',
};

/** PDF 8a: the single hub for every test. Completed tests show "See gap analysis"; the paid set unlocks as a group. */
export default async function AssessmentsPage({ searchParams }: { searchParams: Promise<{ subject?: string }> }) {
  const persona = await currentPersona();
  if (!persona) redirect('/login');
  const student = getStudent(persona.id);
  if (!student) redirect('/login');
  const { subject } = await searchParams;
  const attempts = getAttempts(student.id);
  const initial = await initialTests(student.id);
  const subjects = await subjectTests(student);
  const active = subjects.find((s) => s.subjectId === subject) ?? subjects[0];
  const paid = student.plan === 'full_package';
  const today = demoToday();
  const due = getTasks(student.id, undefined, { status: 'todo' }).filter((t) => t.kind === 'test' && t.dueDate >= today).slice(0, 4);
  const lastFor = (ids: string[], kind?: string) => attempts.find((a) => (!kind || a.kind === kind) && ids.every((id) => a.questionIds.includes(id)) && a.questionIds.length === ids.length);
  const onbEvents = getEvents(student.id, { type: 'onboarding_completed' });
  const sectionDone = (section: string) =>
    onbEvents.some((e) => (section === 'reasoning' ? !!e.payload.reasoning : section === 'about' ? !!(e.payload.riasec as { code?: string } | null)?.code : false));
  const onbAttempt = (section: string, subjectId: string) =>
    attempts.find((a) => a.kind === 'onboarding' && a.id.endsWith(`_onb_${section}`)) ?? attempts.find((a) => a.kind === 'onboarding' && a.subjectId === subjectId);
  const anyOnboarding = attempts.some((a) => a.kind === 'onboarding');

  return (
    <>
      <PageHeader title="Assessments" description="Short checks that find exactly where you are stuck, then plan the fix into your week." />

      {due.length > 0 && (
        <Card className="mb-6 border-brand-200 bg-brand-50/50 p-4">
          <p className="text-sm font-semibold text-ink">Due soon</p>
          <ul className="mt-2 flex flex-col gap-2">
            {due.map((t) => (
              <li key={t.id} className="flex flex-wrap items-center gap-2 text-sm">
                <ClipboardCheck className="size-4 text-brand-600" />
                <span className="font-medium text-ink">{t.title}</span>
                <span className="text-muted">due {new Date(t.dueDate).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}</span>
                <Link href={t.questionIds?.length ? testHref(`task.${t.id}`) : t.href ?? '/student/assessments'} className="ml-auto text-sm font-medium text-brand-700 hover:underline">Start</Link>
              </li>
            ))}
          </ul>
        </Card>
      )}

      <section className="mb-8">
        <div className="mb-3 flex flex-wrap items-center gap-2 border-b border-dashed border-line pb-2">
          <h2 className="text-base font-semibold text-ink">Initial tests</h2>
          <Badge tone="success">Free</Badge>
          <span className="text-sm text-muted">Quick checks for your recommendations and a first gap analysis</span>
        </div>
        {initial.length ? (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
            {initial.map((t, i) => (
              <TestCard key={t.id} test={t} last={onbAttempt(t.section!, t.subjectId)} done={sectionDone(t.section!)} highlight={!anyOnboarding && i === 0} />
            ))}
          </div>
        ) : (
          <EmptyState title="No starting test for your class yet" description="Your chapter checks below work the same way." />
        )}
      </section>

      <section className="mb-8">
        <div className="mb-3 flex flex-wrap items-center gap-2 border-b border-dashed border-line pb-2">
          <h2 className="text-base font-semibold text-ink">Chapter checks and practice</h2>
          <Badge tone="success">Free</Badge>
        </div>
        {subjects.length === 0 ? (
          <EmptyState title="Finish onboarding to see your subjects" description="Your chapter checks appear here once we know your board and class." action={<Link href="/onboarding/about" className={buttonVariants({ size: 'sm' })}>Finish onboarding</Link>} />
        ) : (
          <>
            <div className="mb-4 flex gap-2 overflow-x-auto pb-1" role="tablist">
              {subjects.map((s) => (
                <Link key={s.subjectId} href={`/student/assessments?subject=${s.subjectId}`} role="tab" aria-selected={s.subjectId === active.subjectId}
                  className={cn('whitespace-nowrap rounded-full border px-3 py-1.5 text-sm', s.subjectId === active.subjectId ? 'border-ink bg-ink text-white' : 'border-line bg-surface text-muted hover:text-ink')}>
                  {s.subjectName}
                </Link>
              ))}
            </div>
            {active.chapters.every((c) => !c.check) ? (
              <EmptyState title={`${active.subjectName} questions are being written`} description="Chapter checks for this subject appear here as soon as its question bank is ready." />
            ) : (
              <Card className="overflow-hidden">
                <Table>
                  <THead>
                    <TR>
                      <TH>Chapter</TH>
                      <TH className="hidden md:table-cell">Last result</TH>
                      <TH className="text-right">Tests</TH>
                    </TR>
                  </THead>
                  <TBody>
                    {active.chapters.map((c) => {
                      const pct = c.lastAttempt?.maxScore ? Math.round((100 * c.lastAttempt.score) / c.lastAttempt.maxScore) : null;
                      return (
                        <TR key={c.chapterId}>
                          <TD>
                            <p className="font-medium text-ink">{c.order}. {c.name}</p>
                            <p className="text-xs text-muted">
                              {c.check ? `${c.check.questions} Q · ${c.check.minutes} min` : 'Questions coming soon'}
                              {c.current && <Badge tone="brand" className="ml-2">In class now</Badge>}
                            </p>
                          </TD>
                          <TD className="hidden md:table-cell">
                            {c.lastAttempt ? (
                              <Link href={resultHref(c.lastAttempt.id)} className="text-sm text-brand-700 hover:underline">
                                {KIND_LABEL[c.lastAttempt.kind] ?? 'Test'} · {pct}%
                              </Link>
                            ) : (
                              <span className="text-sm text-subtle">Not taken</span>
                            )}
                          </TD>
                          <TD className="text-right">
                            <div className="flex flex-wrap justify-end gap-2">
                              {c.check && (
                                <Link href={testHref(c.check.id)} className={buttonVariants({ size: 'sm', variant: c.current && !c.lastAttempt ? 'primary' : 'secondary' })}>
                                  {c.lastAttempt ? 'Check again' : 'Chapter check'}
                                </Link>
                              )}
                              {c.practice.map((p) => (
                                <Link key={p.id} href={testHref(p.id)} className={cn(buttonVariants({ size: 'sm', variant: 'ghost' }), 'hidden sm:inline-flex')}>
                                  {p.id.startsWith('pfa') ? 'Practice A' : 'Practice B'}
                                </Link>
                              ))}
                            </div>
                          </TD>
                        </TR>
                      );
                    })}
                  </TBody>
                </Table>
              </Card>
            )}
          </>
        )}
      </section>

      <section className="mb-8">
        <div className="mb-3 flex flex-wrap items-center gap-2 border-b border-dashed border-line pb-2">
          <h2 className="text-base font-semibold text-ink">In-depth assessments</h2>
          <Badge tone={paid ? 'success' : 'neutral'}>{paid ? 'Unlocked' : 'Paid'}</Badge>
          <span className="text-sm text-muted">Full-syllabus mocks with topic-by-topic gap analysis</span>
        </div>
        {subjects.every((s) => s.mocks.length === 0) ? (
          <EmptyState title="No mocks for your class yet" description="Mock papers appear here as each subject's bank is finished." />
        ) : (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {subjects.flatMap((s) => s.mocks.slice(0, 2)).slice(0, 8).map((m) => (
              <TestCard key={m.id} test={m} locked={!paid} last={paid ? lastFor(m.questionIds, 'mock') : undefined} />
            ))}
          </div>
        )}
        {!paid && (
          <div className="mt-4 flex flex-wrap items-center gap-3">
            <span className={cn(buttonVariants({ variant: 'secondary', size: 'sm' }), 'border-brand-300 text-brand-700')}>
              <Sparkles /> Unlock in-depth assessments
            </span>
            <span className="text-xs text-muted">Part of the Full package.</span>
          </div>
        )}
      </section>

      <section>
        <h2 className="mb-3 text-base font-semibold text-ink">History</h2>
        {attempts.length === 0 ? (
          <EmptyState icon={<ClipboardCheck />} title="No tests yet" description="Start with the initial tests above. Each one takes under 10 minutes and gives you a first gap analysis." />
        ) : (
          <Card className="overflow-hidden">
            <Table>
              <THead>
                <TR><TH>Test</TH><TH className="hidden sm:table-cell">Type</TH><TH className="hidden sm:table-cell">Date</TH><TH className="text-right">Score</TH></TR>
              </THead>
              <TBody>
                {attempts.slice(0, 12).map((a) => (
                  <TR key={a.id}>
                    <TD><Link href={resultHref(a.id)} className="font-medium text-ink hover:text-brand-700">{a.title}</Link></TD>
                    <TD className="hidden sm:table-cell text-muted">{KIND_LABEL[a.kind] ?? a.kind}</TD>
                    <TD className="hidden sm:table-cell text-muted">{new Date(a.submittedUtc).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'Asia/Kolkata' })}</TD>
                    <TD className="text-right tabular-nums">{a.score}/{a.maxScore}</TD>
                  </TR>
                ))}
              </TBody>
            </Table>
          </Card>
        )}
      </section>
    </>
  );
}
