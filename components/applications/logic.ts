/**
 * Pure application-support rules: days left, risk flags, pre-submission QA, progress and next step.
 * No data access here; callers pass records from lib/data and DEMO_NOW.
 */
import type { Application, ApplicationStatus, Essay } from '@/lib/data/types';

export const STATUS_ORDER: ApplicationStatus[] = ['shortlisted', 'collecting_documents', 'in_review', 'submitted', 'decision'];

export const STATUS_LABEL: Record<ApplicationStatus, string> = {
  shortlisted: 'Shortlisted',
  collecting_documents: 'Collecting documents',
  in_review: 'In review',
  submitted: 'Submitted',
  decision: 'Decision',
};

export const DECISION_LABEL: Record<NonNullable<Application['decision']>, string> = {
  offer: 'Unconditional offer', conditional_offer: 'Conditional offer', rejected: 'Not successful', waitlisted: 'Waitlisted',
};

/** Whole days from the local date of `now` (IST) to a YYYY-MM-DD date. */
export function daysUntil(date: string, now: Date): number {
  const ist = new Date(now.getTime() + 330 * 60_000).toISOString().slice(0, 10);
  return Math.round((Date.parse(`${date}T00:00:00Z`) - Date.parse(`${ist}T00:00:00Z`)) / 86_400_000);
}

export function wordCount(text: string): number {
  return (text.trim().match(/\S+/g) ?? []).length;
}

export const latestVersion = (e: Essay) => e.versions.reduce((a, b) => (b.version > a.version ? b : a), e.versions[0] ?? { version: 0, text: '', createdAt: '' });

export function openItems(app: Application) {
  return {
    checklist: app.checklist.filter((c) => !c.done),
    recommenders: app.recommenders.filter((r) => r.status !== 'submitted'),
    essays: app.essays.filter((e) => e.status !== 'final'),
  };
}

export function openCount(app: Application) {
  const o = openItems(app);
  // Essay and recommendation checklist items mirror the essays and recommenders, so count only the checklist.
  return o.checklist.length;
}

/** Share of the checklist done, 0..1. Submitted and decided applications are complete. */
export function progress(app: Application): number {
  if (app.status === 'submitted' || app.status === 'decision') return 1;
  if (!app.checklist.length) return app.status === 'shortlisted' ? 0.05 : 0;
  return app.checklist.filter((c) => c.done).length / app.checklist.length;
}

export interface RiskFlagView {
  severity: 'high' | 'medium' | 'low';
  text: string;
}

/**
 * Risk flags, as the brief defines them: deadline under 14 days with open items is high.
 * Also: recommender past their due date, essay over its word limit, deadline passed and not submitted.
 */
export function riskFlags(app: Application, now: Date): RiskFlagView[] {
  if (app.status === 'submitted' || app.status === 'decision') return [];
  const out: RiskFlagView[] = [];
  const days = daysUntil(app.deadline, now);
  const open = openCount(app);
  if (days < 0) out.push({ severity: 'high', text: `Deadline passed ${-days} day${days === -1 ? '' : 's'} ago and not submitted` });
  else if (days < 14 && open > 0) out.push({ severity: 'high', text: `Deadline in ${days} day${days === 1 ? '' : 's'} with ${open} open item${open === 1 ? '' : 's'}` });
  else if (days < 30 && open > 2) out.push({ severity: 'medium', text: `${days} days left and ${open} items still open` });
  for (const r of app.recommenders) {
    if (r.status !== 'submitted' && daysUntil(r.dueOn, now) < 0) out.push({ severity: 'medium', text: `${r.name}'s letter was due ${fmtDate(r.dueOn)}` });
  }
  for (const e of app.essays) {
    const words = wordCount(latestVersion(e).text);
    if (e.wordLimit && words > e.wordLimit) out.push({ severity: 'medium', text: `Essay is ${words - e.wordLimit} words over the ${e.wordLimit}-word limit` });
  }
  return out;
}

export interface QaItem {
  id: string;
  label: string;
  ok: boolean;
  detail?: string;
}

/** Pre-submission QA check: every item must pass before "Mark as submitted" is enabled. */
export function qaCheck(app: Application, now: Date): QaItem[] {
  const o = openItems(app);
  const days = daysUntil(app.deadline, now);
  const items: QaItem[] = [
    { id: 'deadline', label: 'Deadline not passed', ok: days >= 0, detail: days >= 0 ? `${days} days left (${fmtDate(app.deadline)})` : `Passed on ${fmtDate(app.deadline)}` },
    {
      id: 'checklist', label: 'All documents and forms ticked off', ok: o.checklist.length === 0,
      detail: o.checklist.length ? `Open: ${o.checklist.map((c) => c.title).join(', ')}` : `${app.checklist.length} of ${app.checklist.length} done`,
    },
    {
      id: 'essays', label: 'Essays approved by your counsellor', ok: o.essays.length === 0,
      detail: o.essays.length ? `${o.essays.length} essay${o.essays.length === 1 ? '' : 's'} not final yet` : app.essays.length ? 'All essays final' : 'No essays needed',
    },
    ...app.essays.map((e) => {
      const w = wordCount(latestVersion(e).text);
      return { id: `limit-${e.id}`, label: `Word limit: ${shortPrompt(e.prompt)}`, ok: !e.wordLimit || w <= e.wordLimit, detail: `${w} / ${e.wordLimit} words` };
    }),
    {
      id: 'recs', label: 'Recommendation letters submitted', ok: o.recommenders.length === 0,
      detail: o.recommenders.length ? `Waiting on ${o.recommenders.map((r) => r.name).join(', ')}` : app.recommenders.length ? `${app.recommenders.length} received` : 'None needed',
    },
    {
      id: 'comments', label: 'No unresolved comments on the final draft', ok: app.essays.every((e) => e.comments.filter((c) => !c.resolved && !c.parentId && c.version === latestVersion(e).version).length === 0),
    },
  ];
  return items;
}

export const qaPassed = (app: Application, now: Date) => qaCheck(app, now).every((i) => i.ok);

/** Next step line shown on overview cards (PDF 7a "Next: SOP draft -> Heena review"). */
export function nextStep(app: Application, counsellorFirstName = 'your counsellor'): string {
  if (app.status === 'decision') return app.decision ? DECISION_LABEL[app.decision] : 'Decision received';
  if (app.status === 'submitted') return 'Submitted. Waiting for the decision';
  const inReview = app.essays.find((e) => e.status === 'in_review');
  if (inReview) return `${shortPrompt(inReview.prompt)} with ${counsellorFirstName} for review`;
  const drafting = app.essays.find((e) => e.status === 'drafting');
  if (drafting) return `Finish ${shortPrompt(drafting.prompt).toLowerCase()} draft`;
  const item = app.checklist.find((c) => !c.done);
  if (item) return item.title;
  const rec = app.recommenders.find((r) => r.status !== 'submitted');
  if (rec) return `Waiting on ${rec.name}'s letter`;
  if (app.status === 'shortlisted') return 'Start collecting documents';
  return 'Run the QA check and submit';
}

export function shortPrompt(prompt: string): string {
  const head = prompt.split(/[:.(]/)[0]!.trim();
  return head.length > 48 ? `${head.slice(0, 45)}…` : head;
}

// Hand-formatted so server and browser agree (ICU data differs, e.g. "Sep" vs "Sept").
const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
/** Date-only strings are calendar dates; timestamps are shown on the IST calendar. */
const cal = (d: string) => (d.length === 10 ? new Date(`${d}T00:00:00Z`) : new Date(Date.parse(d) + 330 * 60_000));
export const fmtShort = (d: string) => { const x = cal(d); return `${x.getUTCDate()} ${MON[x.getUTCMonth()]}`; };
export const fmtDate = (d: string) => `${fmtShort(d)} ${cal(d).getUTCFullYear()}`;

export function daysLeftLabel(days: number): string {
  if (days < 0) return `${-days} days overdue`;
  if (days === 0) return 'Due today';
  return `${days} day${days === 1 ? '' : 's'} left`;
}
