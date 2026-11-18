'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { NAV, navHref } from '@/lib/nav';
import type { Role } from '@/lib/types';
import { cn } from '@/lib/utils';
import { NavIcon } from './nav-icon';

export function SidebarNav({ role, onNavigate }: { role: Role; onNavigate?: () => void }) {
  const pathname = usePathname();
  return (
    <nav className="flex flex-col gap-0.5" aria-label="Main">
      {NAV[role].map((item) => {
        const href = navHref(role, item);
        const active = item.slug ? pathname === href || pathname.startsWith(`${href}/`) : pathname === href;
        return (
          <Link
            key={href}
            href={href}
            onClick={onNavigate}
            aria-current={active ? 'page' : undefined}
            className={cn(
              'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
              active ? 'bg-brand-50 text-brand-700' : 'text-muted hover:bg-surface-muted hover:text-ink',
            )}
          >
            <NavIcon name={item.icon} className={cn('size-4', active ? 'text-brand-600' : 'text-subtle')} />
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}
