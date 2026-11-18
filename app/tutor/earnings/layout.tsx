import { LinkTabs } from '@/components/tutor/tabs';

/** Tutor HTML 7a-7c share one header and sub-nav. */
export default function EarningsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="mx-auto max-w-5xl">
      <h1 className="mb-4 text-2xl font-semibold text-ink">Earnings</h1>
      <LinkTabs className="mb-6" tabs={[{ href: '/tutor/earnings', label: 'Overview' }, { href: '/tutor/earnings/transactions', label: 'Transactions & payouts' }, { href: '/tutor/earnings/settings', label: 'Payout settings' }]} />
      {children}
    </div>
  );
}
