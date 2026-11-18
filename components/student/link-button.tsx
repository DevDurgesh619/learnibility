import Link from 'next/link';
import type { ComponentProps } from 'react';
import { buttonVariants } from '@/components/ui/button';
import { cn } from '@/lib/utils';

/** A Next link styled as a Button (avoids nesting a button inside an anchor). */
export function LinkButton({ variant, size, className, ...props }: ComponentProps<typeof Link> & { variant?: 'primary' | 'secondary' | 'ghost'; size?: 'sm' | 'md' | 'lg' }) {
  return <Link className={cn(buttonVariants({ variant, size }), className)} {...props} />;
}
