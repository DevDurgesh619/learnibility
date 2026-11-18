import { describe, expect, it } from 'vitest';
import { matchTutors, slotOverlapMinutes, STYLE_FOR_GAP } from '../matchTutors';
import { tutor } from './catalogueFixtures';

const gaps = [
  { id: 'g1', subtopicId: 'cbse-g8-maths-ch01-st2', code: 'G2' as const, hoursToClose: 3 },
  { id: 'g2', subtopicId: 'cbse-g8-maths-ch06-st2', code: 'G3' as const, hoursToClose: 1 },
];
const names = { 'cbse-g8-maths-ch01-st2': 'Square roots: prime factorisation and estimation', 'cbse-g8-maths-ch01': 'A Square and a Cube', 'cbse-g8-maths-ch06-st2': 'Algebraic expressions: terms, like terms, addition' };
const rahul = tutor({ id: 'tut_rahul_verma', displayName: 'Rahul Verma' });
const pricey = tutor({ id: 'tut_pricey', pricing: { ...rahul.pricing, oneToOnePerHourInr: 1500 }, teachingStyles: ['exam_focused', 'practice_first'], languages: ['English'], rating: 4.9, reviewsCount: 5 });
const physics = tutor({ id: 'tut_physics', subjects: [{ subjectSlug: 'physics', boards: ['cbse'], grades: [11, 12], topicStrengths: ['optics'] }] });
const offline = tutor({ id: 'tut_offline', modes: ['offline'], city: 'Mumbai', formats: ['one_to_one'], subjects: [{ subjectSlug: 'maths', boards: ['cbse'], grades: [8], topicStrengths: [] }], verified: false });
const avail = [{ day: 'mon' as const, start: '17:00', end: '19:00' }, { day: 'wed' as const, start: '18:00', end: '19:00' }];

describe('matchTutors', () => {
  const m = matchTutors(gaps, { p178: 8000, p157: ['Hindi'] }, [pricey, physics, rahul, offline], { names, availability: avail });
  it('ranks the topic, style and budget fit first and drops tutors who cannot help', () => {
    expect(m[0].tutorId).toBe('tut_rahul_verma');
    expect(m.map((x) => x.tutorId)).not.toContain('tut_physics');
    expect(m[0].parts.topic).toBe(40);
    expect(m[0].parts.style).toBe(20);
    expect(m[0].parts.price).toBe(15);
    expect(m[0].parts.language).toBe(5);
    expect(m[0].sharedSlotMinutes).toBe(180);
    expect(m[0].parts.slots).toBe(10);
    expect(m[0].reason).toContain('Strong in Square roots');
    expect(m[0].reason).toContain('₹800/hr within budget');
    expect(m[0].reason).toContain('teaches in Hindi');
  });
  it('scores price down above budget and penalises unverified tutors', () => {
    const p = m.find((x) => x.tutorId === 'tut_pricey')!;
    expect(p.parts.price).toBeLessThan(15);
    expect(p.parts.style).toBe(4);
    expect(p.reason).toContain('budget ₹1,000/hr');
    const o = m.find((x) => x.tutorId === 'tut_offline')!;
    expect(o.reason).toContain('not yet verified');
    expect(o.parts.topic).toBe(20);
  });
  it('filters by mode, city and format', () => {
    expect(matchTutors(gaps, {}, [rahul, offline], { mode: 'offline', city: 'Mumbai', names }).map((x) => x.tutorId)).toEqual(['tut_offline']);
    expect(matchTutors(gaps, {}, [rahul, offline], { mode: 'online', names }).map((x) => x.tutorId)).toEqual(['tut_rahul_verma']);
    const g = matchTutors(gaps, {}, [rahul, offline], { format: 'group', names });
    expect(g.map((x) => x.tutorId)).toEqual(['tut_rahul_verma']);
    expect(g[0].pricePerHourInr).toBe(350);
  });
  it('handles unknown budget, zero budget, no availability and a stated style', () => {
    const u = matchTutors(gaps, undefined, [rahul], { names });
    expect(u[0].parts.price).toBe(8);
    expect(u[0].parts.slots).toBe(5);
    expect(u[0].parts.language).toBe(3);
    expect(matchTutors(gaps, { p178: 'none' }, [rahul])[0].parts.price).toBe(0);
    expect(matchTutors(gaps, {}, [rahul, pricey], { preferredStyle: 'exam_focused' }).find((x) => x.tutorId === 'tut_pricey')!.parts.style).toBe(20);
    expect(matchTutors(gaps, { p178: 'high' }, [rahul])[0].parts.price).toBe(15);
    expect(matchTutors([], {}, [rahul])[0].parts.style).toBe(10);
  });
  it('helpers', () => {
    expect(slotOverlapMinutes(avail, rahul.availability)).toBe(180);
    expect(Object.keys(STYLE_FOR_GAP)).toHaveLength(10);
  });
});
