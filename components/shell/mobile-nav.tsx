'use client';

import { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import { Menu, X } from 'lucide-react';
import type { NavItem } from '@/lib/nav';
import type { Role } from '@/lib/types';
import { SidebarNav } from './sidebar-nav';
import { Logo } from './logo';

export function MobileNav({ role, items }: { role: Role; items: NavItem[] }) {
  const [open, setOpen] = useState(false);
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  return (
    <>
      <button className="rounded-lg p-2 text-muted hover:bg-surface-muted lg:hidden" onClick={() => setOpen(true)} aria-label="Open menu">
        <Menu className="size-5" />
      </button>
      {open && mounted && createPortal(
        <div className="fixed inset-0 z-50 lg:hidden" role="dialog" aria-modal="true">
          <div className="absolute inset-0 bg-ink/30" onClick={() => setOpen(false)} />
          <div className="absolute inset-y-0 left-0 flex w-72 flex-col gap-6 bg-surface p-4 shadow-xl">
            <div className="flex items-center justify-between">
              <Logo href={`/${role}`} />
              <button className="rounded-lg p-2 text-muted hover:bg-surface-muted" onClick={() => setOpen(false)} aria-label="Close menu">
                <X className="size-5" />
              </button>
            </div>
            <SidebarNav role={role} items={items} onNavigate={() => setOpen(false)} />
          </div>
        </div>,
        // Portal: the sticky header uses backdrop-blur, which would trap a fixed-position drawer inside it.
        document.body,
      )}
    </>
  );
}
