import Link from 'next/link';
import { Avatar } from '@/components/ui';
import type { CaseloadEntry } from '@/lib/data';
import { cn } from '@/lib/utils';

export function MenteeSwitcher({ mentees, selectedId, basePath }: { mentees: CaseloadEntry[]; selectedId?: string; basePath: string }) {
  if (mentees.length < 2) return null;
  return (
    <nav aria-label="Choose mentee" className="mb-6 flex flex-wrap gap-2">
      {mentees.map((m) => (
        <Link key={m.student.id} href={`${basePath}?mentee=${m.student.id}`} aria-current={m.student.id === selectedId ? 'page' : undefined}
          className={cn('inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-sm', m.student.id === selectedId ? 'border-brand-300 bg-brand-50 font-medium text-brand-700' : 'border-line bg-surface text-muted hover:bg-surface-muted hover:text-ink')}>
          <Avatar name={m.student.name} size="sm" className="size-6 text-[10px]" />{m.student.firstName}
        </Link>
      ))}
    </nav>
  );
}
