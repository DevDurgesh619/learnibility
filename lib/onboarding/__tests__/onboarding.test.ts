import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { DEFAULT_LADDER, nextDifficulty, runGroup } from '../ladder';
import { bandFor, scoreOnboarding, type OnboardingResponses } from '../score';
import type { OnboardingAcademicItem, OnboardingFormFile, OnboardingSurveyItem } from '../../types/onboarding';

const DIR = path.join(process.cwd(), 'data', 'questions', 'onboarding');
const load = (formId: string) => JSON.parse(fs.readFileSync(path.join(DIR, `${formId}.json`), 'utf8')) as OnboardingFormFile;
const formIds = fs.readdirSync(DIR).filter((f) => f.startsWith('onb-')).map((f) => f.replace(/\.json$/, ''));
const partA = (file: OnboardingFormFile, group?: string) =>
  file.items.filter((it): it is OnboardingAcademicItem => it.part === 'A' && (!group || (it as OnboardingAcademicItem).group === group));

describe('ladder', () => {
  it('starts at D2, drops after a miss, climbs after two hits, and stays within D1-D3', () => {
    expect(nextDifficulty([])).toBe('D2');
    expect(nextDifficulty([{ difficulty: 'D2', correct: false }])).toBe('D1');
    expect(nextDifficulty([{ difficulty: 'D1', correct: false }, { difficulty: 'D1', correct: false }])).toBe('D1');
    expect(nextDifficulty([{ difficulty: 'D2', correct: true }])).toBe('D2');
    expect(nextDifficulty([{ difficulty: 'D2', correct: true }, { difficulty: 'D2', correct: true }])).toBe('D3');
    const fourHits = Array.from({ length: 4 }, () => ({ difficulty: 'D3' as const, correct: true }));
    expect(nextDifficulty(fourHits)).toBe(DEFAULT_LADDER.ceiling);
  });

  it('shows exactly one item per slot, in slot order, for every group of every form', () => {
    expect(formIds.length).toBe(27);
    for (const id of formIds) {
      const file = load(id);
      for (const g of file.form.scoring.groups) {
        const items = partA(file, g.group);
        expect(items.length, `${id} ${g.group}`).toBe(21);
        let flip = false;
        const path = runGroup(items, () => (flip = !flip));
        expect(path.map((p) => p.item.slot)).toEqual([1, 2, 3, 4, 5, 6, 7, 8]);
      }
    }
  });

  it('a strong student reaches D3 and a struggling student never leaves D1-D2', () => {
    const items = partA(load('onb-cbse-g9-none'), 'maths');
    const strong = runGroup(items, () => true).map((p) => p.item.difficulty);
    expect(strong[0]).toBe('D2');
    expect(strong.slice(2)).toContain('D3');
    const weak = runGroup(items, () => false).map((p) => p.item.difficulty);
    expect(weak[0]).toBe('D2');
    expect(weak.slice(1).every((d) => d === 'D1')).toBe(true);
  });
});

describe('bands', () => {
  it('uses the brief cut-offs: <45, 45-64, 65-79, >=80', () => {
    expect(bandFor(44)).toBe('below_avg');
    expect(bandFor(45)).toBe('average');
    expect(bandFor(64)).toBe('average');
    expect(bandFor(65)).toBe('above_avg');
    expect(bandFor(79)).toBe('above_avg');
    expect(bandFor(80)).toBe('excellent');
  });
});

function simulate(file: OnboardingFormFile, correct: (it: OnboardingAcademicItem) => boolean): OnboardingResponses {
  const academic = file.form.scoring.groups.flatMap((g) =>
    runGroup(partA(file, g.group), correct).map((p) => ({ questionId: p.item.id, correct: p.correct, secondsTaken: 40, confidence: 3 as const })),
  );
  const reasoning = file.items.filter((it) => it.part === 'B').map((it) => ({ questionId: it.id, answer: String(it.answer), secondsTaken: 20 }));
  const survey = file.items
    .filter((it): it is OnboardingSurveyItem => it.part === 'C' || it.part === 'P')
    .map((it) => ({ questionId: it.id, value: it.riasec ? (it.riasec === 'I' ? 5 : 2) : (it.options?.[0]?.value ?? 3) }));
  return { academic, reasoning, survey };
}

describe('scoreOnboarding', () => {
  const ctx = { learnerId: 'stu-test', nowUtc: '2026-11-18T00:00:00Z' };

  it('an all-correct student is excellent everywhere with no suspected gaps', () => {
    const file = load('onb-cbse-g9-none');
    const res = scoreOnboarding(file, simulate(file, () => true), ctx);
    expect(res.groups).toHaveLength(4);
    for (const g of res.groups) {
      expect(g.itemsSeen).toBe(8);
      expect(g.band).toBe('excellent');
    }
    expect(res.suspectedGaps).toHaveLength(0);
    expect(res.reasoning.numerical).toBe(100);
    expect(res.riasec.code[0]).toBe('I');
  });

  it('an all-wrong student is below average and every miss becomes a suspected gap', () => {
    const file = load('onb-ib-g12-commerce');
    const res = scoreOnboarding(file, simulate(file, () => false), ctx);
    expect(res.groups).toHaveLength(3);
    expect(res.groups.every((g) => g.band === 'below_avg' && g.percent === 0)).toBe(true);
    expect(res.suspectedGaps).toHaveLength(3 * 8);
    expect(new Set(res.suspectedGaps.map((g) => g.status))).toEqual(new Set(['suspected']));
    // prerequisite misses are G1 (no recall / prerequisite)
    const preIds = new Set(partA(file).filter((it) => it.half === 'prerequisite').map((it) => it.id));
    expect(res.suspectedGaps.filter((g) => preIds.has(g.evidenceItemIds[0])).every((g) => g.code === 'G1')).toBe(true);
  });

  it('flags G9 for confident wrong answers and seeds the profile at low confidence', () => {
    const file = load('onb-cambridge-g11-science');
    const r = simulate(file, (it) => it.slot % 2 === 0);
    r.academic = r.academic.map((a) => ({ ...a, confidence: 5 as const }));
    const res = scoreOnboarding(file, r, ctx);
    expect(res.suspectedGaps.length).toBeGreaterThan(0);
    expect(res.suspectedGaps.every((g) => g.secondaryFlags.includes('G9'))).toBe(true);
    const ids = new Set(res.profile.map((p) => p.paramId));
    for (const p of ['p1', 'p3', 'p5', 'p278', 'p279', 'p61', 'p62', 'p63', 'p64', 'p200', 'p30']) expect(ids.has(p), p).toBe(true);
    expect(res.profile.find((p) => p.paramId === 'p278')?.confidence).toBe('low');
    // the parent's answer wins where both were asked
    expect(res.profile.filter((p) => p.paramId === 'p21')).toHaveLength(1);
  });
});
