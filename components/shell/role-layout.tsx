import type { ReactNode } from 'react';
import { redirect } from 'next/navigation';
import { roleHome } from '@/lib/nav';
import { currentPersona } from '@/lib/session';
import type { Role } from '@/lib/types';
import { AppShell } from './app-shell';

/** Shared layout for every role area: requires a persona of that role, else sends them home or to /login. */
export async function RoleLayout({ role, children }: { role: Role; children: ReactNode }) {
  const persona = await currentPersona();
  if (!persona) redirect('/login');
  if (persona.role !== role) redirect(roleHome(persona.role));
  return (
    <AppShell role={role} persona={persona}>
      {children}
    </AppShell>
  );
}
