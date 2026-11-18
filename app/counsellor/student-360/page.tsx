import Link from 'next/link';
import { ShieldCheck } from 'lucide-react';
import { FilterChips } from '@/components/counsellor/filter-chips';
import { buildStudent360, overallCompleteness } from '@/components/counsellor/profile360';
import { DensityOverview, SectionTable } from '@/components/counsellor/student-360-view';
import { StudentPicker } from '@/components/counsellor/student-picker';
import { loadStudent360 } from '@/components/counsellor/load';
import { Avatar, Badge, BandBadge, Button, Card, CardBody, EmptyState, PageHeader, StatTile } from '@/components/ui';
import type { Tier } from '@/lib/types';

export const dynamic = 'force-dynamic';

export default async function Student360Page({ searchParams }: { searchParams: Promise<{ student?: string; tier?: string; view?: string }> }) {
  const sp = await searchParams;
  const data = await loadStudent360(sp.student);
  if (!data) return <EmptyState title="No students in your caseload" description="Students appear here once they are assigned to you." />;
  const { student, students, params, values, now, alr, openGaps } = data;
  const tier = (['T1', 'T2', 'T3', 'C'] as const).find((t) => t === sp.tier) as Tier | undefined;
  const filledOnly = sp.view === 'filled';
  const sections = buildStudent360(tier ? params.filter((p) => p.tier === tier) : params, values, now);
  const all = buildStudent360(params, values, now);
  const completeness = overallCompleteness(all);
  const filled = all.reduce((s, x) => s + x.filled, 0);
  const low = all.reduce((s, x) => s + x.lowConfidence, 0);
  const stale = all.reduce((s, x) => s + x.stale, 0);

  return (
    <>
      <PageHeader eyebrow="Student 360" title={student.name} description={`${student.programme} · ${student.school}, ${student.city}`}
        actions={<StudentPicker students={students} value={student.id} />} />

      <Card className="mb-6">
        <CardBody className="flex flex-col gap-4 sm:flex-row sm:items-center">
          <Avatar name={student.name} src={student.avatar} size="lg" />
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <BandBadge band={student.band} />
              <Badge tone="brand">{student.plan === 'free' ? 'Free plan' : student.plan === 'application_support' ? 'Application Support' : 'Full package'}</Badge>
              <Badge>{student.weeklyHours} h a week</Badge>
            </div>
            {student.story && <p className="mt-2 text-sm text-muted">{student.story}</p>}
          </div>
          <div className="flex flex-wrap gap-2">
            <Link href={`/counsellor/career-sessions?student=${student.id}`}><Button variant="secondary">Career session</Button></Link>
            <Link href={`/counsellor/timetable-requests?student=${student.id}`}><Button variant="secondary">Timetable requests</Button></Link>
          </div>
        </CardBody>
      </Card>

      <div className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatTile label="Profile complete" value={`${Math.round(completeness * 100)}%`} hint={`${filled} of 430 parameters`} />
        <StatTile label="Learning rate (LRS)" value={alr != null ? alr.toFixed(2) : '—'} hint="year to date" />
        <StatTile label="Open gaps" value={openGaps} />
        <StatTile label="Needs attention" value={low + stale} hint={`${low} low confidence · ${stale} stale`} />
      </div>

      <div className="mb-6"><DensityOverview sections={all} /></div>

      <div className="mb-3 flex items-start gap-2 rounded-lg bg-info-50 px-4 py-3 text-sm text-info-600">
        <ShieldCheck className="mt-0.5 size-4 shrink-0" />
        <p>You see every tier. T2 and T3 values never leave this screen verbatim: parents get summaries, teachers, tutors and mentors never see them, and T3 never feeds ranking, admissions fit or career fit.</p>
      </div>

      <div className="mb-4 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <FilterChips base="/counsellor/student-360" param="tier" value={tier} keep={{ student: student.id, view: sp.view }} options={[
          { value: '', label: 'All tiers' }, { value: 'T1', label: 'T1 Standard' }, { value: 'T2', label: 'T2 Elevated' }, { value: 'T3', label: 'T3 Sensitive' }, { value: 'C', label: 'Consent' },
        ]} />
        <FilterChips base="/counsellor/student-360" param="view" value={sp.view} keep={{ student: student.id, tier }} options={[
          { value: '', label: 'All parameters' }, { value: 'filled', label: 'Collected only' },
        ]} />
      </div>

      <div className="space-y-3">
        {sections.filter((s) => s.total > 0).map((s, i) => <SectionTable key={s.section} section={s} open={i === 0} filledOnly={filledOnly} />)}
      </div>
    </>
  );
}
