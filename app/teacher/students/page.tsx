import type { Metadata } from 'next';
import Link from 'next/link';
import { ArrowLeft, Lock, Users } from 'lucide-react';
import { BarChart } from '@/components/charts';
import { NoSection } from '@/components/teacher/no-section';
import { SectionTabs } from '@/components/teacher/section-tabs';
import { chaptersOf, meanMastery, sectionGaps, sectionHref, studentDetail, subtopicName, teacherContext } from '@/components/teacher/data';
import { LEVEL_CELL } from '@/components/teacher/mastery-heatmap';
import {
  Avatar, Badge, BandBadge, Card, CardBody, CardHeader, EmptyState, GapBadge, LEVEL_LABEL, PageHeader, StatTile, Table, TBody, TD, TH, THead, TR,
} from '@/components/ui';
import { getAlr, getProfile, getSectionHeatmap, listParameters } from '@/lib/data';
import { formatHours, formatPercent } from '@/lib/format';
import { cn } from '@/lib/utils';

export const metadata: Metadata = { title: 'Students · Learnibility' };

const fmtDate = (iso: string) => (iso ? new Date(iso).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'Asia/Kolkata' }) : '–');

function show(v: unknown): string {
  if (v === null || v === undefined || v === '') return '–';
  if (typeof v === 'number') return Number.isInteger(v) ? String(v) : v.toFixed(2);
  if (typeof v === 'boolean') return v ? 'Yes' : 'No';
  if (Array.isArray(v)) return v.map(show).join(', ');
  if (typeof v === 'object') return Object.entries(v as Record<string, unknown>).slice(0, 4).map(([k, x]) => `${k}: ${show(x)}`).join(' · ');
  return String(v);
}

export default async function StudentsPage({ searchParams }: { searchParams: Promise<{ section?: string; id?: string }> }) {
  const sp = await searchParams;
  const ctx = await teacherContext(sp.section);
  const section = ctx.section;
  if (!section) return <NoSection title="Students" description="One student in depth: mastery, gaps and history." />;
  const tabs = <SectionTabs sections={ctx.sections.map((s) => ({ id: s.id, name: s.name, count: s.learnerIds.length }))} activeId={section.id} hrefFor={(id) => sectionHref('/teacher/students', id)} />;

  if (sp.id && section.learnerIds.includes(sp.id)) return <StudentView sectionId={section.id} learnerId={sp.id} />;

  // ---- list
  const hm = getSectionHeatmap(section.id);
  const gaps = sectionGaps(section, { open: true });
  const rows = (hm?.rows ?? []).map((r) => {
    const tested = Object.values(r.cells).filter((c) => c);
    const last = tested.map((c) => c!.lastTestedUtc).sort().pop() ?? '';
    const g = gaps.filter((x) => x.learnerId === r.learnerId);
    return { id: r.learnerId, name: r.name, isPersona: r.isPersona, avg: meanMastery(r.cells), tested: tested.length, last, gaps: g.length, worst: g[0] };
  }).sort((a, b) => a.name.localeCompare(b.name));

  return (
    <>
      <PageHeader eyebrow={section.name} title="Students" description="Pick a student to see their mastery, gaps and test history. You see learning data only; family, wellbeing and health details stay with the counsellor." />
      <div className="mb-6">{tabs}</div>
      <Card>
        {rows.length ? (
          <Table>
            <THead><TR><TH>Student</TH><TH>Mastery</TH><TH className="hidden sm:table-cell">Subtopics tested</TH><TH>Open gaps</TH><TH className="hidden md:table-cell">Last tested</TH></TR></THead>
            <TBody>
              {rows.map((r) => (
                <TR key={r.id}>
                  <TD>
                    <Link href={sectionHref('/teacher/students', section.id, { id: r.id })} className="flex items-center gap-2 font-medium text-ink hover:text-brand-700">
                      <Avatar name={r.name} size="sm" />{r.name}
                    </Link>
                  </TD>
                  <TD className="tabular-nums">{r.avg === undefined ? '–' : formatPercent(r.avg)}</TD>
                  <TD className="hidden tabular-nums sm:table-cell">{r.tested}</TD>
                  <TD><div className="flex flex-wrap items-center gap-2"><span className="tabular-nums">{r.gaps}</span>{r.worst && <GapBadge code={r.worst.code} />}</div></TD>
                  <TD className="hidden md:table-cell">{fmtDate(r.last)}</TD>
                </TR>
              ))}
            </TBody>
          </Table>
        ) : (
          <CardBody><EmptyState icon={<Users />} title="No students in this section" description="Students appear here once they join the class." /></CardBody>
        )}
      </Card>
    </>
  );
}

async function StudentView({ sectionId, learnerId }: { sectionId: string; learnerId: string }) {
  const ctx = await teacherContext(sectionId);
  const section = ctx.section!;
  const d = studentDetail(section, learnerId);
  const chapters = chaptersOf(section.subjectId);
  const byChapter = chapters
    .map((c) => {
      const ms = d.mastery.filter((m) => subtopicName(section.subjectId, m.subtopicId).chapterId === c.id);
      return { x: `Ch ${c.order}`, name: c.name, mastery: ms.length ? ms.reduce((a, m) => a + m.pMastery, 0) / ms.length : null };
    })
    .filter((c) => c.mastery !== null) as { x: string; name: string; mastery: number }[];
  const openGaps = d.gaps.filter((g) => g.status !== 'closed');
  const avg = d.mastery.length ? d.mastery.reduce((a, m) => a + m.pMastery, 0) / d.mastery.length : undefined;
  const alr = d.isPersona ? getAlr(learnerId) : undefined;
  const alrSubject = alr?.chapters.filter((c) => c.subjectId === section.subjectId) ?? [];
  const lrs = alrSubject.length ? alrSubject.reduce((a, c) => a + c.LRS, 0) / alrSubject.length : undefined;
  const latestBand = alrSubject.sort((a, b) => b.asOfUtc.localeCompare(a.asOfUtc))[0]?.band;

  // Teacher sees T1 only (lib/visibility). Group the visible values by profile section.
  const params = new Map(listParameters().map((p) => [p.id, p]));
  const visible = d.isPersona ? getProfile(learnerId, 'teacher').filter((v) => v.mode === 'full') : [];
  const groups = new Map<string, { name: string; value: string; asOf?: string }[]>();
  for (const v of visible) {
    const p = params.get(v.paramId);
    if (!p) continue;
    groups.set(p.section, [...(groups.get(p.section) ?? []), { name: p.name, value: show(v.value), asOf: v.asOfUtc }]);
  }

  return (
    <>
      <Link href={sectionHref('/teacher/students', section.id)} className="mb-4 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ArrowLeft className="size-4" /> {section.name} students</Link>
      <div className="mb-6 flex items-center gap-4">
        <Avatar name={d.name} size="lg" />
        <div className="min-w-0">
          <h1 className="text-2xl font-semibold tracking-tight text-ink">{d.name}</h1>
          <p className="text-sm text-muted">{d.student ? `${d.student.programme} · ${d.student.school}` : `${section.name} · ${section.school}`}</p>
        </div>
      </div>

      <div className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatTile label="Average mastery" value={avg === undefined ? '–' : formatPercent(avg)} hint={`${d.mastery.length} subtopics tested`} />
        <StatTile label="Open gaps" value={openGaps.length} hint={openGaps.length ? `${formatHours(openGaps.reduce((a, g) => a + g.hoursToClose, 0))} to close` : 'None open'} />
        <StatTile label="Learning rate (LRS)" value={lrs === undefined ? '–' : lrs.toFixed(2)} hint={latestBand ? <BandBadge band={latestBand} /> : 'Not enough tests yet'} />
        <StatTile label="Tests in this subject" value={d.isPersona ? d.attempts.length : d.testScores.length} />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader title="Mastery by chapter" description="Mean of tested subtopics" />
          <CardBody>
            {byChapter.length ? <BarChart data={byChapter.map(({ x, mastery }) => ({ x, mastery }))} series={[{ key: 'mastery', label: 'Mastery' }]} format="percent" /> : <EmptyState title="Not tested yet" description="Assign a chapter check to see where this student stands." />}
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Gaps" description="Diagnosed by the gap engine; validate them in the Gap log." action={<Link href={sectionHref('/teacher/gap-log', section.id, { student: learnerId })} className="text-sm font-medium text-brand-600 hover:underline">Gap log</Link>} />
          <CardBody className="space-y-2">
            {openGaps.length ? openGaps.map((g) => (
              <div key={g.id} className="flex items-start justify-between gap-3 rounded-lg border border-line p-3">
                <div className="min-w-0">
                  <p className="text-sm font-medium text-ink">{g.subtopicName}</p>
                  <p className="text-xs text-subtle">{g.chapterName} · {LEVEL_LABEL[g.level]} · {formatHours(g.hoursToClose)} to close</p>
                </div>
                <div className="flex shrink-0 flex-col items-end gap-1">
                  <GapBadge code={g.code} />
                  {g.validation && <Badge tone={g.validation.verdict === 'rejected' ? 'neutral' : 'success'}>Teacher {g.validation.verdict}</Badge>}
                </div>
              </div>
            )) : <p className="text-sm text-muted">No open gaps in this subject.</p>}
          </CardBody>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader title="Subtopic levels" />
          <CardBody>
            {d.mastery.length ? (
              <div className="grid gap-2 sm:grid-cols-2 xl:grid-cols-3">
                {d.mastery.map((m) => {
                  const n = subtopicName(section.subjectId, m.subtopicId);
                  return (
                    <div key={m.subtopicId} className="flex items-center gap-3 rounded-lg border border-line p-2">
                      <span className={cn('flex size-9 shrink-0 items-center justify-center rounded text-xs font-semibold', LEVEL_CELL[m.level])}>L{m.level}</span>
                      <div className="min-w-0">
                        <p className="truncate text-sm text-ink" title={n.name}>{n.name}</p>
                        <p className="text-xs text-subtle">{formatPercent(m.pMastery)} · tested {fmtDate(m.lastTestedUtc)}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : <p className="text-sm text-muted">No subtopic tested yet.</p>}
          </CardBody>
        </Card>

        <Card className="min-w-0">
          <CardHeader title="Test history" />
          {(d.isPersona ? d.attempts.length : d.testScores.length) ? (
            <Table className="mt-3">
              <THead><TR><TH>Test</TH><TH>Date</TH><TH>Score</TH></TR></THead>
              <TBody>
                {d.isPersona
                  ? d.attempts.slice(0, 12).map((a) => (
                    <TR key={a.id}><TD>{a.title}</TD><TD className="whitespace-nowrap">{fmtDate(a.submittedUtc)}</TD><TD className="tabular-nums">{a.maxScore ? formatPercent(a.score / a.maxScore) : '–'}</TD></TR>
                  ))
                  : d.testScores.map((t) => (
                    <TR key={`${t.title}${t.date}`}><TD>{t.title}</TD><TD className="whitespace-nowrap">{fmtDate(`${t.date}T06:00:00Z`)}</TD><TD className="tabular-nums">{Math.round(t.pct)}%</TD></TR>
                  ))}
              </TBody>
            </Table>
          ) : <CardBody><p className="text-sm text-muted">No tests yet.</p></CardBody>}
        </Card>

        <Card>
          <CardHeader title="Learning profile" description="Standard (T1) details only." action={<span className="inline-flex items-center gap-1 text-xs text-subtle"><Lock className="size-3.5" /> Teacher view</span>} />
          <CardBody>
            {groups.size ? (
              <div className="space-y-2">
                {[...groups.entries()].map(([sec, items]) => (
                  <details key={sec} className="rounded-lg border border-line px-3 py-2">
                    <summary className="cursor-pointer text-sm font-medium text-ink">{sec} <span className="text-subtle">({items.length})</span></summary>
                    <dl className="mt-2 space-y-1.5">
                      {items.map((i) => (
                        <div key={i.name} className="grid grid-cols-[minmax(0,1fr)_minmax(0,1fr)] gap-3 text-sm">
                          <dt className="text-muted">{i.name}</dt><dd className="text-ink">{i.value}</dd>
                        </div>
                      ))}
                    </dl>
                  </details>
                ))}
              </div>
            ) : <p className="text-sm text-muted">{d.isPersona ? 'No standard profile details recorded yet.' : 'This student has not set up a Learnibility profile.'}</p>}
          </CardBody>
        </Card>
      </div>
    </>
  );
}
