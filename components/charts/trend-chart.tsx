'use client';

import { CartesianGrid, Legend, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { formatValue, type ValueFormat } from '@/lib/format';
import { CHART_COLORS } from './colors';

export interface TrendSeries {
  key: string;
  label: string;
  color?: string;
}

/**
 * Trend over time (learning rate, LRS, MCI, mock scores ...).
 * data: [{ x: 'Week 1', lrs: 0.62, mci: 0.55 }, ...]
 */
export function TrendChart({
  data, series, height = 260, domain = [0, 1], target, format = 'decimal',
}: {
  data: Array<{ x: string } & Record<string, number | string | null>>;
  series: TrendSeries[];
  height?: number;
  domain?: [number, number];
  target?: { value: number; label: string };
  format?: ValueFormat;
}) {
  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 8, right: 12, bottom: 0, left: -12 }}>
          <CartesianGrid stroke="var(--color-line)" vertical={false} />
          <XAxis dataKey="x" tick={{ fill: 'var(--color-subtle)', fontSize: 12 }} axisLine={false} tickLine={false} />
          <YAxis domain={domain} tick={{ fill: 'var(--color-subtle)', fontSize: 12 }} axisLine={false} tickLine={false} tickFormatter={(v) => formatValue(Number(v), format)} />
          <Tooltip formatter={(v) => formatValue(Number(v), format)} contentStyle={{ borderRadius: 8, borderColor: 'var(--color-line)', fontSize: 12 }} />
          {target && <ReferenceLine y={target.value} stroke="var(--color-subtle)" strokeDasharray="4 4" label={{ value: target.label, fill: 'var(--color-subtle)', fontSize: 11, position: 'insideTopRight' }} />}
          {series.map((s, i) => (
            <Line key={s.key} type="monotone" dataKey={s.key} name={s.label} stroke={s.color ?? CHART_COLORS[i % CHART_COLORS.length]} strokeWidth={2} dot={{ r: 3 }} activeDot={{ r: 5 }} connectNulls />
          ))}
          {series.length > 1 && <Legend iconType="circle" wrapperStyle={{ fontSize: 12 }} />}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
