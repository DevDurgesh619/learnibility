'use client';

import { usePathname, useRouter, useSearchParams } from 'next/navigation';

/** A select that writes its value to one URL query param (chapter filter, student picker ...). */
export function QuerySelect({
  param, value, options, label, allLabel,
}: {
  param: string;
  value: string;
  options: { value: string; label: string }[];
  label: string;
  /** When set, adds a first option with an empty value that clears the param. */
  allLabel?: string;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const params = useSearchParams();
  return (
    <label className="flex min-w-0 items-center gap-2 text-sm text-muted">
      <span className="shrink-0">{label}</span>
      <select
        className="h-9 min-w-0 max-w-full rounded-lg border border-line bg-surface px-2 text-sm text-ink shadow-sm focus:border-brand-400 focus:outline-none"
        value={value}
        onChange={(e) => {
          const next = new URLSearchParams(params.toString());
          if (e.target.value) next.set(param, e.target.value);
          else next.delete(param);
          router.push(`${pathname}?${next.toString()}`);
        }}
      >
        {allLabel !== undefined && <option value="">{allLabel}</option>}
        {options.map((o) => (
          <option key={o.value} value={o.value}>{o.label}</option>
        ))}
      </select>
    </label>
  );
}
