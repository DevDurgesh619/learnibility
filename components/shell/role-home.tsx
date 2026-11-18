import { Sparkles } from 'lucide-react';
import { EmptyState } from '@/components/ui/empty-state';
import { PageHeader } from '@/components/ui/page-header';
import { StatTile } from '@/components/ui/stat-tile';
import { NAV, ROLE_LABEL } from '@/lib/nav';
import { currentPersona } from '@/lib/session';
import type { Role } from '@/lib/types';

const TILES: Record<Role, string[]> = {
  student: ['Learning rate', 'Retention', 'Open gaps', 'Tasks this week'],
  parent: ['Weekly progress', 'Open gaps', 'Spend this month', 'Next deadline'],
  teacher: ['Students', 'Average mastery', 'Gap clusters', 'Diagnoses to validate'],
  counsellor: ['Caseload', 'Risk flags', 'Requests to approve', 'Drafts to review'],
  tutor: ['New requests', 'Sessions this week', 'Earnings this month', 'Rating'],
  mentor: ['Mentees', 'Sessions this month', 'Open action items', 'Skill plans'],
};

/** Placeholder role home until the role's real home screen lands. */
export async function RoleHome({ role }: { role: Role }) {
  const persona = await currentPersona();
  const first = persona?.name.split(' ')[0] ?? 'there';
  return (
    <>
      <PageHeader eyebrow={ROLE_LABEL[role]} title={`Hi ${first}`} description={NAV[role][0]!.blurb} />
      <div className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        {TILES[role].map((label) => (
          <StatTile key={label} label={label} value="—" hint="Fills in once your data loads" />
        ))}
      </div>
      <EmptyState icon={<Sparkles />} title="Your dashboard is being set up" description="This is the shell for your role. Screens arrive section by section in the sidebar." />
    </>
  );
}
