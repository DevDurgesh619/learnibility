import type { Metadata } from 'next';
import Link from 'next/link';
import { Send, Sparkles } from 'lucide-react';
import { NoSection } from '@/components/teacher/no-section';
import { QuerySelect } from '@/components/teacher/query-select';
import { SectionTabs } from '@/components/teacher/section-tabs';
import { chaptersOf, interventionsFor, sectionClusters, sectionHref, teacherContext } from '@/components/teacher/data';
import { Avatar, Badge, Button, Card, CardBody, CardFooter, CardHeader, EmptyState, GapBadge, GAP_LABEL, PageHeader, Table, TBody, TD, TH, THead, TR } from '@/components/ui';
import { assignWork } from '@/lib/actions/teacher';
import { addDaysLocal, demoToday } from '@/lib/data';
import { GAP_TAXONOMY } from '@/lib/engines';
import { formatHours } from '@/lib/format';

export const metadata: Metadata = { title: 'Class gaps · Learnibility' };

export default async function ClassGapsPage({ searchParams }: { searchParams: Promise<{ section?: string; chapter?: string }> }) {
  const sp = await searchParams;
  const ctx = await teacherContext(sp.section);
  const section = ctx.section;
  if (!section) return <NoSection title="Class gaps" description="Gap clusters across the class, by subtopic and gap type." />;
  const chapters = chaptersOf(section.subjectId);
  const chapterId = chapters.some((c) => c.id === sp.chapter) ? sp.chapter : undefined;
  const clusters = sectionClusters(section, chapterId);
  const due = addDaysLocal(demoToday(), 3);
  // Big clusters get a card each; smaller ones go in a compact list so the page stays scannable.
  const big = clusters.filter((c, i) => c.learners.length >= 3 && i < 6);
  const small = clusters.filter((c) => !big.includes(c));

  return (
    <>
      <PageHeader eyebrow={section.name} title="Class gaps" description="Open gaps grouped by subtopic and gap type. One re-teach set reaches every student in a cluster, and lands in their tasks." />
      <div className="mb-6 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <SectionTabs sections={ctx.sections.map((s) => ({ id: s.id, name: s.name, count: s.learnerIds.length }))} activeId={section.id} hrefFor={(id) => sectionHref('/teacher/class-gaps', id)} />
        <QuerySelect param="chapter" value={chapterId ?? ''} label="Chapter" allLabel="All chapters" options={chapters.map((c) => ({ value: c.id, label: `${c.order}. ${c.name}` }))} />
      </div>

      {clusters.length === 0 ? (
        <EmptyState icon={<Sparkles />} title="No shared gaps" description={`No gap is shared by two or more students in ${section.name}${chapterId ? ' in this chapter' : ''}. Individual gaps are in the Gap log.`} action={<Link href={sectionHref('/teacher/gap-log', section.id)}><Button variant="secondary">Open the gap log</Button></Link>} />
      ) : (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          {big.map((c) => {
            const info = GAP_TAXONOMY[c.code];
            const plan = interventionsFor(c.code);
            return (
              <Card key={`${c.subtopicId}|${c.code}`} className="flex flex-col">
                <CardHeader
                  title={`${c.learners.length} students at ${c.code} in ${c.subtopicName}`}
                  description={`${c.chapterName} · ${GAP_LABEL[c.code]} gap · about ${formatHours(c.meanHours)} each to close`}
                  action={<GapBadge code={c.code} />}
                />
                <CardBody className="flex-1 space-y-4">
                  <p className="text-sm text-muted"><span className="font-medium text-ink">What it looks like: </span>{info.signature}</p>
                  <div className="flex flex-wrap gap-2">
                    {c.learners.map((l) => (
                      <Link key={l.id} href={sectionHref('/teacher/students', section.id, { id: l.id })} className="inline-flex items-center gap-1.5 rounded-full border border-line bg-surface py-0.5 pl-0.5 pr-2.5 text-xs hover:border-brand-300">
                        <Avatar name={l.name} size="sm" className="size-6 text-[10px]" />
                        {l.name}
                        <span className="text-subtle">L{l.level}</span>
                      </Link>
                    ))}
                  </div>
                  {plan.length > 0 && (
                    <div>
                      <p className="mb-2 text-xs font-medium uppercase tracking-wide text-subtle">Free plan, in order</p>
                      <ol className="space-y-2">
                        {plan.map((p) => (
                          <li key={p.id} className="flex gap-2 text-sm">
                            <Badge tone={p.rank === 1 ? 'brand' : 'neutral'}>{p.rank}</Badge>
                            <span><span className="font-medium text-ink">{p.name}</span> <span className="text-subtle">· {p.timeCost}</span></span>
                          </li>
                        ))}
                      </ol>
                    </div>
                  )}
                </CardBody>
                <CardFooter className="flex-wrap justify-between">
                  <form action={assignWork} className="flex flex-wrap items-center gap-2">
                    <input type="hidden" name="sectionId" value={section.id} />
                    <input type="hidden" name="kind" value="reteach" />
                    <input type="hidden" name="subtopicId" value={c.subtopicId} />
                    <input type="hidden" name="gapCode" value={c.code} />
                    {c.learners.map((l) => <input key={l.id} type="hidden" name="learnerIds" value={l.id} />)}
                    <label className="flex items-center gap-1.5 text-xs text-muted">
                      Due
                      <input type="date" name="dueDate" defaultValue={due} min={demoToday()} className="h-8 rounded-md border border-line bg-surface px-2 text-xs text-ink" />
                    </label>
                    <Button type="submit" size="sm"><Send /> Push re-teach set</Button>
                  </form>
                  <Link href={sectionHref('/teacher/assign', section.id, { kind: 'reteach', subtopic: c.subtopicId, code: c.code, learners: c.learners.map((l) => l.id).join(',') })} className="text-sm font-medium text-brand-600 hover:underline">Adjust first</Link>
                </CardFooter>
              </Card>
            );
          })}
          {small.length > 0 && (
            <Card className="min-w-0 lg:col-span-2">
              <CardHeader title="Smaller clusters" description="Shared by fewer students. Open one in Assign to adjust the group before sending." />
              <Table className="mt-3">
                <THead><TR><TH>Subtopic</TH><TH>Gap</TH><TH>Students</TH><TH className="hidden md:table-cell">Hours each</TH><TH /></TR></THead>
                <TBody>
                  {small.map((c) => (
                    <TR key={`${c.subtopicId}|${c.code}`}>
                      <TD className="min-w-48"><p className="text-sm text-ink">{c.subtopicName}</p><p className="text-xs text-subtle">{c.chapterName}</p></TD>
                      <TD><GapBadge code={c.code} /></TD>
                      <TD className="text-sm">{c.learners.map((l) => l.name.split(' ')[0]).join(', ')}</TD>
                      <TD className="hidden whitespace-nowrap md:table-cell">{formatHours(c.meanHours)}</TD>
                      <TD className="text-right"><Link href={sectionHref('/teacher/assign', section.id, { kind: 'reteach', subtopic: c.subtopicId, code: c.code, learners: c.learners.map((l) => l.id).join(',') })} className="whitespace-nowrap text-sm font-medium text-brand-600 hover:underline">Re-teach</Link></TD>
                    </TR>
                  ))}
                </TBody>
              </Table>
            </Card>
          )}
        </div>
      )}
    </>
  );
}
