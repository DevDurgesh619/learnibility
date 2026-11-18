'use client';

import { Bar, BarChart as RBarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { formatValue, type ValueFormat } from '@/lib/format';
import { CHART_COLORS } from './colors';

/** Grouped or stacked bars: hours per subject, rupees per plan, gaps per code ... */
export function BarChart({
  data, series, height = 260, stacked = false, format = 'number',
}: {
  data: Array<{ x: string } & Record<string, number | string>>;
  series: { key: string; label: string; color?: string }[];
  height?: number;
  stacked?: boolean;
  format?: ValueFormat;
}) {
  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <RBarChart data={data} margin={{ top: 8, right: 12, bottom: 0, left: -12 }}>
          <CartesianGrid stroke="var(--color-line)" vertical={false} />
          <XAxis dataKey="x" tick={{ fill: 'var(--color-subtle)', fontSize: 12 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fill: 'var(--color-subtle)', fontSize: 12 }} axisLine={false} tickLine={false} tickFormatter={(v) => formatValue(Number(v), format)} />
          <Tooltip formatter={(v) => formatValue(Number(v), format)} cursor={{ fill: 'var(--color-surface-muted)' }} contentStyle={{ borderRadius: 8, borderColor: 'var(--color-line)', fontSize: 12 }} />
          {series.map((s, i) => (
            <Bar key={s.key} dataKey={s.key} name={s.label} fill={s.color ?? CHART_COLORS[i % CHART_COLORS.length]} radius={[4, 4, 0, 0]} stackId={stacked ? 'a' : undefined} maxBarSize={40} />
          ))}
          {series.length > 1 && <Legend iconType="circle" wrapperStyle={{ fontSize: 12 }} />}
        </RBarChart>
      </ResponsiveContainer>
    </div>
  );
}
