import { CalendarCheck } from 'lucide-react';
import { DayPlan } from '@/components/counsellor/day-plan';
import { FilterChips } from '@/components/counsellor/filter-chips';
import { loadRequests } from '@/components/counsellor/load';
import { RequestCard } from '@/components/counsellor/request-card';
import { EmptyState, PageHeader } from '@/components/ui';

export const dynamic = 'force-dynamic';

export default async function TimetableRequestsPage({ searchParams }: { searchParams: Promise<{ status?: string; student?: string; done?: string }> }) {
  const sp = await searchParams;
  const { items, now, students } = await loadRequests();
  const byStudent = sp.student ? items.filter((i) => i.request.learnerId === sp.student) : items;
  const pending = byStudent.filter((i) => i.request.status === 'pending');
  const decided = byStudent.filter((i) => i.request.status !== 'pending');
  const list = sp.status === 'decided' ? decided : pending;
  const done = sp.done ? items.find((i) => i.request.id === sp.done) : undefined;
  const studentName = sp.student ? students.find((s) => s.id === sp.student)?.name : undefined;

  return (
    <>
      <PageHeader eyebrow="Counsellor" title="Timetable requests" description="Students ask for schedule changes here. Approving re-plans the rest of their week straight away." />
      {done && (
        <div className="mb-6 rounded-[var(--radius-card)] border border-success-600/20 bg-success-50 p-4">
          <p className="flex items-center gap-2 font-medium text-success-700"><CalendarCheck className="size-4" />
            {done.request.status === 'declined' ? `Declined. ${done.studentName.split(' ')[0]} has been told why.` : `Approved. ${done.studentName.split(' ')[0]}'s week has been re-planned.`}
          </p>
          {done.request.status !== 'declined' && done.after && <div className="mt-3"><DayPlan week={done.after} highlight={done.changedBlockIds} /></div>}
        </div>
      )}
      <div className="mb-4 flex flex-wrap items-center gap-3">
        <FilterChips base="/counsellor/timetable-requests" param="status" value={sp.status} keep={{ student: sp.student }} options={[
          { value: '', label: 'Pending', count: pending.length }, { value: 'decided', label: 'Decided', count: decided.length },
        ]} />
        {studentName && <FilterChips base="/counsellor/timetable-requests" param="student" value={sp.student} keep={{ status: sp.status }} options={[{ value: sp.student!, label: studentName }, { value: '', label: 'Show everyone' }]} />}
      </div>
      {list.length === 0 ? (
        <EmptyState icon={<CalendarCheck />} title={sp.status === 'decided' ? 'No decided requests yet' : 'No requests waiting'}
          description={sp.status === 'decided' ? 'Approved and declined requests show here.' : 'When a student asks to change their timetable, it lands here for you.'} />
      ) : (
        <div className="space-y-4">
          {list.map((i) => <RequestCard key={i.request.id} request={i.request} studentName={i.studentName} blocks={i.blocks} now={now} />)}
        </div>
      )}
    </>
  );
}
