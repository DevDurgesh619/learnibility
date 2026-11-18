import { describe, expect, it } from 'vitest';
import parameters from '@/data/profile/parameters.json';
import methods from '@/data/profile/collection-methods.json';
import tiers from '@/data/profile/sensitivity-tiers.json';
import { parseParamId } from './ids';
import { CADENCES, PROFILE_SECTIONS, SOURCE_METHODS, TIERS, type DataFile, type ProfileParameter } from './types';

const params = (parameters as DataFile<ProfileParameter>).items;

describe('data/profile/parameters.json', () => {
  it('has the data-file envelope', () => {
    expect(parameters.schemaVersion).toBe(1);
    expect(parameters.generatedBy).toBe('scripts/foundations/import-430.py');
  });

  it('holds parameters p1..p430 in order with valid fields', () => {
    expect(params).toHaveLength(430);
    params.forEach((p, i) => {
      expect(p.id).toBe(`p${i + 1}`);
      expect(parseParamId(p.id)).toBe(p.number);
      expect(PROFILE_SECTIONS).toContain(p.section);
      expect(TIERS).toContain(p.tier);
      expect(CADENCES).toContain(p.cadence);
      expect(p.methods.length).toBeGreaterThan(0);
      p.methods.forEach((m) => expect(SOURCE_METHODS).toContain(m));
      expect(p.name.length).toBeGreaterThan(0);
    });
  });

  it('matches the tier counts in the Sensitivity Tiers sheet', () => {
    const count = (t: string) => params.filter((p) => p.tier === t).length;
    for (const t of tiers.items) expect(count(t.tier)).toBe(t.count);
    expect([count('T1'), count('T2'), count('T3'), count('C')]).toEqual([300, 94, 33, 3]);
  });

  it('keeps provenance: 277 existing and 153 proposed', () => {
    expect(params.filter((p) => p.origin === 'existing_277')).toHaveLength(277);
    expect(params.filter((p) => p.origin === 'proposed_v2')).toHaveLength(153);
  });

  it('lists collection methods M1..M20', () => {
    expect(methods.items.map((m) => m.code)).toEqual(SOURCE_METHODS);
  });
});
