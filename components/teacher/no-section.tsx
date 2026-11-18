import { School } from 'lucide-react';
import { EmptyState } from '@/components/ui/empty-state';
import { PageHeader } from '@/components/ui/page-header';

/** Shown when the signed-in teacher has no sections yet (or the data has not loaded). */
export function NoSection({ title, description }: { title: string; description: string }) {
  return (
    <>
      <PageHeader eyebrow="School teacher" title={title} description={description} />
      <EmptyState icon={<School />} title="No sections yet" description="When your school links a class to you, its students, mastery and gaps show up here." />
    </>
  );
}
