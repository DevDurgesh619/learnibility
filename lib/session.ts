import 'server-only';
import { cookies } from 'next/headers';
import { getPersona } from './data/personas';
import type { PersonaSummary } from './types';

/** Demo login: the chosen persona's ID lives in a cookie. No passwords. */
export const SESSION_COOKIE = 'learnibility_persona';

export async function currentPersona(): Promise<PersonaSummary | undefined> {
  const jar = await cookies();
  return getPersona(jar.get(SESSION_COOKIE)?.value);
}
