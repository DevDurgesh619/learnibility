'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Search, SlidersHorizontal } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { Chip } from './chip';
import { BOARD_LABEL, subjectLabel } from './labels';
import { PRICE_OPTIONS, RATING_OPTIONS, activeFilterCount, filtersToParams, type TutorFilters } from './search';

/** Search box + Filters side panel (PDF 5a top bar, 5b panel). Applying filters navigates, so results render on the server. */
export function ExploreSearch({ base, initial, subjects, languages, openByDefault }: {
  base: string; initial: TutorFilters; subjects: string[]; languages: string[]; openByDefault?: boolean;
}) {
  const router = useRouter();
  const [q, setQ] = useState(initial.q ?? '');
  const [f, setF] = useState<TutorFilters>(initial);
  const [open, setOpen] = useState(!!openByDefault);
  const count = activeFilterCount(initial);
  const go = (next: TutorFilters) => {
    const p = filtersToParams({ ...next, q: q.trim() || undefined });
    router.push(p.size ? `${base}?${p}` : base);
  };
  const toggle = <K extends keyof TutorFilters>(k: K, v: TutorFilters[K]) => setF((s) => ({ ...s, [k]: s[k] === v ? undefined : v }));

  return (
    <div>
      <form className="flex gap-2" onSubmit={(e) => { e.preventDefault(); go(f); }} role="search">
        <label className="relative flex-1">
          <span className="sr-only">Search tutors</span>
          <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-subtle" aria-hidden />
          <input
            value={q} onChange={(e) => setQ(e.target.value)}
            placeholder='Search a subject, exam or tutor, e.g. "JEE physics"'
            className="h-10 w-full rounded-lg border border-line bg-surface pl-9 pr-3 text-sm outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100"
          />
        </label>
        <Button type="button" variant={count ? 'primary' : 'secondary'} onClick={() => setOpen((o) => !o)} aria-expanded={open} className={cn(count && 'bg-success-600 hover:bg-success-700')}>
          <SlidersHorizontal /> <span className="hidden sm:inline">Filters</span>{count ? ` · ${count}` : ''}
        </Button>
        <Button type="submit">Search</Button>
      </form>

      {open && (
        <div className="mt-3 rounded-[var(--radius-card)] border border-line bg-surface p-4 shadow-[var(--shadow-card)]">
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            <Group label="Subject">
              {subjects.map((s) => <Chip key={s} selected={f.subject === s} onClick={() => toggle('subject', s)}>{subjectLabel(s)}</Chip>)}
            </Group>
            <Group label="Board">
              {(['cbse', 'cambridge', 'ib'] as const).map((b) => <Chip key={b} selected={f.board === b} onClick={() => toggle('board', b)}>{BOARD_LABEL[b]}</Chip>)}
            </Group>
            <Group label="Rating">
              {RATING_OPTIONS.map((r) => <Chip key={r} selected={f.minRating === r} onClick={() => toggle('minRating', r)}>★ {r}+</Chip>)}
            </Group>
            <Group label="Price per hour">
              {PRICE_OPTIONS.map((p) => <Chip key={p} selected={f.maxPrice === p} onClick={() => toggle('maxPrice', p)}>under ₹{p.toLocaleString('en-IN')}</Chip>)}
            </Group>
            <Group label="Format and mode">
              <Chip selected={f.format === 'one_to_one'} onClick={() => toggle('format', 'one_to_one')}>1-on-1</Chip>
              <Chip selected={f.format === 'group'} onClick={() => toggle('format', 'group')}>Group</Chip>
              <Chip selected={f.mode === 'online'} onClick={() => toggle('mode', 'online')}>Online</Chip>
              <Chip selected={f.mode === 'offline'} onClick={() => toggle('mode', 'offline')}>In person</Chip>
            </Group>
            <Group label="Language">
              {languages.map((l) => <Chip key={l} selected={f.language === l} onClick={() => toggle('language', l)}>{l}</Chip>)}
              <Chip selected={!!f.verified} onClick={() => setF((s) => ({ ...s, verified: s.verified ? undefined : true }))}>Verified only</Chip>
            </Group>
          </div>
          <div className="mt-4 flex items-center gap-3 border-t border-line pt-4">
            <Button onClick={() => { setOpen(false); go(f); }}>Apply</Button>
            <Button variant="ghost" onClick={() => { setF({}); go({}); }}>Clear</Button>
            <span className="ml-auto text-xs text-muted">Results update when you apply filters</span>
          </div>
        </div>
      )}
    </div>
  );
}

function Group({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <fieldset>
      <legend className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted">{label}</legend>
      <div className="flex flex-wrap gap-2">{children}</div>
    </fieldset>
  );
}
