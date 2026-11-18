'use client';

import { useRef, useState, useTransition } from 'react';
import { Upload } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { uploadToInventory } from '@/lib/actions/timetable';
import { cn } from '@/lib/utils';

const ACCEPT = '.pdf,.jpg,.jpeg,.png';
const MAX = 20 * 1024 * 1024;

/** PDF 4c: drop or choose files. Demo: only the file names are kept. */
export function UploadZone({ shelf, folder, empty, hint }: { shelf: 'academics' | 'activities' | 'application_documents' | 'job_ready'; folder: string; empty: boolean; hint: string }) {
  const input = useRef<HTMLInputElement>(null);
  const [over, setOver] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);
  const [pending, start] = useTransition();

  const send = (files: FileList | null) => {
    if (!files?.length) return;
    const ok = [...files].filter((f) => f.size <= MAX && /\.(pdf|jpe?g|png)$/i.test(f.name));
    const skipped = files.length - ok.length;
    start(async () => {
      if (ok.length) await uploadToInventory(shelf, folder, ok.map((f) => ({ name: f.name, sizeKb: Math.max(1, Math.round(f.size / 1024)) })));
      setMsg(`${ok.length} file${ok.length === 1 ? '' : 's'} added${skipped ? `; ${skipped} skipped (PDF, JPG or PNG up to 20 MB)` : ''}.`);
    });
  };

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setOver(true); }}
      onDragLeave={() => setOver(false)}
      onDrop={(e) => { e.preventDefault(); setOver(false); send(e.dataTransfer.files); }}
      className={cn('flex flex-col items-center justify-center rounded-[var(--radius-card)] border-2 border-dashed px-6 text-center transition-colors',
        empty ? 'py-16' : 'py-6', over ? 'border-brand-500 bg-brand-50' : 'border-line bg-surface')}
    >
      {empty && <p className="text-base font-semibold text-ink">Nothing here yet</p>}
      <p className="mt-1 text-sm text-muted">{empty ? hint : 'Drop more files here.'} PDF, JPG, PNG · max 20 MB</p>
      <input ref={input} type="file" multiple accept={ACCEPT} className="sr-only" onChange={(e) => send(e.target.files)} aria-label="Choose files" />
      <Button className="mt-3" size="sm" disabled={pending} onClick={() => input.current?.click()}><Upload />{pending ? 'Uploading…' : 'Choose files'}</Button>
      {msg && <p role="status" className="mt-2 text-xs text-success-700">{msg}</p>}
    </div>
  );
}
