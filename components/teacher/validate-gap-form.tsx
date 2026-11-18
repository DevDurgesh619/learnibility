'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { GAP_CODES, type GapCode } from '@/lib/types';

const LABEL: Record<GapCode, string> = {
  G1: 'Prerequisite', G2: 'Conceptual', G3: 'Procedural', G4: 'Careless', G5: 'Transfer',
  G6: 'Retention', G7: 'Language', G8: 'Time pressure', G9: 'Calibration', G10: 'Engagement',
};

/** Gap Log "Notes (teacher validation #430)": confirm, correct or reject one diagnosis. */
export function ValidateGapForm({
  action, sectionId, learnerId, gapId, code, gapJson, compact,
}: {
  action: (fd: FormData) => Promise<void>;
  sectionId: string;
  learnerId: string;
  gapId: string;
  code: GapCode;
  /** Background learners: the light gap as a record, written on first validation. */
  gapJson?: string;
  compact?: boolean;
}) {
  const [verdict, setVerdict] = useState<'confirmed' | 'corrected' | 'rejected'>('confirmed');
  const [pending, setPending] = useState(false);
  const sel = 'h-8 rounded-md border border-line bg-surface px-2 text-xs text-ink';
  return (
    <form action={async (fd) => { setPending(true); try { await action(fd); } finally { setPending(false); } }} className={compact ? 'flex flex-wrap items-center gap-1.5' : 'flex flex-wrap items-center gap-2'}>
      <input type="hidden" name="sectionId" value={sectionId} />
      <input type="hidden" name="learnerId" value={learnerId} />
      <input type="hidden" name="gapId" value={gapId} />
      {gapJson && <input type="hidden" name="gap" value={gapJson} />}
      <select name="verdict" aria-label="Your verdict" className={sel} value={verdict} onChange={(e) => setVerdict(e.target.value as typeof verdict)}>
        <option value="confirmed">Confirm {code}</option>
        <option value="corrected">Correct to…</option>
        <option value="rejected">Not a gap</option>
      </select>
      {verdict === 'corrected' && (
        <select name="correctedCode" aria-label="Corrected gap" className={sel} defaultValue={GAP_CODES.find((c) => c !== code)}>
          {GAP_CODES.filter((c) => c !== code).map((c) => <option key={c} value={c}>{c} {LABEL[c]}</option>)}
        </select>
      )}
      <input name="note" aria-label="Note" placeholder="Note (optional)" maxLength={140} className="h-8 w-36 min-w-0 rounded-md border border-line bg-surface px-2 text-xs text-ink" />
      <Button type="submit" size="sm" variant="secondary" disabled={pending}>{pending ? 'Saving…' : 'Save'}</Button>
    </form>
  );
}
