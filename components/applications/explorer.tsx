'use client';

import { fieldLabel } from './fields';
import Link from 'next/link';
import { useMemo, useState } from 'react';
import { Search, SlidersHorizontal, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import { cn } from '@/lib/utils';
import { SHOW_COSTS } from './config';
import { ActionButton } from './action-button';

/** Lightweight university row for client-side search (built on the server from listUniversities). */
export interface UniRow {
  id: string;
  name: string;
  shortName: string;
  country: string;
  countryName: string;
  city: string;
  type: 'public' | 'private';
  qsRank: number | null;
  acceptancePct: number | null;
  tuitionInr: number;
  tuitionLabel: string;
  fields: string[];
  programmes: string[];
  satLabel: string;
  satLow: number | null;
  testOptional: boolean;
  ielts: number | null;
  deadline: string;
  deadlineLabel: string;
  saved: boolean;
  defaultProgrammeId: string;
  /** Programme matching the student's course, when there is one. */
  defaultProgramme?: string;
}

export interface Filters {
  country: string[];
  maxTuition: number | null;
  field: string | null;
  type: 'public' | 'private' | null;
  admit: 'under10' | '10to30' | 'over30' | null;
  rank: 50 | 100 | 200 | null;
  ielts: number | null;
  sat: number | null;
}

const EMPTY: Filters = { country: [], maxTuition: null, field: null, type: null, admit: null, rank: null, ielts: null, sat: null };

const TUITION_STEPS = [
  { v: 1_000_000, l: 'Under ₹10 L / yr' }, { v: 2_500_000, l: 'Under ₹25 L / yr' }, { v: 4_000_000, l: 'Under ₹40 L / yr' }, { v: 6_000_000, l: 'Under ₹60 L / yr' },
];

function matches(r: UniRow, q: string, f: Filters) {
  if (q) {
    const hay = `${r.name} ${r.shortName} ${r.city} ${r.countryName} ${r.programmes.join(' ')} ${r.fields.map(fieldLabel).join(' ')}`.toLowerCase();
    if (!q.toLowerCase().split(/[\s,]+/).filter(Boolean).every((w) => hay.includes(w) || (w === 'cs' && r.fields.includes('computer-science')))) return false;
  }
  if (f.country.length && !f.country.includes(r.country)) return false;
  if (f.maxTuition !== null && r.tuitionInr > f.maxTuition) return false;
  if (f.field && !r.fields.includes(f.field)) return false;
  if (f.type && r.type !== f.type) return false;
  if (f.admit) {
    const a = r.acceptancePct;
    if (a === null) return false;
    if (f.admit === 'under10' && !(a < 10)) return false;
    if (f.admit === '10to30' && !(a >= 10 && a <= 30)) return false;
    if (f.admit === 'over30' && !(a > 30)) return false;
  }
  if (f.rank !== null && (r.qsRank === null || r.qsRank > f.rank)) return false;
  if (f.ielts !== null && r.ielts !== null && r.ielts > f.ielts) return false;
  if (f.sat !== null && !r.testOptional && r.satLow !== null && r.satLow > f.sat) return false;
  return true;
}

function chips(f: Filters): { key: keyof Filters; label: string; value?: string }[] {
  const out: { key: keyof Filters; label: string; value?: string }[] = [];
  for (const c of f.country) out.push({ key: 'country', label: `Location: ${c.toUpperCase()}`, value: c });
  if (f.maxTuition !== null) out.push({ key: 'maxTuition', label: TUITION_STEPS.find((t) => t.v === f.maxTuition)?.l ?? 'Tuition' });
  if (f.field) out.push({ key: 'field', label: `Course: ${fieldLabel(f.field)}` });
  if (f.type) out.push({ key: 'type', label: f.type === 'public' ? 'Public' : 'Private' });
  if (f.admit) out.push({ key: 'admit', label: { under10: 'Admit rate under 10%', '10to30': 'Admit rate 10-30%', over30: 'Admit rate over 30%' }[f.admit] });
  if (f.rank !== null) out.push({ key: 'rank', label: `QS top ${f.rank}` });
  if (f.ielts !== null) out.push({ key: 'ielts', label: `IELTS ${f.ielts} accepted` });
  if (f.sat !== null) out.push({ key: 'sat', label: `SAT ${f.sat} in range` });
  return out;
}

function Select<T extends string | number>({ label, value, options, onChange }: { label: string; value: T | null; options: { v: T; l: string }[]; onChange: (v: T | null) => void }) {
  return (
    <label className="flex flex-col gap-1 text-xs font-medium text-muted">
      {label}
      <select
        className="h-9 rounded-lg border border-line bg-surface px-2 text-sm text-ink"
        value={value === null ? '' : String(value)}
        onChange={(e) => {
          const raw = e.target.value;
          if (!raw) return onChange(null);
          const o = options.find((x) => String(x.v) === raw);
          onChange(o ? o.v : null);
        }}
      >
        <option value="">Any</option>
        {options.map((o) => <option key={String(o.v)} value={String(o.v)}>{o.l}</option>)}
      </select>
    </label>
  );
}

export function UniversityExplorer({
  rows, fields, initialQuery = '', initialFilters, detailBase, top, banner, shortlist, mode = 'free',
}: {
  rows: UniRow[];
  fields: string[];
  initialQuery?: string;
  initialFilters?: Partial<Filters>;
  detailBase: string;
  /** Shown when there is no query and no filter (PDF 6a "Top universities for your target"). */
  top?: React.ReactNode;
  banner?: React.ReactNode;
  /** Paid view: a Shortlist button per row that adds the university to the board. */
  shortlist?: { action: (universityId: string, programmeId: string) => Promise<void>; onBoard: string[] };
  mode?: 'free' | 'paid';
}) {
  const [q, setQ] = useState(initialQuery);
  const [f, setF] = useState<Filters>({ ...EMPTY, ...initialFilters });
  const [open, setOpen] = useState(mode === 'paid');
  const [limit, setLimit] = useState(20);
  const active = chips(f);
  const searching = q.trim().length > 0 || active.length > 0;
  const results = useMemo(() => rows.filter((r) => matches(r, q.trim(), f)).sort((a, b) => (a.qsRank ?? 999) - (b.qsRank ?? 999)), [rows, q, f]);
  const set = <K extends keyof Filters>(k: K, v: Filters[K]) => setF((x) => ({ ...x, [k]: v }));
  const countries = [...new Set(rows.map((r) => r.country))];

  const panel = (
    <div className={cn('grid gap-3 sm:grid-cols-2', mode === 'paid' ? 'lg:grid-cols-1' : 'lg:grid-cols-4')}>
      <div className="flex flex-col gap-1 text-xs font-medium text-muted">
        Location
        <div className="flex flex-wrap gap-1.5">
          {countries.map((c) => {
            const on = f.country.includes(c);
            return (
              <button key={c} type="button" onClick={() => set('country', on ? f.country.filter((x) => x !== c) : [...f.country, c])}
                className={cn('rounded-full border px-2.5 py-1 text-xs', on ? 'border-brand-600 bg-brand-50 text-brand-700' : 'border-line bg-surface text-muted hover:text-ink')}>
                {rows.find((r) => r.country === c)?.countryName}
              </button>
            );
          })}
        </div>
      </div>
      {SHOW_COSTS && <Select label="Tuition" value={f.maxTuition} options={TUITION_STEPS.map((t) => ({ v: t.v, l: t.l }))} onChange={(v) => set('maxTuition', v)} />}
      <Select label="Course" value={f.field} options={fields.map((x) => ({ v: x, l: fieldLabel(x) }))} onChange={(v) => set('field', v)} />
      <Select label="University type" value={f.type} options={[{ v: 'public' as const, l: 'Public' }, { v: 'private' as const, l: 'Private' }]} onChange={(v) => set('type', v)} />
      <Select label="Admission rate" value={f.admit} options={[{ v: 'under10' as const, l: 'Under 10%' }, { v: '10to30' as const, l: '10 to 30%' }, { v: 'over30' as const, l: 'Over 30%' }]} onChange={(v) => set('admit', v)} />
      <Select label="Global rank (QS)" value={f.rank} options={[{ v: 50 as const, l: 'Top 50' }, { v: 100 as const, l: 'Top 100' }, { v: 200 as const, l: 'Top 200' }]} onChange={(v) => set('rank', v)} />
      <Select label="English score (IELTS)" value={f.ielts} options={[6, 6.5, 7, 7.5].map((v) => ({ v, l: `My IELTS is ${v}` }))} onChange={(v) => set('ielts', v)} />
      <Select label="SAT score" value={f.sat} options={[1200, 1300, 1400, 1450, 1500, 1550].map((v) => ({ v, l: `My SAT is ${v}` }))} onChange={(v) => set('sat', v)} />
    </div>
  );

  return (
    <div className={cn(mode === 'paid' && 'lg:grid lg:grid-cols-[240px_1fr] lg:gap-6')}>
      {mode === 'paid' && (
        <aside className="mb-4 hidden lg:block">
          <Card className="sticky top-20 p-4">
            <p className="mb-3 text-sm font-semibold text-ink">Filters</p>
            {panel}
            {active.length > 0 && <Button variant="link" size="sm" className="mt-3 px-0" onClick={() => setF(EMPTY)}>Clear filters</Button>}
          </Card>
        </aside>
      )}
      <div className="min-w-0">
        <form className="flex gap-2" onSubmit={(e) => e.preventDefault()} role="search">
          <div className="relative min-w-0 flex-1">
            <Search className="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-subtle" />
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Type a university, course or country"
              aria-label="Search universities"
              className="h-10 w-full rounded-lg border border-line bg-surface pr-3 pl-9 text-sm text-ink placeholder:text-subtle"
            />
          </div>
          <Button type="button" variant="secondary" onClick={() => setOpen((o) => !o)} className={cn(mode === 'paid' && 'lg:hidden')} aria-expanded={open}>
            <SlidersHorizontal />Filters{active.length ? ` · ${active.length}` : ''}
          </Button>
        </form>

        {open && <Card className={cn('mt-3 p-4', mode === 'paid' && 'lg:hidden')}>{panel}</Card>}

        {active.length > 0 && (
          <div className="mt-3 flex flex-wrap items-center gap-2">
            {active.map((c) => (
              <button key={`${c.key}-${c.value ?? ''}`} type="button"
                onClick={() => (c.key === 'country' ? set('country', f.country.filter((x) => x !== c.value)) : set(c.key, null as never))}
                className="inline-flex items-center gap-1 rounded-full border border-brand-200 bg-brand-50 px-2.5 py-1 text-xs font-medium text-brand-700">
                {c.label}<X className="size-3" />
              </button>
            ))}
            <button type="button" className="text-xs text-muted underline-offset-2 hover:underline" onClick={() => setF(EMPTY)}>Clear all</button>
          </div>
        )}

        {!searching && top}

        {searching && (
          <div className="mt-4">
            {results.length === 0 ? (
              <EmptyState title="No universities match" description="Loosen a filter or try another course or country." action={<Button variant="secondary" onClick={() => { setF(EMPTY); setQ(''); }}>Clear search</Button>} />
            ) : (
              <Card className="divide-y divide-line">
                {results.slice(0, limit).map((r, i) => (
                  <div key={r.id} className="flex flex-col gap-2 p-4 sm:flex-row sm:items-center sm:justify-between">
                    <div className="min-w-0">
                      <p className="font-semibold text-ink">
                        <span className="mr-1 text-subtle">{i + 1}.</span>
                        <Link href={`${detailBase}/${r.id}`} className="hover:text-brand-700 hover:underline">{r.shortName}</Link>
                        <span className="ml-2 text-xs font-normal text-subtle">{r.qsRank ? `QS #${r.qsRank}` : ''}</span>
                      </p>
                      <p className="mt-0.5 text-sm text-muted">
                        {f.field ? fieldLabel(f.field) : r.defaultProgramme ?? fieldLabel(r.fields[0] ?? '')} · {r.satLabel} · Deadline {r.deadlineLabel} · {r.city}, {r.countryName}
                      </p>
                      <p className="mt-0.5 text-xs text-subtle">{SHOW_COSTS ? `Tuition ${r.tuitionLabel} · ` : ''}{r.acceptancePct !== null ? `${r.acceptancePct < 1 ? '<1' : r.acceptancePct}% admitted` : 'admit rate not published'}{r.ielts ? ` · IELTS ${r.ielts}` : ''}</p>
                    </div>
                    <div className="flex shrink-0 gap-2">
                      {shortlist && (shortlist.onBoard.includes(r.id)
                        ? <span className="inline-flex h-8 items-center rounded-lg bg-ink px-3 text-sm font-medium text-white">Shortlisted ✓</span>
                        : <ActionButton size="sm" action={() => shortlist.action(r.id, r.defaultProgrammeId)}>Shortlist</ActionButton>)}
                      <Link href={`${detailBase}/${r.id}`} className="inline-flex h-8 items-center rounded-lg border border-line bg-surface px-3 text-sm font-medium text-ink shadow-sm hover:bg-surface-muted">View details</Link>
                    </div>
                  </div>
                ))}
              </Card>
            )}
            <div className="mt-3 flex items-center justify-between text-xs text-subtle">
              <span>Showing {Math.min(limit, results.length)} of {results.length}{results.length !== rows.length ? ` (${rows.length} in the catalogue)` : ''}</span>
              {results.length > limit && <Button variant="link" size="sm" onClick={() => setLimit((l) => l + 20)}>Show more</Button>}
            </div>
          </div>
        )}
        {banner}
      </div>
    </div>
  );
}
