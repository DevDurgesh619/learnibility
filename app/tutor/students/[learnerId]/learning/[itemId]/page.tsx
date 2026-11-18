import Link from 'next/link';
import { notFound } from 'next/navigation';
import { CheckCircle2, CircleAlert, XCircle } from 'lucide-react';
import { BackLink, Delta, SectionTitle } from '@/components/tutor/bits';
import { itemReview, studentContext } from '@/components/tutor/model';
import { formatDay } from '@/components/marketplace/dates';
import { Badge } from '@/components/ui/badge';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { Table, TBody, TD, TH, THead, TR } from '@/components/ui/table';
import { currentPersona } from '@/lib/session';
import { cn } from '@/lib/utils';

/** 4d gap analysis of one assessment + 4e question level. */
export default async function ItemPage({ params }: { params: Promise<{ learnerId: string; itemId: string }> }) {
  const { learnerId, itemId } = await params;
  const { ws, row } = studentContext((await currentPersona())!.id, learnerId)!;
  const r = itemReview(ws, learnerId, itemId);
  if (!r) notFound();
  const base = `/tutor/students/${learnerId}`;
  const band = r.pct >= 80 ? ['Strong', 'success'] : r.pct >= 60 ? ['On track', 'info'] : ['Needs improvement', 'warning'];
  return (
    <div className="space-y-6">
      <BackLink href={`${base}/learning`}>Learning · {r.title} · {formatDay(r.date)}{r.minutes ? ` · ${r.minutes} min` : ''}</BackLink>
      <Card>
        <CardBody className="grid gap-6 md:grid-cols-[180px_1fr]">
          <div className="text-center md:border-r md:border-line md:pr-6">
            <p className="text-4xl font-semibold text-ink">{r.pct}%</p>
            <Badge tone={band[1] as 'success'} className="mt-1">{band[0]}</Badge>
            <p className="mt-2 flex justify-center">{r.prevPct !== null ? <><Delta value={r.pct - r.prevPct} /><span className="ml-1 text-xs text-muted">vs previous</span></> : <span className="text-xs text-muted">baseline</span>}</p>
          </div>
          <div className="space-y-2 text-sm">
            <p className="font-semibold text-ink">Overall feedback</p>
            <p><span className="font-medium text-success-700">Strength</span> <span className="text-ink">{r.strength}</span></p>
            <p><span className="font-medium text-danger-700">Weakness</span> <span className="text-ink">{r.weakness}</span></p>
            <p className="text-xs text-muted">Written by AI from the marked answers{r.kind === 'assignment' ? ' · edit it when you evaluate' : ''}</p>
          </div>
        </CardBody>
      </Card>

      {r.rows.length > 0 && (
        <Card>
          <Table>
            <THead><TR><TH>Topic</TH><TH>Band</TH><TH className="text-right">No. of Qs</TH><TH className="text-right">Mastery</TH></TR></THead>
            <TBody>
              {r.rows.map((x) => (
                <TR key={x.subtopicId}><TD className="text-ink">{x.name}</TD><TD><Badge tone={x.band === 'Strong' ? 'success' : x.band === 'Medium' ? 'warning' : 'danger'}>{x.band}</Badge></TD><TD className="text-right">{x.n}</TD><TD className="text-right font-medium">{x.pct}%</TD></TR>
              ))}
            </TBody>
          </Table>
        </Card>
      )}

      <Card className="border-brand-200 bg-brand-50/40">
        <CardBody className="flex flex-col gap-3 sm:flex-row sm:items-center">
          <div className="flex-1"><p className="text-sm font-semibold text-ink">Recommended next step</p><p className="text-sm text-ink">{r.nextStep}</p></div>
          <Link href={`${base}/assignments/new${r.weakest ? `?subtopic=${r.weakest}` : ''}`} className={buttonVariants({ size: 'sm' })}>Assign practice</Link>
          {row.nextSession && <Link href={`/tutor/sessions/${row.nextSession.id}/prep`} className={buttonVariants({ size: 'sm', variant: 'secondary' })}>Add to session plan</Link>}
        </CardBody>
      </Card>

      <section>
        <SectionTitle>Question level · {r.questions.length}</SectionTitle>
        {r.questions.length === 0 ? <p className="text-sm text-muted">This test was taken before question-level logging. Scores per topic come from the platform.</p> : (
          <>
            <div className="mb-3 flex flex-wrap gap-1.5">
              {r.questions.map((x) => <a key={x.n} href={`#q${x.n}`} className={cn('flex size-8 items-center justify-center rounded-md text-xs font-medium', x.needsReview ? 'bg-warning-50 text-warning-700 ring-1 ring-warning-600/30' : x.correct ? 'bg-success-50 text-success-700' : x.correct === false ? 'bg-danger-50 text-danger-700' : 'bg-surface-muted text-muted')}>{x.n}</a>)}
            </div>
            <div className="space-y-3">
              {r.questions.filter((x) => x.correct === false || x.needsReview).map((x) => (
                <Card key={x.n} id={`q${x.n}`} className="scroll-mt-24 p-4">
                  <div className="flex items-start gap-2">
                    {x.needsReview ? <CircleAlert className="mt-0.5 size-4 shrink-0 text-warning-600" /> : x.correct ? <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-success-600" /> : <XCircle className="mt-0.5 size-4 shrink-0 text-danger-600" />}
                    <p className="flex-1 text-sm font-medium text-ink">Q{x.n} · {x.q?.stem ?? 'Question'}</p>
                    <Badge tone={x.needsReview ? 'warning' : 'danger'}>{x.needsReview ? 'Needs review' : 'Wrong'}</Badge>
                  </div>
                  <div className="mt-3 grid gap-3 text-sm md:grid-cols-2">
                    <div className="rounded-lg bg-surface-muted p-3"><p className="text-xs font-medium uppercase text-muted">Student&apos;s answer</p><p className="mt-1 text-ink">{x.answer ?? '—'}</p></div>
                    <div className="rounded-lg bg-surface-muted p-3"><p className="text-xs font-medium uppercase text-muted">Why it&apos;s wrong · correct approach</p><p className="mt-1 text-ink">{x.why ?? `Correct answer: ${x.q?.answer}`}</p></div>
                  </div>
                  {x.seconds && <p className="mt-2 text-xs text-muted">Time on question: {Math.floor(x.seconds / 60)} m {x.seconds % 60} s</p>}
                </Card>
              ))}
              {r.questions.every((x) => x.correct) && <p className="text-sm text-success-700">Every question correct.</p>}
            </div>
          </>
        )}
      </section>
    </div>
  );
}
