import { CheckCircle2 } from 'lucide-react';
import type { ReactNode } from 'react';

/** Green confirmation strip shown after a demo write (e.g. ?done=approved). */
export function Notice({ children }: { children: ReactNode }) {
  return (
    <div role="status" className="mb-6 flex items-start gap-2 rounded-lg border border-success-600/20 bg-success-50 px-4 py-3 text-sm text-success-700">
      <CheckCircle2 className="mt-0.5 size-4 shrink-0" />
      <div>{children}</div>
    </div>
  );
}
