import { Lock } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { formatDate } from '@/components/marketplace/dates';
import { studentContext } from '@/components/tutor/model';
import { addNote } from '@/lib/actions/tutor';
import { currentPersona } from '@/lib/session';

/** 4o private notes (manual and from session reports). Only the tutor sees them. */
export default async function Notes({ params }: { params: Promise<{ learnerId: string }> }) {
  const { learnerId } = await params;
  const { ws } = studentContext((await currentPersona())!.id, learnerId)!;
  const notes = ws.notes.filter((n) => n.learnerId === learnerId).slice().reverse();
  return (
    <div className="space-y-4">
      <p className="flex items-center gap-1.5 text-sm text-muted"><Lock className="size-4" /> Only you can see these. Notes from session reports are collected here too.</p>
      <form action={addNote} className="space-y-2 rounded-[var(--radius-card)] border border-line bg-surface p-3">
        <input type="hidden" name="learnerId" value={learnerId} />
        <textarea name="text" required rows={2} placeholder="New note…" className="w-full rounded-lg border border-line p-2 text-sm" />
        <Button size="sm">Save note</Button>
      </form>
      {notes.length === 0 ? <p className="text-sm text-muted">No notes yet.</p> : notes.map((n) => (
        <Card key={n.id} className="p-4">
          <div className="mb-1 flex items-center gap-2 text-xs text-muted"><span>{formatDate(n.createdUtc)}</span><Badge tone={n.source === 'manual' ? 'neutral' : 'brand'}>{n.source === 'manual' ? 'Manual' : 'From session report'}</Badge></div>
          <p className="text-sm text-ink">{n.text}</p>
        </Card>
      ))}
    </div>
  );
}
