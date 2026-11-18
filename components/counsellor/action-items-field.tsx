'use client';

import { Plus, Trash2 } from 'lucide-react';
import { useState } from 'react';

/** Editable action-item rows for a session note; posts itemTitle / itemDue pairs. */
export function ActionItemsField({ initial, defaultDue }: { initial: { title: string; dueOn: string }[]; defaultDue: string }) {
  const [rows, setRows] = useState(initial.length ? initial : [{ title: '', dueOn: defaultDue }]);
  const update = (i: number, patch: Partial<{ title: string; dueOn: string }>) => setRows((r) => r.map((x, j) => (j === i ? { ...x, ...patch } : x)));
  return (
    <div className="space-y-2">
      {rows.map((r, i) => (
        <div key={i} className="flex flex-col gap-2 rounded-lg border border-line bg-surface p-2 sm:flex-row sm:items-center sm:border-0 sm:p-0">
          <input name="itemTitle" value={r.title} onChange={(e) => update(i, { title: e.target.value })} placeholder="Action item, e.g. Finish the free SQL basics course"
            className="h-10 min-w-0 flex-1 rounded-lg border border-line bg-surface px-3 text-sm text-ink" aria-label={`Action item ${i + 1}`} />
          <div className="flex gap-2">
            <input type="date" name="itemDue" value={r.dueOn} onChange={(e) => update(i, { dueOn: e.target.value })}
              className="h-10 flex-1 rounded-lg border border-line bg-surface px-3 text-sm text-ink sm:w-40 sm:flex-none" aria-label={`Due date ${i + 1}`} />
            <button type="button" onClick={() => setRows((x) => x.filter((_, j) => j !== i))} className="inline-flex size-10 items-center justify-center rounded-lg text-muted hover:bg-surface-muted hover:text-danger-700" aria-label="Remove action item">
              <Trash2 className="size-4" />
            </button>
          </div>
        </div>
      ))}
      <button type="button" onClick={() => setRows((x) => [...x, { title: '', dueOn: defaultDue }])} className="inline-flex items-center gap-1 text-sm font-medium text-brand-700 hover:underline">
        <Plus className="size-4" />Add action item
      </button>
    </div>
  );
}
