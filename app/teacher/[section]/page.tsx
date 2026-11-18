import { SectionPlaceholder } from '@/components/shell/section-placeholder';

/** Fallback for sidebar sections without a real page yet. Add app/teacher/<section>/page.tsx to replace one. */
export default async function Page({ params }: { params: Promise<{ section: string }> }) {
  const { section } = await params;
  return <SectionPlaceholder role="teacher" slug={section} />;
}
