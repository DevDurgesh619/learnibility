/**
 * W3-P: each student's headline facts as assertions over engine output. Used by check-stories.ts (on the
 * written files) and by the seed search in simulate.ts --search (on a fresh simulation).
 */
import type { AlrRecord, Attempt, GapRecord, MasteryRecord, PlanRecord, Student } from '@/lib/data/types';

export interface StoryData {
  student: Student;
  attempts: Attempt[];
  gaps: GapRecord[];
  mastery: MasteryRecord[];
  alr: AlrRecord[];
  plans: PlanRecord[];
}
export type Fact = [string, (d: StoryData) => boolean | string];

const open = (d: StoryData, subjectId?: string) => d.gaps.filter((g) => g.status !== 'closed' && (!subjectId || g.subjectId === subjectId));
const has = (gs: GapRecord[], code: string) => gs.some((g) => g.code === code || g.secondaryFlags.includes(code as GapRecord['code']));
const latestByChapter = (alr: AlrRecord[]) => {
  const m = new Map<string, AlrRecord>();
  for (const r of [...alr].sort((a, b) => a.asOfUtc.localeCompare(b.asOfUtc))) m.set(r.chapterId, r);
  return [...m.values()];
};
const mean = (xs: number[]) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : NaN);
export const lrs = (d: StoryData) => mean(latestByChapter(d.alr).map((r) => r.LRS));
const mastery = (d: StoryData, sid: string) => mean(d.mastery.filter((m) => m.subjectId === sid).map((m) => m.pMastery));
const lastPlan = (d: StoryData) => d.plans[d.plans.length - 1];
const firstPaid = (d: StoryData) => d.plans.find((p) => p.plan.paidTuition.recommended)?.createdUtc.slice(0, 10);
const chaptersWithOpen = (d: StoryData, sid: string) => new Set(open(d, sid).map((g) => g.chapterId)).size;
const r2 = (x: number) => Math.round(x * 100) / 100;

export const STORIES: Record<string, Fact[]> = {
  lrn_aarav_kapoor: [
    ['LRS about 0.84 (0.80-0.92)', (d) => (lrs(d) >= 0.8 && lrs(d) <= 0.92) || `LRS ${r2(lrs(d))}`],
    ['excellent band', (d) => d.student.band === 'excellent' || d.student.band],
    ['few open gaps (<= 6)', (d) => open(d).length <= 6 || `${open(d).length} open`],
    ['no paid tuition suggested', (d) => !d.plans.some((p) => p.plan.paidTuition.recommended)],
    ['high mastery in Maths (>= 0.85)', (d) => mastery(d, 'cbse-g8-maths') >= 0.85 || r2(mastery(d, 'cbse-g8-maths')).toString()],
  ],
  lrn_ishita_rao: [
    ['G1 prerequisite gap open in Maths', (d) => has(open(d, 'cambridge-g8-maths'), 'G1')],
    ['paid tutor suggested after the free plan ran 3+ weeks', (d) => !!lastPlan(d)?.plan.paidTuition.recommended && lastPlan(d).freePlanWeeks >= 3],
    ['English stronger than Maths', (d) => mastery(d, 'cambridge-g8-english') > mastery(d, 'cambridge-g8-maths') || `${r2(mastery(d, 'cambridge-g8-english'))} vs ${r2(mastery(d, 'cambridge-g8-maths'))}`],
  ],
  lrn_kabir_singh: [
    ['G4 careless flagged on an open gap', (d) => has(open(d), 'G4')],
    ['G9 over-confidence flagged on an open gap', (d) => has(open(d), 'G9')],
    ['MCI about 0.55 before estimate-first (<= 0.62)', (d) => { const x = mean(d.alr.filter((a) => a.asOfUtc < '2026-10-07').map((a) => a.MCI)); return x <= 0.62 || `${r2(x)}`; }],
    ['MCI about 0.7 now (latest >= 0.66)', (d) => { const x = [...d.alr].sort((a, b) => a.asOfUtc.localeCompare(b.asOfUtc)).slice(-2); return mean(x.map((a) => a.MCI)) >= 0.66 || `${x.map((a) => a.MCI)}`; }],
    ['G3 open on cbse-g9-maths-ch05-st3 (9A re-teach cluster)', (d) => open(d).some((g) => g.subtopicId === 'cbse-g9-maths-ch05-st3' && g.code === 'G3') || open(d).find((g) => g.subtopicId === 'cbse-g9-maths-ch05-st3')?.code || 'closed'],
    ['free plan only (no paid tuition now)', (d) => !lastPlan(d)?.plan.paidTuition.recommended],
    ['average or above-average band', (d) => d.student.band === 'average' || d.student.band === 'above_avg' || d.student.band],
  ],
  lrn_meera_iyer: [
    ['G8 time pressure flagged', (d) => has(open(d), 'G8')],
    ['G9 under-confidence flagged', (d) => has(open(d), 'G9')],
    ['low MCI (<= 0.5)', (d) => mean(d.alr.map((a) => a.MCI)) <= 0.5 || `${r2(mean(d.alr.map((a) => a.MCI)))}`],
    ['Science mastery >= 0.7', (d) => mastery(d, 'ib-g9-science') >= 0.7 || r2(mastery(d, 'ib-g9-science')).toString()],
  ],
  lrn_ananya_kapoor: [
    ['excellent band', (d) => d.student.band === 'excellent' || d.student.band],
    ['LRS >= 0.85', (d) => lrs(d) >= 0.85 || `${r2(lrs(d))}`],
    ['no paid tuition suggested', (d) => !d.plans.some((p) => p.plan.paidTuition.recommended)],
  ],
  lrn_rohan_das: [
    ['G10 engagement gap in his history', (d) => d.gaps.some((g) => g.code === 'G10' || g.secondaryFlags.includes('G10'))],
    ['Maths gaps across 3+ chapters', (d) => chaptersWithOpen(d, 'cbse-g10-maths') >= 3 || `${chaptersWithOpen(d, 'cbse-g10-maths')}`],
    ['paid tutor first suggested between 1 Sep and 16 Oct (before the tutor demo)', (d) => { const f = firstPaid(d); return (!!f && f >= '2026-09-01' && f <= '2026-10-16') || `${f}`; }],
    ['paid tutor still recommended', (d) => !!lastPlan(d)?.plan.paidTuition.recommended],
    ['small recovery: 2+ Maths gaps closed since the tutor started (20 Oct)', (d) => { const n = d.gaps.filter((g) => g.subjectId === 'cbse-g10-maths' && g.status === 'closed' && (g.closedUtc ?? '') >= '2026-10-20').length; return n >= 2 || `${n}`; }],
    ['average or below-average band', (d) => d.student.band === 'average' || d.student.band === 'below_avg' || d.student.band],
  ],
  lrn_vihaan_joshi: [
    ['Chemistry R under 0.7 on a chapter', (d) => latestByChapter(d.alr).some((r) => r.subjectId === 'cbse-g11-chemistry' && r.R > 0 && r.R < 0.7) || latestByChapter(d.alr).filter((r) => r.subjectId === 'cbse-g11-chemistry').map((r) => r.R).join(',')],
    ['G6 retention gap open in Chemistry', (d) => has(open(d, 'cbse-g11-chemistry'), 'G6')],
    ['strong Maths (mastery >= 0.85)', (d) => mastery(d, 'cbse-g11-maths') >= 0.85 || r2(mastery(d, 'cbse-g11-maths')).toString()],
  ],
  lrn_sara_khan: [
    ['G2 conceptual gap open in Economics', (d) => has(open(d, 'cbse-g11-economics'), 'G2')],
    ['Accountancy stronger than Economics', (d) => mastery(d, 'cbse-g11-accountancy') > mastery(d, 'cbse-g11-economics') || `${r2(mastery(d, 'cbse-g11-accountancy'))} vs ${r2(mastery(d, 'cbse-g11-economics'))}`],
    ['no paid tuition now', (d) => !lastPlan(d)?.plan.paidTuition.recommended],
  ],
  lrn_arjun_nair: [
    ['G5 reasoning/transfer gap open', (d) => has(open(d), 'G5')],
    ['uneven: subject mastery spread >= 0.08', (d) => { const m = ['ib-g11-political-science', 'ib-g11-history', 'ib-g11-economics', 'ib-g11-english'].map((s) => mastery(d, s)); return Math.max(...m) - Math.min(...m) >= 0.08 || m.map(r2).join(','); }],
  ],
  lrn_diya_sharma: [
    ['4 mock rounds taken', (d) => new Set(d.attempts.filter((a) => a.kind === 'mock').map((a) => a.startedUtc.slice(0, 10))).size === 4],
    ['mock scores swing (range >= 10 points)', (d) => { const p = d.attempts.filter((a) => a.kind === 'mock').map((a) => (100 * a.score) / a.maxScore); return Math.max(...p) - Math.min(...p) >= 10 || `${r2(Math.max(...p) - Math.min(...p))}`; }],
    ['retention dip: G6 open', (d) => has(open(d), 'G6')],
  ],
  lrn_nikhil_reddy: [
    ['Application Support plan', (d) => d.student.plan === 'application_support'],
  ],
  lrn_tara_menon: [
    ['essay-side gap open in English (G4/G5)', (d) => has(open(d, 'ib-g12-english'), 'G5') || has(open(d, 'ib-g12-english'), 'G4') || has(open(d, 'ib-g12-english'), 'G3')],
    ['strong Computer Science (mastery >= 0.85)', (d) => mastery(d, 'ib-g12-computer-science') >= 0.85 || r2(mastery(d, 'ib-g12-computer-science')).toString()],
    ['Application Support plan', (d) => d.student.plan === 'application_support'],
  ],
  lrn_kunal_verma: [
    ['G7 language gap open', (d) => has(open(d), 'G7')],
    ['weak marks: LRS < 0.6', (d) => lrs(d) < 0.6 || `${r2(lrs(d))}`],
  ],
};

export function failures(id: string, d: StoryData): string[] {
  return (STORIES[id] ?? []).flatMap(([name, f]) => {
    const r = f(d);
    return r === true ? [] : [`${name}${r === false ? '' : ` (got ${r})`}`];
  });
}
