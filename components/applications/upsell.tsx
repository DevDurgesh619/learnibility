import Link from 'next/link';
import { Sparkles } from 'lucide-react';
import { buttonVariants } from '@/components/ui/button';
import { cn } from '@/lib/utils';

/** Upgrade prompt into Application Support (PDF 6a banner, 6g funnel card). */
export function Upsell({ variant = 'banner' }: { variant?: 'banner' | 'funnel' }) {
  if (variant === 'funnel') {
    return (
      <div className="mt-6 rounded-[var(--radius-card)] border border-success-600/30 bg-success-50 p-5 sm:p-6">
        <p className="text-base font-semibold text-ink">Turn this into applications.</p>
        <p className="mt-1 max-w-2xl text-sm text-muted">A counsellor builds your shortlist, reviews every essay with you and tracks each deadline, document and recommendation letter. Application Support.</p>
        <ul className="mt-3 grid gap-1 text-sm text-ink sm:grid-cols-3">
          <li>✓ Applications board and QA check</li>
          <li>✓ Essay reviews with your counsellor</li>
          <li>✓ Finance, scholarships and visa</li>
        </ul>
        <Link href="/student/applications/upgrade" className={cn(buttonVariants(), 'mt-4')}><Sparkles />Get Application Support</Link>
      </div>
    );
  }
  return (
    <div className="mt-6 rounded-[var(--radius-card)] border border-dashed border-line bg-surface p-5">
      <p className="text-sm text-ink"><span className="font-semibold">Want someone to handle the applications?</span> <span className="text-muted">Shortlist, essays, documents, visa: with a counsellor.</span></p>
      <Link href="/student/applications/upgrade" className={cn(buttonVariants({ variant: 'secondary', size: 'sm' }), 'mt-3 border-success-600/40 text-success-700')}>Application Support</Link>
    </div>
  );
}
