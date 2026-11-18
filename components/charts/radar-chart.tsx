'use client';

import { PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart as RRadarChart, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { formatValue, type ValueFormat } from '@/lib/format';
import { CHART_COLORS } from './colors';

export interface RadarSeries {
  key: string;
  label: string;
  color?: string;
}

/**
 * Mastery radar: one axis per subject/chapter/skill, values 0..max.
 * data: [{ axis: 'Algebra', you: 0.8, target: 1 }, ...]
 */
export function RadarChart({
  data, series, max = 1, height = 280, format = 'percent',
}: {
  data: Array<{ axis: string } & Record<string, number | string>>;
  series: RadarSeries[];
  max?: number;
  height?: number;
  format?: ValueFormat;
}) {
  return (
    <div style={{ height }} className="w-full">
      <ResponsiveContainer width="100%" height="100%">
        <RRadarChart data={data} outerRadius="75%">
          <PolarGrid stroke="var(--color-line)" />
          <PolarAngleAxis dataKey="axis" tick={{ fill: 'var(--color-muted)', fontSize: 12 }} />
          <PolarRadiusAxis domain={[0, max]} tick={false} axisLine={false} />
          {series.map((s, i) => (
            <Radar
              key={s.key}
              name={s.label}
              dataKey={s.key}
              stroke={s.color ?? CHART_COLORS[i % CHART_COLORS.length]}
              fill={s.color ?? CHART_COLORS[i % CHART_COLORS.length]}
              fillOpacity={i === 0 ? 0.25 : 0.06}
              strokeWidth={2}
              strokeDasharray={i === 0 ? undefined : '4 4'}
            />
          ))}
          <Tooltip formatter={(v) => formatValue(Number(v), format)} contentStyle={{ borderRadius: 8, borderColor: 'var(--color-line)', fontSize: 12 }} />
          {series.length > 1 && <Legend iconType="circle" wrapperStyle={{ fontSize: 12 }} />}
        </RRadarChart>
      </ResponsiveContainer>
    </div>
  );
}
