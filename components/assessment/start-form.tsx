'use client';

import { useState } from 'react';
import Link from 'next/link';
import { buttonVariants } from '@/components/ui/button';
import { cn } from '@/lib/utils';

export function StartForm({ href }: { href: string }) {
  const [ok, setOk] = useState(false);
  return (
    <div className="mt-6 flex flex-col gap-4 border-t border-line pt-4 sm:flex-row sm:items-center sm:justify-between">
      <label className="flex items-center gap-2 text-sm text-ink">
        <input type="checkbox" checked={ok} onChange={(e) => setOk(e.target.checked)} className="size-4 accent-[var(--color-brand-600)]" />
        I&apos;ve read the instructions
      </label>
      <Link href={href} aria-disabled={!ok} tabIndex={ok ? 0 : -1} className={cn(buttonVariants(), !ok && 'pointer-events-none opacity-50')}>
        Start test now
      </Link>
    </div>
  );
}
