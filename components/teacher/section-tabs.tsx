import Link from 'next/link';
import { cn } from '@/lib/utils';

export interface SectionTab {
  id: string;
  name: string;
  count: number;
}

/** Section switcher (9A Maths, 10B Maths ...). Keeps the other query params of the page. */
export function SectionTabs({ sections, activeId, hrefFor }: { sections: SectionTab[]; activeId: string; hrefFor: (id: string) => string }) {
  return (
    <nav aria-label="Sections" className="flex gap-1 overflow-x-auto rounded-xl border border-line bg-surface p-1">
      {sections.map((s) => (
        <Link
          key={s.id}
          href={hrefFor(s.id)}
          aria-current={s.id === activeId ? 'page' : undefined}
          className={cn(
            'flex shrink-0 items-center gap-2 rounded-lg px-3 py-1.5 text-sm font-medium transition-colors',
            s.id === activeId ? 'bg-brand-600 text-white shadow-sm' : 'text-muted hover:bg-surface-muted hover:text-ink',
          )}
        >
          {s.name}
          <span className={cn('rounded-full px-1.5 text-xs', s.id === activeId ? 'bg-white/20' : 'bg-surface-muted')}>{s.count}</span>
        </Link>
      ))}
    </nav>
  );
}
