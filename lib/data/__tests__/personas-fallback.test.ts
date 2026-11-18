import { beforeEach, describe, expect, it, vi } from 'vitest';

vi.mock('server-only', () => ({}));
process.env.LEARNIBILITY_OVERLAY = 'memory';

const { getPersona } = await import('@/lib/data/personas');
const { writeRecord } = await import('@/lib/store/collections');
const { useMemoryOverlay } = await import('@/lib/store/overlay');

beforeEach(() => {
  useMemoryOverlay();
});

describe('getPersona fallback to the store', () => {
  it('finds a learner created at runtime (e.g. converted from a CRM lead)', () => {
    expect(getPersona('lrn_neel_bhatia')).toBeUndefined();
    writeRecord('student', {
      id: 'lrn_neel_bhatia', role: 'student', firstName: 'Neel', lastName: 'Bhatia', name: 'Neel Bhatia',
      board: 'cbse', grade: 10, stream: 'none', programme: 'CBSE Class 10',
    });
    expect(getPersona('lrn_neel_bhatia')).toMatchObject({ id: 'lrn_neel_bhatia', role: 'student', name: 'Neel Bhatia', grade: 10, board: 'cbse' });
  });

  it('finds an adult created at runtime', () => {
    writeRecord('adults', { id: 'par_ritu_bhatia', role: 'parent', firstName: 'Ritu', lastName: 'Bhatia', name: 'Ritu Bhatia', learnerIds: ['lrn_neel_bhatia'] });
    expect(getPersona('par_ritu_bhatia')).toMatchObject({ role: 'parent', linkedLearnerIds: ['lrn_neel_bhatia'] });
  });

  it('still prefers the persona lists', () => {
    expect(getPersona('lrn_kabir_singh')?.name).toBe('Kabir Singh');
    expect(getPersona('nobody')).toBeUndefined();
  });
});
