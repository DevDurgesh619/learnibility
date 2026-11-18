'use client';

import { useMemo, useRef, useState, useTransition } from 'react';
import { useRouter } from 'next/navigation';
import { Bot, Check, GitCompare, Loader2, MessageSquarePlus, PenLine, Send, Sparkles, Upload } from 'lucide-react';
import { Avatar } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import {
  addEssayComment, reviewEssay, runAiPrePass, saveEssayVersion, sendEssayForReview, setCommentResolved,
} from '@/lib/actions/applications';
import type { Essay, EssayComment } from '@/lib/data/types';
import { cn } from '@/lib/utils';
import { outlineFor } from './ai';

const wc = (t: string) => (t.trim().match(/\S+/g) ?? []).length;
// Formatted by hand: server and browser ICU data differ ("Sep" vs "Sept"), which breaks hydration.
const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const ist = (iso: string) => new Date(Date.parse(iso) + 330 * 60_000);
const fmt = (iso: string) => { const d = ist(iso); return `${d.getUTCDate()} ${MON[d.getUTCMonth()]}`; };
const fmtTime = (iso: string) => {
  const d = ist(iso);
  const h = d.getUTCHours();
  return `${fmt(iso)}, ${h % 12 || 12}:${String(d.getUTCMinutes()).padStart(2, '0')} ${h < 12 ? 'am' : 'pm'}`;
};

/** Word-level diff (LCS) for "Compare" between two versions. */
function diffWords(a: string, b: string): { t: string; k: 'same' | 'add' | 'del' }[] {
  const A = a.split(/(\s+)/);
  const B = b.split(/(\s+)/);
  const n = A.length;
  const m = B.length;
  const L = Array.from({ length: n + 1 }, () => new Uint16Array(m + 1));
  for (let i = n - 1; i >= 0; i--) for (let j = m - 1; j >= 0; j--) L[i]![j] = A[i] === B[j] ? L[i + 1]![j + 1]! + 1 : Math.max(L[i + 1]![j]!, L[i]![j + 1]!);
  const out: { t: string; k: 'same' | 'add' | 'del' }[] = [];
  let i = 0;
  let j = 0;
  while (i < n && j < m) {
    if (A[i] === B[j]) { out.push({ t: A[i]!, k: 'same' }); i++; j++; }
    else if (L[i + 1]![j]! >= L[i]![j + 1]!) out.push({ t: A[i++]!, k: 'del' });
    else out.push({ t: B[j++]!, k: 'add' });
  }
  while (i < n) out.push({ t: A[i++]!, k: 'del' });
  while (j < m) out.push({ t: B[j++]!, k: 'add' });
  return out;
}

export interface EssayEditorProps {
  essay: Essay;
  title: string;
  viewer: 'student' | 'counsellor';
  names: Record<string, string>;
  counsellorFirst: string;
  studentFirst: string;
  others?: { id: string; label: string; href: string }[];
}

export function EssayEditor({ essay, title, viewer, names, counsellorFirst, studentFirst, others = [] }: EssayEditorProps) {
  const router = useRouter();
  const latest = essay.versions.reduce((a, b) => (b.version > a.version ? b : a), essay.versions[0]!);
  const [viewV, setViewV] = useState(latest.version);
  const [editing, setEditing] = useState(viewer === 'student' && latest.text.trim() === '');
  const [draft, setDraft] = useState(latest.text);
  const [compare, setCompare] = useState(false);
  const [outline, setOutline] = useState(false);
  const [active, setActive] = useState<string | null>(null);
  const [sel, setSel] = useState<{ start: number; end: number; quote: string } | null>(null);
  const [newComment, setNewComment] = useState('');
  const [reply, setReply] = useState<Record<string, string>>({});
  const [note, setNote] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, start] = useTransition();
  const textRef = useRef<HTMLDivElement>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  // Keep local state in step when the server sends a new version.
  const [seenLatest, setSeenLatest] = useState(latest.version);
  if (seenLatest !== latest.version) {
    setSeenLatest(latest.version);
    setViewV(latest.version);
    setDraft(latest.text);
  }

  const version = essay.versions.find((v) => v.version === viewV) ?? latest;
  const isLatest = version.version === latest.version;
  const comments = essay.comments.filter((c) => c.version === version.version);
  const roots = comments.filter((c) => !c.parentId).sort((a, b) => Number(a.resolved) - Number(b.resolved) || (a.anchor?.start ?? 1e9) - (b.anchor?.start ?? 1e9));
  const openRoots = roots.filter((c) => !c.resolved);
  const resolvedCount = essay.comments.filter((c) => !c.parentId && c.resolved).length;
  const words = wc(editing ? draft : version.text);
  const over = essay.wordLimit && words > essay.wordLimit;
  const prev = essay.versions.find((v) => v.version === version.version - 1);

  const run = (fn: () => Promise<unknown>, msg?: string) =>
    start(async () => {
      setError(null);
      try {
        const r = await fn();
        if (msg) setNote(msg);
        else if (r && typeof r === 'object' && 'summary' in r) setNote(`AI pre-pass: ${(r as { summary: string }).summary}`);
        router.refresh();
      } catch (e) {
        setError(e instanceof Error ? e.message : 'Something went wrong.');
      }
    });

  // Highlight anchored, unresolved comments in the text.
  const segments = useMemo(() => {
    const marks = openRoots.filter((c) => c.anchor && c.anchor.end <= version.text.length).map((c) => ({ ...c.anchor!, id: c.id, ai: c.kind === 'ai' }));
    marks.sort((a, b) => a.start - b.start);
    const out: { text: string; id?: string; ai?: boolean; n?: number }[] = [];
    let pos = 0;
    marks.forEach((m) => {
      if (m.start < pos) return;
      if (m.start > pos) out.push({ text: version.text.slice(pos, m.start) });
      out.push({ text: version.text.slice(m.start, m.end), id: m.id, ai: m.ai, n: roots.indexOf(roots.find((r) => r.id === m.id)!) + 1 });
      pos = m.end;
    });
    out.push({ text: version.text.slice(pos) });
    return out;
  }, [openRoots, roots, version.text]);

  function onMouseUp() {
    const s = window.getSelection();
    const box = textRef.current;
    if (!s || s.isCollapsed || !box || !box.contains(s.anchorNode)) return;
    const r = s.getRangeAt(0);
    const pre = document.createRange();
    pre.selectNodeContents(box);
    pre.setEnd(r.startContainer, r.startOffset);
    const start = pre.toString().length;
    const quote = r.toString();
    if (quote.trim().length < 2) return;
    setSel({ start, end: start + quote.length, quote: quote.slice(0, 200) });
  }

  const statusBadge = essay.status === 'final' ? <Badge tone="success">Final</Badge> : essay.status === 'in_review' ? <Badge tone="info">With {counsellorFirst} for review</Badge> : <Badge tone="warning">Drafting</Badge>;

  return (
    <div className="grid grid-cols-[minmax(0,1fr)] gap-6 lg:grid-cols-[minmax(0,1fr)_340px]">
      <div className="min-w-0 space-y-4">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
          <div className="min-w-0">
            <h2 className="text-lg font-semibold text-ink">{title}</h2>
            <p className="mt-0.5 text-sm text-muted">{essay.prompt}</p>
            <div className="mt-2 flex flex-wrap items-center gap-2">
              <span className="rounded-full border border-line px-2.5 py-0.5 text-xs font-medium text-ink">v{version.version}{isLatest ? ' · current' : ''}</span>
              {statusBadge}
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            {viewer === 'student' && isLatest && !editing && essay.status !== 'final' && <Button size="sm" variant="secondary" onClick={() => { setDraft(latest.text); setEditing(true); }}><PenLine />Edit</Button>}
            {viewer === 'student' && editing && (
              <>
                <input ref={fileRef} type="file" accept=".txt,.md" className="hidden" onChange={async (e) => { const f = e.target.files?.[0]; if (f) setDraft(await f.text()); }} />
                <Button size="sm" variant="secondary" onClick={() => fileRef.current?.click()}><Upload />Upload</Button>
                <Button size="sm" variant="ghost" onClick={() => { setEditing(false); setDraft(latest.text); }}>Cancel</Button>
                <Button size="sm" disabled={pending || draft === latest.text} onClick={() => run(async () => { await saveEssayVersion(essay.id, draft); setEditing(false); }, 'Saved as a new version.')}>{pending ? <Loader2 className="animate-spin" /> : <Check />}Save</Button>
              </>
            )}
          </div>
        </div>

        <Card className="overflow-hidden">
          {editing ? (
            <textarea
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              aria-label="Essay text"
              placeholder="Start writing, or upload a draft. Use the outline helper if you are stuck."
              className="block min-h-[420px] w-full resize-y border-0 p-5 text-[15px] leading-7 text-ink focus:outline-none"
            />
          ) : compare && prev ? (
            <div className="p-5 text-[15px] leading-7 whitespace-pre-wrap text-ink">
              <p className="mb-3 text-xs font-medium text-muted">Changes from v{prev.version} to v{version.version}: <span className="bg-success-50 text-success-700">added</span> · <span className="text-danger-700 line-through">removed</span></p>
              {diffWords(prev.text, version.text).map((d, i) => (
                <span key={i} className={cn(d.k === 'add' && 'bg-success-50 text-success-700', d.k === 'del' && 'text-danger-700 line-through decoration-danger-600/60')}>{d.t}</span>
              ))}
            </div>
          ) : (
            <div ref={textRef} onMouseUp={onMouseUp} className="min-h-[300px] p-5 text-[15px] leading-7 whitespace-pre-wrap text-ink selection:bg-brand-100">
              {version.text.trim() === '' ? <span className="text-subtle">No text yet.</span> : segments.map((s, i) =>
                s.id ? (
                  <mark key={i} onClick={() => setActive(s.id!)} className={cn('cursor-pointer rounded-sm px-0.5 text-ink', s.ai ? 'bg-violet-100' : 'bg-warning-50 ring-1 ring-warning-600/30', active === s.id && 'ring-2 ring-brand-500')}>
                    {s.text}<sup className="ml-0.5 text-[10px] font-semibold text-muted">{s.n}</sup>
                  </mark>
                ) : <span key={i}>{s.text}</span>,
              )}
            </div>
          )}
          <div className="flex flex-wrap items-center justify-between gap-2 border-t border-line px-5 py-2.5 text-xs">
            <span className={cn('font-medium', over ? 'text-danger-700' : 'text-muted')}>{words} / {essay.wordLimit} words{over ? ` · ${words - essay.wordLimit} over` : ''}</span>
            {!editing && !compare && <span className="text-subtle">Select text to comment on it.</span>}
          </div>
        </Card>

        {sel && !editing && (
          <Card className="border-brand-200 p-4">
            <p className="text-xs text-muted">Comment on: <span className="italic text-ink">“{sel.quote.length > 120 ? `${sel.quote.slice(0, 117)}…` : sel.quote}”</span></p>
            <textarea value={newComment} onChange={(e) => setNewComment(e.target.value)} rows={2} aria-label="Comment" placeholder={viewer === 'counsellor' ? `Suggestion for ${studentFirst}` : `Note or question for ${counsellorFirst}`} className="mt-2 w-full rounded-lg border border-line p-2 text-sm" />
            <div className="mt-2 flex justify-end gap-2">
              <Button size="sm" variant="ghost" onClick={() => { setSel(null); setNewComment(''); }}>Cancel</Button>
              <Button size="sm" disabled={!newComment.trim() || pending} onClick={() => run(async () => { await addEssayComment(essay.id, { text: newComment, anchor: sel }); setSel(null); setNewComment(''); }, 'Comment added.')}><MessageSquarePlus />Comment</Button>
            </div>
          </Card>
        )}

        <div className="flex flex-wrap items-center gap-2">
          {isLatest && !editing && essay.status !== 'final' && (
            <Button size="sm" variant="secondary" disabled={pending} onClick={() => run(() => runAiPrePass(essay.id))}><Sparkles />Run AI pre-pass</Button>
          )}
          {viewer === 'student' && <Button size="sm" variant="ghost" onClick={() => setOutline((o) => !o)}><Bot />Outline helper</Button>}
          {viewer === 'student' && isLatest && !editing && essay.status === 'drafting' && version.text.trim() && (
            <Button size="sm" disabled={pending} onClick={() => run(() => sendEssayForReview(essay.id), `Sent to ${counsellorFirst}.`)}><Send />Send to {counsellorFirst} for review</Button>
          )}
          {viewer === 'counsellor' && isLatest && essay.status !== 'final' && (
            <>
              <Button size="sm" disabled={pending} onClick={() => run(() => reviewEssay(essay.id, 'final'), 'Approved as final.')}><Check />Approve as final</Button>
              <Button size="sm" variant="secondary" disabled={pending} onClick={() => run(() => reviewEssay(essay.id, 'return'), `Returned to ${studentFirst} with your comments.`)}>Return to {studentFirst}</Button>
            </>
          )}
          {pending && <Loader2 className="size-4 animate-spin text-muted" />}
          {note && <span className="text-xs text-success-700" role="status">{note}</span>}
          {error && <span className="text-xs text-danger-700" role="alert">{error}</span>}
        </div>

        {outline && (
          <Card className="p-4">
            <p className="text-sm font-semibold text-ink">Outline for this prompt</p>
            <ol className="mt-2 space-y-2 text-sm">
              {outlineFor(essay.prompt, essay.wordLimit).map((o, i) => (
                <li key={i}><p className="font-medium text-ink">{i + 1}. {o.heading}</p><ul className="ml-5 list-disc text-muted">{o.points.map((p) => <li key={p}>{p}</li>)}</ul></li>
              ))}
            </ol>
          </Card>
        )}

        <div className="text-sm">
          <span className="font-semibold text-ink">Version history</span>
          {[...essay.versions].sort((a, b) => b.version - a.version).map((v) => (
            <button key={v.version} type="button" onClick={() => { setViewV(v.version); setEditing(false); setCompare(false); }} className={cn('ml-2 underline-offset-2 hover:underline', v.version === viewV ? 'font-medium text-brand-700' : 'text-muted')}>
              v{v.version}{v.version === latest.version ? ' (current)' : v.version === 1 ? ' (original)' : ''} {fmt(v.createdAt)}
            </button>
          ))}
          {prev && !editing && <button type="button" onClick={() => setCompare((c) => !c)} className="ml-3 inline-flex items-center gap-1 text-brand-700 hover:underline"><GitCompare className="size-3.5" />{compare ? 'Hide changes' : `Compare with v${prev.version}`}</button>}
        </div>
      </div>

      <aside className="space-y-3">
        <h3 className="text-base font-semibold text-ink">Feedback on v{version.version}</h3>
        {roots.length === 0 && <p className="rounded-lg border border-dashed border-line p-4 text-sm text-muted">No comments on this version yet.{isLatest ? ' Run the AI pre-pass for a first read.' : ''}</p>}
        {roots.map((c, idx) => {
          const replies = comments.filter((r) => r.parentId === c.id).sort((a, b) => a.createdAt.localeCompare(b.createdAt));
          return (
            <Card key={c.id} onClick={() => setActive(c.id)} className={cn('p-3', c.resolved && 'opacity-60', active === c.id && 'ring-2 ring-brand-500')}>
              <Comment c={c} n={idx + 1} names={names} />
              {replies.map((r) => <div key={r.id} className="mt-2 border-l-2 border-line pl-3"><Comment c={r} names={names} /></div>)}
              {!c.resolved && isLatest && (
                <div className="mt-2 space-y-2">
                  {c.kind === 'human' && (
                    <div className="flex gap-2">
                      <input value={reply[c.id] ?? ''} onChange={(e) => setReply((x) => ({ ...x, [c.id]: e.target.value }))} placeholder="Reply…" aria-label="Reply" className="h-8 min-w-0 flex-1 rounded-lg border border-line px-2 text-sm" />
                      <Button size="sm" variant="secondary" disabled={!reply[c.id]?.trim() || pending} onClick={() => run(async () => { await addEssayComment(essay.id, { text: reply[c.id]!, parentId: c.id }); setReply((x) => ({ ...x, [c.id]: '' })); })}>Reply</Button>
                    </div>
                  )}
                  <button type="button" disabled={pending} onClick={() => run(() => setCommentResolved(essay.id, c.id, true))} className="text-xs font-medium text-brand-700 hover:underline">Resolve</button>
                </div>
              )}
              {c.resolved && isLatest && <button type="button" onClick={() => run(() => setCommentResolved(essay.id, c.id, false))} className="mt-1 text-xs text-muted hover:underline">Reopen</button>}
            </Card>
          );
        })}
        {resolvedCount > 0 && <p className="rounded-lg border border-dashed border-line px-3 py-2 text-xs text-muted">Resolved · {resolvedCount} comment{resolvedCount === 1 ? '' : 's'} across all versions</p>}
        {others.length > 0 && (
          <p className="text-sm text-muted">Other essays: {others.map((o, i) => <span key={o.id}>{i ? ' · ' : ''}<a href={o.href} className="text-brand-700 underline-offset-2 hover:underline">{o.label}</a></span>)}</p>
        )}
      </aside>
    </div>
  );
}

function Comment({ c, n, names }: { c: EssayComment; n?: number; names: Record<string, string> }) {
  const name = c.kind === 'ai' ? 'AI pre-pass' : names[c.authorId ?? ''] ?? 'Someone';
  return (
    <div>
      <div className="flex items-center gap-2">
        {c.kind === 'ai' ? <span className="flex size-6 items-center justify-center rounded-full bg-violet-100 text-violet-700"><Sparkles className="size-3.5" /></span> : <Avatar name={name} size="sm" className="size-6 text-[10px]" />}
        <span className="text-sm font-medium text-ink">{name}</span>
        <span className="text-xs text-subtle">{fmtTime(c.createdAt)}</span>
        {n && <span className="ml-auto text-xs font-semibold text-muted">{n}</span>}
      </div>
      {c.anchor && <p className="mt-1 line-clamp-2 border-l-2 border-warning-600/40 pl-2 text-xs text-muted italic">“{c.anchor.quote}”</p>}
      <p className="mt-1 text-sm text-ink">{c.text}</p>
    </div>
  );
}
