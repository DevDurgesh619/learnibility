'use server';

/**
 * W2-T tutor actions (tutor HTML 2a to 8e): home layout, session reports with homework, assignments,
 * evaluation, messages, private notes and profile edits. Learner-facing writes call recomputeLearner.
 */
import { cookies } from 'next/headers';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { TUTOR_HOME_COOKIE } from '@/components/tutor/constants';

/** Tutor Home ships both wireframe options (2a teaching-first, 2b marketplace-first) until one is picked. */
export async function setHomeLayout(data: FormData) {
  const v = data.get('layout') === 'b' ? 'b' : 'a';
  (await cookies()).set(TUTOR_HOME_COOKIE, v, { path: '/', maxAge: 60 * 60 * 24 * 365, sameSite: 'lax' });
  revalidatePath('/tutor');
  redirect('/tutor');
}
