import type { Metadata } from 'next';
import { getTutor } from '@/components/marketplace/queries';
import { Saved } from '@/components/tutor/form-bits';
import { readPrefs, withPrefs } from '@/components/tutor/prefs';
import { SectionTitle } from '@/components/tutor/bits';
import { money } from '@/components/tutor/model';
import { Button } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { saveTutorPrefs } from '@/lib/actions/tutor';
import { currentPersona } from '@/lib/session';

export const metadata: Metadata = { title: 'Pricing · Tutor' };

const input = 'h-9 w-28 rounded-lg border border-line bg-surface px-2 text-sm text-ink';

/** Tutor HTML 8d: rates per session type with what the tutor receives after the fee, plus one package. Sample prices. */
export default async function PricingPage({ searchParams }: { searchParams: Promise<{ saved?: string }> }) {
  const sp = await searchParams;
  const persona = (await currentPersona())!;
  const t = withPrefs(getTutor(persona.id)!, await readPrefs(persona.id));
  const p = t.pricing;
  const fee = t.platformFeeRate ?? 0.15;
  const net = (x: number) => money(x - Math.round(x * fee));
  const pkg = p.packages[0];
  return (
    <form action={saveTutorPrefs}>
      <input type="hidden" name="back" value="/tutor/profile/pricing" />
      <input type="hidden" name="section" value="pricing" />
      <Saved show={sp.saved}>Rates saved. They apply to new bookings only.</Saved>
      <Card><CardBody className="space-y-6">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[520px] text-sm">
            <thead><tr className="text-left text-muted"><th className="pb-2 font-medium">Session type</th><th className="pb-2 font-medium">Your rate (₹)</th><th className="pb-2 font-medium">You receive</th><th className="pb-2 font-medium">Market range</th></tr></thead>
            <tbody className="divide-y divide-line">
              <tr><td className="py-3 text-ink">1:1 · {t.sessionMinutes} min</td><td><input name="oneToOne" type="number" min={0} step={50} defaultValue={p.oneToOnePerHourInr} className={input} aria-label="1:1 rate" /></td><td className="text-ink">{net(p.oneToOnePerHourInr)}</td><td className="text-muted">₹600–1,000</td></tr>
              <tr><td className="py-3 text-ink">Group{p.groupSize ? ` (${p.groupSize[0]}–${p.groupSize[1]})` : ''} · per student</td><td><input name="group" type="number" min={0} step={50} defaultValue={p.groupPerStudentPerHourInr ?? ''} placeholder="No groups" className={input} aria-label="Group rate" /></td><td className="text-ink">{p.groupPerStudentPerHourInr ? net(p.groupPerStudentPerHourInr) : '—'}</td><td className="text-muted">₹250–450</td></tr>
              <tr><td className="py-3 text-ink">Demo · {p.demoMinutes} min</td><td><input name="demo" type="number" min={0} step={50} defaultValue={p.demoInr} className={input} aria-label="Demo price" /></td><td className="text-ink">{p.demoInr ? net(p.demoInr) : 'Free'}</td><td className="text-muted">most tutors: free</td></tr>
            </tbody>
          </table>
        </div>
        <section>
          <SectionTitle>Package (optional)</SectionTitle>
          <div className="flex flex-wrap items-center gap-2 text-sm text-muted">
            <input name="pkgSessions" type="number" min={0} defaultValue={pkg?.sessions ?? ''} placeholder="8" className={input} aria-label="Sessions in package" /> sessions a month for ₹
            <input name="pkgPrice" type="number" min={0} step={100} defaultValue={pkg?.priceInr ?? ''} placeholder="6000" className={input} aria-label="Package price" />
            {pkg && <span>· saves the student {money(pkg.sessions * p.oneToOnePerHourInr - pkg.priceInr)}</span>}
          </div>
        </section>
        <p className="rounded-lg bg-surface-muted p-3 text-sm text-muted">New rates apply to new bookings only. Existing students keep their rate until you tell them. Platform fee {Math.round(fee * 100)}% per session.</p>
        <div className="flex justify-end"><Button type="submit">Save</Button></div>
      </CardBody></Card>
    </form>
  );
}
