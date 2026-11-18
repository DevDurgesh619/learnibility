import { Eye, EyeOff, FileCheck2, Lock, ShieldCheck } from 'lucide-react';
import { grantConsent, revokeConsent } from '@/lib/actions/parent';
import { ChildSwitcher } from '@/components/parent/child-switcher';
import { param, parentContext, type SearchParams } from '@/components/parent/context';
import { fmtDateYear } from '@/components/parent/format';
import { NoChild } from '@/components/parent/no-child';
import { Notice } from '@/components/parent/notice';
import { Badge, Button, Card, CardBody, CardHeader, EmptyState, PageHeader, Table, TBody, TD, TH, THead, TierBadge, TR } from '@/components/ui';
import { getConsents, getPersonName, getProfile, listParameters, type Consent } from '@/lib/data';
import { ROLE_LABEL } from '@/lib/nav';
import type { Role, Tier } from '@/lib/types';
import { VISIBILITY, type VisibilityMode } from '@/lib/visibility';

const TIER_TEXT: Record<Tier, string> = {
  T1: 'Marks, test answers, study habits, interests and goals. Used to plan learning.',
  T2: 'Family, money, personality and identity-adjacent answers. Only summaries reach you; nobody sees them word for word except your child and their counsellor.',
  T3: 'Health and wellbeing screening. Used only to adapt support. Never used for ranking, admissions fit, career fit or tutor matching.',
  C: 'Your consents. They control what is processed, and are never treated as a trait of your child.',
};

const SCOPES: { scope: Consent['scope']; label: string; detail: string; required?: boolean }[] = [
  { scope: 'edu_personalisation', label: 'Personalised learning', detail: 'Use test results and study data to build gaps, plans and timetables.', required: true },
  { scope: 'share_with_tutor', label: 'Share gap snapshot with booked tutors', detail: 'A booked tutor sees the gaps in the subject they teach, nothing else.' },
  { scope: 'share_with_school', label: 'Share progress with school teachers', detail: "Teachers see mastery and gaps (T1 only) for their own class." },
  { scope: 'wellbeing_screening', label: 'Wellbeing check-ins', detail: 'The counsellor may run short wellbeing check-ins. Answers stay with the counsellor.' },
  { scope: 'data_research', label: 'Anonymised research', detail: 'Use anonymised data to improve the method. Never sold.' },
  { scope: 'marketing', label: 'Product updates', detail: 'Occasional emails about new features.' },
];

const MODE: Record<VisibilityMode, { label: string; tone: 'success' | 'warning' | 'neutral' | 'info' }> = {
  full: { label: 'Full', tone: 'success' }, summary: { label: 'Summary', tone: 'warning' }, shared_only: { label: 'If shared', tone: 'info' }, hidden: { label: 'Hidden', tone: 'neutral' },
};
const ROLES: Role[] = ['student', 'parent', 'counsellor', 'teacher', 'tutor', 'mentor'];
const TIERS: Tier[] = ['T1', 'T2', 'T3', 'C'];

export default async function ParentPrivacy({ searchParams }: { searchParams: SearchParams }) {
  const sp = await searchParams;
  const { children, child } = await parentContext(searchParams);
  if (!child) return (<><PageHeader eyebrow="Parent" title="Privacy and consent" /><NoChild /></>);
  const s = child.student;
  // Filtered for the parent role: T2 and T3 arrive as summaries (no values).
  const visible = getProfile(s.id, 'parent');
  const params = new Map(listParameters().map((p) => [p.id, p]));
  const byTier = (t: Tier) => visible.filter((v) => v.tier === t);
  const t1BySection = new Map<string, number>();
  for (const v of byTier('T1')) {
    const sec = params.get(v.paramId)?.section ?? 'Other';
    t1BySection.set(sec, (t1BySection.get(sec) ?? 0) + 1);
  }
  const consents = getConsents(s.id);
  const active = new Map(consents.filter((c) => !c.revokedUtc).map((c) => [c.scope, c]));
  const done = param(sp, 'done');

  return (
    <>
      <PageHeader eyebrow="Parent" title="Privacy and consent" description={`What Learnibility holds about ${s.firstName}, who can see it, and the consents you have given.`} />
      <ChildSwitcher children={children} selectedId={s.id} basePath="/parent/privacy" />
      {done === 'revoked' && <Notice>Consent withdrawn. Processing under it has stopped from today.</Notice>}
      {done === 'granted' && <Notice>Consent recorded with today&apos;s date.</Notice>}

      <section className="mb-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {TIERS.map((t) => (
          <Card key={t}>
            <CardBody className="space-y-2">
              <div className="flex items-center justify-between"><TierBadge tier={t} /><span className="text-2xl font-semibold text-ink">{t === 'C' ? consents.length : byTier(t).length}</span></div>
              <p className="text-sm text-muted">{TIER_TEXT[t]}</p>
              <p className="flex items-center gap-1.5 text-xs font-medium text-ink">
                {VISIBILITY.parent[t] === 'full' ? <><Eye className="size-3.5" />You see these in full</> : <><EyeOff className="size-3.5" />You see a summary only</>}
              </p>
            </CardBody>
          </Card>
        ))}
      </section>

      <div className="mb-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader title="What is collected (standard tier)" description="Parameters with a value, by profile section" />
          <CardBody className="pt-3">
            {t1BySection.size ? (
              <ul className="divide-y divide-line">{[...t1BySection.entries()].sort((a, b) => b[1] - a[1]).map(([sec, n]) => (
                <li key={sec} className="flex items-center justify-between py-2 text-sm"><span className="text-ink">{sec}</span><span className="text-muted">{n}</span></li>
              ))}</ul>
            ) : <p className="text-sm text-muted">Nothing collected yet.</p>}
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Sensitive tiers, as summaries" description="You see that these exist and when they were updated, not the answers" />
          <CardBody className="space-y-4 pt-3">
            {(['T2', 'T3'] as const).map((t) => {
              const list = byTier(t);
              const last = list.map((v) => v.asOfUtc ?? '').sort().pop();
              return (
                <div key={t} className="flex items-start gap-3 rounded-lg border border-line px-4 py-3">
                  <Lock className="mt-0.5 size-4 text-subtle" />
                  <div className="text-sm">
                    <p className="font-medium text-ink">{t === 'T2' ? 'Family, money and personality' : 'Wellbeing and health'}</p>
                    <p className="text-muted">{list.length ? `${list.length} item${list.length === 1 ? '' : 's'} held${last ? `, last updated ${fmtDateYear(last)}` : ''}. ${t === 'T3' ? 'Support is in place with the counsellor where needed.' : 'Used to fit plans and budgets.'}` : 'Nothing held.'}</p>
                  </div>
                </div>
              );
            })}
          </CardBody>
        </Card>
      </div>

      <Card className="mb-6">
        <CardHeader title="Who sees what" description="The same rule applies on every screen in the app" />
        <div className="overflow-x-auto">
          <Table className="mt-4 min-w-[560px]">
            <THead><TR><TH>Role</TH>{TIERS.map((t) => <TH key={t}>{t}</TH>)}</TR></THead>
            <TBody>{ROLES.map((r) => (
              <TR key={r}><TD className="font-medium text-ink">{r === 'student' ? s.firstName : ROLE_LABEL[r]}</TD>
                {TIERS.map((t) => <TD key={t}><Badge tone={MODE[VISIBILITY[r][t]].tone}>{MODE[VISIBILITY[r][t]].label}</Badge></TD>)}</TR>
            ))}</TBody>
          </Table>
        </div>
      </Card>

      <Card>
        <CardHeader title="Your consents" description="Dated, versioned, and you can withdraw any time" />
        <CardBody className="pt-3">
          <ul className="divide-y divide-line">
            {SCOPES.map((sc) => {
              const c = active.get(sc.scope);
              const revoked = consents.filter((x) => x.scope === sc.scope && x.revokedUtc).pop();
              return (
                <li key={sc.scope} className="flex flex-col gap-3 py-4 sm:flex-row sm:items-center sm:justify-between">
                  <div className="flex min-w-0 items-start gap-3">
                    {c ? <ShieldCheck className="mt-0.5 size-5 shrink-0 text-success-600" /> : <FileCheck2 className="mt-0.5 size-5 shrink-0 text-subtle" />}
                    <div>
                      <p className="font-medium text-ink">{sc.label}{sc.required && <span className="ml-2 text-xs font-normal text-subtle">needed for the app to work</span>}</p>
                      <p className="text-sm text-muted">{sc.detail}</p>
                      <p className="mt-1 text-xs text-subtle">
                        {c ? `Given ${fmtDateYear(c.grantedUtc)} by ${getPersonName(c.grantedById)?.name ?? 'you'} · version ${c.version}` : revoked ? `Withdrawn ${fmtDateYear(revoked.revokedUtc!)}` : 'Not given'}
                      </p>
                    </div>
                  </div>
                  <form action={c ? revokeConsent : grantConsent} className="shrink-0">
                    <input type="hidden" name="learnerId" value={s.id} />
                    {c ? <input type="hidden" name="consentId" value={c.id} /> : <input type="hidden" name="scope" value={sc.scope} />}
                    <Button type="submit" size="sm" variant={c ? 'secondary' : 'primary'}>{c ? 'Withdraw' : 'Give consent'}</Button>
                  </form>
                </li>
              );
            })}
          </ul>
          {!consents.length && <EmptyState className="mt-4" title="No consents recorded" description="Consents you give during sign-up appear here with their dates." />}
        </CardBody>
      </Card>
    </>
  );
}
