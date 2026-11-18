import type { ReactNode } from 'react';
import Link from 'next/link';
import { LogOut, Repeat, RotateCcw } from 'lucide-react';
import { logout } from '@/app/login/actions';
import { Avatar } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { DEMO_NOW, DEMO_TIMEZONE } from '@/lib/demo-clock';
import { NAV, ROLE_LABEL, type NavItem } from '@/lib/nav';
import type { PersonaSummary, Role } from '@/lib/types';
import { Logo } from './logo';
import { MobileNav } from './mobile-nav';
import { SidebarNav } from './sidebar-nav';

const demoDate = new Intl.DateTimeFormat('en-IN', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric', timeZone: DEMO_TIMEZONE }).format(DEMO_NOW);

/** The signed-in frame: role sidebar on desktop, drawer on mobile, top bar with persona and demo date. */
export function AppShell({ role, persona, nav, children }: { role: Role; persona: PersonaSummary; nav?: NavItem[]; children: ReactNode }) {
  const items = nav ?? NAV[role];
  return (
    <div className="min-h-screen lg:grid lg:grid-cols-[256px_1fr]">
      <aside className="sticky top-0 hidden h-screen flex-col gap-6 border-r border-line bg-surface p-4 lg:flex">
        <Logo href={`/${role}`} />
        <SidebarNav role={role} items={items} />
        <div className="mt-auto rounded-lg bg-surface-muted p-3 text-xs text-muted">
          <p className="font-medium text-ink">Demo mode</p>
          <p>All people and data are fictional. Today is {demoDate}.</p>
        </div>
      </aside>
      <div className="flex min-w-0 flex-col">
        <header className="sticky top-0 z-40 flex h-16 items-center gap-3 border-b border-line bg-surface/90 px-4 backdrop-blur sm:px-6">
          <MobileNav role={role} items={items} />
          <div className="lg:hidden"><Logo href={`/${role}`} /></div>
          <div className="ml-auto flex items-center gap-3">
            <Badge tone="brand" className="hidden sm:inline-flex">{ROLE_LABEL[role]}</Badge>
            <div className="flex items-center gap-2">
              <Avatar name={persona.name} src={persona.avatar} size="sm" />
              <span className="hidden text-sm font-medium text-ink sm:inline">{persona.name}</span>
            </div>
            {/* Clears every demo write (tests taken, bookings, approvals) so the next demo starts clean. */}
            <form action="/api/demo-reset" method="post">
              <button className="rounded-lg p-2 text-muted hover:bg-surface-muted hover:text-ink" title="Reset demo" aria-label="Reset demo">
                <RotateCcw className="size-4" />
              </button>
            </form>
            <Link href="/login" className="rounded-lg p-2 text-muted hover:bg-surface-muted hover:text-ink" title="Switch persona" aria-label="Switch persona">
              <Repeat className="size-4" />
            </Link>
            <form action={logout}>
              <button className="rounded-lg p-2 text-muted hover:bg-surface-muted hover:text-ink" title="Log out" aria-label="Log out">
                <LogOut className="size-4" />
              </button>
            </form>
          </div>
        </header>
        <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-6 sm:px-6 lg:py-8">{children}</main>
      </div>
    </div>
  );
}
