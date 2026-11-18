/**
 * Teacher view models. Server only: composes `@/lib/data` reads into what the teacher screens show.
 * No persona data lives here; everything comes from the data layer.
 * Teachers see T1 only (lib/visibility): profile values go through getProfile(id, 'teacher').
 */
import 'server-only';
import { redirect } from 'next/navigation';
import {
  getAttempts, getGaps, getMastery, getPersonName, getSection, getSectionHeatmap, getSections, getStudent, getSubject, getTasks,
  type GapRecord, type Section, type SectionHeatmap, type Task,
} from '@/lib/data';
import { currentPersona } from '@/lib/session';
import type { Level } from '@/lib/types';

export interface TeacherContext {
  teacherId: string;
  teacherName: string;
  sections: Section[];
  section?: Section;
}

/** Signed-in teacher, their sections and the section chosen by `?section=` (default: first). */
export async function teacherContext(sectionParam?: string): Promise<TeacherContext> {
  const p = await currentPersona();
  if (!p || p.role !== 'teacher') redirect('/login');
  const sections = [...getSections(p.id)].sort((a, b) => a.grade - b.grade || a.name.localeCompare(b.name));
  const section = sections.find((s) => s.id === sectionParam) ?? sections[0];
  return { teacherId: p.id, teacherName: p.name, sections, section };
}

export function sectionHref(path: string, sectionId: string | undefined, extra: Record<string, string | undefined> = {}) {
  const q = new URLSearchParams();
  if (sectionId) q.set('section', sectionId);
  for (const [k, v] of Object.entries(extra)) if (v) q.set(k, v);
  const s = q.toString();
  return s ? `${path}?${s}` : path;
}

/** "3.2" style short label for a subtopic column: chapter order . subtopic order. */
export function shortLabel(subtopicId: string): string {
  const m = /-ch(\d+)-st(\d+)$/.exec(subtopicId);
  return m ? `${Number(m[1])}.${m[2]}` : subtopicId;
}

export function chaptersOf(subjectId: string) {
  return getSubject(subjectId)?.chapters ?? [];
}

export function subtopicName(subjectId: string, subtopicId: string): { name: string; chapterId: string; chapterName: string } {
  const b = getSubject(subjectId);
  const s = b?.subtopics.find((x) => x.id === subtopicId);
  const c = b?.chapters.find((x) => x.id === s?.chapterId);
  return { name: s?.name ?? subtopicId, chapterId: s?.chapterId ?? '', chapterName: c?.name ?? '' };
}

export function heatmap(section: Section, chapterId?: string): SectionHeatmap | undefined {
  return getSectionHeatmap(section.id, { chapterId });
}

/** Mean pMastery over tested cells; undefined when nothing tested. */
export function meanMastery(cells: Record<string, { pMastery: number } | null | undefined>): number | undefined {
  const v = Object.values(cells).filter((c): c is { pMastery: number } => !!c);
  return v.length ? v.reduce((a, c) => a + c.pMastery, 0) / v.length : undefined;
}

/** Stable id for a background student's gap (they have no gaps.json; validation writes one). */
export const backgroundGapId = (learnerId: string, subtopicId: string) => `gap_${learnerId}_${subtopicId}`;

export interface GapLogRow extends GapRecord {
  studentName: string;
  isPersona: boolean;
  subtopicName: string;
  chapterName: string;
}

/**
 * Every gap in a section, as Gap Log rows: persona learners' full records, plus background learners'
 * light gaps turned into records (and any validation already written for them).
 */
export function sectionGaps(section: Section, opts: { open?: boolean } = {}): GapLogRow[] {
  const out: GapLogRow[] = [];
  const bg = new Map(section.background.map((b) => [b.id, b]));
  for (const lid of section.learnerIds) {
    const b = bg.get(lid);
    if (!b) {
      const name = getStudent(lid)?.name ?? lid;
      for (const g of getGaps(lid, { subjectId: section.subjectId, status: opts.open ? 'open' : undefined })) {
        const n = subtopicName(section.subjectId, g.subtopicId);
        out.push({ ...g, studentName: name, isPersona: true, subtopicName: n.name, chapterName: n.chapterName });
      }
      continue;
    }
    const written = new Map(getGaps(lid).map((g) => [g.id, g]));
    for (const g of b.gaps) {
      if (opts.open && g.status === 'closed') continue;
      const n = subtopicName(section.subjectId, g.subtopicId);
      const id = backgroundGapId(lid, g.subtopicId);
      const tested = b.mastery[g.subtopicId]?.lastTestedUtc ?? '';
      const base: GapRecord = {
        id, learnerId: lid, subtopicId: g.subtopicId, code: g.code, secondaryFlags: [], level: g.level, size: Math.max(1, 5 - g.level),
        hoursToClose: g.hoursToClose, status: g.status, chapterId: n.chapterId, subjectId: section.subjectId,
        detectedUtc: tested, updatedUtc: tested, band: 'average', weeks: null, scorePct: Math.round((b.mastery[g.subtopicId]?.pMastery ?? 0) * 100),
        confirmingProbe: null, likelyCauses: null, prerequisiteToProbe: null,
      };
      out.push({ ...base, ...(written.get(id) ?? {}), studentName: b.name, isPersona: false, subtopicName: n.name, chapterName: n.chapterName });
    }
  }
  return out.sort((a, b) => (b.detectedUtc || '').localeCompare(a.detectedUtc || '') || a.studentName.localeCompare(b.studentName));
}

export interface GapCluster {
  subtopicId: string;
  subtopicName: string;
  chapterId: string;
  chapterName: string;
  code: GapRecord['code'];
  learners: { id: string; name: string; level: Level; hours: number }[];
  meanHours: number;
}

/**
 * Gap clusters: open gaps grouped by subtopic × code (teacher corrections applied, rejected diagnoses left out).
 * Same grouping as getSectionHeatmap's clusters, recomputed here so a validation shows at once. Only clusters of 2+.
 */
export function sectionClusters(section: Section, chapterId?: string): GapCluster[] {
  const groups = new Map<string, GapLogRow[]>();
  for (const g of sectionGaps(section, { open: true })) {
    if (g.validation?.verdict === 'rejected') continue;
    if (chapterId && g.chapterId !== chapterId) continue;
    const k = `${g.subtopicId}|${g.code}`;
    groups.set(k, [...(groups.get(k) ?? []), g]);
  }
  return [...groups.values()]
    .filter((rows) => rows.length >= 2)
    .map((rows) => {
      const f = rows[0]!;
      const learners = rows.map((g) => ({ id: g.learnerId, name: g.studentName, level: g.level, hours: g.hoursToClose })).sort((a, b) => a.name.localeCompare(b.name));
      const meanHours = learners.reduce((a, l) => a + l.hours, 0) / learners.length;
      return { subtopicId: f.subtopicId, subtopicName: f.subtopicName, chapterId: f.chapterId, chapterName: f.chapterName, code: f.code, learners, meanHours };
    })
    .sort((a, b) => b.learners.length - a.learners.length || b.meanHours - a.meanHours);
}

export interface AssignmentGroup {
  groupId: string;
  title: string;
  kind: Task['kind'];
  dueDate: string;
  createdUtc: string;
  detail?: string;
  refId?: string;
  learners: { id: string; name: string; status: Task['status'] }[];
}

/** Teacher-created tasks in a section, grouped by assignment (task ids are `{groupId}__{learnerId}`). */
export function sectionAssignments(section: Section, teacherId: string): AssignmentGroup[] {
  const groups = new Map<string, AssignmentGroup>();
  const bg = new Map(section.background.map((b) => [b.id, b.name]));
  for (const lid of section.learnerIds) {
    for (const t of getTasks(lid, undefined, { source: 'teacher', createdBy: teacherId })) {
      if (t.subjectId && t.subjectId !== section.subjectId) continue;
      const gid = t.id.includes('__') ? t.id.split('__')[0]! : t.id;
      const g = groups.get(gid) ?? { groupId: gid, title: t.title, kind: t.kind, dueDate: t.dueDate, createdUtc: t.createdUtc, detail: t.detail, refId: t.refId, learners: [] };
      g.learners.push({ id: lid, name: bg.get(lid) ?? getStudent(lid)?.name ?? lid, status: t.status });
      groups.set(gid, g);
    }
  }
  return [...groups.values()].sort((a, b) => b.createdUtc.localeCompare(a.createdUtc));
}

/** One student in the teacher's view: persona learners have full history, background ones light data. */
export function studentDetail(section: Section, learnerId: string) {
  const b = section.background.find((x) => x.id === learnerId);
  const gaps = sectionGaps(section).filter((g) => g.learnerId === learnerId);
  if (b) {
    return {
      id: learnerId, name: b.name, isPersona: false as const, student: undefined,
      mastery: Object.entries(b.mastery).map(([subtopicId, m]) => ({ subtopicId, ...m })),
      gaps, attempts: [] as ReturnType<typeof getAttempts>, testScores: b.testScores,
    };
  }
  const student = getStudent(learnerId);
  return {
    id: learnerId, name: student?.name ?? getPersonName(learnerId)?.name ?? learnerId, isPersona: true as const, student,
    mastery: getMastery(learnerId, section.subjectId).map((m) => ({ subtopicId: m.subtopicId, level: m.level, pMastery: m.pMastery, lastTestedUtc: m.lastTestedUtc })),
    gaps, attempts: getAttempts(learnerId, { subjectId: section.subjectId }), testScores: [] as { title: string; date: string; pct: number }[],
  };
}

export { getSection };

// ------------------------------------------------------------------ interventions catalogue (read-only, W3)
import interventionsFile from '@/data/catalogues/interventions.json';

export interface InterventionLine { id: string; rank: number; name: string; whatToDo: string; timeCost: string; money: string }

/** The workbook's ranked free interventions for a gap code (rank 1 first). */
export function interventionsFor(code: GapRecord['code']): InterventionLine[] {
  return (interventionsFile.items as unknown as (InterventionLine & { gapCode: string })[])
    .filter((i) => i.gapCode === code)
    .sort((a, b) => a.rank - b.rank)
    .map(({ id, rank, name, whatToDo, timeCost, money }) => ({ id, rank, name, whatToDo, timeCost, money }));
}
