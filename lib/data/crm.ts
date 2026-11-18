/**
 * W3-CRM reads. Base records come from data/crm/*.json (scripts/crm/build.ts); demo writes from lib/actions/crm.ts
 * land in the shared overlay under collections crm_leads, crm_activities, crm_followups, crm_payments,
 * crm_conversions and crm_subscriptions, so "Reset demo" restores the CRM with everything else.
 * Server only. Screens: app/sales/**.
 */
import 'server-only';
import leadsFile from '@/data/crm/leads.json';
import activitiesFile from '@/data/crm/activities.json';
import followupsFile from '@/data/crm/followups.json';
import paymentsFile from '@/data/crm/payments.json';
import conversionsFile from '@/data/crm/conversions.json';
import subscriptionsFile from '@/data/crm/subscriptions.json';
import teamFile from '@/data/crm/team.json';
import packagesFile from '@/data/crm/packages.json';
import templatesFile from '@/data/crm/templates.json';
import rulesFile from '@/data/crm/rules.json';
import { overlay } from '@/lib/store/overlay';
import { DEMO_NOW_ISO } from '@/lib/demo-clock';
import { getAdult, getStudent, listAdults } from '@/lib/data';
import {
  FUNNEL, GST_RATE, SOURCES, type Activity, type Conversion, type CrmPackage, type FollowUp, type FollowUpRule, type Lead, type LeadSource,
  type LeadStatus, type Payment, type Subscription, type TeamMember, type Template,
} from '@/components/crm/types';

export * from '@/components/crm/types';

type Coll = 'crm_leads' | 'crm_activities' | 'crm_followups' | 'crm_payments' | 'crm_conversions' | 'crm_subscriptions';
const BASE: Record<Coll, { items: unknown[] }> = {
  crm_leads: leadsFile, crm_activities: activitiesFile, crm_followups: followupsFile, crm_payments: paymentsFile,
  crm_conversions: conversionsFile, crm_subscriptions: subscriptionsFile,
};

function merged<T extends { id: string }>(name: Coll): T[] {
  const map = new Map<string, T>();
  for (const r of BASE[name].items as T[]) map.set(r.id, r);
  for (const row of overlay().rows(name)) {
    if (row.deleted) map.delete(row.key);
    else map.set(row.key, row.data as T);
  }
  return [...map.values()];
}

/** Upsert a CRM record into the demo overlay (used by lib/actions/crm.ts only). */
export function crmPut<T extends { id: string }>(name: Coll, record: T): T {
  overlay().put(name, record.id, null, record);
  return record;
}

// ------------------------------------------------------------------ config
export const listTeam = (): TeamMember[] => teamFile.items as TeamMember[];
export const getTeamMember = (id: string) => listTeam().find((m) => m.id === id);
export const repName = (id: string) => (id === 'system' ? 'Automation' : getTeamMember(id)?.name ?? id);
export const listPackages = (): CrmPackage[] => packagesFile.items as CrmPackage[];
export const getPackage = (id: string | undefined) => listPackages().find((p) => p.id === id);
export const listTemplates = (): Template[] => templatesFile.items as Template[];
export const getTemplate = (id: string) => listTemplates().find((t) => t.id === id);
export const listRules = (): FollowUpRule[] => rulesFile.items as FollowUpRule[];
export const getRule = (id: string) => listRules().find((r) => r.id === id);
export const gstFor = (amount: number) => Math.round(amount * GST_RATE);

// ------------------------------------------------------------------ records
export const listLeadsRaw = () => merged<Lead>('crm_leads');
export const listActivities = () => merged<Activity>('crm_activities');
export const listFollowUps = () => merged<FollowUp>('crm_followups');
export const listPayments = () => merged<Payment>('crm_payments');
export const listConversions = () => merged<Conversion>('crm_conversions');
export const listSubscriptions = () => merged<Subscription>('crm_subscriptions');

/** The parent's name as the platform knows it (persona families), else the name captured on the lead. */
function displayParent(l: Lead): string {
  if (l.parentId) {
    const a = getAdult(l.parentId);
    if (a) return a.name;
  }
  for (const id of l.learnerIds ?? []) {
    const s = getStudent(id);
    const pid = s?.parentIds?.[0];
    const a = pid ? getAdult(pid) : listAdults('parent').find((p) => p.learnerIds.includes(id));
    if (a) return a.name;
  }
  return l.parentName;
}

export function listLeads(f: { q?: string; status?: string; source?: string; owner?: string; interest?: string } = {}): Lead[] {
  const q = f.q?.trim().toLowerCase();
  return listLeadsRaw()
    .map((l) => ({ ...l, parentName: displayParent(l) }))
    .filter((l) => {
      if (f.status && f.status !== 'all') {
        if (f.status === 'open' ? !isOpen(l.status) : f.status === 'won' ? !isWon(l.status) : l.status !== f.status) return false;
      }
      if (f.source && f.source !== 'all' && l.source !== f.source) return false;
      if (f.owner && f.owner !== 'all' && l.ownerId !== f.owner) return false;
      if (f.interest && f.interest !== 'all' && l.interest !== f.interest) return false;
      if (q && ![l.studentName, l.parentName, l.phone, l.city, l.campaign, l.id].some((v) => v.toLowerCase().includes(q))) return false;
      return true;
    })
    .sort((a, b) => b.createdUtc.localeCompare(a.createdUtc));
}

export function getLead(id: string): Lead | undefined {
  const l = listLeadsRaw().find((x) => x.id === id);
  return l && { ...l, parentName: displayParent(l) };
}
export const getLeadActivities = (leadId: string) => listActivities().filter((a) => a.leadId === leadId).sort((a, b) => b.atUtc.localeCompare(a.atUtc));
export const getLeadPayments = (leadId: string) => listPayments().filter((p) => p.leadId === leadId).sort((a, b) => b.createdUtc.localeCompare(a.createdUtc));
export const getLeadFollowUps = (leadId: string) => listFollowUps().filter((f) => f.leadId === leadId).sort((a, b) => a.dueUtc.localeCompare(b.dueUtc));
export const getConversion = (leadId: string) => listConversions().find((c) => c.leadId === leadId);
export const getPayment = (id: string) => listPayments().find((p) => p.id === id);

export const isWon = (s: LeadStatus) => s === 'closed_won' || s === 'converted';
export const isOpen = (s: LeadStatus) => !isWon(s) && s !== 'closed_lost' && s !== 'nurture';

// ------------------------------------------------------------------ time helpers (IST)
const IST = 5.5 * 3_600_000;
export const istDate = (iso: string) => new Date(Date.parse(iso) + IST).toISOString().slice(0, 10);
export const todayIst = () => istDate(DEMO_NOW_ISO);
export const monthIst = (iso: string) => istDate(iso).slice(0, 7);

export type FollowUpState = 'overdue' | 'today' | 'upcoming' | 'done' | 'skipped';
export function followUpState(f: FollowUp): FollowUpState {
  if (f.status === 'done') return 'done';
  if (f.status === 'skipped') return 'skipped';
  const now = Date.parse(DEMO_NOW_ISO);
  const d = istDate(f.dueUtc);
  if (d === todayIst()) return 'today';
  return Date.parse(f.dueUtc) < now ? 'overdue' : 'upcoming';
}

// ------------------------------------------------------------------ dashboard
export interface FunnelStep { status: LeadStatus; reached: number; current: number; rateFromPrev?: number }

/** Leads that ever reached each funnel stage (from stage activities), and how many sit there now. */
export function funnel(leads = listLeadsRaw()): FunnelStep[] {
  const reached = new Map<string, Set<LeadStatus>>();
  for (const l of leads) reached.set(l.id, new Set<LeadStatus>(['new']));
  for (const a of listActivities()) if (a.type === 'stage' && a.to) reached.get(a.leadId)?.add(a.to === 'converted' ? 'closed_won' : a.to);
  for (const l of leads) {
    const set = reached.get(l.id)!;
    set.add(l.status === 'converted' ? 'closed_won' : l.status);
    // Reaching a later stage implies the earlier ones (e.g. a lead that skipped Negotiation).
    const top = Math.max(...[...set].map((s) => FUNNEL.indexOf(s)));
    for (let i = 0; i <= top; i++) if (FUNNEL[i] !== 'negotiation') set.add(FUNNEL[i]!);
  }
  return FUNNEL.map((status, i) => {
    const n = leads.filter((l) => reached.get(l.id)!.has(status)).length;
    const prev = i === 0 ? undefined : FUNNEL[status === 'closed_won' ? i - 2 : i - 1]!;
    const prevN = prev ? leads.filter((l) => reached.get(l.id)!.has(prev)).length : undefined;
    return {
      status, reached: n,
      current: leads.filter((l) => (status === 'closed_won' ? isWon(l.status) : l.status === status)).length,
      rateFromPrev: prevN ? n / prevN : undefined,
    };
  });
}

export function revenueByMonth(month: string, payments = listPayments()) {
  const paid = payments.filter((p) => p.status === 'paid' && p.paidUtc && monthIst(p.paidUtc) === month);
  return { amountInr: paid.reduce((s, p) => s + p.amountInr, 0), totalInr: paid.reduce((s, p) => s + p.totalInr, 0), count: paid.length };
}

export function prevMonth(month: string) {
  const [y, m] = month.split('-').map(Number) as [number, number];
  return m === 1 ? `${y - 1}-12` : `${y}-${String(m - 1).padStart(2, '0')}`;
}

export function sourceStats(leads = listLeadsRaw()) {
  return SOURCES.map((s: LeadSource) => {
    const ls = leads.filter((l) => l.source === s);
    const won = ls.filter((l) => isWon(l.status));
    return { source: s, leads: ls.length, won: won.length, rate: ls.length ? won.length / ls.length : 0 };
  }).sort((a, b) => b.leads - a.leads);
}

export function leaderboard(month: string) {
  const leads = listLeadsRaw();
  const pays = listPayments();
  return listTeam().map((m) => {
    const mine = leads.filter((l) => l.ownerId === m.id);
    const paid = pays.filter((p) => p.status === 'paid' && p.paidUtc && monthIst(p.paidUtc) === month && mine.some((l) => l.id === p.leadId));
    const revenue = paid.reduce((s, p) => s + p.amountInr, 0);
    return {
      member: m, won: paid.length, revenueInr: revenue, targetPct: m.monthlyTargetInr ? revenue / m.monthlyTargetInr : 0,
      open: mine.filter((l) => isOpen(l.status)).length,
      pipelineInr: mine.filter((l) => isOpen(l.status)).reduce((s, l) => s + l.valueInr, 0),
    };
  }).sort((a, b) => b.revenueInr - a.revenueInr || b.won - a.won);
}

/** Fill a template's placeholders for one lead. */
export function renderTemplate(t: Template, lead: Lead, extra: Record<string, string> = {}): string {
  const p = getPackage(lead.packageId);
  const pay = getLeadPayments(lead.id)[0];
  const fmt = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 });
  const vals: Record<string, string> = {
    parent: lead.parentName.split(' ')[0]!, student: lead.studentName.split(' ')[0]!, rep: repName(lead.ownerId).split(' ')[0]!, lead: lead.id.slice(5),
    demo: lead.demoUtc ? new Date(lead.demoUtc).toLocaleString('en-IN', { timeZone: 'Asia/Kolkata', weekday: 'short', day: 'numeric', month: 'short', hour: 'numeric', minute: '2-digit' }) : 'your chosen slot',
    package: p?.name ?? 'the plan', price: p ? fmt.format(p.priceInr) : '', total: pay ? fmt.format(pay.totalInr) : p ? fmt.format(p.priceInr + gstFor(p.priceInr)) : '',
    link: pay?.link ?? '', invoice: pay?.invoiceNo ?? '', ...extra,
  };
  return t.body.replace(/\{(\w+)\}/g, (_, k: string) => vals[k] ?? `{${k}}`);
}
