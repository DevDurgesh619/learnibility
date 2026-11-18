import 'server-only';
import { redirect } from 'next/navigation';
import { getAdult, getChildren, type ChildSummary } from '@/lib/data';
import { currentPersona } from '@/lib/session';
import type { PersonaSummary } from '@/lib/types';

export interface ParentContext {
  parent: PersonaSummary;
  /** Display name from the adults file when present. */
  parentName: string;
  children: ChildSummary[];
  /** The child picked with ?child=, else the first. Undefined when the account has no linked child yet. */
  child?: ChildSummary;
}

/** Signed-in parent, their children and the selected child (?child=lrn_...). */
export async function parentContext(searchParams?: Promise<Record<string, string | string[] | undefined>>): Promise<ParentContext> {
  const parent = await currentPersona();
  if (!parent || parent.role !== 'parent') redirect('/login');
  const sp = (await searchParams) ?? {};
  const wanted = typeof sp.child === 'string' ? sp.child : undefined;
  const children = getChildren(parent.id);
  const child = children.find((c) => c.student.id === wanted) ?? children[0];
  return { parent, parentName: getAdult(parent.id)?.name ?? parent.name, children, child };
}

export type SearchParams = Promise<Record<string, string | string[] | undefined>>;

export const param = (sp: Record<string, string | string[] | undefined>, k: string) => (typeof sp[k] === 'string' ? (sp[k] as string) : undefined);
