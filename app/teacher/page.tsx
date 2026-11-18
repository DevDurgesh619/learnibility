import type { Metadata } from 'next';
import Link from 'next/link';
import { AlertTriangle, ClipboardCheck, Layers, Users } from 'lucide-react';
import { LevelLegend, MasteryHeatmap, type HeatmapColumn } from '@/components/teacher/mastery-heatmap';
import { NoSection } from '@/components/teacher/no-section';
import { QuerySelect } from '@/components/teacher/query-select';
import { SectionTabs } from '@/components/teacher/section-tabs';
import { chaptersOf, heatmap, meanMastery, sectionClusters, sectionGaps, sectionHref, shortLabel, teacherContext } from '@/components/teacher/data';
import { Button, Card, CardBody, CardHeader, EmptyState, GapBadge, PageHeader, StatTile } from '@/components/ui';
import { formatPercent } from '@/lib/format';

export const metadata: Metadata = { title: 'Classes · Learnibility' };

export default async function ClassesPage({ searchParams }: { searchParams: Promise<{ section?: string; chapter?: string }> }) {
  const sp = await searchParams;
  const ctx = await teacherContext(sp.section);
  const section = ctx.section;
  if (!section) return <NoSection title="Classes" description="Your sections with a students × subtopics mastery heatmap." />;

  const chapters = chaptersOf(section.subjectId);
  const chapterId = chapters.some((c) => c.id === sp.chapter) ? sp.chapter : undefined;
  const hm = heatmap(section, chapterId);
  const columns: HeatmapColumn[] = (hm?.subtopics ?? []).map((s) => ({ id: s.id, short: shortLabel(s.id), name: s.name, chapterName: s.chapterName }));
  // Without a chapter filter, show only subtopics someone has been tested on, so the grid stays readable.
  const tested = new Set((hm?.rows ?? []).flatMap((r) => Object.entries(r.cells).filter(([, c]) => c).map(([id]) => id)));
  const shown = chapterId ? columns : columns.filter((c) => tested.has(c.id));
  const rows = (hm?.rows ?? []).map((r) => ({ id: r.learnerId, name: r.name, cells: r.cells as Record<string, NonNullable<(typeof r.cells)[string]> | undefined>, average: meanMastery(Object.fromEntries(shown.map((c) => [c.id, r.cells[c.id]]))) }))
    .sort((a, b) => (a.average ?? 2) - (b.average ?? 2));
  const classAvg = meanMastery(Object.fromEntries(rows.flatMap((r) => shown.map((c) => [`${r.id}|${c.id}`, r.cells[c.id]]))));
  const clusters = sectionClusters(section, chapterId);
  const toValidate = sectionGaps(section, { open: true }).filter((g) => !g.validation && (!chapterId || g.chapterId === chapterId)).length;
  const struggling = rows.filter((r) => r.average !== undefined && r.average < 0.5).length;

  return (
    <>
      <PageHeader
        eyebrow={`${section.school} · ${ctx.teacherName}`}
        title="Classes"
        description="Mastery level per student and subtopic, from every test they have taken. Lowest first."
        actions={<Link href={sectionHref('/teacher/assign', section.id, { chapter: chapterId })}><Button>Assign work</Button></Link>}
      />
      <div className="mb-4 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <SectionTabs sections={ctx.sections.map((s) => ({ id: s.id, name: s.name, count: s.learnerIds.length }))} activeId={section.id} hrefFor={(id) => sectionHref('/teacher', id)} />
        <QuerySelect param="chapter" value={chapterId ?? ''} label="Chapter" allLabel="All tested subtopics" options={chapters.map((c) => ({ value: c.id, label: `${c.order}. ${c.name}` }))} />
      </div>

      <div className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatTile label="Students" value={section.learnerIds.length} hint={section.name} icon={<Users />} />
        <StatTile label="Average mastery" value={classAvg === undefined ? '–' : formatPercent(classAvg)} hint={chapterId ? 'This chapter' : 'Tested subtopics'} icon={<Layers />} />
        <StatTile label="Gap clusters" value={clusters.length} hint="2 or more students, same subtopic and gap" icon={<AlertTriangle />} />
        <StatTile label="Diagnoses to validate" value={toValidate} hint={`${struggling} ${struggling === 1 ? "student" : "students"} under 50%`} icon={<ClipboardCheck />} />
      </div>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,1fr)_320px]">
        <Card className="min-w-0">
          <CardHeader title={`${section.name} mastery`} description={chapterId ? chapters.find((c) => c.id === chapterId)?.name : `${shown.length} tested subtopics. Hover a cell for the subtopic.`} />
          <CardBody>
            {rows.length && shown.length ? (
              <>
                <MasteryHeatmap rows={rows} columns={shown} studentHref={(id) => sectionHref('/teacher/students', section.id, { id })} />
                <LevelLegend className="mt-4" />
              </>
            ) : (
              <EmptyState title="Nothing tested yet" description={chapterId ? 'No one in this section has taken a test on this chapter. Assign a chapter check to see where they stand.' : 'Assign a chapter check to fill the heatmap.'} action={<Link href={sectionHref('/teacher/assign', section.id, { chapter: chapterId })}><Button variant="secondary">Assign a chapter check</Button></Link>} />
            )}
          </CardBody>
        </Card>

        <Card>
          <CardHeader title="Biggest clusters" description="Re-teach once, help many." action={<Link href={sectionHref('/teacher/class-gaps', section.id, { chapter: chapterId })} className="text-sm font-medium text-brand-600 hover:underline">All</Link>} />
          <CardBody className="space-y-3">
            {clusters.length ? clusters.slice(0, 4).map((c) => (
              <Link key={`${c.subtopicId}|${c.code}`} href={sectionHref('/teacher/class-gaps', section.id, { chapter: chapterId })} className="block rounded-lg border border-line p-3 hover:border-brand-300 hover:bg-brand-50/40">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-sm font-semibold text-ink">{c.learners.length} students</span>
                  <GapBadge code={c.code} />
                </div>
                <p className="mt-1 text-sm text-muted">{c.subtopicName}</p>
              </Link>
            )) : <p className="text-sm text-muted">No gap shared by two or more students{chapterId ? ' in this chapter' : ''}.</p>}
          </CardBody>
        </Card>
      </div>
    </>
  );
}
