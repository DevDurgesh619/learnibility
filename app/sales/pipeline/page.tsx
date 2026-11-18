import { PageHeader, StatTile } from '@/components/ui';
import { PipelineBoard, type BoardCard } from '@/components/crm/pipeline-board';
import { getPackage, isOpen, listLeads, repName, type LeadStatus } from '@/lib/data/crm';
import { DEMO_NOW_ISO } from '@/lib/demo-clock';
import { formatInr } from '@/lib/format';

const COLUMNS: LeadStatus[] = ['new', 'contacted', 'qualified', 'demo_booked', 'demo_done', 'proposal_sent', 'negotiation', 'closed_won'];

export default async function PipelinePage() {
  const now = Date.parse(DEMO_NOW_ISO);
  const leads = listLeads({ status: 'all' }).filter((l) => isOpen(l.status) || ((l.status === 'closed_won' || l.status === 'converted') && now - Date.parse(l.stageChangedUtc) < 30 * 86_400_000));
  const cards: BoardCard[] = leads.map((l) => ({
    id: l.id, title: l.parentName, sub: `${l.studentName} · ${getPackage(l.packageId)?.name ?? `Class ${l.grade} ${l.board.toUpperCase()}`}`,
    valueInr: l.valueInr, score: l.score, owner: repName(l.ownerId), status: l.status,
    badge: l.status === 'converted' ? 'On the platform' : l.status === 'closed_won' ? 'Paid · hand over' : undefined,
  }));
  const open = leads.filter((l) => isOpen(l.status));
  const weighted = open.reduce((s, l) => s + l.valueInr * (l.score / 100), 0);
  return (
    <>
      <PageHeader eyebrow="Sales" title="Pipeline" description="Drag a deal to move it. Closing as won needs a recorded payment; lost needs a reason." />
      <div className="mb-4 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatTile label="Open deals" value={open.length} />
        <StatTile label="Pipeline value" value={formatInr(open.reduce((s, l) => s + l.valueInr, 0))} />
        <StatTile label="Weighted by score" value={formatInr(Math.round(weighted))} />
        <StatTile label="Won, last 30 days" value={leads.length - open.length} />
      </div>
      <PipelineBoard columns={COLUMNS} cards={cards} />
    </>
  );
}
