'use client';

import { useState } from 'react';
import { BookOpen, GraduationCap, HeartHandshake, Users } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { chooseRole } from '@/lib/actions/onboarding';

const ROLES = [
  { value: 'student', label: 'Student', hint: 'Class 8 to 12', icon: GraduationCap },
  { value: 'parent', label: 'Parent', hint: 'Follow your child', icon: Users },
  { value: 'counsellor', label: 'Counsellor', hint: 'Guide a caseload', icon: HeartHandshake },
  { value: 'tutor', label: 'Tutor', hint: 'Teach on Learnibility', icon: BookOpen },
] as const;

export function RolePicker() {
  const [role, setRole] = useState<(typeof ROLES)[number]['value']>('student');
  const label = ROLES.find((r) => r.value === role)!.label;
  return (
    <form action={chooseRole} className="flex flex-col items-center gap-6">
      <h1 className="text-2xl font-semibold tracking-tight text-ink">Who are you?</h1>
      <input type="hidden" name="role" value={role} />
      <div role="radiogroup" aria-label="Role" className="grid w-full grid-cols-2 gap-3 sm:grid-cols-4">
        {ROLES.map((r) => {
          const on = r.value === role;
          return (
            <button
              key={r.value}
              type="button"
              role="radio"
              aria-checked={on}
              onClick={() => setRole(r.value)}
              className={cn(
                'flex flex-col items-center gap-2 rounded-xl border bg-surface p-5 text-center transition',
                on ? 'border-brand-500 bg-brand-50 ring-2 ring-brand-200' : 'border-line hover:border-brand-300',
              )}
            >
              <r.icon className={cn('size-7', on ? 'text-brand-600' : 'text-subtle')} />
              <span className="font-medium text-ink">{r.label}</span>
              <span className="text-xs text-muted">{r.hint}</span>
            </button>
          );
        })}
      </div>
      {role !== 'student' && (
        <p className="max-w-md text-center text-sm text-muted">
          In this demo, {label.toLowerCase()}s sign in from the persona picker, where their accounts already have data.
        </p>
      )}
      <Button type="submit" size="lg">{role === 'student' ? 'Continue as Student' : `Open the ${label.toLowerCase()} demo`}</Button>
    </form>
  );
}
