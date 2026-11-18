import Link from 'next/link';
import { AlertTriangle } from 'lucide-react';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import { PageHeader } from '@/components/ui/page-header';
import { StatTile } from '@/components/ui/stat-tile';
import { Table, TBody, TD, TH, THead, TR } from '@/components/ui/table';
import { ApplicationsBoard } from '@/components/applications/board';
import { caseloadApplications, caseloadLearners, nameOf, uniMap } from '@/components/applications/data';
import { daysUntil, fmtDate, nextStep, STATUS_LABEL } from '@/components/applications/logic';
import { DaysLeft, StatusBadge } from '@/components/applications/ui';
import { DEMO_NOW } from '@/lib/demo-clock';
import { currentPersona } from '@/lib/session';
import { cn } from '@/lib/utils';

export const metadata = { title: 'Applications pipeline · Learnibility' };

export default async function Page({ searchParams }: { searchParams: Promise<{ student?: string }> }) {
  const me = (await currentPersona())!;
  const { student } = await searchParams;
  const all = caseloadApplications(me.id);
  const learners = caseloadLearners(me.id);
  const names = Object.fromEntries(learners.map((id) => [id, nameOf(id)]));
  const apps = student ? all.filter((a) => a.learnerId === student) : all;
  const unis = uniMap();
  const flagged = apps.filter((a) => a.riskFlags?.length);
  const essays = apps.flatMap((a) => a.essays.filter((e) => e.status === 'in_review'));
  const upcoming = apps.filter((a) => a.status !== 'submitted' && a.status !== 'decision').sort((x, y) => x.deadline.localeCompare(y.deadline));

  return (
    <>
      <PageHeader eyebrow="Counsellor" title="Applications pipeline" description="Every application across your students, from shortlist to decision." />
      {all.length === 0 ? (
        <EmptyState title="No applications in your caseload" description="Applications appear here when a student you counsel on applications shortlists a university." />
      ) : (
        <>
          <div className="mb-4 flex flex-wrap gap-2">
            <Link href="/counsellor/applications" className={cn('rounded-full border px-3 py-1 text-sm', !student ? 'border-ink bg-ink text-white' : 'border-line bg-surface text-ink')}>All students</Link>
            {learners.map((id) => (
              <Link key={id} href={`?student=${id}`} className={cn('rounded-full border px-3 py-1 text-sm', student === id ? 'border-ink bg-ink text-white' : 'border-line bg-surface text-ink')}>
                {names[id]} <span className="text-xs opacity-70">{all.filter((a) => a.learnerId === id).length}</span>
              </Link>
            ))}
          </div>
          <div className="mb-6 grid grid-cols-2 gap-3 lg:grid-cols-4">
            <StatTile label="Applications" value={apps.length} hint={`${new Set(apps.map((a) => a.learnerId)).size} students`} />
            <StatTile label="Risk flags" value={flagged.length} hint="Deadline under 14 days with open items" />
            <StatTile label="Essays to review" value={essays.length} hint={<Link href="/counsellor/draft-reviews" className="underline">Open draft reviews</Link>} />
            <StatTile label="Decisions in" value={apps.filter((a) => a.status === 'decision').length} />
          </div>
          {flagged.length > 0 && (
            <Card className="mb-6 border-danger-600/30 bg-danger-50/40">
              <CardBody className="space-y-2 py-3">
                {flagged.map((a) => a.riskFlags!.map((f, i) => (
                  <Link key={`${a.id}-${i}`} href={`/counsellor/applications/${a.id}`} className="flex items-center gap-2 text-sm hover:underline">
                    <AlertTriangle className="size-4 text-danger-600" /><span className="font-medium text-ink">{names[a.learnerId]} · {unis.get(a.universityId)?.shortName}:</span><span className="text-muted">{f}</span>
                  </Link>
                )))}
              </CardBody>
            </Card>
          )}
          <ApplicationsBoard apps={apps} unis={unis} hrefFor={(a) => `/counsellor/applications/${a.id}`} studentNames={student ? undefined : names} counsellorFirst="You" />
          <Card className="mt-6">
            <CardHeader title="Upcoming deadlines" />
            <CardBody className="pt-3">
              <Table>
                <THead><TR><TH>Student</TH><TH>University</TH><TH>Stage</TH><TH>Next step</TH><TH>Deadline</TH></TR></THead>
                <TBody>
                  {upcoming.map((a) => (
                    <TR key={a.id}>
                      <TD className="font-medium text-ink">{names[a.learnerId]}</TD>
                      <TD><Link href={`/counsellor/applications/${a.id}`} className="hover:underline">{unis.get(a.universityId)?.shortName}</Link></TD>
                      <TD><StatusBadge status={a.status} /></TD>
                      <TD className="max-w-xs truncate text-muted" title={nextStep(a, 'you')}>{nextStep(a, 'you')}</TD>
                      <TD className="whitespace-nowrap">{fmtDate(a.deadline)} <DaysLeft days={daysUntil(a.deadline, DEMO_NOW)} className="ml-1" /></TD>
                    </TR>
                  ))}
                </TBody>
              </Table>
              {upcoming.length === 0 && <p className="py-3 text-sm text-muted">Nothing left to submit. {STATUS_LABEL.submitted} applications are waiting for decisions.</p>}
            </CardBody>
          </Card>
        </>
      )}
    </>
  );
}
