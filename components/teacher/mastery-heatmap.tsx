import Link from 'next/link';
import type { Level } from '@/lib/types';
import { LEVEL_LABEL } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

export interface HeatmapColumn {
  id: string;
  /** Short label shown in the header, e.g. "1.2". */
  short: string;
  /** Full subtopic name for the tooltip. */
  name: string;
  chapterName: string;
}

export interface HeatmapCell {
  level: Level;
  /** 0 to 1. */
  pMastery: number;
}

export interface HeatmapRow {
  id: string;
  name: string;
  /** Average mastery across the shown columns, 0 to 1 (undefined when nothing tested). */
  average?: number;
  cells: Record<string, HeatmapCell | undefined>;
}

/** Level → cell colour. L0 to L2 warm, L3 to L4 amber/blue, L5 green. Untested is hatched grey. */
export const LEVEL_CELL: Record<Level, string> = {
  0: 'bg-rose-500 text-white',
  1: 'bg-rose-300 text-rose-950',
  2: 'bg-orange-200 text-orange-950',
  3: 'bg-amber-100 text-amber-900',
  4: 'bg-sky-200 text-sky-950',
  5: 'bg-emerald-400 text-emerald-950',
};

export function LevelLegend({ className }: { className?: string }) {
  return (
    <div className={cn('flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-muted', className)}>
      {([0, 1, 2, 3, 4, 5] as Level[]).map((l) => (
        <span key={l} className="inline-flex items-center gap-1.5">
          <span className={cn('inline-block size-3 rounded-sm', LEVEL_CELL[l])} />
          {LEVEL_LABEL[l]}
        </span>
      ))}
      <span className="inline-flex items-center gap-1.5">
        <span className="inline-block size-3 rounded-sm border border-dashed border-line bg-surface-muted" />
        Not tested yet
      </span>
    </div>
  );
}

/**
 * Students × subtopics mastery heatmap. Server component; each row links to the student's page.
 * Sticky first column so it scrolls sideways on phones.
 */
export function MasteryHeatmap({ rows, columns, studentHref }: { rows: HeatmapRow[]; columns: HeatmapColumn[]; studentHref: (id: string) => string }) {
  return (
    <div className="w-full overflow-x-auto">
      <table className="border-separate border-spacing-1 text-xs">
        <thead>
          <tr>
            <th className="sticky left-0 z-10 min-w-36 bg-surface pr-2 text-left text-xs font-medium text-subtle">Student</th>
            <th className="px-1 text-center font-medium text-subtle" title="Average mastery across the subtopics shown">Avg</th>
            {columns.map((c) => (
              <th key={c.id} title={`${c.chapterName} · ${c.name}`} className="h-8 min-w-9 px-0.5 text-center font-medium text-subtle">
                {c.short}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id}>
              <th scope="row" className="sticky left-0 z-10 bg-surface pr-2 text-left font-medium">
                <Link href={studentHref(r.id)} className="block truncate text-sm text-ink hover:text-brand-700 hover:underline">
                  {r.name}
                </Link>
              </th>
              <td className="px-1 text-center text-muted tabular-nums">{r.average === undefined ? '–' : `${Math.round(r.average * 100)}%`}</td>
              {columns.map((c) => {
                const cell = r.cells[c.id];
                return (
                  <td key={c.id} className="p-0">
                    {cell ? (
                      <div
                        title={`${r.name} · ${c.name}: ${LEVEL_LABEL[cell.level]}, ${Math.round(cell.pMastery * 100)}% mastery`}
                        className={cn('flex h-8 min-w-9 items-center justify-center rounded font-semibold tabular-nums', LEVEL_CELL[cell.level])}
                      >
                        L{cell.level}
                      </div>
                    ) : (
                      <div title={`${r.name} · ${c.name}: not tested yet`} className="h-8 min-w-9 rounded border border-dashed border-line bg-surface-muted" />
                    )}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
