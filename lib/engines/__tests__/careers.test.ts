import { describe, expect, it } from 'vitest';
import { careerGap, cheapestPathway, mapCareers, nonSensitive, riasecScores } from '../careers';
import { career, exams, resources, skills } from './catalogueFixtures';

const swe = career({ id: 'career-software-engineer', title: 'Software engineer' });
const lawyer = career({ id: 'career-corporate-lawyer', title: 'Corporate lawyer', streams: ['humanities', 'commerce'], riasec: ['E', 'S', 'C'], aptitudeParamIds: ['p65'], subjects: [{ subjectSlug: 'english', minPercent: 80, required: true }], skills: [{ skillId: 'skill-communication', targetLevel: 4, importance: 'core' }] });
const profile = [
  { paramId: 'p200', value: 'IRC', asOfUtc: '2026-10-01T00:00:00Z', tier: 'T2' },
  { paramId: 'p62', value: 85, asOfUtc: '2026-10-01T00:00:00Z', tier: 'T1' },
  { paramId: 'p65', value: 80, asOfUtc: '2026-10-01T00:00:00Z', tier: 'T1' },
  { paramId: 'p215', value: 'developing', asOfUtc: '2026-10-01T00:00:00Z', tier: 'T1' },
  { paramId: 'p178', value: 'medium', asOfUtc: '2026-10-01T00:00:00Z', tier: 'T2' },
  { paramId: 'p111', value: 'high', asOfUtc: '2026-10-01T00:00:00Z', tier: 'T3' },
];
const ctx = { grade: 11 as const, stream: 'science' as const, subjectPercents: { maths: 90, physics: 70, english: 72 }, skills, resources, exams };

describe('mapCareers', () => {
  const fits = mapCareers(profile, [lawyer, swe], ctx);
  it('ranks the career that fits interests, aptitude, skills and stream first', () => {
    expect(fits[0].careerId).toBe('career-software-engineer');
    expect(fits[0].parts.interests).toBe(28.4); // IRC vs IRC with ordered weights
    expect(fits[0].confidence).toBe('high');
    expect(fits[0].reasons[0]).toBe('Matches your IR interests');
    expect(fits[1].reasons).toContain('Usually entered from humanities or commerce');
    expect(fits[0].score).toBeGreaterThan(fits[1].score);
  });
  it('never reads T3 values', () => {
    expect(nonSensitive(profile)).not.toHaveProperty('p111');
    const withT3 = mapCareers([...profile, { paramId: 'p62', value: 0, asOfUtc: '2026-12-01T00:00:00Z', tier: 'T3' }], [swe], ctx);
    expect(withT3[0].score).toBe(fits[0].score);
  });
  it('uses neutral values and low confidence with no evidence', () => {
    const f = mapCareers(undefined, [swe]);
    expect(f[0].confidence).toBe('low');
    expect(f[0].parts.interests).toBe(17.5);
    expect(mapCareers({ p200: { R: 20, I: 90, A: 10, S: 10, E: 10, C: 60 } }, [swe], { budgetTotalInr: 100 })[0].reasons.join()).toContain('costs more');
  });
  it('riasec parsing', () => {
    expect(riasecScores(['I', 'A'])).toEqual({ I: 1, A: 0.7 });
    expect(riasecScores({ I: 0.9 })).toEqual({ I: 0.9 });
    expect(riasecScores(null)).toBeNull();
    expect(riasecScores(5)).toBeNull();
    expect(cheapestPathway(swe)!.id).toBe('x-india');
  });
});

describe('careerGap', () => {
  const g = careerGap(profile, swe, { ...ctx, weeklyHours: 5 });
  it('sizes each skill from the level ladder', () => {
    const prog = g.skills.find((s) => s.skillId === 'skill-programming')!;
    expect(prog.currentLevel).toBe(2);
    expect(prog.levelsToClimb).toBe(2);
    expect(prog.hours).toBe(230); // 80 + 150
    const comm = g.skills.find((s) => s.skillId === 'skill-communication')!;
    expect(comm.hours).toBe(50); // 0 → 3
  });
  it('gives a free route and a paid route with rupees and months', () => {
    expect(g.free).toEqual({ hours: 280, inr: 0, months: 12.9 });
    const prog = g.skills.find((s) => s.skillId === 'skill-programming')!;
    expect(prog.freeRoute.resourceIds).toEqual(['res-cs50']);
    expect(prog.paidRoute).toEqual({ resourceId: 'course-python-pro', hours: 184, inr: 12000 });
    expect(g.paid.inr).toBe(12000);
    expect(g.paid.months).toBeLessThan(g.free.months);
  });
  it('lists pathways with exam prep', () => {
    expect(g.pathways[0]).toMatchObject({ id: 'x-india', examPrepHours: 800, examFeesInr: 1000, yearsToEntry: 4 });
    expect(g.pathways[1].examPrepHours).toBe(0);
  });
  it('uses academic hours and explicit levels; unknown skills default to 20 h a level', () => {
    const c = career({ id: 'c', skills: [{ skillId: 'skill-algebra', targetLevel: 3, importance: 'core' }, { skillId: 'skill-unknown', targetLevel: 2, importance: 'helpful' }] });
    const r = careerGap({}, c, { skills, academicHours: { 'skill-algebra': 12.5 }, skillLevels: { 'skill-unknown': 1 } });
    expect(r.skills[0].hours).toBe(12.5);
    expect(r.skills[1].hours).toBe(20);
    expect(r.skills[1].paidRoute.resourceId).toBeNull();
    expect(careerGap({ p215: 5 }, swe, { skills }).skills[0].hours).toBe(0);
  });
});
