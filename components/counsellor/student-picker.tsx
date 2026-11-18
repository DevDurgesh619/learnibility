'use client';

import { usePathname, useRouter, useSearchParams } from 'next/navigation';

/** Pick a caseload student; keeps the current page and swaps ?student=. */
export function StudentPicker({ students, value, label = 'Student' }: { students: { id: string; name: string; meta?: string }[]; value?: string; label?: string }) {
  const router = useRouter();
  const pathname = usePathname();
  const params = useSearchParams();
  return (
    <label className="flex min-w-0 items-center gap-2 text-sm text-muted">
      <span className="shrink-0">{label}</span>
      <select
        className="h-10 min-w-0 flex-1 rounded-lg border border-line bg-surface px-3 text-sm text-ink shadow-sm sm:w-72 sm:flex-none"
        value={value ?? ''}
        onChange={(e) => {
          const next = new URLSearchParams(params.toString());
          next.set('student', e.target.value);
          router.push(`${pathname}?${next.toString()}`);
        }}
      >
        {students.map((s) => (
          <option key={s.id} value={s.id}>{s.name}{s.meta ? ` · ${s.meta}` : ''}</option>
        ))}
      </select>
    </label>
  );
}
