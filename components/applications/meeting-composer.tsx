'use client';

import { useState, useTransition } from 'react';
import { useRouter } from 'next/navigation';
import { Loader2, Sparkles, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { saveMeetingNote } from '@/lib/actions/applications';
import { extractActionItems } from './ai';

/** Meeting intelligence: notes in, summary and action items out; saving turns items into the student's tasks. */
export function MeetingComposer({ learnerId, studentFirst, today }: { learnerId: string; studentFirst: string; today: string }) {
  const router = useRouter();
  const [notes, setNotes] = useState('');
  const [summary, setSummary] = useState('');
  const [decisions, setDecisions] = useState('');
  const [items, setItems] = useState<{ title: string; dueOn: string }[] | null>(null);
  const [msg, setMsg] = useState<string | null>(null);
  const [pending, start] = useTransition();
  const field = 'mt-1 w-full rounded-lg border border-line p-2 text-sm';

  function extract() {
    const found = extractActionItems(notes, studentFirst, today);
    setItems(found);
    if (!summary.trim()) {
      const first = notes.split(/\n/).map((l) => l.trim()).filter(Boolean).filter((l) => !found.some((f) => l.toLowerCase().includes(f.title.toLowerCase().slice(0, 20))));
      setSummary(first.slice(0, 2).join(' ').slice(0, 280));
    }
  }

  return (
    <Card>
      <CardHeader title="New meeting note" description={`Paste or type your notes. Action items become ${studentFirst}'s timetable tasks.`} />
      <CardBody className="space-y-3 pt-3">
        <label className="block text-sm font-medium text-ink">Notes
          <textarea value={notes} onChange={(e) => setNotes(e.target.value)} rows={5} className={field} placeholder={`e.g. Talked through the Rotman answers.\n${studentFirst} will send the revised initiative answer by 25 Nov.\nAsk Ms Raman to upload the reference by Friday.`} />
        </label>
        <Button size="sm" variant="secondary" type="button" disabled={!notes.trim()} onClick={extract}><Sparkles />Extract summary and action items</Button>
        {items && (
          <>
            <label className="block text-sm font-medium text-ink">Summary
              <textarea value={summary} onChange={(e) => setSummary(e.target.value)} rows={2} className={field} />
            </label>
            <label className="block text-sm font-medium text-ink">Decisions (one per line)
              <textarea value={decisions} onChange={(e) => setDecisions(e.target.value)} rows={2} className={field} />
            </label>
            <div>
              <p className="text-sm font-medium text-ink">Action items</p>
              {items.length === 0 && <p className="text-xs text-muted">None found. Start a line with a verb, like “Send…” or “Finish…”.</p>}
              <ul className="mt-1 space-y-2">
                {items.map((it, i) => (
                  <li key={i} className="flex gap-2">
                    <input value={it.title} aria-label="Action item" onChange={(e) => setItems(items.map((x, j) => (j === i ? { ...x, title: e.target.value } : x)))} className="h-9 min-w-0 flex-1 rounded-lg border border-line px-2 text-sm" />
                    <input type="date" value={it.dueOn} aria-label="Due date" onChange={(e) => setItems(items.map((x, j) => (j === i ? { ...x, dueOn: e.target.value } : x)))} className="h-9 rounded-lg border border-line px-2 text-sm" />
                    <button type="button" aria-label="Remove" onClick={() => setItems(items.filter((_, j) => j !== i))} className="text-subtle hover:text-ink"><X className="size-4" /></button>
                  </li>
                ))}
              </ul>
              <button type="button" className="mt-2 text-xs font-medium text-brand-700 hover:underline" onClick={() => setItems([...items, { title: '', dueOn: today }])}>Add item</button>
            </div>
            <div className="flex items-center gap-3">
              <Button size="sm" disabled={pending} onClick={() => start(async () => {
                await saveMeetingNote(learnerId, { summary, notes, decisions, items: items.filter((i) => i.title.trim()) });
                setNotes(''); setSummary(''); setDecisions(''); setItems(null);
                setMsg(`Saved. ${studentFirst} has the action items in their timetable.`);
                router.refresh();
              })}>{pending && <Loader2 className="animate-spin" />}Save note and assign tasks</Button>
            </div>
          </>
        )}
        {msg && <p role="status" className="text-sm text-success-700">{msg}</p>}
      </CardBody>
    </Card>
  );
}
