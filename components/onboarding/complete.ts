import 'server-only';
import { appendEvent, nowStamp, putRecord, recomputeLearner } from '@/lib/actions/core';
import { getGaps, getProfileValues, getStudent, getSubtopic, listSubjects, type Attempt, type GapRecord, type Student } from '@/lib/data';
import { planFor, weeklyHoursPerSubject } from '@/lib/data/derive';
import { LEVEL_TIME_FRACTION } from '@/lib/engines';
import { bandFor, scoreOnboarding, type OnboardingResponses, type OnboardingResult } from '@/lib/onboarding/score';
import type { Band, ProfileValue } from '@/lib/types';
import type { OnboardingAcademicItem, OnboardingFormFile } from '@/lib/types/onboarding';
import type { OnboardingDraft } from './draft';

/** Default study windows for a new student until they edit them (IST, outside school hours). */
const DEFAULT_WINDOWS: Student['availability'] = [
  { day: 'mon', start: '17:30', end: '19:30' },
  { day: 'tue', start: '17:30', end: '19:30' },
  { day: 'wed', start: '17:30', end: '19:30' },
  { day: 'thu', start: '17:30', end: '19:30' },
  { day: 'fri', start: '17:30', end: '19:00' },
  { day: 'sat', start: '10:00', end: '12:30' },
  { day: 'sun', start: '16:00', end: '18:00' },
];

const TARGET_GOAL: Record<string, string> = {
  board_exams: 'Board exams', entrance_exams: 'Entrance exams', sat_act: 'SAT / ACT', study_abroad: 'Study abroad', not_sure: 'Exploring',
};

/** Share of the school year done by the demo date (CBSE starts in April, Cambridge and IB in August). */
function yearProgress(board: Student['board'], nowIso: string): number {
  const now = new Date(nowIso);
  const start = new Date(Date.UTC(now.getUTCFullYear(), board === 'cbse' ? 3 : 7, 1));
  if (start > now) start.setUTCFullYear(start.getUTCFullYear() - 1);
  return Math.min(0.95, (now.getTime() - start.getTime()) / (300 * 86_400_000));
}

function profileCompletion(draft: OnboardingDraft, took: { academic: boolean; reasoning: boolean; about: boolean }): number {
  const parts = [!!draft.name, !!draft.grade, !!draft.target, !!draft.needs?.length, !draft.profileSkipped, took.academic, took.reasoning, took.about];
  return Math.round((100 * parts.filter(Boolean).length) / parts.length);
}

export interface CompleteInput {
  learnerId: string;
  draft: OnboardingDraft;
  file: OnboardingFormFile | null;
  responses: OnboardingResponses;
}

/**
 * Writes everything a finished onboarding produces: the student record, starting profile values,
 * suspected gaps with hours, one onboarding attempt per subject group, a first intervention plan and
 * this week's timetable (through recomputeLearner).
 */
export function completeOnboardingFor({ learnerId, draft, file, responses }: CompleteInput): { result?: OnboardingResult; student: Student } {
  const now = nowStamp();
  const existing = getStudent(learnerId);
  const board = draft.board ?? existing?.board ?? 'cbse';
  const grade = draft.grade ?? existing?.grade ?? 9;
  const stream = grade >= 11 ? draft.stream ?? existing?.stream ?? 'science' : 'none';
  const result = file && (responses.academic.length || responses.reasoning.length || responses.survey.length)
    ? scoreOnboarding(file, responses, { learnerId, nowUtc: now })
    : undefined;

  // Band: mean of answered Part A groups, else average.
  const answered = result?.groups.filter((g) => g.itemsSeen > 0) ?? [];
  const band: Band = answered.length ? bandFor(answered.reduce((s, g) => s + g.percent, 0) / answered.length) : existing?.band ?? 'average';

  const testedSubjects = new Set(
    file?.form.scoring.groups.filter((g) => answered.some((a) => a.group === g.group)).flatMap((g) => g.subjectIds) ?? [],
  );
  const subjects = listSubjects({ board, grade, stream: grade >= 11 ? stream : undefined }).filter((s) => s.grade === grade);
  const progress = yearProgress(board, now);
  const fullSubjects = subjects.filter((s) => testedSubjects.has(s.id) || (!testedSubjects.size && ['maths', 'science'].includes(s.slug)));
  const studyHoursPerDay = Number(result?.profile.find((p) => p.paramId === 'p31')?.value) || 1.5;
  const [firstName, ...rest] = (draft.name ?? existing?.name ?? 'New Student').split(' ');

  const student: Student = {
    ...(existing ?? ({} as Student)),
    id: learnerId,
    role: 'student',
    firstName,
    lastName: rest.join(' '),
    name: draft.name ?? existing?.name ?? firstName,
    board,
    grade,
    stream,
    programme: existing?.programme || `${board === 'cbse' ? 'CBSE' : board === 'ib' ? 'IB' : 'Cambridge'} Class ${grade}`,
    school: draft.school ?? existing?.school ?? '',
    city: existing?.city ?? '',
    band,
    plan: existing?.plan ?? 'free',
    subjects: subjects.map((s) => ({ subjectId: s.id, depth: fullSubjects.some((f) => f.id === s.id) ? 'full' : 'light' })),
    availability: existing?.availability?.length ? existing.availability : DEFAULT_WINDOWS,
    weeklyHours: Math.round(Math.min(14, Math.max(4, studyHoursPerDay * 5)) * 10) / 10,
    tzOffsetMinutes: 330,
    onboardedUtc: now,
    joinedUtc: existing?.joinedUtc ?? now,
    parentIds: existing?.parentIds ?? [],
    counsellorIds: existing?.counsellorIds ?? [],
    mentorIds: existing?.mentorIds ?? [],
    tutorIds: existing?.tutorIds ?? [],
    sectionIds: existing?.sectionIds ?? [],
    currentChapterIds: fullSubjects.flatMap((s) => {
      const n = Math.max(1, Math.round(s.chapterCount * progress));
      return [`${s.id}-ch${String(n).padStart(2, '0')}`];
    }),
    goal: draft.target ? `${TARGET_GOAL[draft.target]}${draft.targetYear ? ` ${draft.targetYear}` : ''}` : existing?.goal,
    profileCompletionPct: profileCompletion(draft, {
      academic: responses.academic.length > 0,
      reasoning: responses.reasoning.length > 0,
      about: responses.survey.length > 0,
    }),
  };
  putRecord('student', student);

  // Profile values: scored ones, plus what the student told us in 1e-1g.
  const pv = (paramId: string, value: unknown, tier: ProfileValue['tier'] = 'T1'): ProfileValue => ({ learnerId, paramId, value, source: 'M1', asOfUtc: now, confidence: 'medium', tier });
  const values: ProfileValue[] = [...(result?.profile ?? [])];
  if (!result) values.push(pv('p1', grade), pv('p3', board));
  if (draft.school) values.push(pv('p2', draft.school));
  if (draft.lastExamPercent) values.push(pv('p8', draft.lastExamPercent));
  if (draft.activities) values.push(pv('p99', draft.activities));
  if (draft.target === 'study_abroad' && draft.targetYear) values.push(pv('p232', draft.targetYear));
  for (const v of values) putRecord('profile', v);

  // Suspected gaps with hours to close (master hours at the band × the level's time fraction).
  if (result) {
    const byId = new Map(file!.items.map((i) => [i.id, i]));
    const bySubtopic = new Map<string, GapRecord>();
    for (const g of result.suspectedGaps) {
      const st = getSubtopic(g.subtopicId);
      const master = st?.masterHours?.[band] ?? 3;
      const frac = LEVEL_TIME_FRACTION[g.level];
      const hours = Math.round(master * (frac.fraction + (g.code === 'G1' ? frac.prerequisiteExtra : 0)) * 10) / 10;
      const item = byId.get(g.evidenceItemIds[0]) as OnboardingAcademicItem | undefined;
      const prev = bySubtopic.get(g.subtopicId);
      if (prev && prev.size >= g.size) continue;
      bySubtopic.set(g.subtopicId, {
        id: `gap_${learnerId.replace(/^lrn_/, '')}_${g.subtopicId}`,
        learnerId,
        subtopicId: g.subtopicId,
        chapterId: st?.chapterId ?? item?.chapterId ?? g.subtopicId.replace(/-st\d+$/, ''),
        subjectId: g.subjectId,
        code: g.code,
        secondaryFlags: g.secondaryFlags,
        level: g.level,
        size: g.size,
        hoursToClose: hours,
        status: 'suspected',
        detectedUtc: now,
        updatedUtc: now,
        band,
        weeks: Math.round((hours / Math.max(1, weeklyHoursPerSubject(student))) * 10) / 10,
        scorePct: 0,
        confirmingProbe: 'Chapter check on this subtopic confirms or clears this starting-test gap.',
        likelyCauses: g.reason,
        prerequisiteToProbe: item?.prerequisiteNote ?? null,
      });
    }
    for (const g of bySubtopic.values()) putRecord('gaps', g);

    // One attempt per subject group, so Assessments shows the initial tests as done with a gap analysis.
    for (const grp of result.groups.filter((x) => x.itemsSeen > 0)) {
      const rs = responses.academic.filter((r) => (byId.get(r.questionId) as OnboardingAcademicItem | undefined)?.group === grp.group);
      const items = rs.map((r) => byId.get(r.questionId) as OnboardingAcademicItem);
      const attempt: Attempt = {
        id: `att_${learnerId.replace(/^lrn_/, '')}_onb_${grp.group}`,
        learnerId,
        kind: 'onboarding',
        title: `${grp.label} · starting test`,
        subjectId: file!.form.scoring.groups.find((g) => g.group === grp.group)?.subjectIds[0] ?? grp.group,
        questionIds: rs.map((r) => r.questionId),
        responses: rs.map((r) => ({ questionId: r.questionId, correct: r.correct, secondsTaken: r.secondsTaken, confidence: r.confidence, answer: (r as { answer?: string }).answer })),
        startedUtc: now,
        submittedUtc: now,
        minutesAllotted: Math.round(items.reduce((s, i) => s + i.minutes, 0)),
        score: items.reduce((s, i, k) => s + (rs[k].correct ? i.marks : 0), 0),
        maxScore: items.reduce((s, i) => s + i.marks, 0),
        status: 'submitted',
      };
      putRecord('attempts', attempt);
    }
  }

  appendEvent(learnerId, {
    sourceMethod: 'M9',
    type: 'onboarding_completed',
    payload: {
      formId: file?.form.formId ?? null,
      needs: draft.needs ?? [],
      target: draft.target ?? null,
      targetYear: draft.targetYear ?? null,
      hardSubjects: draft.hardSubjects ?? [],
      satStatus: draft.satStatus ?? null,
      groups: result?.groups ?? [],
      reasoning: responses.reasoning.length ? result?.reasoning ?? null : null,
      processingSpeed: responses.reasoning.length ? result?.processingSpeed ?? null : null,
      riasec: responses.survey.length ? result?.riasec ?? null : null,
      parameterIds: values.map((v) => v.paramId),
      testTaken: !!result,
    },
  });

  // First plan from the suspected gaps, then this week's timetable.
  const profile = getProfileValues(learnerId).filter((v) => v.tier !== 'T3' && v.tier !== 'C');
  const gaps = getGaps(learnerId);
  if (gaps.length) putRecord('plans', planFor(student, gaps, now, 0, profile));
  recomputeLearner(learnerId, { reason: 'onboarding' });
  return { result, student };
}
