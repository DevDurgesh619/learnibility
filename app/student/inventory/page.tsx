import Link from 'next/link';
import { Lock, Plus } from 'lucide-react';
import { Badge, Card } from '@/components/ui';
import { inventory, SHELF_LABEL, studentCtx, type InventoryFolder, type Shelf } from '@/components/student/load';
import { LinkButton } from '@/components/student/link-button';
import { cn } from '@/lib/utils';

export const metadata = { title: 'My Inventory · Learnibility' };

/** PDF 4a: four shelves of folders; application documents locked for free users. */
export default async function InventoryPage() {
  const ctx = await studentCtx();
  const folders = inventory(ctx);
  const current = folders.find((f) => f.name === `Class ${ctx.grade ?? 9}`) ?? folders[0]!;
  const shelves: Shelf[] = ['academics', 'activities', 'application_documents', 'job_ready'];

  return (
    <>
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-ink">My Inventory</h1>
          <p className="mt-1 text-sm text-muted">Everything you’ve done, in one place. We use it for recommendations and applications.</p>
        </div>
        <LinkButton href={`/student/inventory/${current.slug}`} size="sm"><Plus />Upload</LinkButton>
      </div>
      <div className="grid gap-6 lg:grid-cols-2">
        {shelves.map((s) => (
          <section key={s} className={cn((s === 'academics' || s === 'activities') && 'lg:col-span-2')}>
            <div className="mb-2 flex items-center gap-2 border-b border-dashed border-line pb-1">
              <h2 className="text-sm font-semibold text-ink">{SHELF_LABEL[s]}</h2>
              {s === 'application_documents' && <Badge tone="success">Application Support</Badge>}
            </div>
            <div className={cn('grid gap-3', s === 'academics' || s === 'activities' ? 'grid-cols-2 sm:grid-cols-3 lg:grid-cols-5' : 'grid-cols-2 sm:grid-cols-3')}>
              {folders.filter((f) => f.shelf === s).map((f) => <FolderTile key={f.slug} f={f} />)}
            </div>
          </section>
        ))}
      </div>
    </>
  );
}

function FolderTile({ f }: { f: InventoryFolder }) {
  const n = f.files.length;
  const body = (
    <Card className={cn('h-full p-4 transition-colors', n === 0 && !f.locked && 'border-dashed shadow-none', f.locked ? 'bg-surface-muted/60 opacity-70' : 'group-hover:border-brand-300')}>
      <div className="flex items-start justify-between gap-2">
        <p className="text-sm font-semibold text-ink">{f.name}</p>
        {f.locked && <Lock className="size-3.5 shrink-0 text-subtle" aria-label="Locked" />}
      </div>
      <p className="mt-1 text-xs text-muted">{f.locked ? 'With Application Support' : n ? `${n} file${n === 1 ? '' : 's'}` : 'empty'}</p>
    </Card>
  );
  return f.locked
    ? <Link href="/student/universities" className="group" title="Unlock with Application Support">{body}</Link>
    : <Link href={`/student/inventory/${f.slug}`} className="group">{body}</Link>;
}
