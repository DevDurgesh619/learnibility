import { PageHeader } from '@/components/ui/page-header';
import { LinkTabs } from './ui';

export function FitHeader({ active, title = 'University Fit', description }: { active: 'explore' | 'best-fit'; title?: string; description?: string }) {
  return (
    <>
      <PageHeader title={title} description={description ?? 'Find universities with every detail that matters: courses, deadlines, scores and costs.'} />
      <LinkTabs
        active={active}
        tabs={[
          { key: 'explore', label: 'Explore', href: '/student/universities' },
          { key: 'best-fit', label: 'Best fit for me', href: '/student/universities/best-fit' },
        ]}
      />
    </>
  );
}
