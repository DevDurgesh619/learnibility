'use client';

import { useCallback, useEffect, useMemo, useRef, useState, useTransition } from 'react';
import { ChevronLeft, ChevronRight, Clock, Flag, LayoutGrid, Loader2, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import type { PlayerItem, PlayerResponse, PlayerSubmission } from './types';

const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];
const CONFIDENCE = [
  { v: 1, label: 'Guessing' },
  { v: 2, label: 'Unsure' },
  { v: 3, label: 'Fairly sure' },
  { v: 4, label: 'Sure' },
  { v: 5, label: 'Certain' },
] as const;

export function formatClock(totalSeconds: number) {
  const s = Math.max(0, Math.floor(totalSeconds));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = String(s % 60).padStart(2, '0');
  return h ? `${h}:${String(m).padStart(2, '0')}:${sec}` : `${m}:${sec}`;
}

interface State {
  index: number;
  answers: Record<string, string>;
  confidence: Record<string, 1 | 2 | 3 | 4 | 5>;
  flagged: Record<string, boolean>;
  seconds: Record<string, number>;
  startedAt: number;
}

/**
 * PDF 8d (test in progress) and 8e (submit check, auto-submit when time runs out).
 * Full screen over the app shell. Answers are kept in localStorage under `storageKey`, so a refresh resumes the test.
 */
export function TestPlayer({
  title,
  minutes,
  items,
  storageKey,
  onSubmit,
  askConfidence = true,
  exitHref,
}: {
  title: string;
  minutes: number;
  items: PlayerItem[];
  storageKey: string;
  onSubmit: (submission: PlayerSubmission) => Promise<void>;
  askConfidence?: boolean;
  exitHref?: string;
}) {
  const [state, setState] = useState<State | null>(null);
  const [now, setNow] = useState(() => Date.now());
  const [confirming, setConfirming] = useState(false);
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [pending, startTransition] = useTransition();
  const [error, setError] = useState<string | null>(null);
  const submitted = useRef(false);
  const lastTick = useRef<number>(Date.now());

  // Load or start.
  useEffect(() => {
    let loaded: State | null = null;
    try {
      const raw = localStorage.getItem(storageKey);
      if (raw) loaded = JSON.parse(raw) as State;
    } catch {
      loaded = null;
    }
    setState(loaded ?? { index: 0, answers: {}, confidence: {}, flagged: {}, seconds: {}, startedAt: Date.now() });
  }, [storageKey]);

  useEffect(() => {
    if (state) localStorage.setItem(storageKey, JSON.stringify(state));
  }, [state, storageKey]);

  const totalSeconds = minutes * 60;
  const elapsed = state ? Math.floor((now - state.startedAt) / 1000) : 0;
  const remaining = totalSeconds - elapsed;
  const current = state ? items[state.index] : undefined;

  const submit = useCallback(
    (auto: boolean) => {
      if (!state || submitted.current) return;
      submitted.current = true;
      setConfirming(false);
      const responses: PlayerResponse[] = items.map((it) => ({
        questionId: it.id,
        answer: state.answers[it.id] || undefined,
        secondsTaken: Math.round(state.seconds[it.id] ?? 0),
        confidence: state.confidence[it.id],
        flagged: state.flagged[it.id] || undefined,
      }));
      startTransition(async () => {
        try {
          await onSubmit({ responses, elapsedSeconds: Math.min(elapsed, totalSeconds), autoSubmitted: auto });
          localStorage.removeItem(storageKey);
        } catch (e) {
          // Next.js redirects throw; let them through.
          if (e && typeof e === 'object' && 'digest' in e && String((e as { digest: unknown }).digest).startsWith('NEXT_REDIRECT')) {
            localStorage.removeItem(storageKey);
            throw e;
          }
          submitted.current = false;
          setError('Could not submit. Your answers are saved on this device; try again.');
        }
      });
    },
    [state, items, onSubmit, elapsed, totalSeconds, storageKey],
  );

  // Clock: one tick a second; adds time to the visible question.
  useEffect(() => {
    const t = setInterval(() => {
      const n = Date.now();
      const dt = (n - lastTick.current) / 1000;
      lastTick.current = n;
      setNow(n);
      setState((s) => {
        if (!s || submitted.current) return s;
        const id = items[s.index]?.id;
        if (!id) return s;
        return { ...s, seconds: { ...s.seconds, [id]: (s.seconds[id] ?? 0) + dt } };
      });
    }, 1000);
    return () => clearInterval(t);
  }, [items]);

  useEffect(() => {
    if (state && remaining <= 0 && !submitted.current) submit(true);
  }, [remaining, state, submit]);

  const answeredCount = useMemo(() => (state ? items.filter((it) => (state.answers[it.id] ?? '').trim() !== '').length : 0), [state, items]);
  const flaggedNumbers = useMemo(
    () => (state ? items.map((it, i) => (state.flagged[it.id] ? i + 1 : null)).filter((n): n is number => n !== null) : []),
    [state, items],
  );

  if (!state || !current) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-canvas text-muted">
        <Loader2 className="mr-2 size-5 animate-spin" /> Loading test
      </div>
    );
  }

  const go = (i: number) => {
    setState((s) => (s ? { ...s, index: Math.max(0, Math.min(items.length - 1, i)) } : s));
    setPaletteOpen(false);
  };
  const setAnswer = (v: string) => setState((s) => (s ? { ...s, answers: { ...s.answers, [current.id]: v } } : s));
  const setConf = (v: 1 | 2 | 3 | 4 | 5) => setState((s) => (s ? { ...s, confidence: { ...s.confidence, [current.id]: v } } : s));
  const toggleFlag = () => setState((s) => (s ? { ...s, flagged: { ...s.flagged, [current.id]: !s.flagged[current.id] } } : s));
  const answer = state.answers[current.id] ?? '';
  const isLast = state.index === items.length - 1;
  const lowTime = remaining <= 300;

  const palette = (
    <div className="flex flex-wrap gap-1.5">
      {items.map((it, i) => {
        const done = (state.answers[it.id] ?? '').trim() !== '';
        const flag = state.flagged[it.id];
        const active = i === state.index;
        return (
          <button
            key={it.id}
            type="button"
            onClick={() => go(i)}
            aria-label={`Question ${i + 1}${done ? ', answered' : ''}${flag ? ', flagged' : ''}`}
            aria-current={active ? 'step' : undefined}
            className={cn(
              'relative flex size-8 shrink-0 items-center justify-center rounded-full border text-xs font-medium transition',
              active ? 'border-ink bg-ink text-white' : done ? 'border-brand-200 bg-brand-50 text-brand-700' : 'border-line bg-surface text-muted hover:border-brand-300',
            )}
          >
            {i + 1}
            {flag && <span className="absolute -right-0.5 -top-0.5 size-2.5 rounded-full bg-warning-600 ring-2 ring-surface" />}
          </button>
        );
      })}
    </div>
  );

  return (
    <div className="fixed inset-0 z-50 flex flex-col bg-canvas" role="dialog" aria-label={title}>
      {/* Top bar */}
      <header className="flex items-center gap-3 border-b border-line bg-surface px-4 py-3 sm:px-6">
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-semibold text-ink">{title}</p>
          <p className="text-xs text-muted">
            Question {state.index + 1} of {items.length}
          </p>
        </div>
        <span className="hidden rounded-full border border-line px-3 py-1 text-xs text-muted sm:inline">
          Answered {answeredCount}/{items.length}
        </span>
        <span
          className={cn('inline-flex items-center gap-1 rounded-full px-3 py-1 text-sm font-semibold tabular-nums', lowTime ? 'bg-danger-50 text-danger-700' : 'bg-surface-muted text-ink')}
          aria-live={lowTime ? 'polite' : 'off'}
          title="Time left"
        >
          <Clock className="size-4" /> {formatClock(remaining)}
        </span>
        <Button size="sm" onClick={() => setConfirming(true)} disabled={pending}>
          Submit
        </Button>
        {exitHref && (
          <a href={exitHref} className="hidden rounded-lg p-2 text-muted hover:bg-surface-muted sm:inline-flex" aria-label="Leave test (answers stay saved)" title="Leave test (answers stay saved)">
            <X className="size-4" />
          </a>
        )}
      </header>

      {/* Number strip */}
      <div className="hidden overflow-x-auto border-b border-line bg-surface px-6 py-2 md:block">{palette}</div>

      {/* Question */}
      <main className="flex-1 overflow-y-auto">
        <div className="mx-auto grid max-w-5xl gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[1fr_minmax(280px,380px)] lg:py-10">
          <section>
            <p className="text-xs font-medium uppercase tracking-wide text-brand-600">
              Question {state.index + 1} · {current.topic}
            </p>
            <p className="mt-3 whitespace-pre-line text-lg leading-relaxed text-ink">{current.stem}</p>
            {current.svg && (
              <div className="mt-4 overflow-x-auto rounded-lg border border-line bg-surface p-4 [&_svg]:mx-auto [&_svg]:h-auto [&_svg]:max-w-full" dangerouslySetInnerHTML={{ __html: current.svg }} />
            )}
            <p className="mt-4 text-xs text-subtle">
              {current.marks} {current.marks === 1 ? 'mark' : 'marks'} · about {current.minutes < 1 ? `${Math.round(current.minutes * 60)} s` : `${current.minutes} min`}
            </p>
          </section>

          <section className="flex flex-col gap-3">
            {current.kind === 'mcq' && current.options ? (
              <div role="radiogroup" aria-label="Options" className="flex flex-col gap-2">
                {current.options.map((opt, i) => {
                  const selected = answer === opt;
                  return (
                    <button
                      key={opt + i}
                      type="button"
                      role="radio"
                      aria-checked={selected}
                      onClick={() => setAnswer(selected ? '' : opt)}
                      className={cn(
                        'flex items-start gap-3 rounded-xl border bg-surface p-3 text-left text-sm transition',
                        selected ? 'border-brand-500 ring-2 ring-brand-200' : 'border-line hover:border-brand-300',
                      )}
                    >
                      <span className={cn('flex size-6 shrink-0 items-center justify-center rounded-full border text-xs font-semibold', selected ? 'border-brand-600 bg-brand-600 text-white' : 'border-line text-muted')}>
                        {LETTERS[i]}
                      </span>
                      <span className="pt-0.5 text-ink">{opt}</span>
                    </button>
                  );
                })}
              </div>
            ) : (
              <label className="flex flex-col gap-2 text-sm">
                <span className="font-medium text-ink">{current.kind === 'numerical' ? 'Your answer (number)' : 'Your answer'}</span>
                {current.kind === 'numerical' ? (
                  <input
                    value={answer}
                    onChange={(e) => setAnswer(e.target.value)}
                    inputMode="decimal"
                    className="h-11 rounded-lg border border-line bg-surface px-3 text-base outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-200"
                  />
                ) : (
                  <textarea
                    value={answer}
                    onChange={(e) => setAnswer(e.target.value)}
                    rows={6}
                    className="rounded-lg border border-line bg-surface p-3 text-base outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-200"
                    placeholder="Write your working and answer"
                  />
                )}
              </label>
            )}

            {askConfidence && (
              <fieldset className="mt-2 rounded-xl border border-line bg-surface p-3">
                <legend className="px-1 text-xs font-medium text-muted">How sure are you?</legend>
                <div className="grid grid-cols-5 gap-1">
                  {CONFIDENCE.map((c) => {
                    const on = state.confidence[current.id] === c.v;
                    return (
                      <button
                        key={c.v}
                        type="button"
                        onClick={() => setConf(c.v)}
                        aria-pressed={on}
                        className={cn('flex flex-col items-center rounded-lg px-1 py-1.5 text-xs transition', on ? 'bg-brand-600 text-white' : 'text-muted hover:bg-surface-muted')}
                      >
                        <span className="text-sm font-semibold">{c.v}</span>
                        <span className="hidden sm:block">{c.label}</span>
                      </button>
                    );
                  })}
                </div>
              </fieldset>
            )}
          </section>
        </div>
      </main>

      {error && <p className="bg-danger-50 px-6 py-2 text-sm text-danger-700">{error}</p>}

      {/* Bottom bar */}
      <footer className="flex items-center gap-2 border-t border-line bg-surface px-4 py-3 sm:px-6">
        <Button variant={state.flagged[current.id] ? 'primary' : 'secondary'} size="sm" onClick={toggleFlag} aria-pressed={!!state.flagged[current.id]} className={state.flagged[current.id] ? 'bg-warning-600 hover:bg-warning-700' : ''}>
          <Flag /> <span className="hidden sm:inline">{state.flagged[current.id] ? 'Flagged' : 'Flag'}</span>
        </Button>
        <Button variant="secondary" size="sm" className="md:hidden" onClick={() => setPaletteOpen(true)}>
          <LayoutGrid /> {answeredCount}/{items.length}
        </Button>
        <div className="ml-auto flex gap-2">
          <Button variant="secondary" size="sm" onClick={() => go(state.index - 1)} disabled={state.index === 0}>
            <ChevronLeft /> Prev
          </Button>
          {isLast ? (
            <Button size="sm" onClick={() => setConfirming(true)} disabled={pending}>
              Finish
            </Button>
          ) : (
            <Button size="sm" onClick={() => go(state.index + 1)}>
              {answer ? 'Save & next' : 'Next'} <ChevronRight />
            </Button>
          )}
        </div>
      </footer>

      {/* Mobile palette */}
      {paletteOpen && (
        <div className="fixed inset-0 z-[60] flex items-end bg-ink/40 md:hidden" onClick={() => setPaletteOpen(false)}>
          <div className="w-full rounded-t-2xl bg-surface p-4" onClick={(e) => e.stopPropagation()}>
            <div className="mb-3 flex items-center justify-between">
              <p className="text-sm font-semibold">Questions</p>
              <button onClick={() => setPaletteOpen(false)} aria-label="Close" className="p-1 text-muted">
                <X className="size-4" />
              </button>
            </div>
            {palette}
            <p className="mt-3 text-xs text-muted">Orange dot = flagged · blue = answered</p>
          </div>
        </div>
      )}

      {/* 8e submit check */}
      {(confirming || pending) && (
        <div className="fixed inset-0 z-[70] flex items-center justify-center bg-ink/50 p-4">
          <div className="w-full max-w-md rounded-2xl bg-surface p-5 shadow-xl" role="alertdialog" aria-labelledby="submit-title">
            {pending ? (
              <div className="flex items-center gap-3 py-4 text-sm text-muted">
                <Loader2 className="size-5 animate-spin text-brand-600" /> {remaining <= 0 ? 'Time is up. Submitting your answers…' : 'Marking your test…'}
              </div>
            ) : (
              <>
                <h2 id="submit-title" className="text-lg font-semibold">Submit test?</h2>
                <p className="mt-2 text-sm text-muted">
                  {answeredCount} of {items.length} answered
                  {flaggedNumbers.length > 0 && <> · {flaggedNumbers.length} flagged ({flaggedNumbers.map((n) => `Q${n}`).join(', ')})</>}. You still have {formatClock(remaining)}.
                  {answeredCount < items.length && ' Unanswered questions count as incorrect.'}
                </p>
                <div className="mt-5 flex justify-end gap-2">
                  {flaggedNumbers.length > 0 ? (
                    <Button variant="secondary" onClick={() => { setConfirming(false); go(flaggedNumbers[0] - 1); }}>
                      Review flagged
                    </Button>
                  ) : (
                    <Button variant="secondary" onClick={() => setConfirming(false)}>
                      Keep going
                    </Button>
                  )}
                  <Button onClick={() => submit(false)}>Submit</Button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
