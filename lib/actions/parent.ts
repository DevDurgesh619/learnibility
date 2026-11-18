'use server';
/**
 * W2-P parent writes. Every write goes through lib/actions/core.ts (overlay store), then re-runs the
 * learner's derived state so other roles see the change (the tutor gets the request, the student sees the booking).
 */
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import {
  demoNow, getBookings, getChildren, getConsents, getCurrentPlan, getGaps, getInvoices, getMessages, getSubtopic, getTutor,
  type Approval, type Booking, type Consent, type GapSnapshot, type Invoice, type Message,
} from '@/lib/data';
import { currentPersona } from '@/lib/session';
import { appendEvent, newId, nowStamp, putRecord, recomputeLearner } from './core';

const str = (f: FormData, k: string) => {
  const v = f.get(k);
  return typeof v === 'string' && v.trim() ? v.trim() : undefined;
};

/** The signed-in parent and a check that the learner is their child. */
async function parentFor(learnerId: string | undefined) {
  const me = await currentPersona();
  if (!me || me.role !== 'parent') throw new Error('Only a parent can do this.');
  if (!learnerId || !getChildren(me.id).some((c) => c.student.id === learnerId)) throw new Error('Not your child.');
  return me;
}

function back(path: string, learnerId: string, extra: Record<string, string> = {}): never {
  revalidatePath('/', 'layout');
  redirect(`${path}?${new URLSearchParams({ child: learnerId, ...extra })}`);
}

/** Gap snapshot for the tutor, only when the family consented to sharing with tutors. */
function snapshotFor(learnerId: string, subjectId: string | undefined): GapSnapshot | null {
  const consent = getConsents(learnerId).find((c) => c.scope === 'share_with_tutor' && !c.revokedUtc);
  if (!consent || !subjectId) return null;
  const gaps = getGaps(learnerId, { status: 'open', subjectId });
  return {
    sharedUtc: demoNow(),
    subjectId,
    gaps: gaps.map((g) => ({ gapId: g.id, subtopicId: g.subtopicId, name: getSubtopic(g.subtopicId)?.name ?? g.subtopicId, code: g.code, level: g.level, hoursToClose: g.hoursToClose })),
  };
}

/**
 * Approve paid tutoring. With `bookingId`: approve a booking the student requested (pending parent approval).
 * With `tutorId`: the 3-week rule fired and the parent picks a matched tutor; this creates the booking request.
 */
export async function approvePaidTutor(form: FormData) {
  const learnerId = str(form, 'learnerId');
  const me = await parentFor(learnerId);
  const now = nowStamp();
  const note = str(form, 'note');
  let booking: Booking;
  const existing = str(form, 'bookingId') ? getBookings(learnerId!).find((b) => b.id === str(form, 'bookingId')) : undefined;
  if (existing) {
    booking = { ...existing, parentApproval: { parentId: me.id, status: 'approved', utc: now, reason: note } };
  } else {
    const tutor = getTutor(str(form, 'tutorId') ?? '');
    if (!tutor) throw new Error('Pick a tutor to approve.');
    const subjectId = str(form, 'subjectId');
    booking = {
      id: newId(`bkg_${learnerId}`),
      learnerId: learnerId!,
      tutorId: tutor.id,
      kind: 'regular',
      status: 'requested',
      format: 'one_to_one',
      mode: tutor.modes.includes('online') ? 'online' : tutor.modes[0],
      subjectId,
      priceInr: tutor.pricing.oneToOnePerHourInr,
      requestedAt: now,
      minutes: tutor.sessionMinutes,
      sessionsPerWeek: Number(str(form, 'sessionsPerWeek') ?? 2),
      topic: str(form, 'topic'),
      note: note ?? 'Requested by parent after the free plan ran 3 weeks without closing the gaps.',
      sharedGapSnapshot: snapshotFor(learnerId!, subjectId),
      parentApproval: { parentId: me.id, status: 'approved', utc: now, reason: note },
      matchReason: str(form, 'matchReason'),
    };
  }
  putRecord('bookings', booking);
  const approval: Approval = { id: `apr_${booking.id}`, learnerId: learnerId!, kind: 'paid_tutor', targetId: booking.id, byId: me.id, decision: 'approved', utc: now, note };
  putRecord('approvals', approval);
  appendEvent(learnerId!, {
    sourceMethod: 'M2', type: 'parent_approved_paid_tutor',
    payload: { bookingId: booking.id, tutorId: booking.tutorId, priceInr: booking.priceInr, planId: getCurrentPlan(learnerId!)?.id },
  });
  recomputeLearner(learnerId!, { reason: 'session_booked' });
  back('/parent/plan', learnerId!, { done: 'approved', booking: booking.id });
}

export async function declinePaidTutor(form: FormData) {
  const learnerId = str(form, 'learnerId');
  const me = await parentFor(learnerId);
  const b = getBookings(learnerId!).find((x) => x.id === str(form, 'bookingId'));
  if (!b) throw new Error('Booking not found.');
  const now = nowStamp();
  const note = str(form, 'note');
  putRecord('bookings', { ...b, status: 'cancelled', parentApproval: { parentId: me.id, status: 'declined', utc: now, reason: note } } satisfies Booking);
  putRecord('approvals', { id: `apr_${b.id}`, learnerId: learnerId!, kind: 'paid_tutor', targetId: b.id, byId: me.id, decision: 'declined', utc: now, note } satisfies Approval);
  appendEvent(learnerId!, { sourceMethod: 'M2', type: 'parent_declined_paid_tutor', payload: { bookingId: b.id } });
  recomputeLearner(learnerId!);
  back('/parent/plan', learnerId!, { done: 'declined' });
}

/** Demo payment: marks the invoice paid (no real gateway). */
export async function payInvoice(form: FormData) {
  const learnerId = str(form, 'learnerId');
  const me = await parentFor(learnerId);
  const inv = getInvoices(me.id).find((i) => i.id === str(form, 'invoiceId'));
  if (!inv) throw new Error('Invoice not found.');
  putRecord('invoices', { ...inv, status: 'paid', paidUtc: nowStamp() } satisfies Invoice);
  appendEvent(learnerId!, { sourceMethod: 'M2', type: 'invoice_paid', payload: { invoiceId: inv.id, amountInr: inv.amountInr } });
  back('/parent/payments', learnerId!, { paid: inv.id });
}

export async function revokeConsent(form: FormData) {
  const learnerId = str(form, 'learnerId');
  await parentFor(learnerId);
  const c = getConsents(learnerId!).find((x) => x.id === str(form, 'consentId'));
  if (!c) throw new Error('Consent not found.');
  putRecord('consents', { ...c, revokedUtc: nowStamp() } satisfies Consent);
  appendEvent(learnerId!, { sourceMethod: 'M2', type: 'consent_revoked', payload: { consentId: c.id, scope: c.scope } });
  recomputeLearner(learnerId!);
  back('/parent/privacy', learnerId!, { done: 'revoked' });
}

export async function grantConsent(form: FormData) {
  const learnerId = str(form, 'learnerId');
  const me = await parentFor(learnerId);
  const scope = str(form, 'scope') as Consent['scope'] | undefined;
  if (!scope) throw new Error('Pick a consent.');
  const c: Consent = { id: newId(`cns_${learnerId}_${scope}`), learnerId: learnerId!, grantedById: me.id, scope, version: '2026-11', grantedUtc: nowStamp() };
  putRecord('consents', c);
  appendEvent(learnerId!, { sourceMethod: 'M2', type: 'consent_granted', payload: { consentId: c.id, scope } });
  recomputeLearner(learnerId!);
  back('/parent/privacy', learnerId!, { done: 'granted' });
}

/** Parent message to a teacher, tutor or counsellor about one child. */
export async function sendParentMessage(form: FormData) {
  const learnerId = str(form, 'learnerId');
  const me = await parentFor(learnerId);
  const to = str(form, 'to');
  const text = str(form, 'text');
  if (!to || !text) throw new Error('Write a message first.');
  const threadId = str(form, 'threadId') ?? `${learnerId}:${me.id}:${to}`;
  const known = getMessages(me.id, { threadId });
  const m: Message = {
    id: newId('msg'), threadId, learnerId: learnerId!, from: me.id, toIds: [to], text, sentUtc: nowStamp(), readBy: [me.id],
    ...(to.startsWith('tut_') ? { tutorId: to } : {}),
  };
  putRecord('messages', m);
  back('/parent/messages', learnerId!, { thread: known[0]?.threadId ?? threadId });
}
