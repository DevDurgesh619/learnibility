import { notFound } from 'next/navigation';
import { CheckCircle2, CircleAlert, Sparkles } from 'lucide-react';
import { AssignmentStatus, BackLink } from '@/components/tutor/bits';
import { questionsOf, studentContext, type TutorAssignment } from '@/components/tutor/model';
import { formatDay } from '@/components/marketplace/dates';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { saveEvaluation } from '@/lib/actions/tutor';
import { currentPersona } from '@/lib/session';
import { cn } from '@/lib/utils';

/** 4h Evaluate: auto-checked objective items, AI-scored written answers, tutor override, then publish. */
export default async function Evaluate({ params }: { params: Promise<{ learnerId: string; assignmentId: string }> }) {
  const { learnerId, assignmentId } = await params;
  const { ws, row } = studentContext((await currentPersona())!.id, learnerId)!;
  const a = ws.assignments.find((x) => x.id === assignmentId && x.learnerId === learnerId) as TutorAssignment | undefined;
  if (!a) notFound();
  const qs = questionsOf(a);
  const per = new Map((a.perQuestion ?? []).map((p) => [p.questionId, p]));
  const written = qs.filter((q) => per.get(q.id)?.aiFeedback !== undefined && ['explain', 'short', 'long'].includes(q.type));
  const objective = qs.filter((q) => !written.includes(q));
  const waiting = qs.filter((q) => per.get(q.id)?.needsReview && per.get(q.id)?.tutorScore === undefined);
  const submitted = !!a.perQuestion;
  const max = qs.reduce((t, q) => t + q.marks, 0);
  const provisional = qs.reduce((t, q) => { const p = per.get(q.id); return t + (p?.tutorScore ?? p?.aiScore ?? (p?.correct ? q.marks : 0)); }, 0);
  return (
    <div className="space-y-6">
      <BackLink href={`/tutor/students/${learnerId}/assignments`}>Assignments · {row.name.split(' ')[0]} · {a.title}</BackLink>
      {!submitted ? (
        <Card><CardBody className="space-y-2">
          <div className="flex items-center gap-2"><h2 className="text-lg font-semibold text-ink">{a.title}</h2><AssignmentStatus status={a.status} /></div>
          <p className="text-sm text-muted">{qs.length} questions · due {formatDay(a.dueOn)}. Not submitted yet; it appears in your review queue when {row.name.split(' ')[0]} submits.</p>
          <ol className="mt-3 list-decimal space-y-1 pl-5 text-sm text-ink">{qs.map((q) => <li key={q.id}>{q.stem}</li>)}</ol>
        </CardBody></Card>
      ) : (
        <form action={saveEvaluation} className="space-y-6">
          <input type="hidden" name="learnerId" value={learnerId} />
          <input type="hidden" name="assignmentId" value={a.id} />
          <Card><CardBody className="grid gap-6 md:grid-cols-[160px_1fr_auto] md:items-center">
            <div className="text-center"><p className="text-4xl font-semibold text-ink">{Math.round((provisional / Math.max(1, max)) * 100)}%</p><p className="text-xs text-muted">{a.status === 'completed' ? 'published' : 'provisional'} · {provisional}/{max}</p></div>
            <ul className="space-y-1 text-sm">
              <li className="flex items-center gap-1.5 text-success-700"><CheckCircle2 className="size-4" />{objective.length} objective questions auto-checked</li>
              <li className="flex items-center gap-1.5 text-success-700"><CheckCircle2 className="size-4" />AI evaluation complete for {written.length} written {written.length === 1 ? 'answer' : 'answers'}</li>
              {waiting.length > 0 ? <li className="flex items-center gap-1.5 text-warning-700"><CircleAlert className="size-4" />{waiting.length} {waiting.length === 1 ? 'answer needs' : 'answers need'} your review</li> : <li className="text-muted">Nothing left to review</li>}
            </ul>
            <div className="flex flex-col gap-2">
              <Button name="intent" value="save" variant="secondary">Save</Button>
              <Button name="intent" value="publish">Publish result</Button>
            </div>
          </CardBody></Card>

          <div className="flex flex-wrap gap-1.5">
            {qs.map((q, i) => { const p = per.get(q.id); return <a key={q.id} href={`#e${i + 1}`} className={cn('flex size-8 items-center justify-center rounded-md text-xs font-medium', p?.needsReview ? 'bg-warning-50 text-warning-700 ring-1 ring-warning-600/30' : p?.correct ? 'bg-success-50 text-success-700' : p?.correct === false ? 'bg-danger-50 text-danger-700' : 'bg-brand-50 text-brand-700')}>{i + 1}</a>; })}
          </div>

          {written.map((q) => {
            const p = per.get(q.id)!;
            const n = qs.indexOf(q) + 1;
            return (
              <Card key={q.id} id={`e${n}`} className="scroll-mt-24">
                <CardBody className="space-y-3">
                  <div className="flex items-start gap-2"><p className="flex-1 text-sm font-semibold text-ink">Q{n} · {q.stem}</p>{p.needsReview && <Badge tone="warning">Needs review</Badge>}</div>
                  <div className="rounded-lg bg-surface-muted p-3 text-sm"><p className="text-xs font-medium uppercase text-muted">Student answer</p><p className="mt-1 text-ink">{p.answer}</p></div>
                  <div className="rounded-lg border border-brand-200 bg-brand-50/50 p-3 text-sm"><p className="flex items-center gap-1 text-xs font-medium uppercase text-brand-700"><Sparkles className="size-3.5" />AI evaluation · {p.aiScore}/{q.marks}</p><p className="mt-1 text-ink">{p.aiFeedback}</p>{q.markingKey && <p className="mt-1 text-xs text-muted">Rubric: {q.markingKey}</p>}</div>
                  <div className="grid gap-3 sm:grid-cols-[140px_1fr]">
                    <label className="text-sm"><span className="text-xs font-medium uppercase text-muted">Your score</span><span className="mt-1 flex items-center gap-1"><input name={`score_${q.id}`} type="number" min={0} max={q.marks} step={0.5} defaultValue={p.tutorScore ?? p.aiScore} className="h-9 w-20 rounded-lg border border-line px-2" /> / {q.marks}</span></label>
                    <label className="text-sm"><span className="text-xs font-medium uppercase text-muted">Feedback to {row.name.split(' ')[0]} (suggested; edit or write your own)</span>
                      <textarea name={`fb_${q.id}`} rows={2} defaultValue={p.tutorFeedback ?? (p.aiScore !== undefined && p.aiScore >= q.marks * 0.8 ? 'Good answer. ' : 'Good start. ') + (p.aiFeedback ?? '')} className="mt-1 w-full rounded-lg border border-line p-2" /></label>
                  </div>
                </CardBody>
              </Card>
            );
          })}

          <Card><CardBody className="space-y-2">
            <p className="text-sm font-semibold text-ink">Objective answers</p>
            <ul className="divide-y divide-line text-sm">
              {objective.map((q) => { const p = per.get(q.id); return (
                <li key={q.id} id={`e${qs.indexOf(q) + 1}`} className="flex items-start gap-2 py-2">
                  {p?.correct ? <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-success-600" /> : <CircleAlert className="mt-0.5 size-4 shrink-0 text-danger-600" />}
                  <span className="flex-1"><span className="text-ink">Q{qs.indexOf(q) + 1}. {q.stem}</span>{!p?.correct && <span className="block text-xs text-muted">Answered {p?.answer ?? '—'} · correct {q.answer}{p?.aiFeedback ? ` · ${p.aiFeedback}` : ''}</span>}</span>
                </li>
              ); })}
            </ul>
          </CardBody></Card>

          {a.feedback && (
            <Card><CardBody className="space-y-3">
              <p className="text-sm font-semibold text-ink">Overall gap analysis <span className="font-normal text-muted">(AI draft, editable before publishing)</span></p>
              <label className="block text-sm"><span className="text-xs font-medium uppercase text-success-700">Strength</span><textarea name="strength" rows={2} defaultValue={a.feedback.strength} className="mt-1 w-full rounded-lg border border-line p-2" /></label>
              <label className="block text-sm"><span className="text-xs font-medium uppercase text-danger-700">Weakness</span><textarea name="weakness" rows={2} defaultValue={a.feedback.weakness} className="mt-1 w-full rounded-lg border border-line p-2" /></label>
            </CardBody></Card>
          )}
        </form>
      )}
    </div>
  );
}
