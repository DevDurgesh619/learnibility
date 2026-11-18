'use client';

import Link from 'next/link';
import { useState, useTransition } from 'react';
import { moveLead } from '@/lib/actions/crm';
import { cn } from '@/lib/utils';
import { STATUS_LABEL, type LeadStatus } from './types';

export interface BoardCard { id: string; title: string; sub: string; valueInr: number; score: number; owner: string; status: LeadStatus; badge?: string }

const inr = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 });
const MOVABLE: LeadStatus[] = ['new', 'contacted', 'qualified', 'demo_booked', 'demo_done', 'proposal_sent', 'negotiation'];

/** Drag cards between stages (desktop) or use the "Move to" menu (touch). Won and Lost need the lead page. */
export function PipelineBoard({ columns, cards: initial }: { columns: LeadStatus[]; cards: BoardCard[] }) {
  const [cards, setCards] = useState(initial);
  const [over, setOver] = useState<LeadStatus | null>(null);
  const [message, setMessage] = useState<{ text: string; ok: boolean } | null>(null);
  const [, start] = useTransition();

  function move(id: string, to: LeadStatus) {
    const card = cards.find((c) => c.id === id);
    if (!card || card.status === to) return;
    const before = cards;
    setCards((cs) => cs.map((c) => (c.id === id ? { ...c, status: to } : c)));
    start(async () => {
      const res = await moveLead(id, to);
      if (!res.ok) {
        setCards(before);
        setMessage({ text: res.error ?? 'Could not move that deal.', ok: false });
      } else setMessage({ text: `${card.title} moved to ${STATUS_LABEL[to]}.`, ok: true });
    });
  }

  return (
    <div>
      <p role="status" aria-live="polite" className={cn('mb-3 min-h-5 text-sm', message?.ok ? 'text-success-700' : 'text-danger-700')}>{message?.text}</p>
      <div className="flex gap-3 overflow-x-auto pb-4" data-testid="pipeline">
        {columns.map((col) => {
          const list = cards.filter((c) => c.status === col || (col === 'closed_won' && c.status === 'converted'));
          const value = list.reduce((s, c) => s + c.valueInr, 0);
          return (
            <section
              key={col}
              aria-label={STATUS_LABEL[col]}
              onDragOver={(e) => { e.preventDefault(); setOver(col); }}
              onDragLeave={() => setOver((o) => (o === col ? null : o))}
              onDrop={(e) => { e.preventDefault(); setOver(null); move(e.dataTransfer.getData('text/plain'), col); }}
              className={cn('flex w-64 shrink-0 flex-col rounded-[var(--radius-card)] border border-line bg-surface-muted/60', over === col && 'ring-2 ring-brand-300')}
            >
              <header className="border-b border-line px-3 py-2.5">
                <div className="flex items-center justify-between text-sm font-semibold text-ink"><span>{STATUS_LABEL[col]}</span><span className="text-xs font-medium text-muted">{list.length}</span></div>
                <p className="text-xs tabular-nums text-muted">{inr.format(value)}</p>
              </header>
              <ul className="flex max-h-[68vh] flex-col gap-2 overflow-y-auto p-2">
                {list.map((c) => (
                  <li key={c.id} draggable={MOVABLE.includes(c.status)} onDragStart={(e) => e.dataTransfer.setData('text/plain', c.id)}
                    className={cn('rounded-lg border border-line bg-surface p-3 text-sm shadow-sm', MOVABLE.includes(c.status) && 'cursor-grab active:cursor-grabbing')} data-testid="deal-card">
                    <Link href={`/sales/leads/${c.id}`} className="block font-medium text-ink hover:text-brand-700">{c.title}</Link>
                    <p className="truncate text-xs text-muted">{c.sub}</p>
                    <div className="mt-2 flex items-center justify-between text-xs">
                      <span className="tabular-nums font-medium text-ink">{c.valueInr ? inr.format(c.valueInr) : '—'}</span>
                      <span className="text-muted">{c.owner.split(' ')[0]} · {c.score}</span>
                    </div>
                    {c.badge && <p className="mt-1 text-xs font-medium text-brand-700">{c.badge}</p>}
                    {MOVABLE.includes(c.status) && (
                      <select aria-label={`Move ${c.title}`} value="" onChange={(e) => e.target.value && move(c.id, e.target.value as LeadStatus)}
                        className="mt-2 h-7 w-full rounded-md border border-line bg-surface px-1.5 text-xs text-muted">
                        <option value="">Move to…</option>
                        {MOVABLE.filter((s) => s !== c.status).map((s) => <option key={s} value={s}>{STATUS_LABEL[s]}</option>)}
                      </select>
                    )}
                  </li>
                ))}
                {!list.length && <li className="px-2 py-6 text-center text-xs text-subtle">Drop a deal here</li>}
              </ul>
            </section>
          );
        })}
      </div>
    </div>
  );
}
