'use client';

import { useFormStatus } from 'react-dom';
import { Button, type ButtonProps } from '@/components/ui/button';

/** Submit button that shows a pending state while its server action runs. */
export function Submit({ children, pendingText, ...props }: ButtonProps & { pendingText?: string }) {
  const { pending } = useFormStatus();
  return (
    <Button type="submit" disabled={pending || props.disabled} {...props}>
      {pending ? pendingText ?? 'Saving…' : children}
    </Button>
  );
}
