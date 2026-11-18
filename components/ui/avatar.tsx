import { photoFor } from '@/lib/media';
import { cn } from '@/lib/utils';

const PALETTE = ['bg-brand-100 text-brand-700', 'bg-sky-100 text-sky-700', 'bg-emerald-100 text-emerald-700', 'bg-amber-100 text-amber-700', 'bg-rose-100 text-rose-700', 'bg-violet-100 text-violet-700'];

function hash(s: string) {
  let h = 0;
  for (const c of s) h = (h * 31 + c.charCodeAt(0)) | 0;
  return Math.abs(h);
}

export function initials(name: string) {
  return name.split(/\s+/).filter(Boolean).slice(0, 2).map((p) => p[0]!.toUpperCase()).join('');
}

/**
 * Round avatar: a photo when there is one, otherwise coloured initials.
 * `photo` looks the person up in the bundled profile photos (lib/media) by ID or name.
 */
export function Avatar({ name, src, photo, personId, size = 'md', className }: { name: string; src?: string; photo?: boolean; personId?: string; size?: 'sm' | 'md' | 'lg' | 'xl'; className?: string }) {
  const dims = { sm: 'size-8 text-xs', md: 'size-10 text-sm', lg: 'size-14 text-lg', xl: 'size-20 text-2xl' }[size];
  const image = src ?? (photo ? photoFor(personId) ?? photoFor(name) : undefined);
  if (image) {
    // eslint-disable-next-line @next/next/no-img-element
    return <img src={image} alt={name} loading="lazy" decoding="async" className={cn('shrink-0 rounded-full bg-surface-muted object-cover ring-1 ring-black/5', dims, className)} />;
  }
  return (
    <span aria-hidden className={cn('inline-flex shrink-0 items-center justify-center rounded-full font-semibold', dims, PALETTE[hash(name) % PALETTE.length], className)}>
      {initials(name)}
    </span>
  );
}
