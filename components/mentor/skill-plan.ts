import 'server-only';
import { getCareer, getCareerMatches, getProfile, getStudent, listExams, listResources, listSkills } from '@/lib/data';
import { careerGap, type CareerGapResult } from '@/lib/engines';

/**
 * Skill plan for one mentee and career, computed live with the careers engine (with the skills and resources
 * catalogues, so routes name real resources) on the T1 profile values a mentor may see. Falls back to the
 * stored careerGap result when the career is not in the catalogue.
 */
export function skillPlanFor(learnerId: string, careerId: string): CareerGapResult | undefined {
  const stored = getCareerMatches(learnerId)?.gaps?.[careerId];
  const career = getCareer(careerId);
  const student = getStudent(learnerId);
  if (!career || !student) return stored;
  const profile = getProfile(learnerId, 'mentor')
    .filter((v) => v.mode === 'full' && v.tier === 'T1')
    .map((v) => ({ paramId: v.paramId, value: v.value, asOfUtc: v.asOfUtc ?? '', tier: v.tier }));
  return careerGap(profile, career, { grade: student.grade, stream: student.stream, weeklyHours: 5, skills: listSkills(), resources: listResources(), exams: listExams() });
}

/** Careers to plan for: the mentee's shortlist, else their top 3 fits. */
export function careersToPlan(learnerId: string): { careerId: string; title: string; score?: number }[] {
  const m = getCareerMatches(learnerId);
  if (!m) return [];
  const fit = new Map(m.fits.map((f) => [f.careerId, f]));
  const ids = m.shortlist.length ? m.shortlist : m.fits.slice(0, 3).map((f) => f.careerId);
  return ids.map((id) => ({ careerId: id, title: fit.get(id)?.title ?? getCareer(id)?.title ?? id, score: fit.get(id)?.score }));
}
