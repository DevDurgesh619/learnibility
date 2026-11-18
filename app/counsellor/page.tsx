import Link from 'next/link';
import { AlertTriangle, CalendarClock, ClipboardCheck, Users } from 'lucide-react';
import { CaseloadList, FlagChip } from '@/components/counsellor/caseload-list';
import { FilterChips } from '@/components/counsellor/filter-chips';
import { formatTime } from '@/components/counsellor/format';
import { loadCaseload } from '@/components/counsellor/load';
import { Avatar, Button, Card, CardBody, CardHeader, EmptyState, PageHeader, StatTile } from '@/components/ui';

export const dynamic = 'force-dynamic';

export default async function CaseloadPage({ searchParams }: { searchParams: Promise<{ show?: string; q?: string }> }) {
  const { show, q } = await searchParams;
  const { counsellor, entries, sessionsToday, now } = await loadCaseload();
  const first = counsellor.name.split(' ')[0];
  const today = entries.filter((e) => e.needsYouToday);
  const flagged = entries.filter((e) => e.flags.length > 0);
  const requests = entries.reduce((s, e) => s + e.pendingRequests, 0);
  const flagCount = entries.reduce((s, e) => s + e.flags.length, 0);
  const needle = q?.trim().toLowerCase();
  const visible = (show === 'today' ? today : show === 'flagged' ? flagged : entries)
    .filter((e) => !needle || e.student.name.toLowerCase().includes(needle) || e.student.programme.toLowerCase().includes(needle));

  return (
    <>
      <PageHeader eyebrow="Counsellor" title={`Good morning, ${first}`} description={`${today.length} student${today.length === 1 ? '' : 's'} need you today. Everything else can wait.`}
        actions={<Link href="/counsellor/timetable-requests"><Button variant="secondary"><CalendarClock />Requests ({requests})</Button></Link>} />

      <div className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatTile label="Caseload" value={entries.length} hint="students" icon={<Users />} />
        <StatTile label="Risk flags" value={flagCount} hint={`${entries.filter((e) => e.flags.some((f) => f.severity === 'high')).length} students with a high flag`} icon={<AlertTriangle />} />
        <StatTile label="Requests to approve" value={requests} hint="timetable changes" icon={<CalendarClock />} />
        <StatTile label="Sessions today" value={sessionsToday.length} hint={sessionsToday[0] ? `Next at ${formatTime(sessionsToday[0].startUtc)}` : 'Nothing booked'} icon={<ClipboardCheck />} />
      </div>

      <Card className="mb-6">
        <CardHeader title="Needs you today" description="High flags, waiting requests and today's sessions" />
        <CardBody>
          {today.length === 0 ? (
            <EmptyState title="Nothing urgent today" description="No high flags, waiting requests or sessions. A good day for check-ins." className="border-0 py-6" />
          ) : (
            <ul className="grid gap-3 md:grid-cols-2">
              {today.map((e) => (
                <li key={e.student.id} className="rounded-lg border border-line p-4">
                  <div className="flex items-center gap-3">
                    <Avatar name={e.student.name} src={e.student.avatar} size="sm" />
                    <div className="min-w-0 flex-1">
                      <div className="font-medium text-ink">{e.student.name}</div>
                      <div className="truncate text-xs text-muted">{e.student.programme} · {e.focus}</div>
                    </div>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-1">{e.flags.filter((f) => f.severity !== 'low').slice(0, 3).map((f, i) => <FlagChip key={i} flag={f} />)}</div>
                  <div className="mt-3 flex flex-wrap gap-2 text-sm">
                    {e.pendingRequests > 0 && <Link className="font-medium text-brand-700 hover:underline" href={`/counsellor/timetable-requests?student=${e.student.id}`}>Review request</Link>}
                    <Link className="font-medium text-brand-700 hover:underline" href={`/counsellor/student-360?student=${e.student.id}`}>Open Student 360</Link>
                    <Link className="font-medium text-brand-700 hover:underline" href={`/counsellor/career-sessions?student=${e.student.id}`}>Career session</Link>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </CardBody>
      </Card>

      <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <FilterChips base="/counsellor" param="show" value={show} keep={{ q }} options={[
          { value: '', label: 'All students', count: entries.length },
          { value: 'today', label: 'Needs you today', count: today.length },
          { value: 'flagged', label: 'Flagged', count: flagged.length },
        ]} />
        <form className="flex gap-2" action="/counsellor">
          {show && <input type="hidden" name="show" value={show} />}
          <input name="q" defaultValue={q} placeholder="Search students" className="h-10 w-full rounded-lg border border-line bg-surface px-3 text-sm sm:w-64" aria-label="Search students" />
        </form>
      </div>
      {visible.length ? <CaseloadList entries={visible} /> : <EmptyState title="No students match" description="Try another filter or clear the search." />}
    </>
  );
}
