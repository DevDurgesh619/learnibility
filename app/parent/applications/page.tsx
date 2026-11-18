import Link from 'next/link';
import { AlertTriangle, Lock } from 'lucide-react';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import { PageHeader } from '@/components/ui/page-header';
import { Progress } from '@/components/ui/progress';
import { Table, TBody, TD, TH, THead, TR } from '@/components/ui/table';
import { applicationsBundle, nameOf, studentCtx, uniMap } from '@/components/applications/data';
import { daysUntil, DECISION_LABEL, fmtDate, progress } from '@/components/applications/logic';
import { DaysLeft, FitBadge, StatusBadge, UniMark } from '@/components/applications/ui';
import { getChildren } from '@/lib/data';
import { DEMO_NOW } from '@/lib/demo-clock';
import { currentPersona } from '@/lib/session';
import { cn } from '@/lib/utils';

export const metadata = { title: 'Applications · Parent · Learnibility' };

export default async function Page({ searchParams }: { searchParams: Promise<{ child?: string }> }) {
  const me = (await currentPersona())!;
  const children = getChildren(me.id).map((c) => c.student);
  const { child } = await searchParams;
  // Default to the child with the most application activity.
  const ranked = [...children].sort((a, b) => applicationsBundle(b.id).applications.length + applicationsBundle(b.id).shortlist.length - (applicationsBundle(a.id).applications.length + applicationsBundle(a.id).shortlist.length));
  const kid = children.find((c) => c.id === child) ?? ranked[0];

  if (!kid) {
    return (<><PageHeader eyebrow="Parent" title="Applications" /><EmptyState title="No children linked" description="Applications appear here once your child's account is linked to yours." /></>);
  }
  const b = applicationsBundle(kid.id);
  const ctx = studentCtx(kid.id);
  const unis = uniMap();
  const first = kid.firstName;
  const deadlines = b.applications.filter((a) => a.status !== 'submitted' && a.status !== 'decision').sort((x, y) => x.deadline.localeCompare(y.deadline));

  return (
    <>
      <PageHeader eyebrow="Parent" title="Applications" description={`University deadlines and status for ${first}. Read only: ${first} and ${ctx.counsellorId ? nameOf(ctx.counsellorId) : 'the counsellor'} make the changes.`} />
      {children.length > 1 && (
        <div className="mb-5 flex flex-wrap gap-2">
          {children.map((c) => (
            <Link key={c.id} href={`?child=${c.id}`} className={cn('rounded-full border px-3 py-1 text-sm', c.id === kid.id ? 'border-ink bg-ink text-white' : 'border-line bg-surface text-ink')}>{c.firstName} · {c.programme}</Link>
          ))}
        </div>
      )}

      {b.applications.length === 0 ? (
        <>
          <EmptyState
            title={b.shortlist.length ? `${first} is still exploring` : `${first} has not started applications`}
            description={b.shortlist.length ? `${first} has saved ${b.shortlist.length} universit${b.shortlist.length === 1 ? 'y' : 'ies'} in University Fit. Applications show here once ${first} starts Application Support.` : 'Nothing to show yet.'}
          />
          {b.shortlist.length > 0 && (
            <Card className="mt-6">
              <CardHeader title="Saved universities" />
              <CardBody className="pt-2">
                <ul className="divide-y divide-line">
                  {b.shortlist.map((s) => {
                    const u = unis.get(s.universityId);
                    return u && (
                      <li key={s.universityId} className="flex items-center gap-3 py-2.5 text-sm">
                        <UniMark uni={u} size="sm" />
                        <span className="min-w-0 flex-1 truncate text-ink">{u.name}<span className="text-muted"> · {u.programmes.find((p) => p.id === s.programmeId)?.name}</span></span>
                        {s.fitGroup && <FitBadge band={s.fitGroup} />}
                      </li>
                    );
                  })}
                </ul>
              </CardBody>
            </Card>
          )}
        </>
      ) : (
        <div className="grid grid-cols-[minmax(0,1fr)] gap-6 lg:grid-cols-[minmax(0,1fr)_320px]">
          <Card>
            <CardHeader title={`${b.applications.length} applications`} />
            <CardBody className="pt-3">
              <Table>
                <THead><TR><TH>University</TH><TH>Stage</TH><TH>Progress</TH><TH>Deadline</TH></TR></THead>
                <TBody>
                  {b.applications.map((a) => {
                    const u = unis.get(a.universityId);
                    return (
                      <TR key={a.id}>
                        <TD>
                          <p className="font-medium text-ink">{u?.shortName}</p>
                          <p className="text-xs text-muted">{u?.programmes.find((p) => p.id === a.programmeId)?.name}</p>
                        </TD>
                        <TD><div className="flex flex-col items-start gap-1"><StatusBadge status={a.status} />{a.decision && <span className="text-xs font-medium text-success-700">{DECISION_LABEL[a.decision]}</span>}</div></TD>
                        <TD className="min-w-28"><Progress value={progress(a)} /><span className="text-xs text-subtle">{a.checklist.filter((c) => c.done).length}/{a.checklist.length} items</span></TD>
                        <TD className="whitespace-nowrap">{fmtDate(a.deadline)}{a.status !== 'submitted' && a.status !== 'decision' && <div><DaysLeft days={daysUntil(a.deadline, DEMO_NOW)} /></div>}</TD>
                      </TR>
                    );
                  })}
                </TBody>
              </Table>
            </CardBody>
          </Card>
          <div className="space-y-6">
            {b.applications.some((a) => a.riskFlags?.length) && (
              <Card className="border-danger-600/30 bg-danger-50/40">
                <CardBody className="space-y-2 py-3">
                  {b.applications.flatMap((a) => (a.riskFlags ?? []).map((f, i) => (
                    <p key={`${a.id}${i}`} className="flex gap-2 text-sm"><AlertTriangle className="mt-0.5 size-4 shrink-0 text-danger-600" /><span><span className="font-medium">{unis.get(a.universityId)?.shortName}:</span> {f}</span></p>
                  )))}
                </CardBody>
              </Card>
            )}
            <Card>
              <CardHeader title="Next deadlines" />
              <CardBody className="pt-2">
                {deadlines.length === 0 ? <p className="text-sm text-muted">Everything is submitted.</p> : (
                  <ul className="space-y-3">
                    {deadlines.slice(0, 5).map((a) => (
                      <li key={a.id} className="flex items-center justify-between gap-2 text-sm">
                        <span className="text-ink">{unis.get(a.universityId)?.shortName} <span className="text-subtle">· {fmtDate(a.deadline)}</span></span>
                        <DaysLeft days={daysUntil(a.deadline, DEMO_NOW)} />
                      </li>
                    ))}
                  </ul>
                )}
              </CardBody>
            </Card>
            <p className="flex gap-2 text-xs text-subtle"><Lock className="mt-0.5 size-3.5 shrink-0" />Essays and counsellor comments stay between {first} and the counsellor.</p>
          </div>
        </div>
      )}
    </>
  );
}
