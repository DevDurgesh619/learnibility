import type { Metadata } from 'next';
import Link from 'next/link';
import { ArrowRight, CalendarCheck2, ClipboardCheck, GraduationCap, Target, Users } from 'lucide-react';
import { Logo } from '@/components/shell/logo';
import { buttonVariants } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export const metadata: Metadata = { title: 'Learnibility · Plan your studies, tests and applications in one place' };

const FEATURES = [
  { icon: ClipboardCheck, title: 'Find the exact gap', body: 'A 40-minute starting test and short chapter checks show which subtopic is stuck and why: a missing basic, a concept, steps, speed or confidence.' },
  { icon: CalendarCheck2, title: 'A week built around it', body: 'Your timetable re-plans after every test and every missed task, with spaced reviews so what you learn stays learnt.' },
  { icon: Users, title: 'The right help', body: 'Free resources first. Tutors matched to your gaps, style, budget and free slots when you need more.' },
  { icon: GraduationCap, title: 'Careers and universities', body: 'Careers that fit you, the skills to get there, and reach, target and safe universities with deadlines.' },
];

const STEPS = ['Sign up with your mobile', 'Tell us about you (2 minutes)', 'Take the starting test', 'Get your plan, today'];

/** PDF 1a: landing. Every call to action goes to 1b. */
export default function WelcomePage() {
  return (
    <div className="min-h-screen bg-surface">
      <header className="mx-auto flex max-w-6xl items-center justify-between gap-4 p-4 sm:p-6">
        <Logo href="/welcome" />
        <nav className="flex items-center gap-1 text-sm sm:gap-4">
          <a href="#how" className="hidden px-2 text-muted hover:text-ink sm:inline">How it works</a>
          <a href="#features" className="hidden px-2 text-muted hover:text-ink sm:inline">Solutions</a>
          <Link href="/signup" className={buttonVariants({ variant: 'secondary', size: 'sm' })}>Log in</Link>
        </nav>
      </header>

      <section className="mx-auto grid max-w-6xl items-center gap-10 px-4 pb-16 pt-8 sm:px-6 lg:grid-cols-2 lg:pt-16">
        <div>
          <Badge tone="brand">Grades 8 to 12 · CBSE · Cambridge · IB</Badge>
          <h1 className="mt-4 text-4xl font-semibold tracking-tight text-ink sm:text-5xl">Plan your studies, tests and university applications in one place.</h1>
          <p className="mt-4 text-lg text-muted">
            Tutors, counsellors, an AI timetable, gap analysis and application support for students in class 8 to 12, all working from one record of how you learn.
          </p>
          <div className="mt-8 flex flex-wrap items-center gap-3">
            <Link href="/signup" className={buttonVariants({ size: 'lg' })}>
              Get started, it&apos;s free <ArrowRight />
            </Link>
            <Link href="/login" className={buttonVariants({ variant: 'ghost', size: 'lg' })}>Explore the demo personas</Link>
          </div>
          <p className="mt-3 text-xs text-subtle">No card needed. Free plan includes the starting test, chapter checks and your timetable.</p>
        </div>

        {/* Product preview */}
        <Card className="overflow-hidden p-0">
          <div className="flex items-center gap-1.5 border-b border-line bg-surface-muted px-4 py-2">
            <span className="size-2.5 rounded-full bg-danger-600/60" />
            <span className="size-2.5 rounded-full bg-warning-600/60" />
            <span className="size-2.5 rounded-full bg-success-600/60" />
          </div>
          <div className="grid gap-3 p-5">
            <div className="flex items-center justify-between">
              <p className="text-sm font-semibold">Gap analysis · Maths, chapter check</p>
              <Badge tone="info">27/40 · Average</Badge>
            </div>
            {[
              { t: 'Linear equations', p: 90, tone: 'bg-success-600' },
              { t: 'Number systems', p: 88, tone: 'bg-success-600' },
              { t: 'Algebraic identities', p: 58, tone: 'bg-warning-600' },
              { t: 'Triangles', p: 40, tone: 'bg-danger-600' },
            ].map((r) => (
              <div key={r.t} className="grid grid-cols-[140px_1fr_40px] items-center gap-3 text-sm">
                <span className="truncate text-muted">{r.t}</span>
                <span className="h-2 overflow-hidden rounded-full bg-surface-muted"><span className={`block h-full ${r.tone}`} style={{ width: `${r.p}%` }} /></span>
                <span className="text-right tabular-nums text-ink">{r.p}%</span>
              </div>
            ))}
            <div className="mt-1 rounded-lg border border-brand-200 bg-brand-50 p-3 text-sm">
              <p className="flex items-center gap-1.5 font-medium text-brand-700"><Target className="size-4" /> Focus first: Triangles</p>
              <p className="mt-1 text-muted">Concept gap. 3.6 hours to close, planned as 30-minute blocks this week.</p>
            </div>
          </div>
        </Card>
      </section>

      <section id="features" className="border-t border-line bg-canvas">
        <div className="mx-auto grid max-w-6xl gap-4 px-4 py-14 sm:grid-cols-2 sm:px-6 lg:grid-cols-4">
          {FEATURES.map((f) => (
            <Card key={f.title} className="p-5">
              <f.icon className="size-6 text-brand-600" />
              <h2 className="mt-3 font-semibold text-ink">{f.title}</h2>
              <p className="mt-1 text-sm text-muted">{f.body}</p>
            </Card>
          ))}
        </div>
      </section>

      <section id="how" className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
        <h2 className="text-2xl font-semibold tracking-tight">How it works</h2>
        <ol className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {STEPS.map((s, i) => (
            <li key={s} className="flex items-center gap-3 rounded-xl border border-line p-4">
              <span className="flex size-8 shrink-0 items-center justify-center rounded-full bg-brand-600 text-sm font-semibold text-white">{i + 1}</span>
              <span className="text-sm font-medium text-ink">{s}</span>
            </li>
          ))}
        </ol>
        <div className="mt-10 flex justify-center">
          <Link href="/signup" className={buttonVariants({ size: 'lg' })}>Get started, it&apos;s free <ArrowRight /></Link>
        </div>
      </section>

      <footer className="border-t border-line py-6 text-center text-xs text-subtle">Demo product. All people and data are fictional.</footer>
    </div>
  );
}
