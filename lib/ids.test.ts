import { describe, expect, it } from 'vitest';
import {
  catalogueId, chapterId, idKind, learnerId, mockQuestionId, onboardingQuestionId, paramId,
  parseCatalogueId, parseChapterId, parseParamId, parsePersonId, parseQuestionId, parseSubjectId,
  parseSubtopicId, personId, practiceQuestionId, questionId, slugify, subjectId, subtopicId, universityId,
} from './ids';

describe('contract examples round-trip', () => {
  it('subjects', () => {
    for (const [b, g, s, id] of [
      ['cbse', 8, 'maths', 'cbse-g8-maths'],
      ['cambridge', 11, 'physics', 'cambridge-g11-physics'],
      ['ib', 12, 'economics', 'ib-g12-economics'],
      ['cbse', 12, 'applied-maths', 'cbse-g12-applied-maths'],
    ] as const) {
      expect(subjectId(b, g, s)).toBe(id);
      expect(parseSubjectId(id)).toEqual({ board: b, grade: g, slug: s });
      expect(idKind(id)).toBe('subject');
    }
  });

  it('chapters and subtopics', () => {
    expect(chapterId('cbse-g8-maths', 1)).toBe('cbse-g8-maths-ch01');
    expect(chapterId('cbse-g8-maths', 14)).toBe('cbse-g8-maths-ch14');
    expect(parseChapterId('cbse-g8-maths-ch01')).toEqual({
      board: 'cbse', grade: 8, slug: 'maths', subjectId: 'cbse-g8-maths', chapter: 1,
    });
    expect(subtopicId('cbse-g8-maths-ch01', 2)).toBe('cbse-g8-maths-ch01-st2');
    expect(parseSubtopicId('cbse-g8-maths-ch01-st2')).toMatchObject({
      subjectId: 'cbse-g8-maths', chapterId: 'cbse-g8-maths-ch01', chapter: 1, subtopic: 2,
    });
    expect(idKind('cbse-g8-maths-ch01')).toBe('chapter');
    expect(idKind('cbse-g8-maths-ch01-st2')).toBe('subtopic');
  });

  it('questions of every kind', () => {
    const bank = questionId('cbse-g8-maths-ch01-st2', 3);
    expect(bank).toBe('cbse-g8-maths-ch01-st2-q03');
    expect(parseQuestionId(bank)).toMatchObject({ kind: 'bank', subtopicId: 'cbse-g8-maths-ch01-st2', number: 3 });

    const pf = practiceQuestionId('cbse-g8-maths-ch01', 'A', 1);
    expect(pf).toBe('cbse-g8-maths-ch01-pfa-q01');
    expect(parseQuestionId(pf)).toMatchObject({ kind: 'practice', form: 'A', chapterId: 'cbse-g8-maths-ch01', subjectId: 'cbse-g8-maths', chapter: 1, number: 1 });
    expect(parseQuestionId('ib-g11-physics-ch03-pfb-q12')).toMatchObject({ kind: 'practice', form: 'B', chapter: 3, number: 12 });

    const mock = mockQuestionId('cbse-g10-science', 2, 40);
    expect(mock).toBe('cbse-g10-science-mock2-q40');
    expect(parseQuestionId(mock)).toMatchObject({ kind: 'mock', subjectId: 'cbse-g10-science', mock: 2, number: 40 });

    const onb = onboardingQuestionId('cambridge', 11, 'science', 7);
    expect(onb).toBe('onb-cambridge-g11-science-q07');
    expect(parseQuestionId(onb)).toEqual({ kind: 'onboarding', board: 'cambridge', grade: 11, stream: 'science', number: 7 });
    expect(onboardingQuestionId('cbse', 8, 'none', 1)).toBe('onb-cbse-g8-none-q01');
    expect(questionId('cbse-g8-maths-ch01-st2', 123)).toBe('cbse-g8-maths-ch01-st2-q123');
    expect(idKind(bank)).toBe('question');
  });

  it('people', () => {
    expect(learnerId('Kabir', 'Singh')).toBe('lrn_kabir_singh');
    expect(personId('tutor', 'Rahul', 'Verma')).toBe('tut_rahul_verma');
    expect(personId('parent', 'Neha', 'Kapoor')).toBe('par_neha_kapoor');
    expect(personId('teacher', 'Suresh', 'Iyer')).toBe('tch_suresh_iyer');
    expect(personId('counsellor', 'Heena', 'Shah')).toBe('csl_heena_shah');
    expect(personId('mentor', 'Kelvin', "D'Souza")).toBe('mnt_kelvin_dsouza');
    expect(parsePersonId('lrn_kabir_singh')).toEqual({ kind: 'learner', first: 'kabir', last: 'singh' });
    expect(parsePersonId('tut_rahul_verma')).toEqual({ kind: 'tutor', first: 'rahul', last: 'verma' });
    expect(idKind('lrn_kabir_singh')).toBe('person');
  });

  it('catalogue items', () => {
    expect(universityId('us', 'yale')).toBe('uni-us-yale');
    expect(parseCatalogueId('uni-us-yale')).toEqual({ kind: 'uni', country: 'us', slug: 'yale' });
    expect(catalogueId('career', 'data-analyst')).toBe('career-data-analyst');
    expect(parseCatalogueId('career-data-analyst')).toEqual({ kind: 'career', slug: 'data-analyst' });
    for (const id of ['skill-python', 'course-khan-algebra', 'res-ncert-maths-8']) {
      expect(parseCatalogueId(id)).not.toBeNull();
      expect(idKind(id)).toBe('catalogue');
    }
  });

  it('profile parameters', () => {
    expect(paramId(279)).toBe('p279');
    expect(parseParamId('p279')).toBe(279);
    expect(parseParamId('p1')).toBe(1);
    expect(parseParamId('p430')).toBe(430);
    expect(idKind('p279')).toBe('param');
  });
});

describe('rejects malformed IDs', () => {
  it.each([
    'icse-g8-maths', 'cbse-g7-maths', 'CBSE-g8-maths', 'cbse-g8-Maths', 'cbse-g8-', 'cbse-g8-maths-ch1',
    'cbse-g8-maths-ch001', 'cbse-g8-maths-ch00', 'cbse-g8-maths-ch01-st0', 'cbse-g8-maths-ch01-st02',
    'cbse-g8-maths-ch01-st2-q3', 'cbse-g8-maths-ch01-pfc-q01', 'onb-cbse-g8-science-q01', 'onb-cbse-g11-none-q01',
    'lrn_kabir', 'stu_kabir_singh', 'uni-usa-yale', 'p0', 'p431', 'p010', 'career_data_analyst', '',
  ])('%s', (id) => {
    expect(idKind(id)).toBeNull();
  });

  it('builders refuse bad input', () => {
    // @ts-expect-error invalid board
    expect(() => subjectId('icse', 8, 'maths')).toThrow();
    expect(() => subjectId('cbse', 8, 'Maths')).toThrow();
    expect(() => chapterId('cbse-g8-maths', 0)).toThrow();
    expect(() => chapterId('nope', 1)).toThrow();
    expect(() => subtopicId('cbse-g8-maths', 1)).toThrow();
    expect(() => questionId('cbse-g8-maths-ch01', 1)).toThrow();
    expect(() => onboardingQuestionId('cbse', 8, 'science', 1)).toThrow();
    expect(() => onboardingQuestionId('ib', 12, 'none', 1)).toThrow();
    expect(() => paramId(431)).toThrow();
    expect(() => personId('learner', '', 'Singh')).toThrow();
    expect(() => universityId('USA', 'yale')).toThrow();
  });
});

describe('slugify', () => {
  it('makes kebab slugs', () => {
    expect(slugify('Computer Science')).toBe('computer-science');
    expect(slugify('  Legal Studies! ')).toBe('legal-studies');
    expect(slugify('Business & Management')).toBe('business-and-management');
    expect(slugify('Économie')).toBe('economie');
  });
});
