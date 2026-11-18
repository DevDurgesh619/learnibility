import type { ReactNode } from 'react';
import Link from 'next/link';
import { Logo } from '@/components/shell/logo';

/** Centred card used by 1b-1d. */
export function AuthFrame({ children, wide = false }: { children: ReactNode; wide?: boolean }) {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="mx-auto flex w-full max-w-6xl items-center justify-between p-4 sm:p-6">
        <Logo href="/welcome" />
        <Link href="/login" className="text-sm text-muted hover:text-ink">Demo persona picker</Link>
      </header>
      <main className="flex flex-1 items-start justify-center px-4 pb-16 pt-6 sm:items-center sm:pt-0">
        <div className={wide ? 'w-full max-w-3xl' : 'w-full max-w-md'}>{children}</div>
      </main>
    </div>
  );
}
