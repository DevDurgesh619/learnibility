'use client';

import { useMemo, useState } from 'react';
import { Send } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

export interface AssignFormProps {
  action: (fd: FormData) => Promise<void>;
  sectionId: string;
  chapters: { id: string; label: string; subtopics: { id: string; label: string }[] }[];
  students: { id: string; name: string }[];
  /** Named groups (gap clusters) the teacher can pick in one click. */
  groups: { key: string; label: string; learnerIds: string[]; subtopicId: string; code: string }[];
  today: string;
  defaults: { kind: 'chapter_check' | 'reteach'; chapterId?: string; subtopicId?: string; code?: string; learnerIds?: string[]; dueDate: string };
}

const field = 'h-10 w-full rounded-lg border border-line bg-surface px-3 text-sm text-ink shadow-sm focus:border-brand-400 focus:outline-none';

export function AssignForm({ action, sectionId, chapters, students, groups, today, defaults }: AssignFormProps) {
  const [kind, setKind] = useState(defaults.kind);
  const initialChapter = defaults.chapterId ?? chapters.find((c) => c.subtopics.some((s) => s.id === defaults.subtopicId))?.id ?? chapters[0]?.id ?? '';
  const [chapterId, setChapterId] = useState(initialChapter);
  const subtopics = useMemo(() => chapters.find((c) => c.id === chapterId)?.subtopics ?? [], [chapters, chapterId]);
  const [subtopicId, setSubtopicId] = useState(defaults.subtopicId ?? subtopics[0]?.id ?? '');
  const [code, setCode] = useState(defaults.code ?? '');
  const [whole, setWhole] = useState(!defaults.learnerIds?.length);
  const [picked, setPicked] = useState<Set<string>>(new Set(defaults.learnerIds ?? []));
  const [pending, setPending] = useState(false);

  const toggle = (id: string) => setPicked((p) => { const n = new Set(p); if (n.has(id)) n.delete(id); else n.add(id); return n; });
  const count = whole ? students.length : picked.size;

  return (
    <form
      action={async (fd) => { setPending(true); try { await action(fd); } finally { setPending(false); } }}
      className="space-y-6"
    >
      <input type="hidden" name="sectionId" value={sectionId} />
      <input type="hidden" name="kind" value={kind} />
      {kind === 'reteach' && code && <input type="hidden" name="gapCode" value={code} />}
      {!whole && [...picked].map((id) => <input key={id} type="hidden" name="learnerIds" value={id} />)}

      <fieldset>
        <legend className="mb-2 text-sm font-medium text-ink">What to assign</legend>
        <div className="grid gap-3 sm:grid-cols-2">
          {([
            ['chapter_check', 'Chapter check', 'A short test across the chapter: the easiest item of each concept group per subtopic. Results update gaps and the heatmap.'],
            ['reteach', 'Re-teach set', 'Worked-example and practice items on one subtopic, easiest first. Use it after re-teaching a gap.'],
          ] as const).map(([k, label, text]) => (
            <button
              type="button"
              key={k}
              onClick={() => setKind(k)}
              aria-pressed={kind === k}
              className={cn('rounded-xl border p-4 text-left transition-colors', kind === k ? 'border-brand-500 bg-brand-50 ring-1 ring-brand-500' : 'border-line bg-surface hover:border-brand-300')}
            >
              <span className="block text-sm font-semibold text-ink">{label}</span>
              <span className="mt-1 block text-xs text-muted">{text}</span>
            </button>
          ))}
        </div>
      </fieldset>

      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block text-sm">
          <span className="mb-1 block font-medium text-ink">Chapter</span>
          <select name="chapterId" className={field} value={chapterId} onChange={(e) => { setChapterId(e.target.value); const c = chapters.find((x) => x.id === e.target.value); setSubtopicId(c?.subtopics[0]?.id ?? ''); setCode(''); }}>
            {chapters.map((c) => <option key={c.id} value={c.id}>{c.label}</option>)}
          </select>
        </label>
        {kind === 'reteach' && (
          <label className="block text-sm">
            <span className="mb-1 block font-medium text-ink">Subtopic</span>
            <select name="subtopicId" className={field} value={subtopicId} onChange={(e) => { setSubtopicId(e.target.value); setCode(''); }}>
              {subtopics.map((s) => <option key={s.id} value={s.id}>{s.label}</option>)}
            </select>
          </label>
        )}
        <label className="block text-sm">
          <span className="mb-1 block font-medium text-ink">Due date</span>
          <input type="date" name="dueDate" required min={today} defaultValue={defaults.dueDate} className={field} />
        </label>
        <label className="block text-sm sm:col-span-2">
          <span className="mb-1 block font-medium text-ink">Note to students <span className="font-normal text-subtle">(optional)</span></span>
          <input name="note" maxLength={160} placeholder="e.g. Write every step, as we did in class today." className={field} />
        </label>
      </div>

      <fieldset>
        <legend className="mb-2 text-sm font-medium text-ink">Who gets it</legend>
        <div className="mb-3 flex flex-wrap gap-2">
          <button type="button" onClick={() => setWhole(true)} className={cn('rounded-full border px-3 py-1 text-sm', whole ? 'border-brand-500 bg-brand-600 text-white' : 'border-line text-muted hover:border-brand-300')}>Whole section ({students.length})</button>
          <button type="button" onClick={() => setWhole(false)} className={cn('rounded-full border px-3 py-1 text-sm', !whole ? 'border-brand-500 bg-brand-600 text-white' : 'border-line text-muted hover:border-brand-300')}>A group</button>
        </div>
        {!whole && (
          <div className="space-y-3 rounded-xl border border-line p-4">
            {groups.length > 0 && (
              <div>
                <p className="mb-2 text-xs font-medium uppercase tracking-wide text-subtle">Gap clusters</p>
                <div className="flex flex-wrap gap-2">
                  {groups.map((g) => (
                    <button
                      type="button"
                      key={g.key}
                      onClick={() => {
                        setPicked(new Set(g.learnerIds));
                        setKind('reteach');
                        const c = chapters.find((x) => x.subtopics.some((s) => s.id === g.subtopicId));
                        if (c) setChapterId(c.id);
                        setSubtopicId(g.subtopicId);
                        setCode(g.code);
                      }}
                      className="rounded-full border border-warning-600/30 bg-warning-50 px-3 py-1 text-xs font-medium text-warning-700 hover:border-warning-600"
                    >
                      {g.label}
                    </button>
                  ))}
                </div>
              </div>
            )}
            <div className="grid gap-1 sm:grid-cols-2 lg:grid-cols-3">
              {students.map((s) => (
                <label key={s.id} className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm hover:bg-surface-muted">
                  <input type="checkbox" checked={picked.has(s.id)} onChange={() => toggle(s.id)} className="size-4 accent-brand-600" />
                  {s.name}
                </label>
              ))}
            </div>
          </div>
        )}
      </fieldset>

      <div className="flex flex-wrap items-center gap-3 border-t border-line pt-4">
        <Button type="submit" disabled={pending || count === 0 || (kind === 'reteach' && !subtopicId)}>
          <Send /> {pending ? 'Assigning…' : `Assign to ${count} student${count === 1 ? '' : 's'}`}
        </Button>
        <span className="text-xs text-muted">It appears in each student&apos;s tasks and their week is re-planned around it.</span>
      </div>
    </form>
  );
}
