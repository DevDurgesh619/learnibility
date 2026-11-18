/** Shared number formats. Charts take a ValueFormat key (functions cannot cross the server/client boundary). */
export type ValueFormat = 'percent' | 'decimal' | 'hours' | 'inr' | 'number';

const inr = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 });

export function formatValue(v: number, format: ValueFormat = 'number'): string {
  switch (format) {
    case 'percent': return `${Math.round(v * 100)}%`;
    case 'decimal': return v.toFixed(2);
    case 'hours': return `${Math.round(v * 10) / 10} h`;
    case 'inr': return inr.format(v);
    default: return new Intl.NumberFormat('en-IN').format(v);
  }
}

export const formatInr = (v: number) => formatValue(v, 'inr');
export const formatHours = (v: number) => formatValue(v, 'hours');
export const formatPercent = (v: number) => formatValue(v, 'percent');
