import 'server-only';
import { cookies } from 'next/headers';
import { getPersona } from './data/personas';
import type { PersonaSummary } from './types';
import { RESET_COOKIE, syncResetEpoch } from './store/overlay';

/** Demo login: the chosen persona's ID lives in a cookie. No passwords. */
export const SESSION_COOKIE = 'learnibility_persona';

export async function currentPersona(): Promise<PersonaSummary | undefined> {
  const jar = await cookies();
  syncResetEpoch(Number(jar.get(RESET_COOKIE)?.value));
  return getPersona(jar.get(SESSION_COOKIE)?.value);
}
