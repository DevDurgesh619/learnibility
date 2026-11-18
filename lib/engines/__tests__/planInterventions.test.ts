import { describe, expect, it } from 'vitest';
import fx from '../__fixtures__/maths8.json';
import { diagnoseSubtopic } from '../diagnoseGaps';
import { INTERVENTIONS, deviceCheckText, moneyCheckText, planInterventions, retestRuleText, type PlanGap } from '../planInterventions';
import { pathFor, responsesFrom, subtopics } from './helpers';

const gc = fx.gapCalculator;
const NOW = '2026-11-18T04:30:00.000Z';
const sub = subtopics.find((s) => s.id === gc.subtopicId)!;
const d = diagnoseSubtopic(pathFor(gc.subtopicId), responsesFrom(gc.subtopicId, gc.results as number[], { confidenceWrong: 4 }), sub, {
  learnerId: gc.learnerId, band: 'average', weeklyHours: 3, signals: { [sub.id]: { wordProblemPattern: false } },
});
const gap: PlanGap = { ...d.gap!, chapterId: d.chapterId };

describe('interventions catalogue', () => {
  it('has 3 ranked rows for each of G1-G10 plus 2 ANY rows, all free except ANY', () => {
    expect(INTERVENTIONS).toHaveLength(32);
    for (const i of INTERVENTIONS) if (i.gapCode !== 'ANY') expect(i.money).toBe('free');
    expect(INTERVENTIONS.find((i) => i.id === 'int-any-1')!.inrPerMonth).toEqual({ min: 2000, max: 6000 });
  });
});

describe('planInterventions: Gap Calculator section 4', () => {
  const plan = planInterventions([gap], { p178: 0, p193: 'adequate' }, { now: NOW, weeklyHours: 3 });
  const g = plan.gaps[0];
  it('ranks the same three free interventions', () => {
    expect(g.steps.map((s) => s.name)).toEqual(gc.expected.planNames);
    expect(g.steps.every((s) => s.money === 'free')).toBe(true);
  });
  it('gives the same add-on, money check and re-test rule', () => {
    expect(g.addOnText).toBe(gc.expected.addOns);
    expect(g.addOns[0].interventionId).toBe('int-g9-1');
    expect(g.moneyCheck).toBe(gc.expected.moneyCheck);
    expect(g.deviceCheck).toBe('Video / app options usable.');
    expect(g.retestRule).toContain('after the planned 0.7 weeks');
    expect(g.weeks).toBe(0.7);
    expect(g.retestDateUtc).toBe('2026-11-25T04:30:00.000Z');
    expect(g.retentionProbeDateUtc).toBe('2026-12-02T04:30:00.000Z');
  });
  it('does not recommend paid tuition for one chapter', () => {
    expect(plan.paidTuition.recommended).toBe(false);
    expect(plan.totalInrPerMonth).toEqual({ min: 0, max: 0 });
    expect(plan.optionalApp).toBeNull();
  });
});

describe('paid tuition rule (ANY-1)', () => {
  const g2: PlanGap = { ...gap, id: 'gap_x_2', subtopicId: 'cbse-g8-maths-ch02-st1', chapterId: 'cbse-g8-maths-ch02', code: 'G1', size: 5, hoursToClose: 7.7 };
  it('needs 2+ chapters and 3 weeks of failed free plan', () => {
    expect(planInterventions([gap, g2], {}, { now: NOW, freePlanWeeks: 1 }).paidTuition.recommended).toBe(false);
    const p = planInterventions([gap, g2], { p178: 'medium' }, { now: NOW, freePlanWeeks: 3 });
    expect(p.paidTuition.recommended).toBe(true);
    expect(p.paidTuition.affordable).toBe(true);
    expect(p.totalInrPerMonth).toEqual({ min: 2000, max: 6000 });
    expect(p.gaps[0].code).toBe('G1'); // prerequisites first
    expect(p.optionalApp?.interventionId).toBe('int-any-2');
  });
  it('or a parent request', () => {
    const p = planInterventions([gap], {}, { now: NOW, parentRequestedTuition: true });
    expect(p.paidTuition.recommended).toBe(true);
    expect(p.paidTuition.affordable).toBe(false);
  });
  it('closed gaps are ignored; chapter comes from chapterOf', () => {
    const p = planInterventions([{ ...gap, chapterId: undefined }, { ...g2, status: 'closed' }], [], { now: NOW, chapterOf: { [gap.subtopicId]: 'cbse-g8-maths-ch01' } });
    expect(p.gaps).toHaveLength(1);
    expect(p.gaps[0].chapterId).toBe('cbse-g8-maths-ch01');
    expect(p.gaps[0].weeks).toBeNull();
  });
});

describe('device and money texts', () => {
  it('drops video/app interventions without a device', () => {
    const g1: PlanGap = { ...gap, code: 'G1' };
    const p = planInterventions([g1], { p193: 'none' }, { now: NOW });
    expect(p.gaps[0].steps.map((s) => s.interventionId)).toEqual(['int-g1-1', 'int-g1-3']);
    expect(p.gaps[0].deviceCheck).toBe(deviceCheckText(false));
    expect(planInterventions([g1], { p193: false }, { now: NOW }).gaps[0].steps).toHaveLength(2);
  });
  it('money texts follow C66', () => {
    expect(moneyCheckText(3000, 5)).toContain('gap is deep');
    expect(moneyCheckText(3000, 2)).toContain('gap is shallow');
    expect(retestRuleText(null)).toContain('planned time');
  });
  it('reads budget from profile values in several shapes', () => {
    const pv = [{ paramId: 'p178', value: '₹4,000', asOfUtc: NOW, tier: 'T2' }];
    expect(planInterventions([gap], pv, { now: NOW }).gaps[0].moneyCheck).toContain('Budget available');
    expect(planInterventions([gap], { p178: 2500, p31: 5 }, { now: NOW }).gaps[0].weeks).toBe(0.4);
  });
});
