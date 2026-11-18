import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { BadgeCheck, CheckCircle2 } from 'lucide-react';
import { SectionTitle } from '@/components/tutor/bits';
import { loadWorkspace } from '@/components/tutor/model';
import { readPrefs } from '@/components/tutor/prefs';
import { Button } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { saveTutorPrefs } from '@/lib/actions/tutor';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Payout settings · Tutor' };

/** Tutor HTML 7c: where the money goes. Account, schedule, tax id; not an accounting module. Sample bank details. */
export default async function PayoutSettingsPage({ searchParams }: { searchParams: Promise<{ saved?: string }> }) {
  const sp = await searchParams;
  const persona = (await currentPersona())!;
  const ws = loadWorkspace(persona.id);
  if (!ws) notFound();
  const p = (await readPrefs(persona.id)).payout ?? { schedule: 'weekly', minimumInr: 1000 };
  const field = 'h-10 w-full rounded-lg border border-line bg-surface px-3 text-sm text-ink';
  return (
    <form action={saveTutorPrefs} className="max-w-2xl">
      <input type="hidden" name="back" value="/tutor/earnings/settings" />
      {sp.saved && <p className="mb-4 flex items-center gap-2 rounded-lg bg-success-50 px-3 py-2 text-sm text-success-700"><CheckCircle2 className="size-4" />Payout settings saved.</p>}
      <Card><CardBody className="space-y-6">
        <section>
          <SectionTitle>Bank account</SectionTitle>
          <div className="flex items-center justify-between rounded-lg border border-line p-3 text-sm">
            <span className="text-ink">HDFC Bank · ••••4821 · {ws.tutor.displayName}</span>
            <span className="inline-flex items-center gap-1 text-success-700"><BadgeCheck className="size-4" />Verified</span>
          </div>
          <label className="mt-3 block text-sm text-muted">UPI id (optional)<input name="upi" defaultValue={p.upi} placeholder="name@bank" className={`${field} mt-1`} /></label>
        </section>
        <section>
          <SectionTitle>Payout schedule</SectionTitle>
          <div className="flex gap-4 text-sm">
            {(['weekly', 'monthly'] as const).map((v) => <label key={v} className="flex items-center gap-2"><input type="radio" name="schedule" value={v} defaultChecked={p.schedule === v} className="accent-brand-600" />{v === 'weekly' ? 'Weekly (Mon)' : 'Monthly (1st)'}</label>)}
          </div>
          <label className="mt-3 block text-sm text-muted">Minimum payout (₹)<input name="minimumInr" type="number" min={0} step={100} defaultValue={p.minimumInr} className={`${field} mt-1 max-w-40`} /></label>
        </section>
        <section>
          <SectionTitle>Tax details</SectionTitle>
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="text-sm text-muted">PAN<input disabled value="ABCDE1234F" className={`${field} mt-1 bg-surface-muted`} /></label>
            <label className="text-sm text-muted">GSTIN (optional)<input name="gstin" defaultValue={p.gstin} className={`${field} mt-1`} /></label>
          </div>
          <p className="mt-2 text-xs text-subtle">TDS is deducted as per rules; certificates appear here quarterly.</p>
        </section>
        <input type="hidden" name="section" value="payout" />
        <div className="flex justify-end"><Button type="submit">Save</Button></div>
      </CardBody></Card>
    </form>
  );
}

