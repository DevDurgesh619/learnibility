import { NextResponse } from 'next/server';
import { demoNow, getAlr, getSections, getGaps, getInvoices, getSessions, getStudent, getSubtopic, getTimetable, listPersonas } from '@/lib/data';
import { BAND_LABEL } from '@/components/ui/badge';
import { formatHours, formatInr } from '@/lib/format';

/**
 * GET /demo/facts.json?learner=lrn_kabir_singh: the canonical numbers for one learner straight from the data layer,
 * formatted the way screens format them. scripts/e2e/consistency.spec.ts checks every role's screens against these.
 */
export function GET(req: Request) {
  const id = new URL(req.url).searchParams.get('learner') ?? '';
  const student = getStudent(id);
  if (!student) return NextResponse.json({ error: 'unknown learner' }, { status: 404 });
  const gaps = getGaps(id, { status: 'open' });
  const alr = getAlr(id);
  const hours = Math.round(gaps.reduce((a, g) => a + g.hoursToClose, 0) * 10) / 10;
  const band = alr.overall.band ?? student.band;
  const week = getTimetable(id);
  const sessions = getSessions(id, { from: demoNow(), status: 'scheduled' });
  const invoices = getInvoices(id);
  const people = listPersonas();
  return NextResponse.json({
    id,
    name: student.name,
    firstName: student.firstName,
    band,
    bandLabel: BAND_LABEL[band],
    lrs: alr.overall.LRS != null ? alr.overall.LRS.toFixed(2) : null,
    openGaps: gaps.length,
    hoursToClose: formatHours(hours),
    gaps: gaps.map((g) => ({ id: g.id, code: g.code, name: getSubtopic(g.subtopicId)?.name ?? g.subtopicId, hours: formatHours(g.hoursToClose) })),
    // Study blocks only (no buffers), with the "Review 2/5: " prefix screens show as a badge.
    timetableTitles: [...new Set((week?.blocks ?? []).filter((b) => b.kind !== 'buffer').map((b) => b.title.replace(/^Review \d+\/\d+: /, '')))],
    nextSessions: sessions.slice(0, 3).map((s) => ({ id: s.id, title: s.title, hostId: s.hostId })),
    spend: {
      paid: formatInr(invoices.filter((i) => i.status === 'paid').reduce((a, i) => a + i.amountInr, 0)),
      due: formatInr(invoices.filter((i) => i.status !== 'paid').reduce((a, i) => a + i.amountInr, 0)),
      invoices: invoices.length,
    },
    viewers: {
      parents: people.filter((p) => p.role === 'parent' && p.linkedLearnerIds?.includes(id)).map((p) => p.id),
      teachers: people.filter((p) => p.role === 'teacher' && p.linkedLearnerIds?.includes(id)).map((p) => p.id),
      tutors: people.filter((p) => p.role === 'tutor' && p.linkedLearnerIds?.includes(id)).map((p) => p.id),
      teacherSections: people
        .filter((p) => p.role === 'teacher')
        .flatMap((p) => getSections(p.id).filter((sec) => sec.learnerIds.includes(id)).map((sec) => ({ teacherId: p.id, sectionId: sec.id }))),
      counsellors: people.filter((p) => p.role === 'counsellor' && p.linkedLearnerIds?.includes(id)).map((p) => p.id),
    },
  });
}
