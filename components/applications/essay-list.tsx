import Link from 'next/link';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import { EmptyState } from '@/components/ui/empty-state';
import type { Application } from '@/lib/data/types';
import type { University } from '@/lib/types';
import { fmtDate, latestVersion, shortPrompt, wordCount } from './logic';

export function EssayList({ apps, unis, hrefFor, counsellorFirst, studentNames }: { apps: Application[]; unis: Map<string, University>; hrefFor: (id: string) => string; counsellorFirst?: string; studentNames?: Record<string, string> }) {
  const rows = apps.flatMap((a) => a.essays.map((e) => ({ a, e })));
  if (!rows.length) return <EmptyState title="No essays yet" description="Essays appear here when an application on your board asks for one." />;
  return (
    <Card className="divide-y divide-line">
      {rows.map(({ a, e }) => {
        const v = latestVersion(e);
        const open = e.comments.filter((c) => !c.resolved && !c.parentId && c.version === v.version).length;
        return (
          <Link key={e.id} href={hrefFor(e.id)} className="flex flex-col gap-2 p-4 hover:bg-surface-muted/50 sm:flex-row sm:items-center sm:justify-between">
            <div className="min-w-0">
              {studentNames && <p className="text-xs font-medium text-brand-700">{studentNames[a.learnerId]}</p>}
              <p className="font-medium text-ink">{shortPrompt(e.prompt)} · {unis.get(a.universityId)?.shortName}</p>
              <p className="text-xs text-muted">v{v.version} saved {fmtDate(v.createdAt)} · {wordCount(v.text)} / {e.wordLimit} words · {open} open comment{open === 1 ? '' : 's'}</p>
            </div>
            <Badge tone={e.status === 'final' ? 'success' : e.status === 'in_review' ? 'info' : 'warning'}>{e.status === 'final' ? 'Final' : e.status === 'in_review' ? (counsellorFirst ? `With ${counsellorFirst}` : 'Waiting for review') : 'Drafting'}</Badge>
          </Link>
        );
      })}
    </Card>
  );
}
