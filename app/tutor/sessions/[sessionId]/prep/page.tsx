import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { BookOpen, CheckCircle2, FileText, PlayCircle, Sparkles } from 'lucide-react';
import { SessionHeader } from '@/components/tutor/session-header';
import { Delta, SectionTitle } from '@/components/tutor/bits';
import { aiFocus, openGapsFor, sessionContext, sessionPlan } from '@/components/tutor/model';
import { formatDay, formatTime } from '@/components/marketplace/dates';
import { Button, buttonVariants } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { GapBadge } from '@/components/ui/badge';
import { savePrep } from '@/lib/actions/tutor';
import { namesFor } from '@/lib/data';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Session prep · Tutor' };

/** Tutor HTML 5c: AI briefing. Last session, recent assessment, previous homework, a timed plan and resources. */
export default async function PrepPage({ params, searchParams }: { params: Promise<{ sessionId: string }>; searchParams: Promise<{ saved?: string }> }) {
  const [{ sessionId }, sp] = await Promise.all([params, searchParams]);
  const persona = (await currentPersona())!;
  const ctx = sessionContext(persona.id, sessionId);
  if (!ctx) notFound();
  const { ws, s, lid, prev, prevHomework, latest, latestDelta, lastNote, booking } = ctx;
  const focus = aiFocus(ws, s);
  const plan = sessionPlan(ws, s);
  const planText = s.prepNotes ?? plan.map((p) => `${p.minutes} min ${p.kind}: ${p.text}`).join('\n');
  const gaps = openGapsFor(lid, s.subjectId ? [s.subjectId] : []).sort((a, b) => b.hoursToClose - a.hoursToClose).slice(0, 3);
  const names = namesFor([...new Set(gaps.map((g) => g.subjectId))]);
  const doneHw = prevHomework.filter((t) => t.status === 'done').length;
  const snap = booking?.sharedGapSnapshot;
  const resources = [
    { icon: FileText, label: `${focus.line.split(':')[0]} problem set`, by: 'yours' },
    { icon: PlayCircle, label: `${focus.line.split(':')[0]} explainer video`, by: 'library' },
    { icon: BookOpen, label: '5 past exam questions on this topic', by: 'question bank' },
  ];

  return (
    <div className="mx-auto max-w-4xl">
      <SessionHeader ws={ws} s={s} title="Session briefing" actions={<Link href={`/tutor/sessions/${s.id}/live`} className={buttonVariants()}>Join at {formatTime(new Date(Date.parse(s.startUtc) - 10 * 60_000).toISOString())}</Link>} />
      {sp.saved && <p className="mb-4 flex items-center gap-2 rounded-lg bg-success-50 px-3 py-2 text-sm text-success-700"><CheckCircle2 className="size-4" />Plan saved. It carries into the live view and the report.</p>}

      <Card className="mb-4 border-brand-200 bg-brand-50/40"><CardBody className="flex items-start gap-3">
        <Sparkles className="mt-0.5 size-5 shrink-0 text-brand-600" />
        <div><p className="text-sm text-muted">Focus for today</p><p className="text-lg font-medium text-ink">{focus.line}</p><p className="text-xs text-subtle">{focus.source}</p></div>
      </CardBody></Card>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <Card><CardBody>
          <SectionTitle>Last session{prev ? ` · ${prev.code ?? ''} ${formatDay(prev.startUtc)}` : ''}</SectionTitle>
          {prev?.report ? (
            <div className="space-y-1 text-sm">
              <p className="text-ink">Covered: {prev.report.topics.join(', ')}</p>
              <p className="text-muted">How it went: {prev.report.performance.replace('_', ' ')} · engagement {prev.report.engagement}</p>
              {lastNote && <p className="text-muted">Your note: “{lastNote.text.length > 120 ? lastNote.text.slice(0, 117) + '…' : lastNote.text}”</p>}
            </div>
          ) : snap ? (
            <div className="space-y-2 text-sm">
              <p className="text-muted">First session. {ws.students.find((x) => x.learnerId === lid)?.name.split(' ')[0] ?? 'The student'} shared a gap snapshot{snap.score !== undefined ? ` (latest score ${snap.score}/100)` : ''}:</p>
              <ul className="space-y-1">{snap.gaps.slice(0, 3).map((g) => <li key={g.subtopicId} className="flex items-center gap-2"><GapBadge code={g.code as never} /><span className="text-ink">{g.name}</span></li>)}</ul>
            </div>
          ) : <p className="text-sm text-muted">No earlier session with this student yet.{booking?.topic ? ` They asked about: “${booking.topic}”.` : ''}</p>}
        </CardBody></Card>

        <Card><CardBody>
          <SectionTitle>Recent assessment</SectionTitle>
          {latest ? (
            <div className="space-y-1 text-sm">
              <p className="flex items-center gap-2 text-ink">{latest.title} · {latest.pct}% <Delta value={latestDelta} /></p>
              <p className="text-xs text-subtle">{formatDay(latest.date)} · {latest.source === 'assignment' ? 'your assignment' : 'platform assessment'}</p>
              {gaps.length > 0 && <p className="text-muted">Open gaps: {gaps.map((g) => names[g.subtopicId] ?? g.subtopicId).join(', ')}</p>}
            </div>
          ) : <p className="text-sm text-muted">No scored work in this subject yet.</p>}
        </CardBody></Card>

        <Card><CardBody>
          <SectionTitle>Previous homework</SectionTitle>
          {prevHomework.length ? (
            <>
              <p className="mb-2 text-sm text-ink">{doneHw} / {prevHomework.length} completed</p>
              <ul className="space-y-1 text-sm">{prevHomework.map((t) => <li key={t.id} className="flex justify-between gap-2"><span className="truncate text-ink">{t.title}</span><span className={t.status === 'done' ? 'text-success-700' : 'text-warning-700'}>{t.status === 'done' ? 'done' : 'open'}</span></li>)}</ul>
            </>
          ) : <p className="text-sm text-muted">No homework from the last session.</p>}
        </CardBody></Card>

        <Card><CardBody>
          <SectionTitle>Suggested resources · {resources.length}</SectionTitle>
          <ul className="space-y-2 text-sm">{resources.map((r) => <li key={r.label} className="flex items-center gap-2"><r.icon className="size-4 text-muted" /><span className="text-ink">{r.label}</span><span className="text-xs text-subtle">· {r.by}</span></li>)}</ul>
        </CardBody></Card>
      </div>

      <Card className="mt-4"><CardBody>
        <SectionTitle>Today&apos;s recommended session</SectionTitle>
        <ol className="mb-4 space-y-2">
          {plan.map((p, i) => (
            <li key={i} className="flex gap-3 text-sm"><span className="w-14 shrink-0 font-medium text-ink">{p.minutes} min</span><span className="w-16 shrink-0 text-muted">{p.kind}</span><span className="text-ink">{p.text}</span></li>
          ))}
        </ol>
        <form action={savePrep} className="space-y-3">
          <input type="hidden" name="sessionId" value={s.id} />
          <label className="block text-sm font-medium text-ink" htmlFor="plan">Edit plan or start from blank</label>
          <textarea id="plan" name="plan" rows={5} defaultValue={planText} className="w-full rounded-lg border border-line bg-surface p-3 text-sm text-ink focus:border-brand-400 focus:outline-none" />
          <div className="flex justify-end"><Button type="submit">Save plan</Button></div>
        </form>
      </CardBody></Card>
    </div>
  );
}
