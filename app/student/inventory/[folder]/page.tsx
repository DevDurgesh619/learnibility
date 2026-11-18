import Link from 'next/link';
import { notFound } from 'next/navigation';
import { ChevronLeft, FileText, Lock, Sparkles } from 'lucide-react';
import { Badge, Card, EmptyState } from '@/components/ui';
import { fmtDay, inventory, studentCtx, toLocal } from '@/components/student/load';
import { LinkButton } from '@/components/student/link-button';
import { UploadZone } from '@/components/student/upload-zone';
import { cn } from '@/lib/utils';

export const metadata = { title: 'My Inventory · Learnibility' };

const FILTERS = [
  { key: 'all', label: 'All', kinds: [] as string[] },
  { key: 'results', label: 'Results', kinds: ['result', 'transcript'] },
  { key: 'tests', label: 'Tests', kinds: ['test'] },
  { key: 'assessments', label: 'Assessments', kinds: ['assessment'] },
];

/** PDF 4b (folder with files and auto-filed assessment results) and 4c (empty + upload). */
export default async function FolderPage({ params, searchParams }: { params: Promise<{ folder: string }>; searchParams: Promise<{ type?: string }> }) {
  const { folder } = await params;
  const { type } = await searchParams;
  const ctx = await studentCtx();
  const f = inventory(ctx).find((x) => x.slug === folder);
  if (!f) notFound();
  const filter = FILTERS.find((x) => x.key === type) ?? FILTERS[0]!;
  const files = filter.kinds.length ? f.files.filter((x) => filter.kinds.includes(x.kind)) : f.files;
  const chip = (active: boolean) => cn('rounded-full px-3 py-1 text-sm ring-1 ring-inset', active ? 'bg-ink text-white ring-ink' : 'bg-surface text-muted ring-line hover:text-ink');

  return (
    <>
      <div className="mb-4 flex items-center gap-2">
        <Link href="/student/inventory" className="inline-flex items-center gap-1 text-lg text-muted hover:text-ink"><ChevronLeft className="size-4" />Inventory</Link>
        <span className="text-lg text-subtle">/</span>
        <h1 className="text-2xl font-semibold tracking-tight text-ink">{f.name}</h1>
      </div>

      {f.locked ? (
        <EmptyState icon={<Lock />} title="Application documents come with Application Support"
          description="Essays with versions and counsellor comments, your resume and shortlisted universities, all kept together for every application."
          action={<LinkButton href="/student/universities">See Application Support</LinkButton>} />
      ) : f.files.length === 0 ? (
        <UploadZone shelf={f.shelf} folder={f.slug} empty hint={f.hint} />
      ) : (
        <>
          {f.shelf === 'academics' && (
            <div className="mb-3 flex flex-wrap gap-2">
              {FILTERS.map((x) => <Link key={x.key} href={x.key === 'all' ? `?` : `?type=${x.key}`} className={chip(x === filter)}>{x.label}</Link>)}
            </div>
          )}
          <Card className="mb-4">
            {files.length === 0 ? <p className="p-6 text-center text-sm text-muted">No {filter.label.toLowerCase()} in this folder.</p> : (
              <ul className="divide-y divide-line">
                {files.map((d) => (
                  <li key={d.id} className="flex flex-col gap-1 px-4 py-3 sm:flex-row sm:items-center sm:gap-3">
                    <div className="flex min-w-0 flex-1 items-center gap-3">
                      {d.source === 'auto' ? <Sparkles className="size-4 shrink-0 text-brand-600" /> : <FileText className="size-4 shrink-0 text-subtle" />}
                      <p className="truncate text-sm font-medium text-ink">{d.fileName ?? d.title}</p>
                      {d.fileName && d.fileName !== d.title && <span className="hidden truncate text-xs text-muted md:inline">{d.title}</span>}
                    </div>
                    <div className="flex items-center gap-3 pl-7 sm:pl-0">
                      {d.source === 'auto' ? <Badge tone="success">auto-filed</Badge> : <span className="text-xs text-muted">{d.uploadedAt ? `Uploaded ${fmtDay(toLocal(d.uploadedAt).date)}` : ''}</span>}
                      {d.href && <Link href={d.href} className="text-sm font-medium text-brand-700 hover:text-brand-800">{d.kind === 'assessment' ? 'Open gap analysis' : 'Open'}</Link>}
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </Card>
          <UploadZone shelf={f.shelf} folder={f.slug} empty={false} hint={f.hint} />
        </>
      )}
    </>
  );
}
