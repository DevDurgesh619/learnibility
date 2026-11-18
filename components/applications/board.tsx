import Link from 'next/link';
import { AlertTriangle } from 'lucide-react';
import { Card } from '@/components/ui/card';
import type { Application, ApplicationStatus } from '@/lib/data/types';
import type { University } from '@/lib/types';
import { DEMO_NOW } from '@/lib/demo-clock';
import { cn } from '@/lib/utils';
import { daysUntil, DECISION_LABEL, latestVersion, STATUS_LABEL, STATUS_ORDER } from './logic';
import { DaysLeft, FitBadge } from './ui';

const EMPTY_LINE: Record<ApplicationStatus, string> = {
  shortlisted: 'Nothing shortlisted. Add from Universities.',
  collecting_documents: 'No documents being collected.',
  in_review: 'Nothing with your counsellor right now.',
  submitted: 'Nothing submitted yet.',
  decision: 'No decisions yet.',
};

/** Kanban board (PDF 7c). Student and counsellor share it; the counsellor sees student names. */
export function ApplicationsBoard({
  apps, unis, hrefFor, studentNames, closest, counsellorFirst = 'your counsellor',
}: {
  apps: Application[];
  unis: Map<string, University>;
  hrefFor: (a: Application) => string;
  studentNames?: Record<string, string>;
  closest?: string;
  counsellorFirst?: string;
}) {
  return (
    <div className="-mx-4 overflow-x-auto px-4 pb-2 sm:mx-0 sm:px-0">
      <div className="grid min-w-[1100px] grid-cols-5 gap-3">
        {STATUS_ORDER.map((status) => {
          const col = apps.filter((a) => a.status === status).sort((a, b) => a.deadline.localeCompare(b.deadline));
          return (
            <section key={status} className="flex flex-col rounded-[var(--radius-card)] bg-surface-muted/70 p-2.5" aria-label={STATUS_LABEL[status]}>
              <h2 className="mb-2 flex items-center justify-between px-1 text-sm font-semibold text-ink">
                {STATUS_LABEL[status]}<span className="rounded-full bg-surface px-2 text-xs font-medium text-muted">{col.length}</span>
              </h2>
              <div className="flex flex-col gap-2">
                {col.length === 0 && (
                  <p className="px-1 py-2 text-xs text-subtle">{status === 'submitted' && closest ? `Nothing yet. ${closest} is closest.` : EMPTY_LINE[status]}</p>
                )}
                {col.map((a) => {
                  const u = unis.get(a.universityId);
                  const prog = u?.programmes.find((p) => p.id === a.programmeId);
                  const open = a.checklist.filter((c) => !c.done);
                  const days = daysUntil(a.deadline, DEMO_NOW);
                  const essayInReview = a.essays.find((e) => e.status === 'in_review');
                  return (
                    <Link key={a.id} href={hrefFor(a)} className="block">
                      <Card className={cn('p-3 transition-colors hover:border-brand-300', a.riskFlags?.length && 'border-danger-600/40')}>
                        {studentNames && <p className="mb-1 text-xs font-medium text-brand-700">{studentNames[a.learnerId] ?? a.learnerId}</p>}
                        <div className="flex items-start justify-between gap-2">
                          <p className="font-semibold leading-tight text-ink">{u?.shortName ?? a.universityId}</p>
                          <FitBadge band={a.fitGroup} />
                        </div>
                        <p className="mt-0.5 line-clamp-2 text-xs text-muted">{prog?.name}</p>
                        {status === 'decision' ? (
                          <p className={cn('mt-2 text-sm font-medium', a.decision === 'rejected' ? 'text-danger-700' : 'text-success-700')}>{a.decision ? DECISION_LABEL[a.decision] : 'Decision in'}</p>
                        ) : status === 'submitted' ? (
                          <p className="mt-2 text-xs text-muted">Submitted. Decision by {u?.applicationRoutes.find((r) => r.type === a.routeType)?.decisionBy ?? 'spring'}</p>
                        ) : (
                          <>
                            <ul className="mt-2 space-y-1">
                              {a.checklist.slice(0, 3).map((c) => (
                                <li key={c.id} className="flex items-center gap-1.5 text-xs">
                                  <span className={cn('inline-block size-3 shrink-0 rounded-sm border', c.done ? 'border-ink bg-ink' : 'border-line bg-surface')} />
                                  <span className={cn('truncate', c.done ? 'text-subtle' : 'text-ink')}>{c.title}</span>
                                </li>
                              ))}
                              {a.checklist.length > 3 && <li className="text-xs text-subtle">+{a.checklist.length - 3} more · {open.length} open</li>}
                            </ul>
                            {essayInReview && <p className="mt-2 text-xs text-info-600">{counsellorFirst} reviewing essay v{latestVersion(essayInReview).version}</p>}
                          </>
                        )}
                        <div className="mt-2 flex items-center justify-between gap-2">
                          {status !== 'decision' && status !== 'submitted' ? <DaysLeft days={days} /> : <span />}
                          {a.riskFlags?.length ? <AlertTriangle className="size-3.5 text-danger-600" aria-label={a.riskFlags.join('; ')} /> : null}
                        </div>
                      </Card>
                    </Link>
                  );
                })}
              </div>
            </section>
          );
        })}
      </div>
    </div>
  );
}
