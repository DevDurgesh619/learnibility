import 'server-only';
import { redirect } from 'next/navigation';
import { getAdult, getCaseload, type CaseloadEntry } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import type { PersonaSummary } from '@/lib/types';

export interface MentorContext { mentor: PersonaSummary; mentorName: string; mentees: CaseloadEntry[]; mentee?: CaseloadEntry }

/** Signed-in mentor, their mentees and the one picked with ?mentee=. Mentors see T1 data only (lib/visibility). */
export async function mentorContext(searchParams?: Promise<Record<string, string | string[] | undefined>>): Promise<MentorContext> {
  const mentor = await currentPersona();
  if (!mentor || mentor.role !== 'mentor') redirect('/login');
  const sp = (await searchParams) ?? {};
  const mentees = getCaseload(mentor.id).sort((a, b) => a.student.name.localeCompare(b.student.name));
  const wanted = typeof sp.mentee === 'string' ? sp.mentee : undefined;
  return { mentor, mentorName: getAdult(mentor.id)?.name ?? mentor.name, mentees, mentee: mentees.find((m) => m.student.id === wanted) ?? mentees[0] };
}
