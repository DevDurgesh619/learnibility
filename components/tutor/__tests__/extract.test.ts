import { describe, expect, it } from 'vitest';
import { EXAMPLE_INTRO, extractProfile } from '../extract';

describe('extractProfile', () => {
  it('reads the doc example', () => {
    const x = extractProfile(EXAMPLE_INTRO);
    expect(x.subjects).toEqual(['Mathematics']);
    expect(x.grades).toEqual([9, 10, 11, 12]);
    expect(x.exams).toContain('JEE');
    expect(x.topics).toEqual(['Algebra', 'Calculus']);
    expect(x.years).toBe(6);
    expect(x.audiences).toEqual(['school', 'competitive_exam']);
  });
  it('leaves unknowns empty', () => {
    const x = extractProfile('I like helping people.');
    expect(x.subjects).toEqual([]);
    expect(x.years).toBeNull();
    expect(x.grades).toEqual([]);
  });
  it('reads languages, qualifications and several subjects', () => {
    const x = extractProfile('B.Sc and B.Ed. I teach physics and chemistry to class 11 and 12 for NEET, in English and Hindi. 10 yrs.');
    expect(x.subjects).toEqual(['Physics', 'Chemistry']);
    expect(x.qualifications).toEqual(['B.Sc', 'B.Ed']);
    expect(x.languages).toEqual(['English', 'Hindi']);
    expect(x.grades).toEqual([11, 12]);
    expect(x.years).toBe(10);
  });
});
