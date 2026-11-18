import { beforeEach, describe, expect, it, vi } from 'vitest';

vi.mock('server-only', () => ({}));
process.env.LEARNIBILITY_OVERLAY = 'memory';

const data = await import('@/lib/data');
const core = await import('@/lib/actions/core');
const { useMemoryOverlay } = await import('@/lib/store/overlay');

const KABIR = 'lrn_kabir_singh';
const NIKHIL = 'lrn_nikhil_reddy';
const FIXTURE_STUDENTS = ['lrn_kabir_singh', 'lrn_rohan_das', 'lrn_ishita_rao', 'lrn_sara_khan', 'lrn_nikhil_reddy', 'lrn_ananya_kapoor'];

beforeEach(() => {
  useMemoryOverlay();
});

describe('reads return typed data for fixture learners', () => {
  it.each(FIXTURE_STUDENTS)('%s has a full record', (id) => {
    const s = data.getStudent(id)!;
    expect(s.id).toBe(id);
    expect(data.dataSourceOf(id)).not.toBe('none');
    expect(data.getAttempts(id).length).toBeGreaterThan(5);
    expect(data.getMastery(id).length).toBeGreaterThan(5);
    expect(data.getAlr(id).chapters.length).toBeGreaterThan(0);
    expect(data.getTimetable(id)!.blocks.length).toBeGreaterThan(0);
    expect(data.getTasks(id).length).toBeGreaterThan(0);
    expect(data.getProfile(id, 'student').length).toBeGreaterThan(20);
    expect(data.getSessions(id).length).toBeGreaterThan(0);
    expect(data.getDocuments(id).length).toBeGreaterThan(0);
    expect(data.getCareerMatches(id)!.fits.length).toBeGreaterThan(0);
    expect(data.getNextBestActions(id).length).toBeGreaterThan(0);
    expect(data.getConsents(id).length).toBeGreaterThan(0);
  });

  it('Kabir: grade 9 CBSE with gaps, a plan and a pending timetable request', () => {
    expect(data.getStudent(KABIR)).toMatchObject({ board: 'cbse', grade: 9 });
    expect(data.getGaps(KABIR, { status: 'open' }).length).toBeGreaterThan(0);
    expect(data.getCurrentPlan(KABIR)!.plan.gaps.length).toBeGreaterThan(0);
    expect(data.getTimetableRequests({ counsellorId: 'csl_heena_qureshi', status: 'pending' }).some((r) => r.learnerId === KABIR)).toBe(true);
    const a = data.getAttempts(KABIR)[0];
    expect(data.getAttempt(a.id)!.responses.length).toBeGreaterThan(0);
    expect(data.getQuestions({ ids: a.questionIds }).length).toBe(a.questionIds.length);
  });

  it('Nikhil: grade 12 applicant on Application Support', () => {
    expect(data.getStudent(NIKHIL)).toMatchObject({ grade: 12, plan: 'application_support' });
    expect(data.getInvoices(NIKHIL).length).toBe(3);
    expect(data.getApplications(NIKHIL)).toHaveProperty('applications');
  });

  it('Rohan: paid tutor suggested by the 3-week rule, parent sees him', () => {
    const plan = data.getCurrentPlan('lrn_rohan_das')!;
    expect(plan.plan.paidTuition.recommended).toBe(true);
    expect(plan.freePlanWeeks).toBeGreaterThanOrEqual(3);
    const kids = data.getChildren('par_anita_das');
    expect(kids.map((k) => k.student.id)).toEqual(['lrn_rohan_das']);
    expect(data.getTutorMatches('lrn_rohan_das').length).toBeGreaterThan(0);
  });

  it('adults: parents, teacher sections and heatmap, caseloads', () => {
    expect(data.getChildren('par_neha_kapoor').map((k) => k.student.id)).toContain('lrn_ananya_kapoor');
    const secs = data.getSections('tch_suresh_pillai');
    expect(secs.map((s) => s.id)).toEqual(['sec-cbse-g10-maths-b', 'sec-cbse-g9-maths-a']);
    const hm = data.getSectionHeatmap('sec-cbse-g9-maths-a')!;
    expect(hm.rows).toHaveLength(10);
    expect(hm.rows.find((r) => r.learnerId === KABIR)!.isPersona).toBe(true);
    expect(hm.clusters[0].learnerIds.length).toBeGreaterThanOrEqual(5);
    expect(hm.clusters[0]).toMatchObject({ subtopicId: 'cbse-g9-maths-ch05-st3', code: 'G3' });
    const heena = data.getCaseload('csl_heena_qureshi');
    expect(heena).toHaveLength(6);
    expect(heena.find((c) => c.student.id === KABIR)!.pendingRequests).toBe(1);
    expect(data.getCaseload('mnt_kelvin_thomas').map((c) => c.student.id)).toEqual(['lrn_sara_khan']);
    expect(data.getMeetingNotes('lrn_sara_khan', { kind: 'career' })).toHaveLength(1);
  });

  it('visibility: T3 never reaches parent, teacher, tutor or mentor', () => {
    const rohanT3 = data.getProfileValues('lrn_rohan_das').filter((v) => v.tier === 'T3');
    expect(rohanT3.length).toBeGreaterThan(0);
    for (const role of ['teacher', 'tutor', 'mentor'] as const) expect(data.getProfile('lrn_rohan_das', role).some((v) => v.tier === 'T3')).toBe(false);
    expect(data.getProfile('lrn_rohan_das', 'parent').filter((v) => v.tier === 'T3').every((v) => v.mode === 'summary' && v.value === undefined)).toBe(true);
  });

  it('catalogue readers', () => {
    expect(data.getSubject('cbse-g9-maths')!.subtopics[0].masterHours.average).toBeGreaterThan(0);
    expect(data.getChapter('cbse-g9-maths-ch01')!.subtopics.length).toBeGreaterThan(0);
    expect(data.listTutors({ subjectSlug: 'maths', board: 'cbse', grade: 9 }).length).toBeGreaterThan(0);
    expect(data.listUniversities({ country: 'uk' }).length).toBeGreaterThan(5);
    expect(data.getTutorWorkspace('tut_rahul_verma')!.tutor.id).toBe('tut_rahul_verma');
    expect(data.listPersonas().some((p) => p.id === NIKHIL)).toBe(true);
  });
});

describe('store: writes change the derived data', () => {
  it('a test attempt written through the store changes getGaps and getTimetable', () => {
    const before = data.getGaps(KABIR);
    const gap = data.getGaps(KABIR, { status: 'open' }).find((g) => g.code === 'G3')!;
    const ttBefore = data.getTimetable(KABIR)!;
    expect(ttBefore.blocks.some((b) => b.refId === gap.id || b.refId === gap.subtopicId)).toBe(true);
    // Kabir re-takes the gap subtopic's full check path and gets everything right
    const path = data.getQuestions({ subtopicIds: [gap.subtopicId], includeFixtures: true }).filter((q) => q.id.endsWith('q901') || q.alrRole !== 'retention_probe' || q.conceptGroup === 'C2');
    const questions = path.filter((q) => !q.id.endsWith(`q9${String(path.length).padStart(2, '0')}`) || q.conceptGroup !== 'C1' || q.difficulty !== 'D2');
    core.putRecord('attempts', {
      id: core.newId('att'), learnerId: KABIR, kind: 'chapter_check', title: 'Re-check', subjectId: 'cbse-g9-maths', chapterId: gap.chapterId,
      questionIds: questions.map((q) => q.id), responses: questions.map((q) => ({ questionId: q.id, correct: true, secondsTaken: q.minutes * 50, confidence: 4 })),
      startedUtc: core.nowStamp(), submittedUtc: core.nowStamp(), minutesAllotted: 20, score: 20, maxScore: 20, status: 'submitted',
    });
    const res = core.recomputeLearner(KABIR);
    expect(res.appliedAttemptIds).toHaveLength(1);
    const after = data.getGaps(KABIR).find((g) => g.id === gap.id)!;
    expect(after.code === 'G3' && after.level === gap.level).toBe(false);
    expect(after.level).toBeGreaterThan(gap.level);
    expect(data.getGaps(KABIR)).not.toEqual(before);
    const ttAfter = data.getTimetable(KABIR)!;
    expect(ttAfter.generatedUtc).not.toBe(ttBefore.generatedUtc);
    expect(JSON.stringify(ttAfter.blocks)).not.toBe(JSON.stringify(ttBefore.blocks));
    expect(data.getPlans(KABIR)[0].id).toBe(res.plan!.id);
    // idempotent
    expect(core.recomputeLearner(KABIR).appliedAttemptIds).toHaveLength(0);
    // reset brings back the JSON state
    core.resetDemo();
    expect(data.getGaps(KABIR)).toEqual(before);
  });

  it('a task, request approval and booking show up in reads', () => {
    core.putRecord('tasks', { id: 'task_t1', learnerId: KABIR, title: 'Re-teach set', kind: 'test', dueDate: '2026-11-19', status: 'todo', source: 'teacher', createdBy: 'tch_suresh_pillai', createdUtc: core.nowStamp() });
    expect(data.getTasks(KABIR, '2026-11-19').some((t) => t.id === 'task_t1')).toBe(true);
    const req = data.getTimetableRequests({ learnerId: KABIR, status: 'pending' })[0];
    core.putRecord('requests', { ...req, status: 'approved', decidedBy: 'csl_heena_qureshi', decidedUtc: core.nowStamp() });
    expect(data.getTimetableRequests({ learnerId: KABIR, status: 'pending' })).toHaveLength(0);
    const r = core.recomputeLearner(KABIR, { reason: 'request_approved' });
    expect(r.timetable?.reason).toBe('request_approved');
    core.putRecord('bookings', { id: 'bk_1', learnerId: KABIR, tutorId: 'tut_rahul_verma', kind: 'demo', status: 'requested', format: 'one_to_one', priceInr: 0, requestedAt: core.nowStamp(), minutes: 30, sharedGapSnapshot: null });
    expect(data.getTutorWorkspace('tut_rahul_verma')!.bookings.some((b) => b.id === 'bk_1')).toBe(true);
    core.appendEvent(KABIR, { sourceMethod: 'M14', type: 'task_done', payload: { taskId: 'task_t1' } });
    expect(data.getEvents(KABIR, { type: 'task_done' })).toHaveLength(1);
  });

  it('a gap validation with a corrected code is reflected in getGaps', () => {
    const g = data.getGaps(KABIR, { status: 'open' })[0];
    core.putRecord('gaps', { ...g, validation: { byId: 'tch_suresh_pillai', utc: core.nowStamp(), verdict: 'corrected', correctedCode: 'G7' } });
    expect(data.getGaps(KABIR).find((x) => x.id === g.id)!.code).toBe('G7');
  });
});
