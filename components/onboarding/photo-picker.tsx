'use client';

import { useEffect, useRef, useState } from 'react';
import { Camera } from 'lucide-react';
import { Avatar } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';

/**
 * Profile photo step. The demo keeps the chosen photo in the browser only (nothing is uploaded);
 * "Use demo photo" fills in the persona's bundled photo so a presenter can move on in one click.
 */
export function PhotoPicker({ name, demoPhoto }: { name: string; demoPhoto?: string }) {
  const [src, setSrc] = useState<string | undefined>();
  const input = useRef<HTMLInputElement>(null);
  useEffect(() => () => { if (src?.startsWith('blob:')) URL.revokeObjectURL(src); }, [src]);
  return (
    <div className="flex items-center gap-4 rounded-xl border border-line bg-surface p-4">
      <div className="relative">
        <Avatar name={name} src={src} size="xl" />
        <button type="button" onClick={() => input.current?.click()} aria-label="Choose a profile photo"
          className="absolute -right-1 -bottom-1 flex size-7 items-center justify-center rounded-full bg-brand-600 text-white shadow ring-2 ring-white hover:bg-brand-700">
          <Camera className="size-3.5" />
        </button>
      </div>
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium text-ink">Profile photo <span className="font-normal text-subtle">(optional)</span></p>
        <p className="mt-0.5 text-xs text-muted">Tutors and your counsellor see it. Only a clear photo of your face, please.</p>
        <div className="mt-2 flex flex-wrap gap-2">
          <Button type="button" size="sm" variant="secondary" onClick={() => input.current?.click()}>{src ? 'Change photo' : 'Upload photo'}</Button>
          {demoPhoto && !src && <Button type="button" size="sm" variant="ghost" onClick={() => setSrc(demoPhoto)}>Use demo photo</Button>}
          {src && <Button type="button" size="sm" variant="ghost" onClick={() => setSrc(undefined)}>Remove</Button>}
        </div>
      </div>
      <input ref={input} type="file" accept="image/*" className="hidden"
        onChange={(e) => { const f = e.target.files?.[0]; if (f) setSrc(URL.createObjectURL(f)); }} />
    </div>
  );
}
