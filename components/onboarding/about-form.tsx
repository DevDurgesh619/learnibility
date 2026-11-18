'use client';

import { useActionState, useState } from 'react';
import Link from 'next/link';
import { ChevronLeft, Loader2, Wand2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { saveAbout } from '@/lib/actions/onboarding';
import { BOARD_LABEL, TARGETS, type OnboardingDraft } from './draft';
import { Field, Select, TextInput } from './field';

const DEMO = { name: 'Zoya Fernandes', grade: '9', board: 'cbse', stream: 'none', age: '14', target: 'board_exams', targetYear: '2028' };

export function AboutForm({ draft }: { draft: OnboardingDraft }) {
  const [state, action, pending] = useActionState(saveAbout, {});
  const [v, setV] = useState({
    name: draft.name ?? '',
    grade: draft.grade ? String(draft.grade) : '',
    board: draft.board ?? '',
    stream: draft.stream ?? 'none',
    age: draft.age ? String(draft.age) : '',
    target: draft.target ?? '',
    targetYear: draft.targetYear ? String(draft.targetYear) : '',
  });
  const set = (k: keyof typeof v) => (e: { target: { value: string } }) => setV((s) => ({ ...s, [k]: e.target.value }));
  const senior = Number(v.grade) >= 11;

  return (
    <form action={action} className="mt-6 flex flex-col gap-4">
      <Field label="Full name">
        <TextInput name="name" value={v.name} onChange={set('name')} autoComplete="name" placeholder="As on your school ID" />
      </Field>
      <div className="grid gap-4 sm:grid-cols-[1fr_1fr_120px]">
        <Field label="Class">
          <Select name="grade" value={v.grade} onChange={set('grade')}>
            <option value="">Choose</option>
            {[8, 9, 10, 11, 12].map((g) => <option key={g} value={g}>Class {g}</option>)}
          </Select>
        </Field>
        <Field label="Board">
          <Select name="board" value={v.board} onChange={set('board')}>
            <option value="">Choose</option>
            {(Object.keys(BOARD_LABEL) as (keyof typeof BOARD_LABEL)[]).map((b) => <option key={b} value={b}>{BOARD_LABEL[b]}</option>)}
          </Select>
        </Field>
        <Field label="Age">
          <TextInput name="age" value={v.age} onChange={set('age')} inputMode="numeric" placeholder="14" />
        </Field>
      </div>
      {senior && (
        <Field label="Stream">
          <Select name="stream" value={v.stream} onChange={set('stream')}>
            <option value="none">Choose</option>
            <option value="science">Science</option>
            <option value="commerce">Commerce</option>
            <option value="humanities">Humanities</option>
          </Select>
        </Field>
      )}
      <div className="grid gap-4 sm:grid-cols-[1fr_160px]">
        <Field label="Your main target" hint="Drives your Home cards and how your week is planned.">
          <Select name="target" value={v.target} onChange={set('target')}>
            <option value="">Choose</option>
            {TARGETS.map((t) => <option key={t.value} value={t.value}>{t.label}</option>)}
          </Select>
        </Field>
        <Field label="Target year">
          <Select name="targetYear" value={v.targetYear} onChange={set('targetYear')}>
            <option value="">Choose</option>
            {[2026, 2027, 2028, 2029, 2030, 2031].map((y) => <option key={y} value={y}>{y}</option>)}
          </Select>
        </Field>
      </div>
      {state.error && <p className="text-sm text-danger-700" role="alert">{state.error}</p>}
      <div className="mt-2 flex items-center justify-between gap-3">
        <Link href="/signup/role" className="inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ChevronLeft className="size-4" /> Back</Link>
        <div className="flex gap-2">
          <Button type="button" variant="ghost" onClick={() => setV(DEMO as typeof v)} title="Fill Zoya's details for the demo">
            <Wand2 /> <span className="hidden sm:inline">Demo details</span>
          </Button>
          <Button type="submit" disabled={pending}>{pending && <Loader2 className="animate-spin" />} Continue</Button>
        </div>
      </div>
    </form>
  );
}
