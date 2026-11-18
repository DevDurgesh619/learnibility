import { describe, expect, it } from 'vitest';
import { formatValue } from './format';

describe('formatValue', () => {
  it('formats each kind', () => {
    expect(formatValue(0.789, 'percent')).toBe('79%');
    expect(formatValue(0.789, 'decimal')).toBe('0.79');
    expect(formatValue(7.46, 'hours')).toBe('7.5 h');
    expect(formatValue(125000, 'inr')).toBe('₹1,25,000');
    expect(formatValue(180015)).toBe('1,80,015');
  });
});
