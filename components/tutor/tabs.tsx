'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';

/** Underlined link tabs; the longest matching href is active. */
export function LinkTabs({ tabs, className }: { tabs: { href: string; label: string; count?: number }[]; className?: string }) {
  const path = usePathname();
  const active = [...tabs].sort((a, b) => b.href.length - a.href.length).find((t) => path === t.href || path.startsWith(`${t.href}/`))?.href;
  return (
    <nav className={cn('-mx-4 overflow-x-auto px-4 sm:mx-0 sm:px-0', className)} aria-label="Sections">
      <ul className="flex min-w-max gap-1 border-b border-line">
        {tabs.map((t) => (
          <li key={t.href}>
            <Link
              href={t.href}
              aria-current={active === t.href ? 'page' : undefined}
              className={cn('-mb-px inline-flex items-center gap-1.5 border-b-2 px-3 py-2 text-sm font-medium transition-colors',
                active === t.href ? 'border-brand-600 text-brand-700' : 'border-transparent text-muted hover:text-ink')}
            >
              {t.label}
              {t.count !== undefined && t.count > 0 && <span className="rounded-full bg-surface-muted px-1.5 text-xs text-muted">{t.count}</span>}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}
