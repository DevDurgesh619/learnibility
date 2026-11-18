import Link from 'next/link';
import { ArrowRight, ArrowDownRight, ArrowUpRight, CalendarClock, ClipboardCheck, GraduationCap, Lightbulb, Sparkles, Video } from 'lucide-react';
import { Avatar, Badge, Card, CardBody, CardHeader, Progress } from '@/components/ui';
import { cn } from '@/lib/utils';
import { LinkButton } from './link-button';
import type { ApplicationCard, MetricSummary, NextActionView, SessionItem } from './model';

export function SectionTitle({ title, action }: { title: string; action?: React.ReactNode }) {
  return (
    <div className="mb-3 mt-8 flex items-center justify-between gap-3">
      <h2 className="text-base font-semibold text-ink">{title}</h2>
      {action}
    </div>
  );
}

export function TextLink({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <Link href={href} className="inline-flex items-center gap-1 text-sm font-medium text-brand-700 hover:text-brand-800">
      {children}<ArrowRight className="size-3.5" />
    </Link>
  );
}

/** PDF 2a: first-visit hero. */
export function AssessmentHero() {
  return (
    <Card className="mb-6 border-brand-200 bg-brand-50/60">
      <CardBody className="flex flex-col gap-4 sm:flex-row sm:items-center">
        <div className="flex size-11 shrink-0 items-center justify-center rounded-xl bg-brand-600 text-white"><ClipboardCheck className="size-5" /></div>
        <div className="min-w-0 flex-1">
          <h2 className="text-base font-semibold text-ink">Take your free assessment</h2>
          <p className="text-sm text-muted">3 short tests · about 20 minutes each · unlocks your gap analysis and a smarter timetable.</p>
        </div>
        <LinkButton href="/student/assessments">Start</LinkButton>
      </CardBody>
    </Card>
  );
}

/** Next best action with its reason (blueprint daily loop; engine `nextBestAction`). */
export function NextActionCard({ actions }: { actions: NextActionView[] }) {
  const [top, ...rest] = actions;
  if (!top) return null;
  return (
    <Card className="mb-6 overflow-hidden">
      <div className="flex flex-col gap-4 bg-gradient-to-r from-brand-600 to-brand-500 p-5 text-white sm:flex-row sm:items-center">
        <div className="flex size-10 shrink-0 items-center justify-center rounded-xl bg-white/15"><Sparkles className="size-5" /></div>
        <div className="min-w-0 flex-1">
          <p className="text-xs font-medium uppercase tracking-wide text-white/80">Your next best step</p>
          <p className="text-base font-semibold">{top.title}</p>
          <p className="text-sm text-white/85">{top.reason}</p>
        </div>
        {top.href && <LinkButton href={top.href} variant="secondary" className="border-white/0">{top.cta}</LinkButton>}
      </div>
      {rest.length > 0 && (
        <ul className="divide-y divide-line">
          {rest.map((a, i) => (
            <li key={`${a.kind}-${i}`} className="flex items-center gap-3 px-5 py-3 text-sm">
              <Lightbulb className="size-4 shrink-0 text-subtle" />
              <span className="min-w-0 flex-1"><span className="font-medium text-ink">{a.title}</span> <span className="text-muted">· {a.reason}</span></span>
              {a.href && <Link href={a.href} className="shrink-0 text-sm font-medium text-brand-700 hover:text-brand-800">{a.cta}</Link>}
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
}

export function SessionsCard({ sessions, joinStates, whenLabels }: { sessions: SessionItem[]; joinStates: Record<string, 'open' | 'soon' | 'ended'>; whenLabels: Record<string, string> }) {
  return (
    <Card className="h-full">
      <CardHeader title="Sessions" action={<TextLink href="/student/sessions">All</TextLink>} />
      <CardBody className="pt-3">
        {sessions.length === 0 ? (
          <div className="rounded-lg border border-dashed border-line p-4 text-sm text-muted">
            <p>No sessions yet.</p>
            <Link href="/student/tutors" className="font-medium text-brand-700 hover:text-brand-800">Book a free demo with a tutor</Link>
          </div>
        ) : (
          <ul className="divide-y divide-line">
            {sessions.map((s) => (
              <li key={s.id} className="flex items-center gap-3 py-2.5">
                <Avatar name={s.personName} size="sm" photo />
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-medium text-ink">{s.personName.split(' ')[0]} · {s.roleLabel}</p>
                  <p className="text-xs text-muted">{whenLabels[s.id]}</p>
                </div>
                {joinStates[s.id] === 'open'
                  ? <LinkButton href={`/student/sessions/${s.personId}`} size="sm">Join</LinkButton>
                  : <Video className="size-4 text-subtle" aria-hidden />}
              </li>
            ))}
          </ul>
        )}
      </CardBody>
    </Card>
  );
}

const pct = (v: number) => `${Math.round(v * 100)}%`;

/** PDF 2b: four metric cards that click through to 2d. 2a shows dashed cards with a reason instead of zeros. */
/** Tiny trend line for a metric card (plain SVG, so it renders on the server). */
function Sparkline({ values, up }: { values: (number | null)[]; up: boolean }) {
  const pts = values.map((v, i) => [i, v] as const).filter((p): p is readonly [number, number] => p[1] !== null);
  if (pts.length < 2) return null;
  const w = 96, h = 28, n = values.length - 1;
  const lo = Math.min(...pts.map((p) => p[1])), hi = Math.max(...pts.map((p) => p[1]));
  const y = (v: number) => (hi === lo ? h / 2 : h - 3 - ((v - lo) / (hi - lo)) * (h - 6));
  const d = pts.map(([i, v], k) => `${k ? 'L' : 'M'}${((i / n) * w).toFixed(1)},${y(v).toFixed(1)}`).join(' ');
  const [li, lv] = pts[pts.length - 1]!;
  const color = up ? 'var(--color-success-600)' : 'var(--color-brand-500)';
  return (
    <svg viewBox={`0 0 ${w} ${h}`} className="h-7 w-24 overflow-visible" aria-hidden>
      <path d={d} fill="none" stroke={color} strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx={(li / n) * w} cy={y(lv)} r="2.5" fill={color} />
    </svg>
  );
}

export function MetricCards({ metrics, sparks = {} }: { metrics: MetricSummary[]; sparks?: Record<string, (number | null)[]> }) {
  return (
    <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
      {metrics.map((m) => m.value === null ? (
        <div key={m.key} className="rounded-[var(--radius-card)] border border-dashed border-line bg-surface p-4">
          <p className="text-sm text-muted">{m.label}</p>
          <p className="mt-1 text-2xl font-semibold text-subtle">—</p>
          <p className="mt-1 text-xs text-subtle">{m.emptyReason}</p>
        </div>
      ) : (
        <Link key={m.key} href={`/student?metric=${m.key}`} className="group">
          <Card className="h-full p-4 transition-colors group-hover:border-brand-300">
            <p className="text-sm text-muted">{m.label}</p>
            <div className="mt-1 flex items-end justify-between gap-2">
            <div className="flex items-baseline gap-2">
              <span className="text-2xl font-semibold tracking-tight text-ink">{pct(m.value)}</span>
              {m.delta !== null && m.delta !== 0 && (
                <span className={cn('inline-flex items-center text-xs font-medium', m.delta > 0 ? 'text-success-700' : 'text-danger-700')}>
                  {m.delta > 0 ? <ArrowUpRight className="size-3.5" /> : <ArrowDownRight className="size-3.5" />}
                  {Math.abs(Math.round(m.delta * 100))}
                </span>
              )}
            </div>
            {sparks[m.key] && <Sparkline values={sparks[m.key]!} up={(m.delta ?? 0) >= 0} />}
            </div>
            <p className="mt-1 text-xs text-subtle">vs last week · tap for the graph</p>
          </Card>
        </Link>
      ))}
    </div>
  );
}

/** PDF 2b: soft upsell for free users. */
export function ApplicationUpsell() {
  return (
    <div className="mt-6 flex flex-col gap-3 rounded-[var(--radius-card)] border border-dashed border-brand-300 bg-surface p-4 sm:flex-row sm:items-center">
      <GraduationCap className="size-5 shrink-0 text-brand-600" />
      <p className="flex-1 text-sm text-muted"><span className="font-semibold text-ink">Applying abroad?</span> Track deadlines, essays and visa in one place with Application Support.</p>
      <LinkButton href="/student/universities" variant="secondary" size="sm">See how it works</LinkButton>
    </div>
  );
}

/** PDF 2c: application cards above the metrics for subscribers. */
export function ApplicationCards({ apps, deadlineLabels }: { apps: ApplicationCard[]; deadlineLabels: Record<string, string> }) {
  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
      {apps.map((a) => (
        <Link key={a.id} href="/student/applications" className="group">
          <Card className={cn('h-full p-4 transition-colors group-hover:border-brand-300', a.atRisk && 'border-danger-600/40')}>
            <div className="flex items-start justify-between gap-2">
              <p className="text-sm font-semibold text-ink">{a.title}</p>
              {a.intake && <Badge tone="neutral">{a.intake}</Badge>}
            </div>
            <div className="mt-3 flex items-center gap-2"><Progress value={a.progress} tone={a.atRisk ? 'danger' : 'brand'} /><span className="text-xs text-muted">{pct(a.progress)}</span></div>
            <p className={cn('mt-2 flex items-center gap-1 text-xs', a.atRisk ? 'font-medium text-danger-700' : 'text-muted')}>
              <CalendarClock className="size-3.5" />{deadlineLabels[a.id]} · {a.note}
            </p>
          </Card>
        </Link>
      ))}
    </div>
  );
}
