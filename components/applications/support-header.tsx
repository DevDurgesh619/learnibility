import type { ReactNode } from 'react';
import { Avatar } from '@/components/ui/avatar';
import { LinkTabs } from './ui';

export type SupportTab = 'overview' | 'universities' | 'board' | 'essays' | 'finance' | 'meetings';

/** Application Support header and tabs (PDF 7a: Overview, Universities, Applications, Essays, Finance & Visa, Vault). */
export function SupportHeader({ active, counsellorName, actions }: { active: SupportTab; counsellorName?: string; actions?: ReactNode }) {
  return (
    <>
      <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="mb-1 text-xs font-medium tracking-wide text-brand-600 uppercase">University Fit</p>
          <h1 className="text-2xl font-semibold tracking-tight text-ink">Application Support</h1>
        </div>
        <div className="flex items-center gap-3">
          {actions}
          {counsellorName && (
            <span className="inline-flex items-center gap-2 text-sm text-muted">
              Counsellor <Avatar name={counsellorName} size="sm" photo /> <span className="font-medium text-ink">{counsellorName}</span>
            </span>
          )}
        </div>
      </div>
      <LinkTabs
        active={active}
        tabs={[
          { key: 'overview', label: 'Overview', href: '/student/applications' },
          { key: 'universities', label: 'Universities', href: '/student/applications/universities' },
          { key: 'board', label: 'Applications', href: '/student/applications/board' },
          { key: 'essays', label: 'Essays', href: '/student/applications/essays' },
          { key: 'finance', label: 'Finance & Visa', href: '/student/applications/finance' },
          { key: 'meetings', label: 'Meetings', href: '/student/applications/meetings' },
          { key: 'vault', label: 'Vault', href: '/student/inventory', external: true },
        ]}
      />
    </>
  );
}
