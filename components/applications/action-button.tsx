'use client';

import { useState, useTransition, type ReactNode } from 'react';
import { Loader2 } from 'lucide-react';
import { Button, type ButtonProps } from '@/components/ui/button';

/** A button that runs a server action, shows a spinner while it runs and the error if it fails. */
export function ActionButton({
  action, children, pendingLabel, done, ...props
}: Omit<ButtonProps, 'onClick' | 'action'> & { action: () => Promise<unknown>; pendingLabel?: string; done?: ReactNode }) {
  const [pending, start] = useTransition();
  const [error, setError] = useState<string | null>(null);
  const [ok, setOk] = useState(false);
  return (
    <span className="inline-flex flex-col items-start gap-1">
      <Button
        {...props}
        disabled={pending || props.disabled}
        onClick={() =>
          start(async () => {
            setError(null);
            try {
              await action();
              setOk(true);
            } catch (e) {
              setError(e instanceof Error ? e.message : 'Something went wrong.');
            }
          })
        }
      >
        {pending ? <><Loader2 className="animate-spin" />{pendingLabel ?? children}</> : ok && done ? done : children}
      </Button>
      {error && <span role="alert" className="text-xs text-danger-700">{error}</span>}
    </span>
  );
}
