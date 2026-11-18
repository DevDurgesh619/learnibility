/**
 * W3-CRM record types. Pure types (no server imports) so the generator script and client components can share them.
 * Files: data/crm/{leads,activities,followups,payments,conversions,team,packages,templates,rules}.json,
 * each `{ schemaVersion, generatedBy, items }`, built by `npx tsx scripts/crm/build.ts`.
 */
import type { Board, Grade } from '@/lib/types';
import type { PlanId } from '@/lib/data/types';

export const LEAD_STATUSES = [
  'new', 'contacted', 'qualified', 'demo_booked', 'demo_done', 'proposal_sent', 'negotiation', 'closed_won', 'converted', 'closed_lost', 'nurture',
] as const;
export type LeadStatus = (typeof LEAD_STATUSES)[number];

/** The forward funnel, in order (Converted follows Closed won once the family is handed over). */
export const FUNNEL: LeadStatus[] = ['new', 'contacted', 'qualified', 'demo_booked', 'demo_done', 'proposal_sent', 'negotiation', 'closed_won'];

export const STATUS_LABEL: Record<LeadStatus, string> = {
  new: 'New', contacted: 'Contacted', qualified: 'Qualified', demo_booked: 'Demo booked', demo_done: 'Demo done',
  proposal_sent: 'Proposal sent', negotiation: 'Negotiation', closed_won: 'Closed won', converted: 'Converted',
  closed_lost: 'Closed lost', nurture: 'Nurture',
};

export const SOURCES = ['website', 'google_ads', 'instagram', 'facebook', 'youtube', 'referral', 'school_partnership', 'webinar'] as const;
export type LeadSource = (typeof SOURCES)[number];
export const SOURCE_LABEL: Record<LeadSource, string> = {
  website: 'Website form', google_ads: 'Google Ads', instagram: 'Instagram', facebook: 'Facebook', youtube: 'YouTube',
  referral: 'Referral', school_partnership: 'School partnership', webinar: 'Webinar',
};

export const INTERESTS = ['academic_support', 'career_counselling', 'study_abroad', 'full_package'] as const;
export type LeadInterest = (typeof INTERESTS)[number];
export const INTEREST_LABEL: Record<LeadInterest, string> = {
  academic_support: 'Academic support', career_counselling: 'Career counselling', study_abroad: 'Study abroad', full_package: 'Full package',
};

export const LOST_REASONS = [
  'Price too high', 'Chose another provider', 'Not the right time', 'No response after 5 attempts', 'Wanted offline classes only', 'Student not interested',
] as const;

export interface Lead {
  id: string; // lead_0001
  studentName: string;
  parentName: string;
  phone: string;
  email: string;
  city: string;
  grade: Grade;
  board: Board;
  interest: LeadInterest;
  source: LeadSource;
  campaign: string;
  ownerId: string;
  score: number;
  status: LeadStatus;
  lostReason?: string;
  /** Package proposed or bought (data/crm/packages.json). */
  packageId?: string;
  /** Deal value before GST, integer rupees. */
  valueInr: number;
  createdUtc: string;
  lastContactedUtc?: string;
  stageChangedUtc: string;
  demoUtc?: string;
  /** Platform learners this family maps to (persona families, or created on conversion). */
  learnerIds?: string[];
  parentId?: string;
  /** Persona family leads carry the parent's real persona name; shown in place of parentName. */
  personaFamily?: boolean;
  notes?: string;
}

export type ActivityType = 'stage' | 'call' | 'whatsapp' | 'email' | 'demo' | 'note' | 'payment' | 'handoff' | 'assign' | 'import';

export interface Activity {
  id: string;
  leadId: string;
  type: ActivityType;
  atUtc: string;
  /** Rep who did it, or 'system' for automation. */
  byId: string;
  title: string;
  body?: string;
  from?: LeadStatus;
  to?: LeadStatus;
  outcome?: 'connected' | 'no_answer' | 'busy' | 'call_back' | 'wrong_number';
  durationMin?: number;
  templateId?: string;
  ruleId?: string;
  auto?: boolean;
}

export interface FollowUp {
  id: string;
  leadId: string;
  ruleId: string;
  channel: 'whatsapp' | 'call' | 'email';
  title: string;
  dueUtc: string;
  status: 'open' | 'done' | 'skipped';
  doneUtc?: string;
  ownerId: string;
}

export interface Payment {
  id: string;
  leadId: string;
  packageId: string;
  amountInr: number;
  gstInr: number;
  totalInr: number;
  link: string;
  status: 'pending' | 'paid' | 'failed';
  createdUtc: string;
  paidUtc?: string;
  failedUtc?: string;
  method?: 'UPI' | 'Card' | 'Net banking';
  invoiceNo?: string;
  receiptNo?: string;
}

export interface Conversion {
  id: string; // conv_{leadId}
  leadId: string;
  status: 'waiting' | 'handed_over';
  wonUtc: string;
  handedOverUtc?: string;
  learnerIds: string[];
  parentId?: string;
  counsellorId: string;
  planId: PlanId;
  subscriptionId?: string;
  invoiceId?: string;
}

export interface Subscription {
  id: string;
  learnerId: string;
  parentId?: string;
  planId: PlanId;
  packageId: string;
  startUtc: string;
  endUtc?: string;
  status: 'active';
  leadId: string;
}

export interface TeamMember {
  id: string;
  name: string;
  title: string;
  personaId?: string;
  manager?: boolean;
  monthlyTargetInr: number;
}

export interface CrmPackage {
  id: string;
  name: string;
  /** Platform plan the family gets on conversion. */
  planId: PlanId;
  /** Months of the plan (0 = one-off). */
  months: number;
  priceInr: number;
  blurb: string;
  interests: LeadInterest[];
}

export interface Template {
  id: string;
  name: string;
  channel: 'whatsapp' | 'email';
  body: string;
}

export interface FollowUpRule {
  id: string;
  name: string;
  trigger: string;
  action: string;
  channel: FollowUp['channel'];
}

export const GST_RATE = 0.18;
