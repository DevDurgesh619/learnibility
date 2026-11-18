import 'server-only';
import { redirect } from 'next/navigation';
import { currentPersona } from '@/lib/session';
import { isPaid, nameOf, studentCtx } from './data';

/** Paid Application Support pages: free students go to the upgrade page. */
export async function requireSubscriber() {
  const persona = (await currentPersona())!;
  const ctx = studentCtx(persona.id);
  if (!isPaid(ctx.plan)) redirect('/student/applications/upgrade');
  return { persona, ctx, counsellorName: ctx.counsellorId ? nameOf(ctx.counsellorId) : undefined };
}
