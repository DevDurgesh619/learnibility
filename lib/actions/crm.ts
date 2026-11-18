'use server';

/**
 * W3-CRM writes. Every action logs an activity with the signed-in rep and the demo clock, and lands in the
 * demo overlay (Reset demo restores the CRM). "Convert to platform" hands the family over to the core
 * platform through lib/actions/core.ts.
 */
import { revalidatePath } from 'next/cache';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { appendEvent, newId, nowStamp, putRecord } from '@/lib/actions/core';
import { getAdult, getStudent } from '@/lib/data';
import type { Adult, Invoice, Student } from '@/lib/data/types';
import { learnerId as makeLearnerId, personId } from '@/lib/ids';
import { SESSION_COOKIE, currentPersona } from '@/lib/session';
import {
  LEAD_STATUSES, STATUS_LABEL, crmPut, getConversion, getLead, getLeadFollowUps, getLeadPayments, getPackage, getTemplate, gstFor,
  listLeadsRaw, renderTemplate, type Activity, type Conversion, type FollowUp, type Lead, type LeadStatus, type Payment, type Subscription,
} from '@/lib/data/crm';

async function rep(): Promise<string> {
  const p = await currentPersona();
  if (!p || p.role !== 'sales') redirect('/login');
  return p.id;
}

function log(lead: Lead, a: Omit<Activity, 'id' | 'leadId' | 'atUtc'> & { atUtc?: string }): Activity {
  const rec: Activity = { id: newId('act'), leadId: lead.id, atUtc: a.atUtc ?? nowStamp(), ...a };
  crmPut('crm_activities', rec);
  return rec;
}

function setStage(lead: Lead, to: LeadStatus, by: string, body?: string): Lead {
  if (lead.status === to) return lead;
  const at = nowStamp();
  log(lead, { type: 'stage', byId: by, title: `Stage: ${STATUS_LABEL[lead.status]} → ${STATUS_LABEL[to]}`, from: lead.status, to, body, atUtc: at });
  const next = { ...lead, status: to, stageChangedUtc: at };
  crmPut('crm_leads', stripDisplay(next));
  return next;
}

/** getLead() swaps in the platform's parent name for display; store the lead's own value. */
function stripDisplay(l: Lead): Lead {
  const raw = listLeadsRaw().find((x) => x.id === l.id);
  return { ...l, parentName: raw?.parentName ?? l.parentName };
}

function saveLead(l: Lead) {
  crmPut('crm_leads', stripDisplay(l));
}

function followUp(lead: Lead, ruleId: string, channel: FollowUp['channel'], title: string, dueUtc: string) {
  crmPut('crm_followups', { id: newId('fu'), leadId: lead.id, ruleId, channel, title, dueUtc, status: 'open', ownerId: lead.ownerId } satisfies FollowUp);
}

function closeOpenFollowUps(leadId: string, ruleIds?: string[]) {
  for (const f of getLeadFollowUps(leadId)) {
    if (f.status === 'open' && (!ruleIds || ruleIds.includes(f.ruleId))) crmPut('crm_followups', { ...f, status: 'done', doneUtc: nowStamp() });
  }
}

const refresh = (leadId?: string) => {
  revalidatePath('/sales', 'layout');
  if (leadId) revalidatePath(`/sales/leads/${leadId}`);
};

function must(id: string): Lead {
  const l = getLead(id);
  if (!l) throw new Error(`Unknown lead ${id}`);
  return l;
}

// ------------------------------------------------------------------ lead detail actions

export async function sendTemplateMessage(formData: FormData) {
  const by = await rep();
  const lead = must(String(formData.get('leadId')));
  const t = getTemplate(String(formData.get('templateId')));
  if (!t) return;
  log(lead, { type: t.channel, byId: by, title: `${t.channel === 'email' ? 'Email' : 'WhatsApp'}: ${t.name}`, body: renderTemplate(t, lead), templateId: t.id });
  saveLead({ ...lead, lastContactedUtc: nowStamp() });
  if (lead.status === 'new') setStage(must(lead.id), 'contacted', by);
  refresh(lead.id);
}

export async function logCall(formData: FormData) {
  const by = await rep();
  const lead = must(String(formData.get('leadId')));
  const outcome = String(formData.get('outcome') ?? 'connected') as NonNullable<Activity['outcome']>;
  const minutes = Number(formData.get('minutes')) || (outcome === 'connected' ? 8 : 0);
  const notes = String(formData.get('notes') ?? '').trim();
  log(lead, { type: 'call', byId: by, title: outcome === 'connected' ? `Call, ${minutes} min` : `Call: ${outcome.replace('_', ' ')}`, outcome, durationMin: minutes || undefined, body: notes || undefined });
  saveLead({ ...lead, lastContactedUtc: nowStamp() });
  if (outcome === 'connected' && lead.status === 'new') setStage(must(lead.id), 'contacted', by);
  closeOpenFollowUps(lead.id, ['r_manual', 'r_no_reply_48h', 'r_proposal_3d']);
  refresh(lead.id);
}

export async function addNote(formData: FormData) {
  const by = await rep();
  const lead = must(String(formData.get('leadId')));
  const body = String(formData.get('notes') ?? '').trim();
  if (!body) return;
  log(lead, { type: 'note', byId: by, title: 'Note', body });
  refresh(lead.id);
}

export async function scheduleFollowUp(formData: FormData) {
  await rep();
  const lead = must(String(formData.get('leadId')));
  const when = String(formData.get('when') ?? '');
  const title = String(formData.get('title') ?? '').trim() || 'Call back';
  const due = when ? new Date(`${when}:00+05:30`).toISOString() : nowStamp();
  followUp(lead, 'r_manual', (String(formData.get('channel') ?? 'call') as FollowUp['channel']), title, due);
  refresh(lead.id);
}

export async function bookDemo(formData: FormData) {
  const by = await rep();
  let lead = must(String(formData.get('leadId')));
  const when = String(formData.get('when') ?? '');
  const demoUtc = when ? new Date(`${when}:00+05:30`).toISOString() : new Date(Date.parse(nowStamp()) + 26 * 3_600_000).toISOString();
  lead = { ...lead, demoUtc };
  saveLead(lead);
  lead = setStage(lead, 'demo_booked', by, `Demo on ${new Date(demoUtc).toLocaleString('en-IN', { timeZone: 'Asia/Kolkata', dateStyle: 'medium', timeStyle: 'short' })}`);
  const t = getTemplate('tpl_demo_booked')!;
  log(lead, { type: 'whatsapp', byId: by, title: `WhatsApp: ${t.name}`, body: renderTemplate(t, lead), templateId: t.id });
  followUp(lead, 'r_demo_24h', 'whatsapp', 'Demo reminder (24 h)', new Date(Date.parse(demoUtc) - 24 * 3_600_000).toISOString());
  followUp(lead, 'r_demo_1h', 'whatsapp', 'Demo reminder (1 h)', new Date(Date.parse(demoUtc) - 3_600_000).toISOString());
  refresh(lead.id);
}

export async function markDemoDone(formData: FormData) {
  const by = await rep();
  const lead = must(String(formData.get('leadId')));
  log(lead, { type: 'demo', byId: by, title: 'Demo session, 40 min', body: String(formData.get('notes') ?? '').trim() || 'Demo completed.' });
  closeOpenFollowUps(lead.id, ['r_demo_24h', 'r_demo_1h']);
  setStage(lead, 'demo_done', by);
  refresh(lead.id);
}

export async function sendProposal(formData: FormData) {
  const by = await rep();
  let lead = must(String(formData.get('leadId')));
  const p = getPackage(String(formData.get('packageId')));
  if (!p) return;
  lead = { ...lead, packageId: p.id, valueInr: p.priceInr };
  saveLead(lead);
  lead = setStage(lead, 'proposal_sent', by);
  const gst = gstFor(p.priceInr);
  const pay: Payment = {
    id: newId('pay'), leadId: lead.id, packageId: p.id, amountInr: p.priceInr, gstInr: gst, totalInr: p.priceInr + gst,
    link: `https://pay.learnibility.demo/l/${lead.id.slice(5)}${Date.now().toString(36).slice(-4)}`, status: 'pending', createdUtc: nowStamp(),
  };
  crmPut('crm_payments', pay);
  for (const id of ['tpl_proposal', 'tpl_payment_link']) {
    const t = getTemplate(id)!;
    log(lead, { type: t.channel, byId: by, title: `${t.channel === 'email' ? 'Email' : 'WhatsApp'}: ${t.name}`, body: renderTemplate(t, lead), templateId: t.id });
  }
  followUp(lead, 'r_proposal_3d', 'call', 'Proposal unpaid: call', new Date(Date.parse(nowStamp()) + 3 * 86_400_000).toISOString());
  refresh(lead.id);
}

/** Mark the open payment link paid: invoice and receipt numbers, Closed won, conversion waiting for hand-over. */
export async function recordPayment(formData: FormData) {
  const by = await rep();
  let lead = must(String(formData.get('leadId')));
  const method = (String(formData.get('method') ?? 'UPI') as Payment['method']);
  const pay = getLeadPayments(lead.id).find((p) => p.status === 'pending');
  if (!pay) return;
  const at = nowStamp();
  const seq = String(1000 + (Date.now() % 9000)).padStart(4, '0');
  const paid: Payment = { ...pay, status: 'paid', paidUtc: at, method, invoiceNo: `LRN/2026-27/${seq}`, receiptNo: `RCPT-${20000 + Number(seq)}` };
  crmPut('crm_payments', paid);
  log(lead, { type: 'payment', byId: by, title: `Payment received: ₹${paid.totalInr.toLocaleString('en-IN')} by ${method}`, body: `Invoice ${paid.invoiceNo}, receipt ${paid.receiptNo}. Recorded by ${by === lead.ownerId ? 'owner' : 'team'}.` });
  const t = getTemplate('tpl_payment_received')!;
  log(lead, { type: 'whatsapp', byId: 'system', title: `WhatsApp: ${t.name}`, body: renderTemplate(t, lead), templateId: t.id, auto: true });
  closeOpenFollowUps(lead.id);
  lead = setStage(lead, 'closed_won', by);
  const p = getPackage(paid.packageId)!;
  const conv: Conversion = {
    id: `conv_${lead.id.slice(5)}`, leadId: lead.id, status: 'waiting', wonUtc: at, learnerIds: lead.learnerIds ?? [], parentId: lead.parentId,
    counsellorId: lead.interest === 'study_abroad' ? 'csl_farah_siddiqui' : 'csl_heena_qureshi', planId: p.planId,
  };
  crmPut('crm_conversions', conv);
  refresh(lead.id);
}

export async function markPaymentFailed(formData: FormData) {
  const by = await rep();
  const lead = must(String(formData.get('leadId')));
  const pay = getLeadPayments(lead.id).find((p) => p.status === 'pending');
  if (!pay) return;
  crmPut('crm_payments', { ...pay, status: 'failed', failedUtc: nowStamp() });
  log(lead, { type: 'payment', byId: by, title: 'Payment failed', body: 'Marked failed; a new link can be sent with the proposal.' });
  refresh(lead.id);
}

export async function markLost(formData: FormData) {
  const by = await rep();
  const lead = must(String(formData.get('leadId')));
  const reason = String(formData.get('reason') ?? 'Not the right time');
  const nurture = formData.get('nurture') === 'on';
  saveLead({ ...lead, lostReason: reason });
  setStage(must(lead.id), nurture ? 'nurture' : 'closed_lost', by, `Reason: ${reason}`);
  closeOpenFollowUps(lead.id);
  followUp(lead, 'r_nurture_30d', 'whatsapp', 'Monthly nurture message', new Date(Date.parse(nowStamp()) + 30 * 86_400_000).toISOString());
  refresh(lead.id);
}

// ------------------------------------------------------------------ pipeline, lists

/** Pipeline drag and drop. Won needs a recorded payment and Lost needs a reason, so those go to the lead page. */
export async function moveLead(leadId: string, to: LeadStatus): Promise<{ ok: boolean; error?: string }> {
  const by = await rep();
  if (!LEAD_STATUSES.includes(to)) return { ok: false, error: 'Unknown stage' };
  const lead = must(leadId);
  if (to === 'closed_won' || to === 'converted') return { ok: false, error: 'Record the payment on the lead page to close it as won.' };
  if (to === 'closed_lost') return { ok: false, error: 'Mark it lost from the lead page so the reason is saved.' };
  if (lead.status === 'closed_won' || lead.status === 'converted') return { ok: false, error: 'Won deals stay won.' };
  setStage(lead, to, by);
  refresh(leadId);
  return { ok: true };
}

export async function bulkAssign(formData: FormData) {
  const by = await rep();
  const owner = String(formData.get('owner') ?? '');
  const ids = formData.getAll('ids').map(String);
  if (!owner || !ids.length) return;
  for (const id of ids) {
    const l = getLead(id);
    if (!l || l.ownerId === owner) continue;
    saveLead({ ...l, ownerId: owner });
    log(l, { type: 'assign', byId: by, title: 'Owner changed', body: `Assigned to ${owner}` });
    for (const f of getLeadFollowUps(id)) if (f.status === 'open') crmPut('crm_followups', { ...f, ownerId: owner });
  }
  refresh();
}

const IMPORT_ROWS: Pick<Lead, 'studentName' | 'parentName' | 'city' | 'grade' | 'board' | 'interest'>[] = [
  { studentName: 'Ritika Bhalla', parentName: 'Manish Bhalla', city: 'New Delhi', grade: 10, board: 'cbse', interest: 'academic_support' },
  { studentName: 'Farhan Qadri', parentName: 'Sana Qadri', city: 'Hyderabad', grade: 12, board: 'cambridge', interest: 'study_abroad' },
  { studentName: 'Isha Kulkarni', parentName: 'Mohan Kulkarni', city: 'Pune', grade: 9, board: 'ib', interest: 'full_package' },
  { studentName: 'Tejas Rao', parentName: 'Shobha Rao', city: 'Bengaluru', grade: 11, board: 'cbse', interest: 'career_counselling' },
  { studentName: 'Mahi Arora', parentName: 'Ankit Arora', city: 'Chandigarh', grade: 8, board: 'cbse', interest: 'academic_support' },
];

/** "Import CSV" (mock): adds five leads from an education-fair sign-up sheet. */
export async function importCsv() {
  const by = await rep();
  const existing = listLeadsRaw();
  if (existing.some((l) => l.campaign === 'CSV import · EduFair Nov')) return redirect('/sales/leads?imported=0');
  const reps = ['sal_aman_gupta', 'sal_neha_joseph'];
  IMPORT_ROWS.forEach((r, i) => {
    const at = nowStamp();
    const [pf, ...pl] = r.parentName.split(' ');
    const lead: Lead = {
      ...r, id: `lead_${String(9000 + i)}`, phone: `+91 90000 9${String(i + 1).padStart(4, '0')}`, email: `${pf!.toLowerCase()}.${pl.join('').toLowerCase()}@example.com`,
      source: 'school_partnership', campaign: 'CSV import · EduFair Nov', ownerId: reps[i % 2]!, score: 48 + i * 4, status: 'new', valueInr: 0,
      createdUtc: at, stageChangedUtc: at,
    };
    crmPut('crm_leads', lead);
    log(lead, { type: 'import', byId: by, title: 'Imported from CSV', body: 'edufair-signups-nov.csv, row ' + (i + 2) });
    const t = getTemplate('tpl_welcome')!;
    log(lead, { type: 'whatsapp', byId: 'system', title: `WhatsApp: ${t.name}`, body: renderTemplate(t, lead), templateId: t.id, auto: true, ruleId: 'r_welcome' });
    followUp(lead, 'r_no_reply_48h', 'whatsapp', 'No reply: send WhatsApp nudge', new Date(Date.parse(at) + 48 * 3_600_000).toISOString());
  });
  refresh();
  redirect('/sales/leads?imported=5');
}

export async function completeFollowUp(formData: FormData) {
  const by = await rep();
  const id = String(formData.get('id'));
  const lead = must(String(formData.get('leadId')));
  const f = getLeadFollowUps(lead.id).find((x) => x.id === id);
  if (!f || f.status !== 'open') return;
  crmPut('crm_followups', { ...f, status: 'done', doneUtc: nowStamp() });
  if (f.channel === 'whatsapp') {
    const tpl = f.ruleId === 'r_demo_24h' || f.ruleId === 'r_demo_1h' ? 'tpl_demo_reminder' : f.ruleId === 'r_no_show' ? 'tpl_reschedule' : f.ruleId === 'r_nurture_30d' ? 'tpl_nurture' : 'tpl_nudge';
    const t = getTemplate(tpl)!;
    log(lead, { type: 'whatsapp', byId: by, title: `WhatsApp: ${t.name}`, body: renderTemplate(t, lead), templateId: t.id, ruleId: f.ruleId });
  } else {
    log(lead, { type: f.channel === 'email' ? 'email' : 'call', byId: by, title: f.channel === 'call' ? 'Call, 6 min' : 'Email sent', outcome: f.channel === 'call' ? 'connected' : undefined, durationMin: f.channel === 'call' ? 6 : undefined, body: `Follow-up: ${f.title}`, ruleId: f.ruleId });
  }
  refresh(lead.id);
}

// ------------------------------------------------------------------ convert to platform

const PLAN_NAME = { free: 'Free', application_support: 'Application Support', full_package: 'Full package' } as const;

/**
 * Hand a paid family over to the core platform: Converted stage, hand-off event, learner and parent records
 * (Zoya's persona is activated; any other lead gets a new learner with empty states that onboarding fills),
 * counsellor assigned, subscription and invoice for the chosen plan.
 */
export async function convertToPlatform(formData: FormData) {
  const by = await rep();
  const lead = must(String(formData.get('leadId')));
  const conv = getConversion(lead.id);
  const pay = getLeadPayments(lead.id).find((p) => p.status === 'paid');
  if (!conv || conv.status !== 'waiting' || !pay) return;
  const p = getPackage(pay.packageId)!;
  const now = nowStamp();

  // parent
  const [pFirst, ...pRest] = lead.parentName.split(' ');
  const parentId = lead.parentId ?? personId('parent', pFirst!, pRest.join(' ') || 'Parent');
  const learnerIds = lead.learnerIds?.length ? lead.learnerIds : (() => {
    const [f, ...r] = lead.studentName.split(' ');
    let id = makeLearnerId(f!, r.join(' ') || 'Student');
    if (getStudent(id)) id = `${id}_${lead.id.slice(5)}`;
    return [id];
  })();

  const counsellor = getAdult(conv.counsellorId);
  if (counsellor) putRecord('adults', { ...counsellor, learnerIds: [...new Set([...counsellor.learnerIds, ...learnerIds])] } satisfies Adult);

  const existingParent = getAdult(parentId);
  putRecord('adults', {
    ...(existingParent ?? { id: parentId, role: 'parent', firstName: pFirst!, lastName: pRest.join(' '), name: lead.parentName, city: lead.city, email: lead.email, phone: lead.phone, learnerIds: [] }),
    learnerIds: [...new Set([...(existingParent?.learnerIds ?? []), ...learnerIds])],
    relation: { ...(existingParent?.relation ?? {}), ...Object.fromEntries(learnerIds.map((id) => [id, 'mother' as const])) },
  } satisfies Adult);

  let subscriptionId = '';
  let invoiceId = '';
  for (const id of learnerIds) {
    const existing = getStudent(id);
    const [first, ...rest] = lead.studentName.split(' ');
    const student: Student = {
      ...(existing ?? {
        id, role: 'student', firstName: first!, lastName: rest.join(' '), name: lead.studentName, board: lead.board, grade: lead.grade,
        stream: lead.grade >= 11 ? 'science' : 'none', programme: `${lead.board === 'cbse' ? 'CBSE' : lead.board === 'ib' ? 'IB' : 'Cambridge'} Class ${lead.grade}`,
        school: '', band: 'average', subjects: [], availability: [], weeklyHours: 6, tzOffsetMinutes: 330, joinedUtc: now,
        mentorIds: [], tutorIds: [], sectionIds: [], profileCompletionPct: 10,
      }),
      city: existing?.city || lead.city,
      plan: p.planId,
      parentIds: [...new Set([...(existing?.parentIds ?? []), parentId])],
      counsellorIds: [...new Set([...(existing?.counsellorIds ?? []), conv.counsellorId])],
      joinedUtc: existing?.joinedUtc ?? now,
    } as Student;
    putRecord('student', student);

    const sub: Subscription = {
      id: `sub_${id.slice(4)}`, learnerId: id, parentId, planId: p.planId, packageId: p.id, startUtc: now,
      endUtc: p.months ? new Date(Date.parse(now) + p.months * 30 * 86_400_000).toISOString() : undefined, status: 'active', leadId: lead.id,
    };
    crmPut('crm_subscriptions', sub);
    subscriptionId = sub.id;

    const inv: Invoice = {
      id: `inv_crm_${lead.id.slice(5)}_${id.slice(4)}`, learnerId: id, payerId: parentId, issuedUtc: pay.paidUtc ?? now, dueDate: (pay.paidUtc ?? now).slice(0, 10),
      status: 'paid', paidUtc: pay.paidUtc ?? now,
      lines: [{ title: `${p.name} (${pay.invoiceNo})`, amountInr: pay.amountInr, planId: p.planId }, { title: 'GST 18%', amountInr: pay.gstInr }],
      amountInr: pay.totalInr,
    };
    putRecord('invoices', inv);
    invoiceId = inv.id;

    appendEvent(id, {
      sourceMethod: 'M2', type: 'crm_handoff',
      payload: { leadId: lead.id, source: lead.source, campaign: lead.campaign, interest: lead.interest, packageId: p.id, planId: p.planId, subscriptionId: sub.id, counsellorId: conv.counsellorId, salesRepId: lead.ownerId, paymentId: pay.id },
    });
  }

  crmPut('crm_conversions', { ...conv, status: 'handed_over', handedOverUtc: now, learnerIds, parentId, subscriptionId, invoiceId });
  saveLead({ ...lead, learnerIds, parentId });
  const after = setStage(must(lead.id), 'converted', by, `${PLAN_NAME[p.planId]} plan started; counsellor ${counsellor?.name ?? conv.counsellorId} assigned.`);
  log(after, { type: 'handoff', byId: by, title: 'Converted to platform', body: `Learner ${learnerIds.join(', ')} ${lead.learnerIds?.length ? 'activated' : 'created'}; parent ${parentId}; subscription ${subscriptionId}; invoice ${invoiceId}.` });
  const t = getTemplate('tpl_welcome_platform')!;
  log(after, { type: 'whatsapp', byId: 'system', title: `WhatsApp: ${t.name}`, body: renderTemplate(t, after), templateId: t.id, auto: true });
  refresh(lead.id);
}

/** "Open in platform": sign in as the handed-over student; new students land on onboarding. */
export async function openInPlatform(formData: FormData) {
  await rep();
  const id = String(formData.get('learnerId'));
  const s = getStudent(id);
  const jar = await cookies();
  jar.set(SESSION_COOKIE, id, { path: '/', httpOnly: true, sameSite: 'lax', maxAge: 60 * 60 * 24 * 30 });
  redirect(s?.onboardedUtc ? '/student' : '/onboarding/about');
}

/** Form version of moveLead (e.g. "Move to negotiation" on the lead page). */
export async function moveStageForm(formData: FormData) {
  await moveLead(String(formData.get('leadId')), String(formData.get('to')) as LeadStatus);
}
