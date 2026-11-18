'use client';

import { useState, useTransition } from 'react';
import { BookOpen, RefreshCw, Sparkles, Trash2, Upload, Wand2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import type { TutorQuestion } from './model';
import type { DraftParams } from '@/lib/actions/tutor';

type Q = TutorQuestion & { flag?: string };
type Method = 'ai' | 'bank' | 'upload';

/** 4i choose method → 4j describe (AI) → 4k verify the draft → assign (4l). */
export function AddTestWizard({ learnerId, firstName, topics, suggested, retention, defaultDue, draft, assign }: {
  learnerId: string; firstName: string;
  topics: { id: string; label: string; chapter: string }[];
  suggested: { ids: string[]; text: string };
  retention: string[];
  defaultDue: string;
  draft: (p: DraftParams) => Promise<Q[]>;
  assign: (d: FormData) => Promise<void>;
}) {
  const [step, setStep] = useState<'method' | 'describe' | 'verify'>('method');
  const [method, setMethod] = useState<Method>('ai');
  const [sel, setSel] = useState<string[]>(suggested.ids.length ? suggested.ids : topics.slice(0, 1).map((t) => t.id));
  const [count, setCount] = useState(10);
  const [difficulty, setDifficulty] = useState<DraftParams['difficulty']>('medium');
  const [type, setType] = useState<DraftParams['type']>('mixed');
  const [withRetention, setWithRetention] = useState(retention.length > 0);
  const [prompt, setPrompt] = useState(`${count} questions on ${suggested.text || topics[0]?.label || 'this topic'}, medium difficulty, mix of numeric and short explanation.`);
  const [time, setTime] = useState(30);
  const [due, setDue] = useState(defaultDue);
  const [evaluation, setEvaluation] = useState<'ai_review' | 'manual'>('ai_review');
  const [upload, setUpload] = useState('');
  const [qs, setQs] = useState<Q[]>([]);
  const [seed, setSeed] = useState(1);
  const [pending, start] = useTransition();
  const title = `${topics.find((t) => t.id === sel[0])?.label ?? 'Practice'}${sel.length > 1 ? ` & ${sel.length - 1} more` : ''}`;

  const generate = (s = seed) => start(async () => {
    if (method === 'upload') {
      const lines = upload.split('\n').map((l) => l.trim()).filter(Boolean);
      setQs(lines.map((l, i) => ({ id: `tq_${sel[0]}_u${i + 1}`, type: 'short', subtopicId: sel[0]!, stem: l, answer: 'Tutor to mark', markingKey: 'Tutor marks', marks: 1 })));
    } else {
      setQs(await draft({ subtopicIds: sel, count, difficulty, type, retentionFrom: withRetention ? retention : [], seed: s }));
    }
    setStep('verify');
  });
  const regenOne = (i: number) => start(async () => {
    const one = await draft({ subtopicIds: [qs[i]!.subtopicId], count: 1, difficulty, type, seed: seed + i + 7 });
    setSeed((x) => x + 1);
    setQs((cur) => cur.map((q, j) => (j === i && one[0] ? { ...one[0], id: one[0].id + (one[0].id === q.id ? 'r' : '') } : q)));
  });

  if (step === 'method') {
    const opts: [Method, string, string, React.ReactNode][] = [
      ['ai', 'Create with AI', 'Describe the topic, count and difficulty. You check every question before assigning.', <Wand2 key="a" />],
      ['bank', 'From resources', 'Pick from the platform question bank and your previous tests.', <BookOpen key="b" />],
      ['upload', 'Upload manually', 'Paste or type your own questions, one per line.', <Upload key="c" />],
    ];
    return (
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-ink">How do you want to create it?</h2>
        <div className="grid gap-3 md:grid-cols-3">
          {opts.map(([k, l, d, icon]) => (
            <button key={k} type="button" onClick={() => setMethod(k)} aria-pressed={method === k}
              className={cn('rounded-[var(--radius-card)] border p-4 text-left transition-colors [&_svg]:size-5', method === k ? 'border-brand-600 bg-brand-50 ring-2 ring-brand-200' : 'border-line bg-surface hover:border-brand-300')}>
              <span className="text-brand-600">{icon}</span>
              <p className="mt-2 font-medium text-ink">{l}</p>
              <p className="mt-1 text-sm text-muted">{d}</p>
            </button>
          ))}
        </div>
        <Button onClick={() => setStep('describe')}>Continue</Button>
      </div>
    );
  }

  if (step === 'describe') {
    return (
      <div className="space-y-5">
        <h2 className="text-lg font-semibold text-ink">{method === 'ai' ? 'Create with AI' : method === 'bank' ? 'From the question bank' : 'Upload questions'} · for {firstName}</h2>
        {method === 'ai' && <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} rows={2} className="w-full rounded-lg border border-line p-3 text-sm" aria-label="Describe the test" />}
        <div>
          <p className="mb-1.5 text-sm font-medium text-ink">Topics</p>
          <div className="flex max-h-48 flex-wrap gap-1.5 overflow-y-auto">
            {topics.map((t) => (
              <button key={t.id} type="button" onClick={() => setSel((s) => (s.includes(t.id) ? s.filter((x) => x !== t.id) : [...s, t.id]))}
                className={cn('rounded-full border px-2.5 py-0.5 text-xs', sel.includes(t.id) ? 'border-brand-600 bg-brand-600 text-white' : 'border-line hover:bg-surface-muted')} title={t.chapter}>{t.label}</button>
            ))}
          </div>
        </div>
        {method === 'upload' ? (
          <textarea value={upload} onChange={(e) => setUpload(e.target.value)} rows={6} placeholder="One question per line" className="w-full rounded-lg border border-line p-3 text-sm" />
        ) : (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            <Field label="No. of questions"><input type="number" min={1} max={25} value={count} onChange={(e) => setCount(Number(e.target.value))} className="h-9 w-full rounded-lg border border-line px-2 text-sm" /></Field>
            <Field label="Difficulty"><Select value={difficulty} onChange={(v) => setDifficulty(v as DraftParams['difficulty'])} opts={[['easy', 'Easy'], ['medium', 'Medium'], ['hard', 'Hard']]} /></Field>
            <Field label="Type"><Select value={type} onChange={(v) => setType(v as DraftParams['type'])} opts={[['mixed', 'Mixed'], ['mcq', 'MCQ'], ['numerical', 'Numeric'], ['short', 'Short answer']]} /></Field>
          </div>
        )}
        <div className="grid gap-3 sm:grid-cols-3">
          <Field label="Time limit (min)"><input type="number" min={5} max={120} value={time} onChange={(e) => setTime(Number(e.target.value))} className="h-9 w-full rounded-lg border border-line px-2 text-sm" /></Field>
          <Field label="Due"><input type="date" value={due} onChange={(e) => setDue(e.target.value)} className="h-9 w-full rounded-lg border border-line px-2 text-sm" /></Field>
          <Field label="Evaluation"><Select value={evaluation} onChange={(v) => setEvaluation(v as 'ai_review')} opts={[['ai_review', 'AI + my review'], ['manual', 'I mark it myself']]} /></Field>
        </div>
        {suggested.text && method !== 'upload' && (
          <div className="flex flex-col gap-2 rounded-lg border border-brand-200 bg-brand-50/60 p-3 text-sm sm:flex-row sm:items-center">
            <Sparkles className="size-4 shrink-0 text-brand-600" />
            <p className="flex-1 text-ink"><span className="font-medium">Based on {firstName}&apos;s gaps:</span> {suggested.text}.{retention.length ? ' Include a question from an earlier topic to check retention.' : ''}</p>
            <label className="flex items-center gap-1.5 text-xs"><input type="checkbox" checked={withRetention} onChange={(e) => setWithRetention(e.target.checked)} /> retention check</label>
            <Button size="sm" variant="secondary" onClick={() => setSel(suggested.ids)}>Use suggestion</Button>
          </div>
        )}
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => setStep('method')}>Back</Button>
          <Button disabled={pending || sel.length === 0 || (method === 'upload' && !upload.trim())} onClick={() => generate()}>{pending ? 'Building draft…' : method === 'upload' ? 'Continue' : 'Generate draft'}</Button>
        </div>
      </div>
    );
  }

  return (
    <form action={assign} className="space-y-4">
      <input type="hidden" name="learnerId" value={learnerId} />
      <input type="hidden" name="questions" value={JSON.stringify(qs.map(({ flag: _f, ...q }) => q))} />
      <input type="hidden" name="dueOn" value={due} />
      <input type="hidden" name="timeLimitMin" value={time} />
      <input type="hidden" name="evaluation" value={evaluation} />
      <input type="hidden" name="source" value={method} />
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
        <div className="flex-1">
          <label className="text-xs font-medium uppercase tracking-wide text-muted">Draft title</label>
          <input name="title" defaultValue={title} className="mt-1 h-10 w-full rounded-lg border border-line px-3 text-base font-semibold" />
          <p className="mt-1 text-sm text-muted">{qs.length} questions · {difficulty} · {time} min · {firstName} · due {due}</p>
        </div>
        {method !== 'upload' && <Button type="button" variant="secondary" disabled={pending} onClick={() => { setSeed((x) => x + 3); generate(seed + 3); }}><RefreshCw /> Regenerate all</Button>}
        <Button disabled={qs.length === 0}>Assign to {firstName}</Button>
      </div>
      <ol className="space-y-3">
        {qs.map((q, i) => (
          <li key={q.id + i} className="rounded-[var(--radius-card)] border border-line bg-surface p-4">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-sm font-semibold text-ink">Q{i + 1} · {q.type === 'mcq' ? 'MCQ' : q.type === 'numerical' ? 'Numeric' : 'Short answer'}</span>
              <span className="text-xs text-muted">{topics.find((t) => t.id === q.subtopicId)?.label}</span>
              {q.id.startsWith('tq_') ? <Badge>AI draft</Badge> : <Badge tone="brand">Question bank</Badge>}
              {q.flag && <Badge tone="warning">{q.flag}</Badge>}
              <span className="ml-auto flex gap-1">
                {method !== 'upload' && <button type="button" onClick={() => regenOne(i)} className="rounded p-1 text-muted hover:bg-surface-muted" aria-label="Regenerate"><RefreshCw className="size-4" /></button>}
                <button type="button" onClick={() => setQs((c) => c.filter((_, j) => j !== i))} className="rounded p-1 text-muted hover:bg-surface-muted" aria-label="Remove"><Trash2 className="size-4" /></button>
              </span>
            </div>
            <textarea value={q.stem} onChange={(e) => setQs((c) => c.map((x, j) => (j === i ? { ...x, stem: e.target.value } : x)))} rows={2} className="mt-2 w-full rounded-lg border border-transparent bg-surface-muted/60 p-2 text-sm text-ink focus:border-line focus:bg-surface" aria-label={`Question ${i + 1}`} />
            {q.options && <ul className="mt-1 grid gap-1 text-xs text-muted sm:grid-cols-2">{q.options.map((o) => <li key={o} className={cn(o === q.answer && 'font-medium text-success-700')}>• {o}</li>)}</ul>}
            <p className="mt-1 text-xs text-muted">Answer: {q.answer} · Marking: {q.markingKey}</p>
          </li>
        ))}
      </ol>
      <Button type="button" variant="ghost" onClick={() => setStep('describe')}>Back to settings</Button>
    </form>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return <label className="block"><span className="mb-1 block text-xs font-medium uppercase tracking-wide text-muted">{label}</span>{children}</label>;
}
function Select({ value, onChange, opts }: { value: string; onChange: (v: string) => void; opts: [string, string][] }) {
  return <select value={value} onChange={(e) => onChange(e.target.value)} className="h-9 w-full rounded-lg border border-line px-2 text-sm">{opts.map(([v, l]) => <option key={v} value={v}>{l}</option>)}</select>;
}
