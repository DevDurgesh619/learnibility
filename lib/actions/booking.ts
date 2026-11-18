'use server';

/**
 * W2-T booking actions (marketplace, PDF 5e and tutor HTML 2c, 5g).
 * Student requests a demo → tutor accepts or declines → the session lands in both Sessions and the student's timetable.
 * Writes go through lib/actions/core.ts; every write re-runs the learner's engines.
 */
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { appendEvent, newId, nowStamp, putRecord, recomputeLearner } from '@/lib/actions/core';
import { getBookings, getSessions, getStudent, getTutor } from '@/lib/data';
import type { Booking, Message, Session } from '@/lib/data/types';
import { currentPersona } from '@/lib/session';
import { buildSnapshot, loadMarketplaceLearner, mainSubjectFor, slotsFor } from '@/components/marketplace/queries';

export interface BookingFormState { error?: string }

function revalidateAll() {
  for (const p of ['/student', '/student/tutors', '/student/sessions', '/student/timetable', '/tutor', '/tutor/sessions', '/tutor/students', '/tutor/today', '/parent']) revalidatePath(p, 'layout');
}

function systemMessage(b: Booking, text: string) {
  const m: Message = {
    id: newId('msg'), threadId: `${b.learnerId}:${b.tutorId}`, learnerId: b.learnerId, from: 'system', toIds: [b.learnerId, b.tutorId], text, sentUtc: nowStamp(), tutorId: b.tutorId,
  };
  putRecord('messages', m);
}

/** PDF 5e "Confirm booking": a free demo request in a slot both calendars allow. */
export async function requestDemo(_: BookingFormState, data: FormData): Promise<BookingFormState> {
  const persona = await currentPersona();
  if (!persona || persona.role !== 'student') return { error: 'Sign in as a student to book.' };
  const tutor = getTutor(String(data.get('tutorId') ?? ''));
  if (!tutor) return { error: 'That tutor is no longer listed.' };
  const slot = String(data.get('slotStartUtc') ?? '');
  const learner = await loadMarketplaceLearner(persona.id);
  const student = getStudent(persona.id);
  if (!learner || !student) return { error: 'We could not find your profile.' };
  const { days } = await slotsFor(tutor, student);
  if (!days.some((d) => d.slots.some((s) => s.startUtc === slot))) return { error: 'That slot was just taken. Pick another one.' };
  if (getBookings(persona.id).some((b) => b.tutorId === tutor.id && (b.status === 'requested' || b.status === 'accepted'))) return { error: `You already have a booking with ${tutor.firstName}.` };

  const subjectId = String(data.get('subjectId') ?? '') || mainSubjectFor(learner, tutor);
  const share = data.get('share') === '1';
  const minutes = tutor.pricing.demoMinutes || 30;
  const topic = String(data.get('topic') ?? '').trim().slice(0, 160) || undefined;
  const match = learner.matches.find((m) => m.tutorId === tutor.id);
  const booking: Booking = {
    id: newId('bkg'), learnerId: student.id, tutorId: tutor.id, kind: 'demo', status: 'requested', format: 'one_to_one', mode: 'online',
    subjectId, priceInr: tutor.pricing.demoInr, requestedAt: nowStamp(), slotStartUtc: slot, minutes, topic,
    sharedGapSnapshot: share && subjectId ? buildSnapshot(learner, subjectId) : null,
    matchReason: match?.reason,
  };
  putRecord('bookings', booking);
  const code = `S-${getSessions(tutor.id).length + 1}`;
  const session: Session = {
    id: newId('ses'), code, learnerId: student.id, learnerIds: [student.id], hostId: tutor.id, hostRole: 'tutor', kind: 'demo',
    title: `Demo with ${tutor.displayName}`, subjectId, focus: topic, startUtc: slot, minutes, status: 'scheduled', mode: 'online',
    joinUrl: `https://meet.learnibility.demo/${booking.id}`, bookingId: booking.id, rateInr: 0, report: null,
  };
  putRecord('sessions', session);
  appendEvent(student.id, { sourceMethod: 'M1', type: 'tutor_demo_requested', payload: { bookingId: booking.id, tutorId: tutor.id, shared: share, subjectId } });
  systemMessage(booking, `${student.firstName} requested a free demo${topic ? `: ${topic}` : ''}.`);
  recomputeLearner(student.id, { reason: 'session_booked' });
  revalidateAll();
  redirect(`/student/tutors/booked/${booking.id}`);
}

async function tutorBooking(bookingId: string) {
  const persona = await currentPersona();
  if (!persona || persona.role !== 'tutor') throw new Error('Tutors only');
  const b = getBookings(persona.id).find((x) => x.id === bookingId);
  if (!b) throw new Error('Booking not found');
  return { tutorId: persona.id, b };
}

function sessionOf(b: Booking) {
  return getSessions(b.tutorId).find((s) => s.bookingId === b.id);
}

/** Tutor HTML 2c "Accept demo". */
export async function acceptBooking(data: FormData) {
  const { b } = await tutorBooking(String(data.get('bookingId')));
  putRecord('bookings', { ...b, status: 'accepted', respondedUtc: nowStamp() });
  const s = sessionOf(b);
  if (s) putRecord('sessions', { ...s, status: 'scheduled' });
  appendEvent(b.learnerId, { sourceMethod: 'M15', type: 'tutor_demo_accepted', payload: { bookingId: b.id, tutorId: b.tutorId } });
  systemMessage(b, `${getTutor(b.tutorId)?.firstName ?? 'Your tutor'} accepted the demo. See you then.`);
  recomputeLearner(b.learnerId, { reason: 'session_booked' });
  revalidateAll();
  redirect(`/tutor/students/${b.learnerId}`);
}

/** Tutor HTML 2c "Decline". The shared snapshot is dropped. */
export async function declineBooking(data: FormData) {
  const { b } = await tutorBooking(String(data.get('bookingId')));
  const reason = String(data.get('reason') ?? '').trim() || undefined;
  putRecord('bookings', { ...b, status: 'declined', respondedUtc: nowStamp(), sharedGapSnapshot: null, note: reason ?? b.note });
  const s = sessionOf(b);
  if (s) putRecord('sessions', { ...s, status: 'cancelled' });
  systemMessage(b, `${getTutor(b.tutorId)?.firstName ?? 'The tutor'} can't take this demo${reason ? `: ${reason}` : ''}. Try another time or tutor.`);
  recomputeLearner(b.learnerId, { reason: 'session_cancelled' });
  revalidateAll();
  redirect('/tutor');
}

/** Tutor HTML 5g: move a session to another free slot (the student is told in their messages), or cancel it. */
export async function rescheduleSession(data: FormData) {
  const persona = await currentPersona();
  if (!persona || persona.role !== 'tutor') throw new Error('Tutors only');
  const s = getSessions(persona.id).find((x) => x.id === String(data.get('sessionId')));
  if (!s) throw new Error('Session not found');
  const cancel = data.get('intent') === 'cancel';
  const start = String(data.get('slotStartUtc') ?? '');
  const note = String(data.get('message') ?? '').trim();
  if (!cancel && !start) throw new Error('Pick a slot');
  putRecord('sessions', cancel ? { ...s, status: 'cancelled' } : { ...s, startUtc: start });
  const b = s.bookingId ? getBookings(persona.id).find((x) => x.id === s.bookingId) : undefined;
  if (cancel && b && b.status === 'requested') putRecord('bookings', { ...b, status: 'cancelled' });
  const tutorName = getTutor(persona.id)?.firstName ?? 'Your tutor';
  const when = new Intl.DateTimeFormat('en-IN', { weekday: 'short', day: 'numeric', month: 'short', hour: 'numeric', minute: '2-digit', timeZone: 'Asia/Kolkata' }).format(new Date(start || s.startUtc));
  for (const lid of s.learnerIds?.length ? s.learnerIds : [s.learnerId]) {
    putRecord('messages', {
      id: newId('msg'), threadId: `${lid}:${persona.id}`, learnerId: lid, from: 'system', toIds: [lid, persona.id], tutorId: persona.id, sentUtc: nowStamp(),
      text: cancel ? `${tutorName} cancelled ${s.code ?? 'the session'}${note ? `: ${note}` : '.'}` : `${tutorName} moved ${s.code ?? 'the session'} to ${when}.${note ? ` "${note}"` : ''}`,
    } satisfies Message);
    recomputeLearner(lid, { reason: cancel ? 'session_cancelled' : 'session_booked' });
  }
  revalidateAll();
  redirect('/tutor/sessions');
}
