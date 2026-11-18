import Link from 'next/link';
import { CalendarDays, Plus } from 'lucide-react';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import { applicationsBundle, firstName, getUniversity } from '@/components/applications/data';
import { requireSubscriber } from '@/components/applications/guard';
import { DECISION_LABEL, fmtDate } from '@/components/applications/logic';
import { SupportHeader } from '@/components/applications/support-header';
import { toggleFinanceItem } from '@/lib/actions/applications';
import { cn } from '@/lib/utils';

export const metadata = { title: 'Finance & Visa · Learnibility' };

function Check({ done, label, extra, action }: { done: boolean; label: string; extra?: React.ReactNode; action: () => Promise<void> }) {
  return (
    <li className="flex items-center gap-3 py-2.5 text-sm">
      <form action={action}><button aria-label={`${done ? 'Untick' : 'Tick'} ${label}`} className={cn('flex size-5 items-center justify-center rounded border text-xs', done ? 'border-ink bg-ink text-white' : 'border-line bg-surface hover:border-brand-400')}>{done ? '✓' : ''}</button></form>
      <span className={cn('min-w-0 flex-1', done ? 'text-muted' : 'text-ink')}>{label}</span>
      {extra}
    </li>
  );
}

export default async function Page({ searchParams }: { searchParams: Promise<{ uni?: string }> }) {
  const { persona, ctx, counsellorName } = await requireSubscriber();
  const b = applicationsBundle(persona.id);
  const sp = await searchParams;
  const f = b.finance.find((x) => x.universityId === sp.uni) ?? b.finance[0];
  const app = f && b.applications.find((a) => a.universityId === f.universityId);
  const uni = f && getUniversity(f.universityId);
  return (
    <>
      <SupportHeader active="finance" counsellorName={counsellorName} />
      {!f || !uni ? (
        <EmptyState title="Finance and visa start with an offer" description="Once a university makes you an offer, scholarships, proof of funds and visa steps for it appear here." action={<Link href="/student/applications/board" className="text-sm font-medium text-brand-700 hover:underline">See your applications</Link>} />
      ) : (
        <>
          <div className="mb-5 flex flex-wrap items-center gap-2 text-sm">
            <span className="text-muted">For:</span>
            {b.finance.map((x) => (
              <Link key={x.universityId} href={`?uni=${x.universityId}`} className={cn('rounded-full px-3 py-1 font-medium', x.universityId === f.universityId ? 'bg-ink text-white' : 'border border-line bg-surface text-ink')}>
                {getUniversity(x.universityId)?.shortName} ({app?.decision ? DECISION_LABEL[app.decision].toLowerCase() : 'accepted'})
              </Link>
            ))}
          </div>
          <div className="grid gap-6 lg:grid-cols-2">
            <div className="space-y-6">
              <Card>
                <CardHeader title="Financial aid and scholarships" />
                <CardBody className="pt-1">
                  <ul className="divide-y divide-line">
                    {f.aid.map((x, i) => <Check key={i} done={x.done} label={x.title} action={toggleFinanceItem.bind(null, f.universityId, 'aid', i)} extra={x.status && !x.done ? <span className="rounded-full border border-line px-2 py-0.5 text-xs text-muted">{x.status}</span> : undefined} />)}
                  </ul>
                  {uni.scholarships.length > 0 && <p className="mt-3 text-xs text-subtle">Open to you: {uni.scholarships.map((s) => s.name).join(', ')}. Details on the <Link href={`/student/universities/${uni.id}?tab=costs`} className="underline">university page</Link>.</p>}
                </CardBody>
              </Card>
              <Card>
                <CardHeader title="Visa application" />
                <CardBody className="pt-1">
                  <ul className="divide-y divide-line">
                    {f.visa.map((x, i) => <Check key={i} done={x.done} label={x.title} action={toggleFinanceItem.bind(null, f.universityId, 'visa', i)} extra={x.date ? <span className="text-xs font-medium text-ink">{fmtDate(x.date)}</span> : undefined} />)}
                  </ul>
                </CardBody>
              </Card>
            </div>
            <div className="space-y-6">
              <Card>
                <CardHeader title="Appointments" />
                <CardBody className="space-y-3 pt-2">
                  {f.appointments.length === 0 ? <p className="text-sm text-muted">No appointments booked.</p> : f.appointments.map((x, i) => (
                    <div key={i} className="flex items-start gap-3 rounded-lg border border-line p-3 text-sm">
                      <CalendarDays className="mt-0.5 size-4 text-brand-600" />
                      <div><p className="font-medium text-ink">{x.title}</p><p className="text-muted">{fmtDate(x.date)}{x.place ? ` · ${x.place}` : ''}</p></div>
                    </div>
                  ))}
                  <Link href="/student/sessions" className="inline-block text-sm font-medium text-brand-700 hover:underline">Book another slot with {firstName(ctx.counsellorId)}</Link>
                </CardBody>
              </Card>
              <Card>
                <CardHeader title="Visa document pocket" description="Kept in your vault under application documents." />
                <CardBody className="flex flex-wrap gap-2 pt-3">
                  {f.visaDocs.map((x, i) => (
                    <form key={i} action={toggleFinanceItem.bind(null, f.universityId, 'visaDocs', i)}>
                      <button className={cn('rounded-full border px-3 py-1 text-sm', x.done ? 'border-ink text-ink' : 'border-dashed border-line text-muted')}>{x.title} {x.done ? '✓' : ''}</button>
                    </form>
                  ))}
                  <Link href="/student/inventory" className="inline-flex items-center gap-1 rounded-full border border-success-600/40 px-3 py-1 text-sm text-success-700"><Plus className="size-3.5" />Add</Link>
                </CardBody>
              </Card>
            </div>
          </div>
        </>
      )}
    </>
  );
}
