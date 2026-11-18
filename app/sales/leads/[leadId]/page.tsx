import Link from 'next/link';
import { notFound } from 'next/navigation';
import {
  ArrowLeft, ArrowRightLeft, CalendarCheck, CheckCircle2, CreditCard, ExternalLink, FileUp, Mail, MessageCircle, Phone, Rocket, StickyNote, UserCog,
} from 'lucide-react';
import { Avatar, Badge, Card, CardBody, CardHeader, PageHeader, buttonVariants } from '@/components/ui';
import { Submit } from '@/components/crm/submit';
import { DefRow, Field, fmtDateTime, fmtDateYear, inputCls, PaymentBadge, ScorePill, StatusBadge, textareaCls, toLocalInput } from '@/components/crm/ui';
import {
  addNote, bookDemo, completeFollowUp, convertToPlatform, logCall, markDemoDone, markLost, markPaymentFailed, moveStageForm, openInPlatform,
  recordPayment, scheduleFollowUp, sendProposal, sendTemplateMessage,
} from '@/lib/actions/crm';
import {
  FUNNEL, INTEREST_LABEL, LOST_REASONS, SOURCE_LABEL, STATUS_LABEL, followUpState, getConversion, getLead, getLeadActivities, getLeadFollowUps,
  getLeadPayments, getPackage, getRule, listPackages, listSubscriptions, listTemplates, renderTemplate, repName, type Activity,
} from '@/lib/data/crm';
import { getAdult, getStudent } from '@/lib/data';
import { getPersona } from '@/lib/data/personas';
import { DEMO_NOW_ISO } from '@/lib/demo-clock';
import { formatInr } from '@/lib/format';
import { cn } from '@/lib/utils';

const ICON: Record<Activity['type'], typeof Phone> = {
  stage: ArrowRightLeft, call: Phone, whatsapp: MessageCircle, email: Mail, demo: CalendarCheck, note: StickyNote, payment: CreditCard,
  handoff: Rocket, assign: UserCog, import: FileUp,
};
const ICON_TONE: Partial<Record<Activity['type'], string>> = {
  whatsapp: 'bg-success-50 text-success-700', payment: 'bg-warning-50 text-warning-700', handoff: 'bg-brand-50 text-brand-700', stage: 'bg-info-50 text-info-600',
};

export default async function LeadDetail({ params }: { params: Promise<{ leadId: string }> }) {
  const { leadId } = await params;
  const lead = getLead(leadId);
  if (!lead) notFound();
  const acts = getLeadActivities(lead.id);
  const fus = getLeadFollowUps(lead.id);
  const openFus = fus.filter((f) => f.status === 'open');
  const pays = getLeadPayments(lead.id);
  const pending = pays.find((p) => p.status === 'pending');
  const paid = pays.find((p) => p.status === 'paid');
  const pkg = getPackage(lead.packageId);
  const conv = getConversion(lead.id);
  const subs = listSubscriptions().filter((s) => s.leadId === lead.id);
  const templates = listTemplates();
  const stageIdx = FUNNEL.indexOf(lead.status === 'converted' ? 'closed_won' : lead.status);
  const lostLike = lead.status === 'closed_lost' || lead.status === 'nurture';
  const tomorrow6 = toLocalInput(new Date(Date.parse(DEMO_NOW_ISO.replace('09:00:00', '18:00:00')) + 86_400_000).toISOString());
  const id = <input type="hidden" name="leadId" value={lead.id} />;

  return (
    <>
      <Link href="/sales/leads" className="mb-3 inline-flex items-center gap-1 text-sm text-muted hover:text-ink"><ArrowLeft className="size-4" /> Leads</Link>
      <PageHeader
        eyebrow={`${lead.id.replace('lead_', 'Lead #')} · ${SOURCE_LABEL[lead.source]}`}
        title={<span className="flex flex-wrap items-center gap-3">{lead.parentName} <StatusBadge status={lead.status} /></span>}
        description={`Parent of ${lead.studentName}, Class ${lead.grade} ${lead.board.toUpperCase()} · ${lead.city} · owner ${repName(lead.ownerId)}`}
        actions={<>
          <a href={`tel:${lead.phone.replace(/\s/g, '')}`} className={buttonVariants({ variant: 'secondary', size: 'sm' })}><Phone /> Call</a>
          <a href="#message" className={buttonVariants({ variant: 'secondary', size: 'sm' })}><MessageCircle /> WhatsApp</a>
        </>}
      />

      {/* stage stepper */}
      <Card className="mb-6 overflow-x-auto p-4">
        <ol className="flex min-w-[640px] items-center gap-1 text-xs" data-testid="stepper">
          {FUNNEL.map((s, i) => (
            <li key={s} className={cn('flex-1 rounded-md px-2 py-1.5 text-center font-medium',
              lostLike ? 'bg-surface-muted text-subtle' : i < stageIdx ? 'bg-brand-100 text-brand-700' : i === stageIdx ? 'bg-brand-600 text-white' : 'bg-surface-muted text-subtle')}>
              {STATUS_LABEL[s]}
            </li>
          ))}
          {lead.status === 'converted' && <li className="flex-1 rounded-md bg-success-600 px-2 py-1.5 text-center font-medium text-white">Converted</li>}
        </ol>
        {lostLike && <p className="mt-2 text-sm text-danger-700">{STATUS_LABEL[lead.status]}{lead.lostReason ? `: ${lead.lostReason}` : ''}</p>}
      </Card>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="space-y-6">
          <Card>
            <CardHeader title="Profile" />
            <CardBody className="pt-2">
              <dl className="divide-y divide-line">
                <DefRow label="Student">{lead.studentName}</DefRow>
                <DefRow label="Class and board">Class {lead.grade} · {lead.board.toUpperCase()}</DefRow>
                <DefRow label="Parent">{lead.parentName}</DefRow>
                <DefRow label="Phone"><span className="tabular-nums">{lead.phone}</span></DefRow>
                <DefRow label="Email"><span className="break-all">{lead.email}</span></DefRow>
                <DefRow label="City">{lead.city}</DefRow>
                <DefRow label="Interest">{INTEREST_LABEL[lead.interest]}</DefRow>
                <DefRow label="Source">{SOURCE_LABEL[lead.source]}</DefRow>
                <DefRow label="Campaign">{lead.campaign}</DefRow>
                <DefRow label="Score"><ScorePill score={lead.score} /></DefRow>
                <DefRow label="Created">{fmtDateTime(lead.createdUtc)}</DefRow>
                <DefRow label="Last contacted">{fmtDateTime(lead.lastContactedUtc)}</DefRow>
                {lead.demoUtc && <DefRow label="Demo">{fmtDateTime(lead.demoUtc)}</DefRow>}
              </dl>
              {lead.notes && <p className="mt-3 rounded-lg bg-surface-muted p-3 text-sm text-muted">{lead.notes}</p>}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Deal" />
            <CardBody className="pt-2">
              <dl className="divide-y divide-line">
                <DefRow label="Package">{pkg?.name ?? 'Not chosen yet'}</DefRow>
                <DefRow label="Value">{lead.valueInr ? `${formatInr(lead.valueInr)} + GST` : '—'}</DefRow>
              </dl>
              {pays.length > 0 && (
                <ul className="mt-3 space-y-2">{pays.map((p) => (
                  <li key={p.id} className="rounded-lg border border-line p-3 text-sm">
                    <div className="flex items-center justify-between gap-2"><span className="font-medium tabular-nums">{formatInr(p.totalInr)}</span><PaymentBadge status={p.status} /></div>
                    <p className="mt-1 truncate text-xs text-muted">{p.link}</p>
                    <p className="text-xs text-muted">Sent {fmtDateTime(p.createdUtc)}{p.paidUtc ? ` · paid ${fmtDateTime(p.paidUtc)} by ${p.method}` : ''}</p>
                    {p.invoiceNo && <Link href={`/sales/payments/${p.id}`} className="mt-1 inline-block text-xs font-medium text-brand-700 hover:underline">Invoice {p.invoiceNo} · receipt {p.receiptNo}</Link>}
                  </li>
                ))}</ul>
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Next follow-up" description={openFus.length ? undefined : 'Nothing scheduled.'} />
            <CardBody className="space-y-3 pt-2">
              {openFus.map((f) => {
                const st = followUpState(f);
                return (
                  <div key={f.id} className="flex items-start justify-between gap-3 rounded-lg border border-line p-3">
                    <div className="min-w-0 text-sm">
                      <p className="font-medium text-ink">{f.title}</p>
                      <p className="text-xs text-muted">{fmtDateTime(f.dueUtc)} · {getRule(f.ruleId)?.name}</p>
                      <Badge tone={st === 'overdue' ? 'danger' : st === 'today' ? 'warning' : 'neutral'} className="mt-1">{st === 'overdue' ? 'Overdue' : st === 'today' ? 'Due today' : 'Upcoming'}</Badge>
                    </div>
                    <form action={completeFollowUp}>{id}<input type="hidden" name="id" value={f.id} /><Submit size="sm" variant="secondary">Done</Submit></form>
                  </div>
                );
              })}
              <details className="rounded-lg border border-dashed border-line p-3">
                <summary className="cursor-pointer text-sm font-medium text-brand-700">Schedule a follow-up</summary>
                <form action={scheduleFollowUp} className="mt-3 grid gap-2">
                  {id}
                  <Field label="What"><input name="title" placeholder="Call back about the plan" className={inputCls} /></Field>
                  <Field label="When (IST)"><input type="datetime-local" name="when" defaultValue={tomorrow6} className={inputCls} /></Field>
                  <Field label="Channel"><select name="channel" className={inputCls}><option value="call">Call</option><option value="whatsapp">WhatsApp</option><option value="email">Email</option></select></Field>
                  <Submit size="sm">Schedule</Submit>
                </form>
              </details>
            </CardBody>
          </Card>
        </div>

        <div className="space-y-6 lg:col-span-2">
          {/* contextual next step */}
          <Card className="border-brand-200">
            <CardHeader title="Next step" description={nextStepHint(lead.status, !!pending)} />
            <CardBody className="space-y-4">
              {['new', 'contacted', 'qualified'].includes(lead.status) && (
                <form action={bookDemo} className="flex flex-wrap items-end gap-3" data-testid="book-demo">
                  {id}
                  <Field label="Demo time (IST)"><input type="datetime-local" name="when" defaultValue={tomorrow6} className={inputCls} /></Field>
                  <Submit pendingText="Booking…"><CalendarCheck /> Book demo</Submit>
                </form>
              )}
              {lead.status === 'demo_booked' && (
                <form action={markDemoDone} className="grid gap-3">
                  {id}
                  <p className="text-sm text-muted">Demo on {fmtDateTime(lead.demoUtc)}. Reminders go out 24 hours and 1 hour before.</p>
                  <Field label="Demo notes"><textarea name="notes" className={textareaCls} placeholder="What the family liked, questions asked" /></Field>
                  <div><Submit><CheckCircle2 /> Mark demo done</Submit></div>
                </form>
              )}
              {['qualified', 'demo_done', 'negotiation', 'proposal_sent'].includes(lead.status) && !paid && (
                <form action={sendProposal} className="flex flex-wrap items-end gap-3" data-testid="send-proposal">
                  {id}
                  <Field label={pending ? 'Send a revised proposal' : 'Package'} className="min-w-64 flex-1">
                    <select name="packageId" defaultValue={lead.packageId ?? listPackages().find((p) => p.interests.includes(lead.interest))?.id} className={inputCls}>
                      {listPackages().map((p) => <option key={p.id} value={p.id}>{p.name} · {formatInr(p.priceInr)} + GST</option>)}
                    </select>
                  </Field>
                  <Submit variant={pending ? 'secondary' : 'primary'} pendingText="Sending…"><Mail /> {pending ? 'Resend proposal' : 'Send proposal'}</Submit>
                </form>
              )}
              {pending && (
                <div className="rounded-lg bg-warning-50 p-4" data-testid="record-payment">
                  <p className="text-sm font-medium text-warning-700">Payment pending: {formatInr(pending.totalInr)} incl. GST for {getPackage(pending.packageId)?.name}</p>
                  <p className="mt-0.5 truncate text-xs text-warning-700/80">{pending.link}</p>
                  <div className="mt-3 flex flex-wrap items-end gap-3">
                    <form action={recordPayment} className="flex flex-wrap items-end gap-3">
                      {id}
                      <Field label="Paid by"><select name="method" className={inputCls}><option>UPI</option><option>Card</option><option>Net banking</option></select></Field>
                      <Submit pendingText="Recording…"><CreditCard /> Record payment</Submit>
                    </form>
                    <form action={markPaymentFailed}>{id}<Submit variant="ghost" size="sm">Mark failed</Submit></form>
                    {lead.status === 'proposal_sent' && <form action={moveStageForm}>{id}<input type="hidden" name="to" value="negotiation" /><Submit variant="ghost" size="sm">Move to negotiation</Submit></form>}
                  </div>
                </div>
              )}
              {conv?.status === 'waiting' && (
                <div className="rounded-lg bg-success-50 p-4" data-testid="convert">
                  <p className="text-sm font-medium text-success-700">Paid {fmtDateTime(paid?.paidUtc)}. Ready to hand over to the platform.</p>
                  <p className="mt-0.5 text-xs text-success-700/80">Creates or activates the learner and parent, assigns {getAdult(conv.counsellorId)?.name ?? 'the counsellor'}, starts the {pkg?.name ?? 'plan'} subscription and files the invoice.</p>
                  <form action={convertToPlatform} className="mt-3">{id}<Submit pendingText="Converting…"><Rocket /> Convert to platform</Submit></form>
                </div>
              )}
              {conv?.status === 'handed_over' && (
                <div className="rounded-lg bg-brand-50 p-4" data-testid="converted">
                  <p className="text-sm font-medium text-brand-700">Handed over {fmtDateTime(conv.handedOverUtc)} · counsellor {getAdult(conv.counsellorId)?.name ?? conv.counsellorId}</p>
                  {subs.map((s) => <p key={s.id} className="mt-0.5 text-xs text-brand-700/80">Subscription {s.id}: {getPackage(s.packageId)?.name}, from {fmtDateYear(s.startUtc)}{s.endUtc ? ` to ${fmtDateYear(s.endUtc)}` : ''}</p>)}
                  <div className="mt-3 flex flex-wrap gap-2">
                    {conv.learnerIds.map((lid) => {
                      const persona = getPersona(lid);
                      const st = getStudent(lid);
                      return persona ? (
                        <form key={lid} action={openInPlatform}>
                          <input type="hidden" name="learnerId" value={lid} />
                          <Submit size="sm" pendingText="Opening…"><ExternalLink /> Open {st?.firstName ?? persona.name.split(' ')[0]} in platform</Submit>
                        </form>
                      ) : (
                        <Badge key={lid} tone="brand">Learner {lid} created · sign-in link sent by WhatsApp</Badge>
                      );
                    })}
                  </div>
                </div>
              )}
              {lostLike && <p className="text-sm text-muted">On the monthly nurture drip. Book a demo or send a proposal to reopen it.</p>}
              {lostLike && (
                <form action={moveStageForm} className="flex gap-2">{id}<input type="hidden" name="to" value="contacted" /><Submit size="sm" variant="secondary">Reopen as Contacted</Submit></form>
              )}
              {!lostLike && lead.status !== 'closed_won' && lead.status !== 'converted' && (
                <details className="text-sm">
                  <summary className="cursor-pointer text-muted hover:text-ink">Mark lost</summary>
                  <form action={markLost} className="mt-3 flex flex-wrap items-end gap-3">
                    {id}
                    <Field label="Reason"><select name="reason" className={inputCls}>{LOST_REASONS.map((r) => <option key={r}>{r}</option>)}</select></Field>
                    <label className="flex items-center gap-2 pb-2 text-sm"><input type="checkbox" name="nurture" defaultChecked className="size-4" /> Keep on nurture</label>
                    <Submit variant="danger" size="sm">Mark lost</Submit>
                  </form>
                </details>
              )}
            </CardBody>
          </Card>

          <div className="grid gap-6 md:grid-cols-2">
            <Card id="message">
              <CardHeader title="Send a template" description="Logs the message on the timeline. Nothing is really sent." />
              <CardBody className="pt-3">
                <form action={sendTemplateMessage} className="grid gap-3" data-testid="send-template">
                  {id}
                  <select name="templateId" className={inputCls} aria-label="Template">
                    {templates.map((t) => <option key={t.id} value={t.id}>{t.channel === 'email' ? 'Email' : 'WhatsApp'} · {t.name}</option>)}
                  </select>
                  <details className="text-xs text-muted"><summary className="cursor-pointer">Preview all templates</summary>
                    <ul className="mt-2 space-y-2">{templates.map((t) => <li key={t.id}><span className="font-medium text-ink">{t.name}:</span> {renderTemplate(t, lead)}</li>)}</ul>
                  </details>
                  <div><Submit size="sm" pendingText="Sending…"><MessageCircle /> Send</Submit></div>
                </form>
              </CardBody>
            </Card>
            <Card>
              <CardHeader title="Log a call or note" />
              <CardBody className="pt-3">
                <form action={logCall} className="grid gap-3">
                  {id}
                  <div className="grid grid-cols-2 gap-2">
                    <select name="outcome" className={inputCls} aria-label="Outcome">
                      <option value="connected">Connected</option><option value="no_answer">No answer</option><option value="busy">Busy</option><option value="call_back">Call back</option>
                    </select>
                    <input name="minutes" type="number" min={0} max={90} placeholder="Minutes" className={inputCls} aria-label="Minutes" />
                  </div>
                  <textarea name="notes" className={textareaCls} placeholder="What was discussed" aria-label="Call notes" />
                  <div className="flex gap-2">
                    <Submit size="sm"><Phone /> Log call</Submit>
                    <Submit size="sm" variant="secondary" formAction={addNote}><StickyNote /> Save as note</Submit>
                  </div>
                </form>
              </CardBody>
            </Card>
          </div>

          <Card>
            <CardHeader title="Timeline" description={`${acts.length} activities, newest first.`} />
            <CardBody className="pt-3">
              <ol className="relative space-y-4 border-l border-line pl-6" data-testid="timeline">
                {acts.map((a) => {
                  const Icon = ICON[a.type];
                  return (
                    <li key={a.id} className="relative">
                      <span className={cn('absolute -left-[37px] flex size-6 items-center justify-center rounded-full bg-surface-muted text-muted ring-4 ring-surface', ICON_TONE[a.type])}><Icon className="size-3.5" /></span>
                      <div className="flex flex-wrap items-baseline justify-between gap-x-3">
                        <p className="text-sm font-medium text-ink">{a.title}{a.auto && <Badge className="ml-2">Auto</Badge>}</p>
                        <span className="text-xs tabular-nums text-subtle">{fmtDateTime(a.atUtc)}</span>
                      </div>
                      <p className="text-xs text-muted">{repName(a.byId)}{a.ruleId ? ` · rule: ${getRule(a.ruleId)?.name}` : ''}</p>
                      {(a.body || a.templateId) && <p className="mt-1 text-sm text-muted">{a.body ?? (a.templateId ? renderTemplate(listTemplates().find((t) => t.id === a.templateId)!, lead) : '')}</p>}
                    </li>
                  );
                })}
              </ol>
            </CardBody>
          </Card>
        </div>
      </div>
    </>
  );
}

function nextStepHint(status: string, pending: boolean): string {
  switch (status) {
    case 'new': return 'Call within the hour, then book a demo.';
    case 'contacted': return 'Qualify the need and book a demo.';
    case 'qualified': return 'Book a demo or send a proposal.';
    case 'demo_booked': return 'Run the demo, then mark it done.';
    case 'demo_done': return 'Send a proposal while it is fresh.';
    case 'proposal_sent':
    case 'negotiation': return pending ? 'Waiting for payment. Record it when the family pays.' : 'Send the proposal again.';
    case 'closed_won': return 'Paid. Hand the family over to the platform.';
    case 'converted': return 'This family is on the platform.';
    default: return 'This lead is closed.';
  }
}
