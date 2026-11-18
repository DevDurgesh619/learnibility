/** Engines 6 and 7 on the real W4 catalogues and W2 curriculum names (data/catalogues, data/curriculum). */
import { describe, expect, it } from 'vitest';
import tutorsFile from '../../../data/catalogues/tutors.json';
import careersFile from '../../../data/catalogues/careers.json';
import skillsFile from '../../../data/catalogues/skills.json';
import resourcesFile from '../../../data/catalogues/resources.json';
import examsFile from '../../../data/catalogues/exams.json';
import maths8 from '../../../data/curriculum/cbse-g8-maths.json';
import type { Career, EntranceExam, Resource, Skill, Tutor } from '../../types/catalogue';
import { matchTutors, slotOverlapMinutes } from '../matchTutors';
import { careerGap, mapCareers } from '../careers';

const tutors = tutorsFile.items as unknown as Tutor[];
const careers = careersFile.items as unknown as Career[];
const skills = skillsFile.items as unknown as Skill[];
const resources = resourcesFile.items as unknown as Resource[];
const exams = examsFile.items as unknown as EntranceExam[];
const names: Record<string, string> = {};
for (const c of (maths8 as unknown as { items: { id: string; name: string }[] }).items) names[c.id] = c.name;
for (const s of (maths8 as unknown as { subtopics: { id: string; name: string }[] }).subtopics) names[s.id] = s.name;

describe('matchTutors on the real tutor catalogue', () => {
  const gaps = [
    { id: 'g1', subtopicId: 'cbse-g8-maths-ch01-st2', code: 'G5' as const, hoursToClose: 2.2 }, // square roots
    { id: 'g2', subtopicId: 'cbse-g8-maths-ch13-st2', code: 'G3' as const, hoursToClose: 3.6 }, // factorisation
  ];
  const evenings = (['mon', 'tue', 'wed', 'thu', 'fri'] as const).map((day) => ({ day, start: '17:00', end: '20:00' }));
  const m = matchTutors(gaps, { p178: 60_000, p157: ['Hindi'] }, tutors, { names, availability: evenings, now: '2026-11-18T00:00:00Z' });

  it('returns only tutors who teach CBSE class 8 maths, best first, each with a reason', () => {
    expect(m.length).toBeGreaterThan(0);
    for (const x of m) {
      const t = tutors.find((y) => y.id === x.tutorId)!;
      expect(t.subjects.some((s) => s.subjectSlug === 'maths' && s.boards.includes('cbse') && s.grades.includes(8))).toBe(true);
      expect(x.reason.length).toBeGreaterThan(20);
      expect(x.score).toBeGreaterThan(0);
      expect(x.score).toBeLessThanOrEqual(100);
    }
    for (let i = 1; i < m.length; i++) expect(m[i].score).toBeLessThanOrEqual(m[i - 1].score);
    expect(m[0].parts.topic).toBeGreaterThan(20); // a real topic-strength hit
  });

  it('reads abroad tutors’ availability in their own time zone', () => {
    const london = tutors.find((t) => t.timeZone === 'Europe/London')!;
    const slot = london.availability.find((s) => s.day === 'sat')!;
    // learner (IST) free on Saturday from the tutor's start converted to IST (+5:30 in November) for 90 min
    const [h, mm] = slot.start.split(':').map(Number);
    const ist = h * 60 + mm + 330;
    const hhmm = (x: number) => `${String(Math.floor(x / 60)).padStart(2, '0')}:${String(x % 60).padStart(2, '0')}`;
    expect(slotOverlapMinutes([{ day: 'sat', start: hhmm(ist), end: hhmm(ist + 90) }], london.availability, { tutorTimeZone: london.timeZone, atIso: '2026-11-18T00:00:00Z' })).toBe(90);
    // a weekday 18:30 London slot is after midnight in India, so it does not overlap IST evenings
    expect(slotOverlapMinutes(evenings, [{ day: 'mon', start: '18:30', end: '21:30' }], { tutorTimeZone: 'Europe/London' })).toBe(0);
    expect(slotOverlapMinutes([{ day: 'tue', start: '00:00', end: '03:00' }], [{ day: 'mon', start: '18:30', end: '21:30' }], { tutorTimeZone: 'Europe/London' })).toBe(180);
  });
});

describe('mapCareers and careerGap on the real career catalogue', () => {
  const science = { p200: 'IRC', p62: 85, p65: 78, p63: 80, p215: 'developing', p180: 'medium' };
  const sciFits = mapCareers(science, careers, { grade: 11, stream: 'science', subjectPercents: { maths: 88, physics: 80, chemistry: 75, english: 82 }, skills });
  const humanities = { p200: 'SEA', p65: 75, p210: 4, p211: 4, p180: 'medium' };
  const humFits = mapCareers(humanities, careers, { grade: 11, stream: 'humanities', subjectPercents: { english: 90, history: 85, 'political-science': 88 }, skills });

  it('scores all 40 careers between 0 and 100', () => {
    expect(sciFits).toHaveLength(40);
    for (const f of sciFits) { expect(f.score).toBeGreaterThan(0); expect(f.score).toBeLessThanOrEqual(100); }
  });
  it('puts science careers on top for an IRC science student and humanities careers for an SEA humanities student', () => {
    for (const f of sciFits.slice(0, 5)) expect(careers.find((c) => c.id === f.careerId)!.streams).toContain('science');
    for (const f of humFits.slice(0, 5)) expect(careers.find((c) => c.id === f.careerId)!.streams).toContain('humanities');
    expect(sciFits[0].confidence).toBe('high');
  });
  it('gives every career a gap with hours, a ₹0 free route, a faster paid route and pathway costs', () => {
    for (const c of careers) {
      const g = careerGap(science, c, { skills, resources, exams, weeklyHours: 6 });
      expect(Number.isFinite(g.totalHours)).toBe(true);
      expect(g.free.inr).toBe(0);
      if (g.totalHours > 0) expect(g.paid.months).toBeLessThan(g.free.months);
      expect(g.pathways.some((p) => p.region === 'india')).toBe(true);
      for (const p of g.pathways) expect(p.costInr.typical).toBeGreaterThan(0);
    }
    const swe = careerGap(science, careers.find((c) => c.id === 'career-software-engineer')!, { skills, resources, exams, weeklyHours: 6 });
    expect(swe.pathways.find((p) => p.region === 'india')!.examPrepHours).toBeGreaterThan(0);
  });
});
