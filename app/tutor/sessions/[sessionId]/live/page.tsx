import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { Mic, MonitorUp, PenLine, PhoneOff, Video } from 'lucide-react';
import { LiveTimer } from '@/components/tutor/live-timer';
import { BackLink, SectionTitle } from '@/components/tutor/bits';
import { sessionContext, sessionPlan, sessionWho } from '@/components/tutor/model';
import { Avatar } from '@/components/ui/avatar';
import { Button, buttonVariants } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Live session · Tutor' };

/**
 * Tutor HTML 5d: video area (a stand-in, no real call in the prototype) plus the prep plan as a checklist and a
 * quick-notes box. "End session" carries the notes into the report so it is half written.
 */
export default async function LivePage({ params }: { params: Promise<{ sessionId: string }> }) {
  const { sessionId } = await params;
  const persona = (await currentPersona())!;
  const ctx = sessionContext(persona.id, sessionId);
  if (!ctx) notFound();
  const { ws, s, learners } = ctx;
  const plan = sessionPlan(ws, s);
  const who = sessionWho(ws, s);

  return (
    <div className="mx-auto max-w-6xl">
      <BackLink href={`/tutor/sessions/${s.id}/prep`}>Back to prep</BackLink>
      <div className="mb-3 flex flex-wrap items-center gap-3 text-sm">
        <span className="inline-flex items-center gap-1.5 rounded-full bg-danger-50 px-2.5 py-1 font-medium text-danger-700"><span className="size-2 rounded-full bg-danger-600" />Live · <LiveTimer /></span>
        <span className="font-medium text-ink">{s.code} · {who}</span>
        <span className="text-muted">Recording on</span>
      </div>
      <form action={`/tutor/sessions/${s.id}/report`} method="get" className="grid gap-4 lg:grid-cols-[1fr_360px]">
        <div className="space-y-3">
          <div className="relative flex aspect-video items-center justify-center overflow-hidden rounded-[var(--radius-card)] bg-ink">
            <div className="flex flex-wrap items-center justify-center gap-6">
              {learners.slice(0, 4).map((l) => {
                const n = ws.students.find((x) => x.learnerId === l)?.name ?? who;
                return <div key={l} className="flex flex-col items-center gap-2 text-white/80"><Avatar name={n} size="lg" /><span className="text-sm">{n.split(' ')[0]}</span></div>;
              })}
            </div>
            <p className="absolute bottom-3 left-3 text-xs text-white/60">Video call stand-in for the demo</p>
          </div>
          <div className="flex flex-wrap justify-center gap-2">
            <Button type="button" variant="secondary"><Mic />Mic</Button>
            <Button type="button" variant="secondary"><Video />Cam</Button>
            <Button type="button" variant="secondary"><MonitorUp />Share screen</Button>
            <Button type="button" variant="secondary"><PenLine />Whiteboard</Button>
            <Button type="submit" variant="danger"><PhoneOff />End session</Button>
          </div>
        </div>
        <Card><CardBody className="space-y-4">
          <section>
            <SectionTitle>Plan</SectionTitle>
            <ul className="space-y-2">
              {plan.map((p, i) => (
                <li key={i}><label className="flex items-start gap-2 text-sm"><input type="checkbox" name="done" value={p.text} className="mt-0.5 size-4 accent-brand-600" /><span><span className="text-ink">{p.kind}: {p.text}</span><span className="block text-xs text-subtle">{p.minutes} min</span></span></label></li>
              ))}
            </ul>
          </section>
          <section>
            <label htmlFor="notes" className="mb-1 block text-sm font-semibold text-ink">Quick notes</label>
            <textarea id="notes" name="notes" rows={5} placeholder="Goes into the report…" className="w-full rounded-lg border border-line bg-surface p-3 text-sm text-ink focus:border-brand-400 focus:outline-none" />
            <p className="mt-1 text-xs text-subtle">Notes and ticked steps carry into the report.</p>
          </section>
          <Link href={`/tutor/students/${s.learnerId}`} className={buttonVariants({ variant: 'ghost', size: 'sm' })}>Student profile</Link>
        </CardBody></Card>
      </form>
    </div>
  );
}
