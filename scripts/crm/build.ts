/**
 * W3-CRM demo data: ~180 generic leads over the 90 days before DEMO_NOW plus one lead per persona family
 * (12 Closed won before their platform history starts, Zoya's family at Proposal sent with payment pending).
 * Every stage change, call, template message, demo, payment and hand-off is an activity; follow-ups come
 * from the rules in RULES. Deterministic: seed "learnibility-2026".
 *
 *   npx tsx scripts/crm/build.ts            writes data/crm/*.json (packages.json is hand-written and read here)
 */
import fs from 'node:fs';
import path from 'node:path';
import type {
  Activity, Conversion, CrmPackage, FollowUp, FollowUpRule, Lead, LeadInterest, LeadSource, LeadStatus, Payment, Subscription, TeamMember, Template,
} from '@/components/crm/types';
import { GST_RATE, LOST_REASONS } from '@/components/crm/types';
import type { Board, Grade } from '@/lib/types';

const OUT = path.join(process.cwd(), 'data', 'crm');
const GEN = 'scripts/crm/build.ts';
const NOW = Date.parse('2026-11-18T03:30:00.000Z'); // DEMO_NOW, 09:00 IST
const H = 3_600_000;
const D = 24 * H;
const IST = 5.5 * H;

// ------------------------------------------------------------------ seeded random (same generator as scripts/fixtures/build.ts)
function hashSeed(s: string): number {
  let h = 1779033703 ^ s.length;
  for (let i = 0; i < s.length; i++) (h = Math.imul(h ^ s.charCodeAt(i), 3432918353)), (h = (h << 13) | (h >>> 19));
  return h >>> 0;
}
function rng(seed: string) {
  let a = hashSeed(seed);
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const R = rng('learnibility-2026:crm');
const pick = <T,>(xs: readonly T[]) => xs[Math.floor(R() * xs.length)]!;
const between = (a: number, b: number) => a + R() * (b - a);
const chance = (p: number) => R() < p;
const iso = (ms: number) => new Date(ms).toISOString();
const ist = (date: string, hhmm: string) => Date.parse(`${date}T${hhmm}:00+05:30`);

/** Move a timestamp into working hours (10:00 to 19:30 IST) on the same IST day, or the next day. */
function workHours(ms: number): number {
  const local = ms + IST;
  const day = Math.floor(local / D) * D;
  let hour = (local - day) / H;
  if (hour < 10) hour = 10 + R() * 2;
  if (hour > 19.5) return workHours(day + D + 10 * H - IST + R() * 3 * H);
  return day + hour * H - IST;
}

function write(name: string, items: unknown[]) {
  fs.mkdirSync(OUT, { recursive: true });
  fs.writeFileSync(path.join(OUT, `${name}.json`), JSON.stringify({ schemaVersion: 1, generatedBy: GEN, items }, null, 1) + '\n');
}

// ------------------------------------------------------------------ config
const PACKAGES = (JSON.parse(fs.readFileSync(path.join(OUT, 'packages.json'), 'utf8')) as { items: CrmPackage[] }).items;
const pkg = (id: string) => PACKAGES.find((p) => p.id === id)!;

const TEAM: TeamMember[] = [
  { id: 'sal_priya_malhotra', personaId: 'sal_priya_malhotra', name: 'Priya Malhotra', title: 'Sales manager', manager: true, monthlyTargetInr: 150000 },
  { id: 'sal_aman_gupta', personaId: 'sal_aman_gupta', name: 'Aman Gupta', title: 'Counselling sales rep', monthlyTargetInr: 120000 },
  { id: 'sal_neha_joseph', personaId: 'sal_neha_joseph', name: 'Neha Joseph', title: 'Counselling sales rep', monthlyTargetInr: 120000 },
  { id: 'sal_rhea_bansal', name: 'Rhea Bansal', title: 'Counselling sales rep (study abroad)', monthlyTargetInr: 100000 },
  { id: 'sal_karan_mehta', name: 'Karan Mehta', title: 'Inside sales associate', monthlyTargetInr: 60000 },
];
const OWNER_WEIGHTS: [string, number][] = [['sal_aman_gupta', 0.34], ['sal_neha_joseph', 0.34], ['sal_rhea_bansal', 0.17], ['sal_karan_mehta', 0.1], ['sal_priya_malhotra', 0.05]];
function pickOwner(interest: LeadInterest): string {
  if (interest === 'study_abroad' && chance(0.45)) return 'sal_rhea_bansal';
  let x = R();
  for (const [id, w] of OWNER_WEIGHTS) if ((x -= w) <= 0) return id;
  return 'sal_aman_gupta';
}

const TEMPLATES: Template[] = [
  { id: 'tpl_welcome', name: 'Welcome', channel: 'whatsapp', body: 'Hi {parent}, thanks for your interest in Learnibility for {student}. I am {rep}, your counsellor. When is a good time for a 10-minute call?' },
  { id: 'tpl_nudge', name: 'No-reply nudge', channel: 'whatsapp', body: 'Hi {parent}, just checking in. Would you like a free diagnostic for {student} this week? Reply YES and I will set it up.' },
  { id: 'tpl_demo_booked', name: 'Demo confirmation', channel: 'whatsapp', body: 'Your Learnibility demo for {student} is confirmed for {demo}. You will get the joining link an hour before.' },
  { id: 'tpl_demo_reminder', name: 'Demo reminder', channel: 'whatsapp', body: 'Reminder: {student}’s Learnibility demo is at {demo}. Join here: learnibility.demo/meet/{lead}' },
  { id: 'tpl_reschedule', name: 'Missed demo, reschedule', channel: 'whatsapp', body: 'We missed you today, {parent}. Pick a new slot for {student}’s demo: learnibility.demo/book/{lead}' },
  { id: 'tpl_proposal', name: 'Proposal', channel: 'email', body: 'Dear {parent}, as discussed, here is the plan for {student}: {package} at {price} plus GST. The proposal is valid for 7 days.' },
  { id: 'tpl_payment_link', name: 'Payment link', channel: 'whatsapp', body: 'Here is the secure payment link for {package} ({total} incl. GST): {link}' },
  { id: 'tpl_payment_received', name: 'Payment received', channel: 'whatsapp', body: 'Payment of {total} received, thank you! Invoice {invoice} is on its way. {student}’s Learnibility account is being set up.' },
  { id: 'tpl_nurture', name: 'Monthly nurture', channel: 'whatsapp', body: 'Hi {parent}, this month at Learnibility: free board-exam strategy webinar on Saturday. Want a seat for {student}?' },
  { id: 'tpl_welcome_platform', name: 'Welcome to the platform', channel: 'whatsapp', body: 'Welcome aboard! {student} can sign in at learnibility.demo with this mobile number. First step: the 30-minute starting test.' },
];

const RULES: FollowUpRule[] = [
  { id: 'r_welcome', name: 'Instant welcome', trigger: 'New lead created', action: 'Send the Welcome template within 2 minutes', channel: 'whatsapp' },
  { id: 'r_no_reply_48h', name: 'No reply in 48 hours', trigger: 'Lead is New or Contacted and has not replied for 48 hours', action: 'Send a WhatsApp nudge', channel: 'whatsapp' },
  { id: 'r_demo_24h', name: 'Demo reminder, 24 hours', trigger: 'Demo booked', action: 'WhatsApp reminder 24 hours before the demo', channel: 'whatsapp' },
  { id: 'r_demo_1h', name: 'Demo reminder, 1 hour', trigger: 'Demo booked', action: 'WhatsApp reminder with the joining link 1 hour before', channel: 'whatsapp' },
  { id: 'r_no_show', name: 'Demo no-show', trigger: 'Demo time passed without the family joining', action: 'Send the reschedule message', channel: 'whatsapp' },
  { id: 'r_proposal_3d', name: 'Proposal unpaid for 3 days', trigger: 'Proposal sent, no payment after 3 days', action: 'Create a call task for the owner', channel: 'call' },
  { id: 'r_nurture_30d', name: 'Nurture drip', trigger: 'Closed lost or Nurture', action: 'Send the monthly nurture message every 30 days', channel: 'whatsapp' },
  { id: 'r_manual', name: 'Rep task', trigger: 'Set by the rep', action: 'Next step the rep scheduled', channel: 'call' },
];

// ------------------------------------------------------------------ name pools
const FIRST_KIDS = ['Aditya', 'Advait', 'Anika', 'Arnav', 'Avni', 'Dev', 'Diya', 'Eshan', 'Gauri', 'Ira', 'Ishaan', 'Jiya', 'Kavya', 'Krish', 'Lavanya', 'Manav', 'Myra', 'Navya', 'Neel', 'Nisha', 'Om', 'Pari', 'Pranav', 'Riya', 'Reyansh', 'Saanvi', 'Samar', 'Shaurya', 'Siya', 'Tanvi', 'Ved', 'Vivaan', 'Yash', 'Zara', 'Aryan', 'Kiara', 'Rudra', 'Anvi', 'Kabir', 'Aadhya', 'Harsh', 'Mihika', 'Rehan', 'Sneha', 'Tanish', 'Ahaan', 'Nitya', 'Rishi', 'Trisha', 'Yuvraj'];
const FIRST_PARENTS = ['Rajesh', 'Sunita', 'Amit', 'Pooja', 'Vikram', 'Kavita', 'Sanjay', 'Rekha', 'Manoj', 'Shalini', 'Arvind', 'Meenal', 'Deepak', 'Anjali', 'Suresh', 'Ritu', 'Nitin', 'Swati', 'Ashok', 'Geeta', 'Rahul', 'Preeti', 'Vivek', 'Smita', 'Harish', 'Nandini', 'Gaurav', 'Sapna', 'Kiran', 'Bhavna'];
const LAST = ['Agarwal', 'Bhatia', 'Chopra', 'Desai', 'Ghosh', 'Gupta', 'Iyer', 'Jain', 'Kulkarni', 'Mehta', 'Mishra', 'Nair', 'Pandey', 'Patel', 'Pillai', 'Rao', 'Reddy', 'Saxena', 'Sen', 'Shah', 'Sharma', 'Sinha', 'Srinivasan', 'Tiwari', 'Trivedi', 'Varghese', 'Verma', 'Yadav', 'Bose', 'Malik', 'Chatterjee', 'Kaur', 'Menon', 'Naidu', 'Dutta'];
const CITIES = ['New Delhi', 'Mumbai', 'Bengaluru', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 'Gurugram', 'Noida', 'Ahmedabad', 'Jaipur', 'Kochi', 'Lucknow', 'Chandigarh', 'Indore'];
const CAMPAIGNS: Record<LeadSource, string[]> = {
  website: ['Organic · Free diagnostic', 'Organic · Pricing page', 'Organic · Blog: board exam plan'],
  google_ads: ['Search · Board exam tutoring', 'Search · Study abroad counselling', 'Search · IB DP support'],
  instagram: ['Reels · Class 10 boards', 'Stories · IB and IGCSE help', 'Reels · Career clarity'],
  facebook: ['Lead form · Parents 35-50', 'Lead form · Class 11 stream choice'],
  youtube: ['Pre-roll · Career clarity', 'Pre-roll · JEE and NEET planning'],
  referral: ['Parent referral programme', 'Student referral: 1 month free'],
  school_partnership: ['DPS parent evening', 'Oakridge careers fair', 'KV Salt Lake workshop'],
  webinar: ['Webinar · Studying in the UK (Oct)', 'Webinar · Beat exam anxiety (Nov)', 'Webinar · Choosing a stream after Class 10'],
};
const SOURCE_WEIGHTS: [LeadSource, number][] = [['website', 0.2], ['google_ads', 0.2], ['instagram', 0.15], ['facebook', 0.1], ['youtube', 0.06], ['referral', 0.12], ['school_partnership', 0.08], ['webinar', 0.09]];
const SOURCE_SCORE: Record<LeadSource, number> = { referral: 68, school_partnership: 60, webinar: 57, website: 54, google_ads: 50, instagram: 42, youtube: 40, facebook: 38 };
const STAGE_SCORE: Partial<Record<LeadStatus, number>> = { contacted: 5, qualified: 12, demo_booked: 18, demo_done: 24, proposal_sent: 30, negotiation: 32, closed_won: 40, converted: 40 };

function pickSource(): LeadSource {
  let x = R();
  for (const [s, w] of SOURCE_WEIGHTS) if ((x -= w) <= 0) return s;
  return 'website';
}

// ------------------------------------------------------------------ outputs
const leads: Lead[] = [];
const activities: Activity[] = [];
const followups: FollowUp[] = [];
const payments: Payment[] = [];
const conversions: Conversion[] = [];
const subscriptions: Subscription[] = [];
let actSeq = 0;
let fuSeq = 0;
let invoiceSeq = 0;
let receiptSeq = 0;

function act(lead: Lead, a: Omit<Activity, 'id' | 'leadId'>) {
  if (Date.parse(a.atUtc) > NOW) return;
  actSeq += 1;
  activities.push({ id: `act_${String(actSeq).padStart(5, '0')}`, leadId: lead.id, ...a });
  if (['call', 'whatsapp', 'email', 'demo'].includes(a.type) && !a.auto) lead.lastContactedUtc = a.atUtc;
}
function stage(lead: Lead, to: LeadStatus, at: number, by = lead.ownerId, body?: string) {
  act(lead, { type: 'stage', atUtc: iso(at), byId: by, title: `Stage: ${label(lead.status)} → ${label(to)}`, from: lead.status, to, body });
  lead.status = to;
  lead.stageChangedUtc = iso(at);
}
const label = (s: LeadStatus) => s.replace(/_/g, ' ').replace(/^./, (c) => c.toUpperCase());
function msg(lead: Lead, templateId: string, at: number, opts: { auto?: boolean; ruleId?: string; by?: string } = {}) {
  const t = TEMPLATES.find((x) => x.id === templateId)!;
  act(lead, { type: t.channel, atUtc: iso(at), byId: opts.by ?? (opts.auto ? 'system' : lead.ownerId), title: `${t.channel === 'email' ? 'Email' : 'WhatsApp'}: ${t.name}`, templateId, ruleId: opts.ruleId, auto: opts.auto });
}
function followUp(lead: Lead, ruleId: string, title: string, due: number, done?: number) {
  fuSeq += 1;
  const rule = RULES.find((r) => r.id === ruleId)!;
  const isDone = done !== undefined && done <= NOW;
  followups.push({
    id: `fu_${String(fuSeq).padStart(5, '0')}`, leadId: lead.id, ruleId, channel: rule.channel, title, dueUtc: iso(due),
    status: isDone ? 'done' : 'open', doneUtc: isDone ? iso(done!) : undefined, ownerId: lead.ownerId,
  });
}
function call(lead: Lead, at: number, outcome: Activity['outcome'], body?: string) {
  const dur = outcome === 'connected' ? Math.round(between(4, 16)) : 0;
  act(lead, { type: 'call', atUtc: iso(at), byId: lead.ownerId, title: outcome === 'connected' ? `Call, ${dur} min` : `Call: ${outcome!.replace('_', ' ')}`, outcome, durationMin: dur || undefined, body });
}

function packageFor(interest: LeadInterest, grade: Grade): CrmPackage {
  const options = PACKAGES.filter((p) => p.interests.includes(interest) && p.id !== 'pkg_apps_monthly');
  if (interest === 'study_abroad' && grade < 11) return pkg('pkg_career');
  return pick(options);
}

function createPayment(lead: Lead, p: CrmPackage, at: number): Payment {
  const gst = Math.round(p.priceInr * GST_RATE);
  const pay: Payment = {
    id: `pay_${lead.id.slice(5)}_${payments.filter((x) => x.leadId === lead.id).length + 1}`, leadId: lead.id, packageId: p.id,
    amountInr: p.priceInr, gstInr: gst, totalInr: p.priceInr + gst, link: `https://pay.learnibility.demo/l/${lead.id.slice(5)}${Math.floor(R() * 9000 + 1000)}`,
    status: 'pending', createdUtc: iso(at),
  };
  payments.push(pay);
  return pay;
}
function markPaid(lead: Lead, pay: Payment, at: number) {
  invoiceSeq += 1;
  receiptSeq += 1;
  pay.status = 'paid';
  pay.paidUtc = iso(at);
  pay.method = pick(['UPI', 'UPI', 'Card', 'Net banking'] as const);
  const fy = new Date(at).getUTCMonth() >= 3 ? new Date(at).getUTCFullYear() : new Date(at).getUTCFullYear() - 1;
  pay.invoiceNo = `LRN/${fy}-${String((fy + 1) % 100).padStart(2, '0')}/${String(invoiceSeq).padStart(4, '0')}`;
  pay.receiptNo = `RCPT-${String(10230 + receiptSeq)}`;
  act(lead, { type: 'payment', atUtc: iso(at), byId: 'system', title: `Payment received: ₹${pay.totalInr.toLocaleString('en-IN')} by ${pay.method}`, body: `Invoice ${pay.invoiceNo}, receipt ${pay.receiptNo}.`, auto: true });
  msg(lead, 'tpl_payment_received', at + 3 * 60_000, { auto: true });
}

const COUNSELLOR_FOR = (interest: LeadInterest) => (interest === 'study_abroad' ? 'csl_farah_siddiqui' : 'csl_heena_qureshi');

function won(lead: Lead, at: number, opts: { learnerIds?: string[]; handover?: number } = {}) {
  stage(lead, 'closed_won', at);
  const p = pkg(lead.packageId!);
  // Recent generic wins wait on the Conversions screen so the demo has hand-overs to run.
  const recentWait = opts.handover === undefined && NOW - at < 12 * D && conversions.filter((c) => c.status === 'waiting').length < 4;
  const handover = recentWait ? undefined : opts.handover ?? at + between(0.5, 3) * D;
  const conv: Conversion = {
    id: `conv_${lead.id.slice(5)}`, leadId: lead.id, status: 'waiting', wonUtc: iso(at), learnerIds: opts.learnerIds ?? [],
    parentId: lead.parentId, counsellorId: COUNSELLOR_FOR(lead.interest), planId: p.planId,
  };
  if (handover !== undefined && handover <= NOW) {
    conv.status = 'handed_over';
    conv.handedOverUtc = iso(handover);
    act(lead, { type: 'handoff', atUtc: iso(handover), byId: lead.ownerId, title: 'Converted to platform', body: `Learner account created, counsellor ${conv.counsellorId === 'csl_farah_siddiqui' ? 'Farah Siddiqui' : 'Heena Qureshi'} assigned, ${p.name} started.` });
    msg(lead, 'tpl_welcome_platform', handover + 5 * 60_000, { auto: true });
    lead.status = 'converted';
    lead.stageChangedUtc = iso(handover);
    for (const learnerId of conv.learnerIds) {
      const sub: Subscription = {
        id: `sub_${learnerId.slice(4)}`, learnerId, parentId: lead.parentId, planId: p.planId, packageId: p.id, startUtc: iso(handover),
        endUtc: p.months ? iso(handover + p.months * 30 * D) : undefined, status: 'active', leadId: lead.id,
      };
      subscriptions.push(sub);
      conv.subscriptionId = sub.id;
    }
  }
  conversions.push(conv);
}

function lost(lead: Lead, at: number, reason: string, toNurture = false) {
  lead.lostReason = reason;
  stage(lead, toNurture ? 'nurture' : 'closed_lost', at, lead.ownerId, `Reason: ${reason}`);
  lead.score = Math.min(lead.score, toNurture ? Math.round(between(30, 45)) : Math.round(between(8, 30)));
  // monthly drip
  let t = at + 30 * D;
  while (t <= NOW) {
    const send = workHours(t);
    msg(lead, 'tpl_nurture', send, { auto: true, ruleId: 'r_nurture_30d' });
    followUp(lead, 'r_nurture_30d', 'Monthly nurture message', t, send);
    t += 30 * D;
  }
  followUp(lead, 'r_nurture_30d', 'Monthly nurture message', t);
}

/**
 * Walks one lead through the funnel. `force` makes every step succeed (persona families) and `stopAt` ends at a stage.
 * Returns early when the next step would land after DEMO_NOW, leaving the lead at its current stage.
 */
function simulate(lead: Lead, t0: number, opts: { force?: boolean; stopAt?: LeadStatus; learnerIds?: string[]; handoverBefore?: number } = {}) {
  const f = opts.force;
  const ok = (p: number) => f || chance(p);
  /** Some open leads simply stall at a stage; the rep's next task then sits around today (some overdue). */
  const stalls = (title: string) => {
    if (f || !chance(0.13)) return false;
    followUp(lead, 'r_manual', title, workHours(NOW + between(-4, 2.5) * D));
    return true;
  };
  act(lead, { type: 'stage', atUtc: iso(t0), byId: 'system', title: `Lead captured from ${lead.source.replace(/_/g, ' ')}`, body: `Campaign: ${lead.campaign}`, to: 'new', auto: true });
  msg(lead, 'tpl_welcome', t0 + 2 * 60_000, { auto: true, ruleId: 'r_welcome' });

  // first contact
  let t = workHours(t0 + between(0.1, 1.2) * D);
  if (t > NOW) return followUp(lead, 'r_manual', 'First call', t);
  if (!f && chance(0.3)) {
    call(lead, t, pick(['no_answer', 'busy'] as const));
    const nudge = workHours(t0 + 48 * H);
    if (nudge > NOW) return followUp(lead, 'r_no_reply_48h', 'No reply: send WhatsApp nudge', t0 + 48 * H);
    msg(lead, 'tpl_nudge', nudge, { auto: true, ruleId: 'r_no_reply_48h' });
    followUp(lead, 'r_no_reply_48h', 'No reply: send WhatsApp nudge', t0 + 48 * H, nudge);
    if (chance(0.25)) {
      const lt = workHours(nudge + between(3, 8) * D);
      if (lt > NOW) return followUp(lead, 'r_manual', 'Final call attempt', lt);
      call(lead, lt - 2 * H, 'no_answer');
      return lost(lead, lt, 'No response after 5 attempts');
    }
    t = workHours(nudge + between(0.2, 1.5) * D);
    if (t > NOW) return followUp(lead, 'r_manual', 'Call back after nudge', t);
  }
  call(lead, t, 'connected', pick(['Parent keen, wants to understand how the plan adapts.', 'Student struggling in Maths since last term.', 'Asked about counsellor support and timings.', 'Comparing with two coaching centres.', 'Wants clarity on boards prep and mocks.']));
  stage(lead, 'contacted', t + 15 * 60_000);
  if (stalls('Qualification call')) return;

  // qualify
  t = workHours(t + between(0.4, 3) * D);
  if (t > NOW) return followUp(lead, 'r_manual', 'Qualification call', t);
  if (!ok(0.8)) return lost(lead, t, chance(0.6) ? 'Not the right time' : 'Wanted offline classes only', chance(0.6));
  call(lead, t, 'connected', `Needs: ${lead.interest.replace(/_/g, ' ')}. Budget discussed. Decision maker: ${lead.parentName.split(' ')[0]}.`);
  stage(lead, 'qualified', t + 20 * 60_000);
  if (opts.stopAt === 'qualified' || stalls('Offer a demo slot')) return;

  // book demo
  t = workHours(t + between(0.2, 2) * D);
  if (t > NOW) return followUp(lead, 'r_manual', 'Book the demo', t);
  if (!ok(0.82)) return lost(lead, t, pick(LOST_REASONS), chance(0.4));
  let demo = Math.floor((t + IST) / D) * D + Math.round(between(1, 4)) * D + pick([16, 17, 18, 19]) * H - IST;
  lead.demoUtc = iso(demo);
  stage(lead, 'demo_booked', t);
  msg(lead, 'tpl_demo_booked', t + 5 * 60_000);
  const reminders = () => {
    for (const [rule, before, title] of [['r_demo_24h', 24 * H, 'Demo reminder (24 h)'], ['r_demo_1h', H, 'Demo reminder (1 h)']] as const) {
      const at = demo - before;
      if (at <= NOW) msg(lead, 'tpl_demo_reminder', at, { auto: true, ruleId: rule });
      followUp(lead, rule, title, at, at);
    }
  };
  reminders();
  if (demo > NOW) return;
  if (!f && chance(0.15)) {
    msg(lead, 'tpl_reschedule', demo + H, { auto: true, ruleId: 'r_no_show' });
    followUp(lead, 'r_no_show', 'Demo missed: reschedule', demo + H, demo + H);
    act(lead, { type: 'note', atUtc: iso(demo + 1.2 * H), byId: lead.ownerId, title: 'Demo no-show', body: 'Family did not join. Reschedule link sent.' });
    demo = demo + Math.round(between(2, 4)) * D;
    lead.demoUtc = iso(demo);
    reminders();
    if (demo > NOW) return;
  }
  act(lead, { type: 'demo', atUtc: iso(demo), byId: lead.ownerId, title: `Demo session, ${Math.round(between(32, 50))} min`, body: pick(['Walked through the diagnostic, gap report and weekly timetable. Student tried 6 questions.', 'Showed parent dashboard and spend view; student liked the timetable re-plan.', 'Covered tutor matching and counsellor check-ins. Parent asked about mocks.']) });
  stage(lead, 'demo_done', demo + H);
  if (opts.stopAt === 'demo_done' || stalls('Send the proposal')) return;

  // proposal
  t = workHours(demo + between(0.2, 1.8) * D);
  if (t > NOW) return followUp(lead, 'r_manual', 'Send the proposal', t);
  if (!ok(0.8)) return lost(lead, t, pick(['Student not interested', 'Price too high', 'Chose another provider']));
  const p = lead.packageId ? pkg(lead.packageId) : packageFor(lead.interest, lead.grade);
  lead.packageId = p.id;
  lead.valueInr = p.priceInr;
  stage(lead, 'proposal_sent', t);
  msg(lead, 'tpl_proposal', t + 2 * 60_000);
  const pay = createPayment(lead, p, t + 4 * 60_000);
  msg(lead, 'tpl_payment_link', t + 5 * 60_000);
  const proposalAt = t;
  if (opts.stopAt === 'proposal_sent') return pay;

  // negotiation?
  let closeAt = workHours(t + between(1, 6) * D);
  if (!f ? chance(0.35) : chance(0.3)) {
    const nt = workHours(t + between(0.8, 2.5) * D);
    if (nt > NOW) return followUp(lead, 'r_proposal_3d', 'Proposal unpaid: call', proposalAt + 3 * D);
    call(lead, nt, 'connected', pick(['Asked for a sibling discount.', 'Wants to pay in two instalments.', 'Comparing with another platform’s price.']));
    stage(lead, 'negotiation', nt + 10 * 60_000);
    closeAt = workHours(nt + between(1, 5) * D);
  }
  if (proposalAt + 3 * D < Math.min(closeAt, NOW)) {
    const ct = workHours(proposalAt + 3 * D);
    call(lead, ct, chance(0.7) ? 'connected' : 'call_back', 'Follow-up on the proposal.');
    followUp(lead, 'r_proposal_3d', 'Proposal unpaid: call', proposalAt + 3 * D, ct);
  }
  if (closeAt > NOW) {
    if (proposalAt + 3 * D >= NOW) followUp(lead, 'r_proposal_3d', 'Proposal unpaid: call', proposalAt + 3 * D);
    else followUp(lead, 'r_manual', 'Chase payment', workHours(NOW + between(-1.5, 1.5) * D));
    return;
  }
  if (!ok(0.62)) {
    lost(lead, closeAt, pick(['Price too high', 'Chose another provider', 'Not the right time']), chance(0.3));
    return;
  }
  if (!f && chance(0.12)) {
    pay.status = 'failed';
    pay.failedUtc = iso(closeAt - 3 * H);
    act(lead, { type: 'payment', atUtc: iso(closeAt - 3 * H), byId: 'system', title: 'Payment failed (UPI timeout)', auto: true });
    const retry = createPayment(lead, p, closeAt - 2.5 * H);
    msg(lead, 'tpl_payment_link', closeAt - 2.5 * H);
    markPaid(lead, retry, closeAt);
  } else markPaid(lead, pay, closeAt);
  won(lead, closeAt + 10 * 60_000, { learnerIds: opts.learnerIds, handover: opts.handoverBefore });
  if (opts.handoverBefore !== undefined && Date.parse(conversions.at(-1)!.wonUtc) >= opts.handoverBefore) throw new Error(`${lead.id} won after history start`);
}

function baseLead(i: number, o: Partial<Lead> & Pick<Lead, 'studentName' | 'parentName' | 'grade' | 'board' | 'interest' | 'source' | 'city'>): Lead {
  const campaign = o.campaign ?? pick(CAMPAIGNS[o.source]);
  const [pf, ...pl] = o.parentName.split(' ');
  return {
    id: `lead_${String(i).padStart(4, '0')}`,
    phone: o.phone ?? `+91 90000 ${String(i).padStart(5, '0')}`,
    email: `${pf!.toLowerCase()}.${pl.join('').toLowerCase()}@example.com`,
    campaign,
    ownerId: o.ownerId ?? pickOwner(o.interest),
    score: 0,
    status: 'new',
    valueInr: 0,
    createdUtc: '',
    stageChangedUtc: '',
    ...o,
  } as Lead;
}

function finishScore(lead: Lead) {
  if (lead.status === 'closed_lost' || lead.status === 'nurture') return;
  lead.score = Math.max(5, Math.min(98, Math.round(SOURCE_SCORE[lead.source] + (STAGE_SCORE[lead.status] ?? 0) + between(-8, 8))));
}
function expectedValue(lead: Lead) {
  if (!lead.valueInr) lead.valueInr = packageFor(lead.interest, lead.grade).priceInr;
}

// ------------------------------------------------------------------ persona families
interface Family { learnerIds: string[]; student: string; parent: string; parentId?: string; grade: Grade; board: Board; city: string; interest: LeadInterest; source: LeadSource; campaign: string; owner: string; packageId: string; historyStart: string; phone: string; notes?: string }
const CBSE_START = '2026-04-06';
const INTL_START = '2026-08-17';
const FAMILIES: Family[] = [
  { learnerIds: ['lrn_aarav_kapoor', 'lrn_ananya_kapoor'], student: 'Aarav and Ananya Kapoor', parent: 'Neha Kapoor', parentId: 'par_neha_kapoor', grade: 8, board: 'cbse', city: 'Gurugram', interest: 'full_package', source: 'referral', campaign: 'Parent referral programme', owner: 'sal_neha_joseph', packageId: 'pkg_starter', historyStart: CBSE_START, phone: '+91 90000 10001', notes: 'Two children: Aarav (Class 8 CBSE) and Ananya (Class 10 IGCSE). One parent account.' },
  { learnerIds: ['lrn_ishita_rao'], student: 'Ishita Rao', parent: 'Sunita Rao', parentId: 'par_sunita_rao', grade: 8, board: 'cambridge', city: 'Bengaluru', interest: 'academic_support', source: 'instagram', campaign: 'Stories · IB and IGCSE help', owner: 'sal_aman_gupta', packageId: 'pkg_starter', historyStart: INTL_START, phone: '+91 98110 00002' },
  { learnerIds: ['lrn_kabir_singh'], student: 'Kabir Singh', parent: 'Harpreet Singh', parentId: 'par_harpreet_singh', grade: 9, board: 'cbse', city: 'New Delhi', interest: 'academic_support', source: 'school_partnership', campaign: 'DPS parent evening', owner: 'sal_aman_gupta', packageId: 'pkg_starter', historyStart: CBSE_START, phone: '+91 98110 00001' },
  { learnerIds: ['lrn_meera_iyer'], student: 'Meera Iyer', parent: 'Radha Iyer', grade: 9, board: 'ib', city: 'Chennai', interest: 'academic_support', source: 'google_ads', campaign: 'Search · IB DP support', owner: 'sal_neha_joseph', packageId: 'pkg_starter', historyStart: INTL_START, phone: '+91 90000 10004' },
  { learnerIds: ['lrn_rohan_das'], student: 'Rohan Das', parent: 'Anita Das', parentId: 'par_anita_das', grade: 10, board: 'cbse', city: 'Kolkata', interest: 'academic_support', source: 'facebook', campaign: 'Lead form · Parents 35-50', owner: 'sal_neha_joseph', packageId: 'pkg_starter', historyStart: CBSE_START, phone: '+91 90000 10005' },
  { learnerIds: ['lrn_vihaan_joshi'], student: 'Vihaan Joshi', parent: 'Sanjay Joshi', grade: 11, board: 'cbse', city: 'Pune', interest: 'academic_support', source: 'youtube', campaign: 'Pre-roll · JEE and NEET planning', owner: 'sal_aman_gupta', packageId: 'pkg_starter', historyStart: CBSE_START, phone: '+91 90000 10006' },
  { learnerIds: ['lrn_sara_khan'], student: 'Sara Khan', parent: 'Farida Khan', parentId: 'par_farida_khan', grade: 11, board: 'cbse', city: 'Mumbai', interest: 'career_counselling', source: 'webinar', campaign: 'Webinar · Choosing a stream after Class 10', owner: 'sal_neha_joseph', packageId: 'pkg_career', historyStart: CBSE_START, phone: '+91 90000 10007' },
  { learnerIds: ['lrn_arjun_nair'], student: 'Arjun Nair', parent: 'Deepa Nair', grade: 11, board: 'ib', city: 'Kochi', interest: 'career_counselling', source: 'website', campaign: 'Organic · Free diagnostic', owner: 'sal_aman_gupta', packageId: 'pkg_career', historyStart: INTL_START, phone: '+91 90000 10008' },
  { learnerIds: ['lrn_diya_sharma'], student: 'Diya Sharma', parent: 'Rajesh Sharma', grade: 12, board: 'cbse', city: 'Jaipur', interest: 'academic_support', source: 'google_ads', campaign: 'Search · Board exam tutoring', owner: 'sal_neha_joseph', packageId: 'pkg_starter', historyStart: CBSE_START, phone: '+91 90000 10009' },
  { learnerIds: ['lrn_nikhil_reddy'], student: 'Nikhil Reddy', parent: 'Lakshmi Reddy', parentId: 'par_lakshmi_reddy', grade: 12, board: 'cambridge', city: 'Hyderabad', interest: 'study_abroad', source: 'webinar', campaign: 'Webinar · Studying in the UK (Jul)', owner: 'sal_rhea_bansal', packageId: 'pkg_apps_monthly', historyStart: INTL_START, phone: '+91 98110 00003' },
  { learnerIds: ['lrn_tara_menon'], student: 'Tara Menon', parent: 'Anil Menon', grade: 12, board: 'ib', city: 'Bengaluru', interest: 'study_abroad', source: 'referral', campaign: 'Student referral: 1 month free', owner: 'sal_rhea_bansal', packageId: 'pkg_apps_monthly', historyStart: INTL_START, phone: '+91 90000 10011' },
  { learnerIds: ['lrn_kunal_verma'], student: 'Kunal Verma', parent: 'Sunil Verma', grade: 12, board: 'cbse', city: 'Lucknow', interest: 'career_counselling', source: 'school_partnership', campaign: 'KV Salt Lake workshop', owner: 'sal_aman_gupta', packageId: 'pkg_career', historyStart: CBSE_START, phone: '+91 90000 10012' },
];

let n = 0;
for (const fam of FAMILIES) {
  n += 1;
  const lead = baseLead(n, {
    studentName: fam.student, parentName: fam.parent, parentId: fam.parentId, grade: fam.grade, board: fam.board, city: fam.city, interest: fam.interest,
    source: fam.source, campaign: fam.campaign, ownerId: fam.owner, phone: fam.phone, packageId: fam.packageId, valueInr: pkg(fam.packageId).priceInr,
    learnerIds: fam.learnerIds, personaFamily: true, notes: fam.notes,
  });
  const start = ist(fam.historyStart, '10:00');
  const t0 = workHours(start - between(34, 42) * D);
  lead.createdUtc = iso(t0);
  simulate(lead, t0, { force: true, learnerIds: fam.learnerIds, handoverBefore: start - between(1, 3) * D });
  if (lead.status !== 'converted') throw new Error(`${lead.id} ${fam.student} ended at ${lead.status}`);
  finishScore(lead);
  leads.push(lead);
}

// Zoya's family: live demo lead at Proposal sent, payment pending today.
{
  n += 1;
  const lead = baseLead(n, {
    studentName: 'Zoya Fernandes', parentName: 'Maria Fernandes', grade: 9, board: 'cbse', city: 'Mumbai', interest: 'full_package', source: 'website',
    campaign: 'Organic · Free diagnostic', ownerId: 'sal_aman_gupta', phone: '+91 98765 43210', packageId: 'pkg_full_3m', valueInr: pkg('pkg_full_3m').priceInr,
    learnerIds: ['lrn_zoya_fernandes'], personaFamily: true,
    notes: 'Moved from Goa in June. Mother wants structure for Class 9 Maths and Science and early career clarity.',
  });
  const t0 = ist('2026-11-12', '11:40');
  lead.createdUtc = iso(t0);
  act(lead, { type: 'stage', atUtc: iso(t0), byId: 'system', title: 'Lead captured from website', body: 'Campaign: Organic · Free diagnostic', to: 'new', auto: true });
  msg(lead, 'tpl_welcome', t0 + 2 * 60_000, { auto: true, ruleId: 'r_welcome' });
  call(lead, ist('2026-11-12', '15:05'), 'connected', 'Maria is keen. Zoya finds Class 9 Maths a big jump from Class 8. Wants weekly visibility as a parent.');
  stage(lead, 'contacted', ist('2026-11-12', '15:20'));
  call(lead, ist('2026-11-13', '12:10'), 'connected', 'Needs: full package (academics plus career clarity). Budget fine for 3 months to start. Decision maker: Maria.');
  stage(lead, 'qualified', ist('2026-11-13', '12:30'));
  lead.demoUtc = iso(ist('2026-11-14', '18:00'));
  stage(lead, 'demo_booked', ist('2026-11-13', '12:35'));
  msg(lead, 'tpl_demo_booked', ist('2026-11-13', '12:40'));
  msg(lead, 'tpl_demo_reminder', ist('2026-11-13', '18:00'), { auto: true, ruleId: 'r_demo_24h' });
  followUp(lead, 'r_demo_24h', 'Demo reminder (24 h)', ist('2026-11-13', '18:00'), ist('2026-11-13', '18:00'));
  msg(lead, 'tpl_demo_reminder', ist('2026-11-14', '17:00'), { auto: true, ruleId: 'r_demo_1h' });
  followUp(lead, 'r_demo_1h', 'Demo reminder (1 h)', ist('2026-11-14', '17:00'), ist('2026-11-14', '17:00'));
  act(lead, { type: 'demo', atUtc: iso(ist('2026-11-14', '18:00')), byId: lead.ownerId, title: 'Demo session, 42 min', body: 'Zoya tried the adaptive starter questions; Maria liked the parent spend view and counsellor check-ins.' });
  stage(lead, 'demo_done', ist('2026-11-14', '18:45'));
  stage(lead, 'proposal_sent', ist('2026-11-15', '18:20'));
  msg(lead, 'tpl_proposal', ist('2026-11-15', '18:22'));
  createPayment(lead, pkg('pkg_full_3m'), ist('2026-11-15', '18:24'));
  msg(lead, 'tpl_payment_link', ist('2026-11-15', '18:25'));
  act(lead, { type: 'note', atUtc: iso(ist('2026-11-17', '16:40')), byId: lead.ownerId, title: 'Note', body: 'Maria replied on WhatsApp: will pay on the 18th after salary credit. Call her at 11.' });
  followUp(lead, 'r_proposal_3d', 'Proposal unpaid: call Maria', ist('2026-11-18', '11:00'));
  finishScore(lead);
  leads.push(lead);
}

// ------------------------------------------------------------------ generic leads
const used = new Set<string>();
for (let i = 0; i < 180; i++) {
  n += 1;
  let kid: string, last: string;
  do {
    kid = pick(FIRST_KIDS);
    last = pick(LAST);
  } while (used.has(kid + last));
  used.add(kid + last);
  const interest = pick(['academic_support', 'academic_support', 'academic_support', 'career_counselling', 'study_abroad', 'full_package'] as const);
  const grade = (interest === 'study_abroad' ? pick([10, 11, 12, 12]) : pick([8, 9, 9, 10, 10, 10, 11, 12])) as Grade;
  const source = pickSource();
  const lead = baseLead(n, {
    studentName: `${kid} ${last}`, parentName: `${pick(FIRST_PARENTS)} ${last}`, grade, board: pick(['cbse', 'cbse', 'cbse', 'cambridge', 'ib'] as const),
    city: pick(CITIES), interest, source,
  });
  // more recent leads than old ones; a few from the last day
  const ageDays = i < 4 ? between(0.05, 0.9) : 90 * Math.pow(R(), 1.5);
  const t0 = NOW - ageDays * D;
  lead.createdUtc = iso(t0);
  simulate(lead, t0, { learnerIds: [] });
  expectedValue(lead);
  finishScore(lead);
  leads.push(lead);
}

// conversions of generic leads keep empty learnerIds until "Convert to platform" runs (it creates the learner).
leads.sort((a, b) => a.createdUtc.localeCompare(b.createdUtc));
activities.sort((a, b) => a.atUtc.localeCompare(b.atUtc) || a.id.localeCompare(b.id));
followups.sort((a, b) => a.dueUtc.localeCompare(b.dueUtc));

write('leads', leads);
write('activities', activities);
write('followups', followups);
write('payments', payments);
write('conversions', conversions);
write('subscriptions', subscriptions);
write('team', TEAM);
write('templates', TEMPLATES);
write('rules', RULES);

const by = (k: (l: Lead) => string) => Object.entries(leads.reduce<Record<string, number>>((m, l) => ((m[k(l)] = (m[k(l)] ?? 0) + 1), m), {}));
console.log(`leads ${leads.length}, activities ${activities.length}, follow-ups ${followups.length}, payments ${payments.length}, conversions ${conversions.length}`);
console.log('by status', by((l) => l.status).map(([k, v]) => `${k} ${v}`).join(', '));
console.log('open by rule', Object.entries(followups.filter((f) => f.status === 'open').reduce<Record<string, number>>((m, f) => ((m[f.ruleId] = (m[f.ruleId] ?? 0) + 1), m), {})));
console.log('open follow-ups', followups.filter((f) => f.status === 'open' && Date.parse(f.dueUtc) < NOW).length, 'overdue,', followups.filter((f) => f.status === 'open' && new Date(Date.parse(f.dueUtc) + IST).toISOString().slice(0, 10) === '2026-11-18').length, 'due today');
console.log('paid this month ₹', payments.filter((p) => p.status === 'paid' && p.paidUtc! >= '2026-10-31T18:30').reduce((s, p) => s + p.amountInr, 0));
