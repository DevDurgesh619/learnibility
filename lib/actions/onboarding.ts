'use server';

import { revalidatePath } from 'next/cache';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { SESSION_COOKIE } from '@/lib/session';
import {
  DEMO_OTP,
  NEW_STUDENT_PERSONA_ID,
  RETURNING_PHONES,
  isValidIndianMobile,
  normalisePhone,
} from '@/components/onboarding/demo-auth';
import { DRAFT_COOKIE, parseDraft, type OnboardingDraft } from '@/components/onboarding/draft';
import { completeOnboardingFor } from '@/components/onboarding/complete';
import { loadOnboardingForm } from '@/components/onboarding/forms';
import type { OnboardingResponses } from '@/lib/onboarding/score';

const COOKIE_OPTS = { path: '/', httpOnly: true, sameSite: 'lax' as const, maxAge: 60 * 60 * 24 * 30 };

async function readDraft(): Promise<OnboardingDraft> {
  const jar = await cookies();
  return parseDraft(jar.get(DRAFT_COOKIE)?.value);
}

async function writeDraft(patch: Partial<OnboardingDraft>) {
  const jar = await cookies();
  const next = { ...parseDraft(jar.get(DRAFT_COOKIE)?.value), ...patch };
  jar.set(DRAFT_COOKIE, JSON.stringify(next), COOKIE_OPTS);
  return next;
}

/** 1b → 1c. */
export async function requestOtp(_: unknown, formData: FormData): Promise<{ error?: string }> {
  const phone = normalisePhone(String(formData.get('phone') ?? ''));
  if (!isValidIndianMobile(phone)) return { error: 'Enter a 10-digit Indian mobile number.' };
  redirect(`/signup/verify?phone=${phone}`);
}

/** 1c: returning numbers go straight to their Home (2b); new ones choose a role (1d). */
export async function verifyOtp(_: unknown, formData: FormData): Promise<{ error?: string }> {
  const phone = normalisePhone(String(formData.get('phone') ?? ''));
  const code = String(formData.get('code') ?? '').replace(/\D/g, '');
  if (code.length !== 6) return { error: 'Enter all 6 digits.' };
  if (code !== DEMO_OTP) return { error: "That code didn't match. Try again." };
  const jar = await cookies();
  const returning = RETURNING_PHONES[phone];
  if (returning) {
    jar.set(SESSION_COOKIE, returning, COOKIE_OPTS);
    redirect('/student');
  }
  jar.set(DRAFT_COOKIE, JSON.stringify({ phone } satisfies OnboardingDraft), COOKIE_OPTS);
  redirect('/signup/role');
}

/** 1d: only students continue into onboarding in this demo. */
export async function chooseRole(formData: FormData) {
  const role = String(formData.get('role') ?? 'student');
  if (role !== 'student') redirect('/login');
  const jar = await cookies();
  jar.set(SESSION_COOKIE, NEW_STUDENT_PERSONA_ID, COOKIE_OPTS);
  redirect('/onboarding/about');
}

const GRADES = new Set([8, 9, 10, 11, 12]);

/** 1e. */
export async function saveAbout(_: unknown, formData: FormData): Promise<{ error?: string }> {
  const name = String(formData.get('name') ?? '').trim();
  const grade = Number(formData.get('grade'));
  const board = String(formData.get('board') ?? '') as OnboardingDraft['board'];
  const stream = String(formData.get('stream') ?? 'none') as OnboardingDraft['stream'];
  const age = Number(formData.get('age')) || undefined;
  const target = String(formData.get('target') ?? 'not_sure') as OnboardingDraft['target'];
  const targetYear = Number(formData.get('targetYear')) || undefined;
  if (name.length < 2) return { error: 'Tell us your name.' };
  if (!GRADES.has(grade)) return { error: 'Pick your class.' };
  if (!board || !['cbse', 'cambridge', 'ib'].includes(board)) return { error: 'Pick your board.' };
  if (grade >= 11 && (!stream || stream === 'none')) return { error: 'Pick your stream for class 11 and 12.' };
  await writeDraft({ name, grade: grade as OnboardingDraft['grade'], board, stream: grade >= 11 ? stream : 'none', age, target, targetYear });
  redirect('/onboarding/needs');
}

/** 1f. */
export async function saveNeeds(formData: FormData) {
  const all = formData.get('all') === '1';
  const needs = all ? ['tutors', 'progress', 'applications', 'career'] : formData.getAll('needs').map(String);
  await writeDraft({ needs: needs as OnboardingDraft['needs'] });
  redirect('/onboarding/profile');
}

/** 1g (skippable). */
export async function saveProfile(formData: FormData) {
  if (formData.get('skip') === '1') {
    await writeDraft({ profileSkipped: true });
    redirect('/onboarding/test');
  }
  const pct = Number(formData.get('lastExamPercent'));
  const sat = String(formData.get('satStatus') ?? '') as OnboardingDraft['satStatus'];
  await writeDraft({
    profileSkipped: false,
    school: String(formData.get('school') ?? '').trim() || undefined,
    lastExamPercent: pct > 0 && pct <= 100 ? pct : undefined,
    hardSubjects: formData.getAll('hardSubjects').map(String).slice(0, 3),
    satStatus: sat || undefined,
    satScore: Number(formData.get('satScore')) || undefined,
    activities: String(formData.get('activities') ?? '').trim() || undefined,
  });
  redirect('/onboarding/test');
}

export async function deferTest() {
  await writeDraft({ test: 'later' });
  redirect('/onboarding/setup');
}

export async function getDraft(): Promise<OnboardingDraft> {
  return readDraft();
}

/**
 * 1i: save the starting test and everything from 1e-1g, then build the first plan and timetable.
 * `responses` are the onboarding answers kept on the device during the test; the server re-scores them.
 */
export async function completeOnboarding(input: { formId: string | null; responses: OnboardingResponses }): Promise<{ ok: boolean; openGaps: number; band: string }> {
  const jar = await cookies();
  const learnerId = jar.get(SESSION_COOKIE)?.value;
  if (!learnerId) redirect('/signup');
  const draft = parseDraft(jar.get(DRAFT_COOKIE)?.value);
  const file = input.formId ? await loadOnboardingForm(input.formId) : null;
  // Re-mark Part A on the server from the chosen options.
  const byId = new Map((file?.items ?? []).map((i) => [i.id, i]));
  const academic = (input.responses.academic ?? [])
    .filter((r) => byId.get(r.questionId)?.part === 'A')
    .map((r) => {
      const it = byId.get(r.questionId) as { answer: string };
      const answer = (r as { answer?: string }).answer;
      return { ...r, correct: answer !== undefined ? answer === it.answer : r.correct };
    });
  const { student } = completeOnboardingFor({
    learnerId,
    draft,
    file,
    responses: { academic, reasoning: input.responses.reasoning ?? [], survey: input.responses.survey ?? [] },
  });
  jar.set(DRAFT_COOKIE, JSON.stringify({ ...draft, test: academic.length ? 'done' : 'later' } satisfies OnboardingDraft), COOKIE_OPTS);
  const { getGaps } = await import('@/lib/data');
  revalidatePath('/student', 'layout');
  return { ok: true, openGaps: getGaps(learnerId, { status: 'open' }).length, band: student.band };
}
