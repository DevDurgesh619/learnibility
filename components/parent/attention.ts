import 'server-only';
import { getApplications, getBookings, getCurrentPlan, getInvoices, demoToday, type Booking, type ChildSummary } from '@/lib/data';
import { daysBetween, fmtDate } from './format';

export interface AttentionItem {
  id: string;
  learnerId: string;
  tone: 'danger' | 'warning' | 'brand';
  title: string;
  detail: string;
  href: string;
  cta: string;
}

/** Paid-tutor decisions waiting on this parent: student bookings pending approval, or the 3-week rule firing. */
export function paidTutorDecision(learnerId: string): { pending: Booking[]; ruleFired: boolean; reason: string; approved: Booking[] } {
  const bookings = getBookings(learnerId).filter((b) => b.priceInr > 0 && b.kind === 'regular');
  const pending = bookings.filter((b) => b.parentApproval?.status === 'pending' && b.status !== 'cancelled' && b.status !== 'declined');
  const approved = bookings.filter((b) => b.parentApproval?.status === 'approved' || b.status === 'active' || b.status === 'accepted');
  const plan = getCurrentPlan(learnerId);
  const ruleFired = !!plan?.plan.paidTuition.recommended;
  return { pending, approved, ruleFired, reason: plan?.plan.paidTuition.reason ?? '' };
}

/** Everything a parent should act on, across children, most urgent first. */
export function attentionFor(parentId: string, children: ChildSummary[]): AttentionItem[] {
  const out: AttentionItem[] = [];
  const today = demoToday();
  for (const c of children) {
    const id = c.student.id;
    const first = c.student.firstName;
    const q = `?child=${id}`;
    const d = paidTutorDecision(id);
    for (const b of d.pending) {
      out.push({ id: `apr-${b.id}`, learnerId: id, tone: 'warning', title: `${first} asked for a paid tutor`, detail: 'Needs your approval before the tutor can start.', href: `/parent/plan${q}`, cta: 'Review' });
    }
    if (d.ruleFired && !d.pending.length && !d.approved.length) {
      out.push({ id: `rule-${id}`, learnerId: id, tone: 'warning', title: `A paid tutor is suggested for ${first}`, detail: d.reason, href: `/parent/plan${q}`, cta: 'See why' });
    }
    for (const a of getApplications(id).applications) {
      const days = daysBetween(today, a.deadline);
      if (a.status !== 'submitted' && a.status !== 'decision' && days >= 0 && days <= 21) {
        out.push({ id: `app-${a.id}`, learnerId: id, tone: days < 14 ? 'danger' : 'brand', title: `${first}'s application deadline in ${days} days`, detail: a.riskFlags?.[0] ?? 'Track it in Applications.', href: `/parent/applications${q}`, cta: 'Open' });
      }
    }
  }
  for (const inv of getInvoices(parentId).filter((i) => i.status !== 'paid')) {
    const first = children.find((c) => c.student.id === inv.learnerId)?.student.firstName ?? '';
    out.push({
      id: `inv-${inv.id}`, learnerId: inv.learnerId, tone: inv.status === 'overdue' ? 'danger' : 'brand',
      title: `${inv.status === 'overdue' ? 'Overdue' : 'Invoice due'}: ${inv.lines[0]?.title ?? 'Learnibility'}`,
      detail: `${first ? `${first}, ` : ''}due ${fmtDate(inv.dueDate)}`, href: `/parent/payments?child=${inv.learnerId}`, cta: 'Pay',
    });
  }
  const rank = { danger: 0, warning: 1, brand: 2 };
  return out.sort((a, b) => rank[a.tone] - rank[b.tone]);
}
