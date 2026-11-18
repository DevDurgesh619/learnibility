import Link from 'next/link';
import { AlertTriangle, CheckCircle2, ChevronLeft, Circle, FileText, XCircle } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { markSubmitted, moveApplication, recordDecision, requestRecommender, toggleChecklistItem, updateRecommender } from '@/lib/actions/applications';
import type { Application, DocumentRecord } from '@/lib/data/types';
import { DEMO_NOW } from '@/lib/demo-clock';
import type { University } from '@/lib/types';
import { cn } from '@/lib/utils';
import { ActionButton } from './action-button';
import { mainRoute } from './fit';
import { daysUntil, DECISION_LABEL, fmtDate, latestVersion, qaCheck, riskFlags, shortPrompt, STATUS_LABEL, STATUS_ORDER, wordCount } from './logic';
import { DaysLeft, FitBadge, SourcedFact, StatusBadge, UniMark } from './ui';
import { ROUTE_LABEL } from './university-detail';

const REC_TONE = { requested: 'neutral', drafting: 'warning', submitted: 'success' } as const;

export function ApplicationDetail({
  app, uni, viewer, studentName, counsellorFirst, documents, essayHref, backHref,
}: {
  app: Application;
  uni: University;
  viewer: 'student' | 'counsellor' | 'parent';
  studentName?: string;
  counsellorFirst: string;
  documents: DocumentRecord[];
  essayHref: (essayId: string) => string;
  backHref: string;
}) {
  const prog = uni.programmes.find((p) => p.id === app.programmeId);
  const route = uni.applicationRoutes.find((r) => r.type === app.routeType) ?? mainRoute(uni);
  const days = daysUntil(app.deadline, DEMO_NOW);
  const flags = riskFlags(app, DEMO_NOW);
  const qa = qaCheck(app, DEMO_NOW);
  const qaOk = qa.every((i) => i.ok);
  const canEdit = viewer !== 'parent' && app.status !== 'decision';
  const stepIdx = STATUS_ORDER.indexOf(app.status);

  return (
    <>
      <Link href={backHref} className="mb-3 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" />Applications</Link>
      <div className="mb-5 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="flex min-w-0 items-start gap-3">
          <UniMark uni={uni} size="lg" />
          <div className="min-w-0">
            {studentName && <p className="text-xs font-medium text-brand-700">{studentName}</p>}
            <h1 className="text-2xl font-semibold tracking-tight text-ink">{uni.shortName} · {prog?.name}</h1>
            <p className="mt-1 text-sm text-muted">
              {route ? ROUTE_LABEL[route.type] : app.routeType} · Your deadline {fmtDate(app.deadline)}
              {route && route.deadline.value !== app.deadline && <> · Official <SourcedFact fact={route.deadline}>{fmtDate(route.deadline.value)}</SourcedFact></>}
            </p>
            <div className="mt-2 flex flex-wrap items-center gap-2"><StatusBadge status={app.status} /><FitBadge band={app.fitGroup} />{app.status !== 'submitted' && app.status !== 'decision' && <DaysLeft days={days} />}</div>
          </div>
        </div>
        {viewer === 'student' && <Link href={`/student/universities/${uni.id}`} className={buttonVariants({ variant: 'secondary', size: 'sm' })}>University details</Link>}
      </div>

      <ol className="mb-6 grid grid-cols-5 gap-1" aria-label="Application stage">
        {STATUS_ORDER.map((s, i) => (
          <li key={s} className="min-w-0">
            <div className={cn('h-1.5 rounded-full', i <= stepIdx ? 'bg-brand-600' : 'bg-surface-muted')} />
            <p className={cn('mt-1 truncate text-[11px] sm:text-xs', i === stepIdx ? 'font-semibold text-brand-700' : 'text-subtle')}>{STATUS_LABEL[s]}</p>
          </li>
        ))}
      </ol>

      {flags.length > 0 && (
        <Card className="mb-6 border-danger-600/30 bg-danger-50/40">
          <CardBody className="space-y-1.5 py-3">
            {flags.map((f, i) => <p key={i} className="flex items-center gap-2 text-sm text-ink"><AlertTriangle className={cn('size-4', f.severity === 'high' ? 'text-danger-600' : 'text-warning-600')} />{f.text}</p>)}
          </CardBody>
        </Card>
      )}

      {app.status === 'decision' && app.decision && (
        <Card className="mb-6 border-success-600/30 bg-success-50/60">
          <CardBody className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div><p className="font-semibold text-ink">{DECISION_LABEL[app.decision]}</p><p className="text-sm text-muted">Finance, scholarships and visa steps are ready for this university.</p></div>
            {viewer === 'student' && <Link href="/student/applications/finance" className={buttonVariants({ size: 'sm' })}>Finance & Visa</Link>}
          </CardBody>
        </Card>
      )}

      <div className="grid grid-cols-[minmax(0,1fr)] gap-6 lg:grid-cols-[minmax(0,1fr)_340px]">
        <div className="space-y-6">
          <Card>
            <CardHeader title="Checklist" description={`${app.checklist.filter((c) => c.done).length} of ${app.checklist.length} done`} />
            <CardBody className="pt-2">
              {app.checklist.length === 0 ? <p className="text-sm text-muted">No items yet.</p> : (
                <ul className="divide-y divide-line">
                  {app.checklist.map((c) => (
                    <li key={c.id} className="flex items-center gap-3 py-2.5 text-sm">
                      {canEdit ? (
                        <form action={toggleChecklistItem.bind(null, app.id, c.id)}>
                          <button aria-label={`${c.done ? 'Untick' : 'Tick'} ${c.title}`} className={cn('flex size-5 items-center justify-center rounded border text-xs', c.done ? 'border-brand-600 bg-brand-600 text-white' : 'border-line bg-surface hover:border-brand-400')}>{c.done ? '✓' : ''}</button>
                        </form>
                      ) : c.done ? <CheckCircle2 className="size-5 text-success-600" /> : <Circle className="size-5 text-subtle" />}
                      <span className={cn('min-w-0 flex-1', c.done ? 'text-subtle line-through' : 'text-ink')}>{c.title}</span>
                      <Badge>{c.kind.replace('_', ' ')}</Badge>
                      {c.dueOn && !c.done && <span className="hidden text-xs text-subtle sm:inline">by {fmtDate(c.dueOn)}</span>}
                    </li>
                  ))}
                </ul>
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Essays" />
            <CardBody className="pt-2">
              {app.essays.length === 0 ? <p className="text-sm text-muted">This application needs no essays.</p> : (
                <ul className="divide-y divide-line">
                  {app.essays.map((e) => {
                    const v = latestVersion(e);
                    const open = e.comments.filter((c) => !c.resolved && !c.parentId).length;
                    return (
                      <li key={e.id} className="flex flex-col gap-2 py-3 sm:flex-row sm:items-center sm:justify-between">
                        <div className="min-w-0">
                          <p className="font-medium text-ink">{shortPrompt(e.prompt)}</p>
                          <p className="text-xs text-muted">v{v.version} · {wordCount(v.text)} / {e.wordLimit} words · {open} open comment{open === 1 ? '' : 's'}</p>
                        </div>
                        <div className="flex items-center gap-2">
                          <Badge tone={e.status === 'final' ? 'success' : e.status === 'in_review' ? 'info' : 'warning'}>{e.status === 'in_review' ? `With ${counsellorFirst}` : e.status === 'final' ? 'Final' : 'Drafting'}</Badge>
                          {viewer !== 'parent' && <Link href={essayHref(e.id)} className={buttonVariants({ variant: 'secondary', size: 'sm' })}>{viewer === 'counsellor' ? 'Review' : 'Open'}</Link>}
                        </div>
                      </li>
                    );
                  })}
                </ul>
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Recommendation letters" description="Who you asked and where each letter is." />
            <CardBody className="pt-2">
              {app.recommenders.length === 0 ? <p className="text-sm text-muted">No letters requested{route?.requirements.recommendations ? ` yet. This route asks for ${route.requirements.recommendations}.` : '.'}</p> : (
                <ul className="divide-y divide-line">
                  {app.recommenders.map((r) => (
                    <li key={r.id} className="flex flex-col gap-2 py-3 text-sm sm:flex-row sm:items-center sm:justify-between">
                      <div>
                        <p className="font-medium text-ink">{r.name}</p>
                        <p className="text-xs text-muted">{r.role} · asked {fmtDate(r.requestedOn)} · due {fmtDate(r.dueOn)}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge tone={REC_TONE[r.status]}>{r.status === 'submitted' ? 'Received' : r.status === 'drafting' ? 'Drafting' : 'Requested'}</Badge>
                        {viewer === 'counsellor' && r.status !== 'submitted' && (
                          <ActionButton size="sm" variant="secondary" action={updateRecommender.bind(null, app.id, r.id, 'submitted')}>Mark received</ActionButton>
                        )}
                      </div>
                    </li>
                  ))}
                </ul>
              )}
              {viewer === 'student' && canEdit && (
                <form action={async (f: FormData) => { 'use server'; await requestRecommender(app.id, String(f.get('name') ?? ''), String(f.get('role') ?? ''), String(f.get('due') ?? '')); }} className="mt-3 grid gap-2 border-t border-line pt-3 sm:grid-cols-[1fr_1fr_140px_auto]">
                  <input name="name" required placeholder="Teacher's name" aria-label="Recommender name" className="h-9 rounded-lg border border-line px-3 text-sm" />
                  <input name="role" placeholder="Subject or role" aria-label="Recommender role" className="h-9 rounded-lg border border-line px-3 text-sm" />
                  <input name="due" type="date" aria-label="Due date" defaultValue={app.deadline} className="h-9 rounded-lg border border-line px-2 text-sm" />
                  <button className={buttonVariants({ variant: 'secondary', size: 'sm' })}>Request letter</button>
                </form>
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Documents" description="From your vault (Inventory, application documents)." action={viewer === 'student' ? <Link href="/student/inventory" className="text-sm font-medium text-brand-700 hover:underline">Open vault ↗</Link> : undefined} />
            <CardBody className="pt-2">
              {documents.length === 0 ? <p className="text-sm text-muted">No documents linked yet.</p> : (
                <ul className="divide-y divide-line">
                  {documents.map((d) => (
                    <li key={d.id} className="flex items-center gap-3 py-2.5 text-sm">
                      <FileText className="size-4 text-subtle" />
                      <span className="min-w-0 flex-1 truncate text-ink">{d.title}</span>
                      <span className="text-xs text-subtle">{fmtDate(d.uploadedUtc)}</span>
                    </li>
                  ))}
                </ul>
              )}
            </CardBody>
          </Card>
        </div>

        <div className="space-y-6">
          <Card className={cn(qaOk ? 'border-success-600/40' : '')}>
            <CardHeader title="Pre-submission QA" description={qaOk ? 'Everything checks out.' : `${qa.filter((i) => !i.ok).length} thing${qa.filter((i) => !i.ok).length === 1 ? '' : 's'} to fix before you submit.`} />
            <CardBody className="pt-2">
              <ul className="space-y-2.5">
                {qa.map((i) => (
                  <li key={i.id} className="flex gap-2 text-sm">
                    {i.ok ? <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-success-600" /> : <XCircle className="mt-0.5 size-4 shrink-0 text-danger-600" />}
                    <div className="min-w-0"><p className="text-ink">{i.label}</p>{i.detail && <p className="text-xs break-words text-muted">{i.detail}</p>}</div>
                  </li>
                ))}
              </ul>
              {viewer === 'student' && (app.status === 'collecting_documents' || app.status === 'in_review' || app.status === 'shortlisted') && (
                <div className="mt-4 border-t border-line pt-4">
                  <ActionButton className="w-full" disabled={!qaOk} action={markSubmitted.bind(null, app.id)} pendingLabel="Submitting">Mark as submitted</ActionButton>
                  {!qaOk && <p className="mt-2 text-xs text-subtle">Unlocks when every check passes.</p>}
                </div>
              )}
              {viewer === 'counsellor' && app.status === 'collecting_documents' && (
                <div className="mt-4 border-t border-line pt-4"><ActionButton variant="secondary" className="w-full" action={moveApplication.bind(null, app.id, 'in_review')}>Move to in review</ActionButton></div>
              )}
              {viewer === 'counsellor' && app.status === 'submitted' && (
                <div className="mt-4 space-y-2 border-t border-line pt-4">
                  <p className="text-xs font-medium text-muted">Record the decision</p>
                  <div className="flex flex-wrap gap-2">
                    <ActionButton size="sm" action={recordDecision.bind(null, app.id, 'offer')}>Offer</ActionButton>
                    <ActionButton size="sm" variant="secondary" action={recordDecision.bind(null, app.id, 'conditional_offer')}>Conditional</ActionButton>
                    <ActionButton size="sm" variant="secondary" action={recordDecision.bind(null, app.id, 'waitlisted')}>Waitlisted</ActionButton>
                    <ActionButton size="sm" variant="ghost" action={recordDecision.bind(null, app.id, 'rejected')}>Not successful</ActionButton>
                  </div>
                </div>
              )}
            </CardBody>
          </Card>
          {route && (
            <Card>
              <CardHeader title="Requirements" description={`From the university, as of ${fmtDate(route.deadline.asOf)}`} />
              <CardBody className="space-y-1.5 pt-2 text-sm text-muted">
                {(prog?.typicalOffer ?? route.requirements.typicalOffer) && <p><span className="text-ink">Typical offer:</span> {prog?.typicalOffer ?? route.requirements.typicalOffer}</p>}
                {route.requirements.ielts && <p><span className="text-ink">English:</span> IELTS {route.requirements.ielts}{route.requirements.toefl ? ` or TOEFL ${route.requirements.toefl}` : ''}</p>}
                {route.requirements.otherItems.slice(0, 3).map((o) => <p key={o}>· {o}</p>)}
              </CardBody>
            </Card>
          )}
        </div>
      </div>
    </>
  );
}
