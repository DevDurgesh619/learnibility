import Link from 'next/link';
import { Avatar } from '@/components/ui';
import { cn } from '@/lib/utils';
import type { ChildSummary } from '@/lib/data';

/** Pill switcher for families with more than one child (the Kapoors). Hidden for one child. */
export function ChildSwitcher({ children, selectedId, basePath, extra }: { children: ChildSummary[]; selectedId?: string; basePath: string; extra?: Record<string, string> }) {
  if (children.length < 2) return null;
  return (
    <nav aria-label="Choose child" className="mb-6 flex flex-wrap gap-2">
      {children.map((c) => {
        const q = new URLSearchParams({ ...extra, child: c.student.id });
        const active = c.student.id === selectedId;
        return (
          <Link
            key={c.student.id}
            href={`${basePath}?${q}`}
            aria-current={active ? 'page' : undefined}
            className={cn(
              'inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-sm transition-colors',
              active ? 'border-brand-300 bg-brand-50 font-medium text-brand-700' : 'border-line bg-surface text-muted hover:bg-surface-muted hover:text-ink',
            )}
          >
            <Avatar name={c.student.name} size="sm" className="size-6 text-[10px]" />
            {c.student.firstName}
            <span className="text-xs text-subtle">Grade {c.student.grade}</span>
          </Link>
        );
      })}
    </nav>
  );
}
