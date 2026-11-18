'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Check, ChevronLeft, ClipboardCheck, Compass, GraduationCap, Users } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { saveNeeds } from '@/lib/actions/onboarding';
import { NEEDS, type Need } from './draft';

const ICON: Record<Need, typeof Users> = { tutors: Users, progress: ClipboardCheck, applications: GraduationCap, career: Compass };

export function NeedsForm({ initial, grade }: { initial: Need[]; grade?: number }) {
  const [sel, setSel] = useState<Need[]>(initial);
  const toggle = (n: Need) => setSel((s) => (s.includes(n) ? s.filter((x) => x !== n) : [...s, n]));
  return (
    <form action={saveNeeds} className="mt-6">
      <div className="grid gap-3 sm:grid-cols-2">
        {NEEDS.map((n) => {
          const on = sel.includes(n.value);
          const Icon = ICON[n.value];
          return (
            <button
              key={n.value}
              type="button"
              aria-pressed={on}
              onClick={() => toggle(n.value)}
              className={cn('relative flex items-start gap-3 rounded-xl border bg-surface p-4 text-left transition', on ? 'border-brand-500 bg-brand-50 ring-2 ring-brand-200' : 'border-line hover:border-brand-300')}
            >
              <Icon className={cn('mt-0.5 size-5 shrink-0', on ? 'text-brand-600' : 'text-subtle')} />
              <span>
                <span className="block font-medium text-ink">{n.label}</span>
                <span className="mt-0.5 block text-sm text-muted">{n.hint}</span>
                {n.value === 'applications' && grade !== undefined && grade < 11 && (
                  <span className="mt-1 block text-xs text-subtle">Most students start this in class 11. You can explore University Fit any time.</span>
                )}
              </span>
              {on && <Check className="absolute right-3 top-3 size-4 text-brand-600" />}
              {on && <input type="hidden" name="needs" value={n.value} />}
            </button>
          );
        })}
      </div>
      <div className="mt-6 flex flex-wrap items-center justify-between gap-3">
        <Link href="/onboarding/about" className="inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" /> Back</Link>
        <div className="flex items-center gap-2">
          <Button type="submit" name="all" value="1" variant="ghost">Not sure, show me everything</Button>
          <Button type="submit" disabled={sel.length === 0}>Continue</Button>
        </div>
      </div>
    </form>
  );
}
