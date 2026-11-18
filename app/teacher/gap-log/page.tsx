import type { Metadata } from 'next';
import Link from 'next/link';
import { CheckCircle2, ListChecks } from 'lucide-react';
import { NoSection } from '@/components/teacher/no-section';
import { QuerySelect } from '@/components/teacher/query-select';
import { SectionTabs } from '@/components/teacher/section-tabs';
import { ValidateGapForm } from '@/components/teacher/validate-gap-form';
import { interventionsFor, sectionGaps, sectionHref, teacherContext, type GapLogRow } from '@/components/teacher/data';
import { Badge, BAND_LABEL, Card, CardBody, EmptyState, GapBadge, PageHeader, Table, TBody, TD, TH, THead, TR } from '@/components/ui';
import { validateGap } from '@/lib/actions/teacher';
import { addDaysLocal, getAttempts, getMastery, getPersonName, getSection } from '@/lib/data';
import { formatHours } from '@/lib/format';
import type { GapRecord } from '@/lib/data';

export const metadata: Metadata = { title: 'Gap log · Learnibility' };

const fmtDate = (iso: string) => (iso ? new Date(iso).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'Asia/Kolkata' }) : '–');
const istDate = (iso: string) => new Date(Date.parse(iso) + 330 * 60_000).toISOString().slice(0, 10);

/** The workbook Gap Log's follow-up columns, from what has happened since the diagnosis. */
function followUp(g: GapLogRow, bgMastery?: { level: number; lastTestedUtc: string }) {
  const weeks = g.weeks ?? null;
  const retest = g.detectedUtc ? addDaysLocal(istDate(g.detectedUtc), Math.max(7, Math.ceil((weeks ?? 1) * 7))) : undefined;
  const m = g.isPersona ? getMastery(g.learnerId).find((x) => x.subtopicId === g.subtopicId) : bgMastery;
  const retested = m && g.detectedUtc && m.lastTestedUtc > g.detectedUtc ? m : undefined;
  const attempts = g.isPersona && g.detectedUtc ? getAttempts(g.learnerId, { chapterId: g.chapterId }).filter((a) => a.submittedUtc > g.detectedUtc).length : undefined;
  const ranks = [...interventionsFor(g.code).map((i) => `${g.code}-${i.rank}`), ...g.secondaryFlags.map((f) => `${f}-1`)];
  return {
    retest, ranks,
    retestLevel: retested?.level,
    gained: retested ? retested.level - g.level : undefined,
    attempts,
    recovered: g.status === 'closed' && g.validation?.verdict !== 'rejected' ? true : retested ? retested.level >= 4 : undefined,
  };
}

function Validation({ v }: { v: NonNullable<GapRecord['validation']> }) {
  const who = getPersonName(v.byId)?.name ?? v.byId;
  const text = v.verdict === 'confirmed' ? 'Confirmed' : v.verdict === 'corrected' ? `Corrected to ${v.correctedCode}` : 'Not a gap';
  return (
    <div className="text-xs">
      <Badge tone={v.verdict === 'rejected' ? 'neutral' : v.verdict === 'corrected' ? 'info' : 'success'}>{text}</Badge>
      <p className="mt-1 text-subtle">{who}, {fmtDate(v.utc)}</p>
      {v.note && <p className="mt-0.5 text-muted">“{v.note}”</p>}
    </div>
  );
}

export default async function GapLogPage({ searchParams }: { searchParams: Promise<{ section?: string; student?: string; show?: string; saved?: string }> }) {
  const sp = await searchParams;
  const ctx = await teacherContext(sp.section);
  const section = ctx.section;
  if (!section) return <NoSection title="Gap log" description="Diagnoses to validate, as in the workbook Gap Log." />;
  const full = getSection(section.id)!;
  const bg = new Map(full.background.map((b) => [b.id, b]));
  const all = sectionGaps(section);
  const show = sp.show === 'all' || sp.show === 'validated' ? sp.show : 'to_validate';
  const students = [...new Map(all.map((g) => [g.learnerId, g.studentName])).entries()].sort((a, b) => a[1].localeCompare(b[1]));
  const rows = all
    .filter((g) => !sp.student || g.learnerId === sp.student)
    .filter((g) => (show === 'all' ? true : show === 'validated' ? !!g.validation : !g.validation && g.status !== 'closed'));
  const toValidate = all.filter((g) => !g.validation && g.status !== 'closed').length;
  const saved = sp.saved ? all.find((g) => g.id === sp.saved) : undefined;

  return (
    <>
      <PageHeader eyebrow={section.name} title="Gap log" description="Every diagnosis, in the workbook's Gap Log columns. Confirm or correct it from what you see in class: your call is saved as the student's human-validation status (#430) and the plan follows it." />
      <div className="mb-4 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <SectionTabs sections={ctx.sections.map((s) => ({ id: s.id, name: s.name, count: s.learnerIds.length }))} activeId={section.id} hrefFor={(id) => sectionHref('/teacher/gap-log', id)} />
        <div className="flex flex-wrap gap-3">
          <QuerySelect param="show" value={show === 'to_validate' ? '' : show} label="Show" allLabel={`To validate (${toValidate})`} options={[{ value: 'validated', label: 'Validated' }, { value: 'all', label: 'All diagnoses' }]} />
          <QuerySelect param="student" value={sp.student ?? ''} label="Student" allLabel="Everyone" options={students.map(([id, name]) => ({ value: id, label: name }))} />
        </div>
      </div>

      {saved?.validation && (
        <div role="status" className="mb-4 flex items-center gap-2 rounded-xl border border-success-600/30 bg-success-50 p-3 text-sm text-success-700">
          <CheckCircle2 className="size-5 shrink-0" /> Saved for {saved.studentName}: {saved.subtopicName}, {saved.validation.verdict === 'corrected' ? `corrected to ${saved.validation.correctedCode}` : saved.validation.verdict === 'confirmed' ? `${saved.code} confirmed` : 'marked not a gap'}.
        </div>
      )}

      {rows.length === 0 ? (
        <EmptyState icon={<ListChecks />} title={show === 'to_validate' ? 'All diagnoses validated' : 'No diagnoses here'} description={show === 'to_validate' ? 'Nothing waits for you. New diagnoses appear after each test your students take.' : 'Try another filter.'} action={show === 'to_validate' ? <Link href={sectionHref('/teacher/gap-log', section.id, { show: 'all' })} className="text-sm font-medium text-brand-600 hover:underline">See all diagnoses</Link> : undefined} />
      ) : (
        <>
          {/* Desktop: the workbook table */}
          <Card className="hidden lg:block">
            <Table>
              <THead>
                <TR>
                  <TH>Date</TH><TH>Student</TH><TH>Chapter · Subtopic</TH><TH>Band</TH><TH>Level</TH><TH>Primary gap</TH><TH>Flags</TH>
                  <TH>Hours</TH><TH>Weeks</TH><TH>Interventions</TH><TH>Re-test</TH><TH>Re-test level</TH><TH title="Attempts since diagnosis">Attempts</TH><TH>Gained</TH>
                  <TH title="Recovered? (#290)">Recovered</TH><TH>Teacher validation (#430)</TH>
                </TR>
              </THead>
              <TBody>
                {rows.map((g) => {
                  const f = followUp(g, bg.get(g.learnerId)?.mastery[g.subtopicId]);
                  return (
                    <TR key={g.id} className="align-top">
                      <TD className="whitespace-nowrap text-xs">{fmtDate(g.detectedUtc)}</TD>
                      <TD className="whitespace-nowrap"><Link className="font-medium text-ink hover:text-brand-700" href={sectionHref('/teacher/students', section.id, { id: g.learnerId })}>{g.studentName}</Link></TD>
                      <TD className="min-w-48"><p className="text-xs text-subtle">{g.chapterName}</p><p className="text-sm">{g.subtopicName}</p></TD>
                      <TD className="whitespace-nowrap text-xs">{BAND_LABEL[g.band]}</TD>
                      <TD>L{g.level}</TD>
                      <TD><GapBadge code={g.code} /></TD>
                      <TD className="text-xs">{g.secondaryFlags.length ? g.secondaryFlags.join(', ') : '–'}</TD>
                      <TD className="whitespace-nowrap tabular-nums">{formatHours(g.hoursToClose)}</TD>
                      <TD className="tabular-nums">{g.weeks ?? '–'}</TD>
                      <TD className="text-xs">{f.ranks.join(', ')}</TD>
                      <TD className="whitespace-nowrap text-xs">{f.retest ? fmtDate(`${f.retest}T06:00:00Z`) : '–'}</TD>
                      <TD>{f.retestLevel === undefined ? '–' : `L${f.retestLevel}`}</TD>
                      <TD className="tabular-nums">{f.attempts ?? '–'}</TD>
                      <TD className="tabular-nums">{f.gained === undefined ? '–' : f.gained > 0 ? `+${f.gained}` : f.gained}</TD>
                      <TD>{f.recovered === undefined ? '–' : f.recovered ? <Badge tone="success">Yes</Badge> : <Badge tone="warning">Not yet</Badge>}</TD>
                      <TD className="min-w-64">
                        {g.validation ? <Validation v={g.validation} /> : (
                          <ValidateGapForm compact action={validateGap} sectionId={section.id} learnerId={g.learnerId} gapId={g.id} code={g.code} gapJson={g.isPersona ? undefined : JSON.stringify(stripRow(g))} />
                        )}
                      </TD>
                    </TR>
                  );
                })}
              </TBody>
            </Table>
          </Card>

          {/* Phone and tablet: one card per diagnosis */}
          <div className="space-y-3 lg:hidden">
            {rows.map((g) => {
              const f = followUp(g, bg.get(g.learnerId)?.mastery[g.subtopicId]);
              return (
                <Card key={g.id}>
                  <CardBody className="space-y-3">
                    <div className="flex items-start justify-between gap-3">
                      <div className="min-w-0">
                        <Link className="font-semibold text-ink" href={sectionHref('/teacher/students', section.id, { id: g.learnerId })}>{g.studentName}</Link>
                        <p className="text-sm text-muted">{g.subtopicName}</p>
                        <p className="text-xs text-subtle">{g.chapterName} · {fmtDate(g.detectedUtc)}</p>
                      </div>
                      <GapBadge code={g.code} />
                    </div>
                    <dl className="grid grid-cols-3 gap-2 text-xs">
                      <div><dt className="text-subtle">Level</dt><dd className="font-medium">L{g.level}</dd></div>
                      <div><dt className="text-subtle">Hours</dt><dd className="font-medium">{formatHours(g.hoursToClose)}</dd></div>
                      <div><dt className="text-subtle">Re-test</dt><dd className="font-medium">{f.retest ? fmtDate(`${f.retest}T06:00:00Z`) : '–'}</dd></div>
                      <div><dt className="text-subtle">Band</dt><dd className="font-medium">{BAND_LABEL[g.band]}</dd></div>
                      <div><dt className="text-subtle">Flags</dt><dd className="font-medium">{g.secondaryFlags.join(', ') || '–'}</dd></div>
                      <div><dt className="text-subtle">Plan</dt><dd className="font-medium">{f.ranks.slice(0, 3).join(', ')}</dd></div>
                    </dl>
                    {g.validation ? <Validation v={g.validation} /> : (
                      <ValidateGapForm action={validateGap} sectionId={section.id} learnerId={g.learnerId} gapId={g.id} code={g.code} gapJson={g.isPersona ? undefined : JSON.stringify(stripRow(g))} />
                    )}
                  </CardBody>
                </Card>
              );
            })}
          </div>
        </>
      )}
    </>
  );
}

/** A Gap Log row back to a plain GapRecord (for background learners' first validation). */
function stripRow(g: GapLogRow): GapRecord {
  const { studentName: _n, isPersona: _p, subtopicName: _s, chapterName: _c, ...rec } = g;
  return rec;
}
