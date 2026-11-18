import type { ReactNode } from 'react';

/** Public entry screens (PDF 1a-1d): no sidebar, no persona required. */
export default function EntryLayout({ children }: { children: ReactNode }) {
  return <div className="min-h-screen bg-canvas">{children}</div>;
}
