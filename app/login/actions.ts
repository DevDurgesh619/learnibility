'use server';

import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { getPersona } from '@/lib/data/personas';
import { roleHome } from '@/lib/nav';
import { SESSION_COOKIE } from '@/lib/session';

export async function loginAs(formData: FormData) {
  const persona = getPersona(String(formData.get('personaId') ?? ''));
  if (!persona) redirect('/login');
  const jar = await cookies();
  jar.set(SESSION_COOKIE, persona.id, { path: '/', httpOnly: true, sameSite: 'lax', maxAge: 60 * 60 * 24 * 30 });
  redirect(roleHome(persona.role));
}

export async function logout() {
  const jar = await cookies();
  jar.delete(SESSION_COOKIE);
  redirect('/login');
}
