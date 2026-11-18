import Link from 'next/link';
import { cn } from '@/lib/utils';

export function CareerTabs({ active }: { active: 'fit' | 'insights' }) {
  const tab = (on: boolean) => cn('-mb-px border-b-2 px-1 pb-2 text-sm font-medium', on ? 'border-brand-600 text-ink' : 'border-transparent text-muted hover:text-ink');
  return (
    <nav className="mb-6 flex gap-6 border-b border-line" aria-label="Career sections">
      <Link href="/student/career" className={tab(active === 'fit')}>Career Fit</Link>
      <Link href="/student/career?tab=insights" className={tab(active === 'insights')}>Job Insights</Link>
    </nav>
  );
}

export function FitPill({ score }: { score: number }) {
  return <span className="whitespace-nowrap rounded-full bg-success-50 px-2 py-0.5 text-xs font-semibold text-success-700 ring-1 ring-inset ring-success-600/20">{Math.round(score)}% fit</span>;
}

export function SkillChip({ children, tone = 'outline' }: { children: React.ReactNode; tone?: 'outline' | 'solid' | 'missing' }) {
  return (
    <span className={cn('inline-flex rounded-full px-2.5 py-1 text-xs font-medium', tone === 'solid' ? 'bg-ink text-white' : tone === 'missing' ? 'bg-warning-50 text-warning-700 ring-1 ring-inset ring-warning-600/30' : 'bg-surface text-ink ring-1 ring-inset ring-line')}>
      {children}
    </span>
  );
}
