import { describe, expect, it } from 'vitest';
import tutorsFile from '@/data/catalogues/tutors.json';
import type { Tutor } from '@/lib/types/catalogue';
import { filterTutors, matchesQuery, moreLikeThese, parseFilters, filtersToParams, activeFilterCount } from '../search';
import { demoSlots, localParts, localToUtc } from '../slots';

const tutors = (tutorsFile as { items: Tutor[] }).items;
const rahul = tutors.find((t) => t.id === 'tut_rahul_verma')!;

describe('search', () => {
  it('parses and round-trips filters', () => {
    const f = parseFilters({ q: ' jee physics ', rating: '4', price: '1000', format: 'one_to_one', mode: 'bogus', board: 'cbse' });
    expect(f).toEqual({ q: 'jee physics', minRating: 4, maxPrice: 1000, format: 'one_to_one', board: 'cbse' });
    expect(parseFilters(Object.fromEntries(filtersToParams(f)))).toEqual(f);
    expect(activeFilterCount(f)).toBe(4);
  });
  it('finds Rahul by subject, topic and exam words', () => {
    expect(matchesQuery(rahul, 'JEE physics')).toBe(true);
    expect(matchesQuery(rahul, 'rotational motion')).toBe(true);
    expect(matchesQuery(rahul, 'accountancy')).toBe(false);
  });
  it('applies price, rating, format and subject filters', () => {
    const r = filterTutors(tutors, { subject: 'maths', maxPrice: 800, minRating: 4 });
    expect(r.length).toBeGreaterThan(0);
    for (const t of r) {
      expect(t.pricing.oneToOnePerHourInr).toBeLessThanOrEqual(800);
      expect(t.rating).toBeGreaterThanOrEqual(4);
      expect(t.subjects.some((s) => s.subjectSlug === 'maths')).toBe(true);
    }
    expect(filterTutors(tutors, { format: 'group' }).every((t) => t.formats.includes('group'))).toBe(true);
  });
  it('suggests similar tutors not already shown', () => {
    const more = moreLikeThese(tutors, [rahul]);
    expect(more.length).toBe(3);
    expect(more.some((t) => t.id === rahul.id)).toBe(false);
  });
});

describe('demo slots', () => {
  const now = new Date('2026-11-18T09:00:00+05:30'); // Wednesday
  it('converts local times both ways', () => {
    const u = localToUtc('2026-11-19', '17:00');
    expect(u).toBe('2026-11-19T11:30:00.000Z');
    expect(localParts(u)).toEqual({ date: '2026-11-19', minutes: 17 * 60, day: 'thu' });
  });
  it('offers only times both are free, starting tomorrow', () => {
    const days = demoSlots({ now, minutes: 30, tutorAvailability: [{ day: 'thu', start: '16:00', end: '19:00' }], studentWindows: [{ day: 'thu', start: '17:00', end: '20:00' }] });
    expect(days).toHaveLength(7);
    expect(days[0]!.date).toBe('2026-11-19');
    expect(days[0]!.slots.map((s) => s.start)).toEqual(['17:00', '18:00']);
    expect(days.slice(1).every((d) => d.slots.length === 0)).toBe(true);
  });
  it('removes busy times and respects max sessions a day', () => {
    const busy = [{ startUtc: localToUtc('2026-11-19', '16:00'), minutes: 60 }];
    const d = demoSlots({ now, minutes: 30, tutorAvailability: [{ day: 'thu', start: '16:00', end: '19:00' }], busy })[0]!;
    expect(d.slots.map((s) => s.start)).toEqual(['17:00', '18:00']);
    const full = demoSlots({ now, minutes: 30, maxPerDay: 1, tutorAvailability: [{ day: 'thu', start: '16:00', end: '19:00' }], busy })[0]!;
    expect(full.full).toBe(true);
    expect(full.slots).toEqual([]);
  });
});
