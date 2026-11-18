import { BookOpen, Brain, Gauge, Repeat } from 'lucide-react';
import { RadarChart, TrendChart } from '@/components/charts';
import { ChildSwitcher } from '@/components/parent/child-switcher';
import { parentContext, type SearchParams } from '@/components/parent/context';
import { fmtDate } from '@/components/parent/format';
import { NoChild } from '@/components/parent/no-child';
import { BandBadge, Card, CardBody, CardHeader, EmptyState, GAP_LABEL, GapBadge, LEVEL_LABEL, PageHeader, Progress, StatTile, Table, TBody, TD, TH, THead, TR } from '@/components/ui';
import { addDaysLocal, demoToday, getAlr, getGaps, getMastery, getSubject, getSubtopic, type AlrRecord } from '@/lib/data';
import { formatHours, formatPercent } from '@/lib/format';

const INDICES = [
  { key: 'dK', label: 'Knowledge gain' },
  { key: 'R', label: 'Retention' },
  { key: 'TQ', label: 'Transfer' },
  { key: 'CE', label: 'Efficiency' },
  { key: 'ECV', label: 'Error correction' },
  { key: 'MCI', label: 'Confidence accuracy' },
] as const;

function meanOf(rows: AlrRecord[], k: (typeof INDICES)[number]['key'] | 'LRS'): number | null {
  const latest = new Map<string, AlrRecord>();
  for (const r of rows) latest.set(r.chapterId, r);
  // Indices the engine marked missing (no evidence) are left out, as the LRS does.
  const xs = [...latest.values()].filter((r) => !r.missing?.includes(k)).map((r) => r[k]).filter((x) => typeof x === 'number');
  return xs.length ? Math.min(1, xs.reduce((a, b) => a + b, 0) / xs.length) : null;
}

export default async function ParentProgress({ searchParams }: { searchParams: SearchParams }) {
  const { children, child } = await parentContext(searchParams);
  if (!child) return (<><PageHeader eyebrow="Parent" title="Progress" /><NoChild /></>);
  const s = child.student;
  const mastery = getMastery(s.id);
  const gaps = getGaps(s.id, { status: 'open' });
  const alr = getAlr(s.id);
  const cutoff = addDaysLocal(demoToday(), -28);
  const past = alr.history.filter((h) => h.asOfUtc.slice(0, 10) <= cutoff);

  const subjects = s.subjects.map(({ subjectId, depth }) => {
    const m = mastery.filter((x) => x.subjectId === subjectId);
    const b = getSubject(subjectId);
    const total = b?.subtopics.length ?? m.length;
    const avg = m.length ? m.reduce((a, x) => a + x.pMastery, 0) / m.length : null;
    const mastered = m.filter((x) => x.level >= 5).length;
    const g = gaps.filter((x) => x.subjectId === subjectId);
    return { subjectId, depth, name: b?.subject.name ?? subjectId, avg, tested: m.length, total, mastered, gaps: g.length, hours: g.reduce((a, x) => a + x.hoursToClose, 0) };
  }).filter((x) => x.tested > 0 || x.gaps > 0);

  const radar = INDICES.map((i) => ({ axis: i.label, now: meanOf(alr.history, i.key) ?? 0, before: meanOf(past, i.key) ?? 0 }));
  const hasAlr = alr.history.length > 0;
  const trend = (() => {
    const byWeek = new Map<string, AlrRecord[]>();
    for (const h of alr.history) {
      const wk = h.asOfUtc.slice(0, 10);
      const all = alr.history.filter((x) => x.asOfUtc.slice(0, 10) <= wk);
      byWeek.set(wk, all);
    }
    return [...byWeek.entries()].map(([wk, rows]) => ({ x: fmtDate(wk), lrs: meanOf(rows, 'LRS'), mci: meanOf(rows, 'MCI') }));
  })();
  const o = { LRS: meanOf(alr.history, 'LRS'), R: meanOf(alr.history, 'R'), MCI: meanOf(alr.history, 'MCI'), band: alr.history.length ? s.band : null };

  return (
    <>
      <PageHeader eyebrow="Parent" title={`${s.firstName}'s progress`} description="Mastery, gaps and learning rate by subject, measured against their own past." />
      <ChildSwitcher children={children} selectedId={s.id} basePath="/parent/progress" />

      <section className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatTile label="Learning rate (LRS)" value={o.LRS !== null ? o.LRS.toFixed(2) : '—'} icon={<Gauge />} hint={o.band ? <BandBadge band={o.band} /> : 'Needs a finished chapter'} />
        <StatTile label="Retention" value={o.R !== null ? formatPercent(o.R) : '—'} icon={<Repeat />} hint="Kept after 7 days" />
        <StatTile label="Confidence accuracy" value={o.MCI !== null ? o.MCI.toFixed(2) : '—'} icon={<Brain />} hint="How well they judge their own answers" />
        <StatTile label="Subtopics mastered" value={mastery.filter((m) => m.level >= 5).length} icon={<BookOpen />} hint={`of ${mastery.length} tested`} />
      </section>

      <div className="mb-6 grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader title="How they learn, now vs 4 weeks ago" description={`Six learning indices from ${s.firstName}'s tests. Compared only with ${s.firstName}'s own past.`} />
          <CardBody>
            {hasAlr ? <RadarChart data={radar} series={[{ key: 'now', label: 'Now' }, ...(past.length ? [{ key: 'before', label: '4 weeks ago' }] : [])]} />
              : <EmptyState className="border-0" title="Not enough tests yet" description="The radar fills in after the first finished chapter." />}
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Learning rate over time" description="LRS and confidence accuracy, year to date" />
          <CardBody>
            {trend.length > 1 ? <TrendChart data={trend} series={[{ key: 'lrs', label: 'LRS' }, { key: 'mci', label: 'Confidence accuracy' }]} target={{ value: 0.8, label: 'Excellent 0.80' }} />
              : <EmptyState className="border-0" title="Trend starts after two chapters" />}
          </CardBody>
        </Card>
      </div>

      <Card className="mb-6">
        <CardHeader title="Subject mastery" description="Average mastery of tested subtopics, and what is still open" />
        {subjects.length ? (
          <div className="overflow-x-auto">
            <Table className="mt-4 min-w-[560px]">
              <THead><TR><TH>Subject</TH><TH className="w-56">Mastery</TH><TH>Tested</TH><TH>Mastered</TH><TH>Open gaps</TH><TH>Hours to close</TH></TR></THead>
              <TBody>
                {subjects.map((x) => (
                  <TR key={x.subjectId}>
                    <TD className="font-medium text-ink">{x.name}</TD>
                    <TD><div className="flex items-center gap-2"><Progress value={x.avg ?? 0} tone={(x.avg ?? 0) < 0.4 ? 'danger' : (x.avg ?? 0) < 0.65 ? 'warning' : 'success'} /><span className="w-10 text-xs text-muted">{x.avg !== null ? formatPercent(x.avg) : '—'}</span></div></TD>
                    <TD>{x.tested} of {x.total}</TD><TD>{x.mastered}</TD><TD>{x.gaps}</TD><TD>{formatHours(x.hours)}</TD>
                  </TR>
                ))}
              </TBody>
            </Table>
          </div>
        ) : <CardBody><EmptyState className="border-0" title="No tests yet" description={`Subjects appear here after ${s.firstName}'s first test.`} /></CardBody>}
      </Card>

      <Card>
        <CardHeader title="Open gaps" description="What each gap means and how long it should take to close" />
        <CardBody className="pt-3">
          {gaps.length ? (
            <ul className="divide-y divide-line">
              {gaps.map((g) => {
                const st = getSubtopic(g.subtopicId);
                return (
                  <li key={g.id} className="flex flex-col gap-2 py-3 sm:flex-row sm:items-center sm:justify-between">
                    <div className="min-w-0">
                      <p className="font-medium text-ink">{st?.name ?? g.subtopicId}</p>
                      <p className="text-sm text-muted">{getSubject(g.subjectId)?.subject.name} · {st?.chapterName} · {LEVEL_LABEL[g.level]}</p>
                    </div>
                    <div className="flex flex-wrap items-center gap-2"><GapBadge code={g.code} />{g.secondaryFlags.map((f) => <span key={f} className="text-xs text-subtle">+ {GAP_LABEL[f]}</span>)}<span className="text-sm text-muted">{formatHours(g.hoursToClose)}</span></div>
                  </li>
                );
              })}
            </ul>
          ) : <EmptyState className="border-0" title="No open gaps" description={`${s.firstName} has no open gaps right now.`} />}
        </CardBody>
      </Card>
    </>
  );
}
