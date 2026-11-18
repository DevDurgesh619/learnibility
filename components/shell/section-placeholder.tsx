import { notFound } from 'next/navigation';
import { Hammer } from 'lucide-react';
import { EmptyState } from '@/components/ui/empty-state';
import { PageHeader } from '@/components/ui/page-header';
import { findNavItem, ROLE_LABEL } from '@/lib/nav';
import type { Role } from '@/lib/types';

/** Placeholder for a sidebar section whose real screen has not been built yet. */
export function SectionPlaceholder({ role, slug }: { role: Role; slug: string }) {
  const item = findNavItem(role, slug);
  if (!item) notFound();
  return (
    <>
      <PageHeader eyebrow={ROLE_LABEL[role]} title={item.label} description={item.blurb} />
      <EmptyState icon={<Hammer />} title="This screen is on its way" description={`${item.label} is being built. The sidebar, sign-in and data underneath it are ready.`} />
    </>
  );
}
