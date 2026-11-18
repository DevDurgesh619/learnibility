import { toIcs } from '@/lib/engines';
import { nowUtc, studentCtx, weekTimetable } from '@/components/student/load';

/** PDF 3a: export this week's plan as an .ics file (engine toIcs; buffers left out). */
export async function GET() {
  const ctx = await studentCtx();
  const tt = weekTimetable(ctx);
  if (!tt) return new Response('No timetable yet. Take your first assessment to get one.', { status: 404 });
  const ics = toIcs(tt.blocks.filter((b) => b.endUtc > nowUtc()), { now: nowUtc(), calendarName: `Learnibility · ${ctx.name}` });
  return new Response(ics, {
    headers: {
      'Content-Type': 'text/calendar; charset=utf-8',
      'Content-Disposition': `attachment; filename="learnibility-week-${tt.weekStart}.ics"`,
    },
  });
}
