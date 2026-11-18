import type { ReactNode } from 'react';
import { CheckCircle2 } from 'lucide-react';

/** Checkbox chips posted as list fields for saveTutorPrefs (`list=<key>`, `l.<key>=<value>`). */
export function CheckChips({ name, options, selected, type = 'checkbox' }: { name: string; options: [string, string][]; selected: string[]; type?: 'checkbox' | 'radio' }) {
  return (
    <div className="flex flex-wrap gap-2">
      {type === 'checkbox' && <input type="hidden" name="list" value={name} />}
      {options.map(([v, label]) => (
        <label key={v} className="relative cursor-pointer">
          <input type={type} name={type === 'checkbox' ? `l.${name}` : `f.${name}`} value={v} defaultChecked={selected.includes(v)} className="peer sr-only" />
          <span className="block rounded-full border border-line bg-surface px-3 py-1 text-sm text-muted peer-checked:border-brand-500 peer-checked:bg-brand-50 peer-checked:font-medium peer-checked:text-brand-700 peer-focus-visible:ring-2 peer-focus-visible:ring-brand-400">{label}</span>
        </label>
      ))}
    </div>
  );
}

export function Saved({ show, children = 'Saved.' }: { show?: string; children?: ReactNode }) {
  if (!show) return null;
  return <p className="mb-4 flex items-center gap-2 rounded-lg bg-success-50 px-3 py-2 text-sm text-success-700"><CheckCircle2 className="size-4" />{children}</p>;
}

export const fieldClass = 'w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm text-ink focus:border-brand-400 focus:outline-none';

/** Availability grid bands (tutor HTML 8c, 1e). */
export const BANDS: { key: string; label: string; start: string; end: string }[] = [
  { key: 'm', label: '7–10 am', start: '07:00', end: '10:00' },
  { key: 'd', label: '10–1', start: '10:00', end: '13:00' },
  { key: 'a', label: '4–7 pm', start: '16:00', end: '19:00' },
  { key: 'e', label: '7–10 pm', start: '19:00', end: '22:00' },
];
